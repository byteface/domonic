"""
    domonic.templates
    ====================================
    some builtin templates

"""

from domonic import *


class status_page():

    STATUS = {
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

    DEBUG_MODE = False

    def __init__(self, code=404, wholepage=True):
        self.status_code = code
        self.message = self.STATUS[code]
        # self.host = "http://localhost:8000"
        self.wholepage = wholepage

        self.status_node = div(_id="status")
        self.status_node += h1(f"{self.status_code}")
        self.status_node += p(self.message)

        # if status_page.DEBUG_MODE:
        #     import os
        #     self.status_node.appendChild(
        #         pre(os.environ)
        #     )
        #     import sys
        #     self.status_node.appendChild(
        #         pre(sys.path)
        #     )
        #     import traceback
        #     self.status_node.appendChild(
        #         pre(traceback.format_exc())
        #     )

        page = html(
            head(title(f"{self.status_code}")),
            body(self.status_node)
        )
        self.content = self.wholepage and page or self.status_node

    # def __getattr__(self, name):
    #     return getattr(self.status_node, name)

    # def __setattr__(self, name, value):
    #     setattr(self.status_node, name, value)

    def __str__(self):
        return f'{self.content}'

    # @staticmethod
    # def to_html(output_dir):
    #     for code, name in status_page.STATUS.items():
    #         page = status_page(code, name)
    #         with open(f"{output_dir}/{code}.html", "w") as f:
    #             f.write(f'{page}')


'''
class d_b():
    def __init__(self):
        pass
    def config(self, db_name, db_user, db_pass, db_host, db_port):
        self.db_name = db_name
        self.db_user = db_user
        self.db_pass = db_pass
        self.db_host = db_host
        self.db_port = db_port
    # def connect(self):
    # def query(self, query):
    # def close(self):
'''


# from domonic.templates import status_page

# @app.errorhandler(404)
# def page_not_found(e):
#     return status_page(404)
