"""
File API example
================

This is useful when you want browser-style file handling in Python code:
generate a file-like object, preview it, pass it to fetch/FormData-style APIs,
or expose it through an object URL.
"""

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.html import form, input
from domonic.webapi.file import File, FileList, FileReader
from domonic.webapi.fetch import fetch
from domonic.webapi.url import URL
from domonic.webapi.xhr import FormData


report = File(
    [
        "name,score\n",
        "Ada,100\n",
        "Grace,98\n",
    ],
    "scores.csv",
    {"type": "text/csv", "lastModified": 1_725_000_000_000},
)

reader = FileReader()
reader.onload = lambda event: print("Preview:\n" + reader.result)
reader.readAsText(report)

object_url = URL.createObjectURL(report)
response = fetch(object_url).data
print("Fetched from object URL:", response.text().splitlines()[0])
URL.revokeObjectURL(object_url)

upload_form = form(input(type="file", name="scores"))
upload_form.querySelector("input").files = FileList([report])

data = FormData(upload_form)
print("FormData field:", data.get("scores").name)
print("FormData encoded fallback:", data.toString())
