"""
    domonic.html
    ====================================
    Generate HTML using python 3
"""
import copy
from domonic.javascript import URL
from domonic.dom import Node, Element, Document, DocumentType, Comment, Text

html_tags = [
            "figcaption", "blockquote", "textarea", "progress", "optgroup", "noscript", "fieldset", "datalist",
            "colgroup", "summary", "section", "details", "command", "caption", "article", "address", "submit",
            "strong", "source", "select", "script", "output", "option", "object", "legend", "keygen", "iframe",
            "hgroup", "header", "footer", "figure", "canvas", "button", "video", "track", "title", "title",
            "thead", "tfoot", "tbody", "table", "style", "small", "param", "meter", "label", "input", "embed",
            "audio", "aside", "time", "span", "span", "samp", "ruby", "meta", "meta", "menu", "mark", "link",
            "applet", "object", "basefont", "center", "dir", "embed", "font", "isindex", "listing", "menu",
            "plaintext", "pre", "strike", "xmp", "template", "picture",
            "html", "head", "form", "font", "code", "cite", "body", "base", "area", "abbr", "wbr", "var", "sup",
            "sub", "pre", "nav", "map", "main", "kbd", "ins", "img", "div", "dfn", "del", "col", "bdo", "bdi",
            "ul", "tr", "th", "td", "rt", "rp", "ol", "li", "hr", "hr", "h6", "h5", "h4", "h3", "h2", "h1",
            "em", "dt", "dl", "dd", "br", "u", "s", "q", "p", "i", "b", "a"]
            # big, small, blink, bold, strong, em, i, u, s, strike, tt, code, kbd, samp, var,

html_attributes = [
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
            "title", "translate", "type", "usemap", "value", "width", "wrap", "property", "integrity", "crossorigin",
            "nonce", "autocapitalize", "enterkeyhint", "inputmode", "is", "itemid", "itemprop", "itemref", "itemscope",
            "itemtype", "part", "slot", "spellcheck", "alink", "nowrap", "vlink", "vspace", "language", "clear",
            "hspace", "xmlns", "about", "allowtransparency",
            "datatype", "inlist", "prefix", "resource", "rev", "typeof", "vocab",  # rdfa
            "playsinline", "autopictureinpicture", "buffered", "controlslist", "disableremoteplayback"  # video
            ]


def render(inp, outp='', to=None):  # doctype='html5')
    """render

    Renders the input to string or to a file.

    Args:
        inp (obj): A domonic tag. For example div()
        outp (str): An optional output filename
        to (str): An optional output type. if 'pyml' is specified then pyml is returned instead of html.

    Returns:
        str: A HTML rendered string
    """
    if to == 'pyml':
        if outp != '':
            with open(outp, "w+") as f:
                f.write(inp.__pyml__())
        return inp.__pyml__()
    # else:
    if outp != '':
        with open(outp, "w+") as f:
            f.write(str(inp))
    return str(inp)


class TemplateError(IndexError):

    def __init__(self, error, message="Templating error: "):
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

    # def __str__(self):
    #     return self.message


