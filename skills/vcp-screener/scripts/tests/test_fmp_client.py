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


def _make_wiki_sp500_dataframe(n=5):
    """Create a mock Wikipedia S&P 500 table DataFrame."""
    import pandas as pd

    symbols = ["AAPL", "MSFT", "GOOGL", "AMZN", "BRK.B"][:n]
    names = [
        "Apple Inc.",
        "Microsoft Corp",
        "Alphabet Inc.",
        "Amazon.com Inc.",
        "Berkshire Hathaway",
    ][:n]
    sectors = [
        "Information Technology",
        "Information Technology",
        "Communication Services",
        "Consumer Discretionary",
        "Financials",
    ][:n]
    sub_industries = [
        "Technology Hardware",
        "Systems Software",
        "Interactive Media",
        "Internet Retail",
        "Multi-Sector Holdings",
    ][:n]

    return pd.DataFrame(
        {
            "Symbol": symbols,
            "Security": names,
            "GICS Sector": sectors,
            "GICS Sub-Industry": sub_industries,
            "Headquarters Location": ["Cupertino, CA"] * n,
            "Date added": ["1982-11-30"] * n,
            "CIK": [320193] * n,
            "Founded": ["1976"] * n,
        }
    )


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
            [(col, "SPY") for col in df.columns], names=["Price", "Ticker"]
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
            result = client.get_historical_prices("SPY", days=30)

        assert result is not None
        assert result["symbol"] == "SPY"
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
            result = client.get_historical_prices("SPY", days=30)

        assert result is not None
        assert result["symbol"] == "SPY"
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
            result = client.get_historical_prices("SPY", days=30)

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
            result = client.get_historical_prices("SPY", days=30)

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
            result = client.get_historical_prices("SPY", days=30)

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
            result = client.get_historical_prices("SPY", days=30)

        dates = [bar["date"] for bar in result["historical"]]
        assert dates == sorted(dates, reverse=True)


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
            client.get_historical_prices("SPY", days=30)
            client.get_historical_prices("QQQ", days=30)

        assert client.get_api_stats()["yf_fallback_count"] == 2


class TestFmpErrorResponseFallback:
    """Test that yfinance fallback triggers on FMP 200 + error payloads."""

    def test_quote_fallback_on_error_dict(self, client):
        """FMP returning {"Error": "..."} for quote should trigger yfinance fallback."""
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
        assert client.yf_fallback_count == 1

    def test_historical_fallback_on_error_dict(self, client):
        """FMP returning error dict for historical should trigger yfinance fallback."""
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


def _mock_wiki_response(wiki_df):
    """Create a mock requests.Response that returns HTML parseable by pd.read_html."""
    mock_resp = type("MockResponse", (), {})()
    mock_resp.status_code = 200
    mock_resp.text = wiki_df.to_html()
    mock_resp.raise_for_status = lambda: None
    return mock_resp


class TestSp500WikipediaFallbackTrigger:
    """Test that Wikipedia fallback triggers when FMP returns None for S&P 500."""

    def test_fallback_triggers_on_fmp_none(self, client):
        """When FMP returns None for sp500, Wikipedia should be tried."""
        wiki_df = _make_wiki_sp500_dataframe(n=5)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.requests.get", return_value=_mock_wiki_response(wiki_df)),
            patch("fmp_client.pd.read_html", return_value=[wiki_df]),
        ):
            result = client.get_sp500_constituents()

        assert result is not None
        assert len(result) == 5
        assert result[0]["symbol"] == "AAPL"

    def test_no_fallback_when_fmp_succeeds(self, client):
        """When FMP succeeds, Wikipedia should NOT be called."""
        fmp_data = [
            {
                "symbol": "AAPL",
                "name": "Apple Inc.",
                "sector": "Technology",
                "subSector": "Hardware",
            },
        ]

        with (
            patch.object(client, "_rate_limited_get", return_value=fmp_data),
            patch("fmp_client.requests.get") as mock_requests_get,
        ):
            result = client.get_sp500_constituents()

        mock_requests_get.assert_not_called()
        assert result == fmp_data

    def test_both_fail_returns_none(self, client):
        """When both FMP and Wikipedia fail, should return None."""
        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch(
                "fmp_client.requests.get", side_effect=Exception("Network error")
            ),
        ):
            result = client.get_sp500_constituents()

        assert result is None


class TestSp500WikipediaDataFormat:
    """Test that Wikipedia data is converted to FMP-compatible format."""

    def test_correct_keys_present(self, client):
        """Output dicts must have symbol, name, sector, subSector keys."""
        wiki_df = _make_wiki_sp500_dataframe(n=3)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.requests.get", return_value=_mock_wiki_response(wiki_df)),
            patch("fmp_client.pd.read_html", return_value=[wiki_df]),
        ):
            result = client.get_sp500_constituents()

        required_keys = {"symbol", "name", "sector", "subSector"}
        for item in result:
            assert required_keys.issubset(item.keys())

    def test_ticker_normalization_dot_to_dash(self, client):
        """BRK.B should be normalized to BRK-B."""
        wiki_df = _make_wiki_sp500_dataframe(n=5)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.requests.get", return_value=_mock_wiki_response(wiki_df)),
            patch("fmp_client.pd.read_html", return_value=[wiki_df]),
        ):
            result = client.get_sp500_constituents()

        symbols = [item["symbol"] for item in result]
        assert "BRK-B" in symbols
        assert "BRK.B" not in symbols


class TestSp500WikipediaStats:
    """Test that API stats include Wikipedia fallback count."""

    def test_wiki_fallback_count_in_stats(self, client):
        """get_api_stats should include wiki_fallback_count."""
        stats = client.get_api_stats()
        assert "wiki_fallback_count" in stats
        assert stats["wiki_fallback_count"] == 0

    def test_wiki_fallback_count_increments(self, client):
        """wiki_fallback_count should increment on Wikipedia fallback use."""
        wiki_df = _make_wiki_sp500_dataframe(n=3)

        with (
            patch.object(client, "_rate_limited_get", return_value=None),
            patch("fmp_client.requests.get", return_value=_mock_wiki_response(wiki_df)),
            patch("fmp_client.pd.read_html", return_value=[wiki_df]),
        ):
            client.get_sp500_constituents()

        assert client.get_api_stats()["wiki_fallback_count"] == 1
