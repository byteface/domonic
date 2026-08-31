"""
domonic.webapi.crypto
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Web_Crypto_API
"""

from __future__ import annotations

import array
import hashlib
import re
import secrets
import uuid
from dataclasses import dataclass, field
from typing import Any

from domonic.dom import DOMException
from domonic.javascript import (
    ArrayBuffer,
    DataView,
    Float32Array,
    Float64Array,
    Int8Array,
    Int16Array,
    Int32Array,
    Promise,
    TypedArray,
    Uint8Array,
    Uint8ClampedArray,
    Uint16Array,
    Uint32Array,
)

_MAX_RANDOM_BYTES = 65536
_INTEGER_TYPED_ARRAYS = (
    Int8Array,
    Uint8Array,
    Uint8ClampedArray,
    Int16Array,
    Uint16Array,
    Int32Array,
    Uint32Array,
)
_FLOAT_TYPED_ARRAYS = (Float32Array, Float64Array)
_DIGEST_ALGORITHMS = {
    "SHA-1": "sha1",
    "SHA-256": "sha256",
    "SHA-384": "sha384",
    "SHA-512": "sha512",
}


def _normalize_algorithm(algorithm: str | dict[str, Any]) -> str:
    if isinstance(algorithm, dict):
        algorithm = algorithm.get("name", "")
    name = str(algorithm or "").strip().upper().replace("_", "-")
    name = re.sub(r"^SHA(\d+)$", r"SHA-\1", name)
    if name not in _DIGEST_ALGORITHMS:
        raise DOMException(
            DOMException.NOT_SUPPORTED_ERR,
            f"Unsupported digest algorithm: {algorithm}",
        )
    return name


def _array_buffer_bytes(buffer: ArrayBuffer) -> bytes:
    return bytes(buffer.buffer)


def _view_bytes(view: Any) -> bytes:
    start = int(getattr(view, "byteOffset", 0))
    end = start + int(getattr(view, "byteLength", 0))
    return bytes(view.buffer.buffer[start:end])


def _bytes_from_buffer_source(data: Any) -> bytes:
    if data is None:
        raise TypeError("digest data is required")
    if isinstance(data, DataView):
        start = int(data.byteOffset)
        end = start + int(data.byteLength)
        return bytes(data.buffer.buffer[start:end])
    if isinstance(data, TypedArray):
        return _view_bytes(data)
    if isinstance(data, ArrayBuffer):
        return _array_buffer_bytes(data)
    if isinstance(data, memoryview):
        return data.tobytes()
    if isinstance(data, bytes):
        return data
    if isinstance(data, bytearray):
        return bytes(data)
    if isinstance(data, str):
        return data.encode("utf-8")
    if isinstance(data, (list, tuple)):
        return bytes(data)
    if hasattr(data, "read"):
        return _bytes_from_buffer_source(data.read())
    try:
        return bytes(data)
    except TypeError as exc:
        raise TypeError(
            "digest data must be an ArrayBuffer, typed array, DataView, or bytes"
        ) from exc


def _random_target_byte_length(target: Any) -> int:
    if isinstance(target, DataView):
        raise TypeError("getRandomValues() requires an integer TypedArray")
    if isinstance(target, _FLOAT_TYPED_ARRAYS):
        raise TypeError("getRandomValues() does not support floating point arrays")
    if isinstance(target, _INTEGER_TYPED_ARRAYS):
        return int(target.byteLength)
    if isinstance(target, bytearray):
        return len(target)
    if isinstance(target, memoryview):
        if target.readonly:
            raise TypeError("getRandomValues() target must be writable")
        return target.nbytes
    raise TypeError("getRandomValues() requires an integer TypedArray")


def _fill_random_target(target: Any, random_bytes: bytes) -> None:
    if isinstance(target, _INTEGER_TYPED_ARRAYS):
        start = int(target.byteOffset)
        end = start + int(target.byteLength)
        target.buffer.buffer[start:end] = array.array("B", random_bytes)
        return
    if isinstance(target, bytearray):
        target[:] = random_bytes
        return
    if isinstance(target, memoryview):
        target.cast("B")[:] = random_bytes


@dataclass(frozen=True)
class CryptoKey:
    """Minimal read-only Web Crypto key descriptor."""

    type: str
    extractable: bool
    algorithm: dict[str, Any] = field(default_factory=dict)
    usages: tuple[str, ...] = field(default_factory=tuple)

    def __init__(
        self,
        type: str = "secret",
        extractable: bool = False,
        algorithm: dict[str, Any] | str | None = None,
        usages: list[str] | tuple[str, ...] | None = None,
    ) -> None:
        if type not in {"secret", "private", "public"}:
            raise ValueError("CryptoKey.type must be 'secret', 'private', or 'public'")
        if isinstance(algorithm, str):
            algorithm = {"name": algorithm}
        object.__setattr__(self, "type", type)
        object.__setattr__(self, "extractable", bool(extractable))
        object.__setattr__(self, "algorithm", dict(algorithm or {}))
        object.__setattr__(self, "usages", tuple(usages or ()))


class SubtleCrypto:
    """Small SubtleCrypto surface focused on digest support."""

    @staticmethod
    def digest(algorithm: str | dict[str, Any], data: Any) -> Promise:
        """Return a Promise fulfilled with the digest bytes.

        Browser ``SubtleCrypto.digest()`` resolves with an ``ArrayBuffer``. In
        domonic the fulfilled value is Python ``bytes``, which is the most useful
        direct equivalent and can be passed into ``Uint8Array`` or ``Blob``.
        """
        promise = Promise()
        try:
            algorithm_name = _normalize_algorithm(algorithm)
            payload = _bytes_from_buffer_source(data)
            digest = hashlib.new(_DIGEST_ALGORITHMS[algorithm_name], payload).digest()
        except Exception as exc:
            return promise.reject(exc)
        return promise.resolve(digest)

    @staticmethod
    def digestSync(algorithm: str | dict[str, Any], data: Any) -> bytes:
        """Synchronous convenience wrapper around ``digest()``."""
        result = SubtleCrypto.digest(algorithm, data)
        if result.state == "rejected":
            raise result.data
        return result.data


class Crypto:
    """Basic Web Crypto entry point."""

    def __init__(self) -> None:
        self.subtle = SubtleCrypto()

    @staticmethod
    def getRandomValues(typedArray: Any) -> Any:
        """Fill an integer typed array with cryptographically strong random bytes."""
        byte_length = _random_target_byte_length(typedArray)
        if byte_length > _MAX_RANDOM_BYTES:
            raise DOMException(
                DOMException.QUOTA_EXCEEDED_ERR,
                "getRandomValues() cannot generate more than 65,536 bytes",
            )
        _fill_random_target(typedArray, secrets.token_bytes(byte_length))
        return typedArray

    @staticmethod
    def randomUUID() -> str:
        """Return a random RFC 4122 version 4 UUID string."""
        return str(uuid.uuid4())


crypto = Crypto()


__all__ = ["Crypto", "CryptoKey", "SubtleCrypto", "crypto"]
