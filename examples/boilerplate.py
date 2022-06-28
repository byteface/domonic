# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, "..")

from domonic.javascript import Math
from domonic.html import *
from domonic.dom import DOMConfig

# DOMConfig.GLOBAL_AUTOESCAPE = True  # TODO - script tags shouldn't be escaped?
DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS = False  # TODO - is it putting newlines instead?
DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH = False
DOMConfig.ATTRIBUTE_QUOTES = None

DOMAIN = "mywebsite"

# <!DOCTYPE html>
page = lambda content: html(_lang="en", _class="no-js", _dir="auto").append(
    head(
        meta(_charset="UTF-8"),
        meta(_name="viewport", _content="width=device-width"),
        title("Unique page title - My Site"),
        script(
        """
            document.documentElement.classList.remove('no-js');
            document.documentElement.classList.add('js');
    	""",
        _type="module",
        ),
        link(_rel="stylesheet", _href="/assets/css/styles.css"),
        meta(_name="description", _content="Page description"),
        meta(_property="og:title", _content="Unique page title - My Site"),
        meta(_property="og:description", _content="Page description"),
        meta(_property="og:image", _content=f"https://www.{DOMAIN}.com/image.jpg"),
        meta(_property="og:image:alt", _content="Image description"),
        meta(_property="og:locale", _content="en_GB"),
        meta(_property="og:type", _content="website"),
        meta(_name="twitter:card", _content="summary_large_image"),
        meta(_property="og:url", _content=f"https://www.{DOMAIN}.com/page"),
        link(_rel="canonical", _href=f"https://www.{DOMAIN}.com/page"),
        link(_rel="icon", _href="/favicon.ico"),
        link(_rel="icon", _href="/favicon.svg", _type="image/svg+xml"),
        link(_rel="apple-touch-icon", _href="/apple-touch-icon.png"),
        link(_rel="manifest", _href="/my.webmanifest"),
        meta(_name="theme-color", _content="#FF00FF"),
    ),
    body(content, script(_src="/assets/js/script.js", _type="module")),
)

content = div("Hello World!")

# no pretty printing
# render( page(content), "boilerplate.html" )

# use f-string for pretty printing
render(f"{page(content)}", "boilerplate.html")
