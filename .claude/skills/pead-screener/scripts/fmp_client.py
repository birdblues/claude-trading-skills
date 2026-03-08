#!/usr/bin/env python3
"""
FMP API Client for PEAD Screener

Provides rate-limited access to Financial Modeling Prep API endpoints
for PEAD (Post-Earnings Announcement Drift) screening.

Features:
- Rate limiting (0.3s between requests)
- Automatic retry on 429 errors
- Session caching for duplicate requests
- API call budget enforcement
- Batch company profile support
- Earnings calendar and historical price fetching
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


class ApiCallBudgetExceeded(Exception):
    """Raised when the API call budget has been exhausted."""

    pass


class FMPClient:
    """Client for Financial Modeling Prep API with rate limiting, caching, and budget control"""

    STABLE_URL = "https://financialmodelingprep.com/stable"
    RATE_LIMIT_DELAY = 0.3  # 300ms between requests

    def __init__(self, api_key: Optional[str] = None, max_api_calls: int = 200):
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
        self.max_api_calls = max_api_calls
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
        """Make a rate-limited GET request with budget enforcement.

        Raises:
            ApiCallBudgetExceeded: When api_calls_made >= max_api_calls
        """
        if self.api_calls_made >= self.max_api_calls:
            raise ApiCallBudgetExceeded(
                f"API call budget exhausted: {self.api_calls_made}/{self.max_api_calls} calls used"
            )

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
        except requests.exceptions.Timeout:
            print("ERROR: Request timed out", file=sys.stderr)
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

    def get_earnings_calendar(self, from_date: str, to_date: str) -> Optional[list[dict]]:
        """Fetch earnings calendar for a date range.

        Args:
            from_date: Start date in YYYY-MM-DD format
            to_date: End date in YYYY-MM-DD format

        Returns:
            List of earnings event dicts or None on failure.
            Each dict contains: date, symbol, eps, epsEstimated, revenue,
            revenueEstimated, time (bmo/amc)
        """
        cache_key = f"earnings_{from_date}_{to_date}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.STABLE_URL}/earnings-calendar"
        params = {"from": from_date, "to": to_date}
        data = self._rate_limited_get(url, params)
        if data:
            self.cache[cache_key] = data
        return data

    def get_company_profiles(self, symbols: list[str]) -> dict[str, dict]:
        """Fetch company profiles for multiple symbols one at a time.

        Args:
            symbols: List of stock symbols

        Returns:
            Dict mapping symbol -> profile dict (with marketCap, sector, etc.)
        """
        results = {}
        batch_size = 1
        for i in range(0, len(symbols), batch_size):
            batch = symbols[i : i + batch_size]
            batch_str = ",".join(batch)

            cache_key = f"profile_{batch_str}"
            if cache_key in self.cache:
                for profile in self.cache[cache_key]:
                    results[profile["symbol"]] = profile
                continue

            url = f"{self.STABLE_URL}/profile"
            data = self._rate_limited_get(url, params={"symbol": batch_str})
            if data:
                self.cache[cache_key] = data
                for profile in data:
                    results[profile["symbol"]] = profile
        return results

    def get_historical_prices(self, symbol: str, days: int = 90) -> Optional[list[dict]]:
        """Fetch historical daily OHLCV data.

        Falls back to yfinance when FMP returns no data.

        Args:
            symbol: Stock symbol
            days: Number of trading days to fetch

        Returns:
            List of price dicts (most-recent-first) with: date, open, high, low,
            close, adjClose, volume. Returns None on failure.
        """
        cache_key = f"prices_{symbol}_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        url = f"{self.STABLE_URL}/historical-price-eod/full"
        params = {"symbol": symbol, "from": from_date}
        data = self._rate_limited_get(url, params)
        if data and isinstance(data, list):
            self.cache[cache_key] = data
            return data

        # FMP failed — try yfinance fallback
        if HAS_YFINANCE:
            print(
                f"FMP unavailable for {symbol}, using yfinance fallback...",
                file=sys.stderr,
            )
            yf_data = self._fetch_via_yfinance(symbol, days)
            if yf_data:
                self.yf_fallback_count += 1
                self.cache[cache_key] = yf_data
                return yf_data

        return None

    def get_api_stats(self) -> dict:
        """Return API usage statistics."""
        return {
            "cache_entries": len(self.cache),
            "api_calls_made": self.api_calls_made,
            "max_api_calls": self.max_api_calls,
            "rate_limit_reached": self.rate_limit_reached,
            "budget_remaining": max(0, self.max_api_calls - self.api_calls_made),
        }
