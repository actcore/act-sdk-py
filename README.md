# act-sdk

Python SDK for building [ACT (Agent Component Tools)](https://actcore.dev) components — sandboxed WASM tools for AI agents that work across MCP, HTTP, CLI, and browser hosts.

## Install

```bash
uv add act-sdk
# or
pip install act-sdk
```

## Quick start

```python
from act_sdk import component, tool, ActError

@component
class MyComponent:
    @tool(description="Say hello", read_only=True)
    async def hello(self, name: str = "world") -> str:
        return f"Hello, {name}!"

    @tool(description="Divide two numbers")
    async def divide(self, a: float, b: float) -> float:
        if b == 0:
            raise ActError("std:invalid-args", "Cannot divide by zero")
        return a / b
```

Package with `componentize-py` + `act-build pack` to produce a `.wasm` component that exposes these tools over every ACT transport.

## What you get

- `@component` — declares the class as an ACT component. Generates the `act:core/tool-provider` WIT export.
- `@tool` — declares a method as a tool. Parameters, return type, and docstrings become the JSON Schema automatically (via type hints).
- `ActError("std:kind", "message")` — raise this from a tool body to produce a structured `tool-error` the host forwards to the caller.
- `Json[T]` / `Content(data, mime_type=...)` — explicit return types for when you need control over the wire format; otherwise returns are CBOR-encoded.

## Tool naming

Tool method names are exposed as-is (snake_case). `async def get_weather(...)` becomes the tool name `get_weather` on the wire. See the [tool naming guidelines](https://github.com/actcore/act-context/blob/main/docs/references/tool-naming-guidelines.md) for the recommended style.

## Capabilities

Declare host capabilities inline in `pyproject.toml`:

```toml
[project]
name = "my-component"
version = "0.1.0"
description = "..."

[tool.act.std.capabilities."wasi:http"]
```

`act-build pack` picks up `[tool.act]` and embeds it in the component's `act:component` custom section. The component cannot reach the network unless the host links `wasi:http` at load time. Filesystem, sockets, and other WASI capabilities follow the same pattern.

A separate `act.toml` also works as a last-wins override layer if you need to keep capability metadata out of your build configuration — but for most components, inline `pyproject.toml` is the recommended source of truth.

## Links

- Main site: https://actcore.dev
- Component registry: https://actpkg.dev
- Protocol specification: https://github.com/actcore/act-spec
- Rust SDK: https://crates.io/crates/act-sdk

## License

MIT OR Apache-2.0
