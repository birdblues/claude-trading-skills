#!/usr/bin/env python3
"""
FMP API Client for VCP Screener

Provides rate-limited access to Financial Modeling Prep API endpoints
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
from typing import Optional

try:
    import requests
except ImportError:
    print("ERROR: requests library not found. Install with: pip install requests", file=sys.stderr)
    sys.exit(1)

try:
    import pandas as pd
except ImportError:
    pd = None

try:
    import yfinance as yf

    HAS_YFINANCE = True
except ImportError:
    yf = None
    HAS_YFINANCE = False


class FMPClient:
    """Client for Financial Modeling Prep API with rate limiting and caching"""

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
        self.wiki_fallback_count = 0

    def _is_error_payload(self, data) -> bool:
        """Detect FMP error responses returned with HTTP 200."""
        if isinstance(data, dict) and ("Error Message" in data or "Error" in data):
            print(f"WARNING: FMP error payload detected: {data}", file=sys.stderr)
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
                    return response.json()
                except ValueError:
                    print("WARNING: Failed to decode JSON response", file=sys.stderr)
                    return None
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
            avg_vol = (
                info.get("threeMonthAverageVolume")
                or info.get("tenDayAverageVolume")
                or info.get("lastVolume")
                or 0
            )
            quote = {
                "symbol": symbol,
                "price": float(info["last_price"]),
                "yearHigh": float(info["year_high"]),
                "yearLow": float(info["year_low"]),
                "volume": int(info["last_volume"]),
                "avgVolume": int(avg_vol),
            }
            return [quote]
        except Exception as e:
            print(f"WARNING: yfinance quote fallback failed for {symbol}: {e}", file=sys.stderr)
            return None

    def _fetch_sp500_from_wikipedia(self) -> Optional[list[dict]]:
        """Fetch S&P 500 constituents from Wikipedia as fallback."""
        if pd is None:
            return None

        try:
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            resp = requests.get(
                url,
                headers={"User-Agent": "VCPScreener/1.0 (stock screener tool)"},
                timeout=30,
            )
            resp.raise_for_status()
            from io import StringIO

            tables = pd.read_html(StringIO(resp.text))
            if not tables:
                return None

            df = tables[0]
            records = []
            for _, row in df.iterrows():
                symbol = str(row.get("Symbol", "")).strip().replace(".", "-")
                records.append(
                    {
                        "symbol": symbol,
                        "name": str(row.get("Security", "")),
                        "sector": str(row.get("GICS Sector", "")),
                        "subSector": str(row.get("GICS Sub-Industry", "")),
                    }
                )
            return records if records else None
        except Exception as e:
            print(f"WARNING: Wikipedia S&P 500 fallback failed: {e}", file=sys.stderr)
            return None

    def get_sp500_constituents(self) -> Optional[list[dict]]:
        """Fetch S&P 500 constituent list.

        Returns:
            List of dicts with keys: symbol, name, sector, subSector
            or None on failure.
        """
        cache_key = "sp500_constituents"
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.STABLE_URL}/sp500-constituent"
        data = self._rate_limited_get(url)
        if data and not self._is_error_payload(data):
            self.cache[cache_key] = data
            return data

        # Fallback to Wikipedia
        wiki_data = self._fetch_sp500_from_wikipedia()
        if wiki_data:
            self.wiki_fallback_count += 1
            self.cache[cache_key] = wiki_data
        return wiki_data

    def get_quote(self, symbols: str) -> Optional[list[dict]]:
        """Fetch real-time quote data for one or more symbols (comma-separated)"""
        cache_key = f"quote_{symbols}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.STABLE_URL}/quote"
        data = self._rate_limited_get(url, {"symbol": symbols})
        if data and not self._is_error_payload(data) and isinstance(data, list) and len(data) > 0:
            self.cache[cache_key] = data
            return data

        # Fallback to yfinance for single symbol
        yf_data = self._fetch_quote_via_yfinance(symbols)
        if yf_data:
            self.yf_fallback_count += 1
            self.cache[cache_key] = yf_data
        return yf_data

    def get_historical_prices(self, symbol: str, days: int = 365) -> Optional[dict]:
        """Fetch historical daily OHLCV data"""
        cache_key = f"prices_{symbol}_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.STABLE_URL}/historical-price-eod/full"
        params = {"symbol": symbol}
        data = self._rate_limited_get(url, params)

        need_fallback = data is None or data == [] or self._is_error_payload(data)

        if not need_fallback:
            if isinstance(data, list):
                result = {"symbol": symbol, "historical": data[:days]}
            elif isinstance(data, dict) and "historical" in data:
                data["historical"] = data["historical"][:days]
                result = data
            else:
                result = data
            self.cache[cache_key] = result
            return result

        # Fallback to yfinance
        yf_data = self._fetch_via_yfinance(symbol, days)
        if yf_data:
            self.yf_fallback_count += 1
            result = {"symbol": symbol, "historical": yf_data}
            self.cache[cache_key] = result
            return result
        return None

    def get_batch_quotes(self, symbols: list[str]) -> dict[str, dict]:
        """Fetch quotes for a list of symbols, batching up to 5 per request"""
        results = {}
        batch_size = 5
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
            "wiki_fallback_count": self.wiki_fallback_count,
        }
