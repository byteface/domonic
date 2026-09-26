"""``document.open()`` / ``write()`` / ``close()``: parsing a page as it
arrives, on the browser's own model, under each streaming engine."""

import re
import unittest

import domonic
from domonic.dom import Document, HTMLDocument, MutationObserver
from domonic.html import html
from domonic.window import Window

SRC = (
    "<!DOCTYPE html><html lang=en><head><title>T</title>"
    "<script src=a.js></script><script src=b.js></script></head>"
    "<body><div id=x><p>one</p><p>two</p></div><script src=c.js></script></body></html>"
)
HEAD_END = SRC.index("</head>") + len("</head>")


def _engine_of(doc):
    return doc.__dict__["_parser_session"].engine.name


class StreamingUnderEngine(unittest.TestCase):
    """Shared cases; each subclass pins one engine through ``set_default_parser``."""

    ENGINE = "html5lib"

    def setUp(self):
        domonic.set_default_parser(self.ENGINE)

    def tearDown(self):
        domonic.set_default_parser("auto")

    def test_the_requested_engine_runs(self):
        doc = HTMLDocument()
        doc.open()
        self.assertEqual(_engine_of(doc), self.ENGINE)
        doc.close()

    def test_write_accumulates_until_close(self):
        doc = HTMLDocument()
        doc.open()
        self.assertEqual(doc.readyState, "loading")
        doc.write("<html><body><p>one</p>")
        doc.write("<p>two</p></body></html>")
        self.assertEqual(len(doc.querySelectorAll("p")), 2)  # live before close
        doc.close()
        self.assertEqual(doc.readyState, "complete")
        self.assertEqual([p.textContent for p in doc.querySelectorAll("p")], ["one", "two"])
        self.assertEqual(doc.documentElement.tagName.lower(), "html")
        self.assertIsNone(doc.doctype)
        doc.open()  # a second open empties the document again
        self.assertEqual(list(doc.querySelectorAll("p")), [])
        doc.close()

    def test_partial_document_is_live_between_writes(self):
        doc = HTMLDocument()
        doc.open()
        doc.write(SRC[:HEAD_END])
        self.assertEqual(doc.querySelector("title").textContent, "T")
        self.assertEqual([s.getAttribute("src") for s in doc.querySelectorAll("script")], ["a.js", "b.js"])
        self.assertIsNone(doc.getElementById("x"))
        self.assertIsNone(doc.body)
        self.assertIn("<title>T</title>", str(doc))
        doc.write(SRC[HEAD_END:])
        doc.close()
        self.assertIsNotNone(doc.getElementById("x"))  # the lookup cached above is not stale
        self.assertEqual(len(doc.querySelectorAll("script")), 3)
        self.assertEqual(doc.doctype.name, "html")
        self.assertEqual(doc.getAttribute("lang"), "en")  # the <html> tag is the document
        self.assertIn("<p>two</p>", str(doc))

    def test_bytes_chunks_may_split_a_character(self):
        doc = HTMLDocument()
        doc.open()
        data = "<html><body><p>caf\u00e9 \u2014 ok</p></body></html>".encode("utf-8")
        cut = data.index(b"\xc3") + 1  # inside the two bytes of \u00e9
        doc.write(data[:cut])
        doc.write(data[cut:])
        doc.close()
        self.assertEqual(doc.querySelector("p").textContent, "caf\u00e9 \u2014 ok")
        self.assertEqual(doc.characterSet, "UTF-8")

    def test_bytes_are_decoded_by_the_declared_charset(self):
        doc = HTMLDocument()
        doc.open()
        data = b'<!DOCTYPE html><html><head><meta charset="windows-1252"><title>T</title></head><body>'
        data += b"<p>caf\xe9</p>" * 200 + b"</body></html>"
        for start in range(0, len(data), 700):  # the first chunk is smaller than the prescan window
            doc.write(data[start:][:700])
        doc.close()
        self.assertEqual(doc.characterSet, "windows-1252")
        self.assertEqual(doc.querySelector("p").textContent, "caf\u00e9")
        small = HTMLDocument()
        small.open()
        small.write(b"<p>caf\xe9</p>")  # never reaches the prescan window: decoded at close
        small.close()
        self.assertEqual(small.querySelector("p").textContent, "caf\u00e9")

    def test_ready_state_and_events_fire_in_order(self):
        seen = []
        doc = HTMLDocument()
        win = Window()
        win.attach(doc)
        doc.addEventListener("readystatechange", lambda event: seen.append(("readystatechange", doc.readyState)))
        doc.addEventListener("DOMContentLoaded", lambda event: seen.append(("DOMContentLoaded", doc.readyState)))
        win.addEventListener("load", lambda event: seen.append(("load", doc.readyState)))
        doc.open()
        doc.write("<html><body></body></html>")
        doc.close()
        self.assertEqual(
            seen,
            [
                ("readystatechange", "loading"),
                ("readystatechange", "interactive"),
                ("DOMContentLoaded", "interactive"),
                ("readystatechange", "complete"),
                ("load", "complete"),
            ],
        )

    def test_mutation_observer_sees_nodes_as_they_land(self):
        doc = HTMLDocument()
        srcs = []
        deliveries = []

        def landed(records, observer):
            deliveries.append(len(records))
            for record in records:
                self.assertEqual(record.type, "childList")
                for node in record.addedNodes:
                    if (getattr(node, "nodeName", "") or "").lower() == "script":
                        srcs.append(node.getAttribute("src"))

        observer = MutationObserver(landed)
        observer.observe(doc, {"childList": True, "subtree": True})
        try:
            doc.open()
            doc.write(SRC[:HEAD_END])
            self.assertEqual(srcs, ["a.js", "b.js"])  # delivered after the first write
            doc.write(SRC[HEAD_END:])
            doc.close()
            self.assertEqual(srcs, ["a.js", "b.js", "c.js"])
            self.assertGreaterEqual(len(deliveries), 2)
        finally:
            observer.disconnect()

    def test_window_stop_ends_the_parse(self):
        doc = HTMLDocument()
        win = Window()
        win.attach(doc)

        def landed(records, observer):
            for record in records:
                for node in record.addedNodes:
                    if (getattr(node, "nodeName", "") or "").lower() == "body":
                        win.stop()  # the head is done

        observer = MutationObserver(landed)
        observer.observe(doc, {"childList": True, "subtree": True})
        try:
            doc.open()
            for token in re.findall(r"[^<]+|<[^>]*>", SRC):  # one tag or text run per write
                doc.write(token)
            doc.close()
        finally:
            observer.disconnect()
        self.assertEqual(doc.querySelector("title").textContent, "T")
        self.assertIsNotNone(doc.body)
        self.assertIsNone(doc.getElementById("x"))  # nothing written after the stop landed
        self.assertEqual(doc.readyState, "complete")

    def test_plain_document_gets_an_html_child_and_serialises_its_children(self):
        # ``window.document`` is a plain Document: it has no tag of its own, so
        # the parsed <html> becomes its documentElement and str() shows the children.
        doc = Document()
        self.assertEqual(str(doc), "")
        doc.open()
        doc.write("<!DOCTYPE html><html><body><p>x</p></body></html>")
        doc.close()
        self.assertEqual(doc.documentElement.tagName.lower(), "html")
        self.assertIs(doc.querySelector("p").parentNode.parentNode, doc.documentElement)
        self.assertTrue(str(doc).startswith("<!DOCTYPE html><html>"))
        self.assertIn("<body><p>x</p></body></html>", str(doc))

    def test_write_without_open_empties_the_document_first(self):
        page = html()
        page.write("sup!")
        page.write(" more")
        page.close()  # a trailing text run may only land at the next tag or at EOF
        self.assertIn("sup! more", str(page))
        page.write("<p>x</p>")  # after close, the next write starts over
        page.close()
        self.assertIn("<p>x</p>", str(page))
        self.assertNotIn("sup!", str(page))


