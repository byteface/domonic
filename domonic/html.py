"""
domonic.html
====================================

Generate HTML using python.

"""

from __future__ import annotations

from typing import Any

from domonic.dom import Document  # HTMLOptionsCollection,
from domonic.dom import (Comment, DocumentType, DOMConfig, Element,
                         HTMLAnchorElement, HTMLAreaElement, HTMLAudioElement,
                         HTMLBaseElement, HTMLBaseFontElement, HTMLBodyElement,
                         HTMLBRElement, HTMLButtonElement, HTMLCanvasElement,
                         HTMLContentElement, HTMLDataElement,
                         HTMLDataListElement, HTMLDialogElement,
                         HTMLDivElement, HTMLDListElement, HTMLDocument,
                         HTMLElement, HTMLEmbedElement, HTMLFieldSetElement,
                         HTMLFormControlsCollection, HTMLFormElement,
                         HTMLFrameSetElement, HTMLHeadElement,
                         HTMLHeadingElement, HTMLHRElement, HTMLIFrameElement,
                         HTMLImageElement, HTMLInputElement,
                         HTMLIsIndexElement, HTMLKeygenElement,
                         HTMLLabelElement, HTMLLegendElement, HTMLLIElement,
                         HTMLLinkElement, HTMLMapElement, HTMLMediaElement,
                         HTMLMetaElement, HTMLMeterElement, HTMLModElement,
                         HTMLObjectElement, HTMLOListElement,
                         HTMLOptGroupElement, HTMLOptionElement,
                         HTMLOutputElement, HTMLParagraphElement,
                         HTMLParamElement, HTMLPictureElement,
                         HTMLPortalElement, HTMLPreElement,
                         HTMLProgressElement, HTMLQuoteElement,
                         HTMLScriptElement, HTMLSelectedContentElement,
                         HTMLSelectElement, HTMLShadowElement, HTMLSlotElement,
                         HTMLSourceElement, HTMLSpanElement, HTMLStyleElement,
                         HTMLTableCaptionElement, HTMLTableCellElement,
                         HTMLTableColElement, HTMLTableDataCellElement,
                         HTMLTableElement, HTMLTableHeaderCellElement,
                         HTMLTableRowElement, HTMLTableSectionElement,
                         HTMLTemplateElement, HTMLTextAreaElement,
                         HTMLTimeElement, HTMLTitleElement, HTMLTrackElement,
                         HTMLUListElement, HTMLUnknownElement,
                         HTMLVideoElement, Node, Text)
from domonic.webapi.url import URL

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
    "selectedcontent",
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
    "applet",
    "object",
    "portal",
    "slot",
    "search",
    "basefont",
    "center",
    "embed",
    "frame",
    "frameset",
    "isindex",
    "listing",
    "menuitem",
    "noframes",
    "plaintext",
    "strike",
    "template",
    "picture",
    "dialog",
    "data",
    "time",
    "span",
    "samp",
    "ruby",
    "meta",
    "menu",
    "mark",
    "link",
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
    "main",
    "dir",
    "mod",
    "wbr",
    "var",
    "sup",
    "sub",
    "nav",
    "map",
    "kbd",
    "ins",
    "img",
    "div",
    "dfn",
    "del",
    "col",
    "bdo",
    "bdi",
    "pre",
    "xmp",
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
# big, blink, bold, tt, var, frameset

_HTML_TAG_LOOKUP = set(html_tags)
_TAG_ALIASES = {"del": "del_"}

