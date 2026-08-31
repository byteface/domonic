"""
diffDOM-style patches with domonic.

The diff is plain data, so it can be logged, stored, sent over a socket, or
applied later to another compatible DOM tree.
"""

import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from domonic.diffdom import DiffDOM
from domonic.html import button, div, h1, p

old = div(h1("Hello"), p("Version one"))
new = div(h1("Hello"), p("Version two"), button("Save"))

dd = DiffDOM()
changes = dd.diff(old, new)

print(json.dumps(changes, indent=2))
print("before:", old)

dd.apply(old, changes)

print("after: ", old)
print("match: ", str(old) == str(new))
