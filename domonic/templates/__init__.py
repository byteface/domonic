"""
    domonic.templates
    ====================================
    some builtin templates

"""

from domonic.html import *
from domonic.constants.entities import Char
from domonic.constants import http_response_status_codes


class status_page():
    DEBUG_MODE = False

    def __init__(self, code=404, wholepage=True):
        self.status_code = code
        self.message = http_response_status_codes[code]
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
