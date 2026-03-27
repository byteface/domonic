"""
    domonic.templates
    ====================================
    some builtin templates

"""

from __future__ import annotations

import os
import platform
import sys
from collections.abc import Iterable

from domonic.constants import http_response_status_codes
from domonic.html import *


def _normalize_children(content) -> list:
    if content is None:
        return []
    if isinstance(content, (str, bytes)):
        return [content]
    if isinstance(content, tuple):
        return list(content)
    if isinstance(content, Iterable):
        return list(content)
    return [content]


class _page_template:
    def __init__(self, title_text: str, body_children=None, wholepage: bool = True):
        self.title_text = title_text
        self.wholepage = wholepage
        self.body_node = body(*_normalize_children(body_children))
        self.page = html(head(title(self.title_text), meta(_charset="utf-8")), self.body_node)
        self.content = self.page if wholepage else self.body_node

    def __str__(self) -> str:
        return f"{self.content}"


class status_page(_page_template):
    DEBUG_MODE = False

    def __init__(self, code: int = 404, wholepage: bool = True):
        self.status_code = code
        self.message = http_response_status_codes[code]

        self.status_node = div(_id="status")
        self.status_node += h1(f"{self.status_code}")
        self.status_node += p(self.message)

        super().__init__(f"{self.status_code}", self.status_node, wholepage)


class blank_page(_page_template):
    def __init__(self, title_text: str = "Untitled", content=None, wholepage: bool = True):
        super().__init__(title_text, content, wholepage)


class message_page(_page_template):
    def __init__(
        self,
        title_text: str = "Message",
        heading: str = "Message",
        message: str = "",
        detail: str | None = None,
        wholepage: bool = True,
    ):
        content = div(_id="message")
        content += h1(heading)
        if message:
            content += p(message)
        if detail:
            content += pre(detail)
        super().__init__(title_text, content, wholepage)


class redirect_page(_page_template):
    def __init__(
        self,
        url: str,
        delay: int = 0,
        message: str | None = None,
        wholepage: bool = True,
    ):
        self.url = url
        self.delay = delay
        self.message = message or f"Redirecting to {url}"
        self.wholepage = wholepage

        self.body_node = body(
            div(
                h1("Redirecting"),
                p(self.message),
                p(a(url, _href=url)),
                _id="redirect",
            )
        )
        self.page = html(
            head(
                title("Redirecting"),
                meta(_charset="utf-8"),
                meta(_http_equiv="refresh", _content=f"{delay};url={url}"),
            ),
            self.body_node,
        )
        self.content = self.page if wholepage else self.body_node


class maintenance_page(_page_template):
    def __init__(
        self,
        retry_after: str | None = None,
        message: str = "The service is temporarily unavailable while we carry out maintenance.",
        wholepage: bool = True,
    ):
        content = div(_id="maintenance")
        content += h1("Service Unavailable")
        content += p(message)
        if retry_after:
            content += p(f"Retry after: {retry_after}")
        super().__init__("503", content, wholepage)


class runtime_page(_page_template):
    def __init__(
        self,
        title_text: str = "Runtime Information",
        include_environment: bool = False,
        include_cmd: bool = False,
        wholepage: bool = True,
    ):
        rows = [
            tr(th("Python"), td(sys.version.split()[0])),
            tr(th("Executable"), td(sys.executable)),
            tr(th("Platform"), td(platform.platform())),
            tr(th("Implementation"), td(platform.python_implementation())),
            tr(th("Working Directory"), td(os.getcwd())),
            tr(th("Process ID"), td(str(os.getpid()))),
        ]

        if include_cmd:
            try:
                from domonic.cmd import hostname, whoami

                rows.append(tr(th("Host Name"), td(str(hostname()).strip())))
                rows.append(tr(th("User"), td(str(whoami()).strip())))
            except Exception:
                rows.append(tr(th("Command Info"), td("Unavailable")))

        sections = [
            h1("Runtime Information"),
            table(tbody(*rows), _id="runtime-info"),
        ]

        if include_environment:
            env_rows = [tr(th(key), td(value)) for key, value in sorted(os.environ.items())]
            sections.append(h2("Environment"))
            sections.append(table(tbody(*env_rows), _id="environment-info"))

        super().__init__(title_text, div(*sections, _id="runtime"), wholepage)


__all__ = [
    "blank_page",
    "maintenance_page",
    "message_page",
    "redirect_page",
    "runtime_page",
    "status_page",
]
