"""Orchestrator for chart generation pipeline."""

from pathlib import Path
from typing import Sequence, Type

from .providers import BaseProvider, YFinanceProvider
from .renderers import MplRenderer
from .scene import SceneGraph
from .shapes import BaseShapeProvider, PivotLegShape, RejectionZoneShape, ShapeRegistry


def run_engine(
    symbol: str | Sequence[str] = "MSFT",
    interval: str = "1h",
    bar_count: int = 100,
    provider: BaseProvider | None = None,
    shape_names: Sequence[str] | None = None,
    shape_classes: Sequence[Type[BaseShapeProvider]] | None = None,
    output_dir: str | Path | None = None,
) -> None:
    """Run the full chart generation pipeline.

    Args:
        symbol: Ticker symbol or sequence of symbols.
        interval: Candle interval (e.g. 1h).
        bar_count: Number of bars to display.
        provider: Data provider (default: YFinanceProvider).
        shape_names: Shape names from registry (default: pivot_leg, rejection_zone).
        shape_classes: Explicit shape classes (overrides shape_names if both given).
        output_dir: If set with multiple symbols, save charts here instead of showing.
    """
    symbols = [symbol] if isinstance(symbol, str) else list(symbol)
    provider = provider or YFinanceProvider()
    renderer = MplRenderer()
    out_dir = Path(output_dir) if output_dir else None

    for sym in symbols:
        scene = SceneGraph()
        if shape_classes:
            shapes = [cls(scene) for cls in shape_classes]
        elif shape_names:
            shapes = ShapeRegistry.create_instances(scene, *shape_names)
        else:
            shapes = [PivotLegShape(scene), RejectionZoneShape(scene)]

        data = provider.get_data(sym, interval, bar_count)

        for s in shapes:
            s.sync(data)

        save_path = (out_dir / f"{sym}.png") if out_dir else None
        renderer.render(sym, interval, data, scene, bar_count, save_path=save_path)
