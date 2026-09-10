"""Ported from wpt/dom/nodes/Text-wholeText.html and Text-splitText.html
https://dom.spec.whatwg.org/#dom-text-wholetext

domonic's ``splitText`` raises a plain ``IndexError`` (not
``DOMException("IndexSizeError")``) for an out-of-range offset -- an
established deviation shared by all the ``CharacterData`` range methods -- so
that row is checked with ``IndexError``.
"""

import unittest

from domonic.dom import Document
from tests.wpt._harness import assert_equals

document = Document()


class TextWholeText(unittest.TestCase):
    def test_returns_text_of_all_logically_adjacent_text_nodes_in_document_order(self):
        parent = document.createElement("div")
        t1 = document.createTextNode("a")
        t2 = document.createTextNode("b")
        t3 = document.createTextNode("c")

        assert_equals(t1.wholeText, t1.textContent)

        parent.appendChild(t1)
        assert_equals(t1.wholeText, t1.textContent)

        parent.appendChild(t2)
        assert_equals(t1.wholeText, "ab")
        assert_equals(t2.wholeText, "ab")

        parent.appendChild(t3)
        assert_equals(t1.wholeText, "abc")
        assert_equals(t3.wholeText, "abc")

        a = document.createElement("a")
        a.appendChild(document.createTextNode("anchor"))
        parent.insertBefore(a, t3)
        # a non-text node now separates {t1, t2} from t3
        assert_equals(t1.wholeText, "ab")
        assert_equals(t2.wholeText, "ab")
        assert_equals(t3.wholeText, "c")


class TextSplitText(unittest.TestCase):
    def test_split_after_end_of_data_raises(self):
        text = document.createTextNode("camembert")
        with self.assertRaises(IndexError):
            text.splitText(10)

    def test_split_empty_text(self):
        text = document.createTextNode("")
        new_text = text.splitText(0)
        assert_equals(text.data, "")
        assert_equals(new_text.data, "")

    def test_split_at_beginning(self):
        text = document.createTextNode("comte")
        new_text = text.splitText(0)
        assert_equals(text.data, "")
        assert_equals(new_text.data, "comte")

    def test_split_at_end(self):
        text = document.createTextNode("comte")
        new_text = text.splitText(5)
        assert_equals(text.data, "comte")
        assert_equals(new_text.data, "")

    def test_split_root_leaves_new_node_detached(self):
        text = document.createTextNode("comte")
        new_text = text.splitText(3)
        assert_equals(text.data, "com")
        assert_equals(new_text.data, "te")
        assert_equals(new_text.parentNode, None)

    def test_split_child_inserts_new_node_as_next_sibling(self):
        parent = document.createElement("div")
        text = document.createTextNode("bleu")
        parent.appendChild(text)
        new_text = text.splitText(2)
        assert_equals(text.data, "bl")
        assert_equals(new_text.data, "eu")
        assert_equals(text.nextSibling, new_text)
        assert_equals(new_text.parentNode, parent)


if __name__ == "__main__":
    unittest.main()
