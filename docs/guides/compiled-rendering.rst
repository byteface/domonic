Compiled Server-Side Rendering
==============================

``domonic.compile(view)`` inspects a Python function at startup and builds a
specialized HTML renderer. Literal markup is folded into strings; dynamic text
and attributes remain Python expressions. Supported request paths construct no
DOM nodes. Renderers stay in memory during requests. An optional disk bytecode cache can
reuse generated code across server restarts.

Definition-time decorator
-------------------------

For a standalone view, ``@compiled`` is convenience syntax for
``home = compile(home)``. It compiles immediately when Python defines the function,
so even the first call uses the prepared renderer. No application, lifespan,
route registry or renderer dictionary is needed.

.. code-block:: python

   from domonic import compiled
   from domonic.dom import DOMConfig
   from domonic.html import html, body, h1, p

   DOMConfig.GLOBAL_AUTOESCAPE = True  # set before defining compiled views

   @compiled
   def home(name="World"):
       return html(body(h1("Hello"), p(name)))

   print(home())

Run the tiny, framework-free example with
``python -m examples.ssr.decorated_view``. The advanced server example remains
available separately as ``examples.ssr.compiled_views``.

The default is memory-only. ``@compiled(strict=True, cache_dir="/tmp/domonic")``
passes those settings directly to the existing compiler, including its private
directory requirements. ``@compiled()`` also works. Metadata and the inspectable
signature are preserved; ``home.__original__`` (also ``home.original`` and
``home.__wrapped__``) references the uncompiled function. ``is_compiled``,
``fallback_reason``, ``source`` and ``cache_hit`` remain available.

Escaping, supported syntax, fallback and error behavior are identical to
``compile(view)``. Unsupported views fall back by default; use ``strict=True``
to require compilation at import time. Async views remain unsupported, matching
the existing compiler. The explicit ``compile(view)`` API is unchanged.

A working example
-----------------

.. code-block:: python

   from types import SimpleNamespace
   from domonic import compile
   from domonic.dom import DOMConfig
   from domonic.html import div, h1, p

   DOMConfig.GLOBAL_AUTOESCAPE = True

   def profile(user):
       return div(h1("Profile"), p(user.name, _class="bio"))

   compiled = compile(profile, strict=True)  # startup, before serving requests
   print(compiled(SimpleNamespace(name="Alice & Bob")))
   # <div><h1>Profile</h1><p class="bio">Alice &amp; Bob</p></div>

   print(compiled.source)    # generated Python for review/debugging
   assert compiled.original is profile

Run the FastAPI/Uvicorn example with
``python -m examples.ssr.compiled_views``, then open ``http://127.0.0.1:8000/``.
The example provides ``/``, ``/profile``, ``/dashboard`` and ``/large`` routes.
It requires the optional ``fastapi`` and ``uvicorn`` packages.
Functions must have inspectable source (normally a ``.py`` file). Lambdas and
functions defined with ``exec`` typically fall back. Compilation never calls the
view or re-evaluates its defaults or decorators.

Escaping follows normal domonic serialization: attributes are escaped, while
text follows ``DOMConfig.GLOBAL_AUTOESCAPE`` (False by default). Enable it for
untrusted SSR text. Script/style content remains raw, as in normal rendering;
entity escaping does not make arbitrary values safe JavaScript or CSS.
Configuration changes after compilation cause ordinary view rendering until
recompilation. Do not change global rendering settings during requests.

Routes
------

For individual routes, register the compiled callable. Decorator order matters:

.. code-block:: python

   @app.route("/profile")
   @compile
   def profile():
       return div(h1("Profile"))

For applications with a Flask-style ``view_functions`` dictionary, the optional
mixin supplies ``app.compile()``:

.. code-block:: python

   from flask import Flask
   from domonic.ssr import CompiledRoutes

   class App(CompiledRoutes, Flask):
       pass

   app = App(__name__)

   @app.route("/")
   def home():
       return div(h1("Hello"))

   app.compile()  # after registering all routes, before starting the server
   for endpoint, renderer in app.compiled_views.items():
       print(endpoint, renderer.is_compiled, renderer.fallback_reason)

Only supported handlers are replaced. Unsupported handlers retain their exact
original behavior, including framework response objects and tuples. This mixin
is not a universal adapter for FastAPI/Starlette or other route registries;
register compiled views explicitly with those frameworks.

Supported code and fallback
---------------------------

The initial compiler supports directly imported standard HTML constructors
(including aliases), scalar expressions, simple assignments, ``if``/``else``,
conditional expressions, nested list/generator comprehensions over supplied
iterables, and explicit list/tuple children. Comprehensions generate HTML
strings, not intermediate DOMs. Static text, attributes, and adjoining tag
boundaries are folded together.

