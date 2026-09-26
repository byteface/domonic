"""
domonic.html
====================================

Generate HTML using python.

"""

from __future__ import annotations

import json
import re
from typing import TYPE_CHECKING, Any

from domonic.dom import Document  # HTMLOptionsCollection,
from domonic.dom import (
    Comment,
    DocumentType,
    DOMConfig,
    Element,
    HTMLAnchorElement,
    HTMLAreaElement,
    HTMLAudioElement,
    HTMLBaseElement,
    HTMLBaseFontElement,
    HTMLBodyElement,
    HTMLBRElement,
    HTMLButtonElement,
    HTMLCanvasElement,
    HTMLContentElement,
    HTMLDataElement,
    HTMLDataListElement,
    HTMLDetailsElement,
    HTMLDialogElement,
    HTMLDivElement,
    HTMLDListElement,
    HTMLDocument,
    HTMLElement,
    HTMLEmbedElement,
    HTMLFieldSetElement,
    HTMLFormControlsCollection,
    HTMLFormElement,
    HTMLFrameSetElement,
    HTMLHeadElement,
    HTMLHeadingElement,
    HTMLHRElement,
    HTMLIFrameElement,
    HTMLImageElement,
    HTMLInputElement,
    HTMLIsIndexElement,
    HTMLKeygenElement,
    HTMLLabelElement,
    HTMLLegendElement,
    HTMLLIElement,
    HTMLLinkElement,
    HTMLMapElement,
    HTMLMediaElement,
    HTMLMenuElement,
    HTMLMetaElement,
    HTMLMeterElement,
    HTMLModElement,
    HTMLObjectElement,
    HTMLOListElement,
    HTMLOptGroupElement,
    HTMLOptionElement,
    HTMLOutputElement,
    HTMLParagraphElement,
    HTMLParamElement,
    HTMLPictureElement,
    HTMLPortalElement,
    HTMLPreElement,
    HTMLProgressElement,
    HTMLQuoteElement,
    HTMLScriptElement,
    HTMLSelectedContentElement,
    HTMLSelectElement,
    HTMLShadowElement,
    HTMLSlotElement,
    HTMLSourceElement,
    HTMLSpanElement,
    HTMLStyleElement,
    HTMLSummaryElement,
    HTMLTableCaptionElement,
    HTMLTableCellElement,
    HTMLTableColElement,
    HTMLTableDataCellElement,
    HTMLTableElement,
    HTMLTableHeaderCellElement,
    HTMLTableRowElement,
    HTMLTableSectionElement,
    HTMLTemplateElement,
    HTMLTextAreaElement,
    HTMLTimeElement,
    HTMLTitleElement,
    HTMLTrackElement,
    HTMLUListElement,
    HTMLUnknownElement,
    HTMLVideoElement,
    Node,
)
from domonic.dom import RawHTML as raw
from domonic.dom import (
    Text,
)
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
    "hx-partial",
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
_TAG_ALIASES = {"del": "del_", "hx-partial": "hx_partial"}
# tag name -> element class, populated lazily by ``create_element`` for names
# that are already lower-case (the common ``createElement("div")`` path)
_HTML_TAG_CLASSES: dict = {}

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
    "attributionsrc",
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
    "ontoolactivated",
    "ontoolcancel",
    "ontoolchange",
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
    "toolautosubmit",
    "tooldescription",
    "toolname",
    "toolparamdescription",
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
    "elementtiming",
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
            stream = getattr(inp, "stream", None)
            if callable(stream):
                for chunk in stream():
                    f.write(chunk)
            else:
                f.write(str(inp))
    return str(inp)


def _json_script(type_value: str, payload: Any, *, indent: int | None = None, **kwargs: Any) -> HTMLScriptElement:
    if isinstance(payload, str):
        content = payload
    else:
        dump_kwargs: dict[str, Any] = {"indent": indent}
        if indent is None:
            dump_kwargs["separators"] = (",", ":")
        content = json.dumps(payload, **dump_kwargs)

    kwargs["_type"] = type_value
    return script(content, **kwargs)


def importmap(mapping: Any, *, indent: int | None = None, **kwargs: Any) -> HTMLScriptElement:
    """
    Create a <script type="importmap"> block from JSON import map data.

    Args:
        mapping: A JSON-serializable import map object, or a pre-rendered JSON string.
        indent: Optional JSON indentation for readable output.
        **kwargs: Extra script attributes.

    Returns:
        HTMLScriptElement: A script element containing import map JSON.
    """
    return _json_script("importmap", mapping, indent=indent, **kwargs)


