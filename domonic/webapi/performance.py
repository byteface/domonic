"""
domonic.webapi.performance
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Performance

High resolution time. ``performance.now()`` is a ``DOMHighResTimeStamp``:
milliseconds since the time origin, read from a monotonic clock, with
sub-millisecond precision. Every other high resolution stamp domonic hands out
(``requestAnimationFrame`` callbacks, ``Event.timeStamp``,
``document.timeline.currentTime``, ``Gamepad.timestamp``,
``IntersectionObserverEntry.time``) is taken from the same origin, so they all
compare with each other and with ``performance.now()``.
"""

from __future__ import annotations

import time
from typing import Any, Callable, ClassVar

# The time origin: the wall-clock moment this clock started, in milliseconds
# since the Unix epoch (``performance.timeOrigin``), paired with the monotonic
# reading taken at that same moment. ``now()`` is monotonic time elapsed since
# then, so it never runs backwards when the system clock is adjusted.
_ORIGIN_WALL_MS: float = time.time() * 1000.0
_ORIGIN_MONOTONIC: float = time.perf_counter()


def now() -> float:
    """Milliseconds since the time origin -- a ``DOMHighResTimeStamp``."""
    return (time.perf_counter() - _ORIGIN_MONOTONIC) * 1000.0


class PerformanceEntry:
    """https://developer.mozilla.org/en-US/docs/Web/API/PerformanceEntry"""

    def __init__(self, name: str, entryType: str, startTime: float, duration: float) -> None:
        self.name = str(name)
        self.entryType = str(entryType)
        self.startTime = float(startTime)
        self.duration = float(duration)

    def toJSON(self) -> dict[str, Any]:
        return {
            "name": self.name,
            "entryType": self.entryType,
            "startTime": self.startTime,
            "duration": self.duration,
        }

    def __repr__(self) -> str:
        return f"{type(self).__name__}({self.name!r}, startTime={self.startTime:.3f}, duration={self.duration:.3f})"


class PerformanceMark(PerformanceEntry):
    """https://developer.mozilla.org/en-US/docs/Web/API/PerformanceMark"""

    def __init__(self, name: str, startTime: float, detail: Any = None) -> None:
        super().__init__(name, "mark", startTime, 0.0)
        self.detail = detail

    def toJSON(self) -> dict[str, Any]:
        data = super().toJSON()
        data["detail"] = self.detail
        return data


class PerformanceMeasure(PerformanceEntry):
    """https://developer.mozilla.org/en-US/docs/Web/API/PerformanceMeasure"""

    def __init__(self, name: str, startTime: float, duration: float, detail: Any = None) -> None:
        super().__init__(name, "measure", startTime, duration)
        self.detail = detail

    def toJSON(self) -> dict[str, Any]:
        data = super().toJSON()
        data["detail"] = self.detail
        return data


class PerformanceObserverEntryList(list):
    """The list handed to a ``PerformanceObserver`` callback
    (https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserverEntryList).
    A plain ``list`` of entries with the three lookup methods on top."""

    def getEntries(self) -> list[PerformanceEntry]:
        return list(self)

    def getEntriesByType(self, entryType: str) -> list[PerformanceEntry]:
        return [entry for entry in self if entry.entryType == entryType]

    def getEntriesByName(self, name: str, entryType: str | None = None) -> list[PerformanceEntry]:
        return [entry for entry in self if entry.name == name and (entryType is None or entry.entryType == entryType)]


PerformanceObserverCallback = Callable[[PerformanceObserverEntryList, "PerformanceObserver"], Any]


class PerformanceObserver:
    """https://developer.mozilla.org/en-US/docs/Web/API/PerformanceObserver

    Delivery is synchronous: an observed entry reaches the callback as soon as
    ``performance.mark`` / ``performance.measure`` records it.
    """

    supportedEntryTypes: ClassVar[list[str]] = ["mark", "measure"]
    _all_observers: ClassVar[list["PerformanceObserver"]] = []

    def __init__(self, callback: PerformanceObserverCallback) -> None:
        if not callable(callback):
            raise TypeError("PerformanceObserver callback must be callable")
        self.callback = callback
        self._entry_types: set[str] = set()
        self._records: PerformanceObserverEntryList = PerformanceObserverEntryList()
        PerformanceObserver._all_observers.append(self)

    def observe(self, options: dict[str, Any] | None = None) -> None:
        """``observe({"entryTypes": [...]})`` or ``observe({"type": "mark", "buffered": True})``."""
        options = options or {}
        entry_types = options.get("entryTypes")
        single = options.get("type")
        if entry_types and single is not None:
            raise TypeError("PerformanceObserver.observe takes either entryTypes or type, not both")
        if single is not None:
            entry_types = [single]
        if not entry_types:
            raise TypeError("PerformanceObserver.observe requires entryTypes")
        self._entry_types = {str(entry_type) for entry_type in entry_types}
        if options.get("buffered"):
            for entry in performance.getEntries():
                self._enqueue(entry)
        self._flush()

    def disconnect(self) -> None:
        self._entry_types.clear()
        self._records = PerformanceObserverEntryList()

    def takeRecords(self) -> PerformanceObserverEntryList:
        records = self._records
        self._records = PerformanceObserverEntryList()
        return records

    def _enqueue(self, entry: PerformanceEntry) -> None:
        if entry.entryType in self._entry_types:
            self._records.append(entry)

    def _flush(self) -> None:
        if not self._records:
            return
        self.callback(self.takeRecords(), self)

    @classmethod
    def _notify_entry(cls, entry: PerformanceEntry) -> None:
        for observer in list(cls._all_observers):
            observer._enqueue(entry)
            observer._flush()


