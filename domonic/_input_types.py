"""
domonic._input_types
====================

String <-> number conversions and stepping for the ``<input>`` types that
have a numeric value: ``number``, ``range``, ``date``, ``month``, ``week``,
``time`` and ``datetime-local``
(https://html.spec.whatwg.org/multipage/input.html#common-input-element-apis).

Numbers are ``Decimal`` so stepping is exact (``0.1`` + ``0.2`` is ``0.3``).
The units are the spec's: milliseconds since 1970-01-01T00:00Z for
date / week / datetime-local, milliseconds since midnight for time, months
since 1970-01 for month.

Private to ``domonic.dom``.
"""

from __future__ import annotations

import re
from decimal import ROUND_CEILING, ROUND_FLOOR, Decimal, InvalidOperation

NUMBER_TYPES = frozenset({"number", "range"})
DATE_TYPES = frozenset({"date", "month", "week", "time"})  # valueAsDate applies
NUMERIC_TYPES = NUMBER_TYPES | DATE_TYPES | {"datetime-local"}  # valueAsNumber / stepUp apply

MS_PER_DAY = 86_400_000

_VALID_FLOAT = re.compile(r"-?(?:[0-9]+(?:\.[0-9]+)?|\.[0-9]+)(?:[eE][+-]?[0-9]+)?")
_YEAR = r"([0-9]{4,})"
_TIME = r"([0-9]{2}):([0-9]{2})(?::([0-9]{2})(?:\.([0-9]{1,3}))?)?"
_DATE_RE = re.compile(_YEAR + r"-([0-9]{2})-([0-9]{2})")
_MONTH_RE = re.compile(_YEAR + r"-([0-9]{2})")
_WEEK_RE = re.compile(_YEAR + r"-W([0-9]{2})")
_TIME_RE = re.compile(_TIME)
_LOCAL_RE = re.compile(_YEAR + r"-([0-9]{2})-([0-9]{2})[T ]" + _TIME)

# type -> (default step, step scale factor, default step base)
STEP_DEFAULTS: dict[str, tuple[int, int, int]] = {
    "number": (1, 1, 0),
    "range": (1, 1, 0),
    "date": (1, MS_PER_DAY, 0),
    "month": (1, 1, 0),
    "week": (1, 7 * MS_PER_DAY, -259_200_000),  # Monday 1969-12-29
    "time": (60, 1000, 0),
    "datetime-local": (60, 1000, 0),
}


# -- calendar arithmetic (proleptic Gregorian, any year >= 1) ----------------


def _is_leap(year: int) -> bool:
    return year % 4 == 0 and (year % 100 != 0 or year % 400 == 0)


def _days_in_month(year: int, month: int) -> int:
    if month == 2:
        return 29 if _is_leap(year) else 28
    return 30 if month in (4, 6, 9, 11) else 31


def days_from_civil(year: int, month: int, day: int) -> int:
    """Days since 1970-01-01 (Howard Hinnant's algorithm)."""
    year -= month <= 2
    era = year // 400
    yoe = year - era * 400
    doy = (153 * (month + (-3 if month > 2 else 9)) + 2) // 5 + day - 1
    doe = yoe * 365 + yoe // 4 - yoe // 100 + doy
    return era * 146097 + doe - 719468


