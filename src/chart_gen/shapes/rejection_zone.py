"""Rejection zone horizontal band shape."""

from .base import BaseShapeProvider
from .registry import ShapeRegistry


@ShapeRegistry.register("rejection_zone")
class RejectionZoneShape(BaseShapeProvider):
    """Static zone added once and persisted."""

    def sync(self, df) -> None:
        if not self.handle:
            last_idx = len(df) - 1
            self.handle = self.scene.add(
                {
                    "type": "zone",
                    "x": [last_idx - 30, last_idx],
                    "y1": 400,
                    "y2": 405,
                    "color": "#88d8b0",
                    "alpha": 0.15,
                }
            )
