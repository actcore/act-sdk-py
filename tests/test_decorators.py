import json
from act_sdk.decorators import tool


class TestToolDecorator:
    def test_marks_function(self):
        @tool(description="Say hello")
        async def hello(self, name: str = "world") -> str:
            return f"Hello, {name}\!"

        assert hasattr(hello, "_act_tool")
        info = hello._act_tool
        assert info.name == "hello"
        assert info.description == "Say hello"

    def test_tool_name_uses_hyphens(self):
        @tool(description="Get user info")
        async def get_user_info(self, user_id: str) -> str:
            return ""

        assert get_user_info._act_tool.name == "get-user-info"

    def test_schema_generated(self):
        @tool(description="Query")
        async def query(self, sql: str, limit: int = 100) -> str:
            return ""

        schema = json.loads(query._act_tool.parameters_schema)
        assert schema["properties"]["sql"] == {"type": "string"}
        assert schema["properties"]["limit"] == {"type": "integer", "default": 100}
        assert schema["required"] == ["sql"]

    def test_metadata_flags(self):
        @tool(description="Read", read_only=True, idempotent=True)
        async def read(self) -> str:
            return ""

        info = read._act_tool
        assert info.read_only is True
        assert info.idempotent is True
        assert info.destructive is False

    def test_timeout_ms(self):
        @tool(description="Slow", timeout_ms=30000)
        async def slow(self) -> str:
            return ""

        assert slow._act_tool.timeout_ms == 30000
