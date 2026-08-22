from __future__ import annotations

"""
domonic.constants
====================================
This module defines various constants used in the domonic package.
"""

import mimetypes
from enum import IntEnum
from http import HTTPStatus as StdlibHTTPStatus
from typing import Final


def _status_text(status: "HTTPStatus") -> str:
    try:
        return StdlibHTTPStatus(status.value).phrase
    except ValueError:
        return status.name.replace("_", " ").title()


# Namespaces
namespaces: Final[dict[str, str]] = {
    "atom": "http://www.w3.org/2005/Atom",
    "content": "http://purl.org/rss/1.0/modules/content/",
    "dc": "http://purl.org/dc/elements/1.1/",
    "dcterms": "http://purl.org/dc/terms/",
    "fb": "http://ogp.me/ns/fb#",
    "geo": "http://www.google.com/geo/schemas/sitemap/1.0",
    "image": "http://www.google.com/schemas/sitemap-image/1.1",
    "mathml": "http://www.w3.org/1998/Math/MathML",
    "media": "http://search.yahoo.com/mrss/",
    "mobile": "http://www.google.com/schemas/sitemap-mobile/1.0",
    "news": "http://www.google.com/schemas/sitemap-news/0.9",
    "og": "http://ogp.me/ns#",
    "rdf": "http://www.w3.org/1999/02/22-rdf-syntax-ns#",
    "rss": "http://purl.org/rss/1.0/",
    "schema": "https://schema.org/",
    "xml": "http://www.w3.org/XML/1998/namespace",
    "svg": "http://www.w3.org/2000/svg",
    "video": "http://www.google.com/schemas/sitemap-video/1.1",
    "wsdl": "http://schemas.xmlsoap.org/wsdl/",
    "xlink": "http://www.w3.org/1999/xlink",
    "xmlns": "http://www.w3.org/2000/xmlns/",
    "xm": "http://www.w3.org/2001/xml-events",
    "xh": "http://www.w3.org/1999/xhtml",
    "xsl": "http://www.w3.org/1999/XSL/Transform",
    "xsd": "http://www.w3.org/2001/XMLSchema",
    "xsi": "http://www.w3.org/2001/XMLSchema-instance",
    "xhtml": "http://www.w3.org/1999/xhtml",
    "html": "http://www.w3.org/1999/xhtml",
}

# Document Types
doctypes: Final[dict[str, str]] = {
    "HTML5": "<!DOCTYPE html>",
    "HTML5_LEGACY_COMPAT": '<!DOCTYPE html SYSTEM "about:legacy-compat">',
    "XHTML5": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 5.0//EN" "about:legacy-compat">',
    "XHTML1_0_Strict": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">',
    "XHTML1_0_Transitional": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">',
    "XHTML1_0_Frameset": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">',
    "XHTML1_1": '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">',
    "HTML4_01_Strict": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
    "HTML4_01_Transitional": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
    "HTML4_01_Frameset": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">',
    "HTML3_2": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">',
    "HTML2": '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">',
    "SVG1_0": '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.0//EN" "http://www.w3.org/TR/2001/REC-SVG-20010904/DTD/svg10.dtd">',
    "SVG1_1": '<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">',
    "MATHML2": '<!DOCTYPE math SYSTEM "http://www.w3.org/Math/DTD/mathml2/mathml2.dtd">',
}


