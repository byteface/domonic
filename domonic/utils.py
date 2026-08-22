"""
domonic.utils
====================================
snippets etc
"""

import math
import random
import re
from collections import Counter
from dataclasses import dataclass
from itertools import chain, islice
from numbers import Real
from re import sub
from typing import Any, Iterable, Iterator, Sequence, TypeVar

from domonic.decorators import deprecated

T = TypeVar("T")
D = TypeVar("D")
_random = random.SystemRandom()
_NUMBER_UNIT_RE = re.compile(
    r"^\s*([+-]?(?:\d[\d,_]*(?:\.\d*)?|\.\d+)(?:[eE][+-]?\d+)?)\s*([a-zA-Z%]*)\s*$"
)


@dataclass(frozen=True)
class NumberUnit:
    """A parsed numeric value and its optional unit suffix."""

    value: float
    unit: str = ""

    @property
    def number(self) -> int | float:
        """Return integers as ``int`` while preserving fractional values."""
        if self.value.is_integer():
            return int(self.value)
        return self.value


class NumberUtils:
    """Small numeric helpers for CSS values, web sizes, percentages, and ports."""

    BYTE_UNITS = {
        "": 1,
        "b": 1,
        "byte": 1,
        "bytes": 1,
        "k": 1000,
        "kb": 1000,
        "m": 1000**2,
        "mb": 1000**2,
        "g": 1000**3,
        "gb": 1000**3,
        "t": 1000**4,
        "tb": 1000**4,
        "p": 1000**5,
        "pb": 1000**5,
        "ki": 1024,
        "kib": 1024,
        "mi": 1024**2,
        "mib": 1024**2,
        "gi": 1024**3,
        "gib": 1024**3,
        "ti": 1024**4,
        "tib": 1024**4,
        "pi": 1024**5,
        "pib": 1024**5,
    }

    @staticmethod
    def _as_float(value: Any, name: str = "value") -> float:
        try:
            return NumberUtils.parse_unit(value).value
        except (TypeError, ValueError, OverflowError) as exc:
            raise ValueError(f"{name} must be a finite number") from exc

    @staticmethod
    def _coerce_number(value: float) -> int | float:
        return int(value) if value.is_integer() else value

    @staticmethod
    def is_number(value: Any) -> bool:
        """Return ``True`` for finite real numbers, excluding booleans."""
        if isinstance(value, bool) or not isinstance(value, Real):
            return False
        try:
            return math.isfinite(value)
        except (TypeError, ValueError, OverflowError):
            return False

    @staticmethod
    def parse_unit(value: Any) -> NumberUnit:
        """Parse a number or a string such as ``"12px"``, ``"1.5rem"``, or ``"50%"``."""
        if isinstance(value, bool):
            raise ValueError("boolean values are not numeric")

        if isinstance(value, Real):
            number = float(value)
            if not math.isfinite(number):
                raise ValueError("value must be finite")
            return NumberUnit(number)

        match = _NUMBER_UNIT_RE.match(str(value))
        if not match:
            raise ValueError("value must be a number or number+unit string")

        number = float(match.group(1).replace(",", "").replace("_", ""))
        if not math.isfinite(number):
            raise ValueError("value must be finite")
        return NumberUnit(number, match.group(2))

    @staticmethod
    def to_number(value: Any, default: D | None = None) -> int | float | D | None:
        """Convert a number-like value to ``int`` or ``float``; return ``default`` on failure."""
        try:
            return NumberUtils.parse_unit(value).number
        except (TypeError, ValueError, OverflowError):
            return default

    @staticmethod
    def clamp(value: Any, min_value: Any = None, max_value: Any = None) -> int | float:
        """Clamp ``value`` between optional minimum and maximum bounds."""
        number = NumberUtils._as_float(value)
        minimum = None if min_value is None else NumberUtils._as_float(min_value, "min_value")
        maximum = None if max_value is None else NumberUtils._as_float(max_value, "max_value")

        if minimum is not None and maximum is not None and minimum > maximum:
            raise ValueError("min_value cannot be greater than max_value")
        if minimum is not None:
            number = max(number, minimum)
        if maximum is not None:
            number = min(number, maximum)
        return NumberUtils._coerce_number(number)

    @staticmethod
    def normalize(value: Any, min_value: Any, max_value: Any, clamp_result: bool = False) -> float:
        """Map ``value`` from the given range to a ratio between ``0`` and ``1``."""
        number = NumberUtils._as_float(value)
        minimum = NumberUtils._as_float(min_value, "min_value")
        maximum = NumberUtils._as_float(max_value, "max_value")
        if minimum == maximum:
            raise ValueError("min_value and max_value cannot be the same")
        result = (number - minimum) / (maximum - minimum)
        if clamp_result:
            return float(NumberUtils.clamp(result, 0, 1))
        return result

    @staticmethod
    def lerp(start: Any, end: Any, amount: Any) -> int | float:
        """Linearly interpolate between ``start`` and ``end`` by ``amount``."""
        start_number = NumberUtils._as_float(start, "start")
        end_number = NumberUtils._as_float(end, "end")
        amount_number = NumberUtils._as_float(amount, "amount")
        return NumberUtils._coerce_number(
            start_number + (end_number - start_number) * amount_number
        )

    @staticmethod
    def remap(
        value: Any,
        in_min: Any,
        in_max: Any,
        out_min: Any,
        out_max: Any,
        clamp_result: bool = False,
    ) -> int | float:
        """Map ``value`` from one numeric range into another."""
        ratio = NumberUtils.normalize(value, in_min, in_max, clamp_result)
        output = NumberUtils.lerp(out_min, out_max, ratio)
        return NumberUtils._coerce_number(float(output))

    @staticmethod
    def percent(value: Any, total: Any, scale: Any = 100.0) -> int | float:
        """Return ``value`` as a percentage of ``total``."""
        total_number = NumberUtils._as_float(total, "total")
        if total_number == 0:
            raise ValueError("total cannot be zero")
        result = (NumberUtils._as_float(value) / total_number) * NumberUtils._as_float(
            scale, "scale"
        )
        return NumberUtils._coerce_number(result)

    @staticmethod
    def parse_percent(value: Any, total: Any = 1.0) -> int | float:
        """Resolve a percentage string against ``total``; plain numbers pass through unchanged."""
        parsed = NumberUtils.parse_unit(value)
        if parsed.unit == "%":
            return NumberUtils._coerce_number(
                (parsed.value / 100.0) * NumberUtils._as_float(total, "total")
            )
        if parsed.unit:
            raise ValueError("percentage values may only use the '%' unit")
        return parsed.number

    @staticmethod
    def parse_bytes(value: Any) -> int:
        """Parse byte-size strings such as ``"1KB"`` or ``"1.5 MiB"`` into bytes."""
        parsed = NumberUtils.parse_unit(value)
        unit = parsed.unit.lower()
        if unit not in NumberUtils.BYTE_UNITS:
            raise ValueError(f"unknown byte unit: {parsed.unit}")
        return int(parsed.value * NumberUtils.BYTE_UNITS[unit])

    @staticmethod
    def format_bytes(value: Any, binary: bool = False, precision: int = 1) -> str:
        """Format a byte count with decimal units or binary IEC units."""
        if precision < 0:
            raise ValueError("precision cannot be negative")

        number = NumberUtils._as_float(value)
        base = 1024 if binary else 1000
        units = (
            ["B", "KiB", "MiB", "GiB", "TiB", "PiB"]
            if binary
            else ["B", "KB", "MB", "GB", "TB", "PB"]
        )
        sign = "-" if number < 0 else ""
        number = abs(number)
        index = 0

        while number >= base and index < len(units) - 1:
            number /= base
            index += 1

        if index == 0:
            formatted = str(int(number))
        else:
            formatted = f"{number:.{precision}f}".rstrip("0").rstrip(".")
        return f"{sign}{formatted} {units[index]}"

    @staticmethod
    def is_port(value: Any, allow_zero: bool = True) -> bool:
        """Return whether ``value`` is a valid TCP/UDP port number."""
        return NumberUtils.to_port(value, allow_zero=allow_zero) is not None

    @staticmethod
    def to_port(value: Any, default: D | None = None, allow_zero: bool = True) -> int | D | None:
        """Convert ``value`` to a port number, returning ``default`` when invalid."""
        if isinstance(value, bool):
            return default
        try:
            port = int(str(value).strip())
        except (TypeError, ValueError):
            return default
        minimum = 0 if allow_zero else 1
        if minimum <= port <= 65535:
            return port
        return default


