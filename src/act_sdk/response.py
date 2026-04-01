"""Response types and encoding for ACT tool results."""

from __future__ import annotations

import json
from typing import Generic, TypeVar

import cbor2

T = TypeVar("T")


class Json(Generic[T]):
    """Wrap a value to be serialized as JSON instead of CBOR."""

    def __init__(self, value: T) -> None:
        self.value = value


class Content:
    """Wrap raw bytes with an explicit MIME type."""

    def __init__(self, mime: str, data: bytes) -> None:
        self.mime = mime
        self.data = data


def encode_response(value: object) -> tuple[bytes, str]:
    """Encode a tool return value into (data_bytes, mime_type).

    - str → text/plain
    - bytes → application/octet-stream
    - Json(x) → application/json
    - Content(mime, data) → explicit mime
    - anything else → application/cbor
    """
    if isinstance(value, str):
        return value.encode("utf-8"), "text/plain"
    if isinstance(value, bytes):
        return value, "application/octet-stream"
    if isinstance(value, Json):
        return json.dumps(value.value).encode("utf-8"), "application/json"
    if isinstance(value, Content):
        return value.data, value.mime
    return cbor2.dumps(value), "application/cbor"
