"""
    domonic.html
    ====================================

    Generate HTML using python.
    a simple wrapper around the dom to make creating html easy

"""
from domonic.webapi.url import URL

from domonic.dom import Node, Element, Document, DocumentType, Comment, Text
from domonic.dom import HTMLDialogElement


html_tags = [
    "figcaption",
    "blockquote",
    "textarea",
    "progress",
    "optgroup",
    "noscript",
    "fieldset",
    "datalist",
    "colgroup",
    "summary",
    "section",
    "details",
    "command",
    "caption",
    "article",
    "address",
    "submit",
    "strong",
    "source",
    "select",
    "script",
    "output",
    "option",
    "legend",
    "keygen",
    "iframe",
    "hgroup",
    "header",
    "footer",
    "figure",
    "canvas",
    "button",
    "video",
    "track",
    "title",
    "thead",
    "tfoot",
    "tbody",
    "table",
    "style",
    "small",
    "param",
    "meter",
    "label",
    "input",
    "audio",
    "aside",
    "time",
    "span",
    "samp",
    "ruby",
    "meta",
    "menu",
    "mark",
    "link",
    "applet",
    "object",
    "basefont",
    "center",
    "dir",
    "embed",
    "isindex",
    "listing",
    "menuitem",
    "plaintext",
    "pre",
    "strike",
    "xmp",
    "template",
    "picture",
    "dialog",
    "html",
    "head",
    "form",
    "font",
    "code",
    "cite",
    "body",
    "base",
    "area",
    "abbr",
    "wbr",
    "var",
    "sup",
    "sub",
    "nav",
    "map",
    "main",
    "kbd",
    "ins",
    "img",
    "div",
    "dfn",
    "del",
    "col",
    "bdo",
    "bdi",
    "ul",
    "tr",
    "th",
    "td",
    "rt",
    "rp",
    "ol",
    "li",
    "hr",
    "h6",
    "h5",
    "h4",
    "h3",
    "h2",
    "h1",
    "em",
    "dt",
    "dl",
    "dd",
    "br",
    "u",
    "s",
    "q",
    "p",
    "i",
    "b",
    "a",
]
# big, blink, bold, tt, var,

html_attributes = [
    "accept",
    "accesskey",
    "action",
    "align",
    "alt",
    "async",
    "autocomplete",
    "autofocus",
    "autoplay",
    "bgcolor",
    "border",
    "charset",
    "checked",
    "cite",
    "class",
    "color",
    "cols",
    "colspan",
    "content",
    "contenteditable",
    "controls",
    "coords",
    "data",
    "datetime",
    "default",
    "defer",
    "dir",
    "dirname",
    "disabled",
    "download",
    "draggable",
    "enctype",
    "for",
    "form",
    "formaction",
    "headers",
    "height",
    "hidden",
    "high",
    "href",
    "hreflang",
    "id",
    "ismap",
    "kind",
    "label",
    "lang",
    "list",
    "loop",
    "low",
    "max",
    "maxlength",
    "media",
    "method",
    "min",
    "multiple",
    "muted",
    "name",
    "novalidate",
    "onabort",
    "onafterprint",
    "onbeforeprint",
    "onbeforeunload",
    "onblur",
    "oncanplay",
    "oncanplaythrough",
    "onchange",
    "onclick",
    "oncontextmenu",
    "oncopy",
    "oncuechange",
    "oncut",
    "ondblclick",
    "ondrag",
    "ondragend",
    "ondragenter",
    "ondragleave",
    "ondragover",
    "ondragstart",
    "ondrop",
    "ondurationchange",
    "onemptied",
    "onended",
    "onerror",
    "onfocus",
    "onhashchange",
    "oninput",
    "oninvalid",
    "onkeydown",
    "onkeypress",
    "onkeyup",
    "onload",
    "onloadeddata",
    "onloadedmetadata",
    "onloadstart",
    "onmousedown",
    "onmousemove",
    "onmouseout",
    "onmouseover",
    "onmouseup",
    "onmousewheel",
    "onoffline",
    "ononline",
    "onpagehide",
    "onpageshow",
    "onpaste",
    "onpause",
    "onplay",
    "onplaying",
    "onpopstate",
    "onprogress",
    "onratechange",
    "onreset",
    "onresize",
    "onscroll",
    "onsearch",
    "onseeked",
    "onseeking",
    "onselect",
    "onstalled",
    "onstorage",
    "onsubmit",
    "onsuspend",
    "ontimeupdate",
    "ontoggle",
    "onunload",
    "onvolumechange",
    "onwaiting",
    "onwheel",
    "open",
    "optimum",
    "pattern",
    "placeholder",
    "poster",
    "preload",
    "readonly",
    "rel",
    "required",
    "reversed",
    "rows",
    "rowspan",
    "sandbox",
    "scope",
    "selected",
    "shape",
    "size",
    "sizes",
    "span",
    "spellcheck",
    "src",
    "srcdoc",
    "srclang",
    "srcset",
    "start",
    "step",
    "style",
    "tabindex",
    "target",
    "title",
    "translate",
    "type",
    "usemap",
    "value",
    "width",
    "wrap",
    "property",
    "integrity",
    "crossorigin",
    "nonce",
    "autocapitalize",
    "enterkeyhint",
    "inputmode",
    "is",
    "itemid",
    "itemprop",
    "itemref",
    "itemscope",
    "itemtype",
    "part",
    "slot",
    "spellcheck",
    "alink",
    "nowrap",
    "vlink",
    "vspace",
    "language",
    "clear",
    "hspace",
    "xmlns",
    "about",
    "allowtransparency",
    "datatype",
    "inlist",
    "prefix",
    "resource",
    "rev",
    "typeof",
    "vocab",  # rdfa
    "playsinline",
    "autopictureinpicture",
    "buffered",
    "controlslist",
    "disableremoteplayback",  # video
]