def civil_from_days(days: int) -> tuple[int, int, int]:
    days += 719468
    era = days // 146097
    doe = days - era * 146097
    yoe = (doe - doe // 1460 + doe // 36524 - doe // 146096) // 365
    doy = doe - (365 * yoe + yoe // 4 - yoe // 100)
    mp = (5 * doy + 2) // 153
    day = doy - (153 * mp + 2) // 5 + 1
    month = mp + (3 if mp < 10 else -9)
    return yoe + era * 400 + (month <= 2), month, day


def _weekday(days: int) -> int:
    """0 = Monday ... 6 = Sunday, for a day count since 1970-01-01 (a Thursday)."""
    return (days + 3) % 7


def _week_one_monday(year: int) -> int:
    jan4 = days_from_civil(year, 1, 4)
    return jan4 - _weekday(jan4)


def _weeks_in_year(year: int) -> int:
    jan1 = _weekday(days_from_civil(year, 1, 1))
    return 53 if jan1 == 3 or (jan1 == 2 and _is_leap(year)) else 52


# -- parsing ------------------------------------------------------------------


def _date_days(year: str, month: str, day: str) -> int | None:
    y, m, d = int(year), int(month), int(day)
    if y < 1 or not 1 <= m <= 12 or not 1 <= d <= _days_in_month(y, m):
        return None
    return days_from_civil(y, m, d)


def _time_ms(hour: str, minute: str, second: str | None, fraction: str | None) -> int | None:
    h, m, s = int(hour), int(minute), int(second or 0)
    if h > 23 or m > 59 or s > 59:
        return None
    ms = int((fraction or "0").ljust(3, "0"))
    return ((h * 60 + m) * 60 + s) * 1000 + ms


def parse(input_type: str, value: str) -> Decimal | None:
    """The type's "convert a string to a number"; ``None`` is an error."""
    if input_type in NUMBER_TYPES:
        if not _VALID_FLOAT.fullmatch(value):
            return None
        try:
            number = Decimal(value)
        except InvalidOperation:
            return None
        return number if number.is_finite() else None
    if input_type == "date":
        match = _DATE_RE.fullmatch(value)
        days = _date_days(*match.groups()) if match else None
        return None if days is None else Decimal(days * MS_PER_DAY)
    if input_type == "month":
        match = _MONTH_RE.fullmatch(value)
        if not match or int(match.group(1)) < 1 or not 1 <= int(match.group(2)) <= 12:
            return None
        return Decimal((int(match.group(1)) - 1970) * 12 + int(match.group(2)) - 1)
    if input_type == "week":
        match = _WEEK_RE.fullmatch(value)
        if not match:
            return None
        year, week = int(match.group(1)), int(match.group(2))
        if year < 1 or not 1 <= week <= _weeks_in_year(year):
            return None
        return Decimal((_week_one_monday(year) + (week - 1) * 7) * MS_PER_DAY)
    if input_type == "time":
        match = _TIME_RE.fullmatch(value)
        ms = _time_ms(*match.groups()) if match else None
        return None if ms is None else Decimal(ms)
    if input_type == "datetime-local":
        match = _LOCAL_RE.fullmatch(value)
        if not match:
            return None
        days = _date_days(*match.groups()[:3])
        ms = _time_ms(*match.groups()[3:])
        return None if days is None or ms is None else Decimal(days * MS_PER_DAY + ms)
    return None


# -- serialising ----------------------------------------------------------------


def _format_decimal(number: Decimal) -> str:
    text = format(number.normalize(), "f")
    return "0" if text in ("-0", "") else text


def _format_date(days: int) -> str | None:
    year, month, day = civil_from_days(days)
    if year < 1:
        return None
    return f"{year:04d}-{month:02d}-{day:02d}"


def _format_time(ms: int) -> str:
    ms %= MS_PER_DAY
    seconds, millis = divmod(ms, 1000)
    minutes, second = divmod(seconds, 60)
    hour, minute = divmod(minutes, 60)
    text = f"{hour:02d}:{minute:02d}"
    if second or millis:
        text += f":{second:02d}"
    if millis:
        text += f".{millis:03d}".rstrip("0")
    return text


def serialize(input_type: str, number: Decimal) -> str | None:
    """The type's "convert a number to a string"; ``None`` when there is none
    (a date before year 1)."""
    if input_type in NUMBER_TYPES:
        return _format_decimal(number)
    if input_type == "month":
        months = int(number.to_integral_value(ROUND_FLOOR))
        year, month = 1970 + months // 12, months % 12 + 1
        return f"{year:04d}-{month:02d}" if year >= 1 else None
    ms = int(number.to_integral_value(ROUND_FLOOR))
    if input_type == "date":
        return _format_date(ms // MS_PER_DAY)
    if input_type == "week":
        days = ms // MS_PER_DAY
        monday = days - _weekday(days)
        thursday = monday + 3  # the ISO week-numbering year is the Thursday's year
        year = civil_from_days(thursday)[0]
        if year < 1:
            return None
        return f"{year:04d}-W{(monday - _week_one_monday(year)) // 7 + 1:02d}"
    if input_type == "time":
        return _format_time(ms)
    if input_type == "datetime-local":
        date = _format_date(ms // MS_PER_DAY)
        return None if date is None else f"{date}T{_format_time(ms)}"
    return None


def to_date_ms(input_type: str, number: Decimal) -> int:
    """``valueAsDate``'s instant for a parsed value (month counts months)."""
    if input_type == "month":
        months = int(number)
        return days_from_civil(1970 + months // 12, months % 12 + 1, 1) * MS_PER_DAY
    return int(number)


def from_date_ms(input_type: str, ms: int) -> Decimal:
    """A ``valueAsDate`` instant in the type's own unit."""
    if input_type == "month":
        year, month, _day = civil_from_days(ms // MS_PER_DAY)
        return Decimal((year - 1970) * 12 + month - 1)
    return Decimal(ms)


# -- stepping (https://html.spec.whatwg.org/#dom-input-stepup) --------------------


def aligned(value: Decimal, base: Decimal, step: Decimal, direction: str) -> Decimal:
    """The nearest ``base + k * step`` at or beyond ``value`` in ``direction``
    (``"up"`` / ``"down"``)."""
    rounding = ROUND_CEILING if direction == "up" else ROUND_FLOOR
    return base + ((value - base) / step).to_integral_value(rounding) * step


def is_aligned(value: Decimal, base: Decimal, step: Decimal) -> bool:
    return ((value - base) % step) == 0
