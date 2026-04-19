"""Decorators for ACT tool functions."""

from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable

from act_sdk.schema import params_schema


@dataclass
class ToolInfo:
    """Metadata collected from @tool decorator."""

    name: str
    description: str
    parameters_schema: str  # JSON string
    func: Callable
    read_only: bool = False
    idempotent: bool = False
    destructive: bool = False
    timeout_ms: int | None = None


def tool(
    description: str,
    *,
    read_only: bool = False,
    idempotent: bool = False,
    destructive: bool = False,
    timeout_ms: int | None = None,
) -> Callable:
    """Mark an async method as an ACT tool.

    Collects metadata and JSON schema at decoration time.
    """

    def decorator(func: Callable) -> Callable:
        schema = params_schema(func)
        tool_name = func.__name__

        info = ToolInfo(
            name=tool_name,
            description=description,
            parameters_schema=json.dumps(schema),
            func=func,
            read_only=read_only,
            idempotent=idempotent,
            destructive=destructive,
            timeout_ms=timeout_ms,
        )

        func._act_tool = info  # type: ignore[attr-defined]
        return func

    return decorator
