# act-sdk-py

Python SDK for ACT components.

## Install

```bash
uv add act-sdk
```

## Usage

```python
from act_sdk import component, tool, ActError

@component
class MyComponent:
    @tool(description="Say hello", read_only=True)
    async def hello(self, name: str = "world") -> str:
        return f"Hello, {name}!"
```

## Dev

```bash
uv run pytest
```

## Architecture

- `errors.py` — ActError exception
- `response.py` — Json, Content, encode_response()
- `schema.py` — type hints → JSON Schema
- `decorators.py` — @tool decorator, ToolInfo
- `provider.py` — @component decorator, ToolProvider WIT bridge
