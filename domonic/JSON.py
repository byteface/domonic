"""
domonic.JSON
============

JSON and table-conversion helpers used throughout domonic.

This module focuses on practical conversions between Python objects, JSON
payloads, CSV data, and simple HTML table structures.
"""

from __future__ import annotations

import csv
import json
from collections.abc import Iterable, Mapping
from pathlib import Path
from typing import Any

from domonic.decorators import as_json
from domonic.html import table, td, th, tr

return_json = as_json  # legacy. use the one in decorators package

RowsLike = str | bytes | bytearray | Mapping[str, Any] | Iterable[Mapping[str, Any]]


def parse_file(filepath: str | Path, **kwargs) -> Any:
    """Load a JSON file and return the decoded Python object.

    Args:
        filepath: Path to the JSON file.

    Returns:
        The decoded JSON value.
    """
    with open(filepath, encoding="utf-8") as json_file:
        return json.load(json_file, **kwargs)


def parse(json_string: str | bytes | bytearray, **kwargs) -> Any:
    """Parse a JSON string or bytes object.

    Args:
        json_string: JSON data as text or UTF-8 bytes.

    Returns:
        The decoded JSON value.
    """
    if isinstance(json_string, (bytes, bytearray)):
        json_string = json_string.decode("utf-8")
    return json.loads(json_string, **kwargs)


def stringify(data: Any, filepath: str | Path | None = None, **kwargs) -> str:
    """Serialize a Python object to JSON.

    Args:
        data: Python value to encode.
        filepath: Optional path to write the JSON payload to.

    Returns:
        The JSON string.
    """
    payload = json.dumps(data, **kwargs)
    if filepath is not None:
        with open(filepath, "w", encoding="utf-8") as json_file:
            json_file.write(payload)
    return payload


def _coerce_rows(value: RowsLike, name: str):
    if isinstance(value, (str, bytes, bytearray)):
        value = parse(value)
    if isinstance(value, Mapping):
        return [value]
    if isinstance(value, Iterable):
        rows = list(value)
        if all(isinstance(row, Mapping) for row in rows):
            return rows
    raise ValueError(f"{name} expects a dict or list of dicts")


def _get_headings(items, name: str) -> list[Any]:
    headings: list[Any] = []
    seen = set()
    for each in items:
        if not isinstance(each, Mapping):
            raise ValueError(f"{name} expects a dict or list of dicts")
        for key in each:
            if key not in seen:
                seen.add(key)
                headings.append(key)
    return headings


def tablify(arr: RowsLike):
    """tablify

    takes a json array and returns a html table

    Args:
        arr (list): the json array

    Returns:
        str: a html table
    """
    arr = _coerce_rows(arr, "tablify")
    t = table()
    headings = _get_headings(arr, "tablify")
    t.appendChild(tr(*[th(heading) for heading in headings]))
    for item in arr:
        row = tr(*[td(item.get(heading, "")) for heading in headings])
        t.appendChild(row)
    return t


def table2json(node) -> list[dict[str, str]]:
    """Convert a domonic table node back into a list of row dictionaries."""
    if getattr(node, "tagName", None) != "table":
        raise ValueError("table2json expects a domonic table element")

    rows = node.getElementsByTagName("tr")
    if not rows:
        return []

    heading_cells = rows[0].getElementsByTagName("th")
    if not heading_cells:
        heading_cells = rows[0].getElementsByTagName("td")
    headings = [heading.textContent for heading in heading_cells]
    items: list[dict[str, str]] = []
    for row in rows[1:]:
        cells = row.getElementsByTagName("td")
        items.append(
            {
                heading: cells[index].textContent if index < len(cells) else ""
                for index, heading in enumerate(headings)
            }
        )
    return items


def csvify(
    arr: RowsLike,
    outfile: str | Path = "data.csv",
) -> str:
    """csvify

    takes a json array and dumps a csv file

    Args:
        arr (list): the json array
        outfile (list): the output file

    Returns:
        str: a csv file
    """
    arr = _coerce_rows(arr, "csvify")
    headings = _get_headings(arr, "csvify")
    with open(outfile, "w", encoding="utf-8", newline="") as file:
        output = csv.writer(file)
        output.writerow(headings)
        for row in arr:
            output.writerow([row.get(heading, "") for heading in headings])
    return str(outfile)


def csv2json(
    csv_filepath: str | Path,
    json_filepath: str | Path | None = None,
) -> str:
    """
    convert a CSV to JSON.
    """
    items = []
    with open(csv_filepath, encoding="utf-8", newline="") as csvf:
        csv_reader = csv.DictReader(csvf)
        for row in csv_reader:
            items.append(row)

    payload = json.dumps(items)
    if json_filepath is None:
        return payload

    with open(json_filepath, "w", encoding="utf-8") as json_file:
        json.dump(items, json_file, indent=4)
    return payload


load = parse_file
loads = parse
dumps = stringify
json2csv = csvify


def dump(data: Any, filepath: str | Path | None = None, **kwargs) -> str:
    return stringify(data, filepath=filepath, **kwargs)


"""
def csv2json_hugefile(arr, infile="data.csv", start_row=0):

    def _load_data(csv_fname):
        with open(csv_fname, "r", encoding="latin-1") as records:
            for row in csv.reader(records):
                yield row

    items = iter(load_data(infile))
    headings = next(companies)

    for i in range(start_row):
        next(companies)

    for item in items:
        # TODO - streamwrite to json file.
"""


def flatten(b: Mapping[str, Any], delim: str = "__") -> dict[str, Any]:
    """
    # i.e. input = map( lambda x: JSON.flatten( x, "__" ), input )
    """
    val: dict[str, Any] = {}
    for key, value in b.items():
        if isinstance(value, Mapping):
            get = flatten(value, delim)
            for child_key, child_value in get.items():
                val[key + delim + child_key] = child_value
        else:
            val[key] = value

    return val


def is_json(value: str) -> bool:
    if not isinstance(value, str):
        return False
    value = value.strip()
    if not value:
        return False
    try:
        json.loads(value)
    except (TypeError, ValueError):
        return False
    return True
