Templates and Components
======================================

.. meta::
   :description: Build Python HTML templates and reusable server-side components with domonic, including component classes, render functions, and web framework responses.
   :keywords: Python components, Python HTML templates, server-side rendering Python, reusable HTML components, domonic components

With all these pieces you can build templates and components.

Small Function Component
------------------------

For most pages, a plain Python function is enough.

.. code-block :: python

	from domonic.html import a, article, h2, p

	def card(title, body, url):
	    return article(
	        h2(title),
	        p(body),
	        a("Read more", _href=url),
	        _class="card",
	    )

	print(card("DOM", "Build real document trees in Python.", "/docs/dom"))
	# <article class="card"><h2>DOM</h2><p>Build real document trees in Python.</p><a href="/docs/dom">Read more</a></article>

Reusable Class Component
------------------------

Use a class when the component has state, helper methods, or several render
paths.

.. code-block :: python

	from domonic.html import button, div, span

	class Counter:
	    def __init__(self, value=0):
	        self.value = value

	    def __str__(self):
	        return str(
	            div(
	                span(str(self.value), _class="count"),
	                button("+", _type="button"),
	                _class="counter",
	            )
	        )

	print(Counter(3))
	# <div class="counter"><span class="count">3</span><button type="button">+</button></div>

Server Response
---------------

domonic only provides the view. Return the rendered string from FastAPI, Flask,
Django, Sanic, Starlette, or any framework that accepts HTML responses.

.. code-block :: python

	from domonic.html import body, h1, html, main

	def homepage():
	    return str(html(body(main(h1("Hello from domonic")))))
	# <html><body><main><h1>Hello from domonic</h1></main></body></html>


Templates
----------------
**Some notes on templates**

domonic mixed with lambdas can create templates without needing to make a class.

.. code-block :: python

	from domonic.html import button, div

	MARGIN = 10

	# Create a template.
	some_tmpl = lambda somevar: div( _style=f"display:inline;margin:{MARGIN}px;").html(
	    button(somevar, _style="background-color:white;color:black;")
	)

Then you can use it like this:

.. code-block :: python

	print(some_tmpl("some content"))
	# <div style="display:inline;margin:10px;"><button style="background-color:white;color:black;">some content</button></div>


Here is a larger template that uses a class and takes content as input.

.. code-block :: python

	class Webpage:

	    def __init__(self, content=None):
	        self.content = content

	    def __str__(self):
	        classless_css = link(_rel="stylesheet", _href="https://unpkg.com/marx-css/css/marx.min.css")
	        jquery = script(_src="https://code.jquery.com/jquery-3.5.1.min.js"),
	        script(_src=domonic.JS_MASTER),
        	link(_rel="stylesheet", _type="text/css", _href=domonic.CSS_STYLE),
	        code = script('''
	            $(document).on( "click", ".close", function() {
	                var _id = $(this).data('ref');
	                $('#'+_id).css("display","none");
	            });
	            $(document).on( "click", ".open", function() {
	                var _id = $(this).data('ref');
	                $('#'+_id).css("display","block");
	            });

	            // Pass an element ID and an endpoint to redraw that div with the endpoint response.
	            window.redraw = function( _id, endpoint ){
	                $.get( endpoint, function( data ) {
	                window.console.log(data)
	                $( "#"+_id ).html( $(data).html() );
	                });
	            }

	        ''')
	        styles = style('''
	            .domonic-container {
	                padding:20px;
	            }
	            .modal {
	                display: none;
	                position: fixed;
	                z-index: 1;
	                left: 0;
	                top: 0;
	                width: 100%;
	                height: 100%;
	                overflow: auto;
	                background-color: rgb(0,0,0);
	                background-color: rgba(0,0,0,0.4);
	            }
	            .modal-content {
	                background-color: #fefefe;
	                margin: 15% auto;
	                padding: 20px;
	                border: 1px solid #888;
	                width: 80%;
	            }
	            .btn-sm {
	                font-size:10px;
	                padding: 0px;
	                padding-left: 2px;
	                padding-right: 2px;
	            }
	            .del {
	                background-color:red;
	            }
	            .go {
	                background-color:green;
	            }

	        ''')
	        return str(
	            html(
	                '<!DOCTYPE HTML>',
	                head(classless_css, jquery, code, styles),
	                body(div(self.content, _class="domonic-container"))
	                )
	            )


