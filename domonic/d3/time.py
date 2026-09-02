"""
domonic.d3.time
====================================

A port of `d3-time <https://github.com/d3/d3-time>`_ (v3): calendar intervals
(``timeSecond`` .. ``timeYear`` and their ``utc`` counterparts) plus
``timeTicks`` / ``timeTickInterval``.

Dates are :class:`datetime.datetime`. The ``time*`` intervals use whatever
timezone the datetime carries (naive datetimes are treated as wall-clock and
DST transitions are not modelled); the ``utc*`` intervals do the same
arithmetic and are provided for API parity.
"""

from __future__ import annotations

import math
from datetime import datetime, timedelta
from typing import Any, Callable

__all__ = [
    "timeInterval", "timeMillisecond", "timeSecond", "timeMinute", "timeHour",
    "timeDay", "timeWeek", "timeSunday", "timeMonday", "timeTuesday",
    "timeWednesday", "timeThursday", "timeFriday", "timeSaturday", "timeMonth",
    "timeYear", "timeMilliseconds", "timeSeconds", "timeMinutes", "timeHours",
    "timeDays", "timeWeeks", "timeSundays", "timeMondays", "timeTuesdays",
    "timeWednesdays", "timeThursdays", "timeFridays", "timeSaturdays",
    "timeMonths", "timeYears", "timeTicks", "timeTickInterval",
    "utcMillisecond", "utcSecond", "utcMinute", "utcHour", "utcDay", "utcWeek",
    "utcSunday", "utcMonday", "utcTuesday", "utcWednesday", "utcThursday",
    "utcFriday", "utcSaturday", "utcMonth", "utcYear", "utcTicks",
    "utcTickInterval",
]

_DURATION_SECOND = 1000
_DURATION_MINUTE = _DURATION_SECOND * 60
_DURATION_HOUR = _DURATION_MINUTE * 60
_DURATION_DAY = _DURATION_HOUR * 24
_DURATION_WEEK = _DURATION_DAY * 7
_DURATION_MONTH = _DURATION_DAY * 30
_DURATION_YEAR = _DURATION_DAY * 365


class TimeInterval:
    """A calendar interval: ``floor`` / ``ceil`` / ``round`` / ``offset`` /
    ``range`` / ``filter`` / ``every`` / ``count``."""

    def __init__(
        self,
        floori: Callable[[datetime], datetime],
        offseti: Callable[[datetime, int], datetime],
        count: Callable[[datetime, datetime], float] | None = None,
        field: Callable[[datetime], int] | None = None,
    ) -> None:
        self._floori = floori
        self._offseti = offseti
        self._count = count
        self._field = field

    def __call__(self, date: datetime | None = None) -> datetime:
        return self._floori(date if date is not None else datetime.now())

    def floor(self, date: datetime) -> datetime:
        return self._floori(date)

    def ceil(self, date: datetime) -> datetime:
        d = self._floori(date - timedelta(microseconds=1000))
        return self._floori(self._offseti(d, 1))

    def round(self, date: datetime) -> datetime:
        d0 = self.floor(date)
        d1 = self.ceil(date)
        return d0 if (date - d0) < (d1 - date) else d1

    def offset(self, date: datetime, step: int = 1) -> datetime:
        return self._offseti(date, int(math.floor(step)))

    def range(
        self, start: datetime, stop: datetime, step: int = 1
    ) -> list[datetime]:
        out: list[datetime] = []
        current = self.ceil(start)
        step = int(math.floor(step))
        if not (current < stop) or not (step > 0):
            return out
        previous = current
        while True:
            out.append(current)
            previous = current
            current = self._floori(self._offseti(current, step))
            if not (previous < current and current < stop):
                break
        return out

    def filter(self, test: Callable[[datetime], bool]) -> "TimeInterval":
        def floori(date: datetime) -> datetime:
            date = self._floori(date)
            while not test(date):
                date = self._floori(date - timedelta(microseconds=1000))
            return date

        def offseti(date: datetime, step: int) -> datetime:
            if step < 0:
                while step < 0:
                    date = self._offseti(date, -1)
                    while not test(date):
                        date = self._offseti(date, -1)
                    step += 1
            else:
                while step > 0:
                    date = self._offseti(date, 1)
                    while not test(date):
                        date = self._offseti(date, 1)
                    step -= 1
            return date

        return TimeInterval(floori, offseti)

    def every(self, step: int) -> "TimeInterval | None":
        step = int(math.floor(step))
        if not math.isfinite(step) or not (step > 0):
            return None
        if not (step > 1):
            return self
        if self._field is not None:
            field = self._field
            return self.filter(lambda d: field(d) % step == 0)
        return self.filter(lambda d: self.count(_EPOCH, d) % step == 0)

    def count(self, start: datetime, end: datetime) -> int:
        if self._count is None:
            raise TypeError("this interval does not support count()")
        return int(math.floor(self._count(self._floori(start), self._floori(end))))


