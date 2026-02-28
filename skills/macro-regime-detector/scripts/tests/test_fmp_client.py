"""Tests for FMP client yfinance fallback functionality."""

import os
import sys
from datetime import datetime
from unittest.mock import patch

import pytest

# Ensure scripts directory is on the path (conftest handles this too)
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def client():
    """Create an FMPClient with a dummy API key."""
    with patch.dict(os.environ, {"FMP_API_KEY": "test_key"}):
        from fmp_client import FMPClient

        c = FMPClient(api_key="test_key")
        return c


def _make_yf_dataframe(days=5, multi_index=False):
    """Create a mock yfinance-style DataFrame.

    Args:
        days: Number of rows to generate.
        multi_index: If True, create MultiIndex columns like yfinance 0.2.31+.
    """
    import pandas as pd

    # Use calendar days from a known weekday to avoid business-day edge cases
    dates = pd.date_range(end="2026-02-27", periods=days, freq="D")
    data = {
        "Open": [100.0 + i for i in range(days)],
        "High": [102.0 + i for i in range(days)],
        "Low": [99.0 + i for i in range(days)],
        "Close": [101.0 + i for i in range(days)],
        "Adj Close": [100.5 + i for i in range(days)],
        "Volume": [1000000 + i * 10000 for i in range(days)],
    }
    df = pd.DataFrame(data, index=dates)

    if multi_index:
        # Simulate yfinance 0.2.31+ multi-level columns: (Price, Ticker)
        df.columns = pd.MultiIndex.from_tuples(
            [(col, "SPY") for col in df.columns], names=["Price", "Ticker"]
        )

    return df


class TestYfinanceFallbackTrigger:
    """Test that yfinance fallback triggers when FMP returns None."""

    def test_fallback_triggers_on_fmp_none(self, client):
        """When FMP returns None, yfinance should be tried."""
        df = _make_yf_dataframe(days=5)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("RSP", days=30)

        assert result is not None
        assert result["symbol"] == "RSP"
        assert "historical" in result
        assert len(result["historical"]) == 5

    def test_fallback_triggers_on_fmp_empty_list(self, client):
        """When FMP returns empty list, yfinance should be tried."""
        df = _make_yf_dataframe(days=3)

        with (
            patch.object(client, "_rate_limited_get", return_value=[]),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("TLT", days=30)

        assert result is not None
        assert result["symbol"] == "TLT"
        assert len(result["historical"]) == 3

    def test_no_fallback_when_fmp_succeeds(self, client):
        """When FMP succeeds, yfinance should NOT be called."""
        fmp_data = [
            {"date": "2026-02-27", "open": 100, "high": 102, "low": 99,
             "close": 101, "adjClose": 100.5, "volume": 1000000},
        ]

        with (
            patch.object(client, "_rate_limited_get", return_value=fmp_data),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            result = client.get_historical_prices("SPY", days=30)

        mock_yf.download.assert_not_called()
        assert result is not None
        assert result["historical"] == fmp_data


class TestYfinanceDataFormat:
    """Test that yfinance data is converted to FMP-compatible format."""

    def test_correct_keys_present(self, client):
        """Output dicts must have date, open, high, low, close, adjClose, volume."""
        df = _make_yf_dataframe(days=3)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("RSP", days=30)

        bar = result["historical"][0]
        required_keys = {"date", "open", "high", "low", "close", "adjClose", "volume"}
        assert required_keys.issubset(bar.keys())

    def test_date_is_string_format(self, client):
        """Dates must be YYYY-MM-DD strings."""
        df = _make_yf_dataframe(days=3)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("RSP", days=30)

        for bar in result["historical"]:
            # Validate YYYY-MM-DD format
            datetime.strptime(bar["date"], "%Y-%m-%d")

    def test_numeric_values(self, client):
        """Price and volume values must be numeric."""
        df = _make_yf_dataframe(days=3)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("RSP", days=30)

        bar = result["historical"][0]
        for key in ("open", "high", "low", "close", "adjClose", "volume"):
            assert isinstance(bar[key], (int, float))


class TestDataOrdering:
    """Test that yfinance data is sorted most-recent-first (FMP convention)."""

    def test_most_recent_first(self, client):
        """Historical data should be sorted descending by date."""
        df = _make_yf_dataframe(days=10)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("IWM", days=30)

        dates = [bar["date"] for bar in result["historical"]]
        assert dates == sorted(dates, reverse=True)


class TestNoYfinanceInstalled:
    """Test behavior when yfinance is not installed."""

    def test_returns_none_without_yfinance(self, client):
        """When HAS_YFINANCE is False, fallback should be skipped and return None."""
        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", False),
        ):
            result = client.get_historical_prices("RSP", days=30)

        assert result is None


class TestMultiIndexHandling:
    """Test that multi-level column DataFrames (yfinance 0.2.31+) are handled."""

    def test_multi_index_columns_flattened(self, client):
        """MultiIndex columns should be flattened to simple column names."""
        df = _make_yf_dataframe(days=5, multi_index=True)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("RSP", days=30)

        assert result is not None
        bar = result["historical"][0]
        assert "adjClose" in bar
        assert "close" in bar
        assert len(result["historical"]) == 5


class TestApiStats:
    """Test that API stats include yfinance fallback count."""

    def test_yf_fallback_count_in_stats(self, client):
        """get_api_stats should include yf_fallback_count."""
        stats = client.get_api_stats()
        assert "yf_fallback_count" in stats
        assert stats["yf_fallback_count"] == 0

    def test_yf_fallback_count_increments(self, client):
        """yf_fallback_count should increment on each fallback use."""
        df = _make_yf_dataframe(days=3)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            client.get_historical_prices("RSP", days=30)
            client.get_historical_prices("TLT", days=30)

        assert client.get_api_stats()["yf_fallback_count"] == 2


class TestYfinanceEmptyDataFrame:
    """Test handling of empty DataFrame from yfinance."""

    def test_empty_dataframe_returns_none(self, client):
        """When yfinance returns an empty DataFrame, should return None."""
        import pandas as pd

        empty_df = pd.DataFrame()

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = empty_df
            result = client.get_historical_prices("BADTICKER", days=30)

        assert result is None


class TestCacheWithFallback:
    """Test that yfinance fallback results are cached."""

    def test_cached_after_yf_fallback(self, client):
        """Second call for same symbol should return cached result, not call yfinance again."""
        df = _make_yf_dataframe(days=3)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result1 = client.get_historical_prices("RSP", days=30)
            result2 = client.get_historical_prices("RSP", days=30)

        # yfinance should only be called once due to caching
        assert mock_yf.download.call_count == 1
        assert result1 == result2
