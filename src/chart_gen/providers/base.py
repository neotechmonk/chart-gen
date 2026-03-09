"""Abstract base for data providers."""

from abc import ABC, abstractmethod


class BaseProvider(ABC):
    """Abstract data provider interface."""

    @abstractmethod
    def get_data(self, symbol: str, interval: str, count: int):
        """Fetch OHLCV data for symbol."""
        pass
