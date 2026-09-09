"""Conservative compilation of domonic HTML views with optional disk bytecode caching.

Compile after setting DOMConfig and before serving requests. Supported views
return HTML directly without constructing nodes. Unsupported Python remains a
normal view, exposed through ``original`` and ``fallback_reason``.
"""

from __future__ import annotations

import ast
import copy
import functools
import inspect
import textwrap
from collections.abc import Iterable

from domonic.dom import (
    DOMConfig,
    Node,
    RawHTML,
    Text,
    _ATTRIBUTE_NAME_REMAP,
    _BOOLEAN_ATTRIBUTES,
    _HTML_RAWTEXT_ELEMENTS,
    _dom_config_render_fingerprint,
    _escape_html,
    _normalize_alpine_attribute,
    _normalize_htmx_attribute,
    _render_attribute_value,
)
import importlib

from domonic._ssr_cache import compiled_code

raw = RawHTML

_html = importlib.import_module("domonic.html")
_TAGS = {
    value
    for value in vars(_html).values()
    if isinstance(value, type) and issubclass(value, Node) and "name" in value.__dict__
}
# form sets its tag name on instances instead of on the class.
_TAGS.add(_html.form)
_OPTIONAL = frozenset(
    "html head body p dt dd li option thead th tbody tr td tfoot colgroup".split()
)


class UnsupportedView(ValueError):
    """A view cannot safely use the supported AST subset."""


def _text(value):
    if type(value) is str:
        return _escape_html(value) if DOMConfig.GLOBAL_AUTOESCAPE else value
    if callable(value) and not isinstance(value, (Node, str)):
        value = value()
    if isinstance(value, RawHTML):
        return str(value)
    if isinstance(value, Text):
        text = str(value.textContent)
        return (
            _escape_html(text)
            if (
                DOMConfig.GLOBAL_AUTOESCAPE
                or getattr(value, "_escape_text_on_render", False)
            )
            else text
        )
    if isinstance(value, Node):
        # A runtime-supplied DOM is an explicit subtree fallback.
        return str(value)
    if not isinstance(value, (str, bytes, bytearray, dict)) and isinstance(
        value, Iterable
    ):
        return "".join(_text(item) for item in value)
    value = str(value)
    return _escape_html(value) if DOMConfig.GLOBAL_AUTOESCAPE else value


def _attribute(key, value):
    key = key[1:] if key.startswith("_") else key
    key = _ATTRIBUTE_NAME_REMAP.get(key, key)
    if value is True:
        value = "true"
    elif value is False:
        value = "false"
    if DOMConfig.HTMX_ENABLED:
        normalized = _normalize_htmx_attribute(key)
        if normalized is not None:
            return " " + normalized + "=" + _render_attribute_value(value, escape=True)
    if DOMConfig.ALPINE_ENABLED:
        normalized = _normalize_alpine_attribute(key)
        if normalized is not None:
            return " " + normalized + "=" + _render_attribute_value(value, escape=True)
    if key in _BOOLEAN_ATTRIBUTES and (value == "" or value == key):
        return " " + key
    return " " + key + "=" + _render_attribute_value(value, escape=True)


def _quoted_attribute(value, quote):
    # Standard quoted attributes have no value-dependent delimiter. Keep bool
    # spelling identical to Node.__attributes__, and escape only that delimiter.
    if type(value) is not str:
        value = "true" if value is True else "false" if value is False else str(value)
    value = value.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;")
    return (
        value.replace('"', "&quot;") if quote == '"' else value.replace("'", "&#x27;")
    )


def _attribute_dq(value):
    return _quoted_attribute(value, '"')


def _attribute_sq(value):
    return _quoted_attribute(value, "'")


def _join(parts):
    """Fold adjacent literal chunks into one constant in the generated code."""
    merged = []
    for part in parts:
        if isinstance(part, ast.Constant) and isinstance(part.value, str):
            if merged and isinstance(merged[-1], ast.Constant):
                merged[-1].value += part.value
            elif part.value:
                merged.append(part)
        else:
            merged.append(part)
    if not merged:
        return ast.Constant("")
    if len(merged) == 1:
        return merged[0]
    return ast.JoinedStr(
        [
            part if isinstance(part, ast.Constant) else ast.FormattedValue(part, -1)
            for part in merged
        ]
    )


