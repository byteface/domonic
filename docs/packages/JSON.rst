JSON
=============

decorate any function that returns python objects to return json instead

.. code-block :: python

	from domonic.JSON import *

	@return_json
	def somefunc():
	    myObj = {"hi":[1,2,3]}
	    return myObj

	print( somefunc() )
	print( is_json(somefunc()) )


convert json arrays into html tables...

.. code-block :: python

	from domonic.JSON import *

	# i.e. containting flat json array of dicts... [{"id":"01","name": "some item"},{"id":"02","name": "some other item"}]

	json_data = JSON.parse_file('somefile.json')
	mytable = JSON.tablify(json_data)
	print(mytable)


convert json arrays into csv files...

.. code-block :: python

	from domonic.JSON import *

	json_data = JSON.parse_file('somefile.json')
	JSON.csvify(json_data, 'data.csv')


convert csv files to json...

.. code-block :: python

	from domonic.JSON import *

	json_data =JSON.csv2json("data.csv")
	print(json_data)


more to come...

.. automodule:: domonic.JSON
    :members:
    :noindex:
    