"""
    domonic.html
    ====================================
    Generate HTML using python 3
"""
import copy
from domonic.javascript import URL
from domonic.dom import Element, Document


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
            "title", "translate", "type", "usemap", "value", "width", "wrap", "property", "integrity", "crossorigin", "nonce",
            "autocapitalize", "enterkeyhint", "inputmode", "is", "itemid", "itemprop", "itemref", "itemscope", "itemtype", "part",
            "slot", "spellcheck", "alink", "nowrap", "vlink", "vspace", "language", "clear", "hspace", "xmlns", "about", "allowtransparency",
            "datatype", "inlist", "prefix", "resource", "rev", "typeof", "vocab",  # rdfa
            "playsinline", "autopictureinpicture", "buffered", "controlslist", "disableremoteplayback"  # video
            ]


def render(inp, outp=''):
    """render

    Renders the input to string or to a file.

    Args:
        inp (obj): A domonic tag. For example div()
        outp (str): An optional output filename

    Returns:
        str: A HTML rendered string
    """
    if outp != '':
        with open(outp, "w+") as f:
            f.write(str(inp))
    return str(inp)


class TemplateError(IndexError):
    def __init__(self, error, message="Templating error: "):
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

    # TODO - slots?.

    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs
        # self.name = 'tag'  # not set which means extended tags that don't use create_element will break
        try:
            self.content = ''.join([each.__str__() for each in args])
            self.attributes = ''.join([''' %s="%s"''' % (key.split('_', 1)[1], value) for key, value in kwargs.items()])
        except IndexError as e:
            raise TemplateError(e)
        # except Exception as e:
            # print(e)

    @property
    def content(self):  # TODO - test
        return ''.join([each.__str__() for each in self.args])

    @content.setter
    def content(self, ignore):
        self.__content = ''.join([each.__str__() for each in self.args])
        return

    @property
    def attributes(self):
        try:
            return ''.join([''' %s="%s"''' % (key.split('_', 1)[1], value) for key, value in self.kwargs.items()])
        except IndexError as e:
            raise TemplateError(e)
        # except Exception as e:
            # print(e)

    @attributes.setter
    def attributes(self, ignore):
        try:
            self.__attributes = ''.join([''' %s="%s"''' % (key.split('_', 1)[1], value) for key, value in self.kwargs.items()])
        except IndexError as e:
            raise TemplateError(e)
        # except Exception as e:
            # print(e)

    def __str__(self):
        return f"<{self.name}{self.attributes}>{self.content}</{self.name}>"

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

    def __getitem__(self, index):
        return self.args[index]

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

        # raise AttributeError("This attribute or method does not appear to exist on this object:", attr)
        raise AttributeError

    # def __repr__(self):
    #     return f"<{self.name}{self.attributes}>{self.content}</{self.name}>"

    # def __setitem__(self,key,value):
        # self.args[key] = value
        # print(self.args[key])

    # def __enter__(self):
    # def __exit__(self ,type, value, traceback):
    # def __dir__/__getattr__/__getattribute)) - .... dot notation for attributes


class closed_tag(tag):
    def __str__(self):
        return f"<{self.name}{self.attributes} />"


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
hr = type('hr', (tag, Element), {'name': 'hr', '__init__': tag_init})
div = type('div', (tag, Element), {'name': 'div', '__init__': tag_init})
span = type('span', (tag, Element), {'name': 'span', '__init__': tag_init})
strong = type('strong', (tag, Element), {'name': 'strong', '__init__': tag_init})
blockquote = type('blockquote', (tag, Element), {'name': 'blockquote', '__init__': tag_init})
table = type('table', (tag, Element), {'name': 'table', '__init__': tag_init})
tr = type('tr', (tag, Element), {'name': 'tr', '__init__': tag_init})
td = type('td', (tag, Element), {'name': 'td', '__init__': tag_init})
title = type('title', (tag, Element), {'name': 'title', '__init__': tag_init})
meta = type('meta', (tag, Element), {'name': 'meta', '__init__': tag_init})


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

main = type('command', (tag, Element), {'name': 'main', '__init__': tag_init})  # TODO - y was this missing?


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


class doctype():
    """doctype

    Returns:
        str: <!DOCTYPE html>
    """
    def __str__(self):
        return "<!DOCTYPE html>"

    def __repr__(self):
        return "<!DOCTYPE html>"

    def __call__(self, *args, **kwargs):
        return self.__str__()


class comment():
    """comment

    Args:
        content (str): Message to be rendered inside the comment tag

    Returns:
        str: "<!-- {self.content} -->
    """
    def __init__(self, content=""):
        self.content = content

    def __str__(self):
        return f"<!-- {self.content} -->"

    def __repr__(self):
        return f"<!-- {self.content} -->"

    def __call__(self, *args, **kwargs):
        return self.__str__()


def create_element(name='custom_tag', *args, **kwargs):
    '''
    If you must, a method for creating custom tags
    tag name needs to be set due to custom tags with hyphens can't be classnames.
    i.e. hypenated tags <some-custom-tag></some-custom-tag>
    '''
    # TODO - check for existing elements first and return if available

    custom_tag = type('custom_tag', (tag, Element), {'name': name, '__init__': tag_init})
    # t = tag(*args, **kwargs)  #  TODO - this is not an element.
    t = custom_tag(*args, **kwargs)
    t.name = name
    return t
    # new_tag = type('custom_tag', (tag, Element), {'name': name, '__init__': tag_init})
    # return new_tag
