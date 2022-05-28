# -*- coding: utf-8 -*-

import sys
sys.path.insert(0, '../..')

from domonic import *
from domonic.html import *


# 'loads' imports a pyml file and turns it into a program

# the example loads a template and passing params for rendering

# create some vars. you will see these referenced in the template file
brand = "MyBrand"
links = ['one', 'two', 'three']

# load a template and pass it some data
webpage = domonic.loads('templates/webpage.com.pyml', links=links, brand=brand)

render(webpage, 'webpage.html')



# 'load' is different to 'loads', it takes html strings and converts to a program

from domonic.dQuery import º

webpage = domonic.load('<html><head></head><body id="test"></body></html>')
º(webpage)
º('#test').append(div("Hello World"))
render(webpage, 'webpage2.html')



# useful plugin for formatting flat .pyml in vscode
# https://marketplace.visualstudio.com/items?itemName=mgesbert.indent-nested-dictionary