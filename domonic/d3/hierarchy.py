"""
domonic.d3.hierarchy
====================================

A port of `d3-hierarchy <https://github.com/d3/d3-hierarchy>`_ (v3): the
``hierarchy`` / ``stratify`` constructors and the ``tree``, ``cluster``,
``partition``, ``treemap`` and ``pack`` layouts.
"""

from __future__ import annotations

import math
import random as _random
from typing import Any, Callable, Iterable

__all__ = [
    "hierarchy", "Node", "stratify", "tree", "cluster", "partition", "treemap",
    "pack", "packSiblings", "packEnclose", "treemapBinary", "treemapDice",
    "treemapSlice", "treemapSliceDice", "treemapSquarify", "treemapResquarify",
]


class Node:
    def __init__(self, data: Any) -> None:
        self.data = data
        self.depth = 0
        self.height = 0
        self.parent: "Node | None" = None
        self.children: list["Node"] | None = None
        self.value: float | None = None
        # layout coordinates (filled in by a layout)
        self.x = 0.0
        self.y = 0.0
        self.x0 = self.y0 = self.x1 = self.y1 = 0.0
        self.r = 0.0
        self._pack_center = (0.0, 0.0)

    # -- traversal ----------------------------------------------------
    def each(self, callback: Callable, that: Any = None) -> "Node":
        index = 0
        queue = [self]
        while queue:
            node = queue.pop(0)
            callback(node, index, self) if that is None else callback(that, node, index, self)
            index += 1
            if node.children:
                queue.extend(node.children)
        return self

    def eachBefore(self, callback: Callable, that: Any = None) -> "Node":
        index = 0
        nodes = [self]
        while nodes:
            node = nodes.pop()
            callback(node, index, self)
            index += 1
            if node.children:
                nodes.extend(reversed(node.children))
        return self

    def eachAfter(self, callback: Callable, that: Any = None) -> "Node":
        index = 0
        nodes = [self]
        next_nodes: list[Node] = []
        while nodes:
            node = nodes.pop()
            next_nodes.append(node)
            if node.children:
                nodes.extend(node.children)
        while next_nodes:
            node = next_nodes.pop()
            callback(node, index, self)
            index += 1
        return self

    def find(self, callback: Callable) -> "Node | None":
        found: list[Node] = []
        self.each(lambda n, *_: found.append(n) if not found and callback(n) else None)
        return found[0] if found else None

    # -- aggregation --------------------------------------------------
    def sum(self, value: Callable[[Any], float]) -> "Node":
        def visit(node: Node, *_a):
            total = float(value(node.data) or 0)
            for child in (node.children or []):
                total += child.value or 0
            node.value = total

        return self.eachAfter(visit)

    def count(self) -> "Node":
        return self.eachAfter(_count_children)

    # -- structure --------------------------------------------------
    def sort(self, compare: Callable[["Node", "Node"], float]) -> "Node":
        import functools

        def visit(node: Node, *_a):
            if node.children:
                node.children.sort(
                    key=functools.cmp_to_key(lambda a, b: _cmp(compare(a, b)))
                )

        return self.eachBefore(visit)

    def path(self, end: "Node") -> list["Node"]:
        start: "Node | None" = self
        ancestor = _least_common_ancestor(self, end)
        nodes: list[Node] = [self]
        while start is not ancestor and start is not None:
            start = start.parent
            if start is not None:
                nodes.append(start)
        k = len(nodes)
        cur: "Node | None" = end
        while cur is not ancestor and cur is not None:
            nodes.insert(k, cur)
            cur = cur.parent
        return nodes

    def ancestors(self) -> list["Node"]:
        node: "Node | None" = self
        out: list[Node] = [self]
        while node is not None and node.parent is not None:
            node = node.parent
            out.append(node)
        return out

    def descendants(self) -> list["Node"]:
        out: list[Node] = []
        self.each(lambda n, *_: out.append(n))
        return out

    def leaves(self) -> list["Node"]:
        out: list[Node] = []
        self.eachBefore(lambda n, *_: out.append(n) if not n.children else None)
        return out

    def links(self) -> list[dict]:
        root = self
        out: list[dict] = []
        root.each(
            lambda node, *_: out.append({"source": node.parent, "target": node})
            if node is not root
            else None
        )
        return out

    def copy(self) -> "Node":
        return hierarchy(self).eachBefore(_copy_data)

    def __iter__(self):
        return iter(self.descendants())


