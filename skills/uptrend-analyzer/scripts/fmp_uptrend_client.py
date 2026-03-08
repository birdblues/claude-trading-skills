#!/usr/bin/env python3
"""
Uptrend Analyzer - FMP Self-Calculation Client

Alternative to CSV client: fetches S&P 500 constituent prices via FMP API,
computes Monty's 8-condition uptrend signals, and derives sector-level
ratios/10MA/slope/trend matching the UptrendDataFetcher output schema.

Covers S&P 500 (~503 stocks) vs Monty's ~2,800 stock universe.
Directional signals are similar but absolute values may differ.

Features:
- Disk cache with per-symbol JSON files (avoids re-fetching)
- Budget-aware fetching (respects max_api_calls)
- Wikipedia fallback for S&P 500 constituents + GICS sector mapping
- Pure-Python uptrend signal computation (8 conditions from uptrend_methodology.md)

Usage:
    from fmp_uptrend_client import FMPUptrendClient

    client = FMPUptrendClient(api_key="...", cache_dir=".uptrend_cache")
    all_timeseries, sector_summary, sector_latest = client.calculate_uptrend_data()
"""

import json
import os
import sys
import time
from datetime import datetime, timedelta
from pathlib import Path

try:
    import requests
except ImportError:
    print(
        "ERROR: requests library not found. Install with: pip install requests",
        file=sys.stderr,
    )
    sys.exit(1)

try:
    import pandas as pd

    HAS_PANDAS = True
except ImportError:
    pd = None  # type: ignore[assignment]
    HAS_PANDAS = False

# ---------------------------------------------------------------------------
# GICS -> Monty sector name mapping
# ---------------------------------------------------------------------------

GICS_TO_MONTY = {
    "Information Technology": "Technology",
    "Consumer Discretionary": "Consumer Cyclical",
    "Communication Services": "Communication Services",
    "Financials": "Financial",
    "Industrials": "Industrials",
    "Utilities": "Utilities",
    "Consumer Staples": "Consumer Defensive",
    "Health Care": "Healthcare",
    "Real Estate": "Real Estate",
    "Energy": "Energy",
    "Materials": "Basic Materials",
}

# Reverse: Monty display name -> worksheet key
DISPLAY_TO_WORKSHEET = {
    "Basic Materials": "sec_basicmaterials",
    "Communication Services": "sec_communicationservices",
    "Consumer Cyclical": "sec_consumercyclical",
    "Consumer Defensive": "sec_consumerdefensive",
    "Energy": "sec_energy",
    "Financial": "sec_financial",
    "Healthcare": "sec_healthcare",
    "Industrials": "sec_industrials",
    "Real Estate": "sec_realestate",
    "Technology": "sec_technology",
    "Utilities": "sec_utilities",
}

# Thresholds matching data_fetcher.py
OVERBOUGHT_THRESHOLD = 0.37
OVERSOLD_THRESHOLD = 0.097

# ---------------------------------------------------------------------------
# Disk cache helpers (duplicated from fmp_breadth_client for skill isolation)
# ---------------------------------------------------------------------------

_CONSTITUENTS_TTL_DAYS = 7
_PRICE_TTL_DAYS = 1


def _is_cache_stale(fetched_at_str, ttl_days):
    """Return True if cache entry is older than ttl_days."""
    try:
        fetched_at = datetime.fromisoformat(fetched_at_str)
    except (ValueError, TypeError):
        return True
    return (datetime.now() - fetched_at).total_seconds() > ttl_days * 86400


def _read_json(path):
    """Read JSON file, return None on any error."""
    try:
        with open(path) as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError):
        return None


