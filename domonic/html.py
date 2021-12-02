"""
    domonic.html
    ====================================
    Generate HTML using python 3
"""
import copy
from domonic.javascript import URL
from domonic.dom import Node, Element, Document, DocumentType, Comment, Text
from domonic.dom import (HTMLDialogElement)


# TODO - this is for now until we refactor all tag class onto node needs calling in 3 places so making a util.
# it basically allows non-underscore kwargs to be passed to the tag by making them underscored.
def _fixkwargs(kwargs):
    # TODO - this causes a lot of cycles on super calling. so will refactor all tag directly to node
    # print('LETS DO IT!', self.kwargs)
    # make sure all kwargs begin with a _
    new_kwargs = {}
    for k, v in kwargs.items():
        if k[0] != "_":
            # print("WARNING: kwarg '{}' should begin with an underscore".format(k))
            new_kwargs[f"_{k}"] = v
        else:
            new_kwargs[k] = v
    # kwargs = new_kwargs
    # print('kwargs is', self.kwargs)
    return new_kwargs


html_tags = [
            "figcaption", "blockquote", "textarea", "progress", "optgroup", "noscript", "fieldset", "datalist",
            "colgroup", "summary", "section", "details", "command", "caption", "article", "address", "submit",
            "strong", "source", "select", "script", "output", "option", "legend", "keygen", "iframe",
            "hgroup", "header", "footer", "figure", "canvas", "button", "video", "track", "title",
            "thead", "tfoot", "tbody", "table", "style", "small", "param", "meter", "label", "input",
            "audio", "aside", "time", "span", "samp", "ruby", "meta", "menu", "mark", "link",
            "applet", "object", "basefont", "center", "dir", "embed", "isindex", "listing", "menuitem",
            "plaintext", "pre", "strike", "xmp", "template", "picture", "dialog"
            "html", "head", "form", "font", "code", "cite", "body", "base", "area", "abbr", "wbr", "var", "sup",
            "sub", "nav", "map", "main", "kbd", "ins", "img", "div", "dfn", "del", "col", "bdo", "bdi",
            "ul", "tr", "th", "td", "rt", "rp", "ol", "li", "hr", "h6", "h5", "h4", "h3", "h2", "h1",
            "em", "dt", "dl", "dd", "br", "u", "s", "q", "p", "i", "b", "a"]
            # big, blink, bold, tt, var,

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


class tag(Node):
    """
    The class from which all html tags extend.
    """

    # __slots__ = [
    #     "args",
    #     "kwargs",
    #     "__content",
    #     "____attributes__",  # ? seems to work. but not sure if its correct
    # ]

    __context: list = None  # private. tags will append to last item in context on creation.

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        # if a context is open, add this tag to the context
        if tag.__context is not None:
            tag.__context[len(tag.__context) - 1] += self
        super().__init__(*args, **kwargs)


    @property
    def content(self):  # TODO - test
        # return ''.join([each.__str__() for each in self.args])
        # if any child are lists by mistake, loop and call __str__ on each first
        cnt = self.args
        for i, arg in enumerate(cnt):
            if isinstance(arg, list):
                cnt = list(cnt)
                cnt[i] = ''.join([each.__str__() for each in arg])
                cnt = tuple(cnt)
        return ''.join([each.__str__() for each in cnt])

    @content.setter
    def content(self, ignore):
        self.__content = ''.join([each.__str__() for each in self.args])
        return

    @property
    def __attributes__(self):
        # print('kwargs is22', self.kwargs)
        def format_attr(key, value):
            if value is True:
                value = 'true'
            if value is False:
                value = 'false'
            key = key.split('_', 1)[1]
            # lets us have boolean attributes  # TODO - should be optional by a global config
            if key in ['async', 'checked', 'autofocus', 'disabled', 'formnovalidate', 'hidden', 'multiple',
                       'novalidate', 'readonly', 'required', 'selected', "open", "contenteditable"]:
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
        """ adds an item to the nodes of children. can also pass a list and it will unpack them """

        if isinstance(item, (list, tuple)):
            for i in item:
                self.args = self.args + (i,)
            return self

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
        # from domonic.dom import Text
        params = ""
        for key, value in self.kwargs.items():
            if '-' in key:
                params += f'**\u007b"{key}":{value}\u007d,'
            else:
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
        # TODO - if self is document do dentage
        return f"{self.name}({params[:-2]})"
        # return f"{self.name}({params})"
        # return f"{self.name}({args}, {params})"
        # return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    # def __repr__(self):
    #     return f"<{self.name}{self.__attributes__}>{self.content}</{self.name}>"

    def __setitem__(self, key, value):
        # self.args[key] = value
        # print(self.args[key])
        try:
            self.kwargs[key] = value
            return self
        except Exception as e:
            print(e)
            raise ValueError

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


