import sys
sys.path.insert(0, '..')

import os
from sanic import Sanic
from sanic import response
from domonic.html import *
from domonic.CDN import *

# from app import *
# from app.components import *

app = Sanic(name='Long poll grid test')
app.static('/assets', './assets')

MARGIN = 1
PADDING = 2

# create a template
cell = lambda x = None: div( _class=x if x else '', _style=f"display:inline;margin:{MARGIN}px;padding:{PADDING}px;").html(
    			# button(":)", _style="background-color:white;color:black;")
			)

row = lambda *x : div(*x, _class="row")

# TODO - random color gen is required.
# TODO - random face gen is required.

# world grid
_grid = div(
# row( cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d') ),
# row( cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d') ),
# row( cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d') ),
# row( cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d') ),
# row( cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d') ),
# row( cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d'),cell('d') ),
row( cell('d')/100 )/100,
row( cell('d')/100 )/100,
# _style="max-width:100px;",
_class="container-fluid"
)
# print( str(cell()*10) )
# cells = cell()*10
# print(''.join([str(c) for c in cells]))


_materials = style("""
/* default */
.d{
	background-color: black;
}
.g{
	background-color: green;
}
.r{
	background-color: red;
}
.b{
	background-color: blue;
}
.y{
	background-color: yellow;
}
.p{
	background-color: purple;
}

""")

_scripts = script("""
//alert('yo world!')
""")

class World:

	def __init__(self, request, *args, **kwargs):
		pass

	def __str__(self):
		return str(
			div(
			_materials,
			_scripts,
			_grid
			)
			)


@app.route('/')
@app.route('/world')
async def world(request):
	# check the diffs against our diff map
    return response.html(str(html(
    		head(),
    		body(
    		link(_rel="stylesheet", _type="text/css", _href=CDN_CSS.BOOTSTRAP_4),
    		str(World(request))
    		))))


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True)
