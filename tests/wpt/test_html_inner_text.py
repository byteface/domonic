"""Ported from wpt/html/dom/elements/the-innertext-and-outertext-properties/
getter-tests.js + getter.html (fetched 2026-11-23).
https://html.spec.whatwg.org/#the-innertext-idl-attribute

Upstream, ``testText(html, expected, name)`` sets ``#container.innerHTML`` in
getter.html (whose stylesheet is ``STYLE`` below), fills the ``poke`` /
``poke-<tag>`` / ``shadow`` placeholders, and checks ``innerText`` and
``outerText`` of ``#target`` (or the container's first element child).
``testTextInSVG`` does the same with the nodes moved into an ``<svg>``.
CASES and SVG_CASES are those rows, in order; the rows domonic can't pass are
in KnownDeviations instead.
"""

import unittest

import pytest

from domonic.dom import DOMParser, Element

STYLE = """
.before::before { content:'abc'; }
.table { display:table; }
.itable { display:inline-table; }
.row { display:table-row; }
.cell { display:table-cell; }
.first-line-uppercase::first-line { text-transform:uppercase; }
.first-letter-uppercase::first-letter { text-transform:uppercase; }
.first-letter-float::first-letter { float:left; }
"""

PAGE = (
    "<!DOCTYPE html><title>innerText/outerText getter test</title><style>" + STYLE + "</style>"
    '<div id="container"></div><svg id="svgContainer"></svg>'
)