def render(inp, outp="", to=None):  # doctype='html5')
    """write the input to string or to a file.

    Args:
        inp (obj): A domonic tag. For example div()
        outp (str): An optional output filename
        to (str): An optional output type. if 'pyml' is specified then pyml is returned instead of html.

    Returns:
        str: A HTML rendered string
    """
    if to == "pyml":
        if outp != "":
            with open(outp, "w+") as f:
                f.write(inp.__pyml__())
        return inp.__pyml__()
    # else:
    if outp != "":
        with open(outp, "w+") as f:
            f.write(str(inp))
    return str(inp)


class TemplateError(IndexError):
    def __init__(self, error, message="TemplateError: "):
        """[raised when a template error occurs]

        Args:
            error ([type]): [the error]
            message (str, optional): [description]. Defaults to "Templating error: ".
        """
        self.error = error
        self.hint = ""
        print(self.error)
        if str(self.error) == "list index out of range":
            self.hint = "MISSING UNDERSCORE ON AN ATTRIBUTE"
        self.message = message + self.hint
        super().__init__(self.message)


# class tag(Node):
#     """
#     The class from which all html tags extend.
#     """

#     pass


class closed_tag(Node):
    def __str__(self):
        return f"<{self.name}{self.__attributes__} />"


html = type("html", (Document,), {"name": "html"})
body = type("body", (Element,), {"name": "body"})
head = type("head", (Element,), {"name": "head"})
script = type("script", (Element,), {"name": "script"})
style = type("style", (Element,), {"name": "style"})
h1 = type("h1", (Element,), {"name": "h1"})
h2 = type("h2", (Element,), {"name": "h2"})
h3 = type("h3", (Element,), {"name": "h3"})
h4 = type("h4", (Element,), {"name": "h4"})
h5 = type("h5", (Element,), {"name": "h5"})
h6 = type("h6", (Element,), {"name": "h6"})
p = type("p", (Element,), {"name": "p"})
i = type("i", (Element,), {"name": "i"})
b = type("b", (Element,), {"name": "b"})

portal = type("portal", (Element,), {"name": "portal"})


def Atag(self, *args, **kwargs):

    # print('Atag: ', args, kwargs)
    Node.__init__(self, *args, **kwargs)
    Element.__init__(self, *args, **kwargs)

    # TODO - fix BUG. this stops having no href on a tags
    if kwargs.get("_href", None) is not None:
        URL.__init__(self, url=kwargs["_href"])
    else:
        URL.__init__(self, *args, **kwargs)


def __update__(self, *args, **kwargs):

    # print('__update__: ', args, kwargs)
    URL.__update__(self)

    # TODO - fix BUG. this stops having no href on a tags
    self.kwargs["_href"] = self.href
    Node.__init__(self, *args, **kwargs)