class tag(object):
    """
    The class from which all html tags extend.
    """

    __slots__ = [
        "args",
        "kwargs",
        "__content",
        "____attributes__",  # ? seems to work. but not sure if its correct
    ]

    __context: list = None  # private. tags will append to last item in context on creation.

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        # self.name = 'tag'  # not set which means extended tags that don't use create_element will break

        # TODO - this may break a lot of existing implementations.
        # convert any strings to Text nodes
        # for i, arg in enumerate(self.args):
        #     if isinstance(arg, (str, int)):
        #         self.args = list(self.args)
        #         self.args[i] = Text(str(arg))
        #         self.args = tuple(self.args)

        try:
            self.content = ''.join([each.__str__() for each in args])
            self.__attributes__ = ''.join([''' %s="%s"''' % (key.split('_', 1)[1], value) for key, value in kwargs.items()])
        except IndexError as e:
            raise TemplateError(e)
        # except Exception as e:
            # print(e)

        # if a context is open, add this tag to the context
        if tag.__context is not None:
            tag.__context[len(tag.__context) - 1] += self

    @property
    def content(self):  # TODO - test
        return ''.join([each.__str__() for each in self.args])

    @content.setter
    def content(self, ignore):
        self.__content = ''.join([each.__str__() for each in self.args])
        return

    @property
    def __attributes__(self):
        def format_attr(key, value):
            if value is True:
                value = 'true'
            if value is False:
                value = 'false'
            key = key.split('_', 1)[1]
            # lets us have boolean attributes  # TODO - should be optional by a global config
            if key in ['async', 'checked', 'autofocus', 'disabled', 'formnovalidate', 'hidden', 'multiple',
                       'novalidate', 'readonly', 'required', 'selected']:
                if value == '' or value == key:
                    return ''' %s''' % key
            return ''' %s="%s"''' % (key, value)
        try:
            return ''.join([format_attr(key, value) for key, value in self.kwargs.items()])
        except IndexError as e:
            raise TemplateError(e)
        # except Exception as e:
            # print(e)

    @__attributes__.setter
    def __attributes__(self, ignore):
        try:
            self.__attributes = ''.join([''' %s="%s"''' % (key.split('_', 1)[1], value) for key, value in self.kwargs.items()])
        except IndexError as e:
            raise TemplateError(e)
        # except Exception as e:
            # print(e)

    def __str__(self):
        return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    def __mul__(self, other):
        """
        requires you to render yourself i.e.
        cells = cell()*10
        print(''.join([str(c) for c in cells]))
        """
        reproducer = []
        for i in range(other):
            reproducer.append(copy.deepcopy(self))
        return reproducer

    def __rmul__(self, other):
        """
        requires you to render yourself i.e.
        cells = cell()*10
        print(''.join([str(c) for c in cells]))
        """
        reproducer = []
        for i in range(other):
            reproducer.append(copy.deepcopy(self))
        return reproducer

    def __truediv__(self, other):
        """ use to render clones without having to parse commas yourself """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return ''.join(reproducer)

    def __rtruediv__(self, other):
        """ use to render clones without having to parse commas yourself """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return ''.join(reproducer)

    def __div__(self, other):
        """
        useful for prototyping as renders. to retain objects use multiply
        """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return ''.join(reproducer)

    def __rdiv__(self, other):
        """
        useful for prototyping as renders. to retain objects use multiply
        """
        reproducer = []
        for i in range(other):
            reproducer.append(str(self))
        return ''.join(reproducer)

    def __or__(self, other):
        """ return self unless other is something """
        if other is not False:
            return other
        return self

    def __iadd__(self, item):
        """ adds an item to the nodes of children """
        self.args = self.args + (item,)
        return self

    def __isub__(self, item):
        """ removes an item from the list of children """
        replace_args = list(self.args)
        replace_args.remove(item)
        self.args = tuple(replace_args)
        return self

    def __getitem__(self, index):  # TODO - move dunders to Node?
        # print('getting an item::', index, type(index))
        if isinstance(index, int):
            return self.args[index]
        # elif isinstance(index, str):
        #     if index.startswith('_'):
        #         return self.kwargs[index]
        #     else:
        #         return getattr(self, index)
        # super(Node, self).__getitem__(index)

        if isinstance(index, str):
            # call props on self
            # print('erk!')
            try:
                # return Node.__dict__[index]
                return getattr(self, index)
            except Exception as e:
                print(e)
                # return None
        # return super(Node, self).__getitem__(index)

    def __rshift__(self, item):
        try:
            for key in item.keys():
                self.kwargs[key] = item[key]
            return self
        except Exception as e:
            print(e)
            raise ValueError

    # def __add__(self, item):
    #     try:
    #         self.args = self.args + (item,)
    #         return self
    #     except Exception as e:
    #         print(e)
    #         raise ValueError

    # def __sub__(self, item):
    #     try:
    #         self.args = self.args - (item,)
    #         return self
    #     except Exception as e:
    #         print(e)
    #         raise ValueError

    # def render()

    def __getattr__(self, attr):
        """
        allows dot notation for reading attributes
        *credit to the peeps on discord/python for this one*
        """
        kwargs = super().__getattribute__('kwargs')
        # print("sup::", attr)
        # print("sup2::", kwargs)

        if attr in kwargs:
            return kwargs[attr]

        retry = "_" + attr
        if retry in kwargs:
            return kwargs[retry]

        retry = attr[1:len(attr)]
        if retry in kwargs:
            return kwargs[retry]

        try:
            return getattr(super(), attr)
        except AttributeError:
            raise AttributeError("This attribute or method does not appear to exist on this object:", attr)

        raise AttributeError

    def __pyml__(self):
        """ [returns a representation of the object as a pyml string] """
        from domonic.dom import Text
        params = ""
        for key, value in self.kwargs.items():
            params += f'{key}="{value}", '
        # TODO - will need to loop args and call __pyml__ on each one
        for arg in self.args:
            try:
                if isinstance(arg, Text):
                    params += str(arg) + ", "
                else:
                    params += f"{arg.__pyml__()}, "
            except Exception as e:
                params += str(arg) + ", "
        return f"{self.name}({params[:-2]})"
        # return f"{self.name}({params})"
        # return f"{self.name}({args}, {params})"
        # return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    # def __repr__(self):
    #     return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    # def __setitem__(self,key,value):
        # self.args[key] = value
        # print(self.args[key])

    def __enter__(self):
        if tag.__context is None:
            tag.__context = []
        tag.__context.append(self)
        return self

    def __exit__(self, type, value, traceback, *args, **kwargs):
        tag.__context.pop()
        if len(tag.__context) == 0:
            tag.__context = None
        return self

    # def __dir__(self):
    #     return self.__dict__.keys()

    # TODO - these are hard and wil need tests
    # def __setattr__(self, attr, value):
    # def __delattr__(self, attr):
    # def __next__(self):
    # def __iter__(self):

    def __format__(self, format_spec):
        # return super().__format__(format_spec)
        # get node depth by counting parents

        # TODO - this is a hack to get the depth of the node
        n = self
        depth = 0
        while n is not None:
            # print(type(n), type(n.parentNode))
            n = n.parentNode
            depth += 1

        depth -= 1

        # print(f"depth: {depth}")
        # dent = '    ' * depth
        dent = '\t' * depth

        # loop the children and call __format__ on each one
        # content = ""
        # for child in self.childNodes:
        #     content += child.__format__(format_spec)

        self._update_parents()

        content = ''.join([each.__format__(format_spec) for each in self.args])

        wrap = False
        if len(self.args) == 1:
            if not isinstance(self.args[0], Element):
                wrap = True

        dtype = ""
        if isinstance(self, Document):
            # dtype = "<!DOCTYPE html>"
            dtype = self.doctype

        # if self is a closed_tag, return the content
        if isinstance(self, closed_tag):
            return f"\n{dent}<{self.name}{self.__attributes__} />"

        size = len(str(content))
        if size < 150 and wrap:
            return f"\n{dent}<{self.name}{self.__attributes__}>{content}</{self.name}>"
        else:
            return f"{dtype}\n{dent}<{self.name}{self.__attributes__}>{content}\n{dent}</{self.name}>"

    # def __call__(self, *args, **kwargs):
    #     """
    #     allows for calling the object as a function
    #     """
    #     print('calling a tag')
    #     print(args)
    #     print(kwargs)
    #     print(self.name)
    #     print(self.args)
    #     print(self.kwargs)
    #     print(self.__attributes__)
    #     print(self.content)
    #     print(self.parentNode)
    #     print(self.childNodes)
    #     print(self.previousSibling)
    #     print(self.nextSibling)
    #     print(self.ownerDocument)
    #     print(self.nodeValue)
    #     print(self.nodeName)
    #     print(self.nodeType)


