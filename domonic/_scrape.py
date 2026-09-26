"""
domonic._scrape
====================================

``scrape()`` -- the Pythonic front door for pulling a web page, or many, and
getting straight at the content.

``scrape(url)`` returns a parsed domonic DOM. ``to=`` swaps that for raw text,
JSON or PyML. ``selector=`` returns the matched element. ``response=True`` also
hands back the underlying :class:`domonic.webapi.fetch.Response` as
``(response, result)`` so status and headers stay one unpack away.

Everything here is a thin layer over :mod:`domonic.webapi.fetch`; the batch form
reuses that module's pooled fetch and preserves input order. The name is exposed
as ``domonic.scrape`` and ``from domonic import scrape``.
"""

from __future__ import annotations

import re

from typing import Any
from urllib.parse import urljoin, urlparse

_TO_CHOICES = ("text", "json", "pyml", "dom")
_ERROR_CHOICES = ("raise", "return")

# Keyword arguments whose names match ``Request`` fields are used to build the
# request; everything else is forwarded to ``requests``. Resolved once from the
# ``Request`` signature so the two stay in step.
_REQUEST_FIELDS: set[str] | None = None

# Cross-origin stylesheet requests must not inherit credentials intended for
# the page request. These transport-only options are safe/useful to retain.
_CROSS_ORIGIN_CSS_KWARGS = frozenset(("timeout", "verify", "proxies", "allow_redirects"))


class ScrapeHTTPError(RuntimeError):
    """Raised by ``scrape(..., raise_for_status=True)`` for a non-2xx response."""

    def __init__(self, response: Any) -> None:
        self.response = response
        status = getattr(response, "status", None)
        status_text = getattr(response, "statusText", "") or ""
        url = getattr(response, "url", "") or ""

        detail = " ".join(part for part in (str(status) if status is not None else "", status_text) if part)
        message = f"HTTP {detail}" if detail else "HTTP request failed"
        if url:
            message += f" for {url}"
        super().__init__(message)


def _request_fields() -> set[str]:
    global _REQUEST_FIELDS
    if _REQUEST_FIELDS is None:
        import inspect

        from domonic.webapi.fetch import Request

        names = {
            name
            for name, param in inspect.signature(Request.__init__).parameters.items()
            if param.kind not in (param.VAR_POSITIONAL, param.VAR_KEYWORD)
        }
        names.discard("self")
        names.discard("url")
        names.discard("init")
        names.add("json")  # accepted by Request via ``init``
        _REQUEST_FIELDS = names
    return _REQUEST_FIELDS


def _make_request(target: Any, init: dict[str, Any]) -> Any:
    from domonic.webapi.fetch import Request

    # Request(Request(...), init=...) deliberately clones the request while
    # applying any explicit scrape() overrides.
    return Request(target, init=dict(init))


def _fetch_request(request: Any, request_kwargs: dict[str, Any]) -> Any:
    from domonic.webapi.fetch import fetch

    promise = fetch(request, **request_kwargs)
    if promise.state == "rejected":
        error = promise.data
        if isinstance(error, BaseException):
            raise error
        raise RuntimeError(error)
    return promise.data


def _fetch_many(requests: list[Any], request_kwargs: dict[str, Any]) -> list[Any]:
    from domonic.webapi.fetch import fetch_pooled

    return list(fetch_pooled(requests, **request_kwargs))


def _http_error(response: Any) -> ScrapeHTTPError | None:
    if getattr(response, "ok", True) is False:
        return ScrapeHTTPError(response)
    return None


def _origin(url: str) -> tuple[str, str, int | None] | None:
    try:
        parsed = urlparse(url)
        if not parsed.scheme or not parsed.hostname:
            return None
        port = parsed.port
    except (TypeError, ValueError):
        return None

    scheme = parsed.scheme.lower()
    if port is None:
        if scheme == "http":
            port = 80
        elif scheme == "https":
            port = 443

    return scheme, parsed.hostname.lower(), port


def _same_origin(left: str, right: str) -> bool:
    left_origin = _origin(left)
    right_origin = _origin(right)
    return left_origin is not None and left_origin == right_origin


def _document_base_url(document: Any) -> str:
    page_url = str(getattr(document, "URL", "") or "")
    base_uri = str(getattr(document, "baseURI", "") or "")
    return urljoin(page_url, base_uri) if base_uri else page_url