_EPOCH = datetime(1970, 1, 1)


def timeInterval(floori, offseti, count=None, field=None) -> TimeInterval:
    return TimeInterval(floori, offseti, count, field)


# -- fixed-duration intervals --------------------------------------

def _fixed_interval(unit_ms: int, floor_key) -> TimeInterval:
    delta = timedelta(milliseconds=unit_ms)

    def floori(date: datetime) -> datetime:
        return floor_key(date)

    def offseti(date: datetime, step: int) -> datetime:
        return date + delta * step

    def count(start: datetime, end: datetime) -> float:
        return (end - start).total_seconds() * 1000 / unit_ms

    return TimeInterval(floori, offseti, count)


timeMillisecond = TimeInterval(
    lambda d: d,
    lambda d, s: d + timedelta(milliseconds=s),
    lambda a, b: (b - a).total_seconds() * 1000,
)

timeSecond = _fixed_interval(
    _DURATION_SECOND, lambda d: d.replace(microsecond=0)
)
timeMinute = _fixed_interval(
    _DURATION_MINUTE, lambda d: d.replace(second=0, microsecond=0)
)
timeHour = _fixed_interval(
    _DURATION_HOUR, lambda d: d.replace(minute=0, second=0, microsecond=0)
)

utcSecond = timeSecond
utcMinute = timeMinute
utcHour = timeHour
utcMillisecond = timeMillisecond


# -- calendar intervals -------------------------------------------

def _midnight(d: datetime) -> datetime:
    return d.replace(hour=0, minute=0, second=0, microsecond=0)


timeDay = TimeInterval(
    _midnight,
    lambda d, s: _add_days(d, s),
    lambda a, b: (b - a).total_seconds() / 86400,
    lambda d: d.timetuple().tm_yday - 1,
)
utcDay = timeDay


def _add_days(d: datetime, step: int) -> datetime:
    return d + timedelta(days=step)


def _weekday_interval(iso_weekday: int) -> TimeInterval:
    """iso_weekday: Monday=0 .. Sunday=6 for the start-of-week day."""

    def floori(d: datetime) -> datetime:
        d0 = _midnight(d)
        delta = (d0.weekday() - iso_weekday) % 7
        return d0 - timedelta(days=delta)

    def offseti(d: datetime, step: int) -> datetime:
        return d + timedelta(weeks=step)

    def count(a: datetime, b: datetime) -> float:
        return (b - a).total_seconds() / _DURATION_WEEK * 1000

    return TimeInterval(floori, offseti, count)


timeSunday = _weekday_interval(6)
timeMonday = _weekday_interval(0)
timeTuesday = _weekday_interval(1)
timeWednesday = _weekday_interval(2)
timeThursday = _weekday_interval(3)
timeFriday = _weekday_interval(4)
timeSaturday = _weekday_interval(5)
timeWeek = timeSunday

utcSunday = timeSunday
utcMonday = timeMonday
utcTuesday = timeTuesday
utcWednesday = timeWednesday
utcThursday = timeThursday
utcFriday = timeFriday
utcSaturday = timeSaturday
utcWeek = utcSunday


def _month_floor(d: datetime) -> datetime:
    return d.replace(day=1, hour=0, minute=0, second=0, microsecond=0)


def _month_offset(d: datetime, step: int) -> datetime:
    month_index = d.year * 12 + (d.month - 1) + step
    year, month = divmod(month_index, 12)
    return d.replace(year=year, month=month + 1)