class closed_tag(tag):
    def __str__(self):
        return f"<{self.name}{self.__attributes__} />"


def tag_init(self, *args, **kwargs):
    tag.__init__(self, *args, **kwargs)
    Element.__init__(self, *args, **kwargs)


html = type('html', (tag, Document), {'name': 'html', '__init__': tag_init})
body = type('body', (tag, Element), {'name': 'body', '__init__': tag_init})
head = type('head', (tag, Element), {'name': 'head', '__init__': tag_init})
script = type('script', (tag, Element), {'name': 'script', '__init__': tag_init})
style = type('style', (tag, Element), {'name': 'style', '__init__': tag_init})
h1 = type('h1', (tag, Element), {'name': 'h1', '__init__': tag_init})
h2 = type('h2', (tag, Element), {'name': 'h2', '__init__': tag_init})
h3 = type('h3', (tag, Element), {'name': 'h3', '__init__': tag_init})
h4 = type('h4', (tag, Element), {'name': 'h4', '__init__': tag_init})
h5 = type('h5', (tag, Element), {'name': 'h5', '__init__': tag_init})
h6 = type('h6', (tag, Element), {'name': 'h6', '__init__': tag_init})
p = type('p', (tag, Element), {'name': 'p', '__init__': tag_init})
i = type('i', (tag, Element), {'name': 'i', '__init__': tag_init})
b = type('b', (tag, Element), {'name': 'b', '__init__': tag_init})

