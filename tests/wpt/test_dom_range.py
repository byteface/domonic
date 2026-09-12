"""Ported from wpt/dom/ranges/Range-attributes.html, Range-collapse.html,
Range-comparePoint.html, Range-isPointInRange.html, Range-selectNode.html,
Range-commonAncestorContainer(-2).html, Range-intersectsNode-2.html,
Range-cloneRange.html and Range-stringifier.html, plus hand-derived tests for
compareBoundaryPoints, insertNode and surroundContents.
https://dom.spec.whatwg.org/#interface-range

Most of dom/ranges/ (cloneContents, deleteContents, extractContents,
insertNode, surroundContents, compareBoundaryPoints, cloneRange, set) is
driven by a large, generative, iframe-based shared harness
(dom/common.js + Range-mutations.js: a combinatorial matrix of "test ranges"
run through a reference JS implementation of each algorithm, diffed against
the real one) rather than individual test() blocks -- not something this
project's line-for-line port style can transcribe. Past the files listed
above, this file hand-tests the same spec behaviour directly against small
trees, which is how it found the bugs below.

Known, deliberate gaps (not fixed in this pass):

- Live range mutation tracking (https://dom.spec.whatwg.org/#concept-live-range,
  "Range-mutations-*.html" upstream): a Range's boundary points do not move
  when the tree around them is edited elsewhere (insertBefore, removeChild,
  splitText, CharacterData edits, normalize()). Implementing this needs a
  per-document live-range registry and adjustment hooks on every one of
  those mutation paths -- a real feature, not a bug fix, and not attempted
  here.
- cloneContents/extractContents only correctly trim a boundary that sits
  directly in the common ancestor's own children, or in a single shared
  Text/element container. When a boundary is nested inside a partially
  selected element (e.g. start at (textInsideP, 2) with P only partially in
  the range), the spec clones just the selected portion of P; domonic
  currently includes (or excises) all of P. Tracked as xfail below.
- surroundContents() does not implement the spec's validity checks (throws
  InvalidStateError if the range partially selects a non-Text node,
  InvalidNodeTypeError for a Document/DocumentType/DocumentFragment
  newParent); it just extracts and re-inserts unconditionally.
"""

import unittest

import pytest

from domonic.dom import DOMException, Document, Range

document = Document()


def _tree():
    root = document.createElement("root")
    document.appendChild(root)
    kids = [document.createElement(name) for name in ("a", "b", "c")]
    for kid in kids:
        root.appendChild(kid)
    return root, kids


class RangeAttributes(unittest.TestCase):
    def test_fresh_range_is_anchored_at_the_document(self):
        r = document.createRange()
        self.assertIs(r.startContainer, document)
        self.assertIs(r.endContainer, document)
        self.assertEqual(r.startOffset, 0)
        self.assertEqual(r.endOffset, 0)
        self.assertTrue(r.collapsed)

    def test_detach_is_a_noop(self):
        r = document.createRange()
        r.detach()
        self.assertIs(r.startContainer, document)
        self.assertIs(r.endContainer, document)
        self.assertEqual((r.startOffset, r.endOffset), (0, 0))
        self.assertTrue(r.collapsed)


class RangeCollapse(unittest.TestCase):
    def test_collapsed_reflects_equal_boundary_points(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 1)
        r.setEnd(root, 2)
        self.assertFalse(r.collapsed)

        r.collapse(True)
        self.assertTrue(r.collapsed)
        self.assertIs(r.endContainer, root)
        self.assertEqual(r.endOffset, 1)

    def test_collapse_to_end(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 0)
        r.setEnd(root, 3)
        r.collapse(False)
        self.assertTrue(r.collapsed)
        self.assertEqual(r.startOffset, 3)


class RangeComparePoint(unittest.TestCase):
    def test_relative_to_boundary_points(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 1)
        r.setEnd(root, 2)
        self.assertEqual(r.comparePoint(root, 0), -1)
        self.assertEqual(r.comparePoint(root, 1), 0)
        self.assertEqual(r.comparePoint(root, 2), 0)
        self.assertEqual(r.comparePoint(root, 3), 1)

    def test_point_in_a_different_tree_throws_wrong_document_error(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 0)
        r.setEnd(root, 1)
        stranger = document.createElement("stranger")
        with self.assertRaises(DOMException) as ctx:
            r.comparePoint(stranger, 0)
        self.assertEqual(ctx.exception.name, "WrongDocumentError")

    def test_offset_past_the_end_throws(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 0)
        r.setEnd(root, 1)
        with self.assertRaises(Exception):
            r.comparePoint(root, 99)