def _count_children(node: Node, *_a) -> None:
    total = 0.0
    children = node.children
    i = len(children) if children else 0
    if not i:
        total = 1
    else:
        for child in (children or []):
            total += child.value or 0
    node.value = total


def _copy_data(node: Node, *_a) -> None:
    if node.data is not None and hasattr(node.data, "data"):
        node.data = node.data.data


def _cmp(x: float) -> int:
    return 0 if x != x else (-1 if x < 0 else (1 if x > 0 else 0))


def _least_common_ancestor(a: "Node | None", b: "Node | None") -> "Node | None":
    if a is None or b is None:
        return None
    if a is b:
        return a
    a_nodes = a.ancestors()
    b_nodes = b.ancestors()
    c = None
    a_nodes.reverse()
    b_nodes.reverse()
    for x, y in zip(a_nodes, b_nodes):
        if x is y:
            c = x
        else:
            break
    return c


def _default_children(d: Any):
    if isinstance(d, dict):
        return d.get("children")
    return getattr(d, "children", None)


def hierarchy(data: Any, children: Callable[[Any], Any] | None = None) -> Node:
    """Build a :class:`Node` tree from hierarchical *data*."""
    if children is None:
        children = _default_children
    root = Node(data)
    nodes = [root]
    while nodes:
        node = nodes.pop()
        child_data = children(node.data)
        if child_data:
            child_list = list(child_data)
            node.children = []
            for cd in child_list:
                child = Node(cd)
                child.parent = node
                child.depth = node.depth + 1
                node.children.append(child)
                nodes.append(child)

    def set_height(n: Node, *_a):
        h = 0
        if n.children:
            h = max(c.height for c in n.children) + 1
        n.height = h

    root.eachAfter(set_height)
    root.parent = None
    root.depth = 0
    return root


# -- stratify ---------------------------------------------------

def stratify():
    id_accessor: Callable[[Any], Any] = lambda d: (
        d.get("id") if isinstance(d, dict) else getattr(d, "id", None)
    )
    parent_id_accessor: Callable[[Any], Any] = lambda d: (
        d.get("parentId") if isinstance(d, dict) else getattr(d, "parentId", None)
    )

    def stratifier(data: Iterable) -> Node:
        data = list(data)
        node_by_id: dict[Any, Node] = {}
        nodes: list[Node] = []
        root: Node | None = None
        for d in data:
            node = Node(d)
            nid = id_accessor(d)
            if nid is not None:
                node_by_id[str(nid).strip()] = node
            nodes.append(node)
        for node in nodes:
            pid = parent_id_accessor(node.data)
            if pid is None or str(pid).strip() == "":
                if root is not None:
                    raise ValueError("stratify: multiple roots")
                root = node
            else:
                parent = node_by_id.get(str(pid).strip())
                if parent is None:
                    raise ValueError(f"stratify: missing parent {pid!r}")
                if parent.children is None:
                    parent.children = []
                parent.children.append(node)
                node.parent = parent
        if root is None:
            raise ValueError("stratify: no root")

        def set_depth(n: Node, *_a):
            n.depth = (n.parent.depth + 1) if n.parent else 0

        root.eachBefore(set_depth)

        def set_height(n: Node, *_a):
            n.height = (max(c.height for c in n.children) + 1) if n.children else 0

        root.eachAfter(set_height)
        return root

    def id_fn(fn=None):
        nonlocal id_accessor
        if fn is None:
            return id_accessor
        id_accessor = fn
        return stratifier

    def parent_id_fn(fn=None):
        nonlocal parent_id_accessor
        if fn is None:
            return parent_id_accessor
        parent_id_accessor = fn
        return stratifier

    stratifier.id = id_fn
    stratifier.parentId = parent_id_fn
    return stratifier


