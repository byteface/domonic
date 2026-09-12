# WPT conformance ports

Selected [web-platform-tests](https://github.com/web-platform-tests/wpt)
`dom/` tests, transcribed to Python and run against `domonic.dom`.

WPT tests are browser JavaScript (`testharness.js` + live `document`/`window`),
so they can't be run directly. Each file here is a near-line-for-line port of
one upstream `.html` file: the `test(function () { … }, "name")` blocks become
`unittest` methods, and `_harness.py` supplies WPT-style assertion helpers
(`assert_equals`, `assert_array_equals`, `assert_throws_dom`, …) so a failure
reads like the original.

## Running

```
pytest tests/wpt/
```

## Ported so far

`Node-isEqualNode`, `Node-nodeValue`, `Node-contains`, `Document-getElementById`,
`ChildNode-replaceWith`
/ `-before` / `-after`, `Node-childNodes`, `Node-compareDocumentPosition` (+
`getRootNode`), `Node-appendChild` / `-insertBefore` / `-replaceChild`
(pre-insertion validity), `Element-classlist`, `Element-getElementsByTagName`
/ `-getElementsByClassName` / `getElementsByName`, `Document-createElement` /
`-createProcessingInstruction`, `attributes.html` (toggleAttribute /
setAttribute), `insert-adjacent`, `DOMImplementation-createHTMLDocument` /
`-createDocumentType`, `Text-wholeText` / `-splitText`, `TreeWalker-basic` /
`TreeWalker-acceptNode-filter`, `NodeIterator`, `Range-attributes` /
`-collapse` / `-comparePoint` / `-isPointInRange` / `-selectNode`, and a batch
of `dom/events/` (EventTarget add/remove, dispatch order and phases,
propagation, once, handleEvent, CustomEvent), `ParentNode-append` /
`-prepend` / `-replaceChildren` (Element / Document / DocumentFragment),
`Node-cloneNode` / `Document-importNode` / `Document-adoptNode`,
`Node-properties` (parentElement, sibling elements), the WHATWG
fragment-serialisation checks for `innerHTML` / `outerHTML`, `dom/abort/`
(`AbortSignal.abort` / `.timeout` / `.any`), `DOMParser` / `XMLSerializer`,
`Document-*` metadata (compatMode / contentType / readyState),
`attributes-namednodemap`, DocumentFragment insertion (appendChild /
insertBefore / replaceChild), `shadow-dom/Element-interface-attachShadow`
+ shadow-including `getRootNode`, `Element-matches` / `Element-closest`
(including `:scope`), the `<template>` element's `.content`, the live
`document.forms` / `images` / `links` / `scripts` / `anchors` / `embeds`
accessors, the `<form>` element (`elements`, `length`, named access,
`RadioNodeList.value`, control `.form`), and IDL reflection
(`id` / `className` / `hidden` / `tabIndex`), the Selectors-API
conformance suite (`selectors.js` + `ParentNode-querySelector-All.js` +
`-content.html`) against `querySelector()` / `querySelectorAll()`, and
`CharacterData` (`appendData` / `deleteData` / `insertData` / `replaceData` /
`substringData` / `.data` / `appendChild`), run against both `Text` and
`Comment`, and `Range` (`commonAncestorContainer`, `compareBoundaryPoints`,
`intersectsNode`, `cloneRange`, the stringifier, `cloneContents` /
`deleteContents` / `extractContents` / `insertNode` / `surroundContents`
for the shapes they get right), and a grab-bag of smaller members:
`Node.nodeName` / `-isSameNode` / `-isDefaultNamespace` / the `nodeType`
constants, `Element.hasAttribute(s)` / `-webkitMatchesSelector`,
`Attr.ownerElement` / `-localName` / `-prefix` / `-namespaceURI` /
`-specified`, and `Document.createCDATASection`, and the rest of
`TreeWalker` (`NodeFilter` constants, `currentNode`, `previousNode`
respecting the filter, surviving detachment/regrafting).

## When a port fails

It's one of two things:

- **A real discrepancy** — fix it in `domonic/dom.py` and the test goes green.
  (`Node-isEqualNode` was `str(a) == str(b)`; the port drove it to a proper
  per-interface comparison. `Node-appendChild`/`insertBefore`/`replaceChild`
  drove the "pre-insertion validity" cycle check — inserting a node into its
  own subtree used to hang — and typed `DOMException` names. `Element-classlist`
  drove the `DOMTokenList` spec fixes: `SyntaxError`/`InvalidCharacterError`
  names, non-validating `contains()`, verbatim stringifier, ordered-set
  `replace()`, no-op force `toggle()`, `supports()` raising `TypeError`.
  `Node-childNodes` drove out-of-range indexed access returning `None`.
  `Node-compareDocumentPosition` drove the combined bitmasks
  (`CONTAINS | PRECEDING`, `CONTAINED_BY | FOLLOWING`, and
  `DISCONNECTED | IMPLEMENTATION_SPECIFIC | direction` for separate trees).
  `Element-getElementsByTagName` drove a real `_LiveHTMLCollection` for
  `getElementsByTagName`/`-ClassName`/`-Name` — they used to return a static
  snapshot. The Selectors-API port drove a cluster of CSS selector-engine
  bugs: `+`/`~` were only combinators when whitespace-separated, so `div+p`
  silently failed; a descendant combinator directly before `[`/`(` (`#id
  [attr]`) merged into one compound instead of splitting; a compound that was
  only a pseudo-class (`:nth-child(3)`, `:not(div)`, `:empty` alone) failed to
  parse and fell through to a buggier XPath fallback (which returned Text
  nodes as matches, or ran `:enabled`/`:disabled` into a crash); `.foo:empty`
  read the class as the literal "foo:empty" instead of class `foo` plus the
  `:empty` pseudo; `:empty` and `[x^=""]`/`[x$=""]`/`[x*=""]` mismatched
  spec; `:root` matched the query context instead of the document root; CSS
  identifier/attribute-value escapes (`\e9`, `\:`, `\.`) were not decoded;
  and `:lang()` was not implemented at all. That last one also found a bug two
  layers deeper, in the html5lib parser adapter: `AttrList.__getitem__`
  (`domonic/ext/html5lib_/__init__.py`) caught every exception and returned
  `""` instead of letting a missing attribute's `KeyError` propagate, which
  silently broke every `x not in element.attributes` check -- including
  html5lib's own "merge a later `<html ...>` tag's attributes onto the
  already-inserted root" step, so any `<html lang="..." class="...">`
  attribute was discarded by every `parseString(document=True)` parse.
  The `CharacterData` port found that `Comment`/`ProcessingInstruction`/
  `CDATASection` had no `appendData`/`deleteData`/`insertData`/`replaceData`/
  `substringData` at all (added via a shared `_CharacterDataOnAttr` mixin,
  since their storage model -- data on a plain attribute -- differs from
  `Text`'s `Node.args`-based one); that a `Comment`/`ProcessingInstruction`/
  `CDATASection`'s `.data` was a bare slot with no coercion, so `comment.data
  = None` stored a literal `None` instead of `""`; that `offset`/`count`
  arguments were rejected outright for a negative value instead of wrapping
  modulo 2**32 like the spec's `unsigned long` IDL type (so
  `insertData(-0x100000000 + 2, "X")` incorrectly raised); and that inserting
  into a `Text`/`Comment`/`ProcessingInstruction`/`CDATASection` node (which
  can never have children) silently succeeded instead of throwing
  `HierarchyRequestError`. The `Range` port found more, one of them well
  outside Range itself: `_compare_points` (backing `comparePoint`,
  `isPointInRange`, `compareBoundaryPoints`, `intersectsNode` and the
  stringifier) never handled one boundary point's node being an *ancestor*
  of the other's -- an extremely common range shape -- and gave wrong
  answers for it. `Range.toString()` returned `str()`/markup of whatever
  nodes sat between the boundaries instead of the spec's Text-content-only
  concatenation (`<p>hi</p><p>bye</p>` stringified to itself, not `"hibye"`);
  fixing it to walk raw-string children as text too (domonic's
  `div("hello")` shorthand) is what surfaced the big one: `cloneNode(deep)`
  (and so `Range.cloneContents`/`extractContents`, which use it) raised
  `RecursionError` on any node with a real `ownerDocument`. It used
  `copy.deepcopy`, which follows every reachable reference -- including each
  descendant's `_ownerDocument`, dragging in the *entire* Document object
  (`localStorage`, loggers, a `threading.RLock` `copy.deepcopy` can't even
  copy) -- and `Storage.__getattr__` compounded it by catching every
  exception and returning `""`/`None` instead of raising `AttributeError`
  for a missing dunder, so `hasattr(storage, "__setstate__")` recursed into
  `self.storage` before `__init__` had set it, forever. Also: `Range`
  boundary offsets into a `Comment`/`ProcessingInstruction` (both
  `CharacterData`, both meant to be addressable by character offset) always
  raised, because `Range._container_length` only special-cased `Text`. The
  Node/Element odds sweep found: `Attr` had no `ownerElement`,
  `localName`/`prefix` (derived from the qualified name), or `specified` at
  all — and accessing the missing `ownerElement` returned a raw `property`
  object instead of `None`/raising, because `Attr.__init__` skips
  `Node.__init__` (so it never gets a `parentNode`) and `Node.__getattr__`'s
  fallback for a property whose getter itself raised `AttributeError`
  (`self.parentNode`, unset) is `getattr(self.__class__, name)`, which for a
  property accessed on the *class* returns the descriptor itself. `Element`
  had no `webkitMatchesSelector` (now `= matches`). `Document.
  createCDATASection` never refused in an HTML document (CDATA sections are
  XML-only). `Node.isDefaultNamespace` compared against this node's own
  `namespaceURI` instead of the namespace actually in scope
  (`lookupNamespaceURI(None)`) — since every node defaults to the HTML
  namespace at construction (`DocumentFragment` included), a fragment could
  never report itself as being in the default namespace. `Text.lastChild`/
  `hasChildNodes()` read the same slot Text stores its data in as if it
  were a child node (`text.lastChild` returned the text's own string data);
  `firstChild` had already been fixed the same way but the other two hadn't.
  The TreeWalker sweep found a real hang: `TreeWalker.previousNode()`, when
  walking backward, would try a candidate sibling and -- if filtering it (or
  its descendants) didn't return `FILTER_ACCEPT` -- **loop on that same
  candidate forever**, because the spec's "set sibling to node's previous
  sibling" retry step was missing; any `FILTER_REJECT`/`FILTER_SKIP` in the
  way of a backward walk hung the whole process. Also: `TreeWalker.
  currentNode` had no setter validation at all (assigning `None`, `{}`, or
  any non-`Node` value was silently accepted, corrupting every later
  traversal call instead of raising `TypeError`).
- **A deliberate domonic deviation** — mark the method
  `@pytest.mark.xfail(reason=…, strict=True)` with the reason, so the gap is
  tracked rather than silently passing or failing. Known ones:
  - namespaced attributes: `setAttributeNS()` ignores the namespace.
  - `document.createElement(...).tagName` stays lower-case (see the
    `domonic-serialization` note — `createElement` is a `@staticmethod` with no
    HTML document to consult).
  - `getElementsByTagName` normalises names to lower case, so the
    foreign-namespace / prefixed-name case-sensitivity rows from the upstream
    shared helper are not ported.
  - `replaceChild` returns `oldChild` unchanged when it is not a child instead
    of throwing `NotFoundError`; `removeChild` returns `None` in the same case.
  - namespace selectors (`*|div`, `|div`, `|*`) are not implemented.
  - `querySelectorAll('#id')` is a `getElementById()`-speed shortcut, so a
    duplicate (invalid-HTML) id returns only the first match.
  - a descendant combinator's left-hand compound is only looked up inside the
    queried subtree, not above the query root (`root.querySelectorAll("body
    ...")` never finds `body` when `root` is itself inside `<body>`).
  - `:target` (no navigation/URL-fragment state) and unterminated `[...`
    selectors (no auto-close leniency) are not supported.
  - `CharacterData` range methods (`deleteData`, `insertData`, `replaceData`,
    `substringData`, `Text.splitText`) raise a plain `IndexError` for an
    out-of-range offset/count, not `DOMException("IndexSizeError")` — an
    existing, deliberate convention (see `Text-splitText.html`'s port) this
    batch kept rather than relitigated.
  - offsets/counts are not JS-`ToNumber`-coerced: a numeric string (`"0"`)
    raises `TypeError` rather than being parsed, matching how every other
    offset/index argument in the codebase is already treated.
  - `.length` and every `CharacterData` offset count Python string
    codepoints, not UTF-16 code units — they agree for BMP text but not for
    astral-plane characters (most emoji): `"🌠".length` is 1 here, 2 in a
    browser. Splitting or joining a surrogate pair
    (`CharacterData-surrogates.html`) is out of scope.
  - a `Range`'s boundary points do not move when the tree around them is
    edited elsewhere (`Range-mutations-*.html`) — implementing
    https://dom.spec.whatwg.org/#concept-live-range needs a per-document
    live-range registry and adjustment hooks on every mutation path
    (`insertBefore`, `removeChild`, `splitText`, every `CharacterData` edit,
    `normalize()`); a real feature, not attempted.
  - `Range.cloneContents`/`extractContents` only correctly trim a boundary
    that sits directly in the common ancestor's own children, or in a
    single shared container; a boundary nested inside a partially selected
    element is not split — the whole element is included (or excised)
    instead of just its selected portion. `surroundContents()` also skips
    the spec's validity checks (`InvalidStateError` for a range that
    partially selects a non-Text node, `InvalidNodeTypeError` for a
    Document/DocumentType/DocumentFragment `newParent`).
  - `Node.lookupNamespaceURI` is a static well-known-prefix lookup (`xml`,
    `svg`, ...), not the spec's algorithm of walking `xmlns:*` attribute
    declarations up the tree -- blocked by the same "setAttributeNS ignores
    the namespace" gap. `Document.createAttribute` does not lowercase the
    name in an HTML document (the same limitation as `createElement`'s
    tagName casing: it is a `@staticmethod` with no document to consult).
    `removeAttribute`/`removeAttributeNS` and multi-namespace
    `getAttributeNS` scenarios that rely on two attributes sharing a local
    name but differing only by namespace are also blocked by it, since
    domonic's attribute storage is a flat `name -> value` map.
  - `Attr.value` is not "live": mutating it after `setAttributeNode()` does
    not update the owning element's attribute, and vice versa. Each is an
    independent copy rather than a shared slot. `setAttributeNode()` now at
    least records `attr.ownerElement`, but does not yet return/detach a
    replaced same-name `Attr`, since domonic's `NamedNodeMap` does not keep
    a stable `Attr` identity per attribute slot (it builds a fresh `Attr` on
    every `.attributes` access).
  - `NodeIterator` has no "pre-removing steps" -- its `referenceNode` /
    `pointerBeforeReferenceNode` do not adjust when a node is removed from
    the tree elsewhere, the same class of gap as `Range`'s live boundary
    points.

## Adding a port

1. Grab the upstream body:
   `wpt/dom/nodes/<Name>.html` → the largest `<script>` block.
2. New `test_dom_<name>.py`, one method per `test()` block, docstring = the
   upstream test name, module-level `document = Document()`.
3. Translate `document.createElement` etc. straight across; `for (var i…)`
   loops become Python loops; `assert_*` come from `_harness`.
4. Run. Fix bugs; xfail deviations with a reason.
