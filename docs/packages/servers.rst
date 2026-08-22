Servers
=================

Generating static HTML files with domonic is fun.

Python has a built-in server for viewing generated files locally:


Running a Python Server to View Static Pages
--------------------------------------------------------

.. code-block :: bash
    
    cd Desktop/yourproject
    python3 -m http.server 8080


Now go to http://localhost:8080 and view your website.


Serving dynamic content
----------------------------

For dynamic content, you will need a web server.

domonic does not come with a web server, but the Python community has plenty of great ones to choose from.

Below are examples of using domonic with popular web servers.

WARNING: When generating dynamic content, escape user-generated content to avoid `XSS attacks <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>`_.

CLI project scaffolds
--------------------------------

The project command can generate a one-file hello world for a pinned server or framework:

.. code-block :: bash

    domonic project mysite --server fasthtml

Current scaffold choices are:

.. code-block :: text

    none
    sanic
    flask
    apiflask
    cherrypy
    django
    django-ninja
    bottle
    pyramid
    werkzeug
    tornado
    aiohttp
    fastapi
    fasthtml
    starlette
    blacksheep
    muffin
    falcon
    baize
    esmerald
    granian
    emmett
    eve
    klein
    litestar
    quart
    robyn

Project-shaped tools such as Connexion and py4web, and app suites such as NiceGUI,
Reflex, Streamlit, Gradio, and Shiny, are better handled as dedicated examples
instead of pretending they fit a single ``app.py`` scaffold.


Using domonic with Cherrypy
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install cherrypy
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python
                
    import cherrypy
    from domonic.html import *

    class HelloWorld:

        @cherrypy.expose
        def index(self):
            return str( 
                        html(
                        head(),
                        body(
                            div(span("Hello, World!"))
                            )
                        )
                    )

    cherrypy.quickstart(HelloWorld())


Run it with:

.. code-block :: bash

    python app.py

Then visit http://localhost:8080 in your browser.

`Find out more about CherryPy <https://pypi.org/project/CherryPy/>`_.


Using domonic with Pyramid
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install pyramid
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python

    from wsgiref.simple_server import make_server
    from pyramid.config import Configurator
    from pyramid.response import Response
    from domonic.html import *

    def hello_world(request):
        return Response(str( 
                        html(
                        head(),
                        body(
                            div(span("Hello, World!"))
                            )
                        )
                    )
                )

    if __name__ == '__main__':
        with Configurator() as config:
            config.add_route('hello', '/')
            config.add_view(hello_world, route_name='hello')
            app = config.make_wsgi_app()
        server = make_server('0.0.0.0', 8080, app)
        server.serve_forever()


Run it with:

.. code-block :: bash

    python app.py

Then visit http://localhost:8080 in your browser.

`Find out more about Pyramid <https://trypyramid.com/>`_.


Using domonic with Bottle
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install bottle
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python

    from bottle import route, run
    from domonic.html import *

    @route('/hello/<name>')
    def index(name):
        return str( 
                html(
                head(),
                body(
                    div(span(f"Hello, {name}!"))
                    )
                )
            )

    run(host='localhost', port=8080)

Run it with:

.. code-block :: bash

    python app.py

Then visit http://localhost:8080/hello/yourname in your browser.


`Find out more about Bottle <https://bottlepy.org/docs/dev/>`_.


Using domonic with Sanic
--------------------------------

A lot of the examples in the repo use Sanic. It feels Flask-like and is async.

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install sanic
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python
        
    from sanic import Sanic
    from sanic import response
    from domonic.html import *

    app = Sanic("My Hello, world app")

    @app.route('/')
    async def test(request):
        return response.html(str( 
            html(
            head(),
            body(
                div(span("Hello World!"))
                )
            ))
        )

    if __name__ == '__main__':
        app.run()


Run it with:

.. code-block :: bash

    python app.py

Then visit http://localhost:8000 in your browser.

`Find out more about Sanic <https://sanic.readthedocs.io/en/stable/>`_.


Using domonic with Flask
--------------------------------

Flask already comes with Jinja, but using domonic is still possible.

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install flask
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python
    
    from flask import Flask
    from domonic.html import *

    app = Flask(__name__)

    @app.route("/")
    def hello():
        return str( 
            html(
            head(),
            body(
                div(span("Hello World!"))
                )
            ))

    if __name__ == '__main__':
        app.run()


Run it with:

.. code-block :: bash

    python app.py

Then visit http://localhost:5000 in your browser.

`Find out more about Flask <https://flask.palletsprojects.com/>`_.


Using domonic with FastAPI
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install fastapi
    pip install uvicorn
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python
            
    from fastapi import FastAPI
    from fastapi.responses import HTMLResponse
    from domonic.html import *

    app = FastAPI()

    @app.get("/", response_class=HTMLResponse)
    def read_root():
        return str( 
        html(
        head(),
        body(
            div(span("Hello World!"))
            )
        ))


Run it with:

.. code-block :: bash

    uvicorn app:app --reload

Then visit http://localhost:8000 in your browser.

`Find out more about FastAPI <https://fastapi.tiangolo.com/>`_.