# -- tree / cluster (Reingold-Tilford / Buchheim et al.) ---------

# -- tree / cluster (tidy tree) ----------------------------------

def _tidy_layout(is_tree: bool):
    separation: Callable = lambda a, b: 1 if a.parent is b.parent else 2
    dx = 1.0
    dy = 1.0
    node_size = None

    def layout(root):
        x_counter = [-1.0]
        prev_leaf = [None]

        def assign(node):
            if node.children:
                for c in node.children:
                    assign(c)
                node.x = sum(c.x for c in node.children) / len(node.children)
            else:
                if prev_leaf[0] is not None:
                    x_counter[0] += separation(node, prev_leaf[0])
                else:
                    x_counter[0] += 1
                node.x = x_counter[0]
                prev_leaf[0] = node

        assign(root)

        # resolve subtree overlaps with a left-to-right contour sweep
        if is_tree:
            _resolve_overlaps(root, separation)
            # re-center parents over their (possibly shifted) children
            def recenter(node):
                if node.children:
                    for c in node.children:
                        recenter(c)
                    node.x = (node.children[0].x + node.children[-1].x) / 2
            recenter(root)

        nodes = root.descendants()
        left = min(n.x for n in nodes)
        right = max(n.x for n in nodes)
        max_depth = max(n.depth for n in nodes) or 1
        max_leaf_depth = max(
            (n.depth for n in nodes if not n.children), default=max_depth
        )
        span = right - left or 1
        for n in nodes:
            if node_size:
                n.x = (n.x - left) * node_size[0]
                n.y = n.depth * node_size[1]
            else:
                n.x = (n.x - left) / span * dx
                depth = n.depth if is_tree else max_leaf_depth if not n.children else n.depth
                n.y = (depth / max_leaf_depth) * dy
        return root

    def size_fn(value=None):
        nonlocal dx, dy, node_size
        if value is None:
            return None if node_size else [dx, dy]
        node_size = None
        dx, dy = float(value[0]), float(value[1])
        return layout

    def node_size_fn(value=None):
        nonlocal node_size
        if value is None:
            return list(node_size) if node_size else None
        node_size = (float(value[0]), float(value[1]))
        return layout

    def separation_fn(fn=None):
        nonlocal separation
        if fn is None:
            return separation
        separation = fn
        return layout

    layout.size = size_fn
    layout.nodeSize = node_size_fn
    layout.separation = separation_fn
    return layout


def _left_contour(node, depth, acc):
    acc.setdefault(depth, node.x)
    acc[depth] = min(acc[depth], node.x)
    for c in (node.children or []):
        _left_contour(c, depth + 1, acc)


def _right_contour(node, depth, acc):
    acc.setdefault(depth, node.x)
    acc[depth] = max(acc[depth], node.x)
    for c in (node.children or []):
        _right_contour(c, depth + 1, acc)


def _shift(node, dx):
    node.x += dx
    for c in (node.children or []):
        _shift(c, dx)


def _resolve_overlaps(node, separation):
    children = node.children or []
    for c in children:
        _resolve_overlaps(c, separation)
    for i in range(1, len(children)):
        left = {}
        right = {}
        for j in range(i):
            _right_contour(children[j], 0, right)
        _left_contour(children[i], 0, left)
        min_gap = None
        for d in left:
            if d in right:
                gap = left[d] - right[d]
                min_gap = gap if min_gap is None else min(min_gap, gap)
        need = separation(children[i], children[i - 1])
        if min_gap is not None and min_gap < need:
            _shift(children[i], need - min_gap)


