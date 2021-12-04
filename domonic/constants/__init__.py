"""
    domonic.constants
    ====================================

"""

#: namespaces
namespaces: dict = {
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


#: document types
doctypes: dict = {
    "HTML5": "<!DOCTYPE html>",
    # XHTML 1.1	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1//EN" "http://www.w3.org/TR/xhtml11/DTD/xhtml11.dtd">
    # XHTML 1.1 Strict	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    # XHTML 1.1 Transitional	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    # XHTML 1.1 Frameset	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.1 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">
    # XHTML 1.0 Strict	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Strict//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-strict.dtd">
    # XHTML 1.0 Transitional	<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Transitional//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd">
    # XHTML_1_0_Frameset = '<!DOCTYPE html PUBLIC "-//W3C//DTD XHTML 1.0 Frameset//EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-frameset.dtd">'
    "HTML4_01_Strict": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01//EN" "http://www.w3.org/TR/html4/strict.dtd">',
    "HTML4_01_Transitional": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">',
    "HTML4_01_Frameset": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Frameset//EN" "http://www.w3.org/TR/html4/frameset.dtd">',
    "HTML3_2": '<!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">',
    "HTML2": '<!DOCTYPE HTML PUBLIC "-//IETF//DTD HTML//EN">',
}


#: html response status codes
http_response_status_codes: dict = {
    200: "200 OK",
    201: "201 Created",
    202: "202 Accepted",
    203: "203 Non-Authoritative Information",
    204: "204 No Content",
    205: "205 Reset Content",
    206: "206 Partial Content",
    207: "207 Multi-Status",
    208: "208 Already Reported",
    226: "226 IM Used",
    300: "300 Multiple Choices",
    301: "301 Moved Permanently",
    302: "302 Found",
    303: "303 See Other",
    304: "304 Not Modified",
    305: "305 Use Proxy",
    306: "306 Switch Proxy",
    307: "307 Temporary Redirect",
    308: "308 Permanent Redirect",
    400: "400 Bad Request",
    401: "401 Unauthorized",
    402: "402 Payment Required",
    403: "403 Forbidden",
    404: "404 Not Found",
    405: "405 Method Not Allowed",
    406: "406 Not Acceptable",
    407: "407 Proxy Authentication Required",
    408: "408 Request Timeout",
    409: "409 Conflict",
    410: "410 Gone",
    411: "411 Length Required",
    412: "412 Precondition Failed",
    413: "413 Payload Too Large",
    414: "414 URI Too Long",
    415: "415 Unsupported Media Type",
    416: "416 Range Not Satisfiable",
    417: "417 Expectation Failed",
    418: "418 I'm a teapot",
    421: "421 Misdirected Request",
    422: "422 Unprocessable Entity",
    423: "423 Locked",
    424: "424 Failed Dependency",
    426: "426 Upgrade Required",
    428: "428 Precondition Required",
    429: "429 Too Many Requests",
    431: "431 Request Header Fields Too Large",
    451: "451 Unavailable For Legal Reasons",
    499: "499 Client Closed Request",
    500: "500 Internal Server Error",
    501: "501 Not Implemented",
    502: "502 Bad Gateway",
    503: "503 Service Unavailable",
    504: "504 Gateway Timeout",
    505: "505 HTTP Version Not Supported",
    506: "506 Variant Also Negotiates",
    507: "507 Insufficient Storage",
    508: "508 Loop Detected",
    510: "510 Not Extended",
    511: "511 Network Authentication Required",
}


# file_extensions = {
#     "html": "text/html",
#     "htm": "text/html",
#     "xhtml": "application/xhtml+xml",
#     "xml": "application/xml",
#     "svg": "image/svg+xml",
#     "css": "text/css",
#     "js": "application/javascript",
#     "json": "application/json",
#     "txt": "text/plain",
#     "pdf": "application/pdf",
#     "png": "image/png",
#     "jpg": "image/jpeg",
#     "jpeg": "image/jpeg",
#     "gif": "image/gif",
#     "ico": "image/x-icon",
#     "tiff": "image/tiff",
#     "tif": "image/tiff",
#     "bmp": "image/bmp",
#     "mp3": "audio/mpeg",
#     "mp4": "video/mp4",
#     "mpeg": "video/mpeg",
#     "mpg": "video/mpeg",
#     "mov": "video/quicktime",
#     "qt": "video/quicktime",
#     "avi": "video/x-msvideo",
#     "wmv": "video/x-ms-wmv",
#     "flv": "video/x-flv",
#     "swf": "application/x-shockwave-flash",
#     "zip": "application/zip",
#     "gz": "application/x-gzip",
#     "bz2": "application/x-bzip2",
#     "rar": "application/x-rar-compressed",
#     "tar": "application/x-tar",
#     "7z": "application/x-7z-compressed",
#     "exe": "application/x-msdownload",
#     "msi": "application/x-msdownload",
#     "cab": "application/vnd.ms-cab-compressed",
#     "doc": "application/msword",
#     "docx": "application/vnd.openxmlformats-officedocument.wordprocessingml.document",
#     "xls": "application/vnd.ms-excel",
#     "xlsx": "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
#     "ppt": "application/vnd.ms-powerpoint",
#     "pptx": "application/vnd.openxmlformats-officedocument.presentationml.presentation",
# }

# """
# tag_states = {
#     'a' : {
#         'hover' : 'a:hover',
#         'visited' : 'a:visited',
#         'link' : 'a:link',
#         'active' : 'a:active',
#         'focus' : 'a:focus',
#         # 'not' : 'a:not',
#     }
# }
# """
