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
	print( is_json(somefunc()) )


Convert JSON arrays into HTML tables:

.. code-block :: python

	import domonic.JSON as JSON

	# A flat JSON array of dicts, for example:
	# [{"id": "01", "name": "some item"}, {"id": "02", "name": "some other item"}]

	json_data = JSON.parse_file('somefile.json')
	mytable = JSON.tablify(json_data)
	print(mytable)


Convert JSON arrays into CSV files:

.. code-block :: python

	import domonic.JSON as JSON

	json_data = JSON.parse_file('somefile.json')
	JSON.csvify(json_data, 'data.csv')


Convert CSV files to JSON:

.. code-block :: python

	import domonic.JSON as JSON

	json_data = JSON.csv2json("data.csv")
	print(json_data)


The module also includes helpers for validation, flattening, and turning table nodes back into row dictionaries.

API Response Helpers
--------------------

.. code-block :: python

	from domonic.JSON import return_json

	@return_json
	def api_payload():
	    return {"name": "domonic", "features": ["html", "dom", "webapi"]}

	print(api_payload())

Data to Markup
--------------

.. code-block :: python

	import domonic.JSON as JSON
	from domonic.html import h2, section

	rows = [{"name": "Ada", "role": "engineer"}, {"name": "Grace", "role": "compiler"}]
	page = section(h2("People"), JSON.tablify(rows))
	print(page)

.. automodule:: domonic.JSON
    :members:
    :noindex:
    
