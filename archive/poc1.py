"""
from jizz import *

render( html( head( script(), style() ), body(f"hello world") ) )

TODO - use args/kwargs for 
TODO - when done. post here? .. https://stackoverflow.com/questions/6748559/generating-html-documents-in-python
TODO - throw warnings if wrong tags are used.. i.e if someone puts not li element in a ul

TODO - consider a setting to auto render html tags.. 'asumptions=on' or something
TODO - formatting 'on' for newlines
TODO - mutlitple classnames. i.e. h1 = H1

"""

# TODO - a base class to capture attributes that others can call super on.
# TODO - maybe different types of base. i.e. list containers could extend arrays
# class tag:
# def __init__(self, content='' ):
# self.content = content

# def __str__(self):
#     return str(f"<html>{self.content}</html>")

# class tag:
#     def __init__(self, content=''):
#         self.content = content
# def __str__(self):
#     return str(f"<{self.tag()}>{self.content}</{self.tag()}>")
# def tag(self):
#     return self.__str__().split('<')[1].split('>')[0]


class html:  # (tag):
    def __init__(self, content="", *args, **kwargs):
        self.content = content  # + ''.join(args)

    def __str__(self):
        return str(f"<html>{self.content}</html>")


class head:
    def __init__(self, content="", *args, **kwargs):
        self.content = content  # + ''.join([str(each.__str__()) for each in args])

    def __str__(self):
        return f"<head>{self.content}</head>"


class body:
    def __init__(self, content="", *args, **kwargs):
        self.content = content
        self.args = args

    def __str__(self):
        return f"<body>{self.content}{''.join([each.__str__() for each in self.args])}</body>"


class script:
    def __init__(self, content="", *args, **kwargs):
        self.content = content

    def __str__(self):
        return f"<script>{self.content}</script>"


class style:
    def __init__(self, content="", *args, **kwargs):
        self.content = content

    def __str__(self):
        return f"<style>{self.content}</style>"


class img:
    def __init__(self, src="", *args, **kwargs):
        self.content = content

    def __str__(self):
        return f"<img src={self.content}/>"


class div:
    def __init__(self, content="", *args, **kwargs):
        self.content = content
        self.args = args

    def __str__(self):
        # return f"<div>{self.content}</div>"
        return f"<div>{self.content}{''.join([each.__str__() for each in self.args])}</div>"


class a:
    def __init__(self, content="", attr=[], *args, **kwargs):
        self.content = content
        self.args = args
        self.kwargs = kwargs
        self.attr = attr

    def __str__(self):
        # return f"<a {[ '''%s=%s''' % (key, value) for key, value in self.attr.items() ]}>{self.content}</a>"
        return f"<a {[ '''%s=%s''' % (key, value) for key, value in self.kwargs.items() ]}>{self.content}</a>"


class footer:
    def __init__(self, content="", *args, **kwargs):
        self.content = content

    def __str__(self):
        return f"<footer>{self.content}</footer>"


class header:
    def __init__(self, content="", *args, **kwargs):
        self.content = content

    def __str__(self):
        return f"<header>{self.content}</header>"


class ul:
    def __init__(self, content="", *args, **kwargs):
        self.content = content

    def __str__(self):
        return f"<ul>{self.content}</ul>"


class li:
    def __init__(self, content="", *args, **kwargs):
        self.content = content

    def __str__(self):
        return f"<header>{self.content}</header>"


class p:
    def __init__(self, content="", *args, **kwargs):
        self.content = content

    def __str__(self):
        return f"<p>{self.content}</p>"


class H1:
    def __init__(self, content="", *args, **kwargs):
        self.content = content

    def __str__(self):
        return f"<p>{self.content}</p>"


# TODO-
def render(inp, outp=""):
    print(inp)
    return inp


# render( html( head( script(), style() ), body(f"hello world") ) )

# render( html() )
# render( div("hello world") )
# render( html(body(div("hello world"))) )

# render(
#     html(
#         body(
#             div("hello world"),
#             div("hello world"),
#             a( "this is a link", attr={"href":"http://www.fuckoff.com", "waf":"cheese"})
#             )))


class tag:
    def __init__(self, *args, **kwargs):
        self.args = args

    def __str__(self):
        return f"<{self.name}>{''.join([each.__str__() for each in self.args])}</{self.name}>"


# obj = type('obj', (object,), {'propertyName' : 'propertyValue'})
# type(obj)
span = type("span", (tag,), {"name": "span"})
ol = type("ol", (tag,), {"name": "ol"})


def get_tag(name=""):
    return type(f"{name}", (tag,), {"name": f"{name}"})


anything = get_tag("anything")


# render(
#     html(
#         body(
#             div("hello world"),
#             div("hello world"),
#             a( "this is a link", href="http://www.fuckoff.com", style="font-size:10px;"),
#             span("fuck"),
#             ol(),
#             anything()
#             )))


# render(
#     html(
#         body(
#             div("hello world"),
#             div("hello world"),
#             a( "this is a link", href="http://www.fuckoff.com", style="font-size:10px;"),
#             span("fuck"),
#             ol(),
#             [f'{anything()}' for thing in range(10)]
#             )))


# divs = [div("hello world"),div("hello world")]

# render(
#     html(
#         body(divs)))


# TODO-
def render(inp, outp=""):
    print(inp)
    return inp


class tag:
    def __init__(self, *args, **kwargs):
        self.args = args

    def __str__(self):
        return f"<{self.name} {[ '''%s=%s''' % (key, value) for key, value in self.kwargs.items() ]}> \
            {''.join([each.__str__() for each in self.args])}</{self.name}>"


html = type("html", (tag,), {"name": "html"})
body = type("body", (tag,), {"name": "body"})
head = type("head", (tag,), {"name": "head"})
script = type("script", (tag,), {"name": "script"})
style = type("style", (tag,), {"name": "style"})
h1 = type("h1", (tag,), {"name": "h1"})
h2 = type("h2", (tag,), {"name": "h2"})
h3 = type("h3", (tag,), {"name": "h3"})
h4 = type("h4", (tag,), {"name": "h4"})
h5 = type("h5", (tag,), {"name": "h5"})
h6 = type("h6", (tag,), {"name": "h6"})
p = type("p", (tag,), {"name": "p"})
i = type("i", (tag,), {"name": "i"})
b = type("b", (tag,), {"name": "b"})
a = type("a", (tag,), {"name": "a"})
ul = type("ul", (tag,), {"name": "ul"})
ol = type("ol", (tag,), {"name": "ol"})
li = type("li", (tag,), {"name": "li"})
blockquote = type("blockquote", (tag,), {"name": "blockquote"})
hr = type("hr", (tag,), {"name": "hr"})
img = type("img", (tag,), {"name": "img"})
div = type("div", (tag,), {"name": "div"})
span = type("span", (tag,), {"name": "span"})
strong = type("strong", (tag,), {"name": "strong"})


render(
    html(
        body(
            div("hello world"),
            div("hello world"),
            a("this is a link", href="http://www.somesite.com", style="font-size:10px;"),
            span("hi"),
            ol(),
            [f"{anything()}" for thing in range(10)],
        )
    )
)
