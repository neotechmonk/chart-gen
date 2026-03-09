"""Abstract base for shape providers."""

from abc import ABC, abstractmethod


class BaseShapeProvider(ABC):
    """Syncs shape geometry from dataframe to scene graph."""

    def __init__(self, scene_graph):
        self.scene = scene_graph
        self.handle: str | None = None

    @abstractmethod
    def sync(self, df) -> None:
        """Update scene with shape data derived from df."""
        pass