a = type(
    "a", (Element, URL), {"name": "a", "__init__": Atag}
)  # , '__update__': __update__})

ul = type("ul", (Element,), {"name": "ul"})
ol = type("ol", (Element,), {"name": "ol"})
li = type("li", (Element,), {"name": "li"})
div = type("div", (Element,), {"name": "div"})
strong = type("strong", (Element,), {"name": "strong"})
blockquote = type("blockquote", (Element,), {"name": "blockquote"})
table = type("table", (Element,), {"name": "table"})
tr = type("tr", (Element,), {"name": "tr"})
td = type("td", (Element,), {"name": "td"})
# form = type('form', (Element,), {'name': 'form'})


class form(Element):
    def __init__(self, *args, **kwargs):
        new_kwargs = {}
        for k, v in kwargs.items():
            if k[0] != "_":
                # print("WARNING: kwarg '{}' should begin with an underscore".format(k))
                new_kwargs[f"_{k}"] = v
            else:
                new_kwargs[k] = v
        kwargs = new_kwargs

        self.name = "form"
        Node.__init__(self, *args, **kwargs)
        Element.__init__(self, *args, **kwargs)

    @property
    def elements(self):
        kids = []
        for child in self.children:
            if isinstance(
                child, (button, fieldset, input, object, output, select, textarea)
            ):
                kids.append(child)
        return kids


label = type("label", (Element,), {"name": "label"})
# label.__doc__ = '''
#                 .. highlight:: python
#                 .. code-block:: python

#                     # used to label form elements. i.e.
#                     label(_for=None, _text=None, **kwargs)
#                     # <label for=""></label>
#                 '''

submit = type("submit", (Element,), {"name": "submit"})
title = type("title", (Element,), {"name": "title"})
noscript = type("noscript", (Element,), {"name": "noscript"})
section = type("section", (Element,), {"name": "section"})
nav = type("nav", (Element,), {"name": "nav"})
article = type("article", (Element,), {"name": "article"})
aside = type("aside", (Element,), {"name": "aside"})
hgroup = type("hgroup", (Element,), {"name": "hgroup"})
address = type("address", (Element,), {"name": "address"})
pre = type("pre", (Element,), {"name": "pre"})
dl = type("dl", (Element,), {"name": "dl"})
dt = type("dt", (Element,), {"name": "dt"})
dd = type("dd", (Element,), {"name": "dd"})
figure = type("figure", (Element,), {"name": "figure"})
figcaption = type("figcaption", (Element,), {"name": "figcaption"})
em = type("em", (Element,), {"name": "em"})
small = type("small", (Element,), {"name": "small"})
s = type("s", (Element,), {"name": "s"})
cite = type("cite", (Element,), {"name": "cite"})
q = type("q", (Element,), {"name": "q"})
dfn = type("dfn", (Element,), {"name": "dfn"})
abbr = type("abbr", (Element,), {"name": "abbr"})
code = type("code", (Element,), {"name": "code"})
var = type("var", (Element,), {"name": "var"})
samp = type("samp", (Element,), {"name": "samp"})
kbd = type("kbd", (Element,), {"name": "kbd"})
sub = type("sub", (Element,), {"name": "sub"})
sup = type("sup", (Element,), {"name": "sup"})
u = type("u", (Element,), {"name": "u"})
mark = type("mark", (Element,), {"name": "mark"})
ruby = type("ruby", (Element,), {"name": "ruby"})
rt = type("rt", (Element,), {"name": "rt"})
rp = type("rp", (Element,), {"name": "rp"})
bdi = type("bdi", (Element,), {"name": "bdi"})
bdo = type("bdo", (Element,), {"name": "bdo"})
span = type("span", (Element,), {"name": "span"})
ins = type("ins", (Element,), {"name": "ins"})
iframe = type("iframe", (Element,), {"name": "iframe"})
video = type("video", (Element,), {"name": "video"})
audio = type("audio", (Element,), {"name": "audio"})
canvas = type("canvas", (Element,), {"name": "canvas"})
caption = type("caption", (Element,), {"name": "caption"})
colgroup = type("colgroup", (Element,), {"name": "colgroup"})
tbody = type("tbody", (Element,), {"name": "tbody"})
thead = type("thead", (Element,), {"name": "thead"})
tfoot = type("tfoot", (Element,), {"name": "tfoot"})
th = type("th", (Element,), {"name": "th"})
fieldset = type("fieldset", (Element,), {"name": "fieldset"})
legend = type("legend", (Element,), {"name": "legend"})
button = type("button", (Element,), {"name": "button"})
select = type("select", (Element,), {"name": "select"})
datalist = type("datalist", (Element,), {"name": "datalist"})
optgroup = type("optgroup", (Element,), {"name": "optgroup"})
option = type("option", (Element,), {"name": "option"})
textarea = type("textarea", (Element,), {"name": "textarea"})
output = type("output", (Element,), {"name": "output"})  # ?----------
progress = type("progress", (Element,), {"name": "progress"})
meter = type("meter", (Element,), {"name": "meter"})
details = type("details", (Element,), {"name": "details"})
summary = type("summary", (Element,), {"name": "summary"})
menu = type("menu", (Element,), {"name": "menu"})
menuitem = type("menuitem", (Element,), {"name": "menuitem"})  # dead but may be used
font = type("font", (Element,), {"name": "font"})
header = type("header", (Element,), {"name": "header"})
footer = type("footer", (Element,), {"name": "footer"})
# map_ = type('map_', (tag,), {'name': 'map_'})
# object_ = type('object_', (tag,), {'name': 'object_'})
# del_ = type('del_', (tag,), {'name': 'del_'})
# time_ = type('time_', (tag,), {'name': 'time_'})