class Html5libStreaming(StreamingUnderEngine):
    ENGINE = "html5lib"

    def test_auto_and_non_streaming_backends_mean_html5lib(self):
        for name in ("auto", "selectolax", "turbohtml", "lxml_html"):
            domonic.set_default_parser(name)
            doc = HTMLDocument()
            doc.open()
            self.assertEqual(_engine_of(doc), "html5lib", name)
            doc.close()

    def test_partial_tree_is_the_spec_tree(self):
        # The HTML5 repairs are visible mid-stream: implied tbody, foster
        # parenting out of the table, and the adoption agency for <b><p>...</b>.
        doc = HTMLDocument()
        doc.open()
        doc.write("<html><body><table><div>foster</div><tr><td>1</td></tr>")
        self.assertEqual(doc.querySelector("table").firstChild.tagName.lower(), "tbody")
        self.assertIs(doc.querySelector("div").nextSibling, doc.querySelector("table"))
        doc.write("</table><b><p>x</b>y</p>")
        doc.close()
        self.assertIn("<b></b><p><b>x</b>y</p>", str(doc.body))

    def test_records_are_delivered_once_per_write(self):
        doc = HTMLDocument()
        deliveries = []
        observer = MutationObserver(lambda records, obs: deliveries.append(len(records)))
        observer.observe(doc, {"childList": True, "subtree": True})
        try:
            doc.open()
            doc.write(SRC[:HEAD_END])
            self.assertEqual(len(deliveries), 1)  # every parent's record in one callback
            doc.write(SRC[HEAD_END:])
            self.assertEqual(len(deliveries), 2)
            doc.close()
        finally:
            observer.disconnect()
        self.assertLessEqual(len(deliveries), 3)

    def test_dropping_finished_nodes_as_they_land_bounds_memory(self):
        import gc
        import pathlib
        import tracemalloc

        path = pathlib.Path(__file__).resolve().parents[1] / "benchmarks" / "html_meaty_page.html"
        if not path.exists():
            self.skipTest("fixture page missing")

        def stream(drop):
            doc = HTMLDocument()
            seen = 0

            def landed(records, observer):
                nonlocal seen
                for record in records:
                    for node in list(record.target.childNodes)[:-1]:  # every child but the last has finished
                        seen += len(node.textContent or "")  # read it on its way through
                        node.remove()

            observer = MutationObserver(landed) if drop else None
            if observer:
                observer.observe(doc, {"childList": True, "subtree": True})
            gc.collect()
            tracemalloc.start()
            try:
                doc.open()
                with open(path, encoding="utf-8") as handle:
                    while chunk := handle.read(16384):
                        doc.write(chunk)
                        if drop:
                            gc.collect()  # dropped nodes are reference cycles (parent <-> child)
                doc.close()
                return tracemalloc.get_traced_memory()[1], seen
            finally:
                tracemalloc.stop()
                if observer:
                    observer.disconnect()

        kept_peak, _ = stream(drop=False)
        dropped_peak, characters = stream(drop=True)
        self.assertGreater(characters, 10_000)  # the content was still seen on its way through
        self.assertLess(dropped_peak * 3, kept_peak)

    def test_a_parser_error_surfaces_on_the_main_thread(self):
        doc = HTMLDocument()
        doc.open()
        session = doc.__dict__["_parser_session"]
        session.engine._error = RuntimeError("boom")  # as if the worker had raised
        with self.assertRaises(RuntimeError):
            doc.write("<p>x</p>")
        session.engine._done = True
        session.closed = True


class StdlibStreaming(StreamingUnderEngine):
    ENGINE = "html.parser"


if __name__ == "__main__":
    unittest.main()