class RangeIsPointInRange(unittest.TestCase):
    def test_true_only_between_the_boundary_points(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 1)
        r.setEnd(root, 2)
        self.assertFalse(r.isPointInRange(root, 0))
        self.assertTrue(r.isPointInRange(root, 1))
        self.assertFalse(r.isPointInRange(root, 3))

    def test_point_in_a_different_tree_is_false_not_an_error(self):
        root, _kids = _tree()
        r = document.createRange()
        r.setStart(root, 0)
        r.setEnd(root, 1)
        stranger = document.createElement("stranger")
        self.assertFalse(r.isPointInRange(stranger, 0))


class RangeSelectNode(unittest.TestCase):
    def test_select_node_wraps_the_node(self):
        root, kids = _tree()
        r = document.createRange()
        r.selectNode(kids[1])
        self.assertIs(r.startContainer, root)
        self.assertEqual(r.startOffset, 1)
        self.assertEqual(r.endOffset, 2)
        self.assertIs(r.commonAncestorContainer, root)

    def test_select_node_contents_spans_the_children(self):
        root, kids = _tree()
        kids[0].appendChild(document.createElement("grandchild"))
        r = document.createRange()
        r.selectNodeContents(kids[0])
        self.assertIs(r.startContainer, kids[0])
        self.assertEqual(r.startOffset, 0)
        self.assertEqual(r.endOffset, 1)


class RangeCommonAncestorContainer(unittest.TestCase):
    def test_detached_range_is_the_document(self):
        r = document.createRange()
        r.detach()  # a documented no-op
        self.assertIs(r.commonAncestorContainer, document)

    def test_across_fragment_children_and_within_one(self):
        df = document.createDocumentFragment()
        foo = df.appendChild(document.createElement("foo"))
        foo.appendChild(document.createTextNode("Foo"))
        bar = df.appendChild(document.createElement("bar"))
        bar.appendChild(document.createComment("Bar"))

        cases = [
            (foo, 0, bar, 0, df),
            (foo, 0, foo.firstChild, 3, foo),
            (foo.firstChild, 0, bar, 0, df),
            (foo.firstChild, 3, bar.firstChild, 2, df),
        ]
        for start_node, start_offset, end_node, end_offset, expected in cases:
            with self.subTest(start=start_node, end=end_node):
                r = document.createRange()
                r.setStart(start_node, start_offset)
                r.setEnd(end_node, end_offset)
                self.assertIs(r.commonAncestorContainer, expected)


class RangeCompareBoundaryPoints(unittest.TestCase):
    def test_all_four_modes(self):
        div = document.createElement("div")
        a = document.createTextNode("aaaa")
        b = document.createTextNode("bbbb")
        div.appendChild(a)
        div.appendChild(b)

        earlier = document.createRange()
        earlier.setStart(a, 1)
        earlier.setEnd(a, 3)
        later = document.createRange()
        later.setStart(b, 1)
        later.setEnd(b, 3)

        self.assertEqual(earlier.compareBoundaryPoints(Range.START_TO_START, later), -1)
        self.assertEqual(earlier.compareBoundaryPoints(Range.END_TO_END, later), -1)
        self.assertEqual(earlier.compareBoundaryPoints(Range.START_TO_END, later), -1)
        self.assertEqual(earlier.compareBoundaryPoints(Range.END_TO_START, later), -1)
        self.assertEqual(later.compareBoundaryPoints(Range.START_TO_START, earlier), 1)

    def test_ancestor_and_descendant_boundary_points(self):
        # A regression check for _compare_points: comparing a point in an
        # ancestor element against a point inside one of its descendants
        # used to be handled as if they were unrelated siblings, giving
        # wrong answers for one of the most common range shapes there is.
        div = document.createElement("div")
        p = document.createElement("p")
        text = document.createTextNode("hi")
        p.appendChild(text)
        div.appendChild(p)

        before_p = document.createRange()
        before_p.setStart(div, 0)
        before_p.setEnd(div, 0)
        self.assertEqual(before_p.comparePoint(text, 0), 1)  # (div,0) is before (text,0)

        after_p = document.createRange()
        after_p.setStart(div, 1)
        after_p.setEnd(div, 1)
        self.assertEqual(after_p.comparePoint(text, 0), -1)  # (div,1) is after (text,0)