html_attributes = [
    "accept",
    "accept-charset",
    "accesskey",
    "alpha",
    "loading",
    "action",
    "align",
    "alt",
    "async",
    "autocomplete",
    "autofocus",
    "autoplay",
    "abbr",
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
    "colorspace",
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
    "formenctype",
    "formmethod",
    "formnovalidate",
    "formtarget",
    "headers",
    "headingoffset",
    "headingreset",
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
    "onauxclick",
    "onbeforeprint",
    "onbeforeinput",
    "onbeforematch",
    "onbeforetoggle",
    "onbeforeunload",
    "onblur",
    "oncancel",
    "oncanplay",
    "oncanplaythrough",
    "onchange",
    "onclick",
    "onclose",
    "oncommand",
    "oncontextmenu",
    "oncontextlost",
    "oncontextrestored",
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
    "onformdata",
    "onhashchange",
    "oninput",
    "oninvalid",
    "onkeydown",
    "onkeypress",
    "onkeyup",
    "onlanguagechange",
    "onload",
    "onloadeddata",
    "onloadedmetadata",
    "onloadstart",
    "onmessage",
    "onmessageerror",
    "onmouseenter",
    "onmouseleave",
    "onmousedown",
    "onmousemove",
    "onmouseout",
    "onmouseover",
    "onmouseup",
    "onmousewheel",
    "onoffline",
    "ononline",
    "onpagehide",
    "onpagereveal",
    "onpageshow",
    "onpageswap",
    "onpaste",
    "onpause",
    "onplay",
    "onplaying",
    "onpopstate",
    "onprogress",
    "onratechange",
    "onreset",
    "onresize",
    "onrejectionhandled",
    "onscroll",
    "onscrollend",
    "onsearch",
    "onsecuritypolicyviolation",
    "onseeked",
    "onseeking",
    "onselect",
    "onslotchange",
    "onstalled",
    "onstorage",
    "onsubmit",
    "onsuspend",
    "ontimeupdate",
    "ontoggle",
    "onunhandledrejection",
    "onunload",
    "onvolumechange",
    "onwaiting",
    "onwheel",
    "open",
    "optimum",
    "pattern",
    "placeholder",
    "ping",
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
    "http-equiv",
    "inlist",
    "allow",
    "allowfullscreen",
    "anchor",
    "as",
    "autocorrect",
    "blocking",
    "browsingtopics",
    "capture",
    "closedby",
    "command",
    "commandfor",
    "credentialless",
    "decoding",
    "disablepictureinpicture",
    "exportparts",
    "fetchpriority",
    "imagesizes",
    "imagesrcset",
    "inert",
    "interestfor",
    "minlength",
    "nomodule",
    "popovertarget",
    "popovertargetaction",
    "popover",
    "referrerpolicy",
    "shadowrootclonable",
    "shadowrootcustomelementregistry",
    "shadowrootdelegatesfocus",
    "shadowrootmode",
    "shadowrootserializable",
    "shadowrootslotassignment",
    "writingsuggestions",
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


def render(inp: Node, outp: str = "", to: str | None = None) -> str:
    """
    Render an HTML element or document to a string or file.

    Args:
        inp (obj): A domonic tag. For example div()
        outp (str): An optional output filename
        to (str): An optional output type. if 'pyml' is specified then pyml is returned instead of html.

    Returns:
        str: The rendered HTML string (or PyML if specified).

    Examples:
        >>> div()
        '<div></div>'
        >>> render(div(), outp='output.html')
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
    def __init__(self, error: Exception, message: str = "TemplateError: "):
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


tag = Node  # legacy support?. TODO - remove in future? 0.0.9


class closed_tag(Node):
    def __str__(self):
        if DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH:
            if DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH:
                return f"<{self.name}{self.__attributes__} />"
            else:
                return f"<{self.name}{self.__attributes__}/>"
        return f"<{self.name}{self.__attributes__}>"


html = type("html", (HTMLDocument,), {"name": "html"})
body = type("body", (HTMLBodyElement,), {"name": "body"})
head = type("head", (HTMLHeadElement,), {"name": "head"})
script = type("script", (HTMLScriptElement,), {"name": "script"})
style = type("style", (HTMLStyleElement,), {"name": "style"})
h1 = type("h1", (HTMLHeadingElement,), {"name": "h1"})
h2 = type("h2", (HTMLHeadingElement,), {"name": "h2"})
h3 = type("h3", (HTMLHeadingElement,), {"name": "h3"})
h4 = type("h4", (HTMLHeadingElement,), {"name": "h4"})
h5 = type("h5", (HTMLHeadingElement,), {"name": "h5"})
h6 = type("h6", (HTMLHeadingElement,), {"name": "h6"})
p = type("p", (HTMLParagraphElement,), {"name": "p"})

i = type("i", (Element,), {"name": "i"})
b = type("b", (Element,), {"name": "b"})
portal = type("portal", (HTMLPortalElement, Element), {"name": "portal"})


def Atag(self, *args: Any, **kwargs: Any) -> None:
    """
    Base class for the a tag
    """
    HTMLAnchorElement.__init__(self, *args, **kwargs)


a = type("a", (HTMLAnchorElement, Element, URL), {"name": "a", "__init__": Atag})
ul = type("ul", (HTMLUListElement,), {"name": "ul"})
ol = type("ol", (HTMLOListElement,), {"name": "ol"})
li = type("li", (HTMLLIElement,), {"name": "li"})
div = type("div", (HTMLDivElement,), {"name": "div"})

strong = type("strong", (Element,), {"name": "strong"})
blockquote = type("blockquote", (Element,), {"name": "blockquote"})
table = type("table", (HTMLTableElement,), {"name": "table"})
tr = type("tr", (HTMLTableRowElement,), {"name": "tr"})
td = type("td", (HTMLTableCellElement,), {"name": "td"})


class form(HTMLFormElement):

    def __init__(self, *args: Any, **kwargs: Any):
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
    def elements(self) -> HTMLFormControlsCollection:
        return super().elements


label = type("label", (HTMLLabelElement,), {"name": "label"})
# label.__doc__ = '''
#                 .. highlight:: python
#                 .. code-block:: python

#                     # used to label form elements. i.e.
#                     label(_for=None, _text=None, **kwargs)
#                     # <label for=""></label>
#                 '''

submit = type("submit", (Element,), {"name": "submit"})
title = type("title", (HTMLTitleElement,), {"name": "title"})
noscript = type("noscript", (Element,), {"name": "noscript"})
section = type("section", (Element,), {"name": "section"})
nav = type("nav", (Element,), {"name": "nav"})
article = type("article", (Element,), {"name": "article"})
aside = type("aside", (Element,), {"name": "aside"})
hgroup = type("hgroup", (Element,), {"name": "hgroup"})
address = type("address", (Element,), {"name": "address"})
pre = type("pre", (HTMLPreElement,), {"name": "pre"})
dl = type("dl", (HTMLDListElement,), {"name": "dl"})
dt = type("dt", (Element,), {"name": "dt"})
dd = type("dd", (Element,), {"name": "dd"})
figure = type("figure", (Element,), {"name": "figure"})
figcaption = type("figcaption", (Element,), {"name": "figcaption"})
em = type("em", (Element,), {"name": "em"})
small = type("small", (Element,), {"name": "small"})
s = type("s", (Element,), {"name": "s"})
cite = type("cite", (Element,), {"name": "cite"})
q = type("q", (HTMLQuoteElement,), {"name": "q"})
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
span = type("span", (HTMLSpanElement,), {"name": "span"})
ins = type("ins", (Element,), {"name": "ins"})
iframe = type("iframe", (HTMLIFrameElement,), {"name": "iframe"})
video = type("video", (HTMLVideoElement,), {"name": "video"})
audio = type("audio", (HTMLAudioElement,), {"name": "audio"})
canvas = type("canvas", (HTMLCanvasElement,), {"name": "canvas"})
caption = type("caption", (HTMLTableCaptionElement,), {"name": "caption"})
colgroup = type("colgroup", (Element,), {"name": "colgroup"})
tbody = type("tbody", (HTMLTableSectionElement,), {"name": "tbody"})
thead = type(
    "thead", (Element,), {"name": "thead"}
)  # Note - also should extend HTMLTableSectionElement
tfoot = type("tfoot", (Element,), {"name": "tfoot"})
th = type("th", (HTMLTableHeaderCellElement,), {"name": "th"})
fieldset = type("fieldset", (HTMLFieldSetElement,), {"name": "fieldset"})
legend = type("legend", (HTMLLegendElement,), {"name": "legend"})
button = type("button", (HTMLButtonElement,), {"name": "button"})
select = type("select", (HTMLSelectElement,), {"name": "select"})
selectedcontent = type(
    "selectedcontent", (HTMLSelectedContentElement,), {"name": "selectedcontent"}
)
datalist = type("datalist", (HTMLDataListElement,), {"name": "datalist"})
optgroup = type("optgroup", (HTMLOptGroupElement,), {"name": "optgroup"})
option = type("option", (HTMLOptionElement,), {"name": "option"})
textarea = type("textarea", (HTMLTextAreaElement,), {"name": "textarea"})
output = type("output", (HTMLOutputElement,), {"name": "output"})
progress = type("progress", (HTMLProgressElement,), {"name": "progress"})
meter = type("meter", (HTMLMeterElement,), {"name": "meter"})
details = type("details", (Element,), {"name": "details"})
summary = type("summary", (Element,), {"name": "summary"})
menu = type("menu", (Element,), {"name": "menu"})
menuitem = type("menuitem", (Element,), {"name": "menuitem"})  # dead but may be used
font = type("font", (Element,), {"name": "font"})
header = type("header", (Element,), {"name": "header"})
footer = type("footer", (Element,), {"name": "footer"})
map = type("map", (HTMLMapElement,), {"name": "map"})
object = type("object", (HTMLObjectElement,), {"name": "object"})
del_ = type("del_", (HTMLModElement,), {"name": "del"})
mod = type("mod", (HTMLModElement,), {"name": "mod"})

time = type("time", (HTMLTimeElement,), {"name": "time"})
data = type("data", (HTMLDataElement,), {"name": "data"})

base = type("base", (closed_tag, HTMLBaseElement), {"name": "base"})
link = type(
    "link", (closed_tag, HTMLLinkElement), {"name": "link"}
)  # HTMLLinkElement TODO - closed tags
meta = type(
    "meta", (closed_tag, HTMLMetaElement), {"name": "meta"}
)  # HTMLMetaElement TODO - closed tags
hr = type("hr", (closed_tag, HTMLHRElement), {"name": "hr"})
br = type(
    "br",
    (
        closed_tag,
        HTMLBRElement,
    ),
    {"name": "br"},
)
wbr = type("wbr", (closed_tag, Element), {"name": "wbr"})
img = type("img", (closed_tag, HTMLImageElement), {"name": "img"})
param = type("param", (closed_tag, HTMLParamElement), {"name": "param"})
source = type("source", (closed_tag, HTMLSourceElement), {"name": "source"})
track = type("track", (closed_tag, HTMLTrackElement), {"name": "track"})
area = type("area", (closed_tag, HTMLAreaElement), {"name": "area"})
col = type("col", (closed_tag, HTMLTableColElement), {"name": "col"})
input = type("input", (closed_tag, HTMLInputElement), {"name": "input"})
keygen = type("keygen", (closed_tag, HTMLKeygenElement), {"name": "keygen"})
command = type("command", (closed_tag, Element), {"name": "command"})

main = type("main", (Element,), {"name": "main"})
slot = type("slot", (HTMLSlotElement,), {"name": "slot"})
search = type("search", (Element,), {"name": "search"})

# obsolete
applet = type("applet", (Element,), {"name": "applet"})
basefont = type("basefont", (HTMLBaseFontElement,), {"name": "basefont"})
center = type("center", (Element,), {"name": "center"})
dir = type("dir", (Element,), {"name": "dir"})
embed = type("embed", (closed_tag, HTMLEmbedElement), {"name": "embed"})
frame = type("frame", (Element,), {"name": "frame"})
frameset = type("frameset", (HTMLFrameSetElement,), {"name": "frameset"})
isindex = type("isindex", (Element,), {"name": "isindex"})
listing = type("listing", (Element,), {"name": "listing"})
noframes = type("noframes", (Element,), {"name": "noframes"})
plaintext = type("plaintext", (Element,), {"name": "plaintext"})
strike = type("strike", (Element,), {"name": "strike"})
xmp = type("xmp", (Element,), {"name": "xmp"})
# shadow

template = type("template", (HTMLTemplateElement,), {"name": "template"})

picture = type("picture", (HTMLPictureElement,), {"name": "picture"})
dialog = type("dialog", (HTMLDialogElement,), {"name": "dialog"})

# legacy.
doctype = type("doctype", (DocumentType,), {"name": "doctype"})
comment = type("comment", (Comment,), {"name": "comment"})
content = type("content", (HTMLContentElement,), {"name": "content"})


def create_element(name: str = "custom_tag", *args: Any, **kwargs: Any) -> Element:
    """
    A method for creating custom tags

    tag name needs to be set due to custom tags with hyphens can't be classnames.
    i.e. hypenated tags <some-custom-tag></some-custom-tag>
    """
    # checks if already exists
    normalized_name = str(name).strip().lower()
    if not normalized_name:
        normalized_name = "custom_tag"
        name = "custom_tag"
    if normalized_name in _HTML_TAG_LOOKUP:
        tag_name = _TAG_ALIASES.get(normalized_name, normalized_name)
        return globals()[tag_name](*args, **kwargs)

    try:
        from domonic.window import window as domonic_window

        registry = getattr(domonic_window, "customElements", None)
        if registry is not None:
            registered = registry.get(name) or registry.get(normalized_name)
            if registered is not None:
                return registered(*args, **kwargs)
    except Exception:
        pass

    # NOTE: we care calling it custom_tag because it can't have hyphens < Note - use HTMLUnknownElement?
    custom_tag = type("custom_tag", (Element,), {"name": name})
    new_tag = custom_tag(*args, **kwargs)
    new_tag.name = name
    return new_tag
