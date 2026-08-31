"""
Messaging example
=================

Wire browser-style message ports and named broadcasts inside Python.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.webapi.messaging import BroadcastChannel, MessageChannel

channel = MessageChannel()
channel.port1.onmessage = lambda event: print("port1 received:", event.data)
channel.port2.postMessage({"kind": "direct", "ok": True})

first = BroadcastChannel("demo")
second = BroadcastChannel("demo")

second.onmessage = lambda event: print("broadcast received:", event.data)
first.postMessage("hello everyone else")

first.close()
second.close()
