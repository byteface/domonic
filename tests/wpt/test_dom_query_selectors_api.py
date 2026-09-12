"""Ported from the Selectors-API conformance suite: wpt/dom/nodes/selectors.js
+ ParentNode-querySelector-All.js + ParentNode-querySelector-All-content.html.
https://dom.spec.whatwg.org/#dom-parentnode-queryselector

The upstream suite drives the same selector table through four contexts
(document, in-document element, detached element, fragment) and two methods
(querySelector/querySelectorAll, matches -- and the never-shipped, proprietary
find()/findAll()). This port keeps only the "in-document element" context
against an HTML document -- calling ``#root.querySelectorAll(...)`` -- which is
how domonic is actually used; ``matches()`` already has its own port in
test_dom_matches_closest.py.

VALID_SELECTORS_QSA is selectors.js's ``validSelectors``, filtered to the rows
applicable here (``testType & TEST_QSA``, not excluded for "element"/"html")
and to selectors that were not themselves commented out upstream (the ``>>``
descendant-combinator proposal was dropped from the spec and its rows are
commented out in the source). A handful of remaining rows are real, tracked
domonic deviations -- see KnownDeviations below -- and are excluded from the
table instead of asserted twice.
"""

import unittest

import pytest

from domonic import domonic

# wpt/dom/nodes/ParentNode-querySelector-All-content.html, trimmed of nothing
# but the outer iframe-loading harness (the suite loads this as a child
# document; domonic just parses it directly).
FIXTURE_HTML = """<!DOCTYPE html>
<html id="html" lang="en">
<head id="head">
  <meta id="meta" charset="UTF-8">
  <title id="title">Selectors-API Test Suite: HTML with Selectors Level 2 using TestHarness: Test Document</title>

  <!-- Links for :link and :visited pseudo-class test -->
  <link id="pseudo-link-link1" href="">
  <link id="pseudo-link-link2" href="http://example.org/">
  <link id="pseudo-link-link3">
  <style>
  @namespace ns "http://www.w3.org/1999/xhtml";
   /* Declare the namespace prefix used in tests. This declaration should not be used by the API. */
  </style>
</head>
<body id="body">
<div id="root">
  <div id="target"></div>

  <div id="universal">
    <p id="universal-p1">Universal selector tests inside element with <code id="universal-code1">id="universal"</code>.</p>
    <hr id="universal-hr1">
    <pre id="universal-pre1">Some preformatted text with some <span id="universal-span1">embedded code</span></pre>
    <p id="universal-p2">This is a normal link: <a id="universal-a1" href="http://www.w3.org/">W3C</a></p>
    <address id="universal-address1">Some more nested elements <code id="universal-code2"><a href="#" id="universal-a2">code hyperlink</a></code></address>
  </div>

  <div id="attr-presence">
    <div class="attr-presence-div1" id="attr-presence-div1" align="center"></div>
    <div class="attr-presence-div2" id="attr-presence-div2" align=""></div>
    <div class="attr-presence-div3" id="attr-presence-div3" valign="center"></div>
    <div class="attr-presence-div4" id="attr-presence-div4" alignv="center"></div>
    <p id="attr-presence-p1"><a  id="attr-presence-a1" tItLe=""></a><span id="attr-presence-span1" TITLE="attr-presence-span1"></span><i id="attr-presence-i1"></i></p>
    <pre id="attr-presence-pre1" data-attr-presence="pre1"></pre>
    <blockquote id="attr-presence-blockquote1" data-attr-presence="blockquote1"></blockquote>
    <ul id="attr-presence-ul1" data-中文=""></ul>

    <select id="attr-presence-select1">
      <option id="attr-presence-select1-option1">A</option>
      <option id="attr-presence-select1-option2">B</option>
      <option id="attr-presence-select1-option3">C</option>
      <option id="attr-presence-select1-option4">D</option>
    </select>
    <select id="attr-presence-select2">
      <option id="attr-presence-select2-option1">A</option>
      <option id="attr-presence-select2-option2">B</option>
      <option id="attr-presence-select2-option3">C</option>
      <option id="attr-presence-select2-option4" selected="selected">D</option>
    </select>
    <select id="attr-presence-select3" multiple="multiple">
      <option id="attr-presence-select3-option1">A</option>
      <option id="attr-presence-select3-option2" selected="">B</option>
      <option id="attr-presence-select3-option3" selected="selected">C</option>
      <option id="attr-presence-select3-option4">D</option>
    </select>
  </div>

  <div id="attr-value">
    <div id="attr-value-div1" align="center"></div>
      <div id="attr-value-div2" align=""></div>
      <div id="attr-value-div3" data-attr-value="&#xE9;"></div>
      <div id="attr-value-div4" data-attr-value_foo="&#xE9;"></div>

    <form id="attr-value-form1">
      <input id="attr-value-input1" type="text">
      <input id="attr-value-input2" type="password">
      <input id="attr-value-input3" type="hidden">
      <input id="attr-value-input4" type="radio">
      <input id="attr-value-input5" type="checkbox">
      <input id="attr-value-input6" type="radio">
      <input id="attr-value-input7" type="text">
      <input id="attr-value-input8" type="hidden">
      <input id="attr-value-input9" type="radio">
    </form>

    <div id="attr-value-div5" data-attr-value="中文"></div>
  </div>

  <div id="attr-whitespace">
    <div id="attr-whitespace-div1" class="foo div1 bar"></div>
      <div id="attr-whitespace-div2" class=""></div>
      <div id="attr-whitespace-div3" class="foo div3 bar"></div>

      <div id="attr-whitespace-div4" data-attr-whitespace="foo &#xE9; bar"></div>
      <div id="attr-whitespace-div5" data-attr-whitespace_foo="&#xE9; foo"></div>

    <a id="attr-whitespace-a1" rel="next bookmark"></a>
    <a id="attr-whitespace-a2" rel="tag nofollow"></a>
    <a id="attr-whitespace-a3" rel="tag bookmark"></a>
    <a id="attr-whitespace-a4" rel="book mark"></a> <!-- Intentional space in "book mark" -->
    <a id="attr-whitespace-a5" rel="nofollow"></a>
    <a id="attr-whitespace-a6" rev="bookmark nofollow"></a>
    <a id="attr-whitespace-a7" rel="prev next tag alternate nofollow author help icon noreferrer prefetch search stylesheet tag"></a>

    <p id="attr-whitespace-p1" title="Chinese 中文 characters"></p>
  </div>

  <div id="attr-hyphen">
    <div id="attr-hyphen-div1"></div>
      <div id="attr-hyphen-div2" lang="fr"></div>
      <div id="attr-hyphen-div3" lang="en-AU"></div>
      <div id="attr-hyphen-div4" lang="es"></div>
  </div>

  <div id="attr-begins">
    <a id="attr-begins-a1" href="http://www.example.org"></a>
    <a id="attr-begins-a2" href="http://example.org/"></a>
    <a id="attr-begins-a3" href="http://www.example.com/"></a>

      <div id="attr-begins-div1" lang="fr"></div>
      <div id="attr-begins-div2" lang="en-AU"></div>
      <div id="attr-begins-div3" lang="es"></div>
      <div id="attr-begins-div4" lang="en-US"></div>
      <div id="attr-begins-div5" lang="en"></div>

    <p id="attr-begins-p1" class=" apple"></p> <!-- Intentional space in class value " apple". -->
  </div>

  <div id="attr-ends">
    <a id="attr-ends-a1" href="http://www.example.org"></a>
    <a id="attr-ends-a2" href="http://example.org/"></a>
    <a id="attr-ends-a3" href="http://www.example.org"></a>

      <div id="attr-ends-div1" lang="fr"></div>
      <div id="attr-ends-div2" lang="de-CH"></div>
      <div id="attr-ends-div3" lang="es"></div>
      <div id="attr-ends-div4" lang="fr-CH"></div>

    <p id="attr-ends-p1" class="apple "></p> <!-- Intentional space in class value "apple ". -->
  </div>

  <div id="attr-contains">
    <a id="attr-contains-a1" href="http://www.example.org"></a>
    <a id="attr-contains-a2" href="http://example.org/"></a>
    <a id="attr-contains-a3" href="http://www.example.com/"></a>

      <div id="attr-contains-div1" lang="fr"></div>
      <div id="attr-contains-div2" lang="en-AU"></div>
      <div id="attr-contains-div3" lang="de-CH"></div>
      <div id="attr-contains-div4" lang="es"></div>
      <div id="attr-contains-div5" lang="fr-CH"></div>
      <div id="attr-contains-div6" lang="en-US"></div>

    <p id="attr-contains-p1" class=" apple banana orange "></p>
  </div>

  <div id="pseudo-nth">
    <table id="pseudo-nth-table1">
      <tr id="pseudo-nth-tr1"><td id="pseudo-nth-td1"></td><td id="pseudo-nth-td2"></td><td id="pseudo-nth-td3"></td><td id="pseudo-nth-td4"></td><td id="pseudo-nth--td5"></td><td id="pseudo-nth-td6"></td></tr>
      <tr id="pseudo-nth-tr2"><td id="pseudo-nth-td7"></td><td id="pseudo-nth-td8"></td><td id="pseudo-nth-td9"></td><td id="pseudo-nth-td10"></td><td id="pseudo-nth-td11"></td><td id="pseudo-nth-td12"></td></tr>
      <tr id="pseudo-nth-tr3"><td id="pseudo-nth-td13"></td><td id="pseudo-nth-td14"></td><td id="pseudo-nth-td15"></td><td id="pseudo-nth-td16"></td><td id="pseudo-nth-td17"></td><td id="pseudo-nth-td18"></td></tr>
    </table>

    <ol id="pseudo-nth-ol1">
      <li id="pseudo-nth-li1"></li>
      <li id="pseudo-nth-li2"></li>
      <li id="pseudo-nth-li3"></li>
      <li id="pseudo-nth-li4"></li>
      <li id="pseudo-nth-li5"></li>
      <li id="pseudo-nth-li6"></li>
      <li id="pseudo-nth-li7"></li>
      <li id="pseudo-nth-li8"></li>
      <li id="pseudo-nth-li9"></li>
      <li id="pseudo-nth-li10"></li>
      <li id="pseudo-nth-li11"></li>
      <li id="pseudo-nth-li12"></li>
    </ol>

    <p id="pseudo-nth-p1">
      <span id="pseudo-nth-span1">span1</span>
      <em id="pseudo-nth-em1">em1</em>
      <!-- comment node-->
      <em id="pseudo-nth-em2">em2</em>
      <span id="pseudo-nth-span2">span2</span>
      <strong id="pseudo-nth-strong1">strong1</strong>
      <em id="pseudo-nth-em3">em3</em>
      <span id="pseudo-nth-span3">span3</span>
      <span id="pseudo-nth-span4">span4</span>
      <strong id="pseudo-nth-strong2">strong2</strong>
      <em id="pseudo-nth-em4">em4</em>
    </p>
  </div>

  <div id="pseudo-first-child">
    <div id="pseudo-first-child-div1"></div>
    <div id="pseudo-first-child-div2"></div>
    <div id="pseudo-first-child-div3"></div>

    <p id="pseudo-first-child-p1"><span id="pseudo-first-child-span1"></span><span id="pseudo-first-child-span2"></span></p>
    <p id="pseudo-first-child-p2"><span id="pseudo-first-child-span3"></span><span id="pseudo-first-child-span4"></span></p>
    <p id="pseudo-first-child-p3"><span id="pseudo-first-child-span5"></span><span id="pseudo-first-child-span6"></span></p>
  </div>

  <div id="pseudo-last-child">
    <p id="pseudo-last-child-p1"><span id="pseudo-last-child-span1"></span><span id="pseudo-last-child-span2"></span></p>
    <p id="pseudo-last-child-p2"><span id="pseudo-last-child-span3"></span><span id="pseudo-last-child-span4"></span></p>
    <p id="pseudo-last-child-p3"><span id="pseudo-last-child-span5"></span><span id="pseudo-last-child-span6"></span></p>

    <div id="pseudo-last-child-div1"></div>
    <div id="pseudo-last-child-div2"></div>
    <div id="pseudo-last-child-div3"></div>
  </div>

  <div id="pseudo-only">
    <p id="pseudo-only-p1">
      <span id="pseudo-only-span1"></span>
    </p>
    <p id="pseudo-only-p2">
      <span id="pseudo-only-span2"></span>
      <span id="pseudo-only-span3"></span>
    </p>
    <p id="pseudo-only-p3">
      <span id="pseudo-only-span4"></span>
      <em id="pseudo-only-em1"></em>
      <span id="pseudo-only-span5"></span>
    </p>
  </div>

  <div id="pseudo-empty">
    <p id="pseudo-empty-p1"></p>
    <p id="pseudo-empty-p2"><!-- comment node --></p>
    <p id="pseudo-empty-p3"> </p>
    <p id="pseudo-empty-p4">Text node</p>
    <p id="pseudo-empty-p5"><span id="pseudo-empty-span1"></span></p>
  </div>

  <div id="pseudo-link">
    <a id="pseudo-link-a1" href="">with href</a>
    <a id="pseudo-link-a2" href="http://example.org/">with href</a>
    <a id="pseudo-link-a3">without href</a>
    <map name="pseudo-link-map1" id="pseudo-link-map1">
      <area id="pseudo-link-area1" href="">
      <area id="pseudo-link-area2">
    </map>
  </div>

  <div id="pseudo-lang">
    <div id="pseudo-lang-div1"></div>
      <div id="pseudo-lang-div2" lang="fr"></div>
      <div id="pseudo-lang-div3" lang="en-AU"></div>
      <div id="pseudo-lang-div4" lang="es"></div>
  </div>

  <div id="pseudo-ui">
    <input id="pseudo-ui-input1" type="text">
    <input id="pseudo-ui-input2" type="password">
    <input id="pseudo-ui-input3" type="radio">
    <input id="pseudo-ui-input4" type="radio" checked="checked">
    <input id="pseudo-ui-input5" type="checkbox">
    <input id="pseudo-ui-input6" type="checkbox" checked="checked">
    <input id="pseudo-ui-input7" type="submit">
    <input id="pseudo-ui-input8" type="button">
    <input id="pseudo-ui-input9" type="hidden">
    <textarea id="pseudo-ui-textarea1"></textarea>
    <button id="pseudo-ui-button1">Enabled</button>

    <input id="pseudo-ui-input10" disabled="disabled" type="text">
    <input id="pseudo-ui-input11" disabled="disabled" type="password">
    <input id="pseudo-ui-input12" disabled="disabled" type="radio">
    <input id="pseudo-ui-input13" disabled="disabled" type="radio" checked="checked">
    <input id="pseudo-ui-input14" disabled="disabled" type="checkbox">
    <input id="pseudo-ui-input15" disabled="disabled" type="checkbox" checked="checked">
    <input id="pseudo-ui-input16" disabled="disabled" type="submit">
    <input id="pseudo-ui-input17" disabled="disabled" type="button">
    <input id="pseudo-ui-input18" disabled="disabled" type="hidden">
    <textarea id="pseudo-ui-textarea2" disabled="disabled"></textarea>
    <button id="pseudo-ui-button2" disabled="disabled">Disabled</button>
  </div>

  <div id="not">
    <div id="not-div1"></div>
    <div id="not-div2"></div>
    <div id="not-div3"></div>

    <p id="not-p1"><span id="not-span1"></span><em id="not-em1"></em></p>
    <p id="not-p2"><span id="not-span2"></span><em id="not-em2"></em></p>
    <p id="not-p3"><span id="not-span3"></span><em id="not-em3"></em></p>
  </div>

  <div id="pseudo-element">All pseudo-element tests</div>

  <div id="class">
    <p id="class-p1" class="foo class-p bar"></p>
    <p id="class-p2" class="class-p foo bar"></p>
    <p id="class-p3" class="foo bar class-p"></p>

    <!-- All permutations of the classes should match -->
    <div id="class-div1" class="apple orange banana"></div>
    <div id="class-div2" class="apple banana orange"></div>
    <p id="class-p4" class="orange apple banana"></p>
    <div id="class-div3" class="orange banana apple"></div>
    <p id="class-p6" class="banana apple orange"></p>
    <div id="class-div4" class="banana orange apple"></div>
    <div id="class-div5" class="apple orange"></div>
    <div id="class-div6" class="apple banana"></div>
    <div id="class-div7" class="orange banana"></div>

    <span id="class-span1" class="台北Táiběi 台北"></span>
    <span id="class-span2" class="台北"></span>

    <span id="class-span3" class="foo:bar"></span>
    <span id="class-span4" class="test.foo[5]bar"></span>
  </div>

  <div id="id">
    <div id="id-div1"></div>
    <div id="id-div2"></div>

    <ul id="id-ul1">
      <li id="id-li-duplicate"></li>
      <li id="id-li-duplicate"></li>
      <li id="id-li-duplicate"></li>
      <li id="id-li-duplicate"></li>
    </ul>

    <span id="台北Táiběi"></span>
    <span id="台北"></span>

    <span id="#foo:bar"></span>
    <span id="test.foo[5]bar"></span>
  </div>

  <div id="descendant">
    <div id="descendant-div1" class="descendant-div1">
      <div id="descendant-div2" class="descendant-div2">
        <div id="descendant-div3" class="descendant-div3">
        </div>
      </div>
    </div>
    <div id="descendant-div4" class="descendant-div4"></div>
  </div>

  <div id="child">
    <div id="child-div1" class="child-div1">
      <div id="child-div2" class="child-div2">
        <div id="child-div3" class="child-div3">
        </div>
      </div>
    </div>
    <div id="child-div4" class="child-div4"></div>
  </div>

  <div id="adjacent">
    <div id="adjacent-div1" class="adjacent-div1"></div>
    <div id="adjacent-div2" class="adjacent-div2">
      <div id="adjacent-div3" class="adjacent-div3"></div>
    </div>
    <div id="adjacent-div4" class="adjacent-div4">
      <p id="adjacent-p1" class="adjacent-p1"></p>
      <div id="adjacent-div5" class="adjacent-div5"></div>
    </div>
    <div id="adjacent-div6" class="adjacent-div6"></div>
    <p id="adjacent-p2" class="adjacent-p2"></p>
    <p id="adjacent-p3" class="adjacent-p3"></p>
  </div>

  <div id="sibling">
    <div id="sibling-div1" class="sibling-div"></div>
    <div id="sibling-div2" class="sibling-div">
      <div id="sibling-div3" class="sibling-div"></div>
    </div>
    <div id="sibling-div4" class="sibling-div">
      <p id="sibling-p1" class="sibling-p"></p>
      <div id="sibling-div5" class="sibling-div"></div>
    </div>
    <div id="sibling-div6" class="sibling-div"></div>
    <p id="sibling-p2" class="sibling-p"></p>
    <p id="sibling-p3" class="sibling-p"></p>
  </div>

  <div id="group">
    <em id="group-em1"></em>
    <strong id="group-strong1"></strong>
  </div>
</div>
</body>
</html>
"""

