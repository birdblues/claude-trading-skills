"""Tests for FMP Uptrend Client.

Unit tests cover signal computation (no API calls).
Integration tests mock FMP API responses.
"""

import os
import tempfile
from unittest.mock import MagicMock, patch

from fmp_uptrend_client import (
    DISPLAY_TO_WORKSHEET,
    GICS_TO_MONTY,
    OVERBOUGHT_THRESHOLD,
    OVERSOLD_THRESHOLD,
    FMPUptrendClient,
    _is_cache_stale,
    _read_json,
    _write_json,
)
from helpers import make_sector_summary_row, make_timeseries_row

# ---------------------------------------------------------------------------
# Helpers: generate synthetic price data
# ---------------------------------------------------------------------------


def _make_prices(
    n=300,
    base_close=100.0,
    base_volume=200_000,
    start_date="2024-01-02",
    close_trend=0.0,
    volume_override=None,
    close_override=None,
):
    """Generate n days of {date, close, volume} sorted ascending.

    Args:
        n: Number of trading days.
        base_close: Starting close price.
        base_volume: Starting volume.
        start_date: Start date string.
        close_trend: Daily additive trend on close.
        volume_override: If set, use this volume for all rows.
        close_override: If set, use this close for all rows.
    """
    from datetime import datetime, timedelta

    prices = []
    dt = datetime.strptime(start_date, "%Y-%m-%d")
    for i in range(n):
        close = close_override if close_override is not None else base_close + close_trend * i
        vol = volume_override if volume_override is not None else base_volume
        prices.append(
            {
                "date": dt.strftime("%Y-%m-%d"),
                "close": close,
                "volume": vol,
            }
        )
        dt += timedelta(days=1)
        # Skip weekends
        while dt.weekday() >= 5:
            dt += timedelta(days=1)
    return prices


def _make_uptrend_prices(n=300):
    """Generate prices where all 8 uptrend conditions are met after warmup.

    Conditions satisfied:
    1. close > $10 (close=150)
    2. avg_vol > 100K (volume=200K)
    3. Market cap > $50M (skipped for S&P 500)
    4. close > SMA20 (close rises steadily)
    5. close > SMA200 (close >> base after warmup)
    6. SMA50 > SMA200 (steady uptrend)
    7. close > 52W_low * 1.30 (close >> min)
    8. close > close_4w_ago (positive 4-week perf)
    """
    return _make_prices(n=n, base_close=100.0, close_trend=0.15, base_volume=200_000)


def _make_downtrend_prices(n=300):
    """Generate prices in a persistent downtrend (close declines)."""
    return _make_prices(n=n, base_close=200.0, close_trend=-0.10, base_volume=200_000)


# ---------------------------------------------------------------------------
# Unit tests: compute_uptrend_signals
# ---------------------------------------------------------------------------