def _write_json(path, data):
    """Write JSON file atomically (write to tmp then rename)."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    tmp = path + ".tmp"
    with open(tmp, "w") as f:
        json.dump(data, f, separators=(",", ":"))
    os.replace(tmp, path)


# ---------------------------------------------------------------------------
# FMP Uptrend Client
# ---------------------------------------------------------------------------

STABLE_URL = "https://financialmodelingprep.com/stable"
RATE_LIMIT_DELAY = 0.3
_HISTORY_CALENDAR_DAYS = 750  # ~500 trading days -> 252 warmup + ~250 signal days


class FMPUptrendClient:
    """Fetch S&P 500 prices and compute Monty-style uptrend data.

    Args:
        api_key: FMP API key (falls back to $FMP_API_KEY).
        cache_dir: Path to disk cache directory.
        max_api_calls: Maximum API calls per run (budget).
        min_coverage: Minimum fraction of symbols needed (0-1).
    """

    def __init__(
        self,
        api_key=None,
        cache_dir=".uptrend_cache",
        max_api_calls=245,
        min_coverage=0.8,
    ):
        self.api_key = api_key or os.getenv("FMP_API_KEY")
        if not self.api_key:
            raise ValueError("FMP API key required. Set FMP_API_KEY env var or pass --api-key.")
        self.cache_dir = cache_dir
        self.max_api_calls = max_api_calls
        self.min_coverage = min_coverage

        self.session = requests.Session()
        self._last_call_time = 0.0
        self.api_calls_made = 0
        self._rate_limit_reached = False

    # ------------------------------------------------------------------
    # Low-level API
    # ------------------------------------------------------------------

    def _rate_limited_get(self, url, params=None):
        """GET with rate limiting and basic error handling."""
        if self._rate_limit_reached:
            return None

        params = dict(params or {})
        params["apikey"] = self.api_key

        elapsed = time.time() - self._last_call_time
        if elapsed < RATE_LIMIT_DELAY:
            time.sleep(RATE_LIMIT_DELAY - elapsed)

        try:
            resp = self.session.get(url, params=params, timeout=30)
            self._last_call_time = time.time()
            self.api_calls_made += 1

            if resp.status_code == 200:
                data = resp.json()
                if isinstance(data, dict) and ("Error Message" in data or "Error" in data):
                    msg = data.get("Error Message") or data.get("Error", "")
                    print(f"WARNING: FMP API error: {msg}", file=sys.stderr)
                    return None
                return data
            elif resp.status_code == 429:
                print("WARNING: FMP daily rate limit reached.", file=sys.stderr)
                self._rate_limit_reached = True
                return None
            else:
                print(
                    f"WARNING: FMP HTTP {resp.status_code}: {resp.text[:200]}",
                    file=sys.stderr,
                )
                return None
        except requests.RequestException as e:
            print(f"WARNING: FMP request failed: {e}", file=sys.stderr)
            return None

    # ------------------------------------------------------------------
    # S&P 500 constituents + GICS sector
    # ------------------------------------------------------------------

    def get_stock_universe(self):
        """Return S&P 500 symbols with GICS sector mapping.

        Returns:
            dict with keys:
                symbols: list[str] — sorted ticker symbols
                sector_map: dict[str, str] — {symbol: monty_sector_name}
        """
        cache_path = os.path.join(self.cache_dir, "constituents.json")
        cached = _read_json(cache_path)
        if cached and not _is_cache_stale(cached.get("fetched_at", ""), _CONSTITUENTS_TTL_DAYS):
            return {"symbols": cached["symbols"], "sector_map": cached.get("sector_map", {})}

        # Try Wikipedia (free, includes GICS sector)
        print("  Fetching S&P 500 constituents + GICS sectors...", end=" ", flush=True)
        result = self._fetch_sp500_from_wikipedia()
        if result and result["symbols"]:
            _write_json(
                cache_path,
                {
                    "fetched_at": datetime.now().isoformat(),
                    "symbols": result["symbols"],
                    "sector_map": result["sector_map"],
                },
            )
            print(
                f"OK ({len(result['symbols'])} symbols, {len(set(result['sector_map'].values()))} sectors)"
            )
            return result

        # Fallback: FMP profile batch
        print("FAILED — trying FMP profile...", end=" ", flush=True)
        result = self._fetch_sp500_from_fmp()
        if result and result["symbols"]:
            _write_json(
                cache_path,
                {
                    "fetched_at": datetime.now().isoformat(),
                    "symbols": result["symbols"],
                    "sector_map": result["sector_map"],
                },
            )
            print(f"OK ({len(result['symbols'])} symbols)")
            return result

        # Stale cache
        if cached:
            print("FAILED — using stale cache")
            return {"symbols": cached["symbols"], "sector_map": cached.get("sector_map", {})}

        print("FAILED")
        return {"symbols": [], "sector_map": {}}

    def _fetch_sp500_from_wikipedia(self):
        """Fetch S&P 500 symbols + GICS sector from Wikipedia."""
        if not HAS_PANDAS:
            return None
        try:
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            resp = requests.get(
                url,
                headers={"User-Agent": "UptrendAnalyzer/1.0"},
                timeout=30,
            )
            resp.raise_for_status()
            from io import StringIO

            tables = pd.read_html(StringIO(resp.text))
            if not tables:
                return None
            df = tables[0]
            symbols = []
            sector_map = {}
            for _, row in df.iterrows():
                sym = str(row.get("Symbol", "")).strip().replace(".", "-")
                gics = str(row.get("GICS Sector", "")).strip()
                if not sym:
                    continue
                symbols.append(sym)
                monty_sector = GICS_TO_MONTY.get(gics)
                if monty_sector:
                    sector_map[sym] = monty_sector
            symbols = sorted(set(symbols))
            return {"symbols": symbols, "sector_map": sector_map}
        except Exception as e:
            print(f"Wikipedia fallback failed: {e}", file=sys.stderr)
            return None

    def _fetch_sp500_from_fmp(self):
        """Fetch S&P 500 constituents from FMP with sector info."""
        data = self._rate_limited_get(f"{STABLE_URL}/sp500-constituent")
        if not data or not isinstance(data, list):
            return None
        symbols = []
        sector_map = {}
        for d in data:
            sym = d.get("symbol")
            if not sym:
                continue
            symbols.append(sym)
            gics = d.get("sector", "")
            monty_sector = GICS_TO_MONTY.get(gics)
            if monty_sector:
                sector_map[sym] = monty_sector
        return {"symbols": sorted(set(symbols)), "sector_map": sector_map}

    # ------------------------------------------------------------------
    # Historical prices (per-symbol, cached)
    # ------------------------------------------------------------------

    def get_historical_prices(self, symbol, days=_HISTORY_CALENDAR_DAYS):
        """Return list of {date, close, volume} sorted by date asc.

        Uses cache (1-day TTL).
        """
        cache_path = os.path.join(self.cache_dir, "prices", f"{symbol}.json")
        cached = _read_json(cache_path)
        if cached and not _is_cache_stale(cached.get("fetched_at", ""), _PRICE_TTL_DAYS):
            return cached.get("prices", [])

        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        data = self._rate_limited_get(
            f"{STABLE_URL}/historical-price-eod/full",
            params={"symbol": symbol, "from": from_date},
        )
        if data and isinstance(data, list):
            prices = sorted(
                [
                    {
                        "date": d["date"],
                        "close": float(d["close"]),
                        "volume": int(d.get("volume", 0)),
                    }
                    for d in data
                    if "date" in d and "close" in d
                ],
                key=lambda x: x["date"],
            )
            _write_json(
                cache_path,
                {
                    "fetched_at": datetime.now().isoformat(),
                    "symbol": symbol,
                    "prices": prices,
                },
            )
            return prices

        # Stale cache
        if cached:
            return cached.get("prices", [])

        return []

    def _get_cached_or_fetch(self, symbol, budget_remaining):
        """Get prices from cache or fetch if budget allows."""
        cache_path = os.path.join(self.cache_dir, "prices", f"{symbol}.json")
        cached = _read_json(cache_path)

        if cached and not _is_cache_stale(cached.get("fetched_at", ""), _PRICE_TTL_DAYS):
            return cached.get("prices", [])

        if budget_remaining <= 0:
            if cached:
                return cached.get("prices", [])
            return []

        return self.get_historical_prices(symbol)

    # ------------------------------------------------------------------
    # Uptrend signal computation
    # ------------------------------------------------------------------

    @staticmethod
    def compute_uptrend_signals(prices_list):
        """Compute daily uptrend signals using Monty's 8 conditions.

        Args:
            prices_list: list of {date, close, volume} sorted by date asc.
                Must have >= 252 entries for 52-week lookback.

        Returns:
            dict with keys:
                signals: dict[str, bool] — {date: is_uptrend} for each date
                    after warmup period
                base_filter: dict[str, bool] — {date: passes_base_filter}
                    True if price > $10 AND avg_vol > 100K
        """
        if len(prices_list) < 252:
            return {"signals": {}, "base_filter": {}}

        closes = [p["close"] for p in prices_list]
        volumes = [p["volume"] for p in prices_list]
        dates = [p["date"] for p in prices_list]

        signals = {}
        base_filter = {}

        for i in range(252, len(prices_list)):
            close = closes[i]

            # Base filters (price > $10, avg volume > 100K)
            avg_vol = sum(volumes[i - 19 : i + 1]) / 20
            passes_base = close > 10 and avg_vol > 100_000
            base_filter[dates[i]] = passes_base

            if not passes_base:
                # Does not pass base filter -> excluded from both numerator and denominator
                continue

            # Technical conditions
            sma20 = sum(closes[i - 19 : i + 1]) / 20
            sma50 = sum(closes[i - 49 : i + 1]) / 50
            sma200 = sum(closes[i - 199 : i + 1]) / 200
            low_52w = min(closes[i - 251 : i + 1])
            close_4w_ago = closes[i - 20]

            uptrend = (
                close > sma20
                and close > sma200
                and sma50 > sma200
                and close > low_52w * 1.30
                and close > close_4w_ago
            )
            signals[dates[i]] = uptrend

        return {"signals": signals, "base_filter": base_filter}

    # ------------------------------------------------------------------
    # Main uptrend computation
    # ------------------------------------------------------------------

    def calculate_uptrend_data(self):
        """Compute uptrend data from FMP prices.

        Returns:
            (all_timeseries, sector_summary, sector_timeseries_dict) matching
            UptrendDataFetcher output schema:

            all_timeseries: list[dict] — daily rows for "all" worksheet
                {worksheet, date, count, total, ratio, ma_10, slope, trend}

            sector_summary: list[dict] — latest snapshot per sector
                {Sector, Ratio, 10MA, Trend, Slope, Status, Count, Total}

            sector_timeseries_dict: dict[str, dict] — worksheet -> latest row
                {worksheet, date, count, total, ratio, ma_10, slope, trend}
        """
        # 1. Get universe
        universe = self.get_stock_universe()
        symbols = universe["symbols"]
        sector_map = universe["sector_map"]

        if not symbols:
            print("ERROR: No S&P 500 symbols available.", file=sys.stderr)
            return [], [], {}

        # 2. Fetch prices (budget-aware)
        print(
            f"  Fetching constituent prices (budget: {self.max_api_calls} calls)...",
            flush=True,
        )
        all_prices = {}  # symbol -> list of {date, close, volume}

        for sym in symbols:
            if self._rate_limit_reached:
                break
            budget_remaining = self.max_api_calls - self.api_calls_made
            prices = self._get_cached_or_fetch(sym, budget_remaining)
            if prices:
                all_prices[sym] = prices

        coverage = len(all_prices) / len(symbols) if symbols else 0
        print(
            f"  Coverage: {len(all_prices)}/{len(symbols)} symbols "
            f"({coverage:.0%}), API calls: {self.api_calls_made}"
        )

        if coverage < self.min_coverage:
            print(
                f"  WARNING: Coverage {coverage:.0%} is below "
                f"minimum {self.min_coverage:.0%}. "
                f"Re-run to fetch more symbols from cache.",
                file=sys.stderr,
            )

        if not all_prices:
            print("ERROR: No price data available.", file=sys.stderr)
            return [], [], {}

        # 3. Compute per-symbol uptrend signals
        print("  Computing uptrend signals...", end=" ", flush=True)
        symbol_signals = {}  # symbol -> {signals: {date: bool}, base_filter: {date: bool}}
        for sym, prices in all_prices.items():
            result = self.compute_uptrend_signals(prices)
            if result["signals"] or result["base_filter"]:
                symbol_signals[sym] = result
        print(f"OK ({len(symbol_signals)} symbols with signals)")

        if not symbol_signals:
            print("ERROR: No uptrend signals computed.", file=sys.stderr)
            return [], [], {}

        # 4. Aggregate daily: overall + per-sector
        all_daily, sector_daily = self._aggregate_daily(symbol_signals, sector_map)

        if not all_daily:
            print("ERROR: No daily aggregation data.", file=sys.stderr)
            return [], [], {}

        # 5. Build timeseries with 10MA, slope, trend
        all_timeseries = self._build_timeseries(all_daily, "all")

        sector_timeseries = {}
        for sector_name, daily_data in sector_daily.items():
            ws_key = DISPLAY_TO_WORKSHEET.get(sector_name, sector_name)
            ts = self._build_timeseries(daily_data, ws_key)
            if ts:
                sector_timeseries[sector_name] = ts

        # 6. Build sector summary (latest row per sector)
        sector_summary = []
        sector_timeseries_dict = {}
        for sector_name, ts in sector_timeseries.items():
            if not ts:
                continue
            latest = ts[-1]
            ws_key = DISPLAY_TO_WORKSHEET.get(sector_name, sector_name)
            sector_timeseries_dict[ws_key] = latest

            ratio = latest.get("ratio")
            status = (
                "Overbought"
                if ratio is not None and ratio > OVERBOUGHT_THRESHOLD
                else "Oversold"
                if ratio is not None and ratio < OVERSOLD_THRESHOLD
                else "Normal"
            )
            sector_summary.append(
                {
                    "Sector": sector_name,
                    "Ratio": ratio,
                    "10MA": latest.get("ma_10"),
                    "Trend": (latest.get("trend") or "").capitalize(),
                    "Slope": latest.get("slope"),
                    "Status": status,
                    "Count": latest.get("count"),
                    "Total": latest.get("total"),
                }
            )

        return all_timeseries, sector_summary, sector_timeseries_dict

    def _aggregate_daily(self, symbol_signals, sector_map):
        """Aggregate per-symbol signals into daily overall + sector counts.

        Returns:
            (all_daily, sector_daily):
            all_daily: dict[date, (count, total)] — overall
            sector_daily: dict[sector_name, dict[date, (count, total)]]
        """
        all_daily = {}  # date -> [uptrend_count, base_count]
        sector_daily = {}  # sector -> date -> [uptrend_count, base_count]

        for sym, result in symbol_signals.items():
            sector = sector_map.get(sym)
            signals = result["signals"]
            base_filter = result["base_filter"]

            # All dates where this symbol passes base filter
            for date, passes in base_filter.items():
                if not passes:
                    continue
                # This symbol passes base filter on this date
                is_uptrend = signals.get(date, False)

                if date not in all_daily:
                    all_daily[date] = [0, 0]
                all_daily[date][1] += 1
                if is_uptrend:
                    all_daily[date][0] += 1

                if sector:
                    if sector not in sector_daily:
                        sector_daily[sector] = {}
                    if date not in sector_daily[sector]:
                        sector_daily[sector][date] = [0, 0]
                    sector_daily[sector][date][1] += 1
                    if is_uptrend:
                        sector_daily[sector][date][0] += 1

        return all_daily, sector_daily

    @staticmethod
    def _build_timeseries(daily_data, worksheet_name):
        """Build timeseries rows with 10MA, slope, trend from daily counts.

        Args:
            daily_data: dict[date, (count, total)] or dict[date, [count, total]]
            worksheet_name: "all" or "sec_xxx"

        Returns:
            list[dict] sorted by date ascending, each with:
            {worksheet, date, count, total, ratio, ma_10, slope, trend}
        """
        sorted_dates = sorted(daily_data.keys())
        if not sorted_dates:
            return []

        rows = []
        ratios = []

        for date in sorted_dates:
            count, total = daily_data[date]
            ratio = count / total if total > 0 else 0.0
            ratios.append(ratio)

            # 10-day SMA of ratio
            if len(ratios) >= 10:
                ma_10 = sum(ratios[-10:]) / 10
            else:
                ma_10 = sum(ratios) / len(ratios)

            # Slope: 1-day difference of ma_10
            if len(rows) >= 1 and rows[-1].get("ma_10") is not None:
                slope = ma_10 - rows[-1]["ma_10"]
            else:
                slope = 0.0

            trend = "up" if slope > 0 else "down"

            rows.append(
                {
                    "worksheet": worksheet_name,
                    "date": date,
                    "count": count,
                    "total": total,
                    "ratio": round(ratio, 6),
                    "ma_10": round(ma_10, 6),
                    "slope": round(slope, 6),
                    "trend": trend,
                }
            )

        return rows

    def get_api_stats(self):
        """Return API usage statistics."""
        return {
            "api_calls_made": self.api_calls_made,
            "rate_limit_reached": self._rate_limit_reached,
            "max_api_calls": self.max_api_calls,
        }