def _stylesheet_request(
    href: str,
    source_request: Any,
    request_kwargs: dict[str, Any],
) -> tuple[Any, dict[str, Any]]:
    source_url = str(getattr(source_request, "url", "") or "")
    same_origin = _same_origin(source_url, href)

    init: dict[str, Any] = {"method": "GET"}

    # Match the source request's redirect behaviour, but never inherit its body.
    redirect = getattr(source_request, "redirect", None)
    if redirect is not None:
        init["redirect"] = redirect

    # Authentication/cookie/custom headers are only inherited by same-origin
    # stylesheets. Cross-origin CSS starts with a clean header set.
    if same_origin:
        headers = getattr(source_request, "headers", None)
        if headers is not None:
            init["headers"] = headers

    fetch_kwargs = dict(request_kwargs)
    for key in ("params", "data", "json", "files"):
        fetch_kwargs.pop(key, None)

    if not same_origin:
        fetch_kwargs = {
            key: value
            for key, value in fetch_kwargs.items()
            if key in _CROSS_ORIGIN_CSS_KWARGS
        }

    return _make_request(href, init), fetch_kwargs


def _fetch_stylesheet_text(
    href: str,
    source_request: Any,
    request_kwargs: dict[str, Any],
) -> str | None:
    try:
        request, fetch_kwargs = _stylesheet_request(href, source_request, request_kwargs)
        response = _fetch_request(request, fetch_kwargs)
    except Exception:
        return None

    if getattr(response, "ok", True) is False:
        return None
    return response.text()


def _replace_stylesheet_rules(sheet: Any, css_text: str) -> bool:
    try:
        sheet.replaceSync(css_text)
    except Exception:
        return False
    return True


def _load_external_stylesheets(
    document: Any,
    source_request: Any,
    request_kwargs: dict[str, Any] | None = None,
) -> None:
    sheets = document.styleSheets
    fetch_kwargs = dict(request_kwargs or {})
    base_url = _document_base_url(document)

    for sheet in sheets:
        href = getattr(sheet, "href", None)
        owner_node = getattr(sheet, "ownerNode", None)
        if not href or getattr(owner_node, "tagName", "").lower() != "link":
            continue
        if len(getattr(sheet, "cssRules", ()) or ()):
            continue

        resolved_href = urljoin(base_url, href)
        sheet._original_href = href
        sheet._resolved_href = resolved_href
        sheet.href = resolved_href

        css_text = _fetch_stylesheet_text(resolved_href, source_request, fetch_kwargs)
        if css_text is not None:
            _replace_stylesheet_rules(sheet, css_text)


def _charset_from_headers(response: Any) -> str | None:
    headers = getattr(response, "headers", None)
    getter = getattr(headers, "get", None)
    content_type = getter("content-type") if callable(getter) else None
    if not content_type:
        return None
    match = re.search(r"charset\s*=\s*[\"']?([A-Za-z0-9_.:-]+)", str(content_type), re.I)
    return match.group(1) if match else None


def _parse(
    response: Any,
    parser: str | None,
    *,
    source_request: Any,
    css: bool = False,
    attach: bool = False,
    request_kwargs: dict[str, Any] | None = None,
) -> Any:
    from domonic import domonic

    raw = response.bytes() if callable(getattr(response, "bytes", None)) else None
    if isinstance(raw, (bytes, bytearray, memoryview)):
        document = domonic.parseString(
            bytes(raw), parser=parser, document=True, encoding=_charset_from_headers(response)
        )
    else:
        document = domonic.parseString(response.text(), parser=parser, document=True)
    document.URL = getattr(response, "url", "") or getattr(document, "URL", "")
    if css:
        _load_external_stylesheets(document, source_request, request_kwargs)
    if attach:
        from domonic.window import Window

        Window().attach(document)
    return document


def _result(
    response: Any,
    to: str | None,
    selector: str | None,
    all_: bool,
    parser: str | None,
    *,
    source_request: Any,
    css: bool = False,
    attach: bool = False,
    request_kwargs: dict[str, Any] | None = None,
) -> Any:
    if selector is not None:
        dom = _parse(
            response,
            parser,
            source_request=source_request,
            css=css,
            attach=attach,
            request_kwargs=request_kwargs,
        )
        return dom.querySelectorAll(selector) if all_ else dom.querySelector(selector)

    if to is None or to == "dom":
        return _parse(
            response,
            parser,
            source_request=source_request,
            css=css,
            attach=attach,
            request_kwargs=request_kwargs,
        )

    if to == "text":
        return response.text()

    if to == "json":
        return response.json()

    from domonic import domonic

    return domonic.parse(response.text())


def _successful_result(
    request: Any,
    response: Any,
    *,
    to: str | None,
    selector: str | None,
    all_: bool,
    parser: str | None,
    include_response: bool,
    css: bool,
    attach: bool,
    request_kwargs: dict[str, Any],
) -> Any:
    # Parsing/decoding consumes a Fetch Response body. When the caller asks for
    # the Response too, consume a clone so the returned Response remains unused.
    source_response = response.clone() if include_response else response

    result = _result(
        source_response,
        to,
        selector,
        all_,
        parser,
        source_request=request,
        css=css,
        attach=attach,
        request_kwargs=request_kwargs,
    )
    return (response, result) if include_response else result


