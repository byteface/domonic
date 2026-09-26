"""
test_bs4
~~~~~~~~
- compatibility tests for domonic.bs4
"""

import re
import subprocess
import sys
import unittest

import domonic
from domonic.bs4 import BeautifulSlop
from domonic.dom import DocumentFragment, Element, Text

HTML = """
<main id="root">
  <article id="story" class="feature external">
    <h1>Title</h1>
    <p class="lede"> Hello <a href="/one" class="external">one</a></p>
    <a href="/two" data-kind="nav">two</a>
  </article>
  <aside><a href="/side">side</a></aside>
</main>
"""


class BeautifulSlopTest(unittest.TestCase):
    def setUp(self):
        self.soup = BeautifulSlop(HTML, "html.parser")

    def test_constructor_parser_selection_and_domonic_nodes(self):
        soup = BeautifulSlop("<section><p>ok</p></section>", "html5lib")

        self.assertIsInstance(soup, (DocumentFragment, Element))
        self.assertEqual(soup.find("p").text, "ok")

    def test_find_and_find_all_delegate_common_cases(self):
        self.assertEqual(self.soup.find("article")["id"], "story")
        self.assertEqual(
            [link["href"] for link in self.soup.find_all("a")],
            ["/one", "/two", "/side"],
        )
        self.assertEqual(self.soup.find("article", id="story").name, "article")
        self.assertEqual(self.soup.find_all("a", class_="external")[0]["href"], "/one")
        self.assertEqual(self.soup.find_all("a", {"data-kind": "nav"})[0].text, "two")
        self.assertEqual(len(self.soup.find_all("a", limit=2)), 2)

    def test_filter_types(self):
        self.assertEqual(
            [node.name for node in self.soup.find_all(["article", "aside"])],
            ["article", "aside"],
        )
        self.assertEqual(self.soup.find(re.compile("^art")).name, "article")
        self.assertEqual(
            self.soup.find(lambda tag: getattr(tag, "name", "") == "aside").name,
            "aside",
        )
        self.assertEqual(self.soup.find("a", href=re.compile("two$")).text, "two")
        self.assertEqual(
            self.soup.find("a", href=lambda value: value == "/side").text, "side"
        )
        self.assertEqual(self.soup.find_all(True)[0].name, "main")

    def test_class_attribute_matching_is_token_based(self):
        soup = BeautifulSlop(
            '<main><p class="body strikeout">x</p><p class="body">y</p></main>',
            "html.parser",
        )

        self.assertEqual(
            [p.text for p in soup.find_all("p", class_="body")],
            ["x", "y"],
        )
        self.assertEqual(soup.find("p", class_="strikeout").text, "x")
        self.assertEqual(soup.find("p", class_=re.compile("^str")).text, "x")
        self.assertEqual(
            soup.find("p", class_=lambda value: value == "body").text,
            "x",
        )
        self.assertEqual(
            [p.text for p in soup.find_all("p", {"class": ["missing", "strikeout"]})],
            ["x"],
        )

    def test_string_filters_return_text_children(self):
        title = self.soup.find(string="Title")

        self.assertIsInstance(title, Text)
        self.assertEqual(str(title), "Title")
        self.assertEqual(self.soup.find("h1", string="Title").name, "h1")
        self.assertEqual(self.soup.find("h1", text="Title").name, "h1")
        self.assertEqual(str(self.soup.find(string=re.compile("one"))), "one")
        self.assertEqual(str(self.soup.find(text=lambda value: value == "two")), "two")

    def test_recursive_false_and_child_aliases(self):
        article = self.soup.find("article")

        self.assertEqual(article.find("a", recursive=False)["href"], "/two")
        self.assertEqual(article.find_child("h1").text, "Title")
        self.assertEqual(article.findChild("h1").text, "Title")
        self.assertEqual(
            [node.name for node in article.find_children()], ["h1", "p", "a"]
        )
        self.assertEqual(
            [node.name for node in article.findChildren("p")],
            ["p"],
        )

    def test_presence_and_absence_attribute_filters(self):
        self.assertEqual(
            [a["href"] for a in self.soup.find_all("a", href=True)],
            ["/one", "/two", "/side"],
        )
        self.assertEqual(self.soup.find("a", href=None), None)

    def test_css_select(self):
        self.assertEqual(self.soup.select_one("article > a")["href"], "/two")
        self.assertEqual(
            [node.text for node in self.soup.select("a")], ["one", "two", "side"]
        )
        self.assertEqual(self.soup.find("article").select("article"), [])
        self.assertEqual(
            [node["href"] for node in self.soup.select('main#root a[href^="/"]')],
            ["/one", "/two", "/side"],
        )
        self.assertEqual(
            [node["href"] for node in self.soup.select('article > a[data-kind="nav"]')],
            ["/two"],
        )
        article = self.soup.find("article")
        badge = article.new_tag("span", class_="badge")
        badge.append("patched")
        article.find("h1").insert_after(badge)
        self.assertEqual(article.select_one("article > span").text, "patched")
        nested = BeautifulSlop(
            '<table><tr><td><table><tr><td><a href="/x">x</a></td></tr></table></td></tr></table>',
            "html.parser",
        )
        self.assertEqual(len(nested.select("table a[href]")), 1)
        self.assertEqual(
            [node.name for node in self.soup.select("aside, article.external")],
            ["article", "aside"],
        )

    def test_common_css_pseudo_selectors(self):
        soup = BeautifulSlop(
            """
            <main>
              <ul>
                <li><a href="/one">one</a></li>
                <li><a href="/two">two</a></li>
                <li><a href="/three">three</a></li>
              </ul>
              <p><span>first</span><span>last</span></p>
            </main>
            """,
            "html.parser",
        )

        self.assertEqual(soup.select_one("li:first-child a")["href"], "/one")
        self.assertEqual(soup.select_one("li:nth-child(2) a")["href"], "/two")
        self.assertEqual(soup.select_one("li:last-child a")["href"], "/three")
        self.assertEqual(
            [
                node.text
                for node in soup.select("p > span:first-child, p > span:last-child")
            ],
            ["first", "last"],
        )

    def test_parents_children_siblings_and_document_order(self):
        first = self.soup.find("a", href="/one")
        second = self.soup.find("a", href="/two")

        self.assertEqual(first.parent.name, "p")
        self.assertEqual(
            [node.name for node in first.parents if getattr(node, "name", None)][:2],
            ["p", "article"],
        )
        self.assertIn(first, list(first.parent.children))
        self.assertEqual(second.find_previous("h1").text, "Title")
        self.assertEqual(first.find_next("a")["href"], "/two")
        self.assertEqual(second.find_previous_sibling("p").name, "p")
        self.assertEqual(first.find_next_sibling(), None)
        self.assertEqual(
            self.soup.find("article").find_next_sibling("aside").name, "aside"
        )
        self.assertEqual(str(first.next_element), "one")
        self.assertEqual(str(second.previous_element).strip(), "")

    def test_attrs_get_and_item_access(self):
        link = self.soup.find("a")

        self.assertTrue(link.has_attr("href"))
        self.assertTrue(link.has_key("href"))
        self.assertEqual(link.get("missing", "fallback"), "fallback")
        self.assertEqual(link.attrs["href"], "/one")
        link["href"] = "/changed"
        self.assertEqual(link.get("href"), "/changed")
        del link["href"]
        self.assertFalse(link.has_attr("href"))

    def test_text_get_text_strings(self):
        article = self.soup.find("article")

        self.assertEqual(article.find("h1").string, "Title")
        self.assertEqual(article.get_text("|", strip=True), "Title|Hello|one|two")
        self.assertIn(" Hello ", list(article.strings))
        self.assertEqual(list(article.find("p").stripped_strings), ["Hello", "one"])

    def test_document_get_text_skips_script_and_style_children(self):
        soup = BeautifulSlop(
            "<main>visible<script>hidden()</script><style>.x{}</style></main>",
            "html.parser",
        )

        self.assertEqual(soup.get_text("", strip=True), "visible")
        self.assertEqual(soup.find("script").get_text("", strip=True), "hidden()")

    def test_mutation_methods(self):
        soup = BeautifulSlop("<section><p>one</p><p>two</p></section>", "html.parser")
        first = soup.find("p", string="one")
        second = soup.find("p", string="two")

        new_link = soup.new_tag("a", href="/new")
        new_link.append("new")
        first.insert_after(new_link)
        self.assertEqual(soup.find("a")["href"], "/new")

        wrapper = soup.new_tag("div", class_="wrap")
        second.wrap(wrapper)
        self.assertEqual(second.parent["class"], "wrap")
        wrapper.unwrap()
        self.assertEqual(second.parent.name, "section")

        replacement = soup.new_tag("strong")
        replacement.append("bold")
        second.replace_with(replacement)
        self.assertEqual(soup.find("strong").text, "bold")

        extracted = first.extract()
        self.assertEqual(extracted.text, "one")
        self.assertIsNone(soup.find("p", string="one"))

        soup.find("strong").decompose()
        self.assertIsNone(soup.find("strong"))

    def test_root_tag_index_is_invalidated_by_mutation(self):
        soup = BeautifulSlop("<section><a>one</a></section>", "html.parser")

        self.assertEqual(len(soup.find_all("a")), 1)
        soup.append(soup.new_tag("a"))
        self.assertEqual(len(soup.find_all("a")), 2)
        soup.find("a").decompose()
        self.assertEqual(len(soup.find_all("a")), 1)

    def test_new_string_clear_smooth_and_rendering(self):
        soup = BeautifulSlop("<section><p>one</p></section>", "html.parser")
        text = soup.new_string("two")

        self.assertIsInstance(text, Text)
        self.assertEqual(text.get_text(strip=True), "two")
        soup.find("p").append(text)
        self.assertEqual(soup.find("p").text, "onetwo")
        soup.find("p").smooth()
        self.assertEqual(soup.find("p").contents, ["onetwo"])
        self.assertIn("<section>", str(soup))
        pretty = soup.prettify()
        # bs4 prettify: one node per line, single-space indent
        self.assertIn("<section>\n <p>\n  onetwo\n </p>\n</section>", pretty)
        soup.find("p").clear()
        self.assertEqual(soup.find("p").contents, [])

    def test_normal_domonic_import_does_not_install_bs4_api(self):
        code = "from domonic.html import div; print(hasattr(div(), 'find'))"
        result = subprocess.run(
            [sys.executable, "-c", code],
            check=True,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.stdout.strip(), "False")

    def test_imported_patch_applies_to_new_and_cloned_nodes(self):
        soup = BeautifulSlop("<div><p>one</p></div>", "html.parser")
        new_tag = soup.new_tag("span")
        clone = soup.cloneNode(True)

        self.assertTrue(hasattr(new_tag, "find"))
        self.assertTrue(hasattr(clone, "find"))
        self.assertEqual(clone.find("p").text, "one")

    def test_turbohtml_tokenized_class_attributes_are_findable(self):
        try:
            import turbohtml  # noqa: F401
        except ImportError:
            self.skipTest("turbohtml is not installed")

        soup = BeautifulSlop(
            '<main><div class="mw-parser-output prose">ok</div></main>',
            "turbohtml",
        )

        self.assertEqual(soup.find(class_="mw-parser-output").name, "div")
        self.assertEqual(soup.select_one(".mw-parser-output").text, "ok")


