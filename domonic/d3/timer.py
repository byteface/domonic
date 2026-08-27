"""
domonic.d3.timer
====================================

"""

from __future__ import annotations

import threading
from typing import Any, Callable

from domonic.javascript import Error, performance

FRAME_DELAY = 17

_timers: list["Timer"] = []
_timers_lock = threading.RLock()


def now() -> float:
    """Return the current high-resolution timestamp in milliseconds."""
    return performance.now()


def _invoke(callback: Callable[..., Any], elapsed: float) -> Any:
    if hasattr(callback, "call"):
        return callback.call(None, elapsed)
    return callback(elapsed)


def _register(timer_: "Timer") -> None:
    with _timers_lock:
        if timer_ not in _timers:
            _timers.append(timer_)


def _unregister(timer_: "Timer") -> None:
    with _timers_lock:
        if timer_ in _timers:
            _timers.remove(timer_)


class Timer:
    """A small d3-timer compatible timer."""

    def __init__(self):
        self._call: Callable[..., Any] | None = None
        self._time: float = 0
        self._start: float = 0
        self._delay: float = 0
        self._repeat: float | None = FRAME_DELAY
        self._handle: threading.Timer | None = None
        self._active = False

    def restart(self, callback, delay=None, time=None):
        """Restart this timer with a callback and optional delay/start time."""
        self._restart(callback, delay, time, FRAME_DELAY)

    def _restart(self, callback, delay=None, time=None, repeat=FRAME_DELAY):
        if not callable(callback):
            raise Error("callback is not a function")
        self.stop()
        self._call = callback
        self._delay = 0 if delay is None else float(delay)
        self._start = now() if time is None else float(time)
        self._time = self._start + self._delay
        self._repeat = repeat
        self._active = True
        _register(self)
        self._schedule()

    def _schedule(self) -> None:
        if not self._active:
            return
        wait = max(0, (self._time - now()) / 1000)
        self._handle = threading.Timer(wait, self._fire)
        self._handle.daemon = True
        self._handle.start()

    def _fire(self) -> None:
        if not self._active or self._call is None:
            return
        elapsed = max(0, now() - self._time)
        _invoke(self._call, elapsed)
        if not self._active:
            return
        if self._repeat is None:
            self.stop()
            return
        self._time = now() + max(float(self._repeat), FRAME_DELAY)
        self._schedule()

    def _flush(self, timestamp: float) -> None:
        if not self._active or self._call is None or timestamp < self._time:
            return
        elapsed = max(0, timestamp - self._time)
        handle = self._handle
        if handle is not None:
            handle.cancel()
            self._handle = None
        _invoke(self._call, elapsed)
        if not self._active:
            return
        if self._repeat is None:
            self.stop()
            return
        self._time = timestamp + max(float(self._repeat), FRAME_DELAY)
        self._schedule()

    def stop(self):
        """Stop this timer."""
        self._active = False
        self._call = None
        if self._handle is not None:
            self._handle.cancel()
            self._handle = None
        _unregister(self)


def timer(callback, delay=None, time=None):
    """Schedule a callback every animation-frame-ish tick until stopped."""
    timer_ = Timer()
    timer_.restart(callback, delay, time)
    return timer_


def timerFlush():
    """Immediately invoke all timers whose scheduled time has elapsed."""
    timestamp = now()
    with _timers_lock:
        pending = list(_timers)
    for timer_ in pending:
        timer_._flush(timestamp)


def timeout(callback, delay=None, time=None):
    """Schedule a callback once."""
    timer_ = Timer()
    delay = 0 if delay is None else float(delay)

    def elapsed_callback(elapsed):
        timer_.stop()
        return _invoke(callback, elapsed + delay)

    timer_._restart(elapsed_callback, delay, time, None)
    return timer_


def interval(callback, delay=None, time=None):
    """Schedule a callback repeatedly."""
    if delay is None:
        return timer(callback, delay, time)
    timer_ = Timer()
    interval_delay = float(delay)
    start_time = now() if time is None else float(time)

    def tick(elapsed):
        return _invoke(callback, elapsed + interval_delay)

    timer_._restart(tick, interval_delay, start_time, interval_delay)
    return timer_