def speculationrules(rules: Any, *, indent: int | None = None, **kwargs: Any) -> HTMLScriptElement:
    """
    Create a <script type="speculationrules"> block from JSON rules.

    Args:
        rules: A JSON-serializable rules object, or a pre-rendered JSON string.
        indent: Optional JSON indentation for readable output.
        **kwargs: Extra script attributes.

    Returns:
        HTMLScriptElement: A script element containing speculation rules JSON.
    """
    return _json_script("speculationrules", rules, indent=indent, **kwargs)


class TemplateError(IndexError):
    def __init__(self, error: Exception, message: str = "TemplateError: "):
        """raised when a template error occurs

        Args:
            error (Exception): The underlying error.
            message (str, optional): Defaults to "TemplateError: ".
        """
        self.error = error
        self.hint = ""
        print(self.error)
        if str(self.error) == "list index out of range":
            self.hint = "MISSING UNDERSCORE ON AN ATTRIBUTE"
        self.message = message + self.hint
        super().__init__(self.message)


tag = Node  # legacy support


class closed_tag(Node):
    def __str__(self):
        return "".join(self.stream())

    def stream(self):
        if DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH:
            if DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH:
                yield f"<{self.name}{self.__attributes__} />"
            else:
                yield f"<{self.name}{self.__attributes__}/>"
            return
        yield f"<{self.name}{self.__attributes__}>"


_DOCTYPE_LITERAL_RE = re.compile(
    r"""<!DOCTYPE\s+(?P<name>[^\s>]+)
        (?:\s+PUBLIC\s+"(?P<public>[^"]*)")?
        (?:\s+(?:SYSTEM\s+)?"(?P<system>[^"]*)")?
    """,
    re.IGNORECASE | re.VERBOSE,
)


def _resolve_doctype(spec: Any) -> DocumentType:
    """Coerce an ``html(..., _doctype=...)`` / ``Webpage`` argument into a
    :class:`~domonic.dom.DocumentType`.

    Accepts ``True`` (HTML5), an existing ``DocumentType``, a key from
    ``domonic.constants.doctypes`` (e.g. ``"HTML5"``, ``"XHTML1_1"``), a bare
    root-element name (``"html"``), or a literal ``"<!DOCTYPE ...>"`` string.
    """
    if spec is True:
        return DocumentType("html", "", "")
    if isinstance(spec, DocumentType):
        return spec
    if isinstance(spec, str):
        from domonic.constants import doctypes

        text = doctypes.get(spec, doctypes.get(spec.upper(), spec)).strip()
        match = _DOCTYPE_LITERAL_RE.match(text)
        if match:
            return DocumentType(
                match.group("name"),
                match.group("public") or "",
                match.group("system") or "",
            )
        return DocumentType(text or "html", "", "")
    raise TypeError(f"Unsupported _doctype value: {spec!r}")


def _html_tag_init(self, *args, _doctype=None, **kwargs):
    """``html`` tag constructor: like ``HTMLDocument`` but with an optional
    ``_doctype`` keyword so a full page can be built in one call, e.g.
    ``html(head(...), body(...), _doctype=True)``. ``Document.doctype`` stays
    ``None`` when the keyword is omitted, matching the parser and the DOM
    spec."""
    HTMLDocument.__init__(self, *args, **kwargs)
    if _doctype not in (None, False):
        self.doctype = _resolve_doctype(_doctype)


def Atag(self, *args: Any, **kwargs: Any) -> None:
    """
    Base class for the a tag
    """
    HTMLAnchorElement.__init__(self, *args, **kwargs)


class form(HTMLFormElement):

    def __init__(self, *args: Any, **kwargs: Any):
        new_kwargs = {}
        for k, v in kwargs.items():
            if k[0] != "_":
                new_kwargs[f"_{k}"] = v
            else:
                new_kwargs[k] = v
        kwargs = new_kwargs

        self.name = "form"
        # Element.__init__ already calls Node.__init__ via super() -- calling
        # Node.__init__ directly here too ran its whole body twice per form()
        # construction, including the `with node:` auto-append
        # (Node.__context[-1] += self), which appended every form built
        # inside a `with` block to the context node twice.
        Element.__init__(self, *args, **kwargs)

    @property
    def elements(self) -> HTMLFormControlsCollection:
        return super().elements