Unknown function/method calls, DOM mutation, imperative loops, custom elements,
expanded ``*args``/``**kwargs``, wrapped functions and complex statements use
normal rendering. Async functions are not supported by this API. Use
``strict=True`` to reject unsupported views at startup; otherwise inspect
``is_compiled`` and ``fallback_reason``. Runtime exceptions propagate without
retrying the view, so side effects are not duplicated.

Scalar child values can also be callables: they are invoked at rendering time,
matching normal domonic behavior. A callable or supplied value that returns an
existing DOM uses ordinary serialization for that subtree. The no-node-creation
guarantee applies to compiled markup; callbacks that create their own DOMs are
outside that guarantee. Keep expressions and comprehensions free of side effects:
compilation combines construction and serialization, so their interleaving can
differ from constructing an entire tree before rendering it.

Existing DOMs
-------------

``compile(existing_dom)`` creates a snapshot of concrete markup. Later mutations
do not affect the snapshot. Callable children remain dynamic and are not called
during compilation. Keep DOMConfig fixed for these snapshots; compile again after
changing it. Custom nodes or iterator children conservatively fall back to normal
serialization (or raise with ``strict=True``).

Cold-render benchmark
---------------------

Run ``python scripts/benchmark_ssr.py --repeats 5``. Every sample starts a fresh
Python process and measures its first render, with no warmup. Imports, input
fixtures and compilation happen before the request timer; startup compilation
is reported separately. Output parity is checked after timing. This measures
view-to-HTML latency, not HTTP/server startup or network time.

On the development machine (Python 3.13), five fresh-process samples per mode
produced these medians. These are examples, not cross-machine guarantees:

=========== ============= =============== ======= ===================
View        Normal (ms)   Compiled (ms)   Speedup Compilation (ms)
=========== ============= =============== ======= ===================
Small       0.068         0.008           8.5x    0.624
Medium      1.436         0.118           12.2x   1.090
Large       29.561        2.333           12.7x   1.200
=========== ============= =============== ======= ===================

The fixtures render 78, 7,811 and 139,919 UTF-8 bytes respectively. Normal rendering
includes both DOM construction and serialization; neither side uses a response
cache. First-request savings exclude startup compilation, which is intentional:
compile before accepting requests.

Disk cache and first-request startup
------------------------------------

.. code-block:: python

   compiled = compile(profile, strict=True, cache_dir="/tmp/my-private-ssr-cache")
   print(compiled.cache_hit)

``cache_dir`` is optional on ``compile(view)``, ``compile(DOM)``, and the
``CompiledRoutes.compile()`` mixin. The directory is created with mode 0700;
an existing directory must also be private and owned by the current user.
The cache contains executable Python bytecode: use an application-owned directory,
not a shared or untrusted folder. Entries are written atomically, keyed by the
generated source, cache format and Python version. Corrupt entries are rebuilt.
Only code and static markup are stored, never runtime globals or request data.
Deleting the directory simply causes compilation on the next startup.

This caches the final Python bytecode compilation step. Source inspection and
AST validation still run at startup, preserving current bindings and fallback
checks. During requests, the callable is already in memory: there is no disk
lookup, compilation or response-cache warmup.

The example uses ``/tmp/domonic-ssr-example-<uid>`` and compiles all four views in
FastAPI's startup lifespan. Uvicorn waits for that lifespan to yield before
accepting requests. The routes only invoke ``app.state.renderers[...]``. Starting
the example again prints disk-cache hits, and the very first request uses the
compiled renderer in both runs. ``strict=True`` makes unsupported markup fail
startup rather than silently serving an uncompiled example.

Explicit trusted HTML
---------------------

.. code-block:: python

   from domonic.html import div, p, raw

   def notice(user_text, trusted_html):
       return div(p(user_text), raw(trusted_html))

``raw(value)`` explicitly marks trusted HTML child content. It works in normal
serialization, compiled views, and DOM snapshots. It creates a string marker,
not a DOM node, and does not sanitize its input. Leave user input unmarked.
Attribute values still escape normally, even when given a raw marker. In the
server example the query parameter is escaped; only the application-owned
``<strong>`` notice is marked raw.

How it works under the hood
---------------------------

The compiler specializes the work normally split between constructing a tree
and serializing it. A normal call builds element objects, sets up their children
and attributes, then walks them to produce HTML. A supported compiled view emits
the same markup directly from Python expressions.

At definition time or explicit compilation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. ``inspect.getsource`` retrieves the view's source. The compiler dedents it and
   parses it with ``ast.parse``. It reads the function's globals and closure
   bindings to identify standard HTML constructors by identity, rather than
   assuming every function named ``div`` is a domonic tag. Shadowed names and
   unknown calls are handled conservatively.
