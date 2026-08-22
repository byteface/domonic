"""
domonic.webapi.history
====================================
https://developer.mozilla.org/en-US/docs/Web/API/History
"""

from copy import deepcopy
from dataclasses import dataclass
from pprint import pformat
from urllib.parse import urljoin

from domonic.events import PopStateEvent

_UNSET = object()


def _clone_state(value):
    try:
        return deepcopy(value)
    except Exception:
        return value


@dataclass
class HistoryEntry:
    url: str
    state: object = _UNSET
    title: str = ""

    @property
    def exposed_state(self):
        if self.state is _UNSET:
            return self.url
        return _clone_state(self.state)

    def to_dict(self):
        data = {"url": self.url, "title": self.title}
        if self.state is not _UNSET:
            data["state"] = self.exposed_state
        return data


class History:  # (EventTarget):
    def __init__(self, window=None):
        self.window = window
        self.index = -1
        self.skip_update = False
        self._entries = []
        self._scrollRestoration = "auto"

        href = self._window_href()
        if href:
            self._entries.append(HistoryEntry(href))
            self.index = 0

    def _window_href(self):
        try:
            if self.window is not None:
                return self.window.location.href
        except Exception:
            return None
        return None

    def _current_entry(self):
        if not self._entries or self.index < 0:
            return None
        if self.index >= len(self._entries):
            self.index = len(self._entries) - 1
        return self._entries[self.index]

    def _base_url(self):
        entry = self._current_entry()
        if entry is not None:
            return entry.url
        return self._window_href() or ""

    def _resolve_url(self, url=None):
        if url is None:
            return self._base_url()
        href = url.href if hasattr(url, "href") else str(url)
        return urljoin(self._base_url(), href)

    def _truncate_forward_entries(self):
        if self.index < len(self._entries) - 1:
            del self._entries[self.index + 1 :]

    def _set_window_url_without_load(self, url):
        if self.window is None:
            return

        try:
            location_type = self.window.location.__class__
            self.window._location = location_type(url)
            if getattr(self.window, "_document", None) is not None:
                self.window._document.URL = url
        except Exception:
            return

    def _navigate_to_current_entry(self):
        entry = self._current_entry()
        if entry is None or self.window is None:
            return

        self.skip_update = True
        try:
            self.window.location = entry.url
        finally:
            self.skip_update = False

        self.window.dispatchEvent(
            PopStateEvent("popstate", {"state": entry.exposed_state})
        )

    def _update(self, url: str):
        """Updates the current history state for normal location navigations."""
        if self.skip_update:
            return

        self._truncate_forward_entries()
        self._entries.append(HistoryEntry(self._resolve_url(url)))
        self.index = len(self._entries) - 1

    def back(self):
        """Loads the previous URL in the history list."""
        return self.go(-1)

    def forward(self):
        """Loads the next URL in the history list."""
        return self.go(1)

    def go(self, delta=0):
        """Loads a specific URL from the history list."""
        try:
            delta = int(delta or 0)
        except (TypeError, ValueError):
            delta = 0

        if not self._entries:
            return self.index
        if delta == 0:
            return self.index

        target = self.index + delta
        if target < 0 or target >= len(self._entries):
            return self.index

        self.index = target
        self._navigate_to_current_entry()
        return self.index

    def pushState(self, data, title="", url=None):
        """Pushes data onto the history stack and optionally updates the URL."""
        href = self._resolve_url(url)
        self._truncate_forward_entries()
        self._entries.append(HistoryEntry(href, _clone_state(data), str(title or "")))
        self.index = len(self._entries) - 1
        self._set_window_url_without_load(href)
        return None

    def replaceState(self, data, title="", url=None):
        """Updates the current history entry data and optional URL."""
        href = self._resolve_url(url)
        entry = HistoryEntry(href, _clone_state(data), str(title or ""))
        if self._entries:
            self._entries[self.index] = entry
        else:
            self._entries.append(entry)
            self.index = 0
        self._set_window_url_without_load(href)
        return None

    @property
    def length(self):
        """Returns the number of URLs in the history list."""
        return len(self._entries)

    @property
    def scrollRestoration(self):
        return self._scrollRestoration

    @scrollRestoration.setter
    def scrollRestoration(self, value):
        if value not in ("auto", "manual"):
            raise ValueError("scrollRestoration must be 'auto' or 'manual'")
        self._scrollRestoration = value

    @property
    def state(self):
        entry = self._current_entry()
        return None if entry is None else entry.exposed_state

    @property
    def states(self):
        return [entry.url for entry in self._entries]

    @property
    def entries(self):
        return [entry.to_dict() for entry in self._entries]

    def __len__(self):
        return self.length

    def __repr__(self) -> str:
        return pformat(self.entries)