document = domonic.parseString(FIXTURE_HTML, parser="html5lib", document=True)
ROOT = document.getElementById("root")

# setupSpecialElements() in the upstream JS harness gives this element a
# namespaced "title" attribute via setAttributeNS(), to test attribute-name
# case sensitivity. domonic's setAttributeNS() does not track namespaces (a
# known deviation, see KnownDeviations.test_namespace_selectors below), so it
# lands as a plain "title" attribute -- reproducing that end state here
# reproduces the upstream row's fixture exactly.
document.getElementById("attr-presence-i1").setAttributeNS("http://www.example.org/ns", "title", "")

# (name, selector, expected ids in tree order) -- ported from selectors.js
# `validSelectors`.
VALID_SELECTORS_QSA = [
    ("Type selector, matching html element", "html", []),
    ("Type selector, matching body element", "body", []),
    (
        "Universal selector, matching all children of element with specified ID",
        "#universal>*",
        ["universal-p1", "universal-hr1", "universal-pre1", "universal-p2", "universal-address1"],
    ),
    (
        "Universal selector, matching all grandchildren of element with specified ID",
        "#universal>*>*",
        ["universal-code1", "universal-span1", "universal-a1", "universal-code2"],
    ),
    ("Universal selector, matching all children of empty element with specified ID", "#empty>*", []),
    (
        "Universal selector, matching all descendants of element with specified ID",
        "#universal *",
        [
            "universal-p1",
            "universal-code1",
            "universal-hr1",
            "universal-pre1",
            "universal-span1",
            "universal-p2",
            "universal-a1",
            "universal-address1",
            "universal-code2",
            "universal-a2",
        ],
    ),
    (
        "Attribute presence selector, matching align attribute with value",
        ".attr-presence-div1[align]",
        ["attr-presence-div1"],
    ),
    (
        "Attribute presence selector, matching align attribute with empty value",
        ".attr-presence-div2[align]",
        ["attr-presence-div2"],
    ),
    (
        "Attribute presence selector, matching title attribute, case insensitivity",
        "#attr-presence [*|TiTlE]",
        ["attr-presence-a1", "attr-presence-span1", "attr-presence-i1"],
    ),
    (
        "Attribute presence selector, matching custom data-* attribute",
        "[data-attr-presence]",
        ["attr-presence-pre1", "attr-presence-blockquote1"],
    ),
    (
        "Attribute presence selector, not matching attribute with similar name",
        ".attr-presence-div3[align], .attr-presence-div4[align]",
        [],
    ),
    (
        "Attribute presence selector, matching attribute with non-ASCII characters",
        "ul[data-中文]",
        ["attr-presence-ul1"],
    ),
    (
        "Attribute presence selector, not matching default option without selected attribute",
        "#attr-presence-select1 option[selected]",
        [],
    ),
    (
        "Attribute presence selector, matching option with selected attribute",
        "#attr-presence-select2 option[selected]",
        ["attr-presence-select2-option4"],
    ),
    (
        "Attribute presence selector, matching multiple options with selected attributes",
        "#attr-presence-select3 option[selected]",
        ["attr-presence-select3-option2", "attr-presence-select3-option3"],
    ),
    (
        "Attribute value selector, matching align attribute with value",
        '#attr-value [align="center"]',
        ["attr-value-div1"],
    ),
    (
        "Attribute value selector, matching align attribute with empty value",
        '#attr-value [align=""]',
        ["attr-value-div2"],
    ),
    ("Attribute value selector, not matching align attribute with partial value", '#attr-value [align="c"]', []),
    (
        "Attribute value selector, not matching align attribute with incorrect value",
        '#attr-value [align="centera"]',
        [],
    ),
    (
        "Attribute value selector, matching custom data-* attribute with unicode escaped value",
        '[data-attr-value="\\e9"]',
        ["attr-value-div3"],
    ),
    (
        "Attribute value selector, matching custom data-* attribute with escaped character",
        '[data-attr-value_foo="\\e9"]',
        ["attr-value-div4"],
    ),
    (
        "Attribute value selector with single-quoted value, matching multiple inputs with type attributes",
        "#attr-value input[type='hidden'],#attr-value input[type='radio']",
        ["attr-value-input3", "attr-value-input4", "attr-value-input6", "attr-value-input8", "attr-value-input9"],
    ),
    (
        "Attribute value selector with double-quoted value, matching multiple inputs with type attributes",
        "#attr-value input[type=\"hidden\"],#attr-value input[type='radio']",
        ["attr-value-input3", "attr-value-input4", "attr-value-input6", "attr-value-input8", "attr-value-input9"],
    ),
    (
        "Attribute value selector with unquoted value, matching multiple inputs with type attributes",
        "#attr-value input[type=hidden],#attr-value input[type=radio]",
        ["attr-value-input3", "attr-value-input4", "attr-value-input6", "attr-value-input8", "attr-value-input9"],
    ),
    (
        "Attribute value selector, matching attribute with value using non-ASCII characters",
        "[data-attr-value=中文]",
        ["attr-value-div5"],
    ),
    (
        "Attribute whitespace-separated list selector, matching class attribute with value",
        '#attr-whitespace [class~="div1"]',
        ["attr-whitespace-div1"],
    ),
    (
        "Attribute whitespace-separated list selector, not matching class attribute with empty value",
        '#attr-whitespace [class~=""]',
        [],
    ),
    (
        "Attribute whitespace-separated list selector, not matching class attribute with partial value",
        '[data-attr-whitespace~="div"]',
        [],
    ),
    (
        "Attribute whitespace-separated list selector, matching custom data-* attribute with unicode escaped value",
        '[data-attr-whitespace~="\\0000e9"]',
        ["attr-whitespace-div4"],
    ),
    (
        "Attribute whitespace-separated list selector, matching custom data-* attribute with escaped character",
        '[data-attr-whitespace_foo~="\\e9"]',
        ["attr-whitespace-div5"],
    ),
    (
        "Attribute whitespace-separated list selector with single-quoted value, matching multiple links with rel "
        "attributes",
        "#attr-whitespace a[rel~='bookmark'],  #attr-whitespace a[rel~='nofollow']",
        ["attr-whitespace-a1", "attr-whitespace-a2", "attr-whitespace-a3", "attr-whitespace-a5", "attr-whitespace-a7"],
    ),
    (
        "Attribute whitespace-separated list selector with double-quoted value, matching multiple links with rel "
        "attributes",
        "#attr-whitespace a[rel~=\"bookmark\"],#attr-whitespace a[rel~='nofollow']",
        ["attr-whitespace-a1", "attr-whitespace-a2", "attr-whitespace-a3", "attr-whitespace-a5", "attr-whitespace-a7"],
    ),
    (
        "Attribute whitespace-separated list selector with unquoted value, matching multiple links with rel "
        "attributes",
        "#attr-whitespace a[rel~=bookmark],    #attr-whitespace a[rel~=nofollow]",
        ["attr-whitespace-a1", "attr-whitespace-a2", "attr-whitespace-a3", "attr-whitespace-a5", "attr-whitespace-a7"],
    ),
    (
        "Attribute whitespace-separated list selector with double-quoted value, not matching value with space",
        '#attr-whitespace a[rel~="book mark"]',
        [],
    ),
    (
        "Attribute whitespace-separated list selector, matching title attribute with value using non-ASCII "
        "characters",
        "#attr-whitespace [title~=中文]",
        ["attr-whitespace-p1"],
    ),
    (
        "Attribute hyphen-separated list selector, not matching unspecified lang attribute",
        '#attr-hyphen-div1[lang|="en"]',
        [],
    ),
    (
        "Attribute hyphen-separated list selector, matching lang attribute with exact value",
        '#attr-hyphen-div2[lang|="fr"]',
        ["attr-hyphen-div2"],
    ),
    (
        "Attribute hyphen-separated list selector, matching lang attribute with partial value",
        '#attr-hyphen-div3[lang|="en"]',
        ["attr-hyphen-div3"],
    ),
    ("Attribute hyphen-separated list selector, not matching incorrect value", '#attr-hyphen-div4[lang|="es-AR"]', []),
    (
        "Attribute begins with selector, matching href attributes beginning with specified substring",
        '#attr-begins a[href^="http://www"]',
        ["attr-begins-a1", "attr-begins-a3"],
    ),
    (
        "Attribute begins with selector, matching lang attributes beginning with specified substring, ",
        '#attr-begins [lang^="en-"]',
        ["attr-begins-div2", "attr-begins-div4"],
    ),
    ("Attribute begins with selector, not matching class attribute with empty value", '#attr-begins [class^=""]', []),
    (
        "Attribute begins with selector, not matching class attribute not beginning with specified substring",
        "#attr-begins [class^=apple]",
        [],
    ),
    (
        "Attribute begins with selector with single-quoted value, matching class attribute beginning with "
        "specified substring",
        "#attr-begins [class^=' apple']",
        ["attr-begins-p1"],
    ),
    (
        "Attribute begins with selector with double-quoted value, matching class attribute beginning with "
        "specified substring",
        '#attr-begins [class^=" apple"]',
        ["attr-begins-p1"],
    ),
    (
        "Attribute begins with selector with unquoted value, not matching class attribute not beginning with "
        "specified substring",
        "#attr-begins [class^= apple]",
        [],
    ),
    (
        "Attribute ends with selector, matching href attributes ending with specified substring",
        '#attr-ends a[href$=".org"]',
        ["attr-ends-a1", "attr-ends-a3"],
    ),
    (
        "Attribute ends with selector, matching lang attributes ending with specified substring, ",
        '#attr-ends [lang$="-CH"]',
        ["attr-ends-div2", "attr-ends-div4"],
    ),
    ("Attribute ends with selector, not matching class attribute with empty value", '#attr-ends [class$=""]', []),
    (
        "Attribute ends with selector, not matching class attribute not ending with specified substring",
        "#attr-ends [class$=apple]",
        [],
    ),
    (
        "Attribute ends with selector with single-quoted value, matching class attribute ending with specified "
        "substring",
        "#attr-ends [class$='apple ']",
        ["attr-ends-p1"],
    ),
    (
        "Attribute ends with selector with double-quoted value, matching class attribute ending with specified "
        "substring",
        '#attr-ends [class$="apple "]',
        ["attr-ends-p1"],
    ),
    (
        "Attribute ends with selector with unquoted value, not matching class attribute not ending with specified "
        "substring",
        "#attr-ends [class$=apple ]",
        [],
    ),
    (
        "Attribute contains selector, matching href attributes beginning with specified substring",
        '#attr-contains a[href*="http://www"]',
        ["attr-contains-a1", "attr-contains-a3"],
    ),
    (
        "Attribute contains selector, matching href attributes ending with specified substring",
        '#attr-contains a[href*=".org"]',
        ["attr-contains-a1", "attr-contains-a2"],
    ),
    (
        "Attribute contains selector, matching href attributes containing specified substring",
        '#attr-contains a[href*=".example."]',
        ["attr-contains-a1", "attr-contains-a3"],
    ),
    (
        "Attribute contains selector, matching lang attributes beginning with specified substring, ",
        '#attr-contains [lang*="en-"]',
        ["attr-contains-div2", "attr-contains-div6"],
    ),
    (
        "Attribute contains selector, matching lang attributes ending with specified substring, ",
        '#attr-contains [lang*="-CH"]',
        ["attr-contains-div3", "attr-contains-div5"],
    ),
    ("Attribute contains selector, not matching class attribute with empty value", '#attr-contains [class*=""]', []),
    (
        "Attribute contains selector with single-quoted value, matching class attribute beginning with specified "
        "substring",
        "#attr-contains [class*=' apple']",
        ["attr-contains-p1"],
    ),
    (
        "Attribute contains selector with single-quoted value, matching class attribute ending with specified "
        "substring",
        "#attr-contains [class*='orange ']",
        ["attr-contains-p1"],
    ),
    (
        "Attribute contains selector with single-quoted value, matching class attribute containing specified "
        "substring",
        "#attr-contains [class*='ple banana ora']",
        ["attr-contains-p1"],
    ),
    (
        "Attribute contains selector with double-quoted value, matching class attribute beginning with specified "
        "substring",
        '#attr-contains [class*=" apple"]',
        ["attr-contains-p1"],
    ),
    (
        "Attribute contains selector with double-quoted value, matching class attribute ending with specified "
        "substring",
        '#attr-contains [class*="orange "]',
        ["attr-contains-p1"],
    ),
    (
        "Attribute contains selector with double-quoted value, matching class attribute containing specified "
        "substring",
        '#attr-contains [class*="ple banana ora"]',
        ["attr-contains-p1"],
    ),
    (
        "Attribute contains selector with unquoted value, matching class attribute beginning with specified "
        "substring",
        "#attr-contains [class*= apple]",
        ["attr-contains-p1"],
    ),
    (
        "Attribute contains selector with unquoted value, matching class attribute ending with specified " "substring",
        "#attr-contains [class*=orange ]",
        ["attr-contains-p1"],
    ),
    (
        "Attribute contains selector with unquoted value, matching class attribute containing specified " "substring",
        "#attr-contains [class*= banana ]",
        ["attr-contains-p1"],
    ),
    (":root pseudo-class selector, not matching document root element", ":root", []),
    (
        ":nth-child selector, matching the third child element",
        "#pseudo-nth-table1 :nth-child(3)",
        ["pseudo-nth-td3", "pseudo-nth-td9", "pseudo-nth-tr3", "pseudo-nth-td15"],
    ),
    (
        ":nth-child selector, matching every third child element",
        "#pseudo-nth li:nth-child(3n)",
        ["pseudo-nth-li3", "pseudo-nth-li6", "pseudo-nth-li9", "pseudo-nth-li12"],
    ),
    (
        ":nth-child selector, matching every second child element, starting from the fourth",
        "#pseudo-nth li:nth-child(2n+4)",
        ["pseudo-nth-li4", "pseudo-nth-li6", "pseudo-nth-li8", "pseudo-nth-li10", "pseudo-nth-li12"],
    ),
    (
        ":nth-child selector, matching every fourth child element, starting from the third",
        "#pseudo-nth-p1 :nth-child(4n-1)",
        ["pseudo-nth-em2", "pseudo-nth-span3"],
    ),
    (
        ":nth-last-child selector, matching the third last child element",
        "#pseudo-nth-table1 :nth-last-child(3)",
        ["pseudo-nth-tr1", "pseudo-nth-td4", "pseudo-nth-td10", "pseudo-nth-td16"],
    ),
    (
        ":nth-last-child selector, matching every third child element from the end",
        "#pseudo-nth li:nth-last-child(3n)",
        ["pseudo-nth-li1", "pseudo-nth-li4", "pseudo-nth-li7", "pseudo-nth-li10"],
    ),
    (
        ":nth-last-child selector, matching every second child element from the end, starting from the fourth " "last",
        "#pseudo-nth li:nth-last-child(2n+4)",
        ["pseudo-nth-li1", "pseudo-nth-li3", "pseudo-nth-li5", "pseudo-nth-li7", "pseudo-nth-li9"],
    ),
    (
        ":nth-last-child selector, matching every fourth element from the end, starting from the third last",
        "#pseudo-nth-p1 :nth-last-child(4n-1)",
        ["pseudo-nth-span2", "pseudo-nth-span4"],
    ),
    (":nth-of-type selector, matching the third em element", "#pseudo-nth-p1 em:nth-of-type(3)", ["pseudo-nth-em3"]),
    (
        ":nth-of-type selector, matching every second element of their type",
        "#pseudo-nth-p1 :nth-of-type(2n)",
        ["pseudo-nth-em2", "pseudo-nth-span2", "pseudo-nth-span4", "pseudo-nth-strong2", "pseudo-nth-em4"],
    ),
    (
        ":nth-of-type selector, matching every second elemetn of their type, starting from the first",
        "#pseudo-nth-p1 span:nth-of-type(2n-1)",
        ["pseudo-nth-span1", "pseudo-nth-span3"],
    ),
    (
        ":nth-last-of-type selector, matching the third last em element",
        "#pseudo-nth-p1 em:nth-last-of-type(3)",
        ["pseudo-nth-em2"],
    ),
    (
        ":nth-last-of-type selector, matching every second last element of their type",
        "#pseudo-nth-p1 :nth-last-of-type(2n)",
        ["pseudo-nth-span1", "pseudo-nth-em1", "pseudo-nth-strong1", "pseudo-nth-em3", "pseudo-nth-span3"],
    ),
    (
        ":nth-last-of-type selector, matching every second last element of their type, starting from the last",
        "#pseudo-nth-p1 span:nth-last-of-type(2n-1)",
        ["pseudo-nth-span2", "pseudo-nth-span4"],
    ),
    (":first-of-type selector, matching the first em element", "#pseudo-nth-p1 em:first-of-type", ["pseudo-nth-em1"]),
    (
        ":first-of-type selector, matching the first of every type of element",
        "#pseudo-nth-p1 :first-of-type",
        ["pseudo-nth-span1", "pseudo-nth-em1", "pseudo-nth-strong1"],
    ),
    (
        ":first-of-type selector, matching the first td element in each table row",
        "#pseudo-nth-table1 tr :first-of-type",
        ["pseudo-nth-td1", "pseudo-nth-td7", "pseudo-nth-td13"],
    ),
    (":last-of-type selector, matching the last em elemnet", "#pseudo-nth-p1 em:last-of-type", ["pseudo-nth-em4"]),
    (
        ":last-of-type selector, matching the last of every type of element",
        "#pseudo-nth-p1 :last-of-type",
        ["pseudo-nth-span4", "pseudo-nth-strong2", "pseudo-nth-em4"],
    ),
    (
        ":last-of-type selector, matching the last td element in each table row",
        "#pseudo-nth-table1 tr :last-of-type",
        ["pseudo-nth-td6", "pseudo-nth-td12", "pseudo-nth-td18"],
    ),
    (
        ":first-child pseudo-class selector, matching first child div element",
        "#pseudo-first-child div:first-child",
        ["pseudo-first-child-div1"],
    ),
    (
        ":first-child pseudo-class selector, doesn't match non-first-child elements",
        ".pseudo-first-child-div2:first-child, .pseudo-first-child-div3:first-child",
        [],
    ),
    (
        ":first-child pseudo-class selector, matching first-child of multiple elements",
        "#pseudo-first-child span:first-child",
        ["pseudo-first-child-span1", "pseudo-first-child-span3", "pseudo-first-child-span5"],
    ),
    (
        ":last-child pseudo-class selector, matching last child div element",
        "#pseudo-last-child div:last-child",
        ["pseudo-last-child-div3"],
    ),
    (
        ":last-child pseudo-class selector, doesn't match non-last-child elements",
        ".pseudo-last-child-div1:last-child, .pseudo-last-child-div2:first-child",
        [],
    ),
    (
        ":last-child pseudo-class selector, matching first-child of multiple elements",
        "#pseudo-last-child span:last-child",
        ["pseudo-last-child-span2", "pseudo-last-child-span4", "pseudo-last-child-span6"],
    ),
    (
        ":pseudo-only-child pseudo-class selector, matching all only-child elements",
        "#pseudo-only :only-child",
        ["pseudo-only-span1"],
    ),
    (":pseudo-only-child pseudo-class selector, matching only-child em elements", "#pseudo-only em:only-child", []),
    (
        ":pseudo-only-of-type pseudo-class selector, matching all elements with no siblings of the same type",
        "#pseudo-only :only-of-type",
        ["pseudo-only-span1", "pseudo-only-em1"],
    ),
    (
        ":pseudo-only-of-type pseudo-class selector, matching em elements with no siblings of the same type",
        "#pseudo-only em:only-of-type",
        ["pseudo-only-em1"],
    ),
    (
        ":empty pseudo-class selector, matching empty p elements",
        "#pseudo-empty p:empty",
        ["pseudo-empty-p1", "pseudo-empty-p2"],
    ),
    (
        ":empty pseudo-class selector, matching all empty elements",
        "#pseudo-empty :empty",
        ["pseudo-empty-p1", "pseudo-empty-p2", "pseudo-empty-span1"],
    ),
    (
        ":link and :visited pseudo-class selectors, matching a and area elements with href attributes",
        "#pseudo-link :link, #pseudo-link :visited",
        ["pseudo-link-a1", "pseudo-link-a2", "pseudo-link-area1"],
    ),
    (
        ":link and :visited pseudo-class selectors, not matching link elements with href attributes",
        "#head :link, #head :visited",
        [],
    ),
    (
        ":link and :visited pseudo-class selectors, chained, mutually exclusive pseudo-classes match nothing",
        ":link:visited",
        [],
    ),
    (
        ":lang pseudo-class selector, matching inherited language",
        "#pseudo-lang-div1:lang(en)",
        ["pseudo-lang-div1"],
    ),
    (
        ":lang pseudo-class selector, matching specified language with exact value",
        "#pseudo-lang-div2:lang(fr)",
        ["pseudo-lang-div2"],
    ),
    (
        ":lang pseudo-class selector, matching specified language with partial value",
        "#pseudo-lang-div3:lang(en)",
        ["pseudo-lang-div3"],
    ),
    (":lang pseudo-class selector, not matching incorrect language", "#pseudo-lang-div4:lang(es-AR)", []),
    (
        ":enabled pseudo-class selector, matching all enabled form controls",
        "#pseudo-ui :enabled",
        [
            "pseudo-ui-input1",
            "pseudo-ui-input2",
            "pseudo-ui-input3",
            "pseudo-ui-input4",
            "pseudo-ui-input5",
            "pseudo-ui-input6",
            "pseudo-ui-input7",
            "pseudo-ui-input8",
            "pseudo-ui-input9",
            "pseudo-ui-textarea1",
            "pseudo-ui-button1",
        ],
    ),
    (":enabled pseudo-class selector, not matching link elements", "#pseudo-link :enabled", []),
    (
        ":disabled pseudo-class selector, matching all disabled form controls",
        "#pseudo-ui :disabled",
        [
            "pseudo-ui-input10",
            "pseudo-ui-input11",
            "pseudo-ui-input12",
            "pseudo-ui-input13",
            "pseudo-ui-input14",
            "pseudo-ui-input15",
            "pseudo-ui-input16",
            "pseudo-ui-input17",
            "pseudo-ui-input18",
            "pseudo-ui-textarea2",
            "pseudo-ui-button2",
        ],
    ),
    (":disabled pseudo-class selector, not matching link elements", "#pseudo-link :disabled", []),
    (
        ":checked pseudo-class selector, matching checked radio buttons and checkboxes",
        "#pseudo-ui :checked",
        ["pseudo-ui-input4", "pseudo-ui-input6", "pseudo-ui-input13", "pseudo-ui-input15"],
    ),
    (":not pseudo-class selector, matching ", "#not>:not(div)", ["not-p1", "not-p2", "not-p3"]),
    (":not pseudo-class selector, matching ", "#not * :not(:first-child)", ["not-em1", "not-em2", "not-em3"]),
    (":not pseudo-class selector, matching nothing", ":not(*)", []),
    (":not pseudo-class selector, matching nothing", ":not(*|*)", []),
    (
        ":not pseudo-class selector argument surrounded by spaces, matching ",
        "#not>:not( div )",
        ["not-p1", "not-p2", "not-p3"],
    ),
    (
        ":first-line pseudo-element (one-colon syntax) selector, not matching any elements",
        "#pseudo-element:first-line",
        [],
    ),
    (
        "::first-line pseudo-element (two-colon syntax) selector, not matching any elements",
        "#pseudo-element::first-line",
        [],
    ),
    (
        ":first-letter pseudo-element (one-colon syntax) selector, not matching any elements",
        "#pseudo-element:first-letter",
        [],
    ),
    (
        "::first-letter pseudo-element (two-colon syntax) selector, not matching any elements",
        "#pseudo-element::first-letter",
        [],
    ),
    (":before pseudo-element (one-colon syntax) selector, not matching any elements", "#pseudo-element:before", []),
    (
        "::before pseudo-element (two-colon syntax) selector, not matching any elements",
        "#pseudo-element::before",
        [],
    ),
    (":after pseudo-element (one-colon syntax) selector, not matching any elements", "#pseudo-element:after", []),
    ("::after pseudo-element (two-colon syntax) selector, not matching any elements", "#pseudo-element::after", []),
    ("Class selector, matching element with specified class", ".class-p", ["class-p1", "class-p2", "class-p3"]),
    (
        "Class selector, chained, matching only elements with all specified classes",
        "#class .apple.orange.banana",
        ["class-div1", "class-div2", "class-p4", "class-div3", "class-p6", "class-div4"],
    ),
    (
        "Class Selector, chained, with type selector",
        "div.apple.banana.orange",
        ["class-div1", "class-div2", "class-div3", "class-div4"],
    ),
    (
        "Class selector, matching element with class value using non-ASCII characters (1)",
        ".台北Táiběi",
        ["class-span1"],
    ),
    (
        "Class selector, matching multiple elements with class value using non-ASCII characters",
        ".台北",
        ["class-span1", "class-span2"],
    ),
    (
        "Class selector, chained, matching element with multiple class values using non-ASCII characters (1)",
        ".台北Táiběi.台北",
        ["class-span1"],
    ),
    ("Class selector, matching element with class with escaped character", r".foo\:bar", ["class-span3"]),
    ("Class selector, matching element with class with escaped character", r".test\.foo\[5\]bar", ["class-span4"]),
    ("ID selector, matching element with specified id", "#id #id-div1", ["id-div1"]),
    ("ID selector, chained, matching element with specified id", "#id-div1, #id-div1", ["id-div1"]),
    ("ID selector, chained, matching element with specified id", "#id-div1, #id-div2", ["id-div1", "id-div2"]),
    ("ID Selector, chained, with type selector", "div#id-div1, div#id-div2", ["id-div1", "id-div2"]),
    ("ID selector, not matching non-existent descendant", "#id #none", []),
    ("ID selector, not matching non-existent ancestor", "#none #id-div1", []),
    ("ID selector, matching id value using non-ASCII characters (1)", "#台北Táiběi", ["台北Táiběi"]),
    ("ID selector, matching id value using non-ASCII characters (2)", "#台北", ["台北"]),
    ("ID selector, matching id values using non-ASCII characters (1)", "#台北Táiběi, #台北", ["台北Táiběi", "台北"]),
    ("ID selector, matching element with id with escaped character", r"#\#foo\:bar", ["#foo:bar"]),
    ("ID selector, matching element with id with escaped character", r"#test\.foo\[5\]bar", ["test.foo[5]bar"]),
    (
        "Descendant combinator, matching element that is a descendant of an element with id",
        "#descendant div",
        ["descendant-div1", "descendant-div2", "descendant-div3", "descendant-div4"],
    ),
    (
        "Descendant combinator, matching element with id that is a descendant of an element",
        "div #descendant-div1",
        ["descendant-div1"],
    ),
    (
        "Descendant combinator, matching element with id that is a descendant of an element with id",
        "#descendant #descendant-div2",
        ["descendant-div2"],
    ),
    (
        "Descendant combinator, matching element with class that is a descendant of an element with id",
        "#descendant .descendant-div2",
        ["descendant-div2"],
    ),
    (
        "Descendant combinator, matching element with class that is a descendant of an element with class",
        ".descendant-div1 .descendant-div3",
        ["descendant-div3"],
    ),
    (
        "Descendant combinator, not matching element with id that is not a descendant of an element with id",
        "#descendant-div1 #descendant-div4",
        [],
    ),
    ("Descendant combinator, whitespace characters", "#descendant\t\r\n#descendant-div2", ["descendant-div2"]),
    (
        "Child combinator, matching element that is a child of an element with id",
        "#child>div",
        ["child-div1", "child-div4"],
    ),
    ("Child combinator, matching element with id that is a child of an element", "div>#child-div1", ["child-div1"]),
    (
        "Child combinator, matching element with id that is a child of an element with id",
        "#child>#child-div1",
        ["child-div1"],
    ),
    (
        "Child combinator, matching element with id that is a child of an element with class",
        "#child-div1>.child-div2",
        ["child-div2"],
    ),
    (
        "Child combinator, matching element with class that is a child of an element with class",
        ".child-div1>.child-div2",
        ["child-div2"],
    ),
    (
        "Child combinator, not matching element with id that is not a child of an element with id",
        "#child>#child-div3",
        [],
    ),
    (
        "Child combinator, not matching element with id that is not a child of an element with class",
        "#child-div1>.child-div3",
        [],
    ),
    (
        "Child combinator, not matching element with class that is not a child of an element with class",
        ".child-div1>.child-div3",
        [],
    ),
    ("Child combinator, surrounded by whitespace", "#child-div1\t\r\n>\t\r\n#child-div2", ["child-div2"]),
    ("Child combinator, whitespace after", "#child-div1>\t\r\n#child-div2", ["child-div2"]),
    ("Child combinator, whitespace before", "#child-div1\t\r\n>#child-div2", ["child-div2"]),
    ("Child combinator, no whitespace", "#child-div1>#child-div2", ["child-div2"]),
    (
        "Adjacent sibling combinator, matching element that is an adjacent sibling of an element with id",
        "#adjacent-div2+div",
        ["adjacent-div4"],
    ),
    (
        "Adjacent sibling combinator, matching element with id that is an adjacent sibling of an element",
        "div+#adjacent-div4",
        ["adjacent-div4"],
    ),
    (
        "Adjacent sibling combinator, matching element with id that is an adjacent sibling of an element with id",
        "#adjacent-div2+#adjacent-div4",
        ["adjacent-div4"],
    ),
    (
        "Adjacent sibling combinator, matching element with class that is an adjacent sibling of an element with " "id",
        "#adjacent-div2+.adjacent-div4",
        ["adjacent-div4"],
    ),
    (
        "Adjacent sibling combinator, matching element with class that is an adjacent sibling of an element with "
        "class",
        ".adjacent-div2+.adjacent-div4",
        ["adjacent-div4"],
    ),
    (
        "Adjacent sibling combinator, matching p element that is an adjacent sibling of a div element",
        "#adjacent div+p",
        ["adjacent-p2"],
    ),
    (
        "Adjacent sibling combinator, not matching element with id that is not an adjacent sibling of an element "
        "with id",
        "#adjacent-div2+#adjacent-p2, #adjacent-div2+#adjacent-div1",
        [],
    ),
    ("Adjacent sibling combinator, surrounded by whitespace", "#adjacent-p2\t\r\n+\t\r\n#adjacent-p3", ["adjacent-p3"]),
    ("Adjacent sibling combinator, whitespace after", "#adjacent-p2+\t\r\n#adjacent-p3", ["adjacent-p3"]),
    ("Adjacent sibling combinator, whitespace before", "#adjacent-p2\t\r\n+#adjacent-p3", ["adjacent-p3"]),
    ("Adjacent sibling combinator, no whitespace", "#adjacent-p2+#adjacent-p3", ["adjacent-p3"]),
    (
        "General sibling combinator, matching element that is a sibling of an element with id",
        "#sibling-div2~div",
        ["sibling-div4", "sibling-div6"],
    ),
    (
        "General sibling combinator, matching element with id that is a sibling of an element",
        "div~#sibling-div4",
        ["sibling-div4"],
    ),
    (
        "General sibling combinator, matching element with id that is a sibling of an element with id",
        "#sibling-div2~#sibling-div4",
        ["sibling-div4"],
    ),
    (
        "General sibling combinator, matching element with class that is a sibling of an element with id",
        "#sibling-div2~.sibling-div",
        ["sibling-div4", "sibling-div6"],
    ),
    (
        "General sibling combinator, matching p element that is a sibling of a div element",
        "#sibling div~p",
        ["sibling-p2", "sibling-p3"],
    ),
    (
        "General sibling combinator, not matching element with id that is not a sibling after a p element",
        "#sibling>p~div",
        [],
    ),
    (
        "General sibling combinator, not matching element with id that is not a sibling after an element with id",
        "#sibling-div2~#sibling-div3, #sibling-div2~#sibling-div1",
        [],
    ),
    ("General sibling combinator, surrounded by whitespace", "#sibling-p2\t\r\n~\t\r\n#sibling-p3", ["sibling-p3"]),
    ("General sibling combinator, whitespace after", "#sibling-p2~\t\r\n#sibling-p3", ["sibling-p3"]),
    ("General sibling combinator, whitespace before", "#sibling-p2\t\r\n~#sibling-p3", ["sibling-p3"]),
    ("General sibling combinator, no whitespace", "#sibling-p2~#sibling-p3", ["sibling-p3"]),
    (
        "Syntax, group of selectors separator, surrounded by whitespace",
        "#group em\t\r \n,\t\r \n#group strong",
        ["group-em1", "group-strong1"],
    ),
    (
        "Syntax, group of selectors separator, whitespace after",
        "#group em,\t\r\n#group strong",
        ["group-em1", "group-strong1"],
    ),
    (
        "Syntax, group of selectors separator, whitespace before",
        "#group em\t\r\n,#group strong",
        ["group-em1", "group-strong1"],
    ),
    ("Syntax, group of selectors separator, no whitespace", "#group em,#group strong", ["group-em1", "group-strong1"]),
    ("Slotted selector", "::slotted(foo)", []),
    ("Slotted selector (no matching closing paren)", "::slotted(foo", []),
]