if TYPE_CHECKING:
    # What type checkers and IDEs see for the tag constructors that the
    # else branch builds with type(): ``div(...) -> div``, carrying the base
    # element's attributes and methods. Keep this list in step with the
    # ``type(...)`` calls below (tests/test_html.py::test_tag_typing_stubs).
    # fmt: off
    class html(HTMLDocument): ...
    class body(HTMLBodyElement): ...
    class head(HTMLHeadElement): ...
    class hx_partial(Element): ...
    class script(HTMLScriptElement): ...
    class style(HTMLStyleElement): ...
    class h1(HTMLHeadingElement): ...
    class h2(HTMLHeadingElement): ...
    class h3(HTMLHeadingElement): ...
    class h4(HTMLHeadingElement): ...
    class h5(HTMLHeadingElement): ...
    class h6(HTMLHeadingElement): ...
    class p(HTMLParagraphElement): ...
    class i(HTMLElement): ...
    class b(HTMLElement): ...
    class portal(HTMLPortalElement, Element): ...
    class a(HTMLAnchorElement, Element, URL): ...
    class ul(HTMLUListElement): ...
    class ol(HTMLOListElement): ...
    class li(HTMLLIElement): ...
    class div(HTMLDivElement): ...
    class strong(HTMLElement): ...
    class blockquote(HTMLQuoteElement): ...
    class table(HTMLTableElement): ...
    class tr(HTMLTableRowElement): ...
    class td(HTMLTableCellElement): ...
    class label(HTMLLabelElement): ...
    class submit(HTMLElement): ...
    class title(HTMLTitleElement): ...
    class noscript(HTMLElement): ...
    class section(HTMLElement): ...
    class nav(HTMLElement): ...
    class article(HTMLElement): ...
    class aside(HTMLElement): ...
    class hgroup(HTMLElement): ...
    class address(HTMLElement): ...
    class pre(HTMLPreElement): ...
    class dl(HTMLDListElement): ...
    class dt(HTMLElement): ...
    class dd(HTMLElement): ...
    class figure(HTMLElement): ...
    class figcaption(HTMLElement): ...
    class em(HTMLElement): ...
    class small(HTMLElement): ...
    class s(HTMLElement): ...
    class cite(HTMLElement): ...
    class q(HTMLQuoteElement): ...
    class dfn(HTMLElement): ...
    class abbr(HTMLElement): ...
    class code(HTMLElement): ...
    class var(HTMLElement): ...
    class samp(HTMLElement): ...
    class kbd(HTMLElement): ...
    class sub(HTMLElement): ...
    class sup(HTMLElement): ...
    class u(HTMLElement): ...
    class mark(HTMLElement): ...
    class ruby(HTMLElement): ...
    class rt(HTMLElement): ...
    class rp(HTMLElement): ...
    class bdi(HTMLElement): ...
    class bdo(HTMLElement): ...
    class span(HTMLSpanElement): ...
    class ins(HTMLModElement): ...
    class iframe(HTMLIFrameElement): ...
    class video(HTMLVideoElement): ...
    class audio(HTMLAudioElement): ...
    class canvas(HTMLCanvasElement): ...
    class caption(HTMLTableCaptionElement): ...
    class colgroup(HTMLTableColElement): ...
    class tbody(HTMLTableSectionElement): ...
    class thead(HTMLTableSectionElement): ...
    class tfoot(HTMLTableSectionElement): ...
    class th(HTMLTableHeaderCellElement): ...
    class fieldset(HTMLFieldSetElement): ...
    class legend(HTMLLegendElement): ...
    class button(HTMLButtonElement): ...
    class select(HTMLSelectElement): ...
    class selectedcontent(HTMLSelectedContentElement): ...
    class datalist(HTMLDataListElement): ...
    class optgroup(HTMLOptGroupElement): ...
    class option(HTMLOptionElement): ...
    class textarea(HTMLTextAreaElement): ...
    class output(HTMLOutputElement): ...
    class progress(HTMLProgressElement): ...
    class meter(HTMLMeterElement): ...
    class details(HTMLDetailsElement): ...
    class summary(HTMLSummaryElement): ...
    class menu(HTMLMenuElement): ...
    class menuitem(HTMLElement): ...
    class font(HTMLElement): ...
    class header(HTMLElement): ...
    class footer(HTMLElement): ...
    class map(HTMLMapElement): ...
    class object(HTMLObjectElement): ...
    class del_(HTMLModElement): ...
    class mod(HTMLModElement): ...
    class time(HTMLTimeElement): ...
    class data(HTMLDataElement): ...
    class base(closed_tag, HTMLBaseElement): ...
    class link(closed_tag, HTMLLinkElement): ...
    class meta(closed_tag, HTMLMetaElement): ...
    class hr(closed_tag, HTMLHRElement): ...
    class br(closed_tag, HTMLBRElement): ...
    class wbr(closed_tag, HTMLElement): ...
    class img(closed_tag, HTMLImageElement): ...
    class param(closed_tag, HTMLParamElement): ...
    class source(closed_tag, HTMLSourceElement): ...
    class track(closed_tag, HTMLTrackElement): ...
    class area(closed_tag, HTMLAreaElement): ...
    class col(closed_tag, HTMLTableColElement): ...
    class input(closed_tag, HTMLInputElement): ...
    class keygen(closed_tag, HTMLKeygenElement): ...
    class command(closed_tag, Element): ...
    class main(HTMLElement): ...
    class slot(HTMLSlotElement): ...
    class search(HTMLElement): ...
    class applet(HTMLUnknownElement): ...
    class basefont(HTMLBaseFontElement): ...
    class center(HTMLElement): ...
    class dir(HTMLElement): ...
    class embed(closed_tag, HTMLEmbedElement): ...
    class frame(HTMLElement): ...
    class frameset(HTMLFrameSetElement): ...
    class isindex(HTMLIsIndexElement): ...
    class listing(HTMLElement): ...
    class noframes(HTMLElement): ...
    class plaintext(HTMLElement): ...
    class strike(HTMLElement): ...
    class xmp(HTMLElement): ...
    class template(HTMLTemplateElement): ...
    class picture(HTMLPictureElement): ...
    class dialog(HTMLDialogElement): ...
    class doctype(DocumentType): ...
    class comment(Comment): ...
    class content(HTMLContentElement): ...
    # fmt: on

