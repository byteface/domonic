"""
domonic.mathml
====================================

Generate MathML using Python 3.

The module exposes the current MathML Core element set and retaining useful Full/legacy MathML
constructors for backwards compatibility.
"""

from __future__ import annotations

from typing import Any

from domonic.dom import MATHML_NAMESPACE, MathMLElement


# MathML Core, W3C Candidate Recommendation (24 June 2025).
#
# Keep this separate from the broader public tag catalogue so consumers can
# distinguish browser-core MathML from Full/legacy MathML without changing the
# long-standing ``mathml_tags`` API.
_MATHML_CORE_TAGS = [
    "annotation",
    "annotation-xml",
    "maction",
    "math",
    "merror",
    "mfrac",
    "mi",
    "mmultiscripts",
    "mn",
    "mo",
    "mover",
    "mpadded",
    "mphantom",
    "mprescripts",
    "mroot",
    "mrow",
    "ms",
    "mspace",
    "msqrt",
    "mstyle",
    "msub",
    "msubsup",
    "msup",
    "mtable",
    "mtd",
    "mtext",
    "mtr",
    "munder",
    "munderover",
    "semantics",
]


# Presentation elements available in Full MathML 4 but not MathML Core.
#
# ``a`` is deliberately supported but is not placed in ``__all__`` below:
# wildcard-importing it would unexpectedly shadow domonic.html.a in existing
# applications. It remains available as ``domonic.xml.mathml.a`` and through
# ``create_element("a")``.
_MATHML_FULL_TAGS = [
    "a",
    "menclose",
    "mfenced",
    "mglyph",
    "maligngroup",
    "malignmark",
    "mstack",
    "mlongdiv",
    "msgroup",
    "msrow",
    "mscarries",
    "mscarry",
    "msline",
]


# Retained for compatibility with MathML 3 / older domonic documents.
#
# ``none`` existed in domonic's public constructor surface already.
# ``mlabeledtr`` was part of older Presentation MathML and remains useful when
# reading or generating legacy documents.
_MATHML_LEGACY_TAGS = [
    "none",
    "mlabeledtr",
]


# Public catalogue used by domonic's parser adapters.  Historically this list
# contained duplicates; de-duplicating it does not remove any supported name.
mathml_tags = list(
    dict.fromkeys(
        _MATHML_CORE_TAGS
        + _MATHML_FULL_TAGS
        + _MATHML_LEGACY_TAGS
    )
)

_MATHML_TAG_LOOKUP = frozenset(mathml_tags)
_PYTHON_NAME_TO_TAG = {tag_name.replace("-", "_"): tag_name for tag_name in mathml_tags}
_CUSTOM_MATHML_CLASSES: dict[str, type[MathMLElement]] = {}


def _python_name(tag_name: str) -> str:
    return tag_name.replace("-", "_")


def _make_mathml_constructor(tag_name: str) -> type[MathMLElement]:
    """Create a MathMLElement subclass for a concrete MathML tag."""
    return type(
        _python_name(tag_name),
        (MathMLElement,),
        {
            "name": tag_name,
            "__module__": __name__,
        },
    )


# Generate the complete constructor surface once at import time.
for _tag_name in mathml_tags:
    globals()[_python_name(_tag_name)] = _make_mathml_constructor(_tag_name)


# Historical domonic spelling.  Keep this as the preferred wildcard-exported
# name so existing ``math_(...)`` code continues to work unchanged.
math_ = globals()["math"]


def create_element(
    name: str = "math",
    *args: Any,
    **kwargs: Any,
) -> MathMLElement:
    """Create a MathML element, including custom or hyphenated names.

    Known MathML names return the module's generated constructor class.
    Python-safe aliases such as ``annotation_xml`` resolve to
    ``annotation-xml``. Unknown names remain MathML-namespaced elements so
    custom/future MathML markup can still round-trip through domonic.
    """
    normalized_name = str(name).strip()
    if not normalized_name:
        normalized_name = "math"

    tag_name = normalized_name
    if tag_name not in _MATHML_TAG_LOOKUP:
        tag_name = _PYTHON_NAME_TO_TAG.get(normalized_name, normalized_name)

    if tag_name in _MATHML_TAG_LOOKUP:
        return globals()[_python_name(tag_name)](*args, **kwargs)

    custom_class = _CUSTOM_MATHML_CLASSES.get(normalized_name)
    if custom_class is None:
        custom_class = type(
            _python_name(normalized_name),
            (MathMLElement,),
            {
                "name": normalized_name,
                "__module__": __name__,
            },
        )
        _CUSTOM_MATHML_CLASSES[normalized_name] = custom_class

    element = custom_class(*args, **kwargs)
    element.name = normalized_name
    return element


# Preserve the old wildcard surface and add the non-conflicting modern names.
#
# ``math`` and the MathML ``a`` element intentionally stay explicit-only to
# avoid introducing new wildcard collisions.  ``math_`` remains the historical
# root constructor.
__all__ = [
    "MATHML_NAMESPACE",
    "MathMLElement",
    "mathml_tags",
    "create_element",
    "math_",
    "annotation",
    "annotation_xml",
    "maction",
    "menclose",
    "merror",
    "mfenced",
    "mfrac",
    "mi",
    "mmultiscripts",
    "mn",
    "mo",
    "mover",
    "mpadded",
    "mphantom",
    "mprescripts",
    "mroot",
    "mrow",
    "ms",
    "mspace",
    "msqrt",
    "mstyle",
    "msub",
    "msubsup",
    "msup",
    "mtable",
    "mtd",
    "mtext",
    "mtr",
    "munder",
    "munderover",
    "semantics",
    "maligngroup",
    "malignmark",
    "mglyph",
    "mstack",
    "mlongdiv",
    "msgroup",
    "msrow",
    "mscarries",
    "mscarry",
    "msline",
    "none",
    "mlabeledtr",
]