class TestUptrendSignalComputation:
    """Test the 8-condition uptrend logic without any API calls."""

    def test_uptrend_all_conditions_met(self):
        """All 8 conditions met -> signals should be True."""
        prices = _make_uptrend_prices(n=300)
        result = FMPUptrendClient.compute_uptrend_signals(prices)

        # Should have signals after 252-day warmup
        assert len(result["signals"]) > 0
        # At least some should be True (steady uptrend)
        true_count = sum(1 for v in result["signals"].values() if v)
        assert true_count > 0, "Expected some uptrend signals for steady uptrend"

    def test_uptrend_price_below_sma200(self):
        """Price below SMA200 -> should fail condition 5."""
        # Start high, then crash -> close < SMA200
        prices = _make_prices(n=300, base_close=150.0, close_trend=-0.20, base_volume=200_000)
        result = FMPUptrendClient.compute_uptrend_signals(prices)

        # Late signals should be False (price below SMA200)
        late_signals = {d: v for d, v in result["signals"].items() if d >= prices[280]["date"]}
        if late_signals:
            true_count = sum(1 for v in late_signals.values() if v)
            assert true_count == 0, "Price below SMA200 should not be uptrend"

    def test_uptrend_no_golden_cross(self):
        """SMA50 < SMA200 -> should fail condition 6.

        Create a scenario with a sharp drop followed by partial recovery.
        """
        prices = []
        from datetime import datetime, timedelta

        dt = datetime(2023, 1, 2)
        # 200 days at high level, then drop, then partial recovery
        for i in range(200):
            prices.append({"date": dt.strftime("%Y-%m-%d"), "close": 150.0, "volume": 200_000})
            dt += timedelta(days=1)
            while dt.weekday() >= 5:
                dt += timedelta(days=1)
        # Drop sharply for 30 days
        for i in range(30):
            prices.append({"date": dt.strftime("%Y-%m-%d"), "close": 80.0, "volume": 200_000})
            dt += timedelta(days=1)
            while dt.weekday() >= 5:
                dt += timedelta(days=1)
        # Partial recovery but SMA50 still < SMA200
        for i in range(70):
            prices.append({"date": dt.strftime("%Y-%m-%d"), "close": 120.0, "volume": 200_000})
            dt += timedelta(days=1)
            while dt.weekday() >= 5:
                dt += timedelta(days=1)

        result = FMPUptrendClient.compute_uptrend_signals(prices)
        # After the drop, SMA50 should be below SMA200 -> no uptrend
        late_signals = {d: v for d, v in result["signals"].items() if d >= prices[260]["date"]}
        if late_signals:
            true_count = sum(1 for v in late_signals.values() if v)
            assert true_count == 0, "SMA50 < SMA200 should prevent uptrend"

    def test_uptrend_low_volume(self):
        """Avg volume < 100K -> excluded from base filter."""
        prices = _make_prices(n=300, base_close=150.0, close_trend=0.1, volume_override=50_000)
        result = FMPUptrendClient.compute_uptrend_signals(prices)

        # All dates should fail base filter (low volume)
        assert len(result["signals"]) == 0, "Low volume stocks should be excluded"
        # base_filter should have entries but all False
        false_count = sum(1 for v in result["base_filter"].values() if not v)
        assert false_count == len(result["base_filter"])

    def test_uptrend_penny_stock(self):
        """Price < $10 -> excluded from base filter."""
        prices = _make_prices(n=300, close_override=5.0, base_volume=200_000)
        result = FMPUptrendClient.compute_uptrend_signals(prices)

        assert len(result["signals"]) == 0, "Penny stocks should be excluded"

    def test_uptrend_52w_range_fail(self):
        """Close not 30% above 52W low -> condition 7 fails.

        Price stays flat, so close == 52W_low (not > 1.30 * 52W_low).
        """
        prices = _make_prices(n=300, close_override=100.0, base_volume=200_000)
        result = FMPUptrendClient.compute_uptrend_signals(prices)

        # Flat price -> close == 52W_low, so close > 52W_low*1.30 fails
        true_count = sum(1 for v in result["signals"].values() if v)
        assert true_count == 0, "Flat price should fail 52W range condition"

    def test_uptrend_4week_negative(self):
        """4-week performance negative -> condition 8 fails."""
        # Create prices that oscillate: recent decline
        from datetime import datetime, timedelta

        prices = []
        dt = datetime(2023, 1, 2)
        for i in range(260):
            # Up for 252 days, then decline
            if i < 252:
                close = 100 + i * 0.2
            else:
                close = 100 + 252 * 0.2 - (i - 252) * 5  # sharp decline
            prices.append({"date": dt.strftime("%Y-%m-%d"), "close": close, "volume": 200_000})
            dt += timedelta(days=1)
            while dt.weekday() >= 5:
                dt += timedelta(days=1)

        result = FMPUptrendClient.compute_uptrend_signals(prices)
        # The last few days should have negative 4-week performance
        late_dates = sorted(result["signals"].keys())[-5:]
        for d in late_dates:
            if d in result["signals"]:
                assert not result["signals"][d], f"4-week negative should prevent uptrend on {d}"

    def test_insufficient_data(self):
        """Less than 252 days of data -> no signals."""
        prices = _make_prices(n=200)
        result = FMPUptrendClient.compute_uptrend_signals(prices)
        assert result["signals"] == {}
        assert result["base_filter"] == {}


# ---------------------------------------------------------------------------
# Unit tests: ratio, SMA, slope, trend computation
# ---------------------------------------------------------------------------


