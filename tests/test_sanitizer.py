"""
test_sanitizer
~~~~~~~~~~~~~~
setHTML / Sanitizer: the output must be inert however a browser parses it.

Each payload's output is re-parsed with html5lib (an independent spec parser)
twice -- once as is, and once with <noscript> read as raw text, the way a
browser with scripting on reads it -- and neither parse may contain anything
that runs script.
"""

import re
import unittest

import html5lib

from domonic.dom import Document
from domonic.html import div
from domonic.webapi.sanitizer import Sanitizer

PAYLOADS = [
    # raw text / RCDATA elements whose end tag hides in an attribute or text
    '<noscript><p title="</noscript><img src=x onerror=alert(1)>">',
    "<noscript>&lt;/noscript&gt;&lt;img src=x onerror=alert(1)&gt;</noscript>",
    '<textarea><img title="</textarea><img src=x onerror=alert(1)>"></textarea>',
    '<title><img title="</title><img src=x onerror=alert(1)>"></title>',
    '<noembed><img title="</noembed><img src=x onerror=alert(1)>"></noembed>',
    '<noframes><img title="</noframes><img src=x onerror=alert(1)>"></noframes>',
    "<xmp></xmp><img src=x onerror=alert(1)></xmp>",
    "<plaintext><img src=x onerror=alert(1)>",
    "<style><img src=x onerror=alert(1)></style>",
    # namespace confusion
    "<svg><style>&lt;/style&gt;&lt;img src=x onerror=alert(1)&gt;</style></svg>",
    "<svg><style><img src=x onerror=alert(1)></style></svg>",
    "<math><mtext><table><mglyph><style><img src=x onerror=alert(1)>",
    "<form><math><mtext></form><form><mglyph><style></math><img src onerror=alert(1)>",
    '<math><mi><mglyph><svg><mtext><textarea><path id="</textarea><img onerror=alert(1) src=1>">',
    '<svg></p><style><a id="</style><img src=1 onerror=alert(1)>">',
    "<svg><foreignObject><img src=x onerror=alert(1)></foreignObject></svg>",
    "<svg><script>alert(1)</script></svg>",
    # parsers that disagree on raw text
    "<select><style></select><img src=x onerror=alert(1)></style></select>",
    "<table><style></table><img src=x onerror=alert(1)></style>",
    # javascript: URLs
    '<a href="jav&#x09;ascript:alert(1)">x</a>',
    '<a href=" javascript:alert(1)">x</a>',
    '<a href="JaVaScRiPt:alert(1)">x</a>',
    '<a href="java\nscript:alert(1)">x</a>',
    '<a href="&#106;avascript:alert(1)">x</a>',
    '<a href="javascript&colon;alert(1)">x</a>',
    '<svg><a xlink:href="javascript:alert(1)"><text>x</text></a></svg>',
    "<svg><a><animate attributeName=href values=javascript:alert(1) /><text>X</text></a></svg>",
    '<svg><set attributeName="xlink:href" to="javascript:alert(1)"/></svg>',
    '<math href="javascript:alert(1)">x</math>',
    '<form action="javascript:alert(1)"><button formaction="javascript:alert(1)">x</button></form>',
    # malformed and unclosed input
    "<img src=x onerror=alert(1)//",
    "a <img src=x onerror=alert(1)//",
    "<!--><img src=x onerror=alert(1)>-->",
    "<!-- --!><img src=x onerror=alert(1)> -->",
    "<scr<script>ipt>alert(1)</script>",
    "</div><img src=x onerror=alert(1)>",
    "<script>alert(1)",
    "<style>x",
    # script-capable elements and attributes
    '<iframe srcdoc="<script>alert(1)</script>"></iframe>',
    '<object data="javascript:alert(1)"></object>',
    '<embed src="javascript:alert(1)">',
    '<svg><use href="data:image/svg+xml,<svg id=x></svg>#x"/></svg>',
    "<template><img src=x onerror=alert(1)></template>",
    "<template><script>alert(1)</script></template>",
    '<div style="background:url(javascript:alert(1))">x</div>',
]
# only dangerous once comments are allowed
COMMENT_PAYLOADS = [
    "<noscript><!--</noscript><img src=x onerror=alert(1)>--></noscript>",
    "<select><style><!--</style><img src=x onerror=alert(1)>--></style></select>",
]

_RUNS_SCRIPT = {"script", "iframe", "frame", "object", "embed", "use"}
_URL_ATTRIBUTES = {"href", "src", "action", "formaction", "data", "xlink:href"}


def _live(markup):
    """What in ``markup`` would run script, by either parse."""
    found = []
    for variant in (markup, re.sub(r"(?i)<(/?)noscript", r"<\1xmp", markup)):
        tree = html5lib.parse(f"<div>{variant}</div>", namespaceHTMLElements=False)
        for element in tree.iter():
            tag = str(element.tag).split("}")[-1].lower()
            if tag in _RUNS_SCRIPT:
                found.append(tag)
            for key, value in element.attrib.items():
                name = str(key).split("}")[-1].lower()
                if name.startswith("on"):
                    found.append(f"{tag}[{name}]")
                if name in _URL_ATTRIBUTES and re.sub(r"[\x00-\x20]", "", value).lower().startswith("javascript:"):
                    found.append(f"{tag}[{name}]")
                if tag in ("animate", "set") and name == "attributename" and value.strip().lower() == "href":
                    found.append(f"{tag}[attributeName]")
    return found