portal = type('portal', (tag, Element), {'name': 'portal', '__init__': tag_init})


def Atag(self, *args, **kwargs):
    # print('Atag: ', args, kwargs)
    tag.__init__(self, *args, **kwargs)
    Element.__init__(self, *args, **kwargs)

    # TODO - fix BUG. this stops having no href on a tags
    if kwargs.get('_href', None) is not None:
        URL.__init__(self, url=kwargs['_href'])
    else:
        URL.__init__(self, *args, **kwargs)


def __update__(self, *args, **kwargs):
    # print('__update__: ', args, kwargs)
    URL.__update__(self)

    # TODO - fix BUG. this stops having no href on a tags
    self.kwargs['_href'] = self.href
    tag.__init__(self, *self.args, **self.kwargs)


a = type('a', (tag, Element, URL), {'name': 'a', '__init__': Atag, '__update__': __update__})

ul = type('ul', (tag, Element), {'name': 'ul', '__init__': tag_init})
ol = type('ol', (tag, Element), {'name': 'ol', '__init__': tag_init})
li = type('li', (tag, Element), {'name': 'li', '__init__': tag_init})
div = type('div', (tag, Element), {'name': 'div', '__init__': tag_init})
strong = type('strong', (tag, Element), {'name': 'strong', '__init__': tag_init})
blockquote = type('blockquote', (tag, Element), {'name': 'blockquote', '__init__': tag_init})
table = type('table', (tag, Element), {'name': 'table', '__init__': tag_init})
tr = type('tr', (tag, Element), {'name': 'tr', '__init__': tag_init})
td = type('td', (tag, Element), {'name': 'td', '__init__': tag_init})
# form = type('form', (tag, Element), {'name': 'form', '__init__': tag_init})


class form(tag, Element):
    def __init__(self, *args, **kwargs):
        self.name = 'form'
        tag.__init__(self, *args, **kwargs)
        Element.__init__(self, *args, **kwargs)

    @property
    def elements(self):
        kids = []
        for child in self.children:
            if isinstance(child, (button, fieldset, input, object, output, select, textarea)):
                kids.append(child)
        return kids


label = type('label', (tag, Element), {'name': 'label', '__init__': tag_init})
# label.__doc__ = '''
#                 .. highlight:: python
#                 .. code-block:: python

#                     # used to label form elements. i.e.
#                     label(_for=None, _text=None, **kwargs)
#                     # <label for=""></label>
#                 '''