def tree():
    return _tidy_layout(True)


def cluster():
    separation: Callable = lambda a, b: 1 if a.parent is b.parent else 2
    dx = 1.0
    dy = 1.0
    node_size: tuple | None = None

    def layout(root: Node) -> Node:
        previous: Node | None = None
        x = [0.0]

        def visit_leaf_or_internal(node: Node, *_a):
            nonlocal previous
            if node.children:
                node.x = sum(c.x for c in node.children) / len(node.children)
                node.y = 1 + max(c.y for c in node.children)
            else:
                if previous is not None:
                    x[0] += separation(node, previous)
                node.x = x[0]
                node.y = 0.0
                previous = node

        root.eachAfter(visit_leaf_or_internal)

        left = min(n.x for n in root.descendants())
        right = max(n.x for n in root.descendants())
        top = min(n.y for n in root.descendants())
        bottom = max(n.y for n in root.descendants())
        kx = dx / (right - left) if right != left else 1
        ky = dy / (bottom - top) if bottom != top else 1
        for n in root.descendants():
            if node_size:
                n.x = (n.x - left) * node_size[0]
                n.y = (bottom - n.y) * node_size[1]
            else:
                n.x = (n.x - left) * kx
                n.y = dy - (n.y - top) * ky
        return root

    def size_fn(value=None):
        nonlocal dx, dy, node_size
        if value is None:
            return None if node_size else [dx, dy]
        node_size = None
        dx, dy = float(value[0]), float(value[1])
        return layout

    def node_size_fn(value=None):
        nonlocal node_size
        if value is None:
            return list(node_size) if node_size else None
        node_size = (float(value[0]), float(value[1]))
        return layout

    def separation_fn(fn=None):
        nonlocal separation
        if fn is None:
            return separation
        separation = fn
        return layout

    layout.size = size_fn
    layout.nodeSize = node_size_fn
    layout.separation = separation_fn
    return layout


# -- partition -------------------------------------------------

def partition():
    dx = 1.0
    dy = 1.0
    padding = 0.0
    round_ = False

    def layout(root: Node) -> Node:
        n = root.height + 1
        root.x0 = padding
        root.y0 = 0.0
        root.x1 = dx
        root.y1 = dy / n if n else dy

        def position_node(node: Node):
            if node.children:
                _dice(node, node.x0, dy * (node.depth + 1) / n, node.x1,
                      dy * (node.depth + 2) / n)

        root.eachBefore(lambda node, *_: position_node(node))
        if round_:
            root.eachBefore(_round_node)
        return root

    def _dice(parent: Node, x0, y0, x1, y1):
        nodes = parent.children or []
        k = (x1 - x0) / (parent.value or 1) if parent.value else 0
        x = x0
        for node in nodes:
            node.y0 = y0
            node.y1 = y1
            node.x0 = x
            x += (node.value or 0) * k
            node.x1 = x

    def size_fn(value=None):
        nonlocal dx, dy
        if value is None:
            return [dx, dy]
        dx, dy = float(value[0]), float(value[1])
        return layout

    def padding_fn(value=None):
        nonlocal padding
        if value is None:
            return padding
        padding = float(value)
        return layout

    def round_fn(value=None):
        nonlocal round_
        if value is None:
            return round_
        round_ = bool(value)
        return layout

    layout.size = size_fn
    layout.padding = padding_fn
    layout.round = round_fn
    return layout


def _round_node(node: Node, *_a) -> None:
    node.x0 = round(node.x0)
    node.y0 = round(node.y0)
    node.x1 = round(node.x1)
    node.y1 = round(node.y1)


# -- treemap --------------------------------------------------

def treemapDice(parent: Node, x0, y0, x1, y1) -> None:
    nodes = parent.children or []
    total = parent.value or 0
    k = (x1 - x0) / total if total else 0
    x = x0
    for node in nodes:
        node.y0, node.y1 = y0, y1
        node.x0 = x
        x += (node.value or 0) * k
        node.x1 = x