class TestRatioAndTimeseries:
    """Test ratio calculation, 10MA, slope, and trend."""

    def test_ratio_calculation(self):
        """15 uptrend out of 60 base -> ratio = 0.25."""
        daily_data = {"2026-03-06": (15, 60)}
        ts = FMPUptrendClient._build_timeseries(daily_data, "all")
        assert len(ts) == 1
        assert ts[0]["ratio"] == 0.25
        assert ts[0]["count"] == 15
        assert ts[0]["total"] == 60

    def test_sma10_and_slope(self):
        """10-day SMA and slope calculation."""
        daily_data = {}
        for i in range(15):
            date = f"2026-01-{i + 1:02d}"
            # Ratio rises from 0.20 to 0.34 over 15 days
            count = 20 + i
            total = 100
            daily_data[date] = (count, total)

        ts = FMPUptrendClient._build_timeseries(daily_data, "all")
        assert len(ts) == 15

        # ma_10 at day 10 (index 9) should be average of first 10 ratios
        ratios = [(20 + i) / 100 for i in range(10)]
        expected_ma = sum(ratios) / 10
        assert abs(ts[9]["ma_10"] - expected_ma) < 0.0001

        # Slope at day 11 = ma_10[10] - ma_10[9]
        assert ts[10]["slope"] != 0  # Should have non-zero slope

    def test_trend_direction(self):
        """slope > 0 -> 'up', slope <= 0 -> 'down'."""
        # Rising ratios -> positive slope -> up trend
        daily_data = {}
        for i in range(20):
            date = f"2026-01-{i + 1:02d}"
            daily_data[date] = (20 + i * 2, 100)

        ts = FMPUptrendClient._build_timeseries(daily_data, "all")
        # After 10 days of rising ratios, slope should be positive
        late_rows = ts[11:]
        for row in late_rows:
            assert row["trend"] == "up", f"Rising ratios should have up trend on {row['date']}"

    def test_zero_total_ratio(self):
        """total=0 should yield ratio=0.0."""
        daily_data = {"2026-03-06": (0, 0)}
        ts = FMPUptrendClient._build_timeseries(daily_data, "all")
        assert ts[0]["ratio"] == 0.0


class TestSectorAggregation:
    """Test GICS mapping and sector-level count/total."""

    def test_gics_mapping_complete(self):
        """All 11 GICS sectors are mapped."""
        assert len(GICS_TO_MONTY) == 11
        expected = {
            "Technology",
            "Consumer Cyclical",
            "Communication Services",
            "Financial",
            "Industrials",
            "Utilities",
            "Consumer Defensive",
            "Healthcare",
            "Real Estate",
            "Energy",
            "Basic Materials",
        }
        assert set(GICS_TO_MONTY.values()) == expected

    def test_sector_aggregation(self):
        """Per-sector count/total aggregation from symbol signals."""
        sector_map = {"AAPL": "Technology", "MSFT": "Technology", "XOM": "Energy"}
        symbol_signals = {
            "AAPL": {
                "signals": {"2026-03-06": True},
                "base_filter": {"2026-03-06": True},
            },
            "MSFT": {
                "signals": {"2026-03-06": False},
                "base_filter": {"2026-03-06": True},
            },
            "XOM": {
                "signals": {"2026-03-06": True},
                "base_filter": {"2026-03-06": True},
            },
        }

        client = FMPUptrendClient.__new__(FMPUptrendClient)
        all_daily, sector_daily = client._aggregate_daily(symbol_signals, sector_map)

        # Overall: 2 uptrend, 3 total
        assert all_daily["2026-03-06"] == [2, 3]

        # Technology: 1 uptrend, 2 total
        assert sector_daily["Technology"]["2026-03-06"] == [1, 2]

        # Energy: 1 uptrend, 1 total
        assert sector_daily["Energy"]["2026-03-06"] == [1, 1]

    def test_display_to_worksheet_complete(self):
        """All Monty sector names map to worksheet keys."""
        assert len(DISPLAY_TO_WORKSHEET) == 11
        for monty_name in GICS_TO_MONTY.values():
            assert monty_name in DISPLAY_TO_WORKSHEET, f"Missing worksheet for {monty_name}"


# ---------------------------------------------------------------------------
# Unit tests: cache
# ---------------------------------------------------------------------------