'''
def tag_init(self, *args, **kwargs):

    # kwargs = _fixkwargs(kwargs)
    # print('kwargs is', self.kwargs)

    new_kwargs = {}
    for k, v in kwargs.items():
        if k[0] != "_":
            # print("WARNING: kwarg '{}' should begin with an underscore".format(k))
            new_kwargs[f"_{k}"] = v
        else:
            new_kwargs[k] = v
    kwargs = new_kwargs

    tag.__init__(self, *args, **kwargs)
    Element.__init__(self, *args, **kwargs)
'''

# class HTMLElement:
#     @property
#     def lang(self):
#         return "unknown"


html = type('html', (tag, Document), {'name': 'html'})
body = type('body', (tag, Element), {'name': 'body'})
head = type('head', (tag, Element), {'name': 'head'})
script = type('script', (tag, Element), {'name': 'script'})
style = type('style', (tag, Element), {'name': 'style'})
h1 = type('h1', (tag, Element), {'name': 'h1'})
h2 = type('h2', (tag, Element), {'name': 'h2'})
h3 = type('h3', (tag, Element), {'name': 'h3'})
h4 = type('h4', (tag, Element), {'name': 'h4'})
h5 = type('h5', (tag, Element), {'name': 'h5'})
h6 = type('h6', (tag, Element), {'name': 'h6'})
p = type('p', (tag, Element), {'name': 'p'})
i = type('i', (tag, Element), {'name': 'i'})
b = type('b', (tag, Element), {'name': 'b'})

portal = type('portal', (tag, Element), {'name': 'portal'})


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
    tag.__init__(self, *args, **kwargs)


a = type('a', (tag, Element, URL), {'name': 'a', '__init__': Atag}) #, '__update__': __update__})

ul = type('ul', (tag, Element), {'name': 'ul'})
ol = type('ol', (tag, Element), {'name': 'ol'})
li = type('li', (tag, Element), {'name': 'li'})
div = type('div', (tag, Element), {'name': 'div'})
strong = type('strong', (tag, Element), {'name': 'strong'})
blockquote = type('blockquote', (tag, Element), {'name': 'blockquote'})
table = type('table', (tag, Element), {'name': 'table'})
tr = type('tr', (tag, Element), {'name': 'tr'})
td = type('td', (tag, Element), {'name': 'td'})
# form = type('form', (tag, Element), {'name': 'form'})


class form(tag, Element):
    def __init__(self, *args, **kwargs):

        # kwargs = _fixkwargs(kwargs)
        # print('kwargs is', self.kwargs)

        new_kwargs = {}
        for k, v in kwargs.items():
            if k[0] != "_":
                # print("WARNING: kwarg '{}' should begin with an underscore".format(k))
                new_kwargs[f"_{k}"] = v
            else:
                new_kwargs[k] = v
        kwargs = new_kwargs

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


label = type('label', (tag, Element), {'name': 'label'})
# label.__doc__ = '''
#                 .. highlight:: python
#                 .. code-block:: python

#                     # used to label form elements. i.e.
#                     label(_for=None, _text=None, **kwargs)
#                     # <label for=""></label>
#                 '''

