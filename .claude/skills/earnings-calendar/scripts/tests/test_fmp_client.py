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
        df.columns = pd.MultiIndex.from_tuples(
            [(col, "QQQ") for col in df.columns], names=["Price", "Ticker"]
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
            result = client.get_historical_prices("QQQ", days=30)

        assert result is not None
        assert result["symbol"] == "QQQ"
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
            result = client.get_historical_prices("QQQ", days=30)

        assert result is not None
        assert result["symbol"] == "QQQ"
        assert len(result["historical"]) == 3

    def test_no_fallback_when_fmp_succeeds(self, client):
        """When FMP succeeds, yfinance should NOT be called."""
        fmp_data = [
            {
                "date": "2026-02-27",
                "open": 100,
                "high": 102,
                "low": 99,
                "close": 101,
                "adjClose": 100.5,
                "volume": 1000000,
            },
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


class TestYfinanceQuoteFallback:
    """Test that yfinance quote fallback triggers when FMP returns None."""

    def test_quote_fallback_triggers_on_fmp_none(self, client):
        """When FMP returns None for quote, yfinance fast_info should be tried."""
        mock_ticker = type("MockTicker", (), {})()
        mock_ticker.fast_info = {
            "last_price": 450.25,
            "year_high": 510.0,
            "year_low": 380.0,
            "last_volume": 50000000,
        }

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.Ticker.return_value = mock_ticker
            result = client.get_quote("QQQ")

        assert result is not None
        assert len(result) == 1
        assert result[0]["symbol"] == "QQQ"
        assert result[0]["price"] == 450.25
        assert result[0]["yearHigh"] == 510.0
        assert result[0]["yearLow"] == 380.0
        assert result[0]["volume"] == 50000000

    def test_quote_no_fallback_when_fmp_succeeds(self, client):
        """When FMP returns valid quote, yfinance should NOT be called."""
        fmp_quote = [{"symbol": "QQQ", "price": 450.0, "volume": 40000000}]

        with (
            patch.object(client, "_rate_limited_get", return_value=fmp_quote),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            result = client.get_quote("QQQ")

        mock_yf.Ticker.assert_not_called()
        assert result == fmp_quote

    def test_quote_fallback_returns_none_without_yfinance(self, client):
        """When HAS_YFINANCE is False, quote fallback should return None."""
        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", False),
        ):
            result = client.get_quote("QQQ")

        assert result is None

    def test_quote_fallback_increments_counter(self, client):
        """Quote fallback should increment yf_fallback_count."""
        mock_ticker = type("MockTicker", (), {})()
        mock_ticker.fast_info = {
            "last_price": 450.25,
            "year_high": 510.0,
            "year_low": 380.0,
            "last_volume": 50000000,
        }

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.Ticker.return_value = mock_ticker
            client.get_quote("QQQ")

        assert client.yf_fallback_count == 1


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
            result = client.get_historical_prices("QQQ", days=30)

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
            result = client.get_historical_prices("QQQ", days=30)

        for bar in result["historical"]:
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
            result = client.get_historical_prices("QQQ", days=30)

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
            result = client.get_historical_prices("QQQ", days=30)

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
            result = client.get_historical_prices("QQQ", days=30)

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
            result = client.get_historical_prices("QQQ", days=30)

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
            client.get_historical_prices("QQQ", days=30)
            client.get_historical_prices("XLK", days=30)

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


class TestErrorPayloadDetection:
    """Test _is_error_payload() detection of FMP error responses."""

    def test_detects_error_message_key(self, client):
        """FMP 'Error Message' payload should be detected."""
        assert client._is_error_payload({"Error Message": "Invalid API KEY."}) is True

    def test_detects_error_key(self, client):
        """FMP 'Error' payload should be detected."""
        assert client._is_error_payload({"Error": "Limit Reach. Please upgrade your plan."}) is True

    def test_normal_dict_not_flagged(self, client):
        """Normal response dict should NOT be flagged."""
        assert client._is_error_payload({"symbol": "AAPL", "price": 150.0}) is False


class TestFmpErrorResponseFallback:
    """Test that yfinance fallback triggers on FMP 200 + error payloads."""

    def test_fallback_on_fmp_200_with_error_dict(self, client):
        """FMP returning {"Error": "..."} should trigger yfinance fallback."""
        error_response = {"Error": "Limit Reach. Please upgrade your plan."}
        mock_ticker = type("MockTicker", (), {})()
        mock_ticker.fast_info = {
            "last_price": 72.50,
            "year_high": 85.0,
            "year_low": 60.0,
            "last_volume": 3000000,
        }

        with (
            patch.object(client, "_rate_limited_get", return_value=error_response),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.Ticker.return_value = mock_ticker
            result = client.get_quote("XLU")

        assert result is not None
        assert result[0]["symbol"] == "XLU"
        assert result[0]["price"] == 72.50
        assert client.yf_fallback_count == 1

    def test_historical_fallback_on_fmp_error_dict(self, client):
        """FMP returning error dict for historical endpoint triggers yfinance fallback."""
        error_response = {"Error": "Limit Reach. Please upgrade your plan."}
        df = _make_yf_dataframe(days=5)

        with (
            patch.object(client, "_rate_limited_get", return_value=error_response),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("XLU", days=30)

        assert result is not None
        assert result["symbol"] == "XLU"
        assert len(result["historical"]) == 5
        assert client.yf_fallback_count == 1

    def test_fallback_on_json_decode_error(self, client):
        """response.json() failure should return None, not raise."""
        from unittest.mock import MagicMock

        mock_response = MagicMock()
        mock_response.status_code = 200
        mock_response.json.side_effect = ValueError("No JSON object could be decoded")

        with patch.object(client.session, "get", return_value=mock_response):
            result = client._rate_limited_get("https://example.com/api")

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
            result1 = client.get_historical_prices("QQQ", days=30)
            result2 = client.get_historical_prices("QQQ", days=30)

        assert mock_yf.download.call_count == 1
        assert result1 == result2
