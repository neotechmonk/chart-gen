"""Registry for shape providers (extensible registration)."""

from typing import Type

from .base import BaseShapeProvider


class ShapeRegistry:
    """Registry of shape provider classes. Add custom shapes without modifying engine."""

    _registry: dict[str, Type[BaseShapeProvider]] = {}

    @classmethod
    def register(cls, name: str):
        """Decorator to register a shape provider class."""

        def _register(shape_cls: Type[BaseShapeProvider]):
            cls._registry[name] = shape_cls
            return shape_cls

        return _register

    @classmethod
    def get(cls, name: str) -> Type[BaseShapeProvider] | None:
        return cls._registry.get(name)

    @classmethod
    def all(cls) -> dict[str, Type[BaseShapeProvider]]:
        return dict(cls._registry)

    @classmethod
    def create_instances(cls, scene_graph, *names: str) -> list[BaseShapeProvider]:
        """Create shape instances by name."""
        return [cls._registry[n](scene_graph) for n in names if n in cls._registry]