submit = type('submit', (tag, Element), {'name': 'submit'})
title = type('title', (tag, Element), {'name': 'title'})
noscript = type('noscript', (tag, Element), {'name': 'noscript'})
section = type('section', (tag, Element), {'name': 'section'})
nav = type('nav', (tag, Element), {'name': 'nav'})
article = type('article', (tag, Element), {'name': 'article'})
aside = type('aside', (tag, Element), {'name': 'aside'})
hgroup = type('hgroup', (tag, Element), {'name': 'hgroup'})
address = type('address', (tag, Element), {'name': 'address'})
pre = type('pre', (tag, Element), {'name': 'pre'})
dl = type('dl', (tag, Element), {'name': 'dl'})
dt = type('dt', (tag, Element), {'name': 'dt'})
dd = type('dd', (tag, Element), {'name': 'dd'})
figure = type('figure', (tag, Element), {'name': 'figure'})
figcaption = type('figcaption', (tag, Element), {'name': 'figcaption'})
em = type('em', (tag, Element), {'name': 'em'})
small = type('small', (tag, Element), {'name': 'small'})
s = type('s', (tag, Element), {'name': 's'})
cite = type('cite', (tag, Element), {'name': 'cite'})
q = type('q', (tag, Element), {'name': 'q'})
dfn = type('dfn', (tag, Element), {'name': 'dfn'})
abbr = type('abbr', (tag, Element), {'name': 'abbr'})
code = type('code', (tag, Element), {'name': 'code'})
var = type('var', (tag, Element), {'name': 'var'})
samp = type('samp', (tag, Element), {'name': 'samp'})
kbd = type('kbd', (tag, Element), {'name': 'kbd'})
sub = type('sub', (tag, Element), {'name': 'sub'})
sup = type('sup', (tag, Element), {'name': 'sup'})
u = type('u', (tag, Element), {'name': 'u'})
mark = type('mark', (tag, Element), {'name': 'mark'})
ruby = type('ruby', (tag, Element), {'name': 'ruby'})
rt = type('rt', (tag, Element), {'name': 'rt'})
rp = type('rp', (tag, Element), {'name': 'rp'})
bdi = type('bdi', (tag, Element), {'name': 'bdi'})
bdo = type('bdo', (tag, Element), {'name': 'bdo'})
span = type('span', (tag, Element), {'name': 'span'})
ins = type('ins', (tag, Element), {'name': 'ins'})
iframe = type('iframe', (tag, Element), {'name': 'iframe'})
video = type('video', (tag, Element), {'name': 'video'})
audio = type('audio', (tag, Element), {'name': 'audio'})
canvas = type('canvas', (tag, Element), {'name': 'canvas'})
caption = type('caption', (tag, Element), {'name': 'caption'})
colgroup = type('colgroup', (tag, Element), {'name': 'colgroup'})
tbody = type('tbody', (tag, Element), {'name': 'tbody'})
thead = type('thead', (tag, Element), {'name': 'thead'})
tfoot = type('tfoot', (tag, Element), {'name': 'tfoot'})
th = type('th', (tag, Element), {'name': 'th'})
fieldset = type('fieldset', (tag, Element), {'name': 'fieldset'})
legend = type('legend', (tag, Element), {'name': 'legend'})
button = type('button', (tag, Element), {'name': 'button'})
select = type('select', (tag, Element), {'name': 'select'})
datalist = type('datalist', (tag, Element), {'name': 'datalist'})
optgroup = type('optgroup', (tag, Element), {'name': 'optgroup'})
option = type('option', (tag, Element), {'name': 'option'})
textarea = type('textarea', (tag, Element), {'name': 'textarea'})
output = type('output', (tag, Element), {'name': 'output'})  # ?----------
progress = type('progress', (tag, Element), {'name': 'progress'})
meter = type('meter', (tag, Element), {'name': 'meter'})
details = type('details', (tag, Element), {'name': 'details'})
summary = type('summary', (tag, Element), {'name': 'summary'})
menu = type('menu', (tag, Element), {'name': 'menu'})
menuitem = type('menuitem', (tag, Element), {'name': 'menuitem'})  # dead but may be used
font = type('font', (tag, Element), {'name': 'font'})
header = type('header', (tag, Element), {'name': 'header'})
footer = type('footer', (tag, Element), {'name': 'footer'})
# map_ = type('map_', (tag,), {'name': 'map_'})
# object_ = type('object_', (tag,), {'name': 'object_'})
# del_ = type('del_', (tag,), {'name': 'del_'})
# time_ = type('time_', (tag,), {'name': 'time_'})

base = type('base', (closed_tag, Element), {'name': 'base'})
link = type('link', (closed_tag, Element), {'name': 'link'})
meta = type('meta', (closed_tag, Element), {'name': 'meta'})
hr = type('hr', (closed_tag, Element), {'name': 'hr'})
br = type('br', (closed_tag, Element), {'name': 'br'})
wbr = type('wbr', (closed_tag, Element), {'name': 'wbr'})
img = type('img', (closed_tag, Element), {'name': 'img'})
param = type('param', (closed_tag, Element), {'name': 'param'})
source = type('source', (closed_tag, Element), {'name': 'source'})
track = type('track', (closed_tag, Element), {'name': 'track'})
area = type('area', (closed_tag, Element), {'name': 'area'})
col = type('col', (closed_tag, Element), {'name': 'col'})
input = type('input', (closed_tag, Element), {'name': 'input'})
keygen = type('keygen', (closed_tag, Element), {'name': 'keygen'})
command = type('command', (closed_tag, Element), {'name': 'command'})
main = type('command', (tag, Element), {'name': 'main'})

# obsolete
applet = type('applet', (tag, Element), {'name': 'applet'})
# object = type('object', (tag, Element), {'name': 'object'})
basefont = type('basefont', (tag, Element), {'name': 'basefont'})
center = type('center', (tag, Element), {'name': 'center'})
# dir = type('dir', (tag, Element), {'name': 'dir'})
embed = type('embed', (tag, Element), {'name': 'embed'})
isindex = type('isindex', (tag, Element), {'name': 'isindex'})
listing = type('listing', (tag, Element), {'name': 'listing'})
plaintext = type('plaintext', (tag, Element), {'name': 'plaintext'})
s = type('s', (tag, Element), {'name': 's'})
u = type('u', (tag, Element), {'name': 'u'})
strike = type('strike', (tag, Element), {'name': 'strike'})
xmp = type('xmp', (tag, Element), {'name': 'xmp'})

template = type('template', (tag, Element), {'name': 'template'})
picture = type('picture', (tag, Element), {'name': 'picture'})
dialog = type('dialog', (tag, HTMLDialogElement), {'name': 'dialog'})
# dialog = HTMLDialogElement  # TODO - might get rid of tag and put all its methods on Node directly

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
    custom_tag = type('custom_tag', (tag, Element), {'name': name})
    new_tag = custom_tag(*args, **kwargs)
    new_tag.name = name
    return new_tag