CASES = [
    ("<div>abc", "abc", "Simplest possible test"),
    ("<div> abc", "abc", "Leading whitespace removed"),
    ("<div>abc ", "abc", "Trailing whitespace removed"),
    ("<div>abc  def", "abc def", "Internal whitespace compressed"),
    ("<div>abc\ndef", "abc def", "\\n converted to space"),
    ("<div>abc\rdef", "abc def", "\\r converted to space"),
    ("<div>abc\tdef", "abc def", "\\t converted to space"),
    ("<div>abc <br>def", "abc\ndef", "Trailing whitespace before hard line break removed"),
    ("<div>abc<br> def", "abc\ndef", "Leading whitespace after hard line break removed"),
    ("<pre> abc", " abc", "Leading whitespace preserved"),
    ("<pre>abc ", "abc ", "Trailing whitespace preserved"),
    ("<pre>abc  def", "abc  def", "Internal whitespace preserved"),
    ("<pre>abc\ndef", "abc\ndef", "\\n preserved"),
    ("<pre>abc\rdef", "abc\ndef", "\\r converted to newline"),
    ("<pre>abc\tdef", "abc\tdef", "\\t preserved"),
    ("<div><pre>abc</pre><pre>def</pre>", "abc\ndef", "Two <pre> siblings"),
    ("<div style='white-space:pre'> abc", " abc", "Leading whitespace preserved"),
    ("<div style='white-space:pre'>abc ", "abc ", "Trailing whitespace preserved"),
    ("<div style='white-space:pre'>abc  def", "abc  def", "Internal whitespace preserved"),
    ("<div style='white-space:pre'>abc\ndef", "abc\ndef", "\\n preserved"),
    ("<div style='white-space:pre'>abc\rdef", "abc\ndef", "\\r converted to newline"),
    ("<div style='white-space:pre'>abc\tdef", "abc\tdef", "\\t preserved"),
    ("<span style='white-space:pre'> abc", " abc", "Leading whitespace preserved"),
    ("<span style='white-space:pre'>abc ", "abc ", "Trailing whitespace preserved"),
    ("<span style='white-space:pre'>abc  def", "abc  def", "Internal whitespace preserved"),
    ("<span style='white-space:pre'>abc\ndef", "abc\ndef", "\\n preserved"),
    ("<span style='white-space:pre'>abc\rdef", "abc\ndef", "\\r converted to newline"),
    ("<span style='white-space:pre'>abc\tdef", "abc\tdef", "\\t preserved"),
    ("<div style='white-space:pre-line'> abc", "abc", "Leading whitespace removed"),
    ("<div style='white-space:pre-line'>abc ", "abc", "Trailing whitespace removed"),
    ("<div style='white-space:pre-line'>abc  def", "abc def", "Internal whitespace collapsed"),
    ("<div style='white-space:pre-line'>abc\ndef", "abc\ndef", "\\n preserved"),
    ("<div style='white-space:pre-line'>abc\rdef", "abc\ndef", "\\r converted to newline"),
    ("<div style='white-space:pre-line'>abc\tdef", "abc def", "\\t converted to space"),
    ("<div><span>abc </span> def", "abc def", "Whitespace collapses across element boundaries"),
    ("<div><span>abc </span><span></span> def", "abc def", "Whitespace collapses across element boundaries"),
    (
        "<div><span>abc </span><span style='white-space:pre'></span> def",
        "abc def",
        "Whitespace collapses across element boundaries",
    ),
    ("<div>abc <input> def", "abc  def", "Whitespace around <input> should not be collapsed"),
    (
        "<div>abc <span style='display:inline-block'></span> def",
        "abc  def",
        "Whitespace around inline-block should not be collapsed",
    ),
    (
        "<div>abc <span style='display:inline-block'> def </span> ghi",
        "abc def ghi",
        "Trailing space at end of inline-block should be collapsed",
    ),
    (
        "<div>abc <span style='display:inline-flex'></span> def",
        "abc  def",
        "Whitespace around inline-flex should not be collapsed",
    ),
    (
        "<div>abc <span style='display:inline-flex'> def </span> ghi",
        "abc def ghi",
        "Trailing space at end of inline-flex should be collapsed",
    ),
    (
        "<div>abc <span style='display:inline-grid'></span> def",
        "abc  def",
        "Whitespace around inline-grid should not be collapsed",
    ),
    (
        "<div>abc <span style='display:inline-grid'> def </span> ghi",
        "abc def ghi",
        "Trailing space at end of grid-flex should be collapsed",
    ),
    ("<div><input> <div>abc</div>", "abc", "Whitespace between <input> and block should be collapsed"),
    (
        "<div><span style='inline-block'></span> <div>abc</div>",
        "abc",
        "Whitespace between inline-block and block should be collapsed",
    ),
    (
        "<div><span style='inline-flex'></span> <div>abc</div>",
        "abc",
        "Whitespace between inline-flex and block should be collapsed",
    ),
    (
        "<div><span style='inline-grid'></span> <div>abc</div>",
        "abc",
        "Whitespace between inline-grid and block should be collapsed",
    ),
    ("<div>abc <img> def", "abc  def", "Whitespace around <img> should not be collapsed"),
    ("<div>abc <img width=1 height=1> def", "abc  def", "Whitespace around <img> should not be collapsed"),
    ("<div><img> abc", " abc", "Leading whitesapce should not be collapsed"),
    ("<div>abc <img>", "abc ", "Trailing whitesapce should not be collapsed"),
    ("<div>abc <b></b> def", "abc def", "Whitespace around empty span should be collapsed"),
    ("<div>abc <b><i></i></b> def", "abc def", "Whitespace around empty spans should be collapsed"),
    ("<div><canvas></canvas> abc", " abc", "<canvas> should not collapse following space"),
    (
        "<div>abc <img style='display:block'> def",
        "abc\ndef",
        "Replaced element <img> with display:block should be treated as block-level",
    ),
    (
        "<div>abc <canvas style='display:block'></canvas> def",
        "abc\ndef",
        "Replaced element <canvas> with display:block should be treated as block-level",
    ),
    ("<div style='width:0'>abc def", "abc def", "Soft line breaks ignored"),
    ("<div style='width:0'>abc-def", "abc-def", "Soft line break at hyphen ignored"),
    ("<div style='width:0'><span>abc</span> <span>def</span>", "abc def", "Whitespace text node preserved"),
    (
        "<div style='width:1px; word-break:break-word'>Hello Kitty</div>",
        "Hello Kitty",
        "Soft breaks ignored in presence of word-break:break-word",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello</x> <x>Kitty</x></div>",
        "Hello Kitty",
        "Element boundaries ignored for soft break handling (1)",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello</x> <x> Kitty</x></div>",
        "Hello Kitty",
        "Whitespace collapses across element boundaries at soft break (1)",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello</x><x> Kitty</x></div>",
        "Hello Kitty",
        "Element boundaries ignored for soft break handling (2)",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello </x> <x>Kitty</x></div>",
        "Hello Kitty",
        "Whitespace collapses across element boundaries at soft break (2)",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello </x><x>Kitty</x></div>",
        "Hello Kitty",
        "Element boundaries ignored for soft break handling (3)",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello </x><x> Kitty</x></div>",
        "Hello Kitty",
        "Whitespace collapses across element boundaries at soft break (3)",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello </x> <x> Kitty</x></div>",
        "Hello Kitty",
        "Whitespace collapses across element boundaries at soft break (4)",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello</x> Kitty</div>",
        "Hello Kitty",
        "Element boundaries ignored for soft break handling (4)",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello </x>Kitty</div>",
        "Hello Kitty",
        "Element boundaries ignored for soft break handling (5)",
    ),
    (
        "<div style='width:1px; word-break:break-word; text-transform:uppercase'>Hello Kitty</div>",
        "HELLO KITTY",
        "Soft breaks ignored, text-transform applied",
    ),
    (
        "<div style='width:1px; word-break:break-word'>Hello<br> Kitty</div>",
        "Hello\nKitty",
        "<br> returned as newline, following space collapsed",
    ),
    (
        "<div style='width:1px; word-break:break-word'>Hello <br>Kitty</div>",
        "Hello\nKitty",
        "<br> returned as newline, preceding space collapsed",
    ),
    (
        "<div style='width:1px; word-break:break-word'><x>Hello </x> <br> <x> Kitty</x></div>",
        "Hello\nKitty",
        "<br> returned as newline, adjacent spaces collapsed across element boundaries",
    ),
    ("<div class='first-letter-float' style='width:0'>abc def", "abc def", "::first-letter float ignored"),
    ("<div>&nbsp;", "\xa0", "&nbsp; preserved"),
    ("<div style='display:none'>abc", "abc", "display:none container"),
    ("<div style='display:none'>abc  def", "abc  def", "No whitespace compression in display:none container"),
    (
        "<div style='display:none'> abc def ",
        " abc def ",
        "No removal of leading/trailing whitespace in display:none container",
    ),
    ("<div>123<span style='display:none'>abc", "123", "display:none child not rendered"),
    ("<div>123<p style='display:none'>abc", "123", "display:none p child not rendered"),
    (
        "<div style='display:none'><span id='target'>abc",
        "abc",
        "display:none container with non-display-none target child",
    ),
    (
        "<div style='display:none'><p id='target'>abc",
        "abc",
        "display:none container with non-display-none p target child",
    ),
    ("<div style='display:contents'>abc", "abc", "display:contents container"),
    ("<div><div style='display:contents'>abc", "abc", "display:contents container"),
    ("<div>123<span style='display:contents'>abc", "123abc", "display:contents rendered"),
    ("<div style='display:contents'>   ", "", "display:contents not processed via textContent"),
    ("<div><div style='display:contents'>   ", "", "display:contents not processed via textContent"),
    ("<div style='visibility:hidden'>abc", "", "visibility:hidden container"),
    ("<div>123<span style='visibility:hidden'>abc", "123", "visibility:hidden child not rendered"),
    (
        "<div style='visibility:hidden'>123<span style='visibility:visible'>abc",
        "abc",
        "visibility:visible child rendered",
    ),
    ("<table><tbody style='visibility:collapse'><tr><td>abc", "", "visibility:collapse row-group"),
    ("<table><tr style='visibility:collapse'><td>abc", "", "visibility:collapse row"),
    ("<table><tr><td style='visibility:collapse'>abc", "", "visibility:collapse cell"),
    (
        "<table><tbody style='visibility:collapse'><tr><td style='visibility:visible'>abc",
        "abc",
        "visibility:collapse row-group with visible cell",
    ),
    (
        "<table><tr style='visibility:collapse'><td style='visibility:visible'>abc",
        "abc",
        "visibility:collapse row with visible cell",
    ),
    (
        "<div style='display:flex'><span style='visibility:collapse'>1</span><span>2</span></div>",
        "2",
        "visibility:collapse honored on flex item",
    ),
    (
        "<div style='display:grid'><span style='visibility:collapse'>1</span><span>2</span></div>",
        "2",
        "visibility:collapse honored on grid item",
    ),
    ("<div style='opacity:0'>abc", "abc", "opacity:0 container"),
    ("<div style='opacity:0'>abc  def", "abc def", "Whitespace compression in opacity:0 container"),
    ("<div style='opacity:0'> abc def ", "abc def", "Remove leading/trailing whitespace in opacity:0 container"),
    ("<div>123<span style='opacity:0'>abc", "123abc", "opacity:0 child rendered"),
    ("<div class='before'>", "", "Generated content not included"),
    ("<div><div class='before'>", "", "Generated content on child not included"),
    ("<button>abc", "abc", "<button> contents preserved"),
    ("<fieldset>abc", "abc", "<fieldset> contents preserved"),
    ("<fieldset><legend>abc", "abc", "<fieldset> <legend> contents preserved"),
    ("<input type='text' value='abc'>", "", "<input> contents ignored"),
    ("<textarea>abc", "", "<textarea> contents ignored"),
    ("<iframe>abc", "", "<iframe> contents ignored"),
    ("<iframe><div id='target'>abc", "", "<iframe> contents ignored"),
    ("<iframe src='data:text/html,abc'>", "", "<iframe> subdocument ignored"),
    ("<audio style='display:block'>abc", "", "<audio> contents ignored"),
    (
        "<audio style='display:block'><source id='target' class='poke' style='display:block'>",
        "abc",
        "<audio> contents ok for element not being rendered",
    ),
    (
        "<audio style='display:block'><source id='target' class='poke' style='display:none'>",
        "abc",
        "<audio> contents ok for element not being rendered",
    ),
    ("<video>abc", "", "<video> contents ignored"),
    (
        "<video style='display:block'><source id='target' class='poke' style='display:block'>",
        "abc",
        "<video> contents ok for element not being rendered",
    ),
    (
        "<video style='display:block'><source id='target' class='poke' style='display:none'>",
        "abc",
        "<video> contents ok for element not being rendered",
    ),
    ("<canvas>abc", "", "<canvas> contents ignored"),
    ("<canvas><div id='target'>abc", "abc", "<canvas><div id='target'> contents ok for element not being rendered"),
    ("<img alt='abc'>", "", "<img> alt text ignored"),
    ("<img src='about:blank' class='poke'>", "", "<img> contents ignored"),
    ("<div><svg><text>abc</text></svg></div>", "abc", "<svg> text contents preserved"),
    ("<div><svg><defs><text>abc</text></defs></svg></div>", "", "<svg><defs> text contents ignored"),
    ("<div><svg><stop>abc</stop></svg></div>", "", "<svg> non-rendered text ignored"),
    (
        "<svg><foreignObject><span id='target'>abc</span></foreignObject></svg>",
        "abc",
        "<foreignObject> contents preserved",
    ),
    ("<select size='1'><option>abc</option><option>def", "abc\ndef", "<select size='1'> contents of options preserved"),
    ("<select size='2'><option>abc</option><option>def", "abc\ndef", "<select size='2'> contents of options preserved"),
    (
        "<select size='1'><option id='target'>abc</option><option>def",
        "abc",
        "<select size='1'> contents of target option preserved",
    ),
    (
        "<select size='2'><option id='target'>abc</option><option>def",
        "abc",
        "<select size='2'> contents of target option preserved",
    ),
    ("<div>a<select></select>bc", "abc", "empty <select>"),
    ("<div>a<select><optgroup></select>bc", "a\nbc", "empty <optgroup> in <select>"),
    ("<div>a<select><option></select>bc", "a\nbc", "empty <option> in <select>"),
    ("<select class='poke'></select>", "", "<select> containing text node child"),
    ("<select><optgroup class='poke-optgroup'></select>", "", "<optgroup> containing <optgroup>"),
    ("<select><optgroup><option>abc</select>", "abc", "<optgroup> containing <option>"),
    ("<select><option class='poke-div'>123</select>", "123\nabc", "<div> in <option>"),
    ("<div>a<optgroup></optgroup>bc", "a\nbc", "empty <optgroup> in <div>"),
    ("<div>a<optgroup>123</optgroup>bc", "a\n123\nbc", "<optgroup> in <div>"),
    ("<div>a<option></option>bc", "a\nbc", "empty <option> in <div>"),
    ("<div>a<option>123</option>bc", "a\n123\nbc", "<option> in <div>"),
    ("<select><option>one</option><div><optgroup label=optgroup><div><option><span>two", "one\ntwo", ""),
    ("<div><button>abc", "abc", "<button> contents preserved"),
    ("<div><fieldset>abc", "abc", "<fieldset> contents preserved"),
    ("<div><fieldset><legend>abc", "abc", "<fieldset> <legend> contents preserved"),
    ("<div><input type='text' value='abc'>", "", "<input> contents ignored"),
    ("<div><textarea>abc", "", "<textarea> contents ignored"),
    (
        "<div><select size='1'><option>abc</option><option>def",
        "abc\ndef",
        "<select size='1'> contents of options preserved",
    ),
    (
        "<div><select size='2'><option>abc</option><option>def",
        "abc\ndef",
        "<select size='2'> contents of options preserved",
    ),
    ("<div><iframe>abc", "", "<iframe> contents ignored"),
    ("<div><iframe src='data:text/html,abc'>", "", " <iframe> subdocument ignored"),
    ("<div><audio>abc", "", "<audio> contents ignored"),
    ("<div><video>abc", "", "<video> contents ignored"),
    ("<div><canvas>abc", "", "<canvas> contents ignored"),
    ("<div><object>abc", "", "<object> contents ignored"),
    ("<div><img alt='abc'>", "", "<img> alt text ignored"),
    ("<div>123<div>abc</div>def", "123\nabc\ndef", "Newline at block boundary"),
    ("<div>123<span style='display:block'>abc</span>def", "123\nabc\ndef", "Newline at display:block boundary"),
    ("<div>abc<div></div>def", "abc\ndef", "Empty block induces single line break"),
    ("<div>abc<div></div><div></div>def", "abc\ndef", "Consecutive empty blocks ignored"),
    ("<div><p>abc", "abc", "No blank lines around <p> alone"),
    ("<div><p>abc</p> ", "abc", "No blank lines around <p> followed by only collapsible whitespace"),
    ("<div> <p>abc</p>", "abc", "No blank lines around <p> preceded by only collapsible whitespace"),
    ("<div><p>abc<p>def", "abc\n\ndef", "Blank line between consecutive <p>s"),
    (
        "<div><p>abc</p> <p>def",
        "abc\n\ndef",
        "Blank line between consecutive <p>s separated only by collapsible whitespace",
    ),
    (
        "<div><p>abc</p><div></div><p>def",
        "abc\n\ndef",
        "Blank line between consecutive <p>s separated only by empty block",
    ),
    (
        "<div><p>abc</p><div>123</div><p>def",
        "abc\n\n123\n\ndef",
        "Blank lines between <p>s separated by non-empty block",
    ),
    ("<div>abc<div><p>123</p></div>def", "abc\n\n123\n\ndef", "Blank lines around a <p> in its own block"),
    ("<div>abc<p>def", "abc\n\ndef", "Blank line before <p>"),
    ("<div><p>abc</p>def", "abc\n\ndef", "Blank line after <p>"),
    ("<div><p>abc<p></p><p></p><p>def", "abc\n\ndef", "One blank line between <p>s, ignoring empty <p>s"),
    (
        "<div style='visibility:hidden'><p><span style='visibility:visible'>abc</span></p>\n<div style='visibility:visible'>def</div>",
        "abc\ndef",
        "Invisible <p> doesn't induce extra line breaks",
    ),
    ("<div><pre>abc\n\n</pre><p>def", "abc\n\n\n\ndef", "<pre> trailing newlines don't suppress <p> blank line"),
    ("<div>abc<div style='margin:2em'>def", "abc\ndef", "No blank lines around <div> with margin"),
    (
        "<div>123<span style='display:inline-block'>abc</span>def",
        "123abcdef",
        "No newlines at display:inline-block boundary",
    ),
    (
        "<div>123<span style='display:inline-block'> abc </span>def",
        "123abcdef",
        "Leading/trailing space removal at display:inline-block boundary",
    ),
    (
        "<div>123<span style='display:inline-flex'> abc </span>def",
        "123abcdef",
        "Leading/trailing space removal at display:inline-flex boundary",
    ),
    (
        "<div>123<span style='display:inline-grid'> abc </span>def",
        "123abcdef",
        "Leading/trailing space removal at display:inline-grid boundary",
    ),
    ("<div>123<p style='margin:0px'>abc</p>def", "123\n\nabc\n\ndef", "Blank lines around <p> even without margin"),
    ("<div>123<h1>abc</h1>def", "123\nabc\ndef", "No blank lines around <h1>"),
    ("<div>123<h2>abc</h2>def", "123\nabc\ndef", "No blank lines around <h2>"),
    ("<div>123<h3>abc</h3>def", "123\nabc\ndef", "No blank lines around <h3>"),
    ("<div>123<h4>abc</h4>def", "123\nabc\ndef", "No blank lines around <h4>"),
    ("<div>123<h5>abc</h5>def", "123\nabc\ndef", "No blank lines around <h5>"),
    ("<div>123<h6>abc</h6>def", "123\nabc\ndef", "No blank lines around <h6>"),
    ("<div>123<p style='display:block'>abc", "123\n\nabc", "2 blank lines around <p> even when display:block"),
    (
        "<div>123<p style='display:inline-block'>abc",
        "123\n\nabc",
        "2 blank lines around <p> even when display:inline-block",
    ),
    ("<div>123<span>abc</span>def", "123abcdef", "<span> boundaries are irrelevant"),
    ("<div>123 <span>abc</span> def", "123 abc def", "<span> boundaries are irrelevant"),
    ("<div style='width:0'>123 <span>abc</span> def", "123 abc def", "<span> boundaries are irrelevant"),
    ("<div>123<em>abc</em>def", "123abcdef", "<em> gets no special treatment"),
    ("<div>123<b>abc</b>def", "123abcdef", "<b> gets no special treatment"),
    ("<div>123<i>abc</i>def", "123abcdef", "<i> gets no special treatment"),
    ("<div>123<strong>abc</strong>def", "123abcdef", "<strong> gets no special treatment"),
    ("<div>123<tt>abc</tt>def", "123abcdef", "<tt> gets no special treatment"),
    ("<div>123<code>abc</code>def", "123abcdef", "<code> gets no special treatment"),
    ("<div>abc&shy;def", "abc\xaddef", "soft hyphen preserved"),
    ("<div style='width:0'>abc&shy;def", "abc\xaddef", "soft hyphen preserved"),
    ("<div><table style='white-space:pre'>  <td>abc</td>  </table>", "abc", "Ignoring non-rendered table whitespace"),
    ("<div><table><tr><td>abc<td>def</table>", "abc\tdef", "Tab-separated table cells"),
    ("<div><table><tr><td>abc<td><td>def</table>", "abc\t\tdef", "Tab-separated table cells including empty cells"),
    ("<div><table><tr><td>abc<td><td></table>", "abc\t\t", "Tab-separated table cells including trailing empty cells"),
    ("<div><table><tr><td>abc<tr><td>def</table>", "abc\ndef", "Newline-separated table rows"),
    ("<div>abc<table><td>def</table>ghi", "abc\ndef\nghi", "Newlines around table"),
    (
        "<div><table style='border-collapse:collapse'><tr><td>abc<td>def</table>",
        "abc\tdef",
        "Tab-separated table cells in a border-collapse table",
    ),
    ("<div><table><tfoot>x</tfoot><tbody>y</tbody></table>", "xy", "tfoot not reordered"),
    (
        "<table><tfoot><tr><td>footer</tfoot><thead><tr><td style='visibility:collapse'>thead</thead><tbody><tr><td>tbody</tbody></table>",
        "footer\n\ntbody",
        "",
    ),
    ("<table><tr><td id=target>abc</td><td>def</td>", "abc", "No tab on table-cell itself"),
    (
        "<table><tr id=target><td>abc</td><td>def</td></tr><tr id=target><td>ghi</td><td>jkl</td></tr>",
        "abc\tdef",
        "No newline on table-row itself",
    ),
    ("<div><table><tr><td>abc<caption>def</caption></table>", "abc\ndef", "Newline between cells and caption"),
    (
        "<div><div class='table'><span class='cell'>abc</span>\n<span class='cell'>def</span></div>",
        "abc\tdef",
        "Tab-separated table cells",
    ),
    (
        "<div><div class='table'><span class='row'><span class='cell'>abc</span></span>\n<span class='row'><span class='cell'>def</span></span></div>",
        "abc\ndef",
        "Newline-separated table rows",
    ),
    ("<div>abc<div class='table'><span class='cell'>def</span></div>ghi", "abc\ndef\nghi", "Newlines around table"),
    (
        "<div><div class='itable'><span class='cell'>abc</span>\n<span class='cell'>def</span></div>",
        "abc\tdef",
        "Tab-separated table cells",
    ),
    (
        "<div><div class='itable'><span class='row'><span class='cell'>abc</span></span>\n<span class='row'><span class='cell'>def</span></span></div>",
        "abc\ndef",
        "Newline-separated table rows",
    ),
    (
        "<div>abc<div class='itable'><span class='cell'>def</span></div>ghi",
        "abcdefghi",
        "No newlines around inline-table",
    ),
    (
        "<div>abc<div class='itable'><span class='row'><span class='cell'>def</span></span>\n<span class='row'><span class='cell'>123</span></span></div>ghi",
        "abcdef\n123ghi",
        "Single newline in two-row inline-table",
    ),
    ("<div style='display:table-row'>", "", "display:table-row on the element itself"),
    ("<div style='display:table-cell'>", "", "display:table-cell on the element itself"),
    ("<div style='display:table-caption'>", "", "display:table-caption on the element itself"),
    ("<div><ol><li>abc", "abc", "<ol> list items get no special treatment"),
    ("<div><ul><li>abc", "abc", "<ul> list items get no special treatment"),
    ("<div><noscript style='display:block'>abc", "", "display:block <noscript> is not rendered (it's not parsed!)"),
    (
        "<div><template style='display:block'>abc",
        "",
        "display:block <template> contents are not rendered (the contents are in a different document)",
    ),
    ("<div>abc<br>def", "abc\ndef", "<br> induces line break"),
    ("<div>abc<br>", "abc\n", "<br> induces line break even at end of block"),
    ("<div><br class='poke'>", "\n", "<br> content ignored"),
    ("<div>abc<hr>def", "abc\ndef", "<hr> induces line break"),
    ("<div>abc<hr><hr>def", "abc\ndef", "<hr><hr> induces just one line break"),
    ("<div>abc<hr><hr><hr>def", "abc\ndef", "<hr><hr><hr> induces just one line break"),
    ("<div><hr class='poke'>", "abc", "<hr> content rendered"),
    ("<div>abc<!--comment-->def", "abcdef", "comment ignored"),
    ("<br>", "", "<br>"),
    ("<p>", "", "empty <p>"),
    ("<div>", "", "empty <div>"),
    ("<div><details><summary>abc</summary>123", "abc", "unopened <details> ignored"),
    ("<div><details open><summary>abc</summary>123", "abc\n123", "opened <details> content shown"),
    ("<div><div style='text-transform:uppercase'>abc", "ABC", "text-transform is applied"),
    ("<div><div style='text-transform:uppercase'>Maß", "MASS", "text-transform handles es-zet"),
    ("<div><div lang='tr' style='text-transform:uppercase'>i ı", "İ I", "text-transform handles Turkish casing"),
    (
        "<div>abc<span>123<div>456</div>789</span>def",
        "abc123\n456\n789def",
        "block-in-inline doesn't add unnecessary newlines",
    ),
    ("<div>abc<div style='float:left'>123</div>def", "abc\n123\ndef", "floats induce a block boundary"),
    ("<div>abc<span style='float:left'>123</span>def", "abc\n123\ndef", "floats induce a block boundary"),
    ("<div style='float:left'>123", "123", "float on the element itself"),
    (
        "<div>abc<div style='position:absolute'>123</div>def",
        "abc\n123\ndef",
        "position:absolute induces a block boundary",
    ),
    (
        "<div>abc<span style='position:absolute'>123</span>def",
        "abc\n123\ndef",
        "position:absolute induces a block boundary",
    ),
    ("<div style='position:absolute'>123", "123", "position:absolute on the element itself"),
    ("<div>abc<div style='position:relative'>123</div>def", "abc\n123\ndef", "position:relative has no effect"),
    ("<div>abc<span style='position:relative'>123</span>def", "abc123def", "position:relative has no effect"),
    ("<div style='overflow:hidden'>abc", "abc", "overflow:hidden ignored"),
    ("<div style='width:0; overflow:hidden'>abc", "abc", "overflow:hidden ignored even with zero width"),
    ("<div style='height:0; overflow:hidden'>abc", "abc", "overflow:hidden ignored even with zero height"),
    ("<div style='width:0; overflow:hidden; text-overflow:ellipsis'>abc", "abc", "text-overflow:ellipsis ignored"),
    ("<div><ruby>abc<rt>def</rt></ruby>", "abcdef", "<rt> and no <rp>"),
    ("<div><ruby>abc<rp>(</rp><rt>def</rt><rp>)</rp></ruby>", "abcdef", "<rp>"),
    ("<div><rp>abc</rp>", "", "Lone <rp>"),
    ("<div><rp style='visibility:hidden'>abc</rp>", "", "visibility:hidden <rp>"),
    ("<div><rp style='display:block'>abc</rp>def", "abc\ndef", "display:block <rp>"),
    ("<div><rp style='display:block'> abc </rp>def", "abc\ndef", "display:block <rp> with whitespace"),
    ("<div><select class='poke-rp'></select>", "", "<rp> in a <select>"),
    ("<div class='shadow'>", "", "Shadow DOM contents ignored"),
    ("<div><div class='shadow'>", "", "Shadow DOM contents ignored"),
    (
        "<div style='display:flex'><div style='order:1'>1</div><div>2</div></div>",
        "1\n2",
        "CSS 'order' property ignored",
    ),
    ("<div style='display:flex'><span>1</span><span>2</span></div>", "1\n2", "Flex items blockified"),
    (
        "<div style='display:grid'><div style='order:1'>1</div><div>2</div></div>",
        "1\n2",
        "CSS 'order' property ignored",
    ),
    ("<div style='display:grid'><span>1</span><span>2</span></div>", "1\n2", "Grid items blockified"),
]

