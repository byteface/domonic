JSON
=============

.. meta::
   :description: JSON helpers for Python HTML tables, CSV conversion, decorators, validation, flattening, and domonic data workflows.
   :keywords: Python JSON, JSON to HTML table, CSV to JSON, JSON decorator, HTML table from JSON, data utilities

domonic includes practical helpers for moving between Python objects, JSON, CSV, and simple HTML tables.

Decorate any function that returns Python objects to return JSON instead:

.. code-block :: python

	from domonic.JSON import *

	@return_json
	def somefunc():
	    myObj = {"hi":[1,2,3]}
	    return myObj

	print( somefunc() )
	# {"hi": [1, 2, 3]}
	print( is_json(somefunc()) )
	# True


Convert JSON arrays into HTML tables:

.. code-block :: python

	import domonic.JSON as JSON

	# A flat JSON array of dicts, for example:
	# [{"id": "01", "name": "some item"}, {"id": "02", "name": "some other item"}]
	json_data = [{"id": "01", "name": "some item"}, {"id": "02", "name": "some other item"}]
	JSON.stringify(json_data, 'somefile.json')  # write it out first, for this example

	loaded = JSON.parse_file('somefile.json')
	mytable = JSON.tablify(loaded)
	print(mytable)
	# <table><tr><th>id</th><th>name</th></tr><tr><td>01</td><td>some item</td></tr><tr><td>02</td><td>some other item</td></tr></table>


Convert JSON arrays into CSV files:

.. code-block :: python

	import domonic.JSON as JSON

	json_data = JSON.parse_file('somefile.json')
	JSON.csvify(json_data, 'data.csv')

	print(open('data.csv').read())
	# id,name
	# 01,some item
	# 02,some other item


Convert CSV files to JSON:

.. code-block :: python

	import domonic.JSON as JSON

	json_data = JSON.csv2json("data.csv")
	print(json_data)
	# [{"id": "01", "name": "some item"}, {"id": "02", "name": "some other item"}]


The module also includes helpers for validation, flattening, and turning table nodes back into row dictionaries.

API Response Helpers
--------------------

.. code-block :: python

	from domonic.JSON import return_json

	@return_json
	def api_payload():
	    return {"name": "domonic", "features": ["html", "dom", "webapi"]}

	print(api_payload())
	# {"name": "domonic", "features": ["html", "dom", "webapi"]}

Data to Markup
--------------

.. code-block :: python

	import domonic.JSON as JSON
	from domonic.html import h2, section

	rows = [{"name": "Ada", "role": "engineer"}, {"name": "Grace", "role": "compiler"}]
	page = section(h2("People"), JSON.tablify(rows))
	print(page)
	# <section><h2>People</h2><table><tr><th>name</th><th>role</th></tr><tr><td>Ada</td><td>engineer</td></tr><tr><td>Grace</td><td>compiler</td></tr></table></section>

.. automodule:: domonic.JSON
    :members:
    :noindex:
    