def treemapSlice(parent: Node, x0, y0, x1, y1) -> None:
    nodes = parent.children or []
    total = parent.value or 0
    k = (y1 - y0) / total if total else 0
    y = y0
    for node in nodes:
        node.x0, node.x1 = x0, x1
        node.y0 = y
        y += (node.value or 0) * k
        node.y1 = y


def treemapSliceDice(parent: Node, x0, y0, x1, y1) -> None:
    (treemapSlice if parent.depth & 1 else treemapDice)(parent, x0, y0, x1, y1)


_PHI = (1 + math.sqrt(5)) / 2


def _worst(areas: list[float], side: float) -> float:
    """Worst (largest) aspect ratio of a row of *areas* laid along *side*."""
    if not areas or side <= 0:
        return math.inf
    s = sum(areas)
    if s <= 0:
        return math.inf
    mx = max(areas)
    mn = min(areas)
    return max((side * side * mx) / (s * s), (s * s) / (side * side * mn))


def treemapSquarify(parent: Node, x0, y0, x1, y1) -> None:
    """Squarified treemap tiling (Bruls, Huizing & van Wijk)."""
    nodes = list(parent.children or [])
    if not nodes:
        return
    total_value = sum(n.value or 0 for n in nodes) or 1
    scale = ((x1 - x0) * (y1 - y0)) / total_value
    areas = [(n.value or 0) * scale for n in nodes]
    remaining = list(zip(nodes, areas))
    while remaining:
        dx, dy = x1 - x0, y1 - y0
        side = min(dx, dy)
        row: list = []
        while remaining:
            candidate = [a for _, a in row] + [remaining[0][1]]
            current = [a for _, a in row]
            if row and _worst(candidate, side) > _worst(current, side):
                break
            row.append(remaining.pop(0))
        row_area = sum(a for _, a in row)
        thickness = row_area / side if side else 0
        if dx >= dy:  # lay the row as a vertical column, filling height
            y = y0
            k = (y1 - y0) / row_area if row_area else 0
            for node, area in row:
                node.x0, node.x1 = x0, x0 + thickness
                node.y0 = y
                y += area * k
                node.y1 = y
            x0 += thickness
        else:  # lay the row as a horizontal strip, filling width
            x = x0
            k = (x1 - x0) / row_area if row_area else 0
            for node, area in row:
                node.y0, node.y1 = y0, y0 + thickness
                node.x0 = x
                x += area * k
                node.x1 = x
            y0 += thickness


treemapResquarify = treemapSquarify


def treemapBinary(parent: Node, x0, y0, x1, y1) -> None:
    nodes = parent.children or []
    if not nodes:
        return
    total = sum(n.value or 0 for n in nodes)

    def partition(i, j, value, cx0, cy0, cx1, cy1):
        if i >= j - 1:
            node = nodes[i]
            node.x0, node.y0, node.x1, node.y1 = cx0, cy0, cx1, cy1
            return
        k = i
        acc = 0.0
        half = value / 2
        while k < j - 1 and acc + (nodes[k].value or 0) < half:
            acc += nodes[k].value or 0
            k += 1
        if k <= i:
            k = i + 1
            acc = nodes[i].value or 0
        left_value = acc
        right_value = value - acc
        if (cx1 - cx0) > (cy1 - cy0):
            xm = cx0 + (cx1 - cx0) * left_value / value if value else cx0
            partition(i, k, left_value, cx0, cy0, xm, cy1)
            partition(k, j, right_value, xm, cy0, cx1, cy1)
        else:
            ym = cy0 + (cy1 - cy0) * left_value / value if value else cy0
            partition(i, k, left_value, cx0, cy0, cx1, ym)
            partition(k, j, right_value, cx0, ym, cx1, cy1)

    partition(0, len(nodes), total, x0, y0, x1, y1)


