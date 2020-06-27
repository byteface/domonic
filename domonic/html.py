# -*- coding: utf-8 -*-
"""
    domonic.html
    ~~~~~
    
    Generate HTML using python 3
"""

from .dom import *
from .javascript import *

def render( inp, outp='' ):
    # print( inp )
    if outp is not '':
        with open(outp,"w+") as f:
            f.write(str(inp))
    return str(inp)


class tag():


    def __init__(self, *args, **kwargs):
        self.args = args
        self.kwargs = kwargs

        # TODO - dont render until called. so put these on a function or lamda?
        # self.name=""
        self.content = ''.join([each.__str__() for each in args])
        
        # try:
        self.attributes = ''.join([ ''' %s="%s"''' % (key.split('_',1)[1], value) for key, value in kwargs.items()])
        # except Exception as e:
            # print("ERROR!: MISSING UNDERSCORE ON AN ATTRIBUTE?", e )
            # self.attributes=''
        # print(self.attributes)


    def __str__(self):
        return f"<{self.name}{self.attributes}>{self.content}</{self.name}>"

    # def __repr__(self):
    #     return f"<{self.name}{self.attributes}>{self.content}</{self.name}>"

    # taken from my rank array on gist to use array accessors for reading content
    # def __repr__(self):
        # return repr([self.args])

    # def __getitem__(self,index):
        # return self.args[index]

    # def __setitem__(self,key,value):
        # self.args[key] = value
        # print( self.args[key] )

    # TODO - consider with?
    # def __enter__(self):
    # def __exit__(self ,type, value, traceback):


class closed_tag(tag):
    def __str__(self):
        return f"<{self.name}{self.attributes} />"

html = type('html', (tag, Document), {'name':'html'}) # document:dom.document
body = type('body', (tag, Element), {'name':'body'})
head = type('head', (tag, Element), {'name':'head'})
script = type('script', (tag, Element), {'name':'script'})
style = type('style', (tag, Element), {'name':'style'})
h1 = type('h1', (tag, Element), {'name':'h1'})
h2 = type('h2', (tag, Element), {'name':'h2'})
h3 = type('h3', (tag, Element), {'name':'h3'})
h4 = type('h4', (tag, Element), {'name':'h4'})
h5 = type('h5', (tag, Element), {'name':'h5'})
h6 = type('h6', (tag, Element), {'name':'h6'})
p = type('p', (tag, Element), {'name':'p'})
i = type('i', (tag, Element), {'name':'i'})
b = type('b', (tag, Element), {'name':'b'})

def Atag(self,*args,**kwargs):
    # print("are you threatening me!!")
    # print(args)
    # print(kwargs)
    tag.__init__(self,*args,**kwargs)
    # Element.__init__(self, url=kwargs['_href'])
    URL.__init__(self, url=kwargs['_href'])


def __update__(self):
    # print('THIS ran')
    # print(self.href)
    URL.__update__(self)
    # print('>>>',self.href)
    tag.__init__(self,_href=self.href)
    


a = type('a', (tag, Element, URL), {'name':'a', '__init__':Atag, '__update__':__update__})

