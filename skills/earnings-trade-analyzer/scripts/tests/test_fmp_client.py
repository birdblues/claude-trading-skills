"""Tests for FMP Client error detection and yfinance fallback."""

import os
import sys
from datetime import datetime
from unittest.mock import patch

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))


@pytest.fixture
def client():
    """Create an FMPClient with a dummy API key."""
    with patch.dict(os.environ, {"FMP_API_KEY": "test_key"}):
        from fmp_client import FMPClient

        c = FMPClient(api_key="test_key")
        return c


def _make_yf_dataframe(days=5, multi_index=False):
    """Create a mock yfinance-style DataFrame."""
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
            [(col, "AAPL") for col in df.columns], names=["Price", "Ticker"]
        )

    return df


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


class TestYfinanceFallbackTrigger:
    """Test that yfinance fallback triggers when FMP returns None for historical."""

    def test_fallback_triggers_on_fmp_none(self, client):
        """When FMP returns None, yfinance should be tried for historical."""
        df = _make_yf_dataframe(days=5)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("AAPL", days=30)

        assert result is not None
        # Earnings-trade-analyzer returns flat list, not wrapped dict
        assert isinstance(result, list)
        assert len(result) == 5

    def test_fallback_triggers_on_fmp_error_dict(self, client):
        """When FMP returns error dict, yfinance should be tried."""
        error_response = {"Error": "Limit Reach. Please upgrade your plan."}
        df = _make_yf_dataframe(days=5)

        with (
            patch.object(client, "_rate_limited_get", return_value=error_response),
            patch("fmp_client.HAS_YFINANCE", True),
            patch("fmp_client.yf") as mock_yf,
        ):
            mock_yf.download.return_value = df
            result = client.get_historical_prices("AAPL", days=30)

        assert result is not None
        assert isinstance(result, list)
        assert len(result) == 5
        assert client.yf_fallback_count == 1

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
            result = client.get_historical_prices("AAPL", days=30)

        mock_yf.download.assert_not_called()
        assert result is not None


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
            result = client.get_historical_prices("AAPL", days=30)

        bar = result[0]
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
            result = client.get_historical_prices("AAPL", days=30)

        for bar in result:
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
            result = client.get_historical_prices("AAPL", days=30)

        bar = result[0]
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
            result = client.get_historical_prices("AAPL", days=30)

        dates = [bar["date"] for bar in result]
        assert dates == sorted(dates, reverse=True)