class QuerySelectorAllConformance(unittest.TestCase):
    def test_valid_selectors(self):
        for name, selector, expect in VALID_SELECTORS_QSA:
            with self.subTest(name=name, selector=selector):
                found = ROOT.querySelectorAll(selector)
                self.assertEqual([el.getAttribute("id") for el in found], expect)
                first = ROOT.querySelector(selector)
                if expect:
                    self.assertIsNotNone(first)
                    self.assertEqual(first.getAttribute("id"), expect[0])
                else:
                    self.assertIsNone(first)


class KnownDeviations(unittest.TestCase):
    """Rows the upstream suite expects to work that domonic does not (yet)
    implement -- tracked individually, per the project's WPT convention,
    instead of silently dropped from VALID_SELECTORS_QSA."""

    @pytest.mark.xfail(
        reason="no auto-close leniency for an unterminated '[...' at the end of a selector",
        strict=True,
    )
    def test_unclosed_attribute_bracket(self):
        found = ROOT.querySelectorAll('#attr-value [align="center"')
        self.assertEqual([el.getAttribute("id") for el in found], ["attr-value-div1"])

    @pytest.mark.xfail(
        reason=":target needs URL-fragment/navigation state domonic does not track",
        strict=True,
    )
    def test_target_pseudo_class(self):
        found = ROOT.querySelectorAll(":target")
        self.assertEqual([el.getAttribute("id") for el in found], ["target"])

    @pytest.mark.xfail(
        reason="querySelectorAll('#id') is a getElementById()-speed shortcut, so it returns only the first "
        "element with a duplicate id, not every element with that id attribute; duplicate ids are invalid "
        "HTML and the shortcut is worth keeping for the common (unique-id) case",
        strict=True,
    )
    def test_id_selector_matches_every_element_with_a_duplicate_id(self):
        found = ROOT.querySelectorAll("#id-li-duplicate")
        self.assertEqual(len(found), 4)

    @pytest.mark.xfail(
        reason="namespace selectors (*|div, |div, |*) are not implemented -- setAttributeNS() does not track "
        "namespaces, see domonic-wpt-conformance",
        strict=True,
    )
    def test_namespace_selectors(self):
        self.assertEqual(len(ROOT.querySelectorAll("#any-namespace *|div")), 4)
        self.assertEqual(len(ROOT.querySelectorAll("#no-namespace |div")), 1)
        self.assertEqual(len(ROOT.querySelectorAll("#no-namespace |*")), 1)

    @pytest.mark.xfail(
        reason="a descendant combinator's left-hand compound is only looked up inside the queried subtree, so "
        "an ancestor of the query root itself (here 'body', an ancestor of #root) is never found",
        strict=True,
    )
    def test_descendant_combinator_searches_above_the_query_root(self):
        found = ROOT.querySelectorAll("body #descendant-div1")
        self.assertEqual([el.getAttribute("id") for el in found], ["descendant-div1"])


if __name__ == "__main__":
    unittest.main()
