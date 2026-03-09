"""Tests for SceneGraph logic."""

import pytest

from chart_gen.scene import SceneGraph


def test_add_returns_uuid():
    scene = SceneGraph()
    uid = scene.add({"type": "line", "x": [0, 1], "y": [0, 1]})
    assert uid is not None
    assert len(uid) == 36  # UUID format


def test_add_stores_shape_data():
    scene = SceneGraph()
    data = {"type": "zone", "x": [0, 10], "y1": 100, "y2": 105}
    uid = scene.add(data)
    render_list = scene.get_render_list()
    assert len(render_list) == 1
    assert render_list[0]["type"] == "zone"
    assert render_list[0]["y1"] == 100


def test_update_modifies_existing():
    scene = SceneGraph()
    uid = scene.add({"type": "line", "x": [0, 1], "y": [0, 1], "color": "red"})
    scene.update(uid, {"color": "blue"})
    render_list = scene.get_render_list()
    assert render_list[0]["color"] == "blue"
    assert render_list[0]["x"] == [0, 1]


def test_update_nonexistent_does_not_raise():
    scene = SceneGraph()
    scene.update("nonexistent-uuid", {"color": "blue"})  # should not raise
    assert scene.get_render_list() == []


def test_get_render_list_returns_all_shapes():
    scene = SceneGraph()
    scene.add({"type": "line"})
    scene.add({"type": "zone"})
    render_list = scene.get_render_list()
    assert len(render_list) == 2
    types = {r["type"] for r in render_list}
    assert types == {"line", "zone"}
