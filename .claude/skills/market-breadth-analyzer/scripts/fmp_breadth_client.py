#!/usr/bin/env python3
"""
Market Breadth Analyzer - FMP Self-Calculation Client

Alternative to CSV client: fetches S&P 500 constituent prices via FMP API,
computes breadth ratio (% above 200DMA), and derives EMA/trend/peak/trough
data matching the csv_client.DETAIL_COLUMNS schema.

Features:
- Disk cache with per-symbol JSON files (avoids re-fetching)
- Budget-aware fetching (respects max_api_calls)
- Wikipedia fallback for S&P 500 constituents
- Pure-Python peak/trough detection (no scipy dependency)

Usage:
    from fmp_breadth_client import FMPBreadthClient

    client = FMPBreadthClient(api_key="...", cache_dir=".breadth_cache")
    detail_rows, summary = client.calculate_breadth_data()
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
# Pure-Python computation helpers
# ---------------------------------------------------------------------------


def compute_ema(values, span):
    """Compute EMA matching pandas ewm(span=span, adjust=False).mean().

    Args:
        values: list of floats (ordered oldest-first).
        span: EMA window size.

    Returns:
        list of floats (same length as values).
    """
    if not values:
        return []
    alpha = 2.0 / (span + 1)
    result = [values[0]]
    for v in values[1:]:
        result.append(alpha * v + (1 - alpha) * result[-1])
    return result


def compute_trend_hysteresis(ema200_series, threshold=0.001):
    """Compute trend direction using hysteresis on EMA-200 slope.

    Returns list of 1 (uptrend) or -1 (downtrend) for each data point.
    Transition requires the EMA-200 delta to exceed threshold in the
    opposite direction of the current trend.
    """
    if not ema200_series:
        return []
    trend = [1]  # assume uptrend at start
    for i in range(1, len(ema200_series)):
        delta = ema200_series[i] - ema200_series[i - 1]
        prev = trend[-1]
        if prev == 1 and delta < -threshold:
            trend.append(-1)
        elif prev == -1 and delta > threshold:
            trend.append(1)
        else:
            trend.append(prev)
    return trend


def _find_peaks(values, distance=50, prominence=0.015):
    """Find local maxima in a 1-D sequence (pure Python).

    Returns sorted list of indices.
    """
    n = len(values)
    if n < 3:
        return []

    # Step 1: all local maxima (strictly greater than at least one neighbor)
    candidates = []
    for i in range(1, n - 1):
        if values[i] >= values[i - 1] and values[i] >= values[i + 1]:
            if values[i] > values[i - 1] or values[i] > values[i + 1]:
                candidates.append(i)

    if not candidates:
        return []

    # Step 2: filter by prominence
    prominent = []
    for idx in candidates:
        left_start = max(0, idx - distance)
        right_end = min(n, idx + distance + 1)
        left_min = min(values[left_start:idx]) if idx > left_start else values[idx]
        right_min = min(values[idx + 1 : right_end]) if idx + 1 < right_end else values[idx]
        prom = values[idx] - max(left_min, right_min)
        if prom >= prominence:
            prominent.append(idx)

    if not prominent:
        return []

    # Step 3: enforce minimum distance (keep highest peak per window)
    filtered = [prominent[0]]
    for idx in prominent[1:]:
        if idx - filtered[-1] >= distance:
            filtered.append(idx)
        elif values[idx] > values[filtered[-1]]:
            filtered[-1] = idx

    return filtered


def _find_troughs(values, distance=50, prominence=0.015):
    """Find local minima in a 1-D sequence. Returns sorted list of indices."""
    inverted = [-v for v in values]
    return _find_peaks(inverted, distance, prominence)


# ---------------------------------------------------------------------------
# Disk cache helpers
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
# FMP Breadth Client
# ---------------------------------------------------------------------------

STABLE_URL = "https://financialmodelingprep.com/stable"
RATE_LIMIT_DELAY = 0.3
_HISTORY_CALENDAR_DAYS = 500  # ~350 trading days → 150 after 200DMA warmup


class FMPBreadthClient:
    """Fetch S&P 500 prices and compute market breadth data.

    Args:
        api_key: FMP API key (falls back to $FMP_API_KEY).
        cache_dir: Path to disk cache directory.
        max_api_calls: Maximum API calls per run (budget).
        min_coverage: Minimum fraction of symbols needed (0-1).
    """

    def __init__(
        self,
        api_key=None,
        cache_dir=".breadth_cache",
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
    # S&P 500 constituents
    # ------------------------------------------------------------------

    def get_sp500_constituents(self):
        """Return list of S&P 500 symbols. Uses cache (7-day TTL).

        Returns:
            list[str] — sorted list of ticker symbols.
        """
        cache_path = os.path.join(self.cache_dir, "constituents.json")
        cached = _read_json(cache_path)
        if cached and not _is_cache_stale(cached.get("fetched_at", ""), _CONSTITUENTS_TTL_DAYS):
            return cached["symbols"]

        # Try FMP
        print("  Fetching S&P 500 constituents from FMP...", end=" ", flush=True)
        data = self._rate_limited_get(f"{STABLE_URL}/sp500-constituent")
        if data and isinstance(data, list):
            symbols = sorted({d["symbol"] for d in data if d.get("symbol")})
            _write_json(
                cache_path,
                {"fetched_at": datetime.now().isoformat(), "symbols": symbols},
            )
            print(f"OK ({len(symbols)} symbols)")
            return symbols

        # Fallback: Wikipedia
        print("FAILED — trying Wikipedia...", end=" ", flush=True)
        symbols = self._fetch_sp500_from_wikipedia()
        if symbols:
            _write_json(
                cache_path,
                {"fetched_at": datetime.now().isoformat(), "symbols": symbols},
            )
            print(f"OK ({len(symbols)} symbols)")
            return symbols

        # Fallback: stale cache
        if cached:
            print("FAILED — using stale cache")
            return cached["symbols"]

        print("FAILED")
        return []

    def _fetch_sp500_from_wikipedia(self):
        """Fetch S&P 500 symbols from Wikipedia. Returns sorted list or []."""
        if not HAS_PANDAS:
            return []
        try:
            url = "https://en.wikipedia.org/wiki/List_of_S%26P_500_companies"
            resp = requests.get(
                url,
                headers={"User-Agent": "MarketBreadthAnalyzer/1.0"},
                timeout=30,
            )
            resp.raise_for_status()
            from io import StringIO

            tables = pd.read_html(StringIO(resp.text))
            if not tables:
                return []
            df = tables[0]
            symbols = sorted(
                str(row.get("Symbol", "")).strip().replace(".", "-")
                for _, row in df.iterrows()
                if row.get("Symbol")
            )
            return [s for s in symbols if s]
        except Exception as e:
            print(f"Wikipedia fallback failed: {e}", file=sys.stderr)
            return []

    # ------------------------------------------------------------------
    # Historical prices (per-symbol, cached)
    # ------------------------------------------------------------------

    def get_historical_prices(self, symbol, days=_HISTORY_CALENDAR_DAYS):
        """Return dict mapping date-str → close price. Uses cache (1-day TTL).

        Returns:
            dict[str, float] — {date_str: close_price} or {} on failure.
        """
        cache_path = os.path.join(self.cache_dir, "prices", f"{symbol}.json")
        cached = _read_json(cache_path)
        if cached and not _is_cache_stale(cached.get("fetched_at", ""), _PRICE_TTL_DAYS):
            return {p["date"]: p["close"] for p in cached.get("prices", [])}

        # Fetch from FMP
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
        data = self._rate_limited_get(
            f"{STABLE_URL}/historical-price-eod/full",
            params={"symbol": symbol, "from": from_date},
        )
        if data and isinstance(data, list):
            prices = [
                {"date": d["date"], "close": float(d["close"])}
                for d in data
                if "date" in d and "close" in d
            ]
            _write_json(
                cache_path,
                {
                    "fetched_at": datetime.now().isoformat(),
                    "symbol": symbol,
                    "prices": prices,
                },
            )
            return {p["date"]: p["close"] for p in prices}

        # Fallback: stale cache
        if cached:
            return {p["date"]: p["close"] for p in cached.get("prices", [])}

        return {}

    def _get_sp500_index_prices(self, days=_HISTORY_CALENDAR_DAYS):
        """Fetch S&P 500 index prices. Returns {date_str: close}.

        Tries ^GSPC first, then SPY as proxy (×10 approximation).
        """
        cache_path = os.path.join(self.cache_dir, "sp500_index.json")
        cached = _read_json(cache_path)
        if cached and not _is_cache_stale(cached.get("fetched_at", ""), _PRICE_TTL_DAYS):
            return {p["date"]: p["close"] for p in cached.get("prices", [])}

        print("  Fetching S&P 500 index prices...", end=" ", flush=True)
        from_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")

        # Try ^GSPC
        data = self._rate_limited_get(
            f"{STABLE_URL}/historical-price-eod/full",
            params={"symbol": "^GSPC", "from": from_date},
        )
        if data and isinstance(data, list) and len(data) > 10:
            prices = [
                {"date": d["date"], "close": float(d["close"])}
                for d in data
                if "date" in d and "close" in d
            ]
            _write_json(
                cache_path,
                {"fetched_at": datetime.now().isoformat(), "prices": prices},
            )
            print(f"OK ({len(prices)} days via ^GSPC)")
            return {p["date"]: p["close"] for p in prices}

        # Fallback: SPY × 10
        data = self._rate_limited_get(
            f"{STABLE_URL}/historical-price-eod/full",
            params={"symbol": "SPY", "from": from_date},
        )
        if data and isinstance(data, list):
            prices = [
                {"date": d["date"], "close": round(float(d["close"]) * 10, 2)}
                for d in data
                if "date" in d and "close" in d
            ]
            _write_json(
                cache_path,
                {"fetched_at": datetime.now().isoformat(), "prices": prices},
            )
            print(f"OK ({len(prices)} days via SPY proxy)")
            return {p["date"]: p["close"] for p in prices}

        # Stale cache
        if cached:
            print("FAILED — using stale cache")
            return {p["date"]: p["close"] for p in cached.get("prices", [])}

        print("FAILED")
        return {}

    # ------------------------------------------------------------------
    # Main breadth computation
    # ------------------------------------------------------------------

    def calculate_breadth_data(self):
        """Compute breadth data from FMP prices.

        Returns:
            (detail_rows, summary) matching csv_client interface:
            - detail_rows: list[dict] with DETAIL_COLUMNS keys, sorted by Date asc.
            - summary: dict[str, str] with aggregate metrics.
        """
        # 1. Constituents
        symbols = self.get_sp500_constituents()
        if not symbols:
            print("ERROR: No S&P 500 symbols available.", file=sys.stderr)
            return [], {}

        # 2. S&P 500 index prices
        sp500_prices = self._get_sp500_index_prices()

        # 3. Fetch constituent prices (budget-aware)
        print(
            f"  Fetching constituent prices (budget: {self.max_api_calls} calls)...",
            flush=True,
        )
        all_prices = {}  # symbol → {date: close}
        budget_remaining = self.max_api_calls - self.api_calls_made
        cached_count = 0
        fetched_count = 0

        for sym in symbols:
            if self._rate_limit_reached:
                break
            prices = self._get_cached_or_fetch(sym, budget_remaining - fetched_count)
            if prices:
                all_prices[sym] = prices
                # Check if this was from cache (no API call counted)
                cache_path = os.path.join(self.cache_dir, "prices", f"{sym}.json")
                c = _read_json(cache_path)
                if c and not _is_cache_stale(c.get("fetched_at", ""), _PRICE_TTL_DAYS):
                    cached_count += 1
                else:
                    fetched_count += 1

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
            return [], {}

        # 4. Compute 200DMA for each symbol
        symbol_above_200dma = self._compute_above_200dma(all_prices)

        # 5. Compute daily breadth ratio
        breadth_series = self._compute_daily_breadth(symbol_above_200dma, all_prices)

        if not breadth_series:
            print("ERROR: No valid breadth data computed.", file=sys.stderr)
            return [], {}

        # Sort by date
        breadth_series.sort(key=lambda x: x["date"])

        # 6. Derive EMA, trend, peaks, troughs
        raw_values = [d["breadth_raw"] for d in breadth_series]

        ema8 = compute_ema(raw_values, span=8)
        ema200 = compute_ema(raw_values, span=200)
        trend = compute_trend_hysteresis(ema200, threshold=0.001)

        peak_indices = set(_find_peaks(ema8, distance=50, prominence=0.015))
        trough_indices = set(_find_troughs(ema8, distance=50, prominence=0.015))

        # 7. Build output rows
        detail_rows = []
        for i, d in enumerate(breadth_series):
            is_peak = i in peak_indices
            is_trough = i in trough_indices
            is_trough_below_04 = is_trough and ema8[i] < 0.4

            row = {
                "Date": d["date"],
                "S&P500_Price": sp500_prices.get(d["date"], 0.0),
                "Breadth_Index_Raw": round(d["breadth_raw"], 6),
                "Breadth_Index_200MA": round(ema200[i], 6),
                "Breadth_Index_8MA": round(ema8[i], 6),
                "Breadth_200MA_Trend": trend[i],
                "Bearish_Signal": False,
                "Is_Peak": is_peak,
                "Is_Trough": is_trough,
                "Is_Trough_8MA_Below_04": is_trough_below_04,
            }
            detail_rows.append(row)

        # 8. Summary
        summary = self.compute_summary(detail_rows)

        print(
            f"  Breadth data: {len(detail_rows)} days "
            f"({detail_rows[0]['Date']} to {detail_rows[-1]['Date']})"
        )

        return detail_rows, summary

    def _get_cached_or_fetch(self, symbol, budget_remaining):
        """Get prices from cache or fetch if budget allows.

        Returns:
            dict[str, float] — {date: close} or {} on failure.
        """
        cache_path = os.path.join(self.cache_dir, "prices", f"{symbol}.json")
        cached = _read_json(cache_path)

        # Fresh cache → use it
        if cached and not _is_cache_stale(cached.get("fetched_at", ""), _PRICE_TTL_DAYS):
            return {p["date"]: p["close"] for p in cached.get("prices", [])}

        # Budget exhausted → use stale cache if available
        if budget_remaining <= 0:
            if cached:
                return {p["date"]: p["close"] for p in cached.get("prices", [])}
            return {}

        # Fetch
        return self.get_historical_prices(symbol)

    def _compute_above_200dma(self, all_prices):
        """For each symbol, compute which dates have close > 200DMA.

        Args:
            all_prices: {symbol: {date: close}}

        Returns:
            {symbol: {date: bool}} — True if close > 200DMA on that date.
        """
        result = {}
        for sym, prices in all_prices.items():
            sorted_dates = sorted(prices.keys())
            closes = [prices[d] for d in sorted_dates]

            if len(closes) < 200:
                continue

            above = {}
            # Running SMA-200 via sliding window
            window_sum = sum(closes[:200])
            for i in range(199, len(closes)):
                if i >= 200:
                    window_sum += closes[i] - closes[i - 200]
                sma200 = window_sum / 200
                above[sorted_dates[i]] = closes[i] > sma200

            result[sym] = above

        return result

    def _compute_daily_breadth(self, symbol_above_200dma, all_prices):
        """Compute daily breadth ratio from per-symbol 200DMA signals.

        Returns:
            list[dict] with keys: date, breadth_raw, total_symbols.
        """
        # Collect all dates that have 200DMA data
        date_counts = {}  # date → (above_count, total_count)
        for sym, above_map in symbol_above_200dma.items():
            for date, is_above in above_map.items():
                if date not in date_counts:
                    date_counts[date] = [0, 0]
                date_counts[date][1] += 1
                if is_above:
                    date_counts[date][0] += 1

        result = []
        for date in sorted(date_counts.keys()):
            above, total = date_counts[date]
            if total > 0:
                result.append(
                    {
                        "date": date,
                        "breadth_raw": above / total,
                        "total_symbols": total,
                    }
                )

        return result

    def compute_summary(self, detail_rows):
        """Compute summary statistics matching csv_client summary format.

        Returns:
            dict[str, str] with keys matching summary CSV Metric names.
        """
        peaks_8ma = [r["Breadth_Index_8MA"] for r in detail_rows if r.get("Is_Peak")]
        troughs_extreme = [
            r["Breadth_Index_8MA"] for r in detail_rows if r.get("Is_Trough_8MA_Below_04")
        ]
        troughs_all = [r["Breadth_Index_8MA"] for r in detail_rows if r.get("Is_Trough")]

        summary = {}

        if peaks_8ma:
            avg_peak = sum(peaks_8ma) / len(peaks_8ma)
            summary["Average Peaks (200MA)"] = f"{avg_peak:.6f}"
            summary["Total Peaks"] = str(len(peaks_8ma))

        if troughs_extreme:
            avg_trough_ext = sum(troughs_extreme) / len(troughs_extreme)
            summary["Average Troughs (8MA < 0.4)"] = f"{avg_trough_ext:.6f}"

        if troughs_all:
            avg_trough_all = sum(troughs_all) / len(troughs_all)
            summary["Average Troughs (All)"] = f"{avg_trough_all:.6f}"
            summary["Total Troughs"] = str(len(troughs_all))

        if detail_rows:
            summary["Analysis Period"] = f"{detail_rows[0]['Date']} to {detail_rows[-1]['Date']}"

        return summary

    def get_api_stats(self):
        """Return API usage statistics."""
        return {
            "api_calls_made": self.api_calls_made,
            "rate_limit_reached": self._rate_limit_reached,
            "max_api_calls": self.max_api_calls,
        }
