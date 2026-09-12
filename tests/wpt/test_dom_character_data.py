"""Ported from wpt/dom/nodes/CharacterData-{data,appendData,deleteData,
insertData,replaceData,substringData,appendChild,remove}.html
https://dom.spec.whatwg.org/#interface-characterdata

Run against both ``Text`` and ``Comment`` -- the two real ``CharacterData``
subtypes upstream tests. domonic does not make ``Comment``,
``ProcessingInstruction`` and ``CDATASection`` actual ``CharacterData``
subclasses (they store their text on a plain ``self.data`` attribute rather
than ``Text``'s ``Node.args``-based storage), so they get the same methods
from a small shared mixin instead -- see ``_CharacterDataOnAttr`` in
``domonic/dom.py``.

Two known, deliberate gaps, both pre-existing conventions this port doesn't
relitigate (``Text-splitText.html`` already documents the first one):

- Range methods raise a plain ``IndexError`` for an out-of-range offset/count,
  not ``DOMException("IndexSizeError")``, so those rows are checked with
  ``IndexError``.
- Offsets/counts are not JS-``ToNumber``-coerced -- passing a numeric string
  (``"0"``) raises ``TypeError`` rather than being parsed, matching how
  domonic already treats every other offset/index argument in this file.

Not ported: ``CharacterData-surrogates.html``. ``.length`` and every offset
counts Python string codepoints, not UTF-16 code units -- they agree for BMP
text, but not for astral-plane characters (most emoji): "🌠".length is 1 here,
2 in a browser. Splitting/joining a surrogate pair is therefore out of scope.
"""

import unittest

from domonic.dom import Document
from tests.wpt._harness import assert_throws_dom

document = Document()

KINDS = ("Text", "Comment")


def _make(kind: str, data: str = "test"):
    return document.createTextNode(data) if kind == "Text" else document.createComment(data)