submit = type('submit', (tag, Element), {'name': 'submit', '__init__': tag_init})
title = type('title', (tag, Element), {'name': 'title', '__init__': tag_init})
noscript = type('noscript', (tag, Element), {'name': 'noscript', '__init__': tag_init})
section = type('section', (tag, Element), {'name': 'section', '__init__': tag_init})
nav = type('nav', (tag, Element), {'name': 'nav', '__init__': tag_init})
article = type('article', (tag, Element), {'name': 'article', '__init__': tag_init})
aside = type('aside', (tag, Element), {'name': 'aside', '__init__': tag_init})
hgroup = type('hgroup', (tag, Element), {'name': 'hgroup', '__init__': tag_init})
address = type('address', (tag, Element), {'name': 'address', '__init__': tag_init})
pre = type('pre', (tag, Element), {'name': 'pre', '__init__': tag_init})
dl = type('dl', (tag, Element), {'name': 'dl', '__init__': tag_init})
dt = type('dt', (tag, Element), {'name': 'dt', '__init__': tag_init})
dd = type('dd', (tag, Element), {'name': 'dd', '__init__': tag_init})
figure = type('figure', (tag, Element), {'name': 'figure', '__init__': tag_init})
figcaption = type('figcaption', (tag, Element), {'name': 'figcaption', '__init__': tag_init})
em = type('em', (tag, Element), {'name': 'em', '__init__': tag_init})
small = type('small', (tag, Element), {'name': 'small', '__init__': tag_init})
s = type('s', (tag, Element), {'name': 's', '__init__': tag_init})
cite = type('cite', (tag, Element), {'name': 'cite', '__init__': tag_init})
q = type('q', (tag, Element), {'name': 'q', '__init__': tag_init})
dfn = type('dfn', (tag, Element), {'name': 'dfn', '__init__': tag_init})
abbr = type('abbr', (tag, Element), {'name': 'abbr', '__init__': tag_init})
code = type('code', (tag, Element), {'name': 'code', '__init__': tag_init})
var = type('var', (tag, Element), {'name': 'var', '__init__': tag_init})
samp = type('samp', (tag, Element), {'name': 'samp', '__init__': tag_init})
kbd = type('kbd', (tag, Element), {'name': 'kbd', '__init__': tag_init})
sub = type('sub', (tag, Element), {'name': 'sub', '__init__': tag_init})
sup = type('sup', (tag, Element), {'name': 'sup', '__init__': tag_init})
u = type('u', (tag, Element), {'name': 'u', '__init__': tag_init})
mark = type('mark', (tag, Element), {'name': 'mark', '__init__': tag_init})
ruby = type('ruby', (tag, Element), {'name': 'ruby', '__init__': tag_init})
rt = type('rt', (tag, Element), {'name': 'rt', '__init__': tag_init})
rp = type('rp', (tag, Element), {'name': 'rp', '__init__': tag_init})
bdi = type('bdi', (tag, Element), {'name': 'bdi', '__init__': tag_init})
bdo = type('bdo', (tag, Element), {'name': 'bdo', '__init__': tag_init})
span = type('span', (tag, Element), {'name': 'span', '__init__': tag_init})
ins = type('ins', (tag, Element), {'name': 'ins', '__init__': tag_init})
iframe = type('iframe', (tag, Element), {'name': 'iframe', '__init__': tag_init})
video = type('video', (tag, Element), {'name': 'video', '__init__': tag_init})
audio = type('audio', (tag, Element), {'name': 'audio', '__init__': tag_init})
canvas = type('canvas', (tag, Element), {'name': 'canvas', '__init__': tag_init})
caption = type('caption', (tag, Element), {'name': 'caption', '__init__': tag_init})
colgroup = type('colgroup', (tag, Element), {'name': 'colgroup', '__init__': tag_init})
tbody = type('tbody', (tag, Element), {'name': 'tbody', '__init__': tag_init})
thead = type('thead', (tag, Element), {'name': 'thead', '__init__': tag_init})
tfoot = type('tfoot', (tag, Element), {'name': 'tfoot', '__init__': tag_init})
th = type('th', (tag, Element), {'name': 'th', '__init__': tag_init})
fieldset = type('fieldset', (tag, Element), {'name': 'fieldset', '__init__': tag_init})
legend = type('legend', (tag, Element), {'name': 'legend', '__init__': tag_init})
button = type('button', (tag, Element), {'name': 'button', '__init__': tag_init})
select = type('select', (tag, Element), {'name': 'select', '__init__': tag_init})
datalist = type('datalist', (tag, Element), {'name': 'datalist', '__init__': tag_init})
optgroup = type('optgroup', (tag, Element), {'name': 'optgroup', '__init__': tag_init})
option = type('option', (tag, Element), {'name': 'option', '__init__': tag_init})
textarea = type('textarea', (tag, Element), {'name': 'textarea', '__init__': tag_init})
output = type('output', (tag, Element), {'name': 'output', '__init__': tag_init})  # ?----------
progress = type('progress', (tag, Element), {'name': 'progress', '__init__': tag_init})
meter = type('meter', (tag, Element), {'name': 'meter', '__init__': tag_init})
details = type('details', (tag, Element), {'name': 'details', '__init__': tag_init})
summary = type('summary', (tag, Element), {'name': 'summary', '__init__': tag_init})
menu = type('menu', (tag, Element), {'name': 'menu', '__init__': tag_init})
font = type('font', (tag, Element), {'name': 'font', '__init__': tag_init})
header = type('header', (tag, Element), {'name': 'header', '__init__': tag_init})
footer = type('footer', (tag, Element), {'name': 'footer', '__init__': tag_init})
# map_ = type('map_', (tag,), {'name': 'map_', '__init__': tag_init})
# object_ = type('object_', (tag,), {'name': 'object_', '__init__': tag_init})
# del_ = type('del_', (tag,), {'name': 'del_', '__init__': tag_init})
# time_ = type('time_', (tag,), {'name': 'time_', '__init__': tag_init})