# HTTP Response Status Codes
class HTTPStatus(IntEnum):
    OK = 200
    CREATED = 201
    ACCEPTED = 202
    NON_AUTHORITATIVE_INFORMATION = 203
    NO_CONTENT = 204
    RESET_CONTENT = 205
    PARTIAL_CONTENT = 206
    MULTI_STATUS = 207
    ALREADY_REPORTED = 208
    IM_USED = 226
    MULTIPLE_CHOICES = 300
    MOVED_PERMANENTLY = 301
    FOUND = 302
    SEE_OTHER = 303
    NOT_MODIFIED = 304
    USE_PROXY = 305
    SWITCH_PROXY = 306
    TEMPORARY_REDIRECT = 307
    PERMANENT_REDIRECT = 308
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    PAYMENT_REQUIRED = 402
    FORBIDDEN = 403
    NOT_FOUND = 404
    METHOD_NOT_ALLOWED = 405
    NOT_ACCEPTABLE = 406
    PROXY_AUTHENTICATION_REQUIRED = 407
    REQUEST_TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH_REQUIRED = 411
    PRECONDITION_FAILED = 412
    PAYLOAD_TOO_LARGE = 413
    URI_TOO_LONG = 414
    UNSUPPORTED_MEDIA_TYPE = 415
    RANGE_NOT_SATISFIABLE = 416
    EXPECTATION_FAILED = 417
    IM_A_TEAPOT = 418
    MISDIRECTED_REQUEST = 421
    UNPROCESSABLE_ENTITY = 422
    LOCKED = 423
    FAILED_DEPENDENCY = 424
    UPGRADE_REQUIRED = 426
    PRECONDITION_REQUIRED = 428
    TOO_MANY_REQUESTS = 429
    REQUEST_HEADER_FIELDS_TOO_LARGE = 431
    UNAVAILABLE_FOR_LEGAL_REASONS = 451
    CLIENT_CLOSED_REQUEST = 499
    INTERNAL_SERVER_ERROR = 500
    NOT_IMPLEMENTED = 501
    BAD_GATEWAY = 502
    SERVICE_UNAVAILABLE = 503
    GATEWAY_TIMEOUT = 504
    HTTP_VERSION_NOT_SUPPORTED = 505
    VARIANT_ALSO_NEGOTIATES = 506
    INSUFFICIENT_STORAGE = 507
    LOOP_DETECTED = 508
    NOT_EXTENDED = 510
    NETWORK_AUTHENTICATION_REQUIRED = 511


http_response_status_codes: Final[dict[int, str]] = {
    status.value: _status_text(status) for status in HTTPStatus
}


def get_namespace(prefix: str, default: str | None = None) -> str | None:
    """Return the namespace URI for a known prefix."""
    return namespaces.get(prefix, default)


def get_doctype(name: str, default: str | None = None) -> str | None:
    """Return a known doctype string by name."""
    return doctypes.get(name, default)


def get_mime_type(extension: str, default: str | None = None) -> str | None:
    """Return the MIME type for a file extension with or without a leading dot."""
    return file_extensions.get(extension.lower().lstrip("."), default)


def get_status_text(code: int, default: str | None = None) -> str | None:
    """Return the status phrase for an HTTP response code."""
    return http_response_status_codes.get(code, default)


mimetypes.init()
_BASE_MIME_TYPES: dict[str, str] = {
    extension.lstrip("."): mime_type
    for extension, mime_type in mimetypes.types_map.items()
    if extension.startswith(".")
}
_BASE_MIME_TYPES.update(
    {
        extension.lstrip("."): mime_type
        for extension, mime_type in getattr(mimetypes, "common_types", {}).items()
        if extension.startswith(".")
    }
)
_BASE_MIME_TYPES.update(
    {
        "avif": "image/avif",
        "csv": "text/csv",
        "heic": "image/heic",
        "heif": "image/heif",
        "js": "application/javascript",
        "json": "application/json",
        "md": "text/markdown",
        "mjs": "text/javascript",
        "wasm": "application/wasm",
        "webmanifest": "application/manifest+json",
        "woff": "font/woff",
        "woff2": "font/woff2",
    }
)

# Common and extended MIME types
file_extensions: Final[dict[str, str]] = dict(sorted(_BASE_MIME_TYPES.items()))

mime_types: Final[dict[str, str]] = file_extensions

__all__ = [
    "HTTPStatus",
    "doctypes",
    "file_extensions",
    "get_doctype",
    "get_mime_type",
    "get_namespace",
    "get_status_text",
    "http_response_status_codes",
    "mime_types",
    "namespaces",
]