def treemap():
    tile = treemapSquarify
    dx = 1.0
    dy = 1.0
    round_ = False
    padding_inner: Callable = lambda d: 0
    padding_top: Callable = lambda d: 0
    padding_right: Callable = lambda d: 0
    padding_bottom: Callable = lambda d: 0
    padding_left: Callable = lambda d: 0

    def layout(root: Node) -> Node:
        root.x0 = 0.0
        root.y0 = 0.0
        root.x1 = dx
        root.y1 = dy
        root.eachBefore(_position)
        if round_:
            root.eachBefore(_round_node)
        return root

    def _position(node: Node, *_a):
        if not node.children:
            return
        pt = padding_top(node)
        pr = padding_right(node)
        pb = padding_bottom(node)
        pl = padding_left(node)
        pi = padding_inner(node) / 2
        x0 = node.x0 + pl
        y0 = node.y0 + pt
        x1 = node.x1 - pr
        y1 = node.y1 - pb
        if x1 < x0:
            x0 = x1 = (x0 + x1) / 2
        if y1 < y0:
            y0 = y1 = (y0 + y1) / 2
        tile(node, x0 + pi, y0 + pi, x1 - pi, y1 - pi)

    def tile_fn(fn=None):
        nonlocal tile
        if fn is None:
            return tile
        tile = fn
        return layout

    def size_fn(value=None):
        nonlocal dx, dy
        if value is None:
            return [dx, dy]
        dx, dy = float(value[0]), float(value[1])
        return layout

    def round_fn(value=None):
        nonlocal round_
        if value is None:
            return round_
        round_ = bool(value)
        return layout

    def _pad_setter(name):
        def setter(value=None):
            nonlocal padding_inner, padding_top, padding_right, padding_bottom, padding_left
            fn = value if callable(value) else (lambda d: float(value))
            if name in ("inner", "all"):
                padding_inner = fn
            if name in ("top", "all", "outer"):
                padding_top = fn
            if name in ("right", "all", "outer"):
                padding_right = fn
            if name in ("bottom", "all", "outer"):
                padding_bottom = fn
            if name in ("left", "all", "outer"):
                padding_left = fn
            return layout

        return setter

    layout.tile = tile_fn
    layout.size = size_fn
    layout.round = round_fn
    layout.padding = _pad_setter("all")
    layout.paddingInner = _pad_setter("inner")
    layout.paddingOuter = _pad_setter("outer")
    layout.paddingTop = _pad_setter("top")
    layout.paddingRight = _pad_setter("right")
    layout.paddingBottom = _pad_setter("bottom")
    layout.paddingLeft = _pad_setter("left")
    return layout


# -- pack -----------------------------------------------------

def _place(b, a, c):
    dx = b["x"] - a["x"]
    dy = b["y"] - a["y"]
    d2 = dx * dx + dy * dy
    if d2:
        a2 = (a["r"] + c["r"]) ** 2
        b2 = (b["r"] + c["r"]) ** 2
        if a2 > b2:
            x = (d2 + b2 - a2) / (2 * d2)
            y = math.sqrt(max(0, b2 / d2 - x * x))
            c["x"] = b["x"] - x * dx - y * dy
            c["y"] = b["y"] - x * dy + y * dx
        else:
            x = (d2 + a2 - b2) / (2 * d2)
            y = math.sqrt(max(0, a2 / d2 - x * x))
            c["x"] = a["x"] + x * dx - y * dy
            c["y"] = a["y"] + x * dy + y * dx
    else:
        c["x"] = a["x"] + c["r"]
        c["y"] = a["y"]


def _intersects(a, b):
    dr = a["r"] + b["r"] - 1e-6
    dx = b["x"] - a["x"]
    dy = b["y"] - a["y"]
    return dr > 0 and dr * dr > dx * dx + dy * dy


