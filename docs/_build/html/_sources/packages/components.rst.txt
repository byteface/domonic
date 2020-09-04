Domonic: templates and components
======================================

With all these pieces you can now build templates or components...


Templates
----------------
**Some notes on templates**

domonic mixed with lambdas can create templates without needing to make a class...

.. code-block :: python

	# create a template
	some_tmpl = lambda somevar: div( _style=f"display:inline;margin:{MARGIN}px;").html(
	    button(somevar, _style="background-color:white;color:black;")
	)

then you can us it like this...

.. code-block :: python

	some_tmpl("some content")


Here is another template. This one is larger and uses a Class. It can take content as input.

.. code-block :: python

	class Webpage(object):

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

	            // pass an ElementID and an endpoint to redraw that div with the endpoints response
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


You can now render your template. Which can take content as input.

.. code-block :: python

	@app.route('/')
	async def home(request):
	    page = article(
	        div(h1("my homepage!"))
	    	)
	    return response.html( render( Webpage(page) ) )



Important notes on templating
--------------------------------

while you can create a div with content like :

.. code-block :: python

    div("some content")

python doesn't allow named params before unamed ones. So you can't do this:

.. code-block :: python

    div(_class="container", p("Some content") )

or it will complain the params are in the wrong order. You have to instead put content before attributes:

.. code-block :: python

    div( p("Some content"), _class="container")

which is annoying when a div gets long.

You can get around this by using 'html' which is available on every Element:

.. code-block :: python

	div( _class="container" ).html("Some content")

This is NOT like jQuery html func that returns just the inner content. use innerHTML for that.

It is used specifically for rendering.



Common Errors
----------------

When you first start templating this way you can make a lot of common mistakes. Usually missing underscores or commas between attributes.

Refer back to this page for a few days until you get used to it.

Here are the 4 most common ones I experienced when creating large templates...

( i.e. bootstrap5 examples in test_domonic.py )

IndexError: list index out of range
    - You most likely didn't put a underscore on an attribute.
    - THIS ALSO APPLIES TO **{"_data-tags":"x"}

SyntaxError: invalid syntax
    - You are Missing a comma between attributes

SyntaxError: positional argument follows keyword argument
    - You have to pass attributes LAST. and strings and objects first. *see docs*

TypeError: unsupported operand type(s) for ** or pow(): 'str' and 'dict'
    - You are Missing a comma between attributes. before the **{}



Components
----------------
**Some notes on components**

A component 'might' look something like this...

.. code-block :: python

	from domonic.html import *
	from domonic.javascript import Math
	from domonic.terminal import ifconfig

	class My_Component(object):
	    
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


Now you will need a server as domonic only provides a view.

These example use Sanic. But it could be Flask or any other that can provide routing.

A component could, for example, take a request directly as input and returns html

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

for this to work the component would need to be in a file called:
app/components/my_component.py


Then a given component or template can just return html and render directly into your page using a bit of javascript.

.. code-block :: javascript

	// pass an ElementID and an endpoint to redraw that div with the endpoints response
	window.redraw = function( _id, endpoint ){
	    $.get( endpoint, function( data ) {
	    window.console.log(data)
	    $( "#"+_id ).html( $(data).html() );
	    });
	}