SVG_CASES = [
    ("<div id='target'>abc", "abc", "non-display-none child of svg"),
    ("<div style='display:none' id='target'>abc", "abc", "display:none child of svg"),
    ("<div style='display:none'><div id='target'>abc", "abc", "child of display:none child of svg"),
]


def text_of(html, in_svg=False):
    """getter.html's textTextInContainer(): ``(innerText, outerText)`` of the target."""
    document = DOMParser().parseFromString(PAGE, "text/html")
    container = document.getElementById("container")
    holder = document.getElementById("svgContainer") if in_svg else container
    container.innerHTML = html
    if holder is not container:
        while container.firstChild is not None:
            holder.appendChild(container.firstChild)
    target = document.getElementById("target") or holder.firstChild
    for poke in list(document.getElementsByClassName("poke")):
        poke.textContent = "abc"
    for tag in ("rp", "optgroup", "div"):
        for poke in list(document.getElementsByClassName("poke-" + tag)):
            child = document.createElement(tag)
            child.textContent = "abc"
            poke.appendChild(child)
    for host in list(document.getElementsByClassName("shadow")):
        host.attachShadow({"mode": "open"}).textContent = "abc"
    while target is not None and not isinstance(target, Element):
        target = target.nextSibling
    return target.innerText, target.outerText


