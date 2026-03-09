"""Tests for data providers (logic only)."""

import pandas as pd
import pytest
from unittest.mock import patch, MagicMock

from chart_gen.providers import YFinanceProvider


def test_yfinance_provider_returns_dataframe():
    mock_df = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=120, freq="h"),
            "Open": [100.0] * 120,
            "High": [101.0] * 120,
            "Low": [99.0] * 120,
            "Close": [100.5] * 120,
        }
    )
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = mock_df

    with patch("chart_gen.providers.yfinance_provider.yf") as mock_yf:
        mock_yf.Ticker.return_value = mock_ticker
        provider = YFinanceProvider()
        result = provider.get_data("MSFT", "1h", 100)

    assert isinstance(result, pd.DataFrame)
    assert "Close" in result.columns
    assert "High" in result.columns
    assert "Low" in result.columns
    assert "Open" in result.columns


def test_yfinance_provider_tail_count_plus_buffer():
    mock_df = pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=200, freq="h"),
            "Open": [100.0] * 200,
            "High": [101.0] * 200,
            "Low": [99.0] * 200,
            "Close": [100.5] * 200,
        }
    )
    mock_ticker = MagicMock()
    mock_ticker.history.return_value = mock_df

    with patch("chart_gen.providers.yfinance_provider.yf") as mock_yf:
        mock_yf.Ticker.return_value = mock_ticker
        provider = YFinanceProvider()
        result = provider.get_data("AAPL", "1h", 100)

    # count=100, buffer=15, so tail(115)
    assert len(result) == 115
