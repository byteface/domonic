# Reliq integration benchmark

Local run on macOS arm64, Python 3.13, Reliq 0.0.48, using
`benchmarks/html_meaty_page.html` (500,994 UTF-8 bytes / 498,579 characters).

| Operation | Median milliseconds |
| --- | ---: |
| Reliq native parsing | 0.788 |
| Selectolax Lexbor native parsing | 5.822 |
| Original Reliq public-API adapter | 111.222 |
| Optimized Reliq through domonic.parseString | 22.438 |
| Selectolax through domonic.parseString | 28.835 |
| TurboHTML through domonic.parseString | 20.894 |
| lxml_html through domonic.parseString | 36.034 |
| html.parser through domonic.parseString | 67.987 |
| Local htmlparser2 domonic adapter | 87.790 |

The optimized Reliq conversion is about 5 times faster than the original
public-API adapter in this run. It beats Selectolax and is within about 7%
of TurboHTML's elapsed time. The previous optimization pass measured 41.6 ms;
bulk packed-array reads bring that down to 22.4 ms.
Native parsing still wins, but traversal and construction dominate the total.

These measurements use 21 iterations after one warmup, with `gc.collect()`
before each iteration and cyclic GC disabled during timing. Native operations
are `reliq(source)` and `LexborHTMLParser(source)`. The public adapter includes
native parsing followed by the original recursive conversion. Other integrated
operations use `domonic.parseString(source, parser=...)`, except htmlparser2,
which calls its local `domonic_adapter.parse` directly without installing the
monkeypatch. The local htmlparser2 source was read from `domonic-ui/src`.

Results are local observations, not equivalent-tree or HTML5 conformance claims.
Reliq preserves its own recovery semantics. Regression tests compare all nodes,
attributes, namespaces, text, doctypes and parent links between its optimized
and public adapters, including this entire fixture.

## What changed

The original profile spent most of its time in Reliq's wrapper traversal,
repeated native node conversion and attribute access. The optimized adapter:

- Walks the native preorder array once, using a stack to assemble child tuples.
- Bulk-copies the native node and attribute arrays, then unpacks records in
  Python without per-record foreign-function calls. A one-record lookahead
  avoids materializing a Python list of every node.
- Checks version, byte order, record sizes and a layout probe before using
  packed reads; keeps Reliq's ctypes conversion functions as a fallback.
- Reads strings using source byte offsets instead of repeated `string_at` calls.
- Caches tag and attribute names within each parse.
- Uses the existing raw DOM constructors and the common HTML namespace fast path.
- Decodes entities only when needed, preserving duplicate-attribute semantics.

The stack assembly follows the same approach as the htmlparser2 raw handler.
No HTML is serialized and reparsed. No native pointer is retained in the DOM.
The fast path uses private bindings, so it is enabled only for checked Reliq
0.0.48. Unrecognized layouts of that version use its C conversion functions;
other versions use the public API. This avoids assuming that an unknown build
has the same private interface. Reliq remains outside the auto cascade.

## Reproduce

```sh
python scripts/benchmark_reliq.py --iterations 21
# Also compare a local checkout containing the htmlparser2 package:
python scripts/benchmark_reliq.py --iterations 21 --htmlparser2-path /path/to/domonic-libs/src
```

The regular benchmark includes Reliq and leaves GC enabled:

```sh
python scripts/benchmark_parsers.py --iterations 21 --parsers reliq selectolax turbohtml lxml_html
```

## Normal GC-enabled run

The regular benchmark with 21 iterations produced these medians (no explicit
warmup or GC control): Reliq **27.25 ms**, Selectolax **33.40 ms**, TurboHTML
**25.75 ms**, and lxml_html **40.58 ms**. Garbage-collection pauses affect the
means much more than these medians. Timings vary between runs; this is a single
fixture and does not establish an overall winner across workloads.
