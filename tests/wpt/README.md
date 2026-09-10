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

`Node-isEqualNode`, `Node-nodeValue`, `Node-contains`, `ChildNode-replaceWith`
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
propagation, once, handleEvent, CustomEvent).

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
  snapshot.)
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

## Adding a port

1. Grab the upstream body:
   `wpt/dom/nodes/<Name>.html` → the largest `<script>` block.
2. New `test_dom_<name>.py`, one method per `test()` block, docstring = the
   upstream test name, module-level `document = Document()`.
3. Translate `document.createElement` etc. straight across; `for (var i…)`
   loops become Python loops; `assert_*` come from `_harness`.
4. Run. Fix bugs; xfail deviations with a reason.