class Performance:
    """https://developer.mozilla.org/en-US/docs/Web/API/Performance"""

    def __init__(self) -> None:
        self._entries: list[PerformanceEntry] = []
        self._marks: dict[str, float] = {}

    @property
    def timeOrigin(self) -> float:
        """Milliseconds since the Unix epoch at which ``now()`` read zero."""
        return _ORIGIN_WALL_MS

    def now(self) -> float:
        """Milliseconds since ``timeOrigin``, from a monotonic clock."""
        return now()

    def _timestamp(self, value: Any, *, what: str) -> float:
        """Resolve a mark name or a number into a timestamp
        (https://w3c.github.io/user-timing/#dfn-convert-a-mark-to-a-timestamp)."""
        if isinstance(value, str):
            if value not in self._marks:
                from domonic.dom import DOMException

                raise DOMException(f"The mark '{value}' does not exist.", "SyntaxError")
            return self._marks[value]
        stamp = float(value)
        if stamp < 0:
            raise TypeError(f"{what} must not be negative")
        return stamp

    def mark(self, name: str, markOptions: dict[str, Any] | None = None) -> PerformanceMark:
        options = markOptions or {}
        start = self._timestamp(options.get("startTime", self.now()), what="startTime")
        entry = PerformanceMark(name, start, options.get("detail"))
        self._marks[entry.name] = start
        self._entries.append(entry)
        PerformanceObserver._notify_entry(entry)
        return entry

    def measure(
        self,
        name: str,
        startOrMeasureOptions: str | float | dict[str, Any] | None = None,
        endMark: str | float | None = None,
    ) -> PerformanceMeasure:
        """``measure(name)``, ``measure(name, startMark, endMark)`` or
        ``measure(name, {"start": ..., "end": ..., "duration": ..., "detail": ...})``."""
        detail = None
        if isinstance(startOrMeasureOptions, dict):
            options = startOrMeasureOptions
            if endMark is not None:
                raise TypeError("measure() takes no endMark when given a measureOptions dict")
            detail = options.get("detail")
            start_opt, end_opt, duration_opt = options.get("start"), options.get("end"), options.get("duration")
            if start_opt is not None and end_opt is not None and duration_opt is not None:
                raise TypeError("measureOptions may give at most two of start, end and duration")
            if end_opt is not None:
                end = self._timestamp(end_opt, what="end")
                if start_opt is not None:
                    start = self._timestamp(start_opt, what="start")
                elif duration_opt is not None:
                    start = end - float(duration_opt)
                else:
                    start = 0.0
            else:
                start = self._timestamp(start_opt, what="start") if start_opt is not None else 0.0
                end = start + float(duration_opt) if duration_opt is not None else self.now()
        else:
            start = 0.0 if startOrMeasureOptions is None else self._timestamp(startOrMeasureOptions, what="startMark")
            end = self.now() if endMark is None else self._timestamp(endMark, what="endMark")
        entry = PerformanceMeasure(name, start, end - start, detail)
        self._entries.append(entry)
        PerformanceObserver._notify_entry(entry)
        return entry

    def getEntries(self) -> list[PerformanceEntry]:
        return list(self._entries)

    def getEntriesByType(self, entryType: str) -> list[PerformanceEntry]:
        return [entry for entry in self._entries if entry.entryType == entryType]

    def getEntriesByName(self, name: str, entryType: str | None = None) -> list[PerformanceEntry]:
        return [
            entry
            for entry in self._entries
            if entry.name == name and (entryType is None or entry.entryType == entryType)
        ]

    def _clear(self, entryType: str, name: str | None) -> None:
        self._entries = [
            entry
            for entry in self._entries
            if not (entry.entryType == entryType and (name is None or entry.name == name))
        ]

    def clearMarks(self, name: str | None = None) -> None:
        if name is None:
            self._marks.clear()
        else:
            self._marks.pop(name, None)
        self._clear("mark", name)

    def clearMeasures(self, name: str | None = None) -> None:
        self._clear("measure", name)

    def toJSON(self) -> dict[str, Any]:
        return {"timeOrigin": self.timeOrigin}

    def __repr__(self) -> str:
        return f"Performance(now={self.now():.3f}ms)"


performance = Performance()
