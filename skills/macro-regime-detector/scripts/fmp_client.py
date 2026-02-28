#!/usr/bin/env python3
"""
FMP API Client for Macro Regime Detector

Provides rate-limited access to Financial Modeling Prep API endpoints
for macro regime detection analysis.

Features:
- Rate limiting (0.3s between requests)
- Automatic retry on 429 errors
- Session caching for duplicate requests
- Batch historical data support
- Treasury rates endpoint support
- yfinance fallback for ETFs unsupported by FMP Starter plans
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
    """Client for Financial Modeling Prep API with rate limiting and caching"""

    BASE_URL = "https://financialmodelingprep.com/api/v3"
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
                return response.json()
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
        """Fetch historical data via yfinance as fallback.

        Converts yfinance DataFrame to FMP-compatible list-of-dicts format.
        Handles both single-level and multi-level column DataFrames.

        Returns:
            List of dicts sorted most-recent-first, or None on failure.
        """
        if not HAS_YFINANCE or yf is None:
            return None

        try:
            import pandas as pd

            df = yf.download(symbol, period=f"{days}d", auto_adjust=False, progress=False)

            if df is None or df.empty:
                return None

            # Handle MultiIndex columns (yfinance 0.2.31+ default)
            if isinstance(df.columns, pd.MultiIndex):
                df = df.droplevel(level=1, axis=1)

            # Map yfinance columns to FMP-compatible keys
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

            # Sort most-recent-first (FMP convention)
            records.sort(key=lambda x: x["date"], reverse=True)
            return records
        except Exception as e:
            print(f"WARNING: yfinance fallback failed for {symbol}: {e}", file=sys.stderr)
            return None

    def get_historical_prices(self, symbol: str, days: int = 600) -> Optional[dict]:
        """Fetch historical daily OHLCV data using stable endpoint.

        Uses /stable/historical-price-eod/full (the legacy /api/v3/historical-price-full
        endpoint was deprecated for subscriptions after August 31, 2025).

        Falls back to yfinance when FMP returns no data (e.g., 402 Premium
        errors for ETFs on Starter plans).

        Returns data wrapped in {"symbol": ..., "historical": [...]} format
        for backward compatibility with existing calculators.
        """
        cache_key = f"prices_{symbol}_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        url = f"{self.STABLE_URL}/historical-price-eod/full"
        params = {"symbol": symbol, "from": from_date}
        data = self._rate_limited_get(url, params)
        if data and isinstance(data, list):
            # Wrap in legacy format for backward compatibility
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

    def get_batch_historical(self, symbols: list[str], days: int = 600) -> dict[str, list[dict]]:
        """Fetch historical prices for multiple symbols"""
        results = {}
        for symbol in symbols:
            data = self.get_historical_prices(symbol, days=days)
            if data and "historical" in data:
                results[symbol] = data["historical"]
        return results

    def get_treasury_rates(self, days: int = 600) -> Optional[list[dict]]:
        """
        Fetch treasury rate data from FMP stable endpoint.

        Returns list of dicts with keys like 'date', 'year2', 'year10', etc.
        Most recent first.
        """
        cache_key = f"treasury_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.STABLE_URL}/treasury-rates"
        params = {"limit": days}
        data = self._rate_limited_get(url, params)
        if data and isinstance(data, list):
            self.cache[cache_key] = data
            return data
        return None

    def get_api_stats(self) -> dict:
        return {
            "cache_entries": len(self.cache),
            "api_calls_made": self.api_calls_made,
            "rate_limit_reached": self.rate_limit_reached,
            "yf_fallback_count": self.yf_fallback_count,
        }