def scrape(
    url: Any,
    *,
    to: str | None = None,
    selector: str | None = None,
    all: bool = False,
    response: bool = False,
    parser: str | None = None,
    headers: Any = None,
    params: Any = None,
    timeout: Any = 30,
    method: str | None = None,
    css: bool = False,
    attach: bool = False,
    raise_for_status: bool = False,
    errors: str = "raise",
    **kwargs: Any,
) -> Any:
    """Fetch one or more web resources and return their content directly.

    ``url`` is a URL string or a ``domonic.webapi.fetch.Request``; an iterable
    of either fetches them all.

    ``scrape(url)`` returns a parsed domonic DOM -- query it straight away with
    ``.querySelector(...)``.

    ``scrape(url, to="text" | "json" | "pyml" | "dom")`` returns just that.

    ``css=True`` eagerly populates ``document.styleSheets`` for DOM results.
    Same-origin stylesheet requests inherit the page request's headers and
    transport options; cross-origin stylesheet requests do not inherit page
    credentials or custom headers.

    ``attach=True`` attaches DOM results to a new :class:`domonic.window.Window`
    so ``document.defaultView`` and ``window.getComputedStyle(...)`` are ready.

    ``scrape(url, selector="article")`` returns the matched element (or
    ``None``); add ``all=True`` for every match.

    ``scrape(url, response=True)`` returns ``(response, result)`` where
    ``response`` is the :class:`domonic.webapi.fetch.Response` (``.status``,
    ``.headers``, ``.ok``, ``.text()``, ``.json()``). The returned response body
    remains unused because the result is produced from a clone.

    ``raise_for_status=True`` turns non-2xx responses into
    :class:`ScrapeHTTPError`.

    ``errors="raise"`` raises fetch/status errors. ``errors="return"`` returns
    the exception in that result position instead. For batches this preserves
    input order and list length.

    Pass an iterable of URLs to fetch them through the pooled fetch, in input
    order; the result is a list of whatever a single URL would have returned
    (a list of ``(response, result)`` pairs when ``response=True``).

    ``method`` and ``headers`` build the request, as does any keyword argument
    that names a ``Request`` field (``body``, ``json``, ``credentials``,
    ``redirect``, ...). When ``url`` is already a ``Request``, explicit values
    supplied to ``scrape`` override the corresponding fields while omitted
    values are preserved. URL strings default to GET via ``Request``.

    ``params``, ``timeout`` and any remaining keyword arguments are forwarded
    to ``requests``.
    """
    if to is not None and to not in _TO_CHOICES:
        raise ValueError(f"scrape(to=...) must be one of {', '.join(_TO_CHOICES)}; got {to!r}")
    if to is not None and selector is not None:
        raise ValueError("pass either scrape(to=...) or scrape(selector=...), not both")
    if all and selector is None:
        raise ValueError("scrape(all=True) needs a selector=")
    if errors not in _ERROR_CHOICES:
        raise ValueError(f"scrape(errors=...) must be one of {', '.join(_ERROR_CHOICES)}; got {errors!r}")

    from domonic.webapi.fetch import Request

    init: dict[str, Any] = {}
    if method is not None:
        init["method"] = method
    if headers is not None:
        init["headers"] = headers

    for key in [name for name in kwargs if name in _request_fields()]:
        init[key] = kwargs.pop(key)

    request_kwargs = dict(kwargs)
    if params is not None:
        request_kwargs["params"] = params
    if timeout is not None:
        request_kwargs["timeout"] = timeout

    if isinstance(url, (str, Request)):
        request = _make_request(url, init)

        try:
            resp = _fetch_request(request, request_kwargs)
            if raise_for_status:
                error = _http_error(resp)
                if error is not None:
                    raise error
            return _successful_result(
                request,
                resp,
                to=to,
                selector=selector,
                all_=all,
                parser=parser,
                include_response=response,
                css=css,
                attach=attach,
                request_kwargs=request_kwargs,
            )
        except Exception as exc:
            if errors == "return":
                return exc
            raise

    requests = [_make_request(target, init) for target in url]
    fetched = _fetch_many(requests, request_kwargs)

    results: list[Any] = []
    for request, item in zip(requests, fetched):
        error: BaseException | None = item if isinstance(item, BaseException) else None

        if error is None and raise_for_status:
            error = _http_error(item)

        if error is not None:
            if errors == "raise":
                raise error
            results.append(error)
            continue

        results.append(
            _successful_result(
                request,
                item,
                to=to,
                selector=selector,
                all_=all,
                parser=parser,
                include_response=response,
                css=css,
                attach=attach,
                request_kwargs=request_kwargs,
            )
        )

    return results