class Utils:
    """Utils"""

    @staticmethod
    def case_camel(s: str) -> str:
        """case_camel('camel-case') > 'camelCase'"""
        s = sub(r"(_|-)+", " ", s).title().replace(" ", "")
        return s[0].lower() + s[1:]

    @staticmethod
    def case_snake(s: str) -> str:
        """
        snake('camelCase') # 'camel_case'
        """
        return "_".join(
            sub(
                "([A-Z][a-z]+)", r" \1", sub("([A-Z]+)", r" \1", s.replace("-", " "))
            ).split()
        ).lower()

    @staticmethod
    def case_kebab(s: str) -> str:
        """
        kebab('camelCase') # 'camel-case'
        """
        return "-".join(
            sub(
                r"(\s|_|-)+",
                " ",
                sub(
                    r"[A-Z]{2,}(?=[A-Z][a-z]+[0-9]*|\b)|[A-Z]?[a-z]+[0-9]*|[A-Z]|[0-9]+",
                    lambda mo: " " + mo.group(0).lower(),
                    s,
                ),
            ).split()
        )

    @staticmethod
    def squash(the_list: Iterable[Iterable[T]]) -> list[T]:
        """[turns a 2d array into a flat one]

        Args:
            the_list ([list]): [a 2d array]

        Returns:
            [list]: [a flattened 1d array]
        """
        return [inner for outer in the_list for inner in outer]

    @staticmethod
    def chunk(values: Sequence[T], size: int) -> list[Sequence[T]]:
        """chunk a list into batches"""
        return [values[i : i + size] for i in range(0, len(values), size)]

    @staticmethod
    def dictify(arr: Iterable[T]) -> dict[T, int]:
        """[turns a list into a dictionary where the list items are the keys]

        Args:
            arr ([list]): [list to change]

        Returns:
            [dict]: [a new dict where the list items are now the keys]
        """
        return {}.fromkeys(arr, 0)

    @staticmethod
    def is_empty(some_str: str) -> bool:
        return not some_str.strip()

    @staticmethod
    def unique(some_arr: Iterable[T]) -> list[T]:
        """[removes duplicates from a list]

        Args:
            some_arr ([list]): [list containing duplicates]

        Returns:
            [list]: [a list containing no duplicates]
        """
        return list(set(some_arr))

    @staticmethod
    def chunks(iterable: Iterable[T], size: int, format: Any = iter) -> Iterator[Any]:
        """Iterate over any iterable (list, set, file, stream, strings, whatever), of ANY size"""
        it = iter(iterable)
        while True:
            try:
                first = next(it)
            except StopIteration:
                return
            yield format(chain((first,), islice(it, size - 1)))

    # >>> l = ["a", "b", "c", "d", "e", "f", "g"]
    # >>> for chunk in chunks(l, 3, tuple):
    # ...         print chunk

    @staticmethod
    def clean(lst: Iterable[T]) -> list[T]:
        """[removes falsy values (False, None, 0 and “”) from a list ]

        Args:
            lst ([list]): [lst to operate on]

        Returns:
            [list]: [a new list with falsy values removed]
        """
        return list(filter(None, lst))

    @staticmethod
    def get_vowels(string: str) -> list[str]:
        """[get a list of vowels from the word]

        Args:
            string ([str]): [the word to check]

        Returns:
            [list]: [a list of vowels]
        """
        return [each for each in string if each in "aeiou"]

    @staticmethod
    def untitle(string: str) -> str:
        """[the opposite of title]

        Args:
            str ([str]): [the string to change]

        Returns:
            [str]: [a string with the first character set to lowercase]
        """
        return string[:1].lower() + string[1:]

    @staticmethod
    def merge_dictionaries(a: dict[Any, Any], b: dict[Any, Any]) -> dict[Any, Any]:
        """[merges 2 dicts]

        Args:
            a ([dict]): [dict a]
            b ([dict]): [dict b]

        Returns:
            [dict]: [a new dict]
        """
        return {**a, **b}

    @staticmethod
    def to_dictionary(keys: Iterable[T], values: Iterable[Any]) -> dict[T, Any]:
        """[take a list of keys and values and returns a dict]

        Args:
            keys ([list]): [a list of keys]
            values ([list]): [a list of value]

        Returns:
            [dict]: [a dictionary]
        """
        return dict(zip(keys, values))

    @staticmethod
    def most_frequent(lst: Sequence[T]) -> T:
        return max(set(lst), key=lst.count)

    @staticmethod
    def is_anagram(first: str, second: str) -> bool:
        return Counter(first) == Counter(second)

    @staticmethod
    def is_palindrome(word: str) -> bool:
        return word == word[::-1]

    @staticmethod
    def acronym(sentence: str) -> str:
        """[pass a sentence, returns the acronym]

        Args:
            sentence ([str]): [typically 3 words]

        Returns:
            [str]: [a TLA (three letter acronym)]
        """
        text = sentence.split()
        a = ""
        for i in text:
            a = a + str(i[0]).upper()
        return a

    @staticmethod
    def frequency(data: Iterable[T]) -> dict[T, int]:
        """[check the frequency of elements in the data]

        Args:
            data ([type]): [the data to check]

        Returns:
            [dict]: [a dict of elements and their frequency]
        """
        freq = {}
        for elem in data:
            if elem in freq:
                freq[elem] += 1
            else:
                freq[elem] = 1
        return freq

    @staticmethod
    def init_assets(dir: str = "assets") -> None:
        """[creates an assets directory with nested js/css/img dirs]

        Args:
            dir (str, optional): [default directory name]. Defaults to 'assets'.
        """
        from domonic.terminal import mkdir, touch

        mkdir(f"{dir}")
        mkdir(f"{dir}/js")
        mkdir(f"{dir}/css")
        mkdir(f"{dir}/img")
        touch(f"{dir}/js/master.js")
        touch(f"{dir}/css/style.css")
        return

    @staticmethod
    def url2file(url: str) -> str:
        """[gen a safe filename from a url. by replacing '/' for '_' and ':' for '__' ]

        Args:
            url ([str]): [the url to turn into a filename]

        Returns:
            [str]: [description]
        """
        import urllib

        url = "_".join(url.split("/"))
        url = "__".join(url.split(":"))
        filename = urllib.parse.quote_plus(url, "")
        return filename

    @staticmethod
    def permutations(word: str) -> list:
        """[provides all the possible permutations of a given word]

        Args:
            word ([str]): [the word to get permutations for]

        Returns:
            [list]: [a list of permutations]
        """
        from itertools import permutations

        return ["".join(perm) for perm in list(permutations(word))]

    @staticmethod  # TODO - remove as we have color class. (might be getting used in examples)
    def random_color(self):
        r = lambda: _random.randint(0, 255)
        return str("#%02X%02X%02X" % (r(), r(), r()))

    @staticmethod
    def escape(s: str) -> str:
        """[escape a string]

        Args:
            s ([str]): [the string to escape]

        Returns:
            [str]: [the escaped string]
        """
        chars = {"&": "&amp;", '"': "&quot;", "'": "&apos;", ">": "&gt;", "<": "&lt;"}
        return "".join(chars.get(c, c) for c in s)

    @staticmethod
    def unescape(s: str) -> str:
        """[unescape a string]

        Args:
            s ([str]): [the string to unescape]

        Returns:
            [str]: [the unescaped string]
        """
        s = s.replace("&lt;", "<")
        s = s.replace("&gt;", ">")
        s = s.replace("&quot;", '"')
        s = s.replace("&apos;", "'")
        s = s.replace("&amp;", "&")
        return s

    @staticmethod
    def replace_between(
        content: str, match: str, replacement: str, start: int = 0, end: int = 0
    ):
        """[replace some text but only between certain indexes]

        Args:
            content (str): [the content whos text you will be replacing]
            match (str): [the string to find]
            replacement (str): [the string to replace it with]
            start (int, optional): [start index]. Defaults to 0.
            end (int, optional): [end index]. Defaults to 0.

        Returns:
            [str]: [the new string]
        """
        front = content[0:start]
        mid = content[start:end]
        end = content[end : len(content)]
        mid = mid.replace(match, replacement)
        return front + mid + end

    @staticmethod
    def truncate(text: str = "", length: int = 0) -> str:
        """[truncates a string and appends 3 dots]

        Args:
            text (str, optional): [the text to truncate]. Defaults to ''.
            length (int, optional): [the max length]. Defaults to 0.

        Returns:
            [str]: [the truncated string]
        """
        if len(text) > length:
            return text[0:length] + "..."
        else:
            return text + "..."

    @staticmethod
    def digits(text: str = "") -> str:
        """[takes a string of mix of digits and letters and returns a string of digits]

        Args:
            text (str, optional): [the text to change]. Defaults to ''.

        Returns:
            [str]: [a string of digits]
        """
        if isinstance(text, int):
            return str(text)
        elif isinstance(text, float):
            return str(int(text))
        elif isinstance(text, str):
            return "".join(i for i in text if i.isdigit())
        else:
            try:
                return str(text)
            except Exception:
                raise ValueError("text must be a string")

    @staticmethod
    def has_internet(url: str = "http://www.google.com/", timeout: int = 5) -> bool:
        """[check if you have internet connection]

        Args:
            url (str, optional): [the url to check]. Defaults to 'http://www.google.com/'.
            timeout (int, optional): [the timeout]. Defaults to 5.

        Returns:
            [bool]: [True if you have internet]
        """
        import requests

        try:
            _ = requests.head(url, timeout=timeout)
            return True
        except requests.ConnectionError:
            # print("No internet connection available.")
            return False

    @staticmethod
    def is_nix() -> bool:
        """[check if the system is a nix based system]

        Returns:
            [bool]: [True if it is a nix based system]
        """
        import os

        return os.name == "posix"

    @staticmethod
    def is_mac() -> bool:
        """[check if the system is a mac]

        Returns:
            [bool]: [True if the system is a mac]
        """
        import sys

        return sys.platform == "darwin"

    @staticmethod
    def is_windows() -> bool:
        """[check if the system is a windows]

        Returns:
            [bool]: [True if windows]
        """
        import os

        return os.name == "nt"

    @staticmethod
    def is_linux() -> bool:
        """[check if the system is a linux]

        Returns:
            [bool]: [description]
        """
        import sys

        return sys.platform.startswith("linux")

    # def convert_file(filepath, filetype=None):
    #     """
    #         convert a file to a different file type
    #         mostly deals with config files
    #     """
    #  files = ['json', 'ini', 'xml', 'yaml', 'yml', 'toml', 'properties', 'conf', 'rc', 'sh', 'bash', 'bat', 'cmd', 'c', 'cpp', 'h', 'hpp', 'java', 'js', 'json', 'md', 'markdown', 'pl', 'py', 'rb', 'sh', 'sql', 'txt', 'xml', 'yaml', 'yml', 'toml']

    '''
    @staticmethod
    def yeahnah(x):
        """ returns a boolean for any given user reply
        """
        reply = x.lower()
        if reply.lower() in ['yeah', "y", "yes", "yup", "si", "yep", "yeah", "yep"]:
            return True
        elif reply.lower() in ['nah', "no", "nope", "n"]:
            return False
        else:
            # return a probability between 0 and 1 for either yes or no based on which list has the most similar words to the input
            # return max([float(reply.count(x)) / len(reply) for x in ['yeah', "y", "yes", "yup", "si", "yep", "yeah", "yep"]]) > max([float(reply.count(x)) / len(reply) for x in ['nah', "n", "no", "nope", "nop", "nope", "n", "nope"]])
            # return max([float(reply.count(x)) / len(reply) for x in ['yeah', "y", "yes", "yup", "si", "yep", "yeah", "yep"]]) > 0.5
        else:
            return None
    '''

    # def get_ip(self):
    #     """[get the current ip]

    #     Returns:
    #         [str]: [the current ip]
    #     """
    #     import socket
    #     return socket.gethostbyname(socket.gethostname())

    # def get_hostname(self):
    #     """[get the current hostname]

    #     Returns:
    #         [str]: [the current hostname]
    #     """
    #     import socket
    #     return socket.gethostname()

    # def get_mac(self):
    #     """[get the current mac]

    #     Returns:
    #         [str]: [the current mac]
    #     """
    #     import uuid
    #     return uuid.UUID(int=uuid.getnode()).hex[-12:]

    # def get_ip_mac(self):
    #     """[get the current ip and mac]

    #     Returns:
    #         [str]: [the current ip and mac]
    #     """
    #     return self.get_ip() + "|" + self.get_mac()

    # def get_os(self):
    #     """[get the current os]

    #     Returns:
    #         [str]: [the current os]
    #     """
    #     import platform
    #     return platform.system()

    # def get_os_version(self):
    #     """[get the current os version]

    #     Returns:
    #         [str]: [the current os version]
    #     """
    #     import platform
    #     return platform.release()

    # def get_os_arch(self):
    #     """[get the current os architecture]

    #     Returns:
    #         [str]: [the current os architecture]
    #     """
    #     import platform
    #     return platform.machine()

    # def get_cpu(self):
    #     """[get the current cpu]

    #     Returns:
    #         [str]: [the current cpu]
    #     """
    #     import platform
    #     return platform.processor()

    @staticmethod
    def numberToBase(n, b):
        if n == 0:
            return [0]
        digits = []
        while n:
            digits.append(int(n % b))
            n //= b
        return digits[::-1]
