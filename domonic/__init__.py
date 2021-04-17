"""
    domonic
    ====================================
    - Generate HTML using python 3
    - DOM-like API in python 3
    - JS-like API in python 3
    - Call Terminal commands using python 3 (this one requires a nix machine)
"""

__version__ = "0.2.13"
__license__ = 'MIT'

# from typing import *

from .html import *
# from .dom import Element
from .javascript import *
# from .terminal import *

import requests
import re

class domonic:

    JS_MASTER = "assets/js/master.js"
    CSS_STYLE = "assets/css/style.css"

    @staticmethod
    def domonify(domonic_string: str):
        """ [
            domonify attempts to turn a domonic_string string back into a python object.
        ]

        Args:
            dominc_string (str): [a string in the form div(_class="123")]

        Returns:
            a python object
        """
        return eval(domonic_string)

    @staticmethod
    def get(url: str):
        """ downloads html and converts to domonic """
        r = requests.get(url)
        # print(r.text.decode("utf-8"))
        return domonic.parse(r.content.decode("utf-8"))

    @staticmethod
    def output(domonic):
        """ outputs HTML str """
        # TODO - prettify using newlines to save installing this?
        # from html5print import HTMLBeautifier
        # render(HTMLBeautifier.beautify(render(output), 4), 'index.html')
        pass

    @staticmethod
    def parse(html: str) -> str:
        """ HTML as input and returns python """

        # NOTE - not working/finished.
        print("attempting to parse the page")

        html = ''.join(html.split('<!DOCTYPE HTML>'))
        html = ''.join(html.split('<!doctype html>'))

        # html = "<html><body>some content</body></html>"

        htmltags = ["figcaption", "blockquote", "textarea", "progress", "optgroup", "noscript", "fieldset", "datalist",
                    "colgroup", "summary", "section", "details", "command", "caption", "article", "address", "submit",
                    "strong", "source", "select", "script", "output", "option", "object", "legend", "keygen", "iframe",
                    "hgroup", "header", "footer", "figure", "canvas", "button", "video", "track", "title", "title",
                    "thead", "tfoot", "tbody", "table", "style", "small", "param", "meter", "label", "input", "embed",
                    "audio", "aside", "time", "span", "span", "samp", "ruby", "meta", "meta", "menu", "mark", "link",
                    "html", "head", "form", "font", "code", "cite", "body", "base", "area", "abbr", "wbr", "var", "sup",
                    "sub", "pre", "nav", "map", "main", "kbd", "ins", "img", "div", "dfn", "del", "col", "bdo", "bdi",
                    "ul", "tr", "th", "td", "rt", "rp", "ol", "li", "hr", "hr", "h6", "h5", "h4", "h3", "h2", "h1",
                    "em", "dt", "dl", "dd", "br", "u", "s", "q", "p", "i", "b", "a"]

        for tag in htmltags:
            # print(tag)
            reg = f"<{tag}>"
            pattern = re.compile(reg)
            html = re.sub(pattern, f'{tag}(', html)  # , flags=re.IGNORECASE )

            # second pass. atrributed
            reg = f"<{tag}"
            pattern = re.compile(reg)
            html = re.sub(pattern, f'{tag}(', html)  # , flags=re.IGNORECASE )

            reg = f"</{tag}>"
            pattern = re.compile(reg)
            html = re.sub(pattern, '),', html)  # , flags=re.IGNORECASE )

            reg = '/>'
            pattern = re.compile(reg)
            html = re.sub(pattern, '),', html)  # , flags=re.IGNORECASE )

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

        # attributes = ["alt", "integrity", "crossorigin", "charset", "lang",
        #               "class", "id", "style", "placeholder", "text", "value",
        #               "href", "width", "height", "src", "name", "content",
        #               "rel", "color", "type", "size"]

        attributes = [
            "accept", "accesskey", "action", "align", "alt", "async", "autocomplete", "autofocus",
            "autoplay", "bgcolor", "border", "charset", "checked", "cite", "class", "color",
            "cols", "colspan", "content", "contenteditable", "controls", "coords", "data", "datetime", "default",
            "defer", "dir", "dirname", "disabled", "download", "draggable", "enctype", "for", "form", "formaction",
            "headers", "height", "hidden", "high", "href", "hreflang", "id", "ismap", "kind", "label", "lang", "list",
            "loop", "low", "max", "maxlength", "media", "method", "min", "multiple", "muted", "name", "novalidate",
            "onabort", "onafterprint", "onbeforeprint", "onbeforeunload", "onblur", "oncanplay", "oncanplaythrough",
            "onchange", "onclick", "oncontextmenu", "oncopy", "oncuechange", "oncut", "ondblclick", "ondrag",
            "ondragend", "ondragenter", "ondragleave", "ondragover", "ondragstart", "ondrop", "ondurationchange",
            "onemptied", "onended", "onerror", "onfocus", "onhashchange", "oninput", "oninvalid", "onkeydown",
            "onkeypress", "onkeyup", "onload", "onloadeddata", "onloadedmetadata", "onloadstart", "onmousedown",
            "onmousemove", "onmouseout", "onmouseover", "onmouseup", "onmousewheel", "onoffline", "ononline",
            "onpagehide", "onpageshow", "onpaste", "onpause", "onplay", "onplaying", "onpopstate", "onprogress",
            "onratechange", "onreset", "onresize", "onscroll", "onsearch", "onseeked", "onseeking", "onselect",
            "onstalled", "onstorage", "onsubmit", "onsuspend", "ontimeupdate", "ontoggle", "onunload", "onvolumechange",
            "onwaiting", "onwheel", "open", "optimum", "pattern", "placeholder", "poster", "preload", "readonly",
            "rel", "required", "reversed", "rows", "rowspan", "sandbox", "scope", "selected", "shape", "size", "sizes",
            "span", "spellcheck", "src", "srcdoc", "srclang", "srcset", "start", "step", "style", "tabindex", "target",
            "title", "translate", "type", "usemap", "value", "width", "wrap", "property"]

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
            html = re.sub(pattern, '"""),', html)  # , flags=re.IGNORECASE )

            reg = '/>'
            pattern = re.compile(reg)
            html = re.sub(pattern, '"""),', html)  # , flags=re.IGNORECASE )

        html = ')'.join(html.split(',)'))

        print(html)

        # return eval('print("test")')
        # return eval('Location()')
        # return eval('html()')
        return html