def _month_count(a: datetime, b: datetime) -> float:
    return (b.year - a.year) * 12 + (b.month - a.month)


timeMonth = TimeInterval(
    _month_floor, _month_offset, _month_count, lambda d: d.month - 1
)
utcMonth = timeMonth


def _year_floor(d: datetime) -> datetime:
    return d.replace(month=1, day=1, hour=0, minute=0, second=0, microsecond=0)


def _year_offset(d: datetime, step: int) -> datetime:
    return d.replace(year=d.year + step)


timeYear = TimeInterval(
    _year_floor,
    _year_offset,
    lambda a, b: b.year - a.year,
    lambda d: d.year,
)
utcYear = timeYear


# -- range helpers (bound .range) --------------------------------

timeMilliseconds = timeMillisecond.range
timeSeconds = timeSecond.range
timeMinutes = timeMinute.range
timeHours = timeHour.range
timeDays = timeDay.range
timeWeeks = timeWeek.range
timeSundays = timeSunday.range
timeMondays = timeMonday.range
timeTuesdays = timeTuesday.range
timeWednesdays = timeWednesday.range
timeThursdays = timeThursday.range
timeFridays = timeFriday.range
timeSaturdays = timeSaturday.range
timeMonths = timeMonth.range
timeYears = timeYear.range


# -- ticks --------------------------------------------------------

_TICK_INTERVALS = [
    (timeSecond, 1, _DURATION_SECOND),
    (timeSecond, 5, 5 * _DURATION_SECOND),
    (timeSecond, 15, 15 * _DURATION_SECOND),
    (timeSecond, 30, 30 * _DURATION_SECOND),
    (timeMinute, 1, _DURATION_MINUTE),
    (timeMinute, 5, 5 * _DURATION_MINUTE),
    (timeMinute, 15, 15 * _DURATION_MINUTE),
    (timeMinute, 30, 30 * _DURATION_MINUTE),
    (timeHour, 1, _DURATION_HOUR),
    (timeHour, 3, 3 * _DURATION_HOUR),
    (timeHour, 6, 6 * _DURATION_HOUR),
    (timeHour, 12, 12 * _DURATION_HOUR),
    (timeDay, 1, _DURATION_DAY),
    (timeDay, 2, 2 * _DURATION_DAY),
    (timeWeek, 1, _DURATION_WEEK),
    (timeMonth, 1, _DURATION_MONTH),
    (timeMonth, 3, 3 * _DURATION_MONTH),
    (timeYear, 1, _DURATION_YEAR),
]


def _tick_interval(start: datetime, stop: datetime, count: int) -> TimeInterval:
    from domonic.d3.array import tickStep

    target = abs((stop - start).total_seconds() * 1000) / count
    # find the tick interval whose step is closest to target
    i = 0
    while i < len(_TICK_INTERVALS) and _TICK_INTERVALS[i][2] < target:
        i += 1
    if i == len(_TICK_INTERVALS):
        step = max(1, round(tickStep(
            start.year, stop.year, count
        )))
        return timeYear.every(step) or timeYear
    if i == 0:
        step = max(1, round(target / _DURATION_SECOND))
        # sub-second -> milliseconds
        ms_step = max(1, round(target))
        return timeMillisecond.every(ms_step) or timeMillisecond
    # choose the nearer of intervals[i-1] and intervals[i]
    if target / _TICK_INTERVALS[i - 1][2] < _TICK_INTERVALS[i][2] / target:
        interval, span, _ = _TICK_INTERVALS[i - 1]
    else:
        interval, span, _ = _TICK_INTERVALS[i]
    return interval.every(span) or interval


def timeTickInterval(start: datetime, stop: datetime, count: int) -> TimeInterval:
    return _tick_interval(start, stop, count)


def timeTicks(start: datetime, stop: datetime, count: int = 10) -> list[datetime]:
    reverse = stop < start
    if reverse:
        start, stop = stop, start
    interval = _tick_interval(start, stop, count)
    out = interval.range(start, stop + timedelta(microseconds=1000), 1)
    return out[::-1] if reverse else out


utcTicks = timeTicks
utcTickInterval = timeTickInterval