class _Compiler:
    def __init__(self, env, local_names):
        self.env = env
        self.locals = local_names
        self.tags = {}
        self.helpers = {
            "__domonic_ssr_text": _text,
            "__domonic_ssr_attr": _attribute,
            "__domonic_ssr_attr_dq": _attribute_dq,
            "__domonic_ssr_attr_sq": _attribute_sq,
            "__domonic_ssr_raw": str,
        }

    def tag(self, expr):
        if isinstance(expr, ast.Name) and expr.id not in self.locals:
            value = self.env.get(expr.id)
            if isinstance(value, type) and value in _TAGS:
                self.tags[expr.id] = value
                return value
        return None

    def scalar(self, expr):
        # Unknown calls may build or mutate a DOM. Never speculate by executing
        # them at compile time or retrying a partially executed view.
        for node in ast.walk(expr):
            if isinstance(
                node,
                (
                    ast.Call,
                    ast.Await,
                    ast.Yield,
                    ast.YieldFrom,
                    ast.NamedExpr,
                    ast.Lambda,
                ),
            ):
                raise UnsupportedView(
                    "runtime calls or mutation in a dynamic expression"
                )
            if isinstance(node, ast.Name) and node.id.startswith("__domonic_ssr_"):
                raise UnsupportedView("reserved compiler name")
        return copy.deepcopy(expr)

    def render(self, expr, raw=False):
        slots = []
        parts = self.parts(expr, slots, raw)
        output = _join(parts)
        if not slots:
            return output
        # Bind values in Python argument order (children before attributes),
        # even though attributes appear before children in the HTML output.
        arguments = ast.arguments(
            posonlyargs=[],
            args=[ast.arg(f"__domonic_ssr_v{i}") for i in range(len(slots))],
            kwonlyargs=[],
            kw_defaults=[],
            defaults=[],
        )
        return ast.Call(ast.Lambda(arguments, output), slots, [])

    def slot(self, expression, slots):
        name = ast.Name(f"__domonic_ssr_v{len(slots)}", ast.Load())
        slots.append(expression)
        return name

    def parts(self, expr, slots, raw=False):
        if isinstance(expr, ast.Call):
            if (
                isinstance(expr.func, ast.Name)
                and expr.func.id not in self.locals
                and self.env.get(expr.func.id) is RawHTML
            ):
                if len(expr.args) != 1 or expr.keywords:
                    raise UnsupportedView("raw() expects one value")
                self.tags[expr.func.id] = RawHTML
                value = self.scalar(expr.args[0])
                if isinstance(value, ast.Constant):
                    return [ast.Constant(str(value.value))]
                value = self.slot(value, slots)
                return [
                    ast.Call(ast.Name("__domonic_ssr_raw", ast.Load()), [value], [])
                ]
            tag = self.tag(expr.func)
            if tag is None:
                raise UnsupportedView(
                    "only directly imported HTML element calls are supported"
                )
            if any(isinstance(arg, ast.Starred) for arg in expr.args):
                raise UnsupportedView("starred element arguments")
            if any(kw.arg is None for kw in expr.keywords):
                raise UnsupportedView("expanded attribute dictionaries")
            keys = [
                kw.arg if kw.arg.startswith("_") else "_" + kw.arg
                for kw in expr.keywords
            ]
            if len(set(keys)) != len(keys):
                raise UnsupportedView("duplicate normalized attribute names")
            name = "form" if tag is _html.form else tag.name
            children = []
            for child in expr.args:
                children.extend(
                    self.parts(child, slots, name in _HTML_RAWTEXT_ELEMENTS)
                )
            attrs = []
            for kw in expr.keywords:
                if isinstance(kw.value, ast.Constant):
                    attrs.append(ast.Constant(_attribute(kw.arg, kw.value.value)))
                else:
                    value = self.slot(self.scalar(kw.value), slots)
                    attrs.extend(self.attribute_parts(kw.arg, value))
            opening = [ast.Constant("<" + name), *attrs]
            if issubclass(tag, _html.closed_tag):
                end = (
                    (" />" if DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH else "/>")
                    if DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH
                    else ">"
                )
                # Dynamic arguments still get evaluated, as with a normal call.
                return opening + [ast.Constant(end)]
            closing = (
                "</" + name + ">"
                if (
                    DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS
                    or name not in _OPTIONAL
                    or name in _HTML_RAWTEXT_ELEMENTS
                )
                else ""
            )
            return opening + [ast.Constant(">"), *children, ast.Constant(closing)]
        if isinstance(expr, ast.IfExp):
            value = ast.IfExp(
                self.scalar(expr.test),
                self.render(expr.body, raw),
                self.render(expr.orelse, raw),
            )
            return [self.slot(value, slots)]
        if isinstance(expr, (ast.ListComp, ast.GeneratorExp)) and not raw:
            generators = copy.deepcopy(expr.generators)
            for gen in generators:
                if gen.is_async:
                    raise UnsupportedView("async comprehension")
                gen.iter = self.scalar(gen.iter)
                gen.ifs = [self.scalar(item) for item in gen.ifs]
            value = ast.Call(
                ast.Attribute(ast.Constant(""), "join", ast.Load()),
                [ast.GeneratorExp(self.render(expr.elt), generators)],
                [],
            )
            return [self.slot(value, slots)]
        if isinstance(expr, (ast.List, ast.Tuple)) and not raw:
            return [part for item in expr.elts for part in self.parts(item, slots)]
        if isinstance(expr, ast.Constant):
            return [ast.Constant(str(expr.value) if raw else _text(expr.value))]
        value = self.slot(self.scalar(expr), slots)
        helper = "__domonic_ssr_raw" if raw else "__domonic_ssr_text"
        return [ast.Call(ast.Name(helper, ast.Load()), [value], [])]

    def attribute_parts(self, key, value):
        name = key[1:] if key.startswith("_") else key
        name = _ATTRIBUTE_NAME_REMAP.get(name, name)
        shortcut = None
        if DOMConfig.HTMX_ENABLED:
            shortcut = _normalize_htmx_attribute(name)
        if shortcut is None and DOMConfig.ALPINE_ENABLED:
            shortcut = _normalize_alpine_attribute(name)
        if shortcut is not None:
            name = shortcut
        # Boolean shorthand and type-dependent/unusual quoting retain the
        # general serializer. Common delimiters and names become literals.
        quote = DOMConfig.ATTRIBUTE_QUOTES
        if (quote == '"' or quote == "'") and (
            shortcut is not None or name not in _BOOLEAN_ATTRIBUTES
        ):
            helper = (
                "__domonic_ssr_attr_dq" if quote == '"' else "__domonic_ssr_attr_sq"
            )
            return [
                ast.Constant(" " + name + "=" + quote),
                ast.Call(ast.Name(helper, ast.Load()), [value], []),
                ast.Constant(quote),
            ]
        return [
            ast.Call(
                ast.Name("__domonic_ssr_attr", ast.Load()),
                [ast.Constant(key), value],
                [],
            )
        ]

    def returned(self, value):
        if isinstance(value, ast.IfExp):
            return ast.IfExp(
                self.scalar(value.test),
                self.returned(value.body),
                self.returned(value.orelse),
            )
        if not isinstance(value, ast.Call):
            raise UnsupportedView("return must be an element expression")
        return self.render(value)

    def statements(self, statements):
        result = []
        for statement in statements:
            if isinstance(statement, ast.Return) and statement.value is not None:
                result.append(ast.Return(self.returned(statement.value)))
            elif isinstance(statement, ast.If):
                result.append(
                    ast.If(
                        self.scalar(statement.test),
                        self.statements(statement.body),
                        self.statements(statement.orelse),
                    )
                )
            elif isinstance(statement, ast.Assign) and all(
                isinstance(target, ast.Name) for target in statement.targets
            ):
                result.append(
                    ast.Assign(
                        copy.deepcopy(statement.targets), self.scalar(statement.value)
                    )
                )
            elif isinstance(statement, ast.Expr) and isinstance(
                statement.value, ast.Constant
            ):
                result.append(copy.deepcopy(statement))  # docstring
            else:
                raise UnsupportedView(
                    "unsupported statement: " + type(statement).__name__
                )
        return result


