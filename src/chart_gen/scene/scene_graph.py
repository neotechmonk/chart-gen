"""Stateful scene graph storing shape overlays by UUID."""

import uuid
from datetime import datetime


class SceneGraph:
    """Registry of shapes keyed by UUID for add/update semantics."""

    def __init__(self):
        self._registry: dict[str, dict] = {}

    def add(self, shape_data: dict) -> str:
        """Create a shape and return its UUID."""
        obj_id = str(uuid.uuid4())
        now = datetime.now()
        self._registry[obj_id] = {
            "id": obj_id,
            "data": shape_data,
            "created_at": now,
            "updated_at": now,
        }
        return obj_id

    def update(self, obj_id: str, new_data: dict) -> None:
        """Update an existing shape by UUID."""
        if obj_id in self._registry:
            self._registry[obj_id]["data"].update(new_data)
            self._registry[obj_id]["updated_at"] = datetime.now()
        else:
            print(f"Warning: Attempted to update non-existent UUID {obj_id}")

    def get_render_list(self) -> list[dict]:
        """Return all shape data for rendering."""
        return [item["data"] for item in self._registry.values()]
