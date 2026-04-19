"""WIT bridge for componentize-py — auto-generates ToolProvider export.

Usage in app.py:

    from act_sdk import component, tool
    from act_sdk.bridge import ToolProvider  # noqa: F401 — componentize-py entry point

    @component
    class MyComponent:
        @tool(description="Do something")
        async def my_tool(self, arg: str) -> str:
            return f"result: {arg}"

The ToolProvider class is the componentize-py export. It delegates to the
@component/@tool registry automatically.
"""

from __future__ import annotations

import traceback

from wit_world import exports
from wit_world.imports.types import (
    Error,
    LocalizedString_Plain,
)
from wit_world.exports.tool_provider import (
    ContentPart,
    ListToolsResponse,
    ToolDefinition,
    ToolEvent_Content,
    ToolEvent_Error,
    ToolResult_Immediate,
)

from act_sdk.provider import dispatch_tool, get_tool_definitions


class ToolProvider(exports.ToolProvider):
    """componentize-py export — bridges WIT interface to @component/@tool registry."""

    async def list_tools(self, metadata):
        defs = get_tool_definitions()
        return ListToolsResponse(
            metadata=[],
            tools=[
                ToolDefinition(
                    name=name,
                    description=LocalizedString_Plain(value=desc),
                    parameters_schema=schema,
                    metadata=meta,
                )
                for name, desc, schema, meta in defs
            ],
        )

    async def call_tool(self, name, arguments, metadata):
        try:
            result = await dispatch_tool(name, bytes(arguments))
            if len(result) == 3 and result[2] == "error":
                kind, message, _ = result
                event = ToolEvent_Error(
                    Error(
                        kind=kind,
                        message=LocalizedString_Plain(value=message),
                        metadata=[],
                    )
                )
            else:
                data, mime = result
                event = ToolEvent_Content(
                    ContentPart(
                        data=data,
                        mime_type=mime,
                        metadata=[],
                    )
                )
        except Exception:
            event = ToolEvent_Error(
                Error(
                    kind="std:internal",
                    message=LocalizedString_Plain(value=traceback.format_exc()),
                    metadata=[],
                )
            )
        return ToolResult_Immediate([event])