class RangeIntersectsNode(unittest.TestCase):
    def test_simple_cases(self):
        div = document.createElement("div")
        s0 = document.createElement("span")
        s0.appendChild(document.createTextNode("s0"))
        s1 = document.createElement("span")
        s1.appendChild(document.createTextNode("s1"))
        s2 = document.createElement("span")
        s2.appendChild(document.createTextNode("s2"))
        for s in (s0, s1, s2):
            div.appendChild(s)

        r = document.createRange()
        r.setStart(div, 0)
        r.setEnd(div, 1)
        self.assertEqual([r.intersectsNode(s) for s in (s0, s1, s2)], [True, False, False])

        r.setStart(div, 1)
        r.setEnd(div, 2)
        self.assertEqual([r.intersectsNode(s) for s in (s0, s1, s2)], [False, True, False])

        r.setStart(div, 2)
        r.setEnd(div, 3)
        self.assertEqual([r.intersectsNode(s) for s in (s0, s1, s2)], [False, False, True])


class RangeCloneRange(unittest.TestCase):
    def test_clone_is_independent(self):
        text = document.createTextNode("testing")
        r = document.createRange()
        r.setStart(text, 1)
        r.setEnd(text, 2)

        clone = r.cloneRange()
        self.assertIs(clone.startContainer, r.startContainer)
        self.assertEqual(clone.startOffset, r.startOffset)

        other = document.createTextNode("testing with different length")
        r.setStart(other, 3)
        self.assertIs(clone.startContainer, text)  # unaffected by mutating the original
        self.assertEqual(clone.startOffset, 1)

        clone.setStart(other, 4)
        self.assertIs(r.startContainer, other)  # unaffected by mutating the clone
        self.assertEqual(r.startOffset, 3)


class RangeStringifier(unittest.TestCase):
    """https://dom.spec.whatwg.org/#dom-range-stringifier -- concatenates
    Text node data only, never markup, and (domonic-specific) treats a raw
    string child the same as a Text node."""

    def test_single_text_node_with_offsets(self):
        text = document.createTextNode("Test div")
        r = document.createRange()
        r.setStart(text, 5)
        r.setEnd(text, 7)
        self.assertEqual(r.toString(), "di")

    def test_spans_element_children_real_text_nodes(self):
        div = document.createElement("div")
        p1 = document.createElement("p")
        p1.appendChild(document.createTextNode("hi"))
        p2 = document.createElement("p")
        p2.appendChild(document.createTextNode("bye"))
        div.appendChild(p1)
        div.appendChild(p2)

        r = document.createRange()
        r.setStart(div, 0)
        r.setEnd(div, 2)
        self.assertEqual(r.toString(), "hibye")  # not "<p>hi</p><p>bye</p>"

    def test_spans_element_children_raw_string_children(self):
        # domonic's `span("a")`-style shorthand stores "a" as a plain string,
        # not a Text node -- the stringifier must still see it as text.
        from domonic.html import div, span

        container = div(span("a"), span("b"), span("c"))
        r = Range()
        r.setStart(container, 1)
        r.setEnd(container, 3)
        self.assertEqual(r.toString(), "bc")

    def test_partial_text_at_each_end_across_siblings(self):
        p1 = document.createElement("p")
        p1.appendChild(document.createTextNode("hi"))
        p2 = document.createElement("p")
        p2.appendChild(document.createTextNode("bye"))
        div = document.createElement("div")
        div.appendChild(p1)
        div.appendChild(p2)

        r = document.createRange()
        r.setStart(p1.firstChild, 1)
        r.setEnd(p2.firstChild, 2)
        self.assertEqual(r.toString(), "iby")

    def test_comment_contributes_no_text(self):
        div = document.createElement("div")
        div.appendChild(document.createTextNode("a"))
        div.appendChild(document.createComment("ignored"))
        div.appendChild(document.createTextNode("b"))

        r = document.createRange()
        r.selectNodeContents(div)
        self.assertEqual(r.toString(), "ab")


