"""
test_html_table
~~~~~~~~~~~~~~~

The HTMLTableElement family (https://html.spec.whatwg.org/#tables).
"""

import unittest

from domonic.dom import DOMException, DOMParser
from domonic.html import caption, div, table, tbody, td, tfoot, th, thead, tr

MARKUP = (
    "<table><caption>Scores</caption>"
    "<tfoot><tr><td>Total</td><td>9</td></tr></tfoot>"
    "<thead><tr><th>Name</th><th>Score</th></tr></thead>"
    "<tbody><tr><td>Ann</td><td>4</td></tr><tr><td>Bob</td><td colspan='2'>5</td></tr></tbody>"
    "</table>"
)


def _parsed_table():
    doc = DOMParser().parseFromString(f"<!doctype html><html><body>{MARKUP}</body></html>", "text/html")
    return doc.querySelector("table")


def _texts(rows):
    return [row.cells[0].textContent for row in rows]


class TestTableElement(unittest.TestCase):
    def test_rows_put_thead_first_and_tfoot_last(self):
        self.assertEqual(_texts(_parsed_table().rows), ["Name", "Ann", "Bob", "Total"])

    def test_sections_and_caption(self):
        t = _parsed_table()
        self.assertEqual(t.caption.textContent, "Scores")
        self.assertEqual(t.tHead.localName, "thead")
        self.assertEqual(t.tFoot.localName, "tfoot")
        self.assertEqual(len(t.tBodies), 1)
        self.assertIsNone(table().caption)
        self.assertIsNone(table().tHead)

    def test_rows_is_live(self):
        t = _parsed_table()
        rows = t.rows
        t.tBodies[0].appendChild(tr(td("Cy")))
        self.assertEqual(len(rows), 5)
        self.assertEqual(rows[3].cells[0].textContent, "Cy")
        self.assertIsNone(rows[9])

    def test_insert_row_into_an_empty_table_adds_a_tbody(self):
        t = table()
        row = t.insertRow()
        self.assertEqual(str(t), "<table><tbody><tr></tr></tbody></table>")
        self.assertIs(t.rows[0], row)

    def test_insert_row_uses_the_existing_last_tbody(self):
        t = table(tbody(), tbody())
        t.insertRow()
        self.assertEqual(str(t), "<table><tbody></tbody><tbody><tr></tr></tbody></table>")

    def test_insert_row_positions(self):
        t = _parsed_table()
        appended = t.insertRow()
        self.assertIs(appended.parentNode, t.tFoot)
        middle = t.insertRow(2)
        self.assertIs(t.rows[2], middle)
        self.assertIs(middle.parentNode, t.tBodies[0])
        self.assertEqual(middle.tagName, "TR")

    def test_delete_row(self):
        t = _parsed_table()
        t.deleteRow(1)
        self.assertEqual(_texts(t.rows), ["Name", "Bob", "Total"])
        t.deleteRow(-1)
        self.assertEqual(_texts(t.rows), ["Name", "Bob"])
        table().deleteRow(-1)  # nothing to delete: no error

    def test_index_errors(self):
        t = _parsed_table()
        for call in (lambda: t.insertRow(-2), lambda: t.insertRow(5), lambda: t.deleteRow(4), lambda: t.deleteRow(-2)):
            with self.assertRaises(DOMException) as caught:
                call()
            self.assertEqual(caught.exception.name, "IndexSizeError")

    def test_create_and_delete_sections(self):
        t = table(tbody())
        head = t.createTHead()
        self.assertIs(t.createTHead(), head)
        t.createTFoot()
        t.createCaption()
        self.assertEqual(str(t), "<table><caption></caption><thead></thead><tbody></tbody><tfoot></tfoot></table>")
        t.deleteCaption()
        t.deleteTHead()
        t.deleteTFoot()
        self.assertEqual(str(t), "<table><tbody></tbody></table>")

    def test_thead_goes_after_caption_and_colgroup(self):
        t = table(caption("c"), tbody())
        t.tHead = thead()
        self.assertEqual(str(t), "<table><caption>c</caption><thead></thead><tbody></tbody></table>")

    def test_section_setters_check_the_type(self):
        t = table()
        with self.assertRaises(DOMException) as caught:
            t.tHead = tfoot()
        self.assertEqual(caught.exception.name, "HierarchyRequestError")
        with self.assertRaises(TypeError):
            t.caption = div()
        t.caption = caption("new")
        self.assertEqual(t.caption.textContent, "new")
        t.caption = None
        self.assertIsNone(t.caption)

    def test_create_tbody_goes_after_the_last_tbody(self):
        t = table(thead(), tbody(), tfoot())
        t.createTBody()
        self.assertEqual(str(t), "<table><thead></thead><tbody></tbody><tbody></tbody><tfoot></tfoot></table>")

    def test_obsolete_attributes_reflect(self):
        t = table(_border="1", _summary="s")
        self.assertEqual((t.border, t.summary, t.width), ("1", "s", ""))


class TestTableSectionAndRow(unittest.TestCase):
    def test_section_rows(self):
        body = _parsed_table().tBodies[0]
        self.assertEqual(_texts(body.rows), ["Ann", "Bob"])
        row = body.insertRow(0)
        self.assertIs(body.rows[0], row)
        body.deleteRow(0)
        self.assertEqual(_texts(body.rows), ["Ann", "Bob"])

    def test_row_and_section_indexes(self):
        t = _parsed_table()
        bob = t.rows[2]
        self.assertEqual((bob.rowIndex, bob.sectionRowIndex), (2, 1))
        total = t.rows[3]
        self.assertEqual((total.rowIndex, total.sectionRowIndex), (3, 0))
        self.assertEqual((tr().rowIndex, tr().sectionRowIndex), (-1, -1))

    def test_cells(self):
        row = tr(th("a"), td("b"))
        self.assertEqual([cell.textContent for cell in row.cells], ["a", "b"])
        cell = row.insertCell(1)
        self.assertEqual(cell.localName, "td")
        self.assertEqual(cell.cellIndex, 1)
        row.deleteCell(-1)
        self.assertEqual(len(row.cells), 2)
        self.assertIs(row.cells[1], cell)
        with self.assertRaises(DOMException):
            row.deleteCell(5)
        self.assertEqual(td().cellIndex, -1)


class TestTableCell(unittest.TestCase):
    def test_span_clamping(self):
        self.assertEqual(td().colSpan, 1)
        self.assertEqual(td(_colspan="0").colSpan, 1)
        self.assertEqual(td(_colspan="5000").colSpan, 1000)
        self.assertEqual(td(_rowspan="0").rowSpan, 0)
        self.assertEqual(td(_rowspan="x").rowSpan, 1)
        cell = td()
        cell.colSpan = 3
        self.assertEqual(cell.getAttribute("colspan"), "3")

    def test_other_cell_attributes(self):
        cell = th(_scope="COL", _abbr="n", _headers="h1 h2")
        self.assertEqual((cell.scope, cell.abbr, cell.headers), ("col", "n", "h1 h2"))
        self.assertEqual(td(_scope="diagonal").scope, "")


if __name__ == "__main__":
    unittest.main()