ul = type('ul', (tag, Element), {'name':'ul'})
ol = type('ol', (tag, Element), {'name':'ol'})
li = type('li', (tag, Element), {'name':'li'})
hr = type('hr', (tag, Element), {'name':'hr'})
div = type('div', (tag, Element), {'name':'div'})
span = type('span', (tag, Element), {'name':'span'})
strong = type('strong', (tag, Element), {'name':'strong'})
blockquote = type('blockquote', (tag, Element), {'name':'blockquote'})
table = type('table', (tag, Element), {'name':'table'})
tr = type('tr', (tag, Element), {'name':'tr'})
td = type('td', (tag, Element), {'name':'td'})
title = type('title', (tag, Element), {'name':'title'})
meta = type('meta', (tag, Element), {'name':'meta'})
form = type('form', (tag, Element), {'name':'form'})
label = type('label', (tag, Element), {'name':'label'})
submit = type('submit', (tag, Element), {'name':'submit'})
title = type('title', (tag, Element), {'name':'title'})
noscript = type('noscript', (tag, Element), {'name':'noscript'})
section = type('section', (tag, Element), {'name':'section'})
nav = type('nav', (tag, Element), {'name':'nav'})
article = type('article', (tag, Element), {'name':'article'})
aside = type('aside', (tag, Element), {'name':'aside'})
hgroup = type('hgroup', (tag, Element), {'name':'hgroup'})
address = type('address', (tag, Element), {'name':'address'})
pre = type('pre', (tag, Element), {'name':'pre'})
dl = type('dl', (tag, Element), {'name':'dl'})
dt = type('dt', (tag, Element), {'name':'dt'})
dd = type('dd', (tag, Element), {'name':'dd'})
figure = type('figure', (tag, Element), {'name':'figure'})
figcaption = type('figcaption', (tag, Element), {'name':'figcaption'})
em = type('em', (tag, Element), {'name':'em'})
small = type('small', (tag, Element), {'name':'small'})
s = type('s', (tag, Element), {'name':'s'})
cite = type('cite', (tag, Element), {'name':'cite'})
q = type('q', (tag, Element), {'name':'q'})
dfn = type('dfn', (tag, Element), {'name':'dfn'})
abbr = type('abbr', (tag, Element), {'name':'abbr'})
code = type('code', (tag, Element), {'name':'code'})
var = type('var', (tag, Element), {'name':'var'})
samp = type('samp', (tag, Element), {'name':'samp'})
kbd = type('kbd', (tag, Element), {'name':'kbd'})
sub = type('sub', (tag, Element), {'name':'sub'})
sup = type('sup', (tag, Element), {'name':'sup'})
u = type('u', (tag, Element), {'name':'u'})
mark = type('mark', (tag, Element), {'name':'mark'})
ruby = type('ruby', (tag, Element), {'name':'ruby'})
rt = type('rt', (tag, Element), {'name':'rt'})
rp = type('rp', (tag, Element), {'name':'rp'})
bdi = type('bdi', (tag, Element), {'name':'bdi'})
bdo = type('bdo', (tag, Element), {'name':'bdo'})
span = type('span', (tag, Element), {'name':'span'})
ins = type('ins', (tag, Element), {'name':'ins'})
iframe = type('iframe', (tag, Element), {'name':'iframe'})
video = type('video', (tag, Element), {'name':'video'})
audio = type('audio', (tag, Element), {'name':'audio'})
canvas = type('canvas', (tag, Element), {'name':'canvas'})
caption = type('caption', (tag, Element), {'name':'caption'})
colgroup = type('colgroup', (tag, Element), {'name':'colgroup'})
tbody = type('tbody', (tag, Element), {'name':'tbody'})
thead = type('thead', (tag, Element), {'name':'thead'})
tfoot = type('tfoot', (tag, Element), {'name':'tfoot'})
th = type('th', (tag, Element), {'name':'th'})
fieldset = type('fieldset', (tag, Element), {'name':'fieldset'})
legend = type('legend', (tag, Element), {'name':'legend'})
button = type('button', (tag, Element), {'name':'button'})
select = type('select', (tag, Element), {'name':'select'})
datalist = type('datalist', (tag, Element), {'name':'datalist'})
optgroup = type('optgroup', (tag, Element), {'name':'optgroup'})
option = type('option', (tag, Element), {'name':'option'})
textarea = type('textarea', (tag, Element), {'name':'textarea'})
output = type('output', (tag, Element), {'name':'output'})#?----------
progress = type('progress', (tag, Element), {'name':'progress'})
meter = type('meter', (tag, Element), {'name':'meter'})
details = type('details', (tag, Element), {'name':'details'})
summary = type('summary', (tag, Element), {'name':'summary'})
menu = type('menu', (tag, Element), {'name':'menu'})
font = type('font', (tag, Element), {'name':'font'})
header = type('header', (tag, Element), {'name':'header'})
footer = type('footer', (tag, Element), {'name':'footer'})
# map_ = type('map_', (tag,), {'name':'map_'})
# object_ = type('object_', (tag,), {'name':'object_'})
# del_ = type('del_', (tag,), {'name':'del_'})
# time_ = type('time_', (tag,), {'name':'time_'})

base = type('base', (closed_tag, Element), {'name':'base'})
link = type('link', (closed_tag, Element), {'name':'link'})
meta = type('meta', (closed_tag, Element), {'name':'meta'})
hr = type('hr', (closed_tag, Element), {'name':'hr'})
br = type('br', (closed_tag, Element), {'name':'br'})
wbr = type('wbr', (closed_tag, Element), {'name':'wbr'})
img = type('img', (closed_tag, Element), {'name':'img'})
embed = type('embed', (closed_tag, Element), {'name':'embed'})
param = type('param', (closed_tag, Element), {'name':'param'})
source = type('source', (closed_tag, Element), {'name':'source'})
track = type('track', (closed_tag, Element), {'name':'track'})
area = type('area', (closed_tag, Element), {'name':'area'})
col = type('col', (closed_tag, Element), {'name':'col'})
input = type('input', (closed_tag, Element), {'name':'input'})
keygen = type('keygen', (closed_tag, Element), {'name':'keygen'})
command = type('command', (closed_tag, Element), {'name':'command'})

main = type('command', (tag, Element), {'name':'main'}) # TODO - y was this missing?

# TODO - this can't be added at the mo. need to push it
class doctype():
    def __str__(self):
        return f"<!DOCTYPE html>"

class comment():
    def __init__(self,content=""):
        self.content = content
    def __str__(self):
        return f"<!-- {self.content} -->"


# output = render( 
#     html(
#         head(
#             style(),script(),
#         ),
#         body(
#             div("hello world"),
#             a("this is a link", _href="http://www.somesite.com", _style="font-size:10px;"),
#             ol(''.join([f'{li()}' for thing in range(5)])),
#             h1("test", _class="test"),
#         )
#     )
# )
