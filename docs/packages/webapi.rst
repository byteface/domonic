webapi
===================

The webapi is the latest package to be added to domonic.


console
----------------

.. code-block :: python

	from domonic.webabi.console import console
	console.log("Hello World")


encoding
----------------

.. code-block :: python

	from domonic.webabi.encoding import TextEncoder, TextDecoder
	encoder = TextEncoder()


fetch
----------------

.. code-block :: python

	from domonic.webabi.fetch import fetch


URL
----------------

url is a wrapper around the urlparse and urlencode functions in python.

.. code-block :: python

	from domonic.webabi.url import URL

	myurl = URL("http://www.google.com/search?q=domonic")
	print(myurl.host)
	print(myurl.query)
	print(myurl.query.q)
	print(myurl.query.q.value)

for more information see mdn docs... 
# TODO - link


XPATH
----------------

Here's a quick example of using xpath...

.. code-block :: python

	from domonic.webapi.xpath import XPathEvaluator, XPathResult
	
	somehtml = '''
	<div>XPath example</div>
	<div>Number of &lt;div&gt;s: <output></output></div>
	'''
	page = domonic.parseString(somehtml)  # NOTE - probably requries html5lib install
	evaluator = XPathEvaluator()
	expression = evaluator.createExpression("//div")
	result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
	assert result.snapshotLength == 2


for more information see mdn docs... 
# TODO - link




.. automodule:: domonic.webapi.console
    :members:
    :noindex:

.. automodule:: domonic.webapi.encoding
    :members:
    :noindex:

.. automodule:: domonic.webapi.fetch
    :members:
    :noindex:

.. automodule:: domonic.webapi.url
    :members:
    :noindex:

.. automodule:: domonic.webapi.xhr
    :members:
    :noindex:

.. automodule:: domonic.webapi.xpath
    :members:
    :noindex:
