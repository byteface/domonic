"""
domonic.d3
====================================

Ported d3 modules: array, color, dispatch, format, hierarchy, interpolate,
path, polygon, queue, scale, selection, shape, tile, time, timer.

Not yet ported: axis, brush, chord, contour, delaunay, drag, dsv, ease, fetch,
force, geo, quadtree, random, scale-chromatic, time-format, transition, zoom.
"""

from domonic.d3.array import *
from domonic.d3.color import *
from domonic.d3.dispatch import *
from domonic.d3.format import *
from domonic.d3.hierarchy import *  # hierarchy's own Node (its internal
# tree-node helper, not part of d3.js's public API) is superseded below by
# the DOM Node class, via d3.selection / domonic.html -- nothing imports
# Node from domonic.d3 today, but that's the one that wins, matching every
# other d3 submodule operating on the DOM.
from domonic.d3.interpolate import *
from domonic.d3.path import *
from domonic.d3.polygon import *
from domonic.d3.queue import *
from domonic.d3.scale import *
from domonic.d3.selection import *  # type: ignore[assignment]
from domonic.d3.shape import *
from domonic.d3.tile import *
from domonic.d3.time import *
from domonic.d3.timer import *
from domonic.dom import document
from domonic.html import *  # type: ignore[assignment]
