"""WIT ToolProvider bridge — connects @component class to componentize-py exports."""

from __future__ import annotations

import traceback
from typing import Any

import cbor2

from act_sdk.decorators import ToolInfo
from act_sdk.errors import ActError
from act_sdk.response import encode_response

# Global registry — set by @component decorator
_registered_component: Any = None
_tool_registry: dict[str, ToolInfo] = {}


def component(cls: type) -> type:
    """Register a class as the ACT component.

    Scans for @tool-decorated methods and registers them.
    """
    global _registered_component, _tool_registry

    instance = cls()
    _registered_component = instance
    _tool_registry = {}

    for attr_name in dir(cls):
        attr = getattr(cls, attr_name, None)
        if callable(attr) and hasattr(attr, "_act_tool"):
            info: ToolInfo = attr._act_tool
            _tool_registry[info.name] = info

    return cls


def get_tool_definitions() -> list[tuple[str, str, str, list[tuple[str, bytes]]]]:
    """Return tool definitions as (name, description, schema_json, metadata) tuples."""
    defs = []
    for info in _tool_registry.values():
        metadata: list[tuple[str, bytes]] = []
        if info.read_only:
            metadata.append(("std:read-only", cbor2.dumps(True)))
        if info.idempotent:
            metadata.append(("std:idempotent", cbor2.dumps(True)))
        if info.destructive:
            metadata.append(("std:destructive", cbor2.dumps(True)))
        if info.timeout_ms is not None:
            metadata.append(("std:timeout-ms", cbor2.dumps(info.timeout_ms)))
        defs.append((info.name, info.description, info.parameters_schema, metadata))
    return defs


async def dispatch_tool(name: str, arguments: bytes) -> tuple[bytes, str] | tuple[str, str, str]:
    """Dispatch a tool call. Returns (data, mime) on success or (kind, message, "error") on error."""
    info = _tool_registry.get(name)
    if info is None:
        return ("std:not-found", f"Unknown tool: {name}", "error")

    try:
        args = cbor2.loads(arguments) if arguments else {}
        result = await info.func(_registered_component, **args)
        return encode_response(result)
    except ActError as e:
        return (e.kind, e.message, "error")
    except Exception:
        return ("std:internal", traceback.format_exc(), "error")