class TestSetHTMLIsInert(unittest.TestCase):
    def check(self, payload, options=None):
        target = Document().createElement("div")
        target.setHTML(payload, options)
        for label, markup in (("innerHTML", target.innerHTML), ("str", str(target)[len("<div>") : -len("</div>")])):
            with self.subTest(payload=payload, output=label):
                self.assertEqual(_live(markup), [], markup)

    def test_payloads(self):
        for payload in PAYLOADS:
            self.check(payload)

    def test_payloads_with_comments_allowed(self):
        for payload in PAYLOADS + COMMENT_PAYLOADS:
            self.check(payload, {"sanitizer": {"comments": True}})


class TestSetHTMLKeepsContent(unittest.TestCase):
    def html(self, value, options=None):
        target = div()
        target.setHTML(value, options)
        return target

    def test_text_is_not_double_escaped(self):
        target = self.html("Tom & Jerry")
        self.assertEqual(target.textContent, "Tom & Jerry")
        self.assertEqual(target.innerHTML, "Tom &amp; Jerry")

    def test_character_references_are_decoded(self):
        target = self.html("<p>5 &lt; 6 &amp; caf&eacute;</p>")
        self.assertEqual(target.textContent, "5 < 6 & café")
        self.assertEqual(target.innerHTML, "<p>5 &lt; 6 &amp; café</p>")

    def test_attribute_values_survive(self):
        target = self.html('<a href="/x?a=1&amp;b=2" title="&quot;q&quot;">x</a>')
        self.assertEqual(target.querySelector("a").getAttribute("href"), "/x?a=1&b=2")
        self.assertEqual(target.querySelector("a").getAttribute("title"), '"q"')

    def test_style_text_is_kept_verbatim(self):
        self.assertEqual(self.html("<style>a>b{color:red}</style>").innerHTML, "<style>a>b{color:red}</style>")

    def test_unsafe_parts_go_and_the_rest_stays(self):
        target = self.html('<p onclick="x()">Hi <script>bad()</script><img src=a.png onerror=x()></p>')
        self.assertEqual(target.innerHTML, '<p>Hi <img src="a.png"></p>')

    def test_comments_follow_the_config(self):
        self.assertEqual(self.html("<p>a<!--c-->b</p>").innerHTML, "<p>ab</p>")
        self.assertEqual(
            self.html("<p>a<!--c-->b</p>", {"sanitizer": {"comments": True}}).innerHTML, "<p>a<!--c-->b</p>"
        )

    def test_unlisted_elements_are_replaced_by_their_children(self):
        target = self.html("<div><b>x</b><i>y</i></div>", {"sanitizer": {"elements": ["b"]}})
        self.assertEqual(target.innerHTML, "<b>x</b>y")

    def test_template_content_is_cleaned(self):
        self.assertEqual(
            self.html("<template><b onclick=x()>t</b></template>").innerHTML, "<template><b>t</b></template>"
        )

    def test_deep_input_does_not_exhaust_the_stack(self):
        depth = 5000
        target = self.html("<b>" * depth + "x" + "</b>" * depth, {"sanitizer": {"elements": []}})
        self.assertEqual(target.innerHTML, "x")

    def test_sanitize_to_string(self):
        self.assertEqual(
            Sanitizer().sanitizeToString("<b>Tom & Jerry</b><img src=x onerror=alert(1)>"),
            '<b>Tom &amp; Jerry</b><img src="x"/>',
        )


class TestSerializerReparsesTheSame(unittest.TestCase):
    """innerHTML / str() output must build the same tree when re-parsed."""

    def roundtrip(self, markup):
        target = Document().createElement("div")
        target.innerHTML = markup
        return target

    def test_lt_and_gt_are_escaped_in_attributes(self):
        target = self.roundtrip('<p title="a<b>">x</p>')
        self.assertEqual(target.innerHTML, '<p title="a&lt;b&gt;">x</p>')

    def test_foreign_style_text_is_escaped(self):
        target = self.roundtrip("<svg><style>&lt;/style&gt;&lt;img&gt;</style></svg>")
        self.assertEqual(target.innerHTML, "<svg><style>&lt;/style&gt;&lt;img&gt;</style></svg>")
        self.assertEqual(str(target), "<div><svg><style>&lt;/style&gt;&lt;img&gt;</style></svg></div>")

    def test_noscript_text_is_escaped(self):
        target = self.roundtrip("<noscript>&lt;/noscript&gt;&lt;b&gt;</noscript>")
        self.assertEqual(target.innerHTML, "<noscript>&lt;/noscript&gt;&lt;b&gt;</noscript>")

    def test_html_raw_text_is_still_verbatim(self):
        target = self.roundtrip("<script>if (a < b && c) {}</script>")
        self.assertEqual(target.innerHTML, "<script>if (a < b && c) {}</script>")

    def test_character_reference_only_text_is_decoded(self):
        target = self.roundtrip("a &amp; b")
        self.assertEqual(target.textContent, "a & b")


if __name__ == "__main__":
    unittest.main()
