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

from typing import Any

_TO_CHOICES = ("text", "json", "pyml", "dom")

# Keyword arguments whose names match ``Request`` fields are used to build the
# request; everything else is forwarded to ``requests``. Resolved once from the
# ``Request`` signature so the two stay in step.
_REQUEST_FIELDS: set[str] | None = None


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


def _parse(response: Any, parser: str | None) -> Any:
    from domonic import domonic

    return domonic.parseString(response.text(), parser=parser, document=True)


def _result(response: Any, to: str | None, selector: str | None, all_: bool, parser: str | None) -> Any:
    if selector is not None:
        dom = _parse(response, parser)
        return dom.querySelectorAll(selector) if all_ else dom.querySelector(selector)
    if to is None or to == "dom":
        return _parse(response, parser)
    if to == "text":
        return response.text()
    if to == "json":
        return response.json()
    from domonic import domonic

    return domonic.parse(response.text())


def _fetch_one(target: Any, init: dict[str, Any], request_kwargs: dict[str, Any]) -> Any:
    from domonic.webapi.fetch import Request, fetch

    request = target if isinstance(target, Request) else Request(target, init=dict(init))
    promise = fetch(request, **request_kwargs)
    if promise.state == "rejected":
        raise promise.data
    return promise.data


def _fetch_many(urls: Any, init: dict[str, Any], request_kwargs: dict[str, Any]) -> list[Any]:
    from domonic.webapi.fetch import Request, fetch_pooled

    targets = [url if isinstance(url, Request) else Request(url, init=dict(init)) for url in urls]
    responses: list[Any] = []
    for item in fetch_pooled(targets, **request_kwargs):
        if isinstance(item, BaseException):
            raise item
        responses.append(item)
    return responses


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
    method: str = "GET",
    **kwargs: Any,
) -> Any:
    """Fetch one or more web resources and return their content directly.

    ``url`` is a URL string or a ``domonic.webapi.fetch.Request``; an iterable
    of either fetches them all.

    ``scrape(url)`` returns a parsed domonic DOM -- query it straight away with
    ``.querySelector(...)``.

    ``scrape(url, to="text" | "json" | "pyml" | "dom")`` returns just that.

    ``scrape(url, selector="article")`` returns the matched element (or
    ``None``); add ``all=True`` for every match.

    ``scrape(url, response=True)`` returns ``(response, result)`` where
    ``response`` is the :class:`domonic.webapi.fetch.Response` (``.status``,
    ``.headers``, ``.ok``, ``.text()``, ``.json()``).

    Pass an iterable of URLs to fetch them through the pooled fetch, in input
    order; the result is a list of whatever a single URL would have returned
    (a list of ``(response, result)`` pairs when ``response=True``).

    ``method`` and ``headers`` build the request, as does any keyword argument
    that names a ``Request`` field (``body``, ``json``, ``credentials``,
    ``redirect``, ...). ``params``, ``timeout`` and any remaining keyword
    arguments are forwarded to ``requests``.
    """
    if to is not None and to not in _TO_CHOICES:
        raise ValueError(f"scrape(to=...) must be one of {', '.join(_TO_CHOICES)}; got {to!r}")
    if to is not None and selector is not None:
        raise ValueError("pass either scrape(to=...) or scrape(selector=...), not both")
    if all and selector is None:
        raise ValueError("scrape(all=True) needs a selector=")

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
        resp = _fetch_one(url, init, request_kwargs)
        result = _result(resp, to, selector, all, parser)
        return (resp, result) if response else result

    responses = _fetch_many(url, init, request_kwargs)
    results = [_result(resp, to, selector, all, parser) for resp in responses]
    return list(zip(responses, results)) if response else results