Using domonic with Werkzeug
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install werkzeug
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python
            
    from werkzeug.wrappers import Request, Response
    from domonic.html import *

    @Request.application
    def application(request):
        return Response(str( 
                        html(
                        head(),
                        body(
                            div(span("Hello World!"))
                            )
                        )), mimetype='text/html')

    if __name__ == '__main__':
        from werkzeug.serving import run_simple
        run_simple('localhost', 4000, application)


Run it with:

.. code-block :: bash

    python app.py

Then visit http://localhost:4000/ in your browser.

`Find out more about Werkzeug <https://werkzeug.palletsprojects.com/>`_.


Using domonic with Starlette
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install starlette
    pip install uvicorn
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python
        
    from starlette.applications import Starlette
    from starlette.responses import HTMLResponse
    from starlette.routing import Route
    from domonic.html import *

    async def homepage(request):
        return HTMLResponse(str( 
                    html(
                    head(),
                    body(
                        div(span("Hello World!"))
                        )
                    ))
            )

    routes = [
        Route("/", endpoint=homepage)
    ]

    app = Starlette(debug=True, routes=routes)


Run it with:

.. code-block :: bash

    uvicorn app:app --reload

Then visit http://localhost:8000 in your browser.

`Find out more about Starlette <https://www.starlette.io/>`_.


Using domonic with Tornado
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install tornado
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python
            
    import tornado.ioloop
    import tornado.web
    from domonic.html import *

    class MainHandler(tornado.web.RequestHandler):
        def get(self):
            self.write(str( 
                html(
                head(),
                body(
                    div(span("Hello World!"))
                    )
                )))

    def make_app():
        return tornado.web.Application([
            (r"/", MainHandler),
        ])

    if __name__ == "__main__":
        app = make_app()
        app.listen(8888)
        tornado.ioloop.IOLoop.current().start()


Run it with:

.. code-block :: bash

    python app.py

Then visit http://localhost:8888/ in your browser.

`Find out more about Tornado <https://www.tornadoweb.org/en/stable/>`_.


Using domonic with Django
--------------------------------

Django already has a template system, but you can still return domonic-rendered HTML from a view.

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install django
    pip install domonic
    django-admin startproject mysite

Now cd into ``mysite`` and edit ``urls.py``:

.. code-block :: python

    from django.contrib import admin
    from django.urls import path
    from django.http import HttpResponse
    from domonic import div, span

    def index(request):
        mywebpage = str(
                    div(span("Hello World!"))
                )
        return HttpResponse(mywebpage)

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', index, name='index'),
    ]


Run it from inside the ``mysite`` folder:

.. code-block :: bash

    python manage.py runserver

Then visit http://localhost:8000/ in your browser.

Note: avoid ``import *`` in Django examples and import the tags you need.

`Find out more about Django <https://www.djangoproject.com/>`_.



Using domonic with aiohttp
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install aiohttp
    pip install domonic

Create a file called ``app.py``:

.. code-block :: python

    from domonic.html import *
    from aiohttp import web

    async def handle(request):
        name = request.match_info.get('name', "Anonymous")
        page = html(head(),body(div(span("Hello, World!"))))
        return web.Response(text=str(page), content_type='text/html')

    app = web.Application()
    app.add_routes([web.get('/', handle),
                    web.get('/{name}', handle)])

    if __name__ == '__main__':
        web.run_app(app)


Run it with:

.. code-block :: bash

    python app.py

Then visit http://localhost:8080/ in your browser.

`Find out more about aiohttp <https://docs.aiohttp.org/en/stable/>`_.



For a broader list of Python web frameworks, see `web-framework-rank <https://github.com/tbicr/web-framework-rank>`_.



SPAs
--------------------------------

Once you have a framework, you can use simple JavaScript to call endpoints and redraw parts of the DOM.

.. code-block :: javascript

    function redraw(_id, endpoint) {
      fetch(endpoint)
        .then(function(response){return response.text();})
        .then(function(data){
                document.getElementById(_id).innerHTML = data;
            }
        )
    }

Check out the templates and components section to take your templating further.

Another alternative to running a web server is running a serverless function.


Using domonic with AWS Lambda
--------------------------------

The original version of domonic was tags-only and written for an AWS Lambda function.

The original proof-of-concept code is `in the archive <https://github.com/byteface/domonic/blob/master/archive/poc.py>`_.

You can create a ``tags.py`` file alongside your Lambda in the AWS GUI, paste in the tags, then import and use them.

To upload entire packages, people often drop ``lambda_function.py`` into the ``site-packages`` folder of their virtual environment.

Then zip and upload the whole thing.

`Find out more about AWS Lambda <https://aws.amazon.com/lambda/>`_.

You can also try an ASGI adapter on Lambda with `Mangum <https://mangum.io/>`_.


Using domonic with Google Cloud Functions
----------------------------------------------

Google has Cloud Functions.

Their documentation explains how to handle package dependencies.

https://cloud.google.com/functions/docs/writing/specifying-dependencies-python

`Find out more about Google Cloud Functions <https://cloud.google.com/functions>`_.