def compile(view, *, strict=False, cache_dir=None):
    """Compile a view (or snapshot an existing DOM) into an HTML callable.

    Uses current DOMConfig settings, including GLOBAL_AUTOESCAPE. Set it True
    for untrusted SSR text/attributes. Configuration changes cause a normal
    rendering fallback until the view is compiled again. ``strict=True`` raises
    UnsupportedView instead of installing an unsupported-view fallback.

    ``original``, ``is_compiled``, ``fallback_reason`` and ``source`` are exposed
    on the result. No view or runtime expression is executed during compilation.
    Optional cache_dir stores generated bytecode in a private (0700) directory;
    cache_hit reports reuse. Source inspection and AST validation still run at
    startup. Request data and globals are never stored in the bytecode cache.
    """
    if isinstance(view, Node):
        try:
            return _snapshot(view, cache_dir=cache_dir)
        except UnsupportedView as exc:
            if strict:
                raise

            def fallback():
                return str(view)

            fallback.cache_hit = False
            fallback.original = view
            fallback.is_compiled = False
            fallback.fallback_reason = str(exc)
            fallback.source = None
            return fallback
    if not inspect.isfunction(view) or inspect.iscoroutinefunction(view):
        raise TypeError(
            "compile expects a synchronous Python view function or DOM node"
        )
    original = view
    reason = None
    try:
        if hasattr(view, "__wrapped__"):
            raise UnsupportedView(
                "wrapped view; compile before applying other decorators"
            )
        source = textwrap.dedent(inspect.getsource(view))
        tree = ast.parse(source)
        function = next(
            (node for node in tree.body if isinstance(node, ast.FunctionDef)), None
        )
        if function is None:
            raise UnsupportedView("source must contain a named function")
        local_names = set(view.__code__.co_varnames)
        local_names.update(
            node.id
            for node in ast.walk(function)
            if isinstance(node, ast.Name) and isinstance(node.ctx, ast.Store)
        )
        if any(name.startswith("__domonic_ssr_") for name in local_names):
            raise UnsupportedView("reserved compiler name")
        closure = inspect.getclosurevars(view)
        env = dict(view.__globals__, **closure.nonlocals)
        compiler = _Compiler(env, local_names)
        function = copy.deepcopy(function)
        function.decorator_list = []
        function.returns = None
        function.body = compiler.statements(function.body)
        if not function.body or not isinstance(function.body[-1], ast.Return):
            function.body.append(ast.Return(ast.Constant("None")))
        # Defaults and annotations are preserved from the original, never evaluated again.
        function.args.defaults = []
        function.args.kw_defaults = [None] * len(function.args.kwonlyargs)
        for node in ast.walk(function.args):
            if isinstance(node, ast.arg):
                node.annotation = None
        module = ast.fix_missing_locations(ast.Module([function], []))
        namespace = dict(env, **compiler.helpers)
        generated_source = ast.unparse(module)
        code, cache_hit = compiled_code(
            generated_source,
            "<domonic-compiled:" + view.__name__ + ">",
            "exec",
            cache_dir,
        )
        # ``code`` is compiled from ``ast.unparse`` of the developer's own view
        # function AST (rewritten by ``_Compiler``); ``namespace`` is that
        # function's own module globals and closure. No external/request input
        # reaches here -- this is build-time codegen, like dataclasses' __init__.
        exec(code, namespace)  # nosec B102
        renderer = namespace[function.name]
        renderer.__defaults__ = view.__defaults__
        renderer.__kwdefaults__ = view.__kwdefaults__
        fingerprint = _dom_config_render_fingerprint()
        global_names = {
            node.id
            for node in ast.walk(function)
            if isinstance(node, ast.Name)
            and isinstance(node.ctx, ast.Load)
            and node.id in view.__globals__
            and node.id not in local_names
        }
        cells = dict(zip(view.__code__.co_freevars, view.__closure__ or ()))
    except (OSError, IOError, SyntaxError, UnsupportedView) as exc:
        if strict:
            raise UnsupportedView(str(exc)) from exc
        reason = str(exc)

    @functools.wraps(original)
    def compiled(*args, **kwargs):
        if reason is not None:
            return str(original(*args, **kwargs))
        if _dom_config_render_fingerprint() != fingerprint:
            return str(original(*args, **kwargs))
        for name in global_names:
            if name not in original.__globals__:
                return str(original(*args, **kwargs))
            namespace[name] = original.__globals__[name]
        for name, cell in cells.items():
            namespace[name] = cell.cell_contents
        if any(namespace.get(name) is not tag for name, tag in compiler.tags.items()):
            return str(original(*args, **kwargs))
        return renderer(*args, **kwargs)

    compiled.cache_hit = cache_hit if reason is None else False
    compiled.original = original
    compiled.is_compiled = reason is None
    compiled.fallback_reason = reason
    compiled.source = generated_source if reason is None else None
    return compiled