2. The AST pass checks the supported subset before producing a renderer. It
   does not execute the original view, runtime expressions, defaults or
   decorators. Mutation-heavy or otherwise unsupported views become normal
   rendering wrappers, or raise ``UnsupportedView`` with ``strict=True``.
3. Element calls become opening tags, attributes, child expressions and closing
   tags. Literal text and attributes are serialized under the current settings;
   adjacent literal chunks are merged. This is markup folding, not arbitrary
   evaluation of application code at compile time.
4. Dynamic expressions remain in the generated function. Temporary bindings
   preserve child-before-attribute argument evaluation even though attributes
   appear first in the output. Conditionals retain their branch tests, and
   comprehensions join rendered strings instead of constructing element lists.
5. Python's built-in ``compile`` produces bytecode, and ``exec`` creates the
   specialized function in a namespace containing the view's bindings and
   serialization helpers. Original defaults and keyword defaults are restored
   without evaluating their expressions again. A wrapper preserves function
   metadata and performs the runtime compatibility checks described below.

For example:

.. code-block:: python

   def profile(user):
       return div(h1("Profile"), p(user.name, _class="bio"))

The generated renderer has this shape (the helper name below is shortened for
readability):

.. code-block:: python

   def profile(user):
       return (lambda value:
           f'<div><h1>Profile</h1><p class="bio">{text(value)}</p></div>'
       )(user.name)

The complete tag structure is a literal string around one dynamic value.
``text`` applies normal domonic child serialization, including configured
escaping. Dynamic attributes use a separate attribute serializer; they cannot
accidentally inherit the trusted-text behavior of ``raw``. Inspect the actual
code with ``renderer.source`` rather than relying on this illustrative spelling.

On each request
~~~~~~~~~~~~~~~

The wrapper checks that rendering configuration still matches the compilation
settings, refreshes referenced global and closure bindings, and checks that
recognized constructor bindings have not been replaced. A configuration change
or constructor rebinding sends that call through the original view and normal
serialization. Otherwise the generated function evaluates current arguments and
returns HTML immediately. This is why the same compiled function can render
many different users without caching their responses.

``@compiled`` invokes this entire preparation process while the function is
defined and returns the wrapper immediately. It is not a lazy initializer.
The FastAPI example explicitly performs preparation in its startup lifespan
instead; both arrangements prepare the first request in advance.

What the caches contain
~~~~~~~~~~~~~~~~~~~~~~~

The in-memory artifact is a callable with reusable Python code and literal
markup. There is no automatic memoization by request arguments. With
``cache_dir``, the compiler additionally persists generated bytecode using
``marshal`` in private, atomically replaced files. The key hashes the generated
source, cache-format version and Python version/ABI. A checksum detects damaged
entries; directory and file ownership/permissions restrict who can supply the
executable cache contents. A checksum is not a substitute for that trust boundary.

A disk hit skips the final source-to-bytecode step. It still inspects and
transforms the current view at startup to establish its generated source,
current bindings and compatibility checks. Dynamic globals, closures and request
arguments are supplied by the current process, not deserialized from disk.
Static markup is part of the cached code, including concrete markup supplied to
``compile(existing_dom)``. No disk read occurs on the request path.

A DOM snapshot starts from an existing tree rather than function source. It
folds the tree's concrete markup and keeps callable children as dynamic inserts.
The snapshot deliberately does not track later tree mutations. Neither approach
turns arbitrary Python into a pure template: runtime DOM values and callbacks
can still require subtree serialization, and side-effectful expressions should
use ordinary rendering when their construction/serialization ordering matters.

Localisation with gettext
-------------------------

Run ``python -m examples.ssr.localised_view`` for a framework-free example with
bundled French and German gettext catalogs and English source messages. It
compiles one template, then renders English, French, German and English again:
``page.is_compiled`` stays True and the template is never recompiled.

.. code-block:: python

   from functools import partial
   from domonic import compiled
   from domonic.html import div, h1

   @compiled(strict=True)
   def page(hello):
       return div(h1(hello))

   # fr is a gettext.translation(...) catalog, loaded outside the template.
   print(page(partial(fr.gettext, "Hello world")))

``partial`` binds the message but does not translate it yet. The callable child
is invoked when the compiled renderer runs, so the catalog can change between
renders. Ordinary text escaping still applies to the translated result.

A direct ``h1(_("Hello world"))`` inside the view currently uses an unsupported
runtime function call: it falls back to normal rendering, or raises with
``strict=True``. Passing a callable child as above keeps the view compiled.
Alternatively, translate before calling the template and pass the translated
string as a normal dynamic argument. The example's ``.po`` sources and matching
``.mo`` files live in ``examples/ssr/locales``; it needs no external service or
translation package.
