"""Tests for shape providers (logic only, no visual)."""

import pandas as pd
import pytest

from chart_gen.scene import SceneGraph
from chart_gen.shapes import PivotLegShape, RejectionZoneShape


def test_pivot_leg_sync_adds_line_shape(sample_ohlcv_df):
    scene = SceneGraph()
    shape = PivotLegShape(scene)
    shape.sync(sample_ohlcv_df)

    render_list = scene.get_render_list()
    assert len(render_list) == 1
    el = render_list[0]
    assert el["type"] == "line"
    assert el["color"] == "orange"
    assert el["style"] == "--"
    assert len(el["x"]) == 2
    assert el["x"][1] == len(sample_ohlcv_df) - 1
    assert el["x"][0] == el["x"][1] - 60


def test_pivot_leg_sync_updates_on_second_call(sample_ohlcv_df):
    scene = SceneGraph()
    shape = PivotLegShape(scene)
    shape.sync(sample_ohlcv_df)
    first_y = scene.get_render_list()[0]["y"]

    # Append a row to simulate new data
    new_row = sample_ohlcv_df.iloc[-1:].copy()
    new_row["Close"] = 500.0
    new_row["High"] = 501.0
    extended_df = pd.concat([sample_ohlcv_df, new_row], ignore_index=True)

    shape.sync(extended_df)
    second_y = scene.get_render_list()[0]["y"]
    assert second_y[1] == 500.0
    assert len(scene.get_render_list()) == 1  # still one shape, updated


def test_rejection_zone_sync_adds_zone_once(sample_ohlcv_df):
    scene = SceneGraph()
    shape = RejectionZoneShape(scene)
    shape.sync(sample_ohlcv_df)

    render_list = scene.get_render_list()
    assert len(render_list) == 1
    el = render_list[0]
    assert el["type"] == "zone"
    assert el["y1"] == 400
    assert el["y2"] == 405
    assert el["color"] == "#88d8b0"
    assert el["alpha"] == 0.15


def test_rejection_zone_sync_idempotent(sample_ohlcv_df):
    scene = SceneGraph()
    shape = RejectionZoneShape(scene)
    shape.sync(sample_ohlcv_df)
    shape.sync(sample_ohlcv_df)
    shape.sync(sample_ohlcv_df)
    assert len(scene.get_render_list()) == 1
