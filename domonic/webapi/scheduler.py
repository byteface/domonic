"""
domonic.webapi.scheduler
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Prioritized_Task_Scheduling_API
"""

from __future__ import annotations

import itertools
import threading
from dataclasses import dataclass, field
from typing import Any, Callable

from domonic.events import AbortSignal, Event

_PRIORITIES = ("user-blocking", "user-visible", "background")
_PRIORITY_ORDER = {priority: index for index, priority in enumerate(_PRIORITIES)}


def _normalize_priority(priority: str | None) -> str:
    if priority is None:
        return "user-visible"
    normalized = str(priority)
    if normalized not in _PRIORITY_ORDER:
        raise TypeError("Task priority must be one of: " + ", ".join(_PRIORITIES))
    return normalized


def _create_promise():
    from domonic.javascript import Promise

    return Promise()


class TaskPriorityChangeEvent(Event):
    """Event fired when a ``TaskSignal`` priority changes."""

    def __init__(
        self,
        _type: str = "prioritychange",
        options: dict[str, Any] | None = None,
    ) -> None:
        options = options or {}
        self.previousPriority = options.get("previousPriority")
        super().__init__(_type, options)


class TaskSignal(AbortSignal):
    """Abort signal carrying a mutable task priority."""

    def __init__(self, priority: str = "user-visible") -> None:
        super().__init__()
        self.priority = _normalize_priority(priority)
        self.onprioritychange = None

    def _set_priority(self, priority: str) -> None:
        priority = _normalize_priority(priority)
        previous = self.priority
        if previous == priority:
            return None
        self.priority = priority
        self.dispatchEvent(
            TaskPriorityChangeEvent("prioritychange", {"previousPriority": previous})
        )
        return None


class TaskController:
    """Controller for aborting tasks and changing ``TaskSignal`` priority."""

    def __init__(self, options: dict[str, Any] | None = None) -> None:
        options = options or {}
        self.signal = TaskSignal(options.get("priority", "user-visible"))

    def abort(self, reason: Any = None) -> None:
        self.signal._signal_abort(reason)

    def setPriority(self, priority: str) -> None:
        self.signal._set_priority(priority)


@dataclass
class _ScheduledTask:
    callback: Callable[[], Any]
    promise: Any
    priority: str
    signal: AbortSignal | None = None
    sequence: int = 0
    mutable_priority: bool = False
    timer: threading.Timer | None = field(default=None, compare=False)
    settled: bool = False

    @property
    def current_priority(self) -> str:
        if self.mutable_priority and self.signal is not None:
            return _normalize_priority(getattr(self.signal, "priority", self.priority))
        return self.priority


class Scheduler:
    """Scheduler for running prioritized tasks.

    ``auto_run=True`` resolves immediate tasks before ``postTask()`` returns,
    matching domonic's synchronous ``Promise`` implementation. Use
    ``auto_run=False`` and call ``run()`` when you want to enqueue several
    tasks and drain them in priority order.
    """

    def __init__(self, *, auto_run: bool = True) -> None:
        self.auto_run = auto_run
        self._queue: list[_ScheduledTask] = []
        self._timers: list[_ScheduledTask] = []
        self._counter = itertools.count()
        self._lock = threading.RLock()

    def postTask(
        self, callback: Callable[[], Any], options: dict[str, Any] | None = None
    ) -> Any:
        """Post a task and return a ``Promise`` for its result."""
        if not callable(callback):
            raise TypeError("Scheduler.postTask() callback must be callable")
        options = options or {}
        signal = options.get("signal")
        delay = max(0, int(options.get("delay", 0) or 0))

        mutable_priority = "priority" not in options and isinstance(signal, TaskSignal)
        priority = _normalize_priority(
            getattr(signal, "priority", None)
            if mutable_priority
            else options.get("priority")
        )

        promise = _create_promise()
        task = _ScheduledTask(
            callback=callback,
            promise=promise,
            priority=priority,
            signal=signal,
            sequence=next(self._counter),
            mutable_priority=mutable_priority,
        )

        if getattr(signal, "aborted", False):
            return self._reject_aborted(task)

        if signal is not None and hasattr(signal, "addEventListener"):
            signal.addEventListener(
                "abort", lambda event: self._reject_aborted(task), {"once": True}
            )

        if delay > 0:
            task.timer = threading.Timer(delay / 1000, self._run_task, args=(task,))
            task.timer.daemon = True
            with self._lock:
                self._timers.append(task)
            task.timer.start()
            return promise

        with self._lock:
            self._queue.append(task)

        if self.auto_run:
            self.run()
        return promise

    def yield_(self) -> Any:
        """Return a resolved ``Promise`` for yielding back to the scheduler."""
        return _create_promise().resolve(None)

    def run(self) -> list[Any]:
        """Drain currently queued tasks in priority and insertion order."""
        results = []
        while True:
            with self._lock:
                if not self._queue:
                    return results
                self._queue.sort(
                    key=lambda task: (
                        _PRIORITY_ORDER[task.current_priority],
                        task.sequence,
                    )
                )
                task = self._queue.pop(0)
            results.append(self._run_task(task))

    def clear(self) -> None:
        """Cancel pending timers and reject queued tasks."""
        with self._lock:
            tasks = list(self._queue) + list(self._timers)
            self._queue = []
            self._timers = []
        for task in tasks:
            if task.timer is not None:
                task.timer.cancel()
            if not task.settled:
                task.promise.reject("AbortError")
                task.settled = True

    def _reject_aborted(self, task: _ScheduledTask) -> Any:
        if task.settled:
            return task.promise
        task.settled = True
        if task.timer is not None:
            task.timer.cancel()
        with self._lock:
            if task in self._queue:
                self._queue.remove(task)
            if task in self._timers:
                self._timers.remove(task)
        reason = getattr(task.signal, "reason", None)
        task.promise.reject(reason if reason is not None else "AbortError")
        return task.promise

    def _run_task(self, task: _ScheduledTask) -> Any:
        with self._lock:
            if task in self._timers:
                self._timers.remove(task)
        if task.settled:
            return task.promise.data
        if getattr(task.signal, "aborted", False):
            self._reject_aborted(task)
            return task.promise.data
        try:
            result = task.callback()
        except Exception as error:
            task.promise.reject(error)
            task.settled = True
            return error
        task.promise.resolve(result)
        task.settled = True
        return result


setattr(Scheduler, "yield", Scheduler.yield_)

scheduler = Scheduler()


__all__ = [
    "Scheduler",
    "TaskController",
    "TaskPriorityChangeEvent",
    "TaskSignal",
    "scheduler",
]