class TestInnerTextGetter(unittest.TestCase):
    def test_getter(self):
        for html, expected, name in CASES:
            with self.subTest(name=name, html=html):
                self.assertEqual(text_of(html), (expected, expected))

    def test_getter_in_svg(self):
        for html, expected, name in SVG_CASES:
            with self.subTest(name=name, html=html):
                self.assertEqual(text_of(html, in_svg=True), (expected, expected))


class KnownDeviations(unittest.TestCase):
    @pytest.mark.xfail(reason="::first-line / ::first-letter need line layout", strict=True)
    def test_first_line_uppercase(self):
        self.assertEqual(text_of("<div class='first-line-uppercase'>abc")[0], "ABC")

    @pytest.mark.xfail(reason="::first-line / ::first-letter need line layout", strict=True)
    def test_first_letter_uppercase(self):
        self.assertEqual(text_of("<div class='first-letter-uppercase' style='width:0'>abc def")[0], "Abc def")

    @pytest.mark.xfail(
        reason="innerHTML parses its value inside a <div>...</div> wrapper, so an unclosed <script>/<style> "
        "keeps the wrapper's </div> as text",
        strict=True,
    )
    def test_display_block_script(self):
        self.assertEqual(text_of("<div><script style='display:block'>abc")[0], "abc")

    @pytest.mark.xfail(reason="domonic defines innerText on every Element, not only HTML elements", strict=True)
    def test_not_on_svg_elements(self):
        svg = DOMParser().parseFromString("<svg>abc</svg>", "text/html").querySelector("svg")
        self.assertFalse(hasattr(svg, "innerText"))  # upstream: undefined


if __name__ == "__main__":
    unittest.main()
