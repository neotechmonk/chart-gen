# chart-gen

Chart generation with extensible data providers and shape overlays. OHLCV data → scene graph (UUID-keyed shapes) → matplotlib renderer.

## Setup

```bash
uv sync
```

## Run

```bash
uv run python -m chart_gen
```

## Tests

```bash
uv run pytest
```

## Architecture

- **Providers** (`providers/`): Abstract `BaseProvider`, `YFinanceProvider` — fetch OHLCV.
- **Scene** (`scene/`): `SceneGraph` — add/update shapes by UUID, `get_render_list()` for renderer.
- **Shapes** (`shapes/`): `BaseShapeProvider`, `ShapeRegistry` — sync df → scene. Built-in: `pivot_leg`, `rejection_zone`.
- **Renderers** (`renderers/`): `MplRenderer` — draws candles + scene graph.

Extensibility: register shapes via `@ShapeRegistry.register("name")`; inject custom provider/shape classes into `run_engine()`.
