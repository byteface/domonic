"""
Web Crypto example
==================

Use browser-style secure randomness, IDs, and hashes from Python.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.javascript import Uint8Array
from domonic.webapi.crypto import crypto

token = Uint8Array(16)
crypto.getRandomValues(token)
print("Token bytes:", bytes(token.buffer.buffer).hex())
print("UUID:", crypto.randomUUID())

digest = crypto.subtle.digest("SHA-256", b"domonic").data
print("SHA-256:", digest.hex())
