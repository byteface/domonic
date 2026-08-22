"""
Web Workers example
===================

Run browser-style worker messaging with a Python callable.
"""

import sys
from pathlib import Path
from threading import Event

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.webapi.webworkers import Worker


done = Event()


def worker_main(scope):
    def handle(event):
        scope.postMessage({"received": event.data, "worker": scope.name})

    scope.onmessage = handle


worker = Worker(worker_main, {"name": "demo-worker"})
worker.onmessage = lambda event: (print("main received:", event.data), done.set())
worker.postMessage("hello from main")

done.wait(2)
worker.terminate()
worker.join(2)
