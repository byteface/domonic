"""
    domonic.d3.queue
    ====================================

    Small Python port of d3-queue's callback-oriented API.
"""

from __future__ import annotations

from typing import Any, Callable

from domonic.javascript import Error

Task = Callable[..., Any]


class Queue:
    def __init__(self, size: int | float):
        if size < 1:
            raise Error("invalid concurrency")

        self._size = size
        self._error: Exception | None = None
        self._tasks: list[tuple[Task, tuple[Any, ...]]] = []
        self._results: list[Any] = []
        self._call: Callable[[Exception | None, list[Any]], Any] | None = None
        self._started = False

    def defer(self, callback: Task, *args: Any) -> Queue:
        if not callable(callback):
            raise Error("invalid callback")
        if self._call is not None:
            raise Error("defer after await")
        if self._error is not None:
            return self

        self._tasks.append((callback, args))
        return self

    def abort(self) -> Queue:
        if self._error is None:
            self._error = Error("abort")
        self._notify()
        return self

    def await_(self, callback: Callable[..., Any]) -> Queue:
        if not callable(callback):
            raise Error("invalid callback")
        if self._call is not None:
            raise Error("multiple await")

        def _call(error: Exception | None, results: list[Any]) -> Any:
            return callback(error, *results)

        self._call = _call
        self._run()
        return self

    def awaitAll(self, callback: Callable[[Exception | None, list[Any]], Any]) -> Queue:
        if not callable(callback):
            raise Error("invalid callback")
        if self._call is not None:
            raise Error("multiple await")

        self._call = callback
        self._run()
        return self

    def _run(self) -> None:
        if self._started:
            self._notify()
            return

        self._started = True
        self._results = [None] * len(self._tasks)

        for index, (task, args) in enumerate(self._tasks):
            if self._error is not None:
                break

            finished = False

            def done(error: Exception | None = None, result: Any = None, *, _index: int = index) -> None:
                nonlocal finished
                if finished:
                    return
                finished = True
                if error is not None and self._error is None:
                    self._error = error
                    return
                self._results[_index] = result

            try:
                result = task(*args, done)
            except Exception as error:
                done(error)
                continue

            if not finished:
                done(None, result)

        self._notify()

    def _notify(self) -> None:
        if self._call is not None and self._started:
            callback = self._call
            self._call = None
            callback(self._error, self._results)


def queue(concurrency: int | float | None = None) -> Queue:
    if concurrency is None:
        concurrency = float("inf")
    return Queue(concurrency)