You can now render your template with content as input.

.. code-block :: python

	@app.route('/')
	async def home(request):
	    page = article(
	        div(h1("my homepage!"))
	    	)
	    return response.html( render( Webpage(page) ) )



Important notes on templating
--------------------------------

You can create a ``div`` with content like this:

.. code-block :: python

    div("some content")

Python does not allow keyword arguments before positional arguments, so this will not work:

.. code-block :: python

    div(_class="container", p("Some content") )

Python will complain that the parameters are in the wrong order. Put content before attributes:

.. code-block :: python

    div( p("Some content"), _class="container")

That can get awkward when a ``div`` gets long.

You can get around this by using ``html``, which is available on every ``Element``:

.. code-block :: python

	div( _class="container" ).html("Some content")

This is not like jQuery's ``html`` function, which returns only inner content. Use ``innerHTML`` for that.

It is used specifically for rendering.



Common Errors
----------------

When you first start templating this way you can make a lot of common mistakes. Usually missing underscores or commas between attributes.

Refer back to this page for a few days until you get used to it.

Here are four common mistakes from larger templates:

(for example, the bootstrap examples in ``test_domonic.py``)

IndexError: list index out of range
    - You most likely forgot an underscore on an attribute.
    - THIS ALSO APPLIES TO ``{"_data-tags":"x"}``

SyntaxError: invalid syntax
    - You are missing a comma between attributes.

SyntaxError: positional argument follows keyword argument
    - Pass strings and child nodes first, then attributes.

TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'dict'
    - You are missing a comma before ``**{}``.



Components
----------------
**Some notes on components**

A component might look something like this:

.. code-block :: python

	from domonic.html import *
	from domonic.javascript import Math
	from domonic.terminal import ifconfig

	class My_Component:
	    
	    def __init__(self, request, *args, **kwargs):
	        self.id = 'launcher'

	    def __str__(self):
	        return str(
	        	div(
		        	div(_id=self.id).html(
		        	"CONTENT"
		            ),
		            script('''

		            '''
		            )
		        )
		    )


Now you need a server, because domonic only provides the view.

These examples use Sanic, but it could be Flask or any other framework that provides routing.

A component could take a request directly as input and return HTML:

.. code-block :: python

	@app.route("/component/<component>")
	async def component(request, component):
	    try:
	        module = __import__(f'app.components.{component}')
	        my_class = getattr(module, component.title())
	        return response.html( str( my_class(request) ) )
	    except Exception as e:
	        print(e)
	        return response.html( str( div("COMPONENT NOT FOUND!") ) )

For this to work, the component would need to be in ``app/components/my_component.py``.


Then a component or template can return HTML and render directly into your page using a little JavaScript.

.. code-block :: javascript

	// Pass an element ID and an endpoint to redraw that div with the endpoint response.
	window.redraw = function( _id, endpoint ){
	    $.get( endpoint, function( data ) {
	    window.console.log(data)
	    $( "#"+_id ).html( $(data).html() );
	    });
	}


*built-in components*

The built-in components package is useful for examples and prototypes. For
production apps, treat these components as starter patterns and keep your own
stable components in your application.

Related Examples and Guides
---------------------------

- :doc:`../guides/server-side-html`
- :doc:`../guides/live-dom-updates`
- `examples/grid.py <https://github.com/byteface/domonic/blob/master/examples/grid.py>`_
- `examples/windowed/app.py <https://github.com/byteface/domonic/blob/master/examples/windowed/app.py>`_
- `examples/games/hangman.py <https://github.com/byteface/domonic/blob/master/examples/games/hangman.py>`_

You should use domonic to make your own components.

Some components used in examples are listed here.


SpriteCSS
----------------

For a working example, see ``examples/ken/sf2.py``.

Pass a UID, width, height, path, duration, steps, looping flag, and y-offset.

.. code-block :: javascript

	animated_monster = SpriteCSS('ken', 70, 80, 'assets/spritesheets/ken.png', 0.8, 4, True, 80)
