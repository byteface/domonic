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
from collections.abc import Mapping, Sequence
from pathlib import Path
from typing import Any

from domonic.decorators import as_json
from domonic.html import table, td, th, tr

return_json = as_json  # legacy. use the one in decorators package


def parse_file(filepath: str | Path) -> Any:
    """[loads a json file and returns a python object]

    Args:
        filepath (str): [path to json file]

    Returns:
        [type]: [a python object]
    """
    with open(filepath, encoding="utf-8") as json_file:
        return json.load(json_file)


def parse(json_string: str | bytes | bytearray) -> Any:
    """[take a json string and return a python object]

    Args:
        json_string (str): [a json string]

    Returns:
        [type]: [a python object]
    """
    if isinstance(json_string, (bytes, bytearray)):
        json_string = json_string.decode("utf-8")
    return json.loads(json_string)


def stringify(data: Any, filepath: str | Path | None = None, **kwargs) -> str:
    """[stringify a python object]

    Args:
        data ([type]): [the python object]
        filepath (str, optional): [an optional filepath to save the stringified object] [default: None]

    Returns:
        [type]: [the stringified object]
    """
    payload = json.dumps(data, **kwargs)
    if filepath is not None:
        with open(filepath, "w", encoding="utf-8") as json_file:
            json_file.write(payload)
    return payload


def tablify(arr: str | Mapping[str, Any] | Sequence[Mapping[str, Any]]):
    """tablify

    takes a json array and returns a html table

    Args:
        arr (list): the json array

    Returns:
        str: a html table
    """

    def _get_headings(items, node):
        headings: list[str] = []
        row = tr()
        for each in items:
            if not isinstance(each, Mapping):
                raise ValueError("tablify expects a dict or list of dicts")
            for key in each:
                if key not in headings:
                    headings.append(key)
                    row.appendChild(th(key))
        node.appendChild(row)
        return headings

    if isinstance(arr, str):
        arr = json.loads(arr)
    if isinstance(arr, dict):
        arr = [arr]
    if not isinstance(arr, Sequence):
        raise ValueError("tablify expects a dict or list of dicts")

    t = table()
    headings = _get_headings(arr, t)
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

    headings = [heading.textContent for heading in rows[0].getElementsByTagName("th")]
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


def csvify(arr: str | Mapping[str, Any] | Sequence[Mapping[str, Any]], outfile: str | Path = "data.csv") -> str:
    """csvify

    takes a json array and dumps a csv file

    Args:
        arr (list): the json array
        outfile (list): the output file

    Returns:
        str: a csv file
    """
    if isinstance(arr, str):
        arr = json.loads(arr)  # leniency. allow for a string
    elif isinstance(arr, dict):
        arr = [arr]
    if not isinstance(arr, Sequence):
        raise ValueError("csvify expects a dict or list of dicts")

    def _get_headings(items):
        headings: list[str] = []
        for each in items:
            if not isinstance(each, Mapping):
                raise ValueError("csvify expects a dict or list of dicts")
            for key in each:
                if key not in headings:
                    headings.append(key)
        return headings

    headings = _get_headings(arr)
    with open(outfile, "w", encoding="utf-8", newline="") as file:
        output = csv.writer(file)
        output.writerow(headings)
        for row in arr:
            output.writerow([row.get(heading, "") for heading in headings])
    return str(outfile)


def csv2json(csv_filepath: str | Path, json_filepath: str | Path | None = None) -> str:
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
    for i in b.keys():
        if isinstance(b[i], dict):
            get = flatten(b[i], delim)
            for j in get.keys():
                val[i + delim + j] = get[j]
        else:
            val[i] = b[i]

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