base = type('base', (closed_tag, Element), {'name': 'base', '__init__': tag_init})
link = type('link', (closed_tag, Element), {'name': 'link', '__init__': tag_init})
meta = type('meta', (closed_tag, Element), {'name': 'meta', '__init__': tag_init})
hr = type('hr', (closed_tag, Element), {'name': 'hr', '__init__': tag_init})
br = type('br', (closed_tag, Element), {'name': 'br', '__init__': tag_init})
wbr = type('wbr', (closed_tag, Element), {'name': 'wbr', '__init__': tag_init})
img = type('img', (closed_tag, Element), {'name': 'img', '__init__': tag_init})
embed = type('embed', (closed_tag, Element), {'name': 'embed', '__init__': tag_init})
param = type('param', (closed_tag, Element), {'name': 'param', '__init__': tag_init})
source = type('source', (closed_tag, Element), {'name': 'source', '__init__': tag_init})
track = type('track', (closed_tag, Element), {'name': 'track', '__init__': tag_init})
area = type('area', (closed_tag, Element), {'name': 'area', '__init__': tag_init})
col = type('col', (closed_tag, Element), {'name': 'col', '__init__': tag_init})
input = type('input', (closed_tag, Element), {'name': 'input', '__init__': tag_init})
keygen = type('keygen', (closed_tag, Element), {'name': 'keygen', '__init__': tag_init})
command = type('command', (closed_tag, Element), {'name': 'command', '__init__': tag_init})
main = type('command', (tag, Element), {'name': 'main', '__init__': tag_init})

# obsolete
applet = type('applet', (tag, Element), {'name': 'applet', '__init__': tag_init})
# object = type('object', (tag, Element), {'name': 'object', '__init__': tag_init})
basefont = type('basefont', (tag, Element), {'name': 'basefont', '__init__': tag_init})
center = type('center', (tag, Element), {'name': 'center', '__init__': tag_init})
# dir = type('dir', (tag, Element), {'name': 'dir', '__init__': tag_init})
embed = type('embed', (tag, Element), {'name': 'embed', '__init__': tag_init})
font = type('font', (tag, Element), {'name': 'font', '__init__': tag_init})
isindex = type('isindex', (tag, Element), {'name': 'isindex', '__init__': tag_init})
listing = type('listing', (tag, Element), {'name': 'listing', '__init__': tag_init})
menu = type('menu', (tag, Element), {'name': 'menu', '__init__': tag_init})
plaintext = type('plaintext', (tag, Element), {'name': 'plaintext', '__init__': tag_init})
pre = type('pre', (tag, Element), {'name': 'pre', '__init__': tag_init})
s = type('s', (tag, Element), {'name': 's', '__init__': tag_init})
u = type('u', (tag, Element), {'name': 'u', '__init__': tag_init})
strike = type('strike', (tag, Element), {'name': 'strike', '__init__': tag_init})
xmp = type('xmp', (tag, Element), {'name': 'xmp', '__init__': tag_init})

template = type('template', (tag, Element), {'name': 'template', '__init__': tag_init})
picture = type('picture', (tag, Element), {'name': 'picture', '__init__': tag_init})


# legacy.
doctype = DocumentType
comment = Comment


def create_element(name='custom_tag', *args, **kwargs):
    '''
    A method for creating custom tags

    tag name needs to be set due to custom tags with hyphens can't be classnames.
    i.e. hypenated tags <some-custom-tag></some-custom-tag>
    '''
    # import sys
    # current_module = sys.modules[__name__]
    # checks if already exists
    if name in html_tags:
        # cl = globals()[name]
        return globals()[name](*args, **kwargs)

    # print('creating custom element')
    custom_tag = type('custom_tag', (tag, Element), {'name': name, '__init__': tag_init})
    new_tag = custom_tag(*args, **kwargs)
    new_tag.name = name
    return new_tag