class RangeContentMethods(unittest.TestCase):
    """cloneContents / deleteContents / extractContents / insertNode /
    surroundContents, for the shapes they already get right: same-container
    slices and whole spanned children."""

    def test_clone_contents_same_text_node(self):
        text = document.createTextNode("abcdef")
        r = document.createRange()
        r.setStart(text, 1)
        r.setEnd(text, 4)
        self.assertEqual(str(r.cloneContents()), "bcd")
        self.assertEqual(text.data, "abcdef")  # cloning doesn't touch the source

    def test_extract_contents_same_text_node(self):
        text = document.createTextNode("abcdef")
        r = document.createRange()
        r.setStart(text, 1)
        r.setEnd(text, 4)
        self.assertEqual(str(r.extractContents()), "bcd")
        self.assertEqual(text.data, "aef")

    def test_clone_and_extract_whole_element_children(self):
        div = document.createElement("div")
        for letter in "abc":
            span = document.createElement("span")
            span.appendChild(document.createTextNode(letter))
            div.appendChild(span)

        r = document.createRange()
        r.setStart(div, 1)
        r.setEnd(div, 3)
        self.assertEqual(str(r.cloneContents()), "<span>b</span><span>c</span>")
        self.assertEqual(len(div.childNodes), 3)  # cloning doesn't touch the source

        self.assertEqual(str(r.extractContents()), "<span>b</span><span>c</span>")
        self.assertEqual(str(div), "<div><span>a</span></div>")

    def test_insert_node_splits_the_start_text_node(self):
        div = document.createElement("div")
        div.appendChild(document.createTextNode("hello"))
        r = document.createRange()
        r.setStart(div.firstChild, 2)
        r.setEnd(div.firstChild, 2)
        marker = document.createElement("b")
        marker.appendChild(document.createTextNode("X"))
        r.insertNode(marker)
        self.assertEqual(str(div), "<div>he<b>X</b>llo</div>")

    def test_surround_contents_wraps_the_selected_text(self):
        div = document.createElement("div")
        div.appendChild(document.createTextNode("hello world"))
        r = document.createRange()
        r.setStart(div.firstChild, 0)
        r.setEnd(div.firstChild, 5)
        r.surroundContents(document.createElement("b"))
        self.assertEqual(str(div), "<div><b>hello</b> world</div>")


class RangeKnownDeviations(unittest.TestCase):
    @pytest.mark.xfail(
        reason="cloneContents/extractContents only trim a boundary that sits directly in the common "
        "ancestor's own children or a single shared container; a boundary nested inside a partially "
        "selected element (e.g. offset 2 into a Text node under a <p> that is only partially in the "
        "range) is not split -- the whole <p> is included instead of just its selected text",
        strict=True,
    )
    def test_clone_contents_trims_partially_selected_nested_elements(self):
        div = document.createElement("div")
        p1 = document.createElement("p")
        p1.appendChild(document.createTextNode("hello"))
        p2 = document.createElement("p")
        p2.appendChild(document.createTextNode("world"))
        div.appendChild(p1)
        div.appendChild(p2)

        r = document.createRange()
        r.setStart(p1.firstChild, 2)
        r.setEnd(p2.firstChild, 3)
        self.assertEqual(str(r.cloneContents()), "<p>llo</p><p>wor</p>")

    @pytest.mark.xfail(
        reason="surroundContents() does not implement the spec's validity checks -- it never raises "
        "InvalidStateError for a range that partially selects a non-Text node, nor InvalidNodeTypeError "
        "for a Document/DocumentType/DocumentFragment newParent",
        strict=True,
    )
    def test_surround_contents_rejects_partially_selected_element(self):
        div = document.createElement("div")
        p1 = document.createElement("p")
        p1.appendChild(document.createTextNode("hello"))
        p2 = document.createElement("p")
        p2.appendChild(document.createTextNode("world"))
        div.appendChild(p1)
        div.appendChild(p2)

        r = document.createRange()
        r.setStart(p1.firstChild, 2)  # partially selects p1
        r.setEnd(p2.firstChild, 3)
        with self.assertRaises(DOMException):
            r.surroundContents(document.createElement("b"))


if __name__ == "__main__":
    unittest.main()