base = type("base", (closed_tag, Element, ), {"name": "base"},)
link = type("link", (closed_tag, Element,), {"name": "link"},)
meta = type("meta", (closed_tag, Element), {"name": "meta"})
hr = type("hr", (closed_tag, Element), {"name": "hr"})
br = type("br", (closed_tag, Element), {"name": "br"})
wbr = type("wbr", (closed_tag, Element), {"name": "wbr"})
img = type("img", (closed_tag, Element), {"name": "img"})
param = type("param", (closed_tag, Element), {"name": "param"})
source = type("source", (closed_tag, Element), {"name": "source"})
track = type("track", (closed_tag, Element), {"name": "track"})
area = type("area", (closed_tag, Element), {"name": "area"})
col = type("col", (closed_tag, Element), {"name": "col"})
input = type("input", (closed_tag, Element), {"name": "input"})
keygen = type("keygen", (closed_tag, Element), {"name": "keygen"})
command = type("command", (closed_tag, Element), {"name": "command"})

main = type("main", (Element,), {"name": "main"})

# obsolete
applet = type("applet", (Element,), {"name": "applet"})
# object = type('object', (Element,), {'name': 'object'})
basefont = type("basefont", (Element,), {"name": "basefont"})
center = type("center", (Element,), {"name": "center"})
# dir = type('dir', (Element,), {'name': 'dir'})
embed = type("embed", (Element,), {"name": "embed"})
isindex = type("isindex", (Element,), {"name": "isindex"})
listing = type("listing", (Element,), {"name": "listing"})
plaintext = type("plaintext", (Element,), {"name": "plaintext"})
s = type("s", (Element,), {"name": "s"})
u = type("u", (Element,), {"name": "u"})
strike = type("strike", (Element,), {"name": "strike"})
xmp = type("xmp", (Element,), {"name": "xmp"})

template = type("template", (Element,), {"name": "template"})
picture = type("picture", (Element,), {"name": "picture"})
dialog = type("dialog", (Element,), {"name": "dialog"})
# dialog = HTMLDialogElement  # TODO - might get rid of tag and put all its methods on Node directly

# legacy.
doctype = DocumentType
comment = Comment


def create_element(name="custom_tag", *args, **kwargs):
    """
    A method for creating custom tags

    tag name needs to be set due to custom tags with hyphens can't be classnames.
    i.e. hypenated tags <some-custom-tag></some-custom-tag>
    """
    # import sys
    # current_module = sys.modules[__name__]
    # checks if already exists
    if name in html_tags:
        # cl = globals()[name]
        return globals()[name](*args, **kwargs)

    # print('creating custom element')
    custom_tag = type("custom_tag", (Element,), {"name": name})
    new_tag = custom_tag(*args, **kwargs)
    new_tag.name = name
    return new_tag
