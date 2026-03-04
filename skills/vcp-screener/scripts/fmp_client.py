#!/usr/bin/env python3
"""
FMP API Client for VCP Screener

Provides rate-limited access to Financial Modeling Prep stable API endpoints
for VCP (Volatility Contraction Pattern) screening.

Features:
- Rate limiting (0.3s between requests)
- Automatic retry on 429 errors
- Session caching for duplicate requests
- Batch quote support
- S&P 500 constituents fetching
"""

import os
import sys
import time
from datetime import datetime, timedelta
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import yfinance as yf

    HAS_YFINANCE = True
except ImportError:
    yf = None  # type: ignore[assignment]
    HAS_YFINANCE = False


class FMPClient:
    """Client for Financial Modeling Prep stable API with rate limiting and caching"""

    STABLE_URL = "https://financialmodelingprep.com/stable"
    RATE_LIMIT_DELAY = 0.3  # 300ms between requests

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("FMP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "FMP API key required. Set FMP_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.session = requests.Session()
        self.cache = {}
        self.last_call_time = 0
        self.rate_limit_reached = False
        self.retry_count = 0
        self.max_retries = 1
        self.api_calls_made = 0
        self.yf_fallback_count = 0

    def _is_error_payload(self, data) -> bool:
        """Detect FMP API error responses returned with HTTP 200."""
        if isinstance(data, dict):
            if "Error Message" in data or "Error" in data:
                msg = data.get("Error Message") or data.get("Error", "")
                print(f"WARNING: FMP API error in 200 response: {msg}", file=sys.stderr)
                return True
        return False

    def _rate_limited_get(self, url: str, params: Optional[dict] = None) -> Optional[dict]:
        if self.rate_limit_reached:
            return None

        if params is None:
            params = {}
        params["apikey"] = self.api_key

        elapsed = time.time() - self.last_call_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)

        try:
            response = self.session.get(url, params=params, timeout=30)
            self.last_call_time = time.time()
            self.api_calls_made += 1

            if response.status_code == 200:
                self.retry_count = 0
                try:
                    data = response.json()
                except (ValueError, Exception):
                    print(
                        f"WARNING: Failed to parse JSON response: {response.text[:200]}",
                        file=sys.stderr,
                    )
                    return None
                if self._is_error_payload(data):
                    return None
                return data
            elif response.status_code == 429:
                self.retry_count += 1
                if self.retry_count <= self.max_retries:
                    print("WARNING: Rate limit exceeded. Waiting 60 seconds...", file=sys.stderr)
                    time.sleep(60)
                    return self._rate_limited_get(url, params)
                else:
                    print("ERROR: Daily API rate limit reached.", file=sys.stderr)
                    self.rate_limit_reached = True
                    return None
            else:
                print(
                    f"ERROR: API request failed: {response.status_code} - {response.text[:200]}",
                    file=sys.stderr,
                )
                return None
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request exception: {e}", file=sys.stderr)
            return None

    def _fetch_via_yfinance(self, symbol: str, days: int) -> Optional[list[dict]]:
        """Fetch historical data via yfinance as fallback."""
        if not HAS_YFINANCE or yf is None:
            return None

        try:
            import pandas as pd

            df = yf.download(symbol, period=f"{days}d", auto_adjust=False, progress=False)

            if df is None or df.empty:
                return None

            if isinstance(df.columns, pd.MultiIndex):
                df = df.droplevel(level=1, axis=1)

            records = []
            for idx, row in df.iterrows():
                records.append(
                    {
                        "date": idx.strftime("%Y-%m-%d"),
                        "open": float(row["Open"]),
                        "high": float(row["High"]),
                        "low": float(row["Low"]),
                        "close": float(row["Close"]),
                        "adjClose": float(row["Adj Close"]),
                        "volume": int(row["Volume"]),
                    }
                )

            records.sort(key=lambda x: x["date"], reverse=True)
            return records
        except Exception as e:
            print(f"WARNING: yfinance fallback failed for {symbol}: {e}", file=sys.stderr)
            return None

    def _fetch_quote_via_yfinance(self, symbol: str) -> Optional[list[dict]]:
        """Fetch quote data via yfinance as fallback."""
        if not HAS_YFINANCE or yf is None:
            return None

        try:
            ticker = yf.Ticker(symbol)
            info = ticker.fast_info
            quote = {
                "symbol": symbol,
                "price": float(info["last_price"]),
                "yearHigh": float(info["year_high"]),
                "yearLow": float(info["year_low"]),
                "volume": int(info["last_volume"]),
            }
            return [quote]
        except Exception as e:
            print(f"WARNING: yfinance quote fallback failed for {symbol}: {e}", file=sys.stderr)
            return None

    def get_sp500_constituents(self) -> Optional[list[dict]]:
        """Fetch S&P 500 constituent list via stable endpoint.

        Returns:
            List of dicts with keys: symbol, name, sector, subSector
            or None on failure.
        """
        cache_key = "sp500_constituents"
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.STABLE_URL}/sp500-constituent"
        data = self._rate_limited_get(url)
        if data:
            self.cache[cache_key] = data
        return data

    def get_quote(self, symbols: str) -> Optional[list[dict]]:
        """Fetch real-time quote data for one or more symbols via stable endpoint.

        Falls back to yfinance when FMP returns no data.
        """
        cache_key = f"quote_{symbols}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.STABLE_URL}/quote"
        data = self._rate_limited_get(url, params={"symbol": symbols})
        if data and isinstance(data, list) and data and isinstance(data[0], dict):
            self.cache[cache_key] = data
            return data

        # FMP failed — try yfinance fallback
        if HAS_YFINANCE:
            print(
                f"FMP unavailable for {symbols}, using yfinance quote fallback...",
                file=sys.stderr,
            )
            yf_data = self._fetch_quote_via_yfinance(symbols)
            if yf_data:
                self.yf_fallback_count += 1
                self.cache[cache_key] = yf_data
                return yf_data

        return None

    def get_historical_prices(self, symbol: str, days: int = 365) -> Optional[dict]:
        """Fetch historical daily OHLCV data via stable endpoint.

        Falls back to yfinance when FMP returns no data.
        Returns data wrapped in {"symbol": ..., "historical": [...]} format.
        """
        cache_key = f"prices_{symbol}_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        url = f"{self.STABLE_URL}/historical-price-eod/full"
        params = {"symbol": symbol, "from": from_date}
        data = self._rate_limited_get(url, params)
        if data and isinstance(data, list):
            wrapped = {"symbol": symbol, "historical": data}
            self.cache[cache_key] = wrapped
            return wrapped

        # FMP failed — try yfinance fallback
        if HAS_YFINANCE:
            print(
                f"FMP unavailable for {symbol}, using yfinance fallback...",
                file=sys.stderr,
            )
            yf_data = self._fetch_via_yfinance(symbol, days)
            if yf_data:
                self.yf_fallback_count += 1
                wrapped = {"symbol": symbol, "historical": yf_data}
                self.cache[cache_key] = wrapped
                return wrapped

        return None

    def get_batch_quotes(self, symbols: list[str]) -> dict[str, dict]:
        """Fetch quotes for a list of symbols via stable endpoint (one per request)"""
        results = {}
        # Stable API doesn't support multi-symbol on all plans
        batch_size = 1
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i : i + batch_size]
            batch_str = ",".join(batch)
            quotes = self.get_quote(batch_str)
            if quotes:
                for q in quotes:
                    results[q["symbol"]] = q
        return results

    def get_batch_historical(self, symbols: list[str], days: int = 260) -> dict[str, list[dict]]:
        """Fetch historical prices for multiple symbols"""
        results = {}
        for symbol in symbols:
            data = self.get_historical_prices(symbol, days=days)
            if data and "historical" in data:
                results[symbol] = data["historical"]
        return results

    def calculate_sma(self, prices: list[float], period: int) -> float:
        """Calculate Simple Moving Average from a list of prices (most recent first)"""
        if len(prices) < period:
            return sum(prices) / len(prices)
        return sum(prices[:period]) / period

    def get_api_stats(self) -> dict:
        return {
            "cache_entries": len(self.cache),
            "api_calls_made": self.api_calls_made,
            "rate_limit_reached": self.rate_limit_reached,
            "yf_fallback_count": self.yf_fallback_count,
        }
