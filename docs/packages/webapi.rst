webapi
===================

The ``webapi`` package groups browser-flavoured APIs that sit alongside the DOM surface.


console
----------------

.. code-block :: python

	from domonic.webapi.console import console
	console.log("Hello World")


encoding
----------------

.. code-block :: python

	from domonic.webapi.encoding import TextEncoder, TextDecoder
	encoder = TextEncoder()


fetch
----------------

.. code-block :: python

	from domonic.webapi.fetch import fetch


URL
----------------

``URL`` is a wrapper around Python's ``urlparse`` and ``urlencode`` helpers.

.. code-block :: python

	from domonic.webapi.url import URL

	myurl = URL("http://www.google.com/search?q=domonic")
	print(myurl.host)
	print(myurl.query)
	print(myurl.query.q)
	print(myurl.query.q.value)

For more information see the MDN URL API docs:
https://developer.mozilla.org/en-US/docs/Web/API/URL


XPATH
----------------

Here's a quick example of using XPath:

.. code-block :: python

	from domonic import domonic
	from domonic.webapi.xpath import XPathEvaluator, XPathResult
	
	somehtml = '''
	<div>XPath example</div>
	<div>Number of &lt;div&gt;s: <output></output></div>
	'''
	page = domonic.parseString(somehtml)
	evaluator = XPathEvaluator()
	expression = evaluator.createExpression("//div")
	result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
	assert result.snapshotLength == 2


For more information, see the MDN Web API docs:
https://developer.mozilla.org/en-US/docs/Web/API




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
