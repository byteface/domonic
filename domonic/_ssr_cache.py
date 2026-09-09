"""Optional private, atomic bytecode cache for SSR startup compilation."""

import hashlib
import marshal
import os
import stat
import sys
import tempfile
import types
from pathlib import Path

_VERSION = "domonic-ssr-1"


def compiled_code(source, filename, mode, cache_dir=None):
    """Return (code, cache_hit). Only accept a private, user-owned directory.

    The key covers the generated program and Python ABI. Runtime globals and
    request data are never serialized. Bad/truncated entries are cache misses.
    The cache contains executable bytecode and must not be shared with other users.
    """
    if cache_dir is None:
        return compile(source, filename, mode), False
    directory = Path(cache_dir)
    directory.mkdir(mode=0o700, parents=True, exist_ok=True)
    info = directory.lstat()
    if not stat.S_ISDIR(info.st_mode) or info.st_mode & 0o077 or (hasattr(os, "getuid") and info.st_uid != os.getuid()):
        raise ValueError("SSR cache_dir must be a private, user-owned directory (mode 0700)")
    key = hashlib.sha256(repr((_VERSION, sys.implementation.cache_tag, sys.version, mode, source)).encode()).hexdigest()
    path = directory / (key + ".bin")
    try:
        fd = os.open(path, os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0))
        with os.fdopen(fd, "rb") as stream:
            info = os.fstat(stream.fileno())
            if not stat.S_ISREG(info.st_mode) or info.st_mode & 0o077:
                raise ValueError("non-private cache entry")
            if hasattr(os, "getuid") and info.st_uid != os.getuid():
                raise ValueError("foreign cache entry")
            data = stream.read()
        checksum, payload = data[:32], data[32:]
        if hashlib.sha256(payload).digest() != checksum:
            raise ValueError("invalid cache checksum")
        # The payload is our own marshalled code object, read from a 0700
        # directory owned by the current uid (checked above and via O_NOFOLLOW +
        # fstat), and SHA-256 verified. This is the same trust model as CPython's
        # own .pyc loader.
        code = marshal.loads(payload)  # nosec B302
        if not isinstance(code, types.CodeType):
            raise ValueError("invalid cached code")
        return code, True
    except (OSError, ValueError, EOFError, TypeError):  # nosec B110 - any cache-read failure just recompiles below
        pass
    code = compile(source, filename, mode)
    payload = marshal.dumps(code)
    fd, temporary = tempfile.mkstemp(prefix=".writing-", dir=directory)
    try:
        with os.fdopen(fd, "wb") as stream:
            stream.write(hashlib.sha256(payload).digest() + payload)
        os.replace(temporary, path)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return code, False
