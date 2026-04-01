import asyncio
import cbor2
from act_sdk import component, tool, ActError, Json, Content
from act_sdk.provider import get_tool_definitions, dispatch_tool


@component
class TestComponent:
    @tool(description="Say hello", read_only=True)
    async def hello(self, name: str = "world") -> str:
        return f"Hello, {name}!"

    @tool(description="Add numbers")
    async def add(self, a: int, b: int) -> int:
        return a + b

    @tool(description="Failing tool")
    async def fail(self) -> str:
        raise ActError.not_found("nothing here")

    @tool(description="Return JSON")
    async def as_json(self, data: dict) -> Json[dict]:
        return Json(data)

    @tool(description="Return binary")
    async def binary(self) -> Content:
        return Content("image/png", b"\x89PNG")


def test_tool_definitions():
    defs = get_tool_definitions()
    names = [d[0] for d in defs]
    assert "hello" in names
    assert "add" in names


def test_hello_dispatch():
    args = cbor2.dumps({"name": "Alice"})
    data, mime = asyncio.run(dispatch_tool("hello", args))
    assert mime == "text/plain"
    assert data == b"Hello, Alice!"


def test_hello_default():
    args = cbor2.dumps({})
    data, mime = asyncio.run(dispatch_tool("hello", args))
    assert data == b"Hello, world!"


def test_add_returns_cbor():
    args = cbor2.dumps({"a": 3, "b": 4})
    data, mime = asyncio.run(dispatch_tool("add", args))
    assert mime == "application/cbor"
    assert cbor2.loads(data) == 7


def test_unknown_tool():
    result = asyncio.run(dispatch_tool("nonexistent", b""))
    assert result[2] == "error"
    assert result[0] == "std:not-found"


def test_act_error():
    result = asyncio.run(dispatch_tool("fail", cbor2.dumps({})))
    assert result[2] == "error"
    assert result[0] == "std:not-found"


def test_json_response():
    args = cbor2.dumps({"data": {"key": "val"}})
    data, mime = asyncio.run(dispatch_tool("as-json", args))
    assert mime == "application/json"


def test_binary_response():
    data, mime = asyncio.run(dispatch_tool("binary", cbor2.dumps({})))
    assert mime == "image/png"
    assert data == b"\x89PNG"