class TestCache:
    def test_cache_write_and_read(self):
        """Cache write then read returns same data."""
        with tempfile.TemporaryDirectory() as tmpdir:
            path = os.path.join(tmpdir, "test.json")
            data = {"key": "value", "numbers": [1, 2, 3]}
            _write_json(path, data)
            loaded = _read_json(path)
            assert loaded == data

    def test_cache_stale_detection(self):
        """Stale cache detection by TTL."""
        from datetime import datetime, timedelta

        fresh = datetime.now().isoformat()
        assert not _is_cache_stale(fresh, 1)

        old = (datetime.now() - timedelta(days=2)).isoformat()
        assert _is_cache_stale(old, 1)

    def test_cache_invalid_timestamp(self):
        """Invalid timestamp -> stale."""
        assert _is_cache_stale("invalid", 1)
        assert _is_cache_stale(None, 1)


# ---------------------------------------------------------------------------
# Unit tests: output format matches CSV client
# ---------------------------------------------------------------------------


class TestOutputFormat:
    """Verify FMP output matches the schema expected by calculators."""

    def test_output_format_matches_csv(self):
        """all_timeseries rows have all required keys."""
        daily_data = {}
        for i in range(20):
            date = f"2026-01-{i + 1:02d}"
            daily_data[date] = (30 + i, 100)

        ts = FMPUptrendClient._build_timeseries(daily_data, "all")
        required_keys = {"worksheet", "date", "count", "total", "ratio", "ma_10", "slope", "trend"}

        for row in ts:
            assert required_keys.issubset(row.keys()), f"Missing keys: {required_keys - row.keys()}"
            assert row["worksheet"] == "all"
            assert isinstance(row["ratio"], float)
            assert isinstance(row["ma_10"], float)
            assert isinstance(row["slope"], float)
            assert row["trend"] in ("up", "down")

    def test_sector_summary_format(self):
        """Sector summary rows match expected schema."""
        # Create a minimal client and call the sector summary builder path
        daily_data = {}
        for i in range(15):
            date = f"2026-01-{i + 1:02d}"
            daily_data[date] = (20 + i, 80)

        ts = FMPUptrendClient._build_timeseries(daily_data, "sec_technology")
        latest = ts[-1]

        # Build a sector summary row like calculate_uptrend_data does
        ratio = latest["ratio"]
        status = (
            "Overbought"
            if ratio > OVERBOUGHT_THRESHOLD
            else "Oversold"
            if ratio < OVERSOLD_THRESHOLD
            else "Normal"
        )
        summary_row = {
            "Sector": "Technology",
            "Ratio": ratio,
            "10MA": latest["ma_10"],
            "Trend": latest["trend"].capitalize(),
            "Slope": latest["slope"],
            "Status": status,
            "Count": latest["count"],
            "Total": latest["total"],
        }

        required_keys = {"Sector", "Ratio", "10MA", "Trend", "Slope", "Status", "Count", "Total"}
        assert required_keys.issubset(summary_row.keys())


# ---------------------------------------------------------------------------
# Integration tests: calculators accept FMP output
# ---------------------------------------------------------------------------