class CharacterDataData(unittest.TestCase):
    def test_initial_value(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.data, "test")
                self.assertEqual(node.length, 4)

    def test_data_none(self):
        # [LegacyNullToEmptyString]: JS `null` -> "" -- Python's None stands in
        # for null; there is no Python equivalent of JS's `undefined`.
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.data = None
                self.assertEqual(node.data, "")
                self.assertEqual(node.length, 0)

    def test_data_number(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.data = 0
                self.assertEqual(node.data, "0")
                self.assertEqual(node.length, 1)

    def test_data_empty_string(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.data = ""
                self.assertEqual(node.data, "")
                self.assertEqual(node.length, 0)

    def test_data_ascii(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.data = "--"
                self.assertEqual(node.data, "--")
                self.assertEqual(node.length, 2)

    def test_data_non_ascii(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.data = "資料"
                self.assertEqual(node.data, "資料")
                self.assertEqual(node.length, 2)


class CharacterDataAppendData(unittest.TestCase):
    def test_append(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.appendData("bar")
                self.assertEqual(node.data, "testbar")

    def test_append_empty(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.appendData("")
                self.assertEqual(node.data, "test")

    def test_append_non_ascii(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.appendData(", append more 資料，測試資料")
                self.assertEqual(node.data, "test, append more 資料，測試資料")
                self.assertEqual(node.length, 25)

    def test_append_none(self):
        # appendData's argument is a plain DOMString (no [LegacyNullToEmptyString]
        # like the .data attribute); domonic still treats None as "nothing"
        # rather than producing the JS-specific string "null".
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.appendData(None)
                self.assertEqual(node.data, "test")

    def test_append_requires_an_argument(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                with self.assertRaises(TypeError):
                    node.appendData()


class CharacterDataDeleteData(unittest.TestCase):
    def test_out_of_bounds(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                for args in ((5, 10), (5, 0), (-1, 10), (-1, 0)):
                    with self.assertRaises(IndexError):
                        node.deleteData(*args)

    def test_at_start(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.deleteData(0, 2), "st")

    def test_at_end(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.deleteData(2, 10), "te")

    def test_in_the_middle(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.deleteData(1, 1), "tst")

    def test_zero_count(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.deleteData(2, 0), "test")
                self.assertEqual(node.deleteData(0, 0), "test")

    def test_small_negative_count_wraps_to_the_rest_of_the_string(self):
        # count is a WebIDL `unsigned long`: a negative Python int wraps
        # modulo 2**32 (matching JS's ToUint32) instead of raising.
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.deleteData(2, -1), "te")

    def test_large_negative_count_wraps(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.deleteData(1, -0x100000000 + 2), "tt")

    def test_non_ascii_data(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind, "This is the character data test, append more 資料，更多測試資料")
                node.deleteData(40, 5)
                self.assertEqual(node.data, "This is the character data test, append 資料，更多測試資料")
                node.deleteData(45, 2)
                self.assertEqual(node.data, "This is the character data test, append 資料，更多資料")


class CharacterDataInsertData(unittest.TestCase):
    def test_out_of_bounds(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                with self.assertRaises(IndexError):
                    node.insertData(5, "x")
                with self.assertRaises(IndexError):
                    node.insertData(5, "")

    def test_negative_out_of_bounds(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                with self.assertRaises(IndexError):
                    node.insertData(-1, "x")
                with self.assertRaises(IndexError):
                    node.insertData(-0x100000000 + 5, "x")

    def test_negative_in_bounds_wraps(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.insertData(-0x100000000 + 2, "X")
                self.assertEqual(node.data, "teXst")

    def test_empty(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.insertData(0, "")
                self.assertEqual(node.data, "test")

    def test_at_the_start(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.insertData(0, "X")
                self.assertEqual(node.data, "Xtest")

    def test_in_the_middle(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.insertData(2, "X")
                self.assertEqual(node.data, "teXst")

    def test_at_the_end(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.insertData(4, "ing")
                self.assertEqual(node.data, "testing")

    def test_none(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.insertData(2, None)
                self.assertEqual(node.data, "test")


class CharacterDataReplaceData(unittest.TestCase):
    def test_invalid_offset(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                for args in ((5, 1, "x"), (5, 0, ""), (-1, 1, "x"), (-1, 0, "")):
                    with self.assertRaises(IndexError):
                        node.replaceData(*args)
                self.assertEqual(node.data, "test")

    def test_clamped_count(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.replaceData(2, 10, "yo")
                self.assertEqual(node.data, "teyo")

    def test_negative_count_wraps_and_clamps(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.replaceData(2, -1, "yo")
                self.assertEqual(node.data, "teyo")

    def test_before_the_start(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.replaceData(0, 0, "yo")
                self.assertEqual(node.data, "yotest")

    def test_at_the_start_shorter(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.replaceData(0, 2, "y")
                self.assertEqual(node.data, "yst")

    def test_at_the_start_equal_length(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.replaceData(0, 2, "yo")
                self.assertEqual(node.data, "yost")

    def test_at_the_start_longer(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.replaceData(0, 2, "yoa")
                self.assertEqual(node.data, "yoast")

    def test_in_the_middle_shorter(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.replaceData(1, 2, "o")
                self.assertEqual(node.data, "tot")

    def test_in_the_middle_equal_length(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                node.replaceData(1, 2, "yo")
                self.assertEqual(node.data, "tyot")


class CharacterDataSubstringData(unittest.TestCase):
    def test_too_few_arguments(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                with self.assertRaises(TypeError):
                    node.substringData()
                with self.assertRaises(TypeError):
                    node.substringData(0)

    def test_invalid_offset(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                for args in ((5, 0), (6, 0), (-1, 0)):
                    with self.assertRaises(IndexError):
                        node.substringData(*args)

    def test_in_bounds_offset(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.substringData(0, 1), "t")
                self.assertEqual(node.substringData(1, 1), "e")
                self.assertEqual(node.substringData(2, 1), "s")
                self.assertEqual(node.substringData(3, 1), "t")
                self.assertEqual(node.substringData(4, 1), "")

    def test_zero_count(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                for offset in range(5):
                    self.assertEqual(node.substringData(offset, 0), "")

    def test_very_large_offset_wraps(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.substringData(0x100000000 + 0, 1), "t")
                self.assertEqual(node.substringData(0x100000000 + 2, 1), "s")

    def test_negative_offset_wraps(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                node = _make(kind)
                self.assertEqual(node.substringData(-0x100000000 + 2, 1), "s")


class CharacterDataAppendChild(unittest.TestCase):
    def test_character_data_cannot_have_children(self):
        # Text, Comment and ProcessingInstruction are all CharacterData: none
        # of them may have children, of any kind.
        def create(kind):
            if kind == "Text":
                return document.createTextNode("test")
            if kind == "Comment":
                return document.createComment("test")
            return document.createProcessingInstruction("target", "test")

        kinds = ("Text", "Comment", "ProcessingInstruction")
        for kind1 in kinds:
            for kind2 in kinds:
                with self.subTest(parent=kind1, child=kind2):
                    assert_throws_dom("HierarchyRequestError", lambda: create(kind1).appendChild(create(kind2)))


class CharacterDataRemove(unittest.TestCase):
    def test_remove(self):
        for kind in KINDS:
            with self.subTest(kind=kind):
                parent = document.createElement("div")
                node = _make(kind)
                parent.appendChild(node)
                self.assertIs(node.parentNode, parent)
                node.remove()
                self.assertIsNone(node.parentNode)
                self.assertEqual(list(parent.childNodes), [])


if __name__ == "__main__":
    unittest.main()
