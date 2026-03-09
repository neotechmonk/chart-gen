"""Tests for ShapeRegistry (extensibility)."""

import pytest

from chart_gen.scene import SceneGraph
from chart_gen.shapes import ShapeRegistry


def test_registry_has_builtin_shapes():
    all_shapes = ShapeRegistry.all()
    assert "pivot_leg" in all_shapes
    assert "rejection_zone" in all_shapes


def test_create_instances_by_name(sample_ohlcv_df):
    scene = SceneGraph()
    shapes = ShapeRegistry.create_instances(scene, "pivot_leg", "rejection_zone")
    assert len(shapes) == 2
    for s in shapes:
        s.sync(sample_ohlcv_df)
    render_list = scene.get_render_list()
    assert len(render_list) == 2
    types = {r["type"] for r in render_list}
    assert types == {"line", "zone"}


def test_create_instances_ignores_unknown():
    scene = SceneGraph()
    shapes = ShapeRegistry.create_instances(scene, "pivot_leg", "unknown_shape")
    assert len(shapes) == 1
