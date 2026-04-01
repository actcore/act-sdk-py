"""Type hint → JSON Schema conversion for ACT tool parameters."""

from __future__ import annotations

import inspect
import types as _types
import typing as _typing
from typing import Any, Callable, get_args, get_origin


_PY_TYPE_TO_JSON: dict[type, str] = {
    str: "string",
    int: "integer",
    float: "number",
    bool: "boolean",
    bytes: "string",  # base64-encoded in JSON context
    list: "array",
    dict: "object",
}


def _annotation_to_schema(annotation: Any) -> dict[str, Any]:
    """Convert a single type annotation to a JSON Schema fragment."""
    if annotation is inspect.Parameter.empty:
        return {}

    origin = get_origin(annotation)
    args = get_args(annotation)

    # Optional[X] / Union[X, None]
    if origin is _typing.Union or origin is getattr(_types, "UnionType", None):
        non_none = [a for a in args if a is not type(None)]
        if len(non_none) == 1:
            return _annotation_to_schema(non_none[0])
        return {"oneOf": [_annotation_to_schema(a) for a in non_none]}

    # list[X]
    if origin is list:
        schema: dict[str, Any] = {"type": "array"}
        if args:
            schema["items"] = _annotation_to_schema(args[0])
        return schema

    # dict[K, V]
    if origin is dict:
        schema = {"type": "object"}
        if len(args) >= 2:
            schema["additionalProperties"] = _annotation_to_schema(args[1])
        return schema

    # Plain types
    if annotation in _PY_TYPE_TO_JSON:
        return {"type": _PY_TYPE_TO_JSON[annotation]}

    # Fallback — unknown type, no constraint
    return {}


def _is_optional(annotation: Any) -> bool:
    """Return True if *annotation* is Optional[X] (i.e. Union[X, None])."""
    origin = get_origin(annotation)
    if origin is _typing.Union or origin is getattr(_types, "UnionType", None):
        return any(a is type(None) for a in get_args(annotation))
    return False


def params_schema(func: Callable) -> dict[str, Any]:
    """Return a JSON Schema *object* describing the parameters of *func*.

    ``self`` and parameters with no annotation are skipped.
    The return annotation is ignored.
    Optional[X] parameters are not listed in ``required`` even without a default.
    """
    sig = inspect.signature(func)
    properties: dict[str, Any] = {}
    required: list[str] = []

    for name, param in sig.parameters.items():
        if name == "self":
            continue

        prop = _annotation_to_schema(param.annotation)

        if param.default is not inspect.Parameter.empty:
            prop = dict(prop)  # copy before mutating
            prop["default"] = param.default
        elif not _is_optional(param.annotation):
            required.append(name)

        properties[name] = prop

    schema: dict[str, Any] = {"type": "object", "properties": properties}
    if required:
        schema["required"] = required
    return schema