def _snapshot(view, *, cache_dir=None):
    """Freeze concrete markup while retaining lazy callable children."""
    namespace = {"__domonic_ssr_text": _text}

    def parts(node):
        if isinstance(node, Text):
            return [ast.Constant(_text(node))]
        if isinstance(node, Node):
            if type(node) not in _TAGS:
                raise UnsupportedView("snapshot requires standard HTML elements")
            opening = "<" + node.name + node.__attributes__
            if isinstance(node, _html.closed_tag):
                end = (
                    (" />" if DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH else "/>")
                    if DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH
                    else ">"
                )
                return [ast.Constant(opening + end)]
            children = []
            for child in node.args:
                if node.name in _HTML_RAWTEXT_ELEMENTS and not isinstance(child, Node):
                    children.append(ast.Constant(str(child)))
                else:
                    children.extend(parts(child))
            closing = (
                "</" + node.name + ">"
                if (
                    DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS
                    or node.name not in _OPTIONAL
                    or node.name in _HTML_RAWTEXT_ELEMENTS
                )
                else ""
            )
            return [ast.Constant(opening + ">"), *children, ast.Constant(closing)]
        if callable(node):
            key = "__domonic_ssr_lazy" + str(len(namespace))
            namespace[key] = node
            return [
                ast.Call(
                    ast.Name("__domonic_ssr_text", ast.Load()),
                    [ast.Name(key, ast.Load())],
                    [],
                )
            ]
        if isinstance(node, (list, tuple)):
            return [part for child in node for part in parts(child)]
        if isinstance(node, Iterable) and not isinstance(
            node, (str, bytes, bytearray, dict)
        ):
            raise UnsupportedView(
                "snapshot requires concrete children, not an iterator"
            )
        return [ast.Constant(_text(node))]

    expression = ast.Expression(
        ast.Lambda(
            ast.arguments(
                posonlyargs=[], args=[], kwonlyargs=[], kw_defaults=[], defaults=[]
            ),
            _join(parts(view)),
        )
    )
    expression = ast.fix_missing_locations(expression)
    code, cache_hit = compiled_code(
        ast.unparse(expression), "<domonic-snapshot>", "eval", cache_dir
    )
    # ``code`` is a lambda AST that domonic synthesised from the rendered DOM
    # tree (string ``ast.Constant``s plus calls to the helpers in ``namespace``);
    # nothing is parsed from a string. Build-time codegen, no external input.
    renderer = eval(code, namespace)  # nosec B307
    renderer.cache_hit = cache_hit
    renderer.original = view
    renderer.is_compiled = True
    renderer.fallback_reason = None
    renderer.source = ast.unparse(expression)
    return renderer