if __name__ == "__main__":
    unittest.main()


class TextIndexTest(unittest.TestCase):
    """BeautifulSlop keeps the parser's record of a whole document's text nodes
    (``parseString(..., text_index=True)``); the record must be exactly what a
    tree walk finds and must retire on any change to the tree."""

    PAGE = (
        "<!doctype html><html><head><title>T</title><style>p{}</style>"
        "<script>var x = 1;</script></head><body><h1>Head</h1>"
        "<p>one <b>two</b> three</p><p id='last'>four</p><script src=a.js>skip()</script></body></html>"
    )

    def _walk(self, soup, strip=False):
        from domonic.bs4 import _collect_text

        parts = []
        _collect_text(soup.__dict__["args"], parts.append, strip)
        return parts

    def test_recorded_text_matches_a_walk(self):
        from domonic.dom import _text_run_for

        soup = BeautifulSlop(self.PAGE, "html.parser")
        self.assertIsNotNone(_text_run_for(soup))
        self.assertEqual(soup.get_text(), "".join(self._walk(soup)))
        self.assertEqual(soup.get_text(" ", strip=True), " ".join(self._walk(soup, strip=True)))
        self.assertEqual(list(soup.strings), self._walk(soup))
        self.assertEqual(list(soup.stripped_strings), self._walk(soup, strip=True))
        self.assertNotIn("var x", soup.get_text())  # script and style text left out
        self.assertNotIn("skip()", soup.get_text())
        self.assertIn("var x = 1;", soup.textContent)  # but DOM textContent keeps it

    def test_plain_parse_string_and_fragments_are_untouched(self):
        from domonic.dom import _text_run_for

        self.assertIsNone(_text_run_for(domonic.parseString(self.PAGE, parser="html.parser")))
        snippet = BeautifulSlop("<p>one <b>two</b></p>", "html.parser")
        self.assertIsNone(_text_run_for(snippet))
        self.assertEqual(snippet.get_text(), "one two")

    def test_the_record_retires_on_any_change(self):
        from domonic.dom import Text, _text_run_for
        from domonic.html import p

        for label, mutate in (
            ("appendChild", lambda s: s.body.appendChild(p("late"))),
            ("removeChild", lambda s: s.body.removeChild(s.select_one("#last"))),
            ("textContent", lambda s: setattr(s.select_one("#last"), "textContent", "changed")),
            ("Text.data", lambda s: setattr(s.select_one("#last").firstChild, "data", "changed")),
            ("args", lambda s: setattr(s.select_one("#last"), "args", (Text("changed"),))),
            ("innerHTML", lambda s: setattr(s.select_one("#last"), "innerHTML", "<i>changed</i>")),
            ("replaceChildren", lambda s: s.select_one("#last").replaceChildren(Text("changed"))),
            ("splitText", lambda s: s.select_one("#last").firstChild.splitText(2)),
            ("remove", lambda s: s.select_one("#last").remove()),
        ):
            with self.subTest(label):
                soup = BeautifulSlop(self.PAGE, "html.parser")
                self.assertIsNotNone(_text_run_for(soup))
                mutate(soup)
                self.assertIsNone(_text_run_for(soup))
                self.assertEqual(soup.get_text(), "".join(self._walk(soup)))
                self.assertEqual(soup.textContent, domonic.parseString(str(soup), parser="html.parser").textContent)

    def test_a_failing_backend_leaves_nothing_in_the_record(self):
        from domonic.ext._rawdom import _create_text_raw

        def boom(source, **options):
            _create_text_raw("garbage")  # a backend that builds a bit, then gives up
            raise RuntimeError("no thanks")

        domonic.register_parser("boom", boom, auto=True)
        try:
            soup = BeautifulSlop(self.PAGE)  # auto: boom fails, the next backend parses
            self.assertNotIn("garbage", soup.get_text())
            self.assertEqual(soup.get_text(), "".join(self._walk(soup)))
        finally:
            domonic.unregister_parser("boom")

    def test_parallel_parses_keep_their_own_records(self):
        import threading

        results = {}

        def work(index):
            page = self.PAGE.replace("four", f"four-{index}") * 40
            soup = BeautifulSlop(page, "html.parser")
            results[index] = (soup.get_text(), "".join(self._walk(soup)))

        threads = [threading.Thread(target=work, args=(i,)) for i in range(6)]
        for thread in threads:
            thread.start()
        for thread in threads:
            thread.join()
        for index, (recorded, walked) in results.items():
            self.assertEqual(recorded, walked, index)
            self.assertIn(f"four-{index}", recorded)