class TestCalculatorsAcceptFMPOutput:
    """Verify the 5 calculators accept FMP-format data."""

    def _make_fmp_style_data(self):
        """Create FMP-style output data for calculator testing."""
        # all_timeseries: 20 rows
        all_timeseries = []
        for i in range(20):
            ratio = 0.20 + 0.005 * i
            ma_10 = ratio - 0.01 if i >= 10 else ratio
            slope = 0.005 if i > 0 else 0.0
            all_timeseries.append(
                make_timeseries_row(
                    ratio=round(ratio, 4),
                    ma_10=round(ma_10, 4),
                    slope=round(slope, 6),
                    trend="up",
                    date=f"2026-01-{i + 1:02d}",
                    count=int(ratio * 480),
                    total=480,
                )
            )

        latest_all = all_timeseries[-1]

        # sector_summary: 11 sectors
        sectors = [
            "Technology",
            "Consumer Cyclical",
            "Communication Services",
            "Financial",
            "Industrials",
            "Utilities",
            "Consumer Defensive",
            "Healthcare",
            "Real Estate",
            "Energy",
            "Basic Materials",
        ]
        sector_summary = []
        for j, s in enumerate(sectors):
            r = 0.15 + j * 0.03
            sector_summary.append(
                make_sector_summary_row(
                    sector=s,
                    ratio=round(r, 4),
                    ma_10=round(r - 0.01, 4),
                    trend="Up",
                    slope=0.003,
                    status="Normal",
                )
            )
            sector_summary[-1]["Count"] = int(r * 50)
            sector_summary[-1]["Total"] = 50

        # sector_latest (worksheet -> latest row)
        ws_map = {
            "Technology": "sec_technology",
            "Consumer Cyclical": "sec_consumercyclical",
            "Communication Services": "sec_communicationservices",
            "Financial": "sec_financial",
            "Industrials": "sec_industrials",
            "Utilities": "sec_utilities",
            "Consumer Defensive": "sec_consumerdefensive",
            "Healthcare": "sec_healthcare",
            "Real Estate": "sec_realestate",
            "Energy": "sec_energy",
            "Basic Materials": "sec_basicmaterials",
        }
        sector_latest = {}
        for j, s in enumerate(sectors):
            r = 0.15 + j * 0.03
            ws_key = ws_map[s]
            sector_latest[ws_key] = make_timeseries_row(
                ratio=round(r, 4),
                ma_10=round(r - 0.01, 4),
                slope=0.003,
                trend="up",
                worksheet=ws_key,
                date="2026-01-20",
                count=int(r * 50),
                total=50,
            )

        return all_timeseries, latest_all, sector_summary, sector_latest

    def test_calculators_accept_fmp_output(self):
        """All 5 calculators produce valid scores from FMP-format data."""
        from calculators.historical_context_calculator import calculate_historical_context
        from calculators.market_breadth_calculator import calculate_market_breadth
        from calculators.momentum_calculator import calculate_momentum
        from calculators.sector_participation_calculator import calculate_sector_participation
        from calculators.sector_rotation_calculator import calculate_sector_rotation

        all_ts, latest_all, sector_summary, sector_latest = self._make_fmp_style_data()

        # Component 1: Market Breadth
        c1 = calculate_market_breadth(latest_all, all_ts)
        assert 0 <= c1["score"] <= 100
        assert "signal" in c1

        # Component 2: Sector Participation
        c2 = calculate_sector_participation(sector_summary, sector_latest)
        assert 0 <= c2["score"] <= 100

        # Component 3: Sector Rotation
        c3 = calculate_sector_rotation(sector_summary, sector_latest)
        assert 0 <= c3["score"] <= 100

        # Component 4: Momentum
        c4 = calculate_momentum(all_ts, sector_summary)
        assert 0 <= c4["score"] <= 100

        # Component 5: Historical Context
        c5 = calculate_historical_context(all_ts)
        assert 0 <= c5["score"] <= 100


class TestPartialCoverage:
    """Test behavior when coverage is below minimum."""

    def test_partial_coverage_warning(self, capsys):
        """Coverage below min_coverage should print warning."""
        client = FMPUptrendClient.__new__(FMPUptrendClient)
        client.api_key = "test"
        client.cache_dir = "/tmp/test_cache"
        client.max_api_calls = 245
        client.min_coverage = 0.8
        client.session = MagicMock()
        client._last_call_time = 0.0
        client.api_calls_made = 0
        client._rate_limit_reached = False

        # Mock get_stock_universe to return 100 symbols
        symbols = [f"SYM{i}" for i in range(100)]
        sector_map = {s: "Technology" for s in symbols}

        with patch.object(
            client,
            "get_stock_universe",
            return_value={"symbols": symbols, "sector_map": sector_map},
        ):
            # Mock _get_cached_or_fetch to return data for only 50 symbols
            call_count = 0

            def mock_fetch(sym, budget):
                nonlocal call_count
                call_count += 1
                if call_count <= 50:
                    return _make_uptrend_prices(n=300)
                return []

            with patch.object(client, "_get_cached_or_fetch", side_effect=mock_fetch):
                client.calculate_uptrend_data()

            captured = capsys.readouterr()
            assert "WARNING" in captured.err
            assert "below" in captured.err
