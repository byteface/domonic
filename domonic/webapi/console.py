"""
domonic.webapi.console
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Console_API
"""

from __future__ import annotations

import builtins
import pprint
import sys
import time
import traceback
from collections.abc import Mapping, Sequence
from typing import Any


class Console:
    """Small Python implementation of the browser ``console`` object."""

    _counts: dict[str, int] = {}
    _timers: dict[str, float] = {}
    _profiles: dict[str, float] = {}
    _groups: list[str] = []
    _timestamps: list[tuple[str, float]] = []

    def __init__(self, *args: Any, reset: bool = False, **kwargs: Any) -> None:
        if reset:
            self.reset()

    @classmethod
    def reset(cls) -> None:
        """Reset counters, timers, profiles, timestamps, and group indentation."""
        cls._counts = {}
        cls._timers = {}
        cls._profiles = {}
        cls._groups = []
        cls._timestamps = []

    @staticmethod
    def _now() -> float:
        return time.perf_counter()

    @staticmethod
    def _format_ms(start: float, end: float | None = None) -> str:
        if end is None:
            end = Console._now()
        return f"{(end - start) * 1000:.3f}ms"

    @classmethod
    def _indent(cls) -> str:
        return "  " * len(cls._groups)

    @staticmethod
    def _stringify(value: Any) -> str:
        if isinstance(value, str):
            return value
        if isinstance(value, BaseException):
            return f"{value.__class__.__name__}: {value}"
        if isinstance(value, Mapping):
            return pprint.pformat(dict(value), compact=True, sort_dicts=False)
        if isinstance(value, (list, tuple, set, frozenset)):
            return pprint.pformat(value, compact=True, sort_dicts=False)
        return str(value)

    @staticmethod
    def _format_number(value: Any, *, integer: bool = False) -> str:
        try:
            number = float(value)
        except Exception:
            return "NaN"
        if integer:
            return str(int(number))
        return str(number)

    @classmethod
    def _format(cls, *data: Any) -> str:
        if not data:
            return ""

        first, *rest = data
        if not isinstance(first, str):
            return " ".join(cls._stringify(item) for item in data)

        output: list[str] = []
        rest_index = 0
        index = 0
        while index < len(first):
            char = first[index]
            if char != "%" or index + 1 >= len(first):
                output.append(char)
                index += 1
                continue

            token = first[index + 1]
            if token == "%":
                output.append("%")
                index += 2
                continue
            if token not in "sdifoOc":
                output.append(char)
                index += 1
                continue
            if rest_index >= len(rest):
                output.append("%" + token)
                index += 2
                continue

            value = rest[rest_index]
            rest_index += 1
            if token == "s":
                output.append(str(value))
            elif token in ("d", "i"):
                output.append(cls._format_number(value, integer=True))
            elif token == "f":
                output.append(cls._format_number(value))
            elif token in ("o", "O"):
                output.append(cls._stringify(value))
            elif token == "c":
                # Browser consoles consume CSS style arguments without rendering
                # them in the text stream.
                index += 2
                continue
            index += 2

        if rest_index < len(rest):
            output.append(" ")
            output.append(" ".join(cls._stringify(item) for item in rest[rest_index:]))
        return "".join(output).rstrip()

    @classmethod
    def _write(cls, line: str, *, stream: Any = None) -> str:
        rendered = cls._indent() + line
        print(rendered, file=stream or sys.stdout)
        return rendered

    @classmethod
    def log(cls, *data: Any, substitute: Any = None) -> str:
        """Outputs a message to the console."""
        if substitute is not None:
            if data:
                data = (data[0], substitute, *data[1:])
            else:
                data = (substitute,)
        return cls._write(cls._format(*data))

    @classmethod
    def info(cls, *data: Any, substitute: Any = None) -> str:
        """Outputs a message to the console with the info log level."""
        return cls.log(*data, substitute=substitute)

    @classmethod
    def debug(cls, *data: Any, substitute: Any = None) -> str:
        """Outputs a message to the console with the debug log level."""
        return cls.log(*data, substitute=substitute)

    @classmethod
    def warn(cls, *data: Any, substitute: Any = None) -> str:
        """Outputs a warning message."""
        return cls.log(*data, substitute=substitute)

    @classmethod
    def error(cls, *data: Any, substitute: Any = None) -> str:
        """Outputs an error message without raising it."""
        return cls.log(*data, substitute=substitute)

    @classmethod
    def exception(cls, *data: Any, substitute: Any = None) -> str:
        """Alias for :meth:`error`, matching browser and Node consoles."""
        return cls.error(*data, substitute=substitute)

    @classmethod
    def assert_(cls, assertion: bool, *data: Any) -> str | None:
        """Log an assertion message if ``assertion`` is false."""
        if assertion:
            return None
        message = "Assertion failed"
        if data:
            message += ": " + cls._format(*data)
        return cls._write(message)

    @classmethod
    def clear(cls) -> str:
        """Clear the terminal console when ANSI escape sequences are supported."""
        sequence = "\033[2J\033[H"
        print(sequence, end="")
        return sequence

    @classmethod
    def count(cls, label: str = "default") -> int:
        """Log and return the number of times a label has been counted."""
        label = "default" if label is None else str(label)
        cls._counts[label] = cls._counts.get(label, 0) + 1
        cls._write(f"{label}: {cls._counts[label]}")
        return cls._counts[label]

    @classmethod
    def countReset(cls, label: str = "default") -> int:
        """Reset a counter label to zero."""
        label = "default" if label is None else str(label)
        cls._counts[label] = 0
        cls._write(f"{label}: 0")
        return 0

    @classmethod
    def time(cls, label: str = "default") -> None:
        """Start a timer for ``label``."""
        label = "default" if label is None else str(label)
        cls._timers[label] = cls._now()

    @classmethod
    def timeLog(cls, label: str = "default", *data: Any) -> str | None:
        """Log elapsed time for an active timer."""
        label = "default" if label is None else str(label)
        start = cls._timers.get(label)
        if start is None:
            return cls._write(f"Timer '{label}' does not exist")
        line = f"{label}: {cls._format_ms(start)}"
        if data:
            line += " " + cls._format(*data)
        return cls._write(line)

    @classmethod
    def timeEnd(cls, label: str = "default") -> str | None:
        """Stop a timer and log the elapsed time."""
        label = "default" if label is None else str(label)
        start = cls._timers.pop(label, None)
        if start is None:
            return cls._write(f"Timer '{label}' does not exist")
        return cls._write(f"{label}: {cls._format_ms(start)}")

    @classmethod
    def timeStamp(cls, label: str = "default") -> str:
        """Record and log a timestamp marker."""
        label = "default" if label is None else str(label)
        timestamp = time.time()
        cls._timestamps.append((label, timestamp))
        return cls._write(f"Timestamp: {label}")

    @classmethod
    def group(cls, *data: Any) -> str:
        """Create a new inline group and indent following output."""
        label = cls._format(*data) if data else ""
        if label:
            cls._write(label)
        cls._groups.append(label)
        return label

    @classmethod
    def groupCollapsed(cls, *data: Any) -> str:
        """Create a collapsed group. In text output this behaves like group()."""
        return cls.group(*data)

    @classmethod
    def groupEnd(cls) -> None:
        """Exit the current inline group."""
        if cls._groups:
            cls._groups.pop()

    @classmethod
    def dir(cls, obj: Any) -> str:
        """Display a property listing for an object."""
        if isinstance(obj, Mapping):
            rendered = pprint.pformat(dict(obj), compact=True, sort_dicts=False)
        elif hasattr(obj, "__dict__"):
            rendered = pprint.pformat(vars(obj), compact=True, sort_dicts=False)
        else:
            rendered = pprint.pformat(builtins.dir(obj), compact=True)
        return cls._write(rendered)

    @classmethod
    def dirxml(cls, obj: Any) -> str:
        """Display an XML/HTML representation when one is available."""
        if hasattr(obj, "toxml") and callable(obj.toxml):
            rendered = obj.toxml()
        else:
            rendered = str(obj)
        return cls._write(rendered)

    @classmethod
    def table(cls, data: Any, columns: Sequence[str] | None = None) -> str:
        """Render tabular data as an ASCII table."""
        headers, rows = cls._normalize_table(data, columns)
        if not rows:
            return cls._write("(empty)")

        widths = [
            max(len(str(header)), *(len(str(row[index])) for row in rows))
            for index, header in enumerate(headers)
        ]
        border = "+" + "+".join("-" * (width + 2) for width in widths) + "+"

        def make_row(values: Sequence[Any]) -> str:
            cells = [
                " " + str(value).replace("\n", "\\n").ljust(widths[index]) + " "
                for index, value in enumerate(values)
            ]
            return "|" + "|".join(cells) + "|"

        lines = [border, make_row(headers), border]
        lines.extend(make_row(row) for row in rows)
        lines.append(border)
        rendered = "\n".join(lines)
        return cls._write(rendered)

    @classmethod
    def _normalize_table(
        cls, data: Any, columns: Sequence[str] | None = None
    ) -> tuple[list[str], list[list[str]]]:
        rows: list[dict[str, Any]] = []
        requested = [str(column) for column in columns] if columns else None

        if isinstance(data, Mapping):
            iterable = list(data.items())
        elif isinstance(data, Sequence) and not isinstance(
            data, (str, bytes, bytearray)
        ):
            iterable = list(enumerate(data))
        else:
            iterable = [(0, data)]

        keys: list[str] = []
        for index, value in iterable:
            row: dict[str, Any] = {"(index)": index}
            if isinstance(value, Mapping):
                row.update(value)
            elif isinstance(value, Sequence) and not isinstance(
                value, (str, bytes, bytearray)
            ):
                row.update({str(i): item for i, item in enumerate(value)})
            else:
                row["Value"] = value

            for key in row:
                key = str(key)
                if key not in keys:
                    keys.append(key)
            rows.append({str(key): value for key, value in row.items()})

        if requested is not None:
            headers = ["(index)"] + [key for key in requested if key != "(index)"]
        else:
            headers = keys

        rendered_rows = [
            [cls._stringify(row.get(header, "")) for header in headers] for row in rows
        ]
        return headers, rendered_rows

    @classmethod
    def trace(cls, *data: Any) -> str:
        """Output a stack trace."""
        label = cls._format(*data) if data else "Trace"
        stack = "".join(traceback.format_stack()[:-1]).rstrip()
        return cls._write(f"{label}\n{stack}")

    @classmethod
    def profile(cls, label: str = "default") -> None:
        """Start a lightweight profiler timer."""
        label = "default" if label is None else str(label)
        cls._profiles[label] = cls._now()

    @classmethod
    def profileEnd(cls, label: str = "default") -> str | None:
        """Stop a lightweight profiler timer and log its duration."""
        label = "default" if label is None else str(label)
        start = cls._profiles.pop(label, None)
        if start is None:
            return cls._write(f"Profile '{label}' does not exist")
        return cls._write(f"Profile '{label}': {cls._format_ms(start)}")


setattr(Console, "assert", Console.assert_)
console = Console