def packSiblings(circles: list) -> list:
    circ = [
        {"x": 0.0, "y": 0.0, "r": float(c["r"] if isinstance(c, dict) else c.r),
         "_": c}
        for c in circles
    ]
    if not circ:
        return []
    n = len(circ)
    a = circ[0]
    a["x"], a["y"] = a["r"], 0.0
    if n == 1:
        _write_back(circles, circ)
        return circles
    b = circ[1]
    b["x"], b["y"] = -b["r"], 0.0
    if n == 2:
        _write_back(circles, circ)
        return circles
    c = circ[2]
    _place(b, a, c)

    # simplified front-chain packing
    chain = [a, b, c]
    for i in range(3, n):
        cc = circ[i]
        # try placing against the last two in the chain, then find non-overlapping
        _place(chain[-1], chain[-2], cc)
        j = 0
        collided = None
        while j < len(chain):
            if _intersects(chain[j], cc):
                collided = chain[j]
                break
            j += 1
        if collided is not None:
            _place(collided, chain[-1], cc)
        chain.append(cc)

    _write_back(circles, circ)
    return circles


def _write_back(circles, circ):
    for src, cc in zip(circles, circ):
        if isinstance(src, dict):
            src["x"], src["y"] = cc["x"], cc["y"]
        else:
            src.x, src.y = cc["x"], cc["y"]


def packEnclose(circles: list) -> dict:
    pts = [
        {"x": (c["x"] if isinstance(c, dict) else c.x),
         "y": (c["y"] if isinstance(c, dict) else c.y),
         "r": (c["r"] if isinstance(c, dict) else c.r)}
        for c in circles
    ]
    if not pts:
        return {"x": 0.0, "y": 0.0, "r": 0.0}
    # crude bounding enclosure: centroid + max distance
    cx = sum(p["x"] for p in pts) / len(pts)
    cy = sum(p["y"] for p in pts) / len(pts)
    r = max(math.hypot(p["x"] - cx, p["y"] - cy) + p["r"] for p in pts)
    return {"x": cx, "y": cy, "r": r}


def pack():
    radius: Callable | None = None
    dx = 1.0
    dy = 1.0
    padding: Callable = lambda d: 0

    def layout(root: Node) -> Node:
        root.x = dx / 2
        root.y = dy / 2
        if radius is not None:
            root.eachBefore(lambda n, *_: setattr(n, "r", radius(n)))
        else:
            root.eachBefore(_radius_leaf)
            root.eachAfter(_radius_parent)
        root.eachBefore(_translate_child)
        s = min(dx, dy) / (2 * root.r) if root.r else 1
        root.eachBefore(lambda n, *_: _scale_node(n, root, s))
        return root

    def _radius_leaf(node: Node, *_a):
        if not node.children:
            node.r = math.sqrt((node.value or 0))

    def _radius_parent(node: Node, *_a):
        if node.children:
            packSiblings(node.children)
            enc = packEnclose(node.children)
            node.r = enc["r"] + padding(node)
            node._pack_center = (enc["x"], enc["y"])

    def _translate_child(node: Node, *_a):
        if node.parent is not None:
            ecx, ecy = getattr(node.parent, "_pack_center", (0.0, 0.0))
            node.x = node.parent.x + (node.x - ecx)
            node.y = node.parent.y + (node.y - ecy)

    def _scale_node(node: Node, root: Node, s: float):
        node.x = root.x + (node.x - root.x) * s
        node.y = root.y + (node.y - root.y) * s
        node.r *= s

    def radius_fn(fn=None):
        nonlocal radius
        if fn is None:
            return radius
        radius = fn
        return layout

    def size_fn(value=None):
        nonlocal dx, dy
        if value is None:
            return [dx, dy]
        dx, dy = float(value[0]), float(value[1])
        return layout

    def padding_fn(value=None):
        nonlocal padding
        if value is None:
            return padding
        padding = value if callable(value) else (lambda d: float(value))
        return layout

    layout.radius = radius_fn
    layout.size = size_fn
    layout.padding = padding_fn
    return layout