else:
    html = type("html", (HTMLDocument,), {"name": "html", "__init__": _html_tag_init})
    body = type("body", (HTMLBodyElement,), {"name": "body"})
    head = type("head", (HTMLHeadElement,), {"name": "head"})
    hx_partial = type("hx-partial", (Element,), {"name": "hx-partial"})
    script = type("script", (HTMLScriptElement,), {"name": "script"})
    style = type("style", (HTMLStyleElement,), {"name": "style"})
    h1 = type("h1", (HTMLHeadingElement,), {"name": "h1"})
    h2 = type("h2", (HTMLHeadingElement,), {"name": "h2"})
    h3 = type("h3", (HTMLHeadingElement,), {"name": "h3"})
    h4 = type("h4", (HTMLHeadingElement,), {"name": "h4"})
    h5 = type("h5", (HTMLHeadingElement,), {"name": "h5"})
    h6 = type("h6", (HTMLHeadingElement,), {"name": "h6"})
    p = type("p", (HTMLParagraphElement,), {"name": "p"})

    i = type("i", (HTMLElement,), {"name": "i"})
    b = type("b", (HTMLElement,), {"name": "b"})
    portal = type("portal", (HTMLPortalElement, Element), {"name": "portal"})

    a = type("a", (HTMLAnchorElement, Element, URL), {"name": "a", "__init__": Atag})
    ul = type("ul", (HTMLUListElement,), {"name": "ul"})
    ol = type("ol", (HTMLOListElement,), {"name": "ol"})
    li = type("li", (HTMLLIElement,), {"name": "li"})
    div = type("div", (HTMLDivElement,), {"name": "div"})

    strong = type("strong", (HTMLElement,), {"name": "strong"})
    blockquote = type("blockquote", (HTMLQuoteElement,), {"name": "blockquote"})
    table = type("table", (HTMLTableElement,), {"name": "table"})
    tr = type("tr", (HTMLTableRowElement,), {"name": "tr"})
    td = type("td", (HTMLTableCellElement,), {"name": "td"})

    label = type("label", (HTMLLabelElement,), {"name": "label"})
    # label.__doc__ = '''
    #                 .. highlight:: python
    #                 .. code-block:: python

    #                     # used to label form elements. i.e.
    #                     label(_for=None, _text=None, **kwargs)
    #                     # <label for=""></label>
    #                 '''

    submit = type("submit", (HTMLElement,), {"name": "submit"})
    title = type("title", (HTMLTitleElement,), {"name": "title"})
    noscript = type("noscript", (HTMLElement,), {"name": "noscript"})
    section = type("section", (HTMLElement,), {"name": "section"})
    nav = type("nav", (HTMLElement,), {"name": "nav"})
    article = type("article", (HTMLElement,), {"name": "article"})
    aside = type("aside", (HTMLElement,), {"name": "aside"})
    hgroup = type("hgroup", (HTMLElement,), {"name": "hgroup"})
    address = type("address", (HTMLElement,), {"name": "address"})
    pre = type("pre", (HTMLPreElement,), {"name": "pre"})
    dl = type("dl", (HTMLDListElement,), {"name": "dl"})
    dt = type("dt", (HTMLElement,), {"name": "dt"})
    dd = type("dd", (HTMLElement,), {"name": "dd"})
    figure = type("figure", (HTMLElement,), {"name": "figure"})
    figcaption = type("figcaption", (HTMLElement,), {"name": "figcaption"})
    em = type("em", (HTMLElement,), {"name": "em"})
    small = type("small", (HTMLElement,), {"name": "small"})
    s = type("s", (HTMLElement,), {"name": "s"})
    cite = type("cite", (HTMLElement,), {"name": "cite"})
    q = type("q", (HTMLQuoteElement,), {"name": "q"})
    dfn = type("dfn", (HTMLElement,), {"name": "dfn"})
    abbr = type("abbr", (HTMLElement,), {"name": "abbr"})
    code = type("code", (HTMLElement,), {"name": "code"})
    var = type("var", (HTMLElement,), {"name": "var"})
    samp = type("samp", (HTMLElement,), {"name": "samp"})
    kbd = type("kbd", (HTMLElement,), {"name": "kbd"})
    sub = type("sub", (HTMLElement,), {"name": "sub"})
    sup = type("sup", (HTMLElement,), {"name": "sup"})
    u = type("u", (HTMLElement,), {"name": "u"})
    mark = type("mark", (HTMLElement,), {"name": "mark"})
    ruby = type("ruby", (HTMLElement,), {"name": "ruby"})
    rt = type("rt", (HTMLElement,), {"name": "rt"})
    rp = type("rp", (HTMLElement,), {"name": "rp"})
    bdi = type("bdi", (HTMLElement,), {"name": "bdi"})
    bdo = type("bdo", (HTMLElement,), {"name": "bdo"})
    span = type("span", (HTMLSpanElement,), {"name": "span"})
    ins = type("ins", (HTMLModElement,), {"name": "ins"})
    iframe = type("iframe", (HTMLIFrameElement,), {"name": "iframe"})
    video = type("video", (HTMLVideoElement,), {"name": "video"})
    audio = type("audio", (HTMLAudioElement,), {"name": "audio"})
    canvas = type("canvas", (HTMLCanvasElement,), {"name": "canvas"})
    caption = type("caption", (HTMLTableCaptionElement,), {"name": "caption"})
    colgroup = type("colgroup", (HTMLTableColElement,), {"name": "colgroup"})
    tbody = type("tbody", (HTMLTableSectionElement,), {"name": "tbody"})
    thead = type("thead", (HTMLTableSectionElement,), {"name": "thead"})
    tfoot = type("tfoot", (HTMLTableSectionElement,), {"name": "tfoot"})
    th = type("th", (HTMLTableHeaderCellElement,), {"name": "th"})
    fieldset = type("fieldset", (HTMLFieldSetElement,), {"name": "fieldset"})
    legend = type("legend", (HTMLLegendElement,), {"name": "legend"})
    button = type("button", (HTMLButtonElement,), {"name": "button"})
    select = type("select", (HTMLSelectElement,), {"name": "select"})
    selectedcontent = type("selectedcontent", (HTMLSelectedContentElement,), {"name": "selectedcontent"})
    datalist = type("datalist", (HTMLDataListElement,), {"name": "datalist"})
    optgroup = type("optgroup", (HTMLOptGroupElement,), {"name": "optgroup"})
    option = type("option", (HTMLOptionElement,), {"name": "option"})
    textarea = type("textarea", (HTMLTextAreaElement,), {"name": "textarea"})
    output = type("output", (HTMLOutputElement,), {"name": "output"})
    progress = type("progress", (HTMLProgressElement,), {"name": "progress"})
    meter = type("meter", (HTMLMeterElement,), {"name": "meter"})
    details = type("details", (HTMLDetailsElement,), {"name": "details"})
    summary = type("summary", (HTMLSummaryElement,), {"name": "summary"})
    menu = type("menu", (HTMLMenuElement,), {"name": "menu"})
    menuitem = type("menuitem", (HTMLElement,), {"name": "menuitem"})  # dead but may be used
    font = type("font", (HTMLElement,), {"name": "font"})
    header = type("header", (HTMLElement,), {"name": "header"})
    footer = type("footer", (HTMLElement,), {"name": "footer"})
    map = type("map", (HTMLMapElement,), {"name": "map"})
    object = type("object", (HTMLObjectElement,), {"name": "object"})
    del_ = type("del_", (HTMLModElement,), {"name": "del"})
    mod = type("mod", (HTMLModElement,), {"name": "mod"})

    time = type("time", (HTMLTimeElement,), {"name": "time"})
    data = type("data", (HTMLDataElement,), {"name": "data"})

    base = type("base", (closed_tag, HTMLBaseElement), {"name": "base"})
    link = type("link", (closed_tag, HTMLLinkElement), {"name": "link"})
    meta = type("meta", (closed_tag, HTMLMetaElement), {"name": "meta"})
    hr = type("hr", (closed_tag, HTMLHRElement), {"name": "hr"})
    br = type(
        "br",
        (
            closed_tag,
            HTMLBRElement,
        ),
        {"name": "br"},
    )
    wbr = type("wbr", (closed_tag, HTMLElement), {"name": "wbr"})
    img = type("img", (closed_tag, HTMLImageElement), {"name": "img"})
    param = type("param", (closed_tag, HTMLParamElement), {"name": "param"})
    source = type("source", (closed_tag, HTMLSourceElement), {"name": "source"})
    track = type("track", (closed_tag, HTMLTrackElement), {"name": "track"})
    area = type("area", (closed_tag, HTMLAreaElement), {"name": "area"})
    col = type("col", (closed_tag, HTMLTableColElement), {"name": "col"})
    input = type("input", (closed_tag, HTMLInputElement), {"name": "input"})
    keygen = type("keygen", (closed_tag, HTMLKeygenElement), {"name": "keygen"})
    command = type("command", (closed_tag, Element), {"name": "command"})

    main = type("main", (HTMLElement,), {"name": "main"})
    slot = type("slot", (HTMLSlotElement,), {"name": "slot"})
    search = type("search", (HTMLElement,), {"name": "search"})

    # obsolete
    applet = type("applet", (HTMLUnknownElement,), {"name": "applet"})
    basefont = type("basefont", (HTMLBaseFontElement,), {"name": "basefont"})
    center = type("center", (HTMLElement,), {"name": "center"})
    dir = type("dir", (HTMLElement,), {"name": "dir"})
    embed = type("embed", (closed_tag, HTMLEmbedElement), {"name": "embed"})
    frame = type("frame", (HTMLElement,), {"name": "frame"})
    frameset = type("frameset", (HTMLFrameSetElement,), {"name": "frameset"})
    isindex = type("isindex", (HTMLIsIndexElement,), {"name": "isindex"})
    listing = type("listing", (HTMLElement,), {"name": "listing"})
    noframes = type("noframes", (HTMLElement,), {"name": "noframes"})
    plaintext = type("plaintext", (HTMLElement,), {"name": "plaintext"})
    strike = type("strike", (HTMLElement,), {"name": "strike"})
    xmp = type("xmp", (HTMLElement,), {"name": "xmp"})
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
    # fast path: an already-normalised, known tag name seen before
    cached = _HTML_TAG_CLASSES.get(name)
    if cached is not None:
        return cached(*args, **kwargs)

    # checks if already exists
    normalized_name = str(name).strip().lower()
    if not normalized_name:
        normalized_name = "custom_tag"
        name = "custom_tag"
    if normalized_name in _HTML_TAG_LOOKUP:
        tag_name = _TAG_ALIASES.get(normalized_name, normalized_name)
        tag_cls = globals()[tag_name]
        if name == normalized_name:
            _HTML_TAG_CLASSES[name] = tag_cls
        return tag_cls(*args, **kwargs)

    try:
        from domonic.window import window as domonic_window

        registry = getattr(domonic_window, "customElements", None)
        if registry is not None:
            registered = registry.get(name) or registry.get(normalized_name)
            if registered is not None:
                return registered(*args, **kwargs)
    except Exception:
        registry = None

    # https://html.spec.whatwg.org/#elements-in-the-dom: a valid custom element
    # name (it has a hyphen) is an HTMLElement awaiting upgrade; any other
    # unknown name is an HTMLUnknownElement.
    custom_tag = type("custom_tag", (HTMLElement if "-" in name else HTMLUnknownElement,), {"name": name})
    new_tag = custom_tag(*args, **kwargs)
    new_tag.name = name
    return new_tag
