# -*- coding: utf-8 -*-
"""
    domonic
    ~~~~~
    - Generate HTML using python 3
    - DOM-like API in python 3
    - JS-like API in python 3
    - Call Terminal commands using python 3 (this one requires a nix machine)
"""

__version__ = "0.1.3"
__license__ = 'MIT'

# from typing import *

# from .html import *
# from .dom import *
from .javascript import *
# from .terminal import *

import requests


class domonic:

    @staticmethod
    def get(url: str):
        ''' downloads html and converts to domonic '''
        r = requests.get(url)
        return domonic.parse(r.text)

    @staticmethod
    def output(domonic):
        ''' outputs HTML str '''
        # TODO - prettify using newlines to save installing this?
        # from html5print import HTMLBeautifier
        # render(HTMLBeautifier.beautify(render(output), 4), 'index.html')
        pass

    @staticmethod
    def parse(html: str) -> str:
        ''' HTML as input and returns python '''

        # NOTE - not working/finished.

        print("attempting to parse the page")

        import re

        html = ''.join(html.split('<!DOCTYPE HTML>'))
        html = ''.join(html.split('<!doctype html>'))

        # html = "<html><body>some content</body></html>"

        htmltags = ["html", "span", "button", "link", "form", "nav",
                    "details", "summary", "header", "head", "body", "meta",
                    "title", "div", "footer", "img", "a", "p", "h1", "h2",
                    "h3", "h4", "h5", "h6", "hr", "ul", "ol", "li", "time",
                    "template", "label", "input", "small", "strong", "option",
                    "select", "main", "td", "tr", "thead", "th", "table",
                    "tbody", "canvas", "b", "center", "br"]

        for tag in htmltags:

            print(tag)

            reg = f"<{tag}>"
            pattern = re.compile(reg)
            html = re.sub(pattern, f'{tag}(', html)  # , flags=re.IGNORECASE )

            # second pass. atrributed
            reg = f"<{tag}"
            pattern = re.compile(reg)
            html = re.sub(pattern, f'{tag}(', html)  # , flags=re.IGNORECASE )

            reg = f"</{tag}>"
            pattern = re.compile(reg)
            html = re.sub(pattern, ')', html)  # , flags=re.IGNORECASE )

            reg = '/>'
            pattern = re.compile(reg)
            html = re.sub(pattern, ')', html)  # , flags=re.IGNORECASE )

        # close any tags that arent properly self closing
        flag = False
        increase_index = 0  # by the amount of new chars you add
        for index, char in enumerate(html):
            index = index + increase_index
            if char == "(":
                flag = True
                tag = html[index - 4] + html[index - 3] + \
                    html[index - 2] + html[index - 1]
                print(tag)

            if char == ")":
                flag = False
            if char == ">" and flag is True:
                if 'meta' in tag or 'link' in tag or 'hr' in tag:
                    # replace it for a '),'
                    html = f"{html[:index]}),{html[index+1:]}"
                    increase_index += 1
                else:
                    # replace for a ','
                    html = f'{html[:index]},{html[index+1:]}'

        # strip any comments
        cleaned = []
        for line in html.splitlines():
            if "<!" in line:
                continue
            cleaned.append(line)
        html = '\n'.join(cleaned)

        attributes = ["alt", "integrity", "crossorigin", "charset", "lang",
                      "class", "id", "style", "placeholder", "text", "value",
                      "href", "width", "height", "src", "name", "content",
                      "rel", "color", "type", "size"]

        # put underscores on all the attributes
        for attr in attributes:
            reg = f' {attr}="'
            pattern = re.compile(reg)
            # , flags=re.IGNORECASE )
            html = re.sub(pattern, f' _{attr}="', html)

        # commas between them
        for attr in attributes:
            reg = f'" _{attr}="'
            pattern = re.compile(reg)
            # , flags=re.IGNORECASE )
            html = re.sub(pattern, f'", _{attr}="', html)

        # TODO - diff between loaded and inline
        # get the style and script tags
        htmltags = ["style", "script"]
        for tag in htmltags:
            reg = f"<{tag}>"
            pattern = re.compile(reg)
            html = re.sub(
                pattern, f'{tag}("""', html)  # , flags=re.IGNORECASE )

            # second pass. atrributed
            reg = f"<{tag}"
            pattern = re.compile(reg)
            html = re.sub(
                pattern, f'{tag}("""', html)  # , flags=re.IGNORECASE )

            reg = f"</{tag}>"
            pattern = re.compile(reg)
            html = re.sub(pattern, '""")', html)  # , flags=re.IGNORECASE )

            reg = '/>'
            pattern = re.compile(reg)
            html = re.sub(pattern, '""")', html)  # , flags=re.IGNORECASE )

        html = ')'.join(html.split(',)'))

        print(html)

        # return eval('print("test")')
        # return eval('Location()')
        # return eval('html()')
        return html
