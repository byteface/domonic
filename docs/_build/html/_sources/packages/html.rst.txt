Domonic: HTML
=============


rendering
----------------
render takes 2 parameters, some domonic and an optional output file.

.. code-block :: python

	page = div(span('Hello World'))
	render(page, 'index.html')


templating
----------------

.. code-block :: python

  from domonic import *

    output = render( 
        html(
            head(
                style(),
                script(),
            ),
            body(
                div("hello world"),
                a("this is a link", _href="http://www.somesite.com", _style="font-size:10px;"),
                ol(''.join([f'{li()}' for thing in range(5)])),
                h1("test", _class="test"),
            )
        )
    )

.. code-block :: html

  <html><head><style></style><script></script></head><body><div>hello world</div><a href="http://www.somesite.com" style="font-size:10px;">this is a link</a><ol><li></li><li></li><li></li><li></li><li></li></ol><h1 class="test">test</h1></body></html>


Take a look in tests/test_html.py at the bootstrap5 alpha examples. All tests passed on several templates.


usage
----------------

.. code-block :: python

    print(html(body(h1('Hello, World!'))))

.. code-block :: html

	<html><body><h1>Hello, World!</h1></body></html>


attributes
----------------
prepend attributes with an underscore ( avoids clashing with python keywords )

.. code-block :: python

	test = label(_class='classname', _for="someinput")
	print(test)

.. code-block :: html

	<label class="classname" for="someinput"></label>


lists
----------------
just do list comprehension and join it to strip the square brackets

.. code-block :: python

	ul(''.join([f'{li()}' for thing in range(5)])),

.. code-block :: html

	<ul><li></li><li></li><li></li><li></li></ul>


data-tags
----------------
python doesn't allow hyphens in parameter names. so use variable keyword argument syntax for custom data-tags

.. code-block :: python

	div("test", **{"_data-test":"test"} )

DONT FORGET TO PREPEND THE UNDERSCORE.


fugly
----------------
use your own methods to prettify. the example uses a library that leverages beautifulsoup. i.e.

.. code-block :: python

	output = render(html(body(h1('Hello, World!'))))
	from html5print import HTMLBeautifier
	print(HTMLBeautifier.beautify(output, 4))


createElement
----------------
to create your own elements use the DOM API

.. code-block :: python

	from domonic.dom import *
	from domonic.html import *

	site = html()
	el = document.createElement('myelement')
	site.appendChild(el)
	print(site)


For more info about the DOM API navigate to that section...