"""
test_reflection
~~~~~~~~~~~~~~~

IDL attributes that reflect content attributes
(https://html.spec.whatwg.org/#reflecting-content-attributes-in-idl-attributes).
"""

import unittest

from domonic.dom import DOMException, DOMParser
from domonic.html import (
    a,
    area,
    base,
    blockquote,
    button,
    canvas,
    div,
    form,
    iframe,
    img,
    input,
    label,
    li,
    link,
    meta,
    ol,
    output,
    script,
    select,
    source,
    textarea,
    time,
    track,
)


def _page(markup, url="https://example.com/dir/page.html"):
    doc = DOMParser().parseFromString(f"<!doctype html><html><head></head><body>{markup}</body></html>", "text/html")
    doc.URL = url
    return doc


class TestStringReflection(unittest.TestCase):
    def test_missing_attribute_reads_empty_string(self):
        el = img()
        for name in ("alt", "srcset", "sizes", "useMap", "title", "lang"):
            self.assertEqual(getattr(el, name), "", name)

    def test_reads_and_writes_the_attribute(self):
        el = img(_alt="cat")
        self.assertEqual(el.alt, "cat")
        el.alt = "dog"
        self.assertEqual(el.getAttribute("alt"), "dog")
        self.assertIn('alt="dog"', str(el))

    def test_none_removes_the_attribute(self):
        el = img(_alt="cat")
        el.alt = None
        self.assertFalse(el.hasAttribute("alt"))

    def test_attribute_with_a_different_content_name(self):
        el = label(_for="email")
        self.assertEqual(el.htmlFor, "email")
        el.htmlFor = "name"
        self.assertEqual(el.getAttribute("for"), "name")
        self.assertEqual(meta(**{"_http-equiv": "refresh"}).httpEquiv, "refresh")
        self.assertEqual(time(_datetime="2026-01-01").dateTime, "2026-01-01")

    def test_parsed_elements_reflect_too(self):
        doc = _page('<input placeholder="Search" pattern="[a-z]+" min="1" max="9" step="2">')
        field = doc.querySelector("input")
        self.assertEqual(
            (field.placeholder, field.pattern, field.min, field.max, field.step), ("Search", "[a-z]+", "1", "9", "2")
        )


class TestURLReflection(unittest.TestCase):
    def test_resolves_against_the_document_url(self):
        doc = _page('<img src="i.png"><script src="/app.js"></script><link href="../s.css">')
        self.assertEqual(doc.querySelector("img").src, "https://example.com/dir/i.png")
        self.assertEqual(doc.querySelector("script").src, "https://example.com/app.js")
        self.assertEqual(doc.querySelector("link").href, "https://example.com/s.css")

    def test_base_element_changes_the_base(self):
        doc = _page('<img src="i.png">')
        doc.querySelector("head").appendChild(base(_href="https://cdn.example.net/assets/"))
        self.assertEqual(doc.querySelector("img").src, "https://cdn.example.net/assets/i.png")

    def test_absolute_urls_are_kept(self):
        doc = _page('<img src="https://other.example/x.png"><iframe src="https://other.example"></iframe>')
        self.assertEqual(doc.querySelector("img").src, "https://other.example/x.png")
        self.assertEqual(doc.querySelector("iframe").src, "https://other.example/")

    def test_without_a_document_url_the_value_is_unchanged(self):
        self.assertEqual(img(_src="/i.png").src, "/i.png")
        self.assertEqual(_page('<img src="i.png">', url="").querySelector("img").src, "i.png")
        self.assertEqual(_page('<img src="i.png">', url="about:blank").querySelector("img").src, "i.png")

    def test_missing_url_attribute_is_empty(self):
        self.assertEqual(_page("<img>").querySelector("img").src, "")
        self.assertEqual(blockquote().cite, "")

    def test_form_action_defaults_to_the_document_url(self):
        doc = _page('<form><button>Go</button></form><form action="search"></form>')
        first, second = doc.querySelectorAll("form")
        self.assertEqual(first.action, "https://example.com/dir/page.html")
        self.assertEqual(second.action, "https://example.com/dir/search")
        self.assertEqual(doc.querySelector("button").formAction, "https://example.com/dir/page.html")

    def test_anchor_href_and_its_parts_resolve(self):
        doc = _page('<a href="/docs?x=1#top">d</a><a href="../up">u</a><a>none</a><area href="map">')
        docs, up, bare = doc.querySelectorAll("a")
        self.assertEqual(docs.href, "https://example.com/docs?x=1#top")
        self.assertEqual((docs.host, docs.pathname, docs.search, docs.hash), ("example.com", "/docs", "?x=1", "#top"))
        self.assertEqual(up.href, "https://example.com/up")
        self.assertEqual(bare.href, "")
        self.assertEqual(doc.querySelector("area").href, "https://example.com/dir/map")
        self.assertEqual(a(_href="/raw").href, "/raw")  # no document URL: as written

    def test_setting_an_anchor_url_part_writes_the_whole_url(self):
        link = _page('<a href="/docs?x=1">d</a>').querySelector("a")
        link.pathname = "/other"
        self.assertEqual(link.getAttribute("href"), "https://example.com/other?x=1")

    def test_base_href_resolves_against_the_document_url(self):
        doc = _page("")
        self.assertEqual(base(_href="/root/").href, "/root/")
        el = doc.createElement("base")
        doc.querySelector("head").appendChild(el)
        self.assertEqual(el.href, "https://example.com/dir/page.html")
        el.href = "../up/"
        self.assertEqual(el.href, "https://example.com/up/")


class TestBooleanReflection(unittest.TestCase):
    def test_presence_is_true_whatever_the_value(self):
        self.assertTrue(input(_required="").required)
        self.assertTrue(input(_disabled="false").disabled)
        self.assertFalse(input().required)
        self.assertFalse(input().readOnly)

    def test_setting(self):
        field = input()
        field.disabled = True
        field.readOnly = True
        self.assertEqual(field.getAttribute("disabled"), "")
        self.assertTrue(field.hasAttribute("readonly"))
        field.disabled = False
        self.assertFalse(field.hasAttribute("disabled"))


class TestNumberReflection(unittest.TestCase):
    def test_long_defaults_and_parsing(self):
        self.assertEqual(ol().start, 1)
        self.assertEqual(ol(_start=" 7th").start, 7)
        self.assertEqual(ol(_start="x").start, 1)
        self.assertEqual(li(_value="-3").value, -3)

    def test_non_negative_long(self):
        self.assertEqual(input().maxLength, -1)
        self.assertEqual(input(_maxlength="-5").maxLength, -1)
        self.assertEqual(textarea(_minlength="4").minLength, 4)
        with self.assertRaises(DOMException) as caught:
            input().maxLength = -1
        self.assertEqual(caught.exception.name, "IndexSizeError")

    def test_unsigned_long_defaults(self):
        self.assertEqual((canvas().width, canvas().height), (300, 150))
        self.assertEqual(canvas(_width="640").width, 640)
        self.assertEqual(img().width, 0)
        self.assertEqual(source(_height="-1").height, 0)

    def test_positive_with_fallback(self):
        self.assertEqual(input().size, 20)
        self.assertEqual(input(_size="0").size, 20)
        self.assertEqual((textarea().cols, textarea().rows), (20, 2))
        field = input()
        field.size = 0
        self.assertEqual(field.getAttribute("size"), "20")

    def test_number_setter_writes_a_string(self):
        el = img()
        el.width = 64
        self.assertEqual(el.getAttribute("width"), "64")


class TestEnumeratedReflection(unittest.TestCase):
    def test_missing_and_invalid_defaults(self):
        self.assertEqual(button().type, "submit")
        self.assertEqual(button(_type="RESET").type, "reset")
        self.assertEqual(button(_type="nope").type, "submit")
        self.assertEqual(form().method, "get")
        self.assertEqual(form(_method="POST").method, "post")
        self.assertEqual(form().enctype, "application/x-www-form-urlencoded")
        self.assertEqual(form(_enctype="multipart/form-data").encoding, "multipart/form-data")
        self.assertEqual(button().formMethod, "")
        self.assertEqual(button(_formmethod="x").formMethod, "get")
        self.assertEqual(img().decoding, "auto")
        self.assertEqual(iframe().loading, "eager")
        self.assertEqual(track().kind, "subtitles")
        self.assertEqual(track(_kind="bogus").kind, "metadata")

    def test_nullable_cross_origin(self):
        self.assertIsNone(img().crossOrigin)
        self.assertEqual(img(_crossorigin="").crossOrigin, "anonymous")
        self.assertEqual(img(_crossorigin="USE-CREDENTIALS").crossOrigin, "use-credentials")
        self.assertEqual(img(_crossorigin="x").crossOrigin, "anonymous")
        el = img(_crossorigin="")
        el.crossOrigin = None
        self.assertFalse(el.hasAttribute("crossorigin"))

    def test_referrer_policy(self):
        self.assertEqual(a().referrerPolicy, "")
        self.assertEqual(a(_referrerpolicy="No-Referrer").referrerPolicy, "no-referrer")
        self.assertEqual(a(_referrerpolicy="bogus").referrerPolicy, "")

    def test_dir(self):
        self.assertEqual(div().dir, "")
        self.assertEqual(div(_dir="RTL").dir, "rtl")
        self.assertEqual(div(_dir="sideways").dir, "")

    def test_keyword_named_properties(self):
        self.assertTrue(getattr(script(_async=""), "async"))
        self.assertFalse(script().async_)
        self.assertEqual(link(_as="style").as_, "style")
        self.assertEqual(getattr(link(_as="bogus"), "as"), "")
        el = script()
        setattr(el, "async", True)
        self.assertTrue(el.hasAttribute("async"))


class TestTokenListReflection(unittest.TestCase):
    def test_rel_list(self):
        anchor = a(_rel="noopener")
        self.assertEqual(list(anchor.relList), ["noopener"])
        anchor.relList.add("noreferrer")
        self.assertEqual(anchor.getAttribute("rel"), "noopener noreferrer")
        self.assertTrue(anchor.relList.supports("NOOPENER"))
        self.assertFalse(anchor.relList.supports("stylesheet"))
        self.assertTrue(link().relList.supports("stylesheet"))
        self.assertEqual(area(_rel="opener").relList.value, "opener")

    def test_no_attribute_is_not_materialised(self):
        el = iframe()
        self.assertEqual(len(el.sandbox), 0)
        el.sandbox.remove("allow-scripts")
        self.assertFalse(el.hasAttribute("sandbox"))
        el.sandbox.add("allow-scripts", "allow-forms")
        self.assertEqual(el.getAttribute("sandbox"), "allow-scripts allow-forms")

    def test_assigning_a_string_sets_the_attribute(self):
        el = output()
        el.htmlFor = "a b"
        self.assertEqual(list(el.htmlFor), ["a", "b"])

    def test_class_list_is_unchanged(self):
        el = div(_class="x")
        with self.assertRaises(TypeError):
            el.classList.supports("x")
        el.classList.add("y")
        self.assertEqual(el.className, "x y")


class TestReflectionDoesNotShadowExistingAPIs(unittest.TestCase):
    def test_hand_written_properties_still_win(self):
        self.assertEqual(input(_type="checkbox").value, "on")
        self.assertEqual(select(_multiple="").type, "select-multiple")
        self.assertEqual(input().type, "text")

    def test_reflected_names_still_render(self):
        el = img(_src="a.png", _alt="A", _width="10")
        self.assertEqual(str(el), '<img src="a.png" alt="A" width="10"/>')


if __name__ == "__main__":
    unittest.main()
