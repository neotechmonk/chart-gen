"""Pytest fixtures."""

import pandas as pd
import pytest


@pytest.fixture
def sample_ohlcv_df():
    """Minimal OHLCV dataframe for shape logic tests."""
    n = 100
    return pd.DataFrame(
        {
            "Date": pd.date_range("2024-01-01", periods=n, freq="h"),
            "Open": [400.0 + i * 0.5 for i in range(n)],
            "High": [401.0 + i * 0.5 for i in range(n)],
            "Low": [399.0 + i * 0.5 for i in range(n)],
            "Close": [400.5 + i * 0.5 for i in range(n)],
        }
    )
