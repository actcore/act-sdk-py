import json
import cbor2
from act_sdk.response import Json, Content, encode_response


def test_str_returns_text_plain():
    data, mime = encode_response("hello")
    assert mime == "text/plain"
    assert data == b"hello"


def test_bytes_returns_octet_stream():
    data, mime = encode_response(b"\x89PNG")
    assert mime == "application/octet-stream"
    assert data == b"\x89PNG"


def test_json_wrapper():
    val = Json({"rows": [1, 2, 3]})
    data, mime = encode_response(val)
    assert mime == "application/json"
    assert json.loads(data) == {"rows": [1, 2, 3]}


def test_content_wrapper():
    val = Content("image/png", b"\x89PNG")
    data, mime = encode_response(val)
    assert mime == "image/png"
    assert data == b"\x89PNG"


def test_dict_returns_cbor():
    val = {"key": "value", "num": 42}
    data, mime = encode_response(val)
    assert mime == "application/cbor"
    assert cbor2.loads(data) == val


def test_list_returns_cbor():
    val = [1, 2, 3]
    data, mime = encode_response(val)
    assert mime == "application/cbor"
    assert cbor2.loads(data) == val


def test_int_returns_cbor():
    data, mime = encode_response(42)
    assert mime == "application/cbor"
    assert cbor2.loads(data) == 42


def test_none_returns_cbor():
    data, mime = encode_response(None)
    assert mime == "application/cbor"
    assert cbor2.loads(data) is None
