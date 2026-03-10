#!/usr/bin/env python3
"""FMP API client for Trump Pain Index market data.

Fetches real-time/recent price data for Pain Index domains:
    - USO (WTI proxy) → Energy domain
    - ^GSPC (S&P 500) → Stock Market domain (drawdown from ATH)
    - TLT (20Y Treasury) → Interest Rates proxy
    - ^VIX (VIX) → supplementary volatility data

Uses FMP stable API with rate limiting, caching, and env-var-first key resolution.
"""

import os
import sys
import time
from typing import Optional

try:
    import requests
except ImportError:
    print(
        "ERROR: requests library not found. Install with: pip install requests",
        file=sys.stderr,
    )
    sys.exit(1)


class FMPClient:
    """Client for Financial Modeling Prep stable API."""

    STABLE_URL = "https://financialmodelingprep.com/stable"
    RATE_LIMIT_DELAY = 0.3  # 300ms between requests

    # Symbols for Pain Index domains
    SYMBOLS = {
        "energy": "USO",  # WTI crude proxy
        "stock_market": "^GSPC",  # S&P 500
        "interest_rates": "TLT",  # 20Y Treasury bond
        "vix": "^VIX",  # Volatility index
    }

    def __init__(self, api_key: Optional[str] = None, max_api_calls: int = 50):
        self.api_key = api_key or os.getenv("FMP_API_KEY")
        if not self.api_key:
            raise ValueError(
                "FMP API key required. Set FMP_API_KEY environment variable "
                "or pass api_key parameter."
            )
        self.session = requests.Session()
        self.cache: dict = {}
        self.last_call_time = 0.0
        self.api_calls_made = 0
        self.max_api_calls = max_api_calls

    def _rate_limited_get(self, url: str, params: Optional[dict] = None) -> Optional[dict | list]:
        """Execute a rate-limited GET request."""
        if self.api_calls_made >= self.max_api_calls:
            print(
                f"WARNING: API call budget ({self.max_api_calls}) exhausted.",
                file=sys.stderr,
            )
            return None

        elapsed = time.time() - self.last_call_time
        if elapsed < self.RATE_LIMIT_DELAY:
            time.sleep(self.RATE_LIMIT_DELAY - elapsed)

        if params is None:
            params = {}
        params["apikey"] = self.api_key

        try:
            response = self.session.get(url, params=params, timeout=30)
            self.last_call_time = time.time()
            self.api_calls_made += 1

            if response.status_code == 200:
                try:
                    data = response.json()
                except ValueError:
                    print(
                        f"WARNING: Failed to parse JSON: {response.text[:200]}",
                        file=sys.stderr,
                    )
                    return None
                if isinstance(data, dict) and ("Error Message" in data or "Error" in data):
                    msg = data.get("Error Message") or data.get("Error", "")
                    print(f"WARNING: FMP API error: {msg}", file=sys.stderr)
                    return None
                return data
            elif response.status_code == 429:
                print("WARNING: Rate limit exceeded. Waiting 60s...", file=sys.stderr)
                time.sleep(60)
                return self._rate_limited_get(url, params)
            else:
                print(
                    f"ERROR: API request failed: {response.status_code} - {response.text[:200]}",
                    file=sys.stderr,
                )
                return None
        except requests.exceptions.Timeout:
            print(f"WARNING: Request timed out for {url}", file=sys.stderr)
            return None
        except requests.exceptions.RequestException as e:
            print(f"ERROR: Request exception: {e}", file=sys.stderr)
            return None

    def get_quote(self, symbol: str) -> Optional[dict]:
        """Fetch real-time quote for a symbol.

        Returns:
            Dict with price, changesPercentage, dayHigh, dayLow, etc.
        """
        cache_key = f"quote_{symbol}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.STABLE_URL}/quote"
        data = self._rate_limited_get(url, {"symbol": symbol})
        if data and isinstance(data, list) and len(data) > 0:
            self.cache[cache_key] = data[0]
            return data[0]
        return None

    def get_historical_prices(self, symbol: str, days: int = 252) -> Optional[list]:
        """Fetch historical daily prices.

        Args:
            symbol: Ticker symbol.
            days: Number of trading days to fetch.

        Returns:
            List of dicts with date, open, high, low, close, volume.
        """
        cache_key = f"hist_{symbol}_{days}"
        if cache_key in self.cache:
            return self.cache[cache_key]

        url = f"{self.STABLE_URL}/historical-price-eod/full"
        data = self._rate_limited_get(url, {"symbol": symbol})
        if data and isinstance(data, dict) and "historical" in data:
            records = data["historical"][:days]
            self.cache[cache_key] = records
            return records
        elif data and isinstance(data, list):
            records = data[:days]
            self.cache[cache_key] = records
            return records
        return None

    def fetch_pain_domain_data(self) -> dict:
        """Fetch all Pain Index market data in one call.

        Returns:
            Dict with domain keys and their market data:
                - energy: {"price": USO price, "wti_estimate": approximate WTI}
                - stock_market: {"price": SPX, "ath": 52w high, "drawdown_pct": %}
                - interest_rates: {"tlt_price": TLT, "yield_estimate": approx 10Y}
                - vix: {"price": VIX level}
        """
        result = {}

        # Energy (USO → WTI estimate)
        uso_quote = self.get_quote(self.SYMBOLS["energy"])
        if uso_quote:
            uso_price = uso_quote.get("price", 0)
            # USO roughly tracks WTI; approximate conversion
            wti_estimate = uso_price * 1.1  # Rough proxy
            result["energy"] = {
                "price": uso_price,
                "wti_estimate": round(wti_estimate, 2),
                "symbol": "USO",
            }

        # Stock Market (^GSPC)
        spx_quote = self.get_quote(self.SYMBOLS["stock_market"])
        if spx_quote:
            spx_price = spx_quote.get("price", 0)
            spx_high = spx_quote.get("yearHigh", spx_price)
            drawdown = ((spx_high - spx_price) / spx_high * 100) if spx_high > 0 else 0
            result["stock_market"] = {
                "price": spx_price,
                "year_high": spx_high,
                "drawdown_pct": round(drawdown, 2),
                "symbol": "^GSPC",
            }

        # Interest Rates (TLT → yield estimate)
        tlt_quote = self.get_quote(self.SYMBOLS["interest_rates"])
        if tlt_quote:
            tlt_price = tlt_quote.get("price", 0)
            # TLT inverse relationship with yields; rough estimate
            # TLT ~90 ≈ 4.5%, TLT ~80 ≈ 5.0%, TLT ~100 ≈ 4.0%
            yield_estimate = max(0, 8.5 - tlt_price * 0.045) if tlt_price > 0 else 4.5
            result["interest_rates"] = {
                "tlt_price": tlt_price,
                "yield_estimate": round(yield_estimate, 2),
                "symbol": "TLT",
            }

        # VIX (supplementary)
        vix_quote = self.get_quote(self.SYMBOLS["vix"])
        if vix_quote:
            result["vix"] = {
                "price": vix_quote.get("price", 0),
                "symbol": "^VIX",
            }

        return result
