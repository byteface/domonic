"""
test_bs4
~~~~~~~~
- compatibility tests for domonic.bs4
"""

import re
import subprocess
import sys
import unittest

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
        self.assertEqual(self.soup.find("a", href=lambda value: value == "/side").text, "side")
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
        self.assertEqual([node.name for node in article.find_children()], ["h1", "p", "a"])
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
        self.assertEqual([node.text for node in self.soup.select("a")], ["one", "two", "side"])
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

    def test_parents_children_siblings_and_document_order(self):
        first = self.soup.find("a", href="/one")
        second = self.soup.find("a", href="/two")

        self.assertEqual(first.parent.name, "p")
        self.assertEqual([node.name for node in first.parents if getattr(node, "name", None)][:2], ["p", "article"])
        self.assertIn(first, list(first.parent.children))
        self.assertEqual(second.find_previous("h1").text, "Title")
        self.assertEqual(first.find_next("a")["href"], "/two")
        self.assertEqual(second.find_previous_sibling("p").name, "p")
        self.assertEqual(first.find_next_sibling(), None)
        self.assertEqual(self.soup.find("article").find_next_sibling("aside").name, "aside")
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

    def test_new_string_clear_smooth_and_rendering(self):
        soup = BeautifulSlop("<section><p>one</p></section>", "html.parser")
        text = soup.new_string("two")

        self.assertIsInstance(text, Text)
        soup.find("p").append(text)
        self.assertEqual(soup.find("p").text, "onetwo")
        soup.find("p").smooth()
        self.assertEqual(soup.find("p").contents, ["onetwo"])
        self.assertIn("<section>", str(soup))
        self.assertIn("<p>onetwo</p>", soup.prettify())
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


if __name__ == "__main__":
    unittest.main()
