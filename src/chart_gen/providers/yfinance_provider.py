"""YFinance data provider implementation."""

import yfinance as yf

from .base import BaseProvider


class YFinanceProvider(BaseProvider):
    """Fetches data via yfinance API."""

    def get_data(self, symbol: str, interval: str, count: int):
        buffer = int(count * 0.15)
        df = yf.Ticker(symbol).history(period="1mo", interval=interval)
        return df.tail(count + buffer).copy().reset_index()
