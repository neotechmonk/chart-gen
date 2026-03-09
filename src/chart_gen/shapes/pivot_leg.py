"""Pivot leg diagonal line shape."""

from .base import BaseShapeProvider
from .registry import ShapeRegistry


@ShapeRegistry.register("pivot_leg")
class PivotLegShape(BaseShapeProvider):
    """Diagonal line that stretches as new data arrives."""

    def sync(self, df) -> None:
        last_idx = len(df) - 1
        curr_price = df["Close"].iloc[-1]
        start_price = df["High"].iloc[max(0, last_idx - 60)]

        shape_props = {
            "type": "line",
            "x": [last_idx - 60, last_idx],
            "y": [start_price, curr_price],
            "color": "orange",
            "style": "--",
            "width": 2,
        }

        if not self.handle:
            self.handle = self.scene.add(shape_props)
        else:
            self.scene.update(self.handle, shape_props)
