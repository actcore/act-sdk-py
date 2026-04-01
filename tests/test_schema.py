from typing import Optional

from act_sdk.schema import params_schema


async def fn_str(self, name: str) -> str: ...
async def fn_int(self, count: int) -> str: ...
async def fn_float(self, value: float) -> str: ...
async def fn_bool(self, flag: bool) -> str: ...
async def fn_list(self, items: list[int]) -> str: ...
async def fn_dict(self, data: dict[str, int]) -> str: ...
async def fn_optional(self, name: Optional[str]) -> str: ...
async def fn_default(self, name: str = "world") -> str: ...
async def fn_multi(self, sql: str, limit: int = 100) -> str: ...
async def fn_no_params(self) -> str: ...


def test_str_param():
    schema = params_schema(fn_str)
    assert schema["properties"]["name"] == {"type": "string"}
    assert "name" in schema["required"]


def test_int_param():
    schema = params_schema(fn_int)
    assert schema["properties"]["count"] == {"type": "integer"}


def test_float_param():
    schema = params_schema(fn_float)
    assert schema["properties"]["value"] == {"type": "number"}


def test_bool_param():
    schema = params_schema(fn_bool)
    assert schema["properties"]["flag"] == {"type": "boolean"}


def test_list_param():
    schema = params_schema(fn_list)
    assert schema["properties"]["items"] == {
        "type": "array",
        "items": {"type": "integer"},
    }


def test_dict_param():
    schema = params_schema(fn_dict)
    assert schema["properties"]["data"] == {
        "type": "object",
        "additionalProperties": {"type": "integer"},
    }


def test_optional_not_required():
    schema = params_schema(fn_optional)
    assert "name" in schema["properties"]
    assert "name" not in schema.get("required", [])


def test_default_value():
    schema = params_schema(fn_default)
    assert schema["properties"]["name"] == {"type": "string", "default": "world"}
    assert "name" not in schema.get("required", [])


def test_multi_params():
    schema = params_schema(fn_multi)
    assert schema["properties"]["sql"] == {"type": "string"}
    assert schema["properties"]["limit"] == {"type": "integer", "default": 100}
    assert schema["required"] == ["sql"]


def test_no_params():
    schema = params_schema(fn_no_params)
    assert schema == {"type": "object", "properties": {}}