class CompiledRoutes:
    """Opt-in mixin for apps with a Flask-style ``view_functions`` dictionary.

    Call ``app.compile()`` after registering routes and before serving. Only
    supported handlers are replaced; unsupported handlers remain untouched,
    preserving framework response objects, tuples and other return protocols.
    Other routing systems should register ``compile(view)`` explicitly.
    """

    def compile(self, *, strict=False, cache_dir=None):
        handlers = self.view_functions
        if not isinstance(handlers, dict):
            raise TypeError("CompiledRoutes requires a view_functions dictionary")
        compiled_views = {}
        for endpoint, handler in handlers.items():
            if getattr(handler, "is_compiled", False):
                original = handler.original
            else:
                original = handler
            if not inspect.isfunction(original) or inspect.iscoroutinefunction(
                original
            ):
                continue
            compiled_views[endpoint] = compile(
                original, strict=strict, cache_dir=cache_dir
            )
        # Build everything before changing registration (strict mode is atomic).
        for endpoint, renderer in compiled_views.items():
            if renderer.is_compiled:
                handlers[endpoint] = renderer
        self.compiled_views = compiled_views
        return self


def compiled(view=None, *, strict=False, cache_dir=None):
    """Compile immediately at definition time, with optional compiler settings.

    Use ``@compiled`` or ``@compiled(strict=True, cache_dir=...)``. This is
    convenience syntax for ``compile(view)``; it has the same supported views,
    escaping, fallback and synchronous-function requirements. No request-time
    initialization is performed. ``__original__`` retains the uncompiled view.
    """

    def decorate(original):
        renderer = compile(original, strict=strict, cache_dir=cache_dir)
        renderer.__original__ = original
        return renderer

    return decorate if view is None else decorate(view)
