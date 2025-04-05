from typing import Dict

"""
domonic.constants
====================================
This module defines various constants used in the domonic package.
"""

# Namespaces
namespaces: Dict[str, str] = {
    "xml": "http://www.w3.org/XML/1998/namespace",
    "svg": "http://www.w3.org/2000/svg",
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
doctypes: Dict[str, str] = {
    "HTML5": "<!DOCTYPE html>",
    "HTML4_01_Strict": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
    "HTML4_01_Transitional": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
    "HTML4_01_Frameset": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">',
    "HTML3_2": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">',
    "HTML2": '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">',
}

# HTTP Response Status Codes
from enum import Enum

class HTTPStatus(Enum):
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
    PROXY_AUTHENTICATION REQUIRED = 407
    REQUEST TIMEOUT = 408
    CONFLICT = 409
    GONE = 410
    LENGTH REQUIRED = 411
    PRECONDITION FAILED = 412
    PAYLOAD TOO LARGE = 413
    URI TOO LONG = 414
    UNSUPPORTED MEDIA TYPE = 415
    RANGE NOT SATISFIABLE = 416
    EXPECTATION FAILED = 417
    IM A TEAPOT = 418
    MISDIRECTED REQUEST = 421
    UNPROCESSABLE ENTITY = 422
    LOCKED = 423
    FAILED DEPENDENCY = 424
    UPGRADE REQUIRED = 426
    PRECONDITION REQUIRED = 428
    TOO MANY REQUESTS = 429
    REQUEST HEADER FIELDS TOO LARGE = 431
    UNAVAILABLE FOR LEGAL REASONS = 451
    CLIENT CLOSED REQUEST = 499
    INTERNAL SERVER ERROR = 500
    NOT IMPLEMENTED = 501
    BAD GATEWAY = 502
    SERVICE UNAVAILABLE = 503
    GATEWAY TIMEOUT = 504
    HTTP VERSION NOT SUPPORTED = 505
    VARIANT ALSO NEGOTIATES = 506
    INSUFFICIENT STORAGE = 507
    LOOP DETECTED = 508
    NOT EXTENDED = 510
    NETWORK AUTHENTICATION REQUIRED = 511

http_response_status_codes = {status.value: status.name.replace('_', ' ').title() for status in HTTPStatus}

# Common MIME Types
file_extensions: Dict[str, str] = {
    "html": "text/html",
    "htm": "text/html",
    "xhtml": "application/xhtml+xml",
    "xml": "application/xml",
    "svg": "image/svg+xml",
    "css": "text/css",
    "js": "application/javascript",
    "json": "application/json",
    "txt": "text/plain",
    "pdf": "application/pdf",
    "png": "image/png",
    "jpg": "image/jpeg",
    "jpeg": "image/jpeg",
    "gif": "image/gif",
    "ico": "image/x-icon",
    "tiff": "image/tiff",
    "tif": "image/tiff",
    "bmp": "image/bmp",
    "mp3": "audio/mpeg",
    "mp4": "video/mp4",
    "mpeg": "video/mpeg",
    "mpg": "video/mpeg",
    "mov": "video/quicktime",
    "qt": "video/quicktime",
    "avi": "video/x-msvideo",
    "wmv": "video/x-ms-wmv",
    "flv": "video/x-flv",
    "swf": "application/x-shockwave-flash",
    "zip": "application/zip",
    "gz": "application/x-gzip",
    "bz2": "application/x-bzip2",
    "rar": "application/x-rar-compressed",
    "tar": "application/x-tar",
    "7z": "application/x-7z-compressed",
    "exe": "application/x-msdownload",
    "msi": "application/x-msdownload",
    "cab": "application/vnd.ms-cab-compressed",
    "doc": "application/msword",
    "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
    "xls": "application/vnd.ms-excel",
    "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
    "ppt": "application/vnd.ms-powerpoint",
    "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
}
