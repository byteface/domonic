"""
domonic.webapi.cssfontloading
====================================
https://developer.mozilla.org/en-US/docs/Web/API/CSS_Font_Loading_API
"""

from __future__ import annotations

from typing import Any, Iterable

from domonic.events import Event, EventTarget


def _create_promise():
    from domonic.javascript import Promise

    return Promise()


class FontFace(EventTarget):
    """Server-side representation of a CSS ``@font-face`` source."""

    def __init__(
        self,
        family: str,
        source: str | bytes,
        descriptors: dict[str, Any] | None = None,
    ) -> None:
        super().__init__()
        descriptors = dict(descriptors or {})
        self.family = str(family)
        self.source = source
        self.style = str(descriptors.get("style", "normal"))
        self.weight = str(descriptors.get("weight", "normal"))
        self.stretch = str(descriptors.get("stretch", "normal"))
        self.unicodeRange = str(descriptors.get("unicodeRange", "U+0-10FFFF"))
        self.variant = str(descriptors.get("variant", "normal"))
        self.featureSettings = str(descriptors.get("featureSettings", "normal"))
        self.variationSettings = str(descriptors.get("variationSettings", "normal"))
        self.display = str(descriptors.get("display", "auto"))
        self.status = "unloaded"
        self.onload = None
        self.onerror = None
        self._loaded = _create_promise()

    @property
    def loaded(self):
        return self._loaded

    def load(self):
        self.status = "loading"
        self.dispatchEvent(Event("loading"))
        if self.source in (None, ""):
            self.status = "error"
            error = ValueError("FontFace source is empty")
            self._loaded.reject(error)
            self.dispatchEvent(Event("error"))
            return self._loaded
        self.status = "loaded"
        self._loaded.resolve(self)
        self.dispatchEvent(Event("load"))
        return self._loaded

    def toCSS(self) -> str:
        source = (
            self.source.decode("utf-8", "replace")
            if isinstance(self.source, bytes)
            else str(self.source)
        )
        lines = [
            "@font-face {",
            f"  font-family: {self.family};",
            f"  src: {source};",
            f"  font-style: {self.style};",
            f"  font-weight: {self.weight};",
            f"  font-stretch: {self.stretch};",
            f"  font-display: {self.display};",
            "}",
        ]
        return "\n".join(lines)

    def __str__(self) -> str:
        return self.toCSS()


class FontFaceSetLoadEvent(Event):
    """Event sent by ``FontFaceSet`` load operations."""

    def __init__(
        self,
        _type: str,
        options: dict[str, Any] | None = None,
        *args: Any,
        **kwargs: Any,
    ) -> None:
        options = options or kwargs
        self.fontfaces = list(options.get("fontfaces", []))
        super().__init__(_type, options, *args, **kwargs)


class FontFaceSet(EventTarget):
    """Set-like collection of ``FontFace`` objects exposed as ``document.fonts``."""

    def __init__(self, fonts: Iterable[FontFace] | None = None) -> None:
        super().__init__()
        self.onloading = None
        self.onloadingdone = None
        self.onloadingerror = None
        self._fonts: list[FontFace] = []
        for font in fonts or []:
            self.add(font)

    @property
    def status(self) -> str:
        if any(font.status == "loading" for font in self._fonts):
            return "loading"
        return "loaded"

    @property
    def ready(self):
        promise = _create_promise()
        if self.status == "loading":
            return promise
        return promise.resolve(self)

    def add(self, font: FontFace) -> "FontFaceSet":
        if not isinstance(font, FontFace):
            raise TypeError("FontFaceSet.add() expects a FontFace")
        if font not in self._fonts:
            self._fonts.append(font)
        return self

    def delete(self, font: FontFace) -> bool:
        if font in self._fonts:
            self._fonts.remove(font)
            return True
        return False

    def clear(self) -> None:
        self._fonts.clear()

    def check(self, font: str, text: str = " ") -> bool:
        matches = self._matching(font)
        return bool(matches) and all(face.status == "loaded" for face in matches)

    def load(self, font: str, text: str = " "):
        matches = self._matching(font)
        self.dispatchEvent(FontFaceSetLoadEvent("loading", {"fontfaces": matches}))
        loaded = []
        errors = []
        for face in matches:
            result = face.load()
            if result.state == "fulfilled":
                loaded.append(face)
            else:
                errors.append(face)
        if errors:
            self.dispatchEvent(
                FontFaceSetLoadEvent("loadingerror", {"fontfaces": errors})
            )
        self.dispatchEvent(FontFaceSetLoadEvent("loadingdone", {"fontfaces": loaded}))
        return _create_promise().resolve(loaded)

    def forEach(self, callback, thisArg: Any | None = None) -> None:
        for font in list(self._fonts):
            if thisArg is None:
                callback(font, font, self)
            else:
                callback(thisArg, font, font, self)

    def values(self) -> list[FontFace]:
        return list(self._fonts)

    def entries(self) -> list[tuple[FontFace, FontFace]]:
        return [(font, font) for font in self._fonts]

    def keys(self) -> list[FontFace]:
        return list(self._fonts)

    def _matching(self, font: str) -> list[FontFace]:
        text = str(font or "").lower()
        return [
            face
            for face in self._fonts
            if face.family.lower() in text or f'"{face.family.lower()}"' in text
        ]

    def __contains__(self, font: object) -> bool:
        return font in self._fonts

    def __iter__(self):
        return iter(self._fonts)

    def __len__(self) -> int:
        return len(self._fonts)


__all__ = ["FontFace", "FontFaceSet", "FontFaceSetLoadEvent"]
