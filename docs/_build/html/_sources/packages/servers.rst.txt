🚀 servers
=================

Generating static html files with domonic is fun.

Python has a built-in server allowing you to view your generated files:


Running a python server to view static pages
--------------------------------------------------------

.. code-block :: python
    
    cd Desktop/yourproject
    python3 -m http.server 8080


now go to localhost:8080 and view your website.


Serving dynamic content
----------------------------

For dynamic content you will need a better webserver.

Domonic does not come with a webserver but there are plenty of great ones in the python community to choose from. 

Below are some examples of how to use domonic with some popular webservers

WARNING: When generating dynamic content make sure to escape any user generated content to avoid `XSS attacks. <https://cheatsheetseries.owasp.org/cheatsheets/Cross_Site_Scripting_Prevention_Cheat_Sheet.html>`_.


Using domonic with Cherrypy
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install cherrypy
    pip install domonic

now create a file called app.py

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


to run it do this:

.. code-block :: bash

    python app.py

and visit localhost:8080 in your browser

`Find out more about Cherrypy here... <https://pypi.org/project/CherryPy/>`_.


Using domonic with Pyramid
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install pyramid
    pip install domonic

now create a file called app.py

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


to run it do this:

.. code-block :: bash

    python app.py

and visit localhost:8080 in your browser

`Find out more about Pyramid here... <https://trypyramid.com/>`_.


Using domonic with Bottle
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install bottle
    pip install domonic

now create a file called app.py

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

to run it do this:

.. code-block :: bash

    python app.py

and visit http://localhost:8080/hello/yourname in your browser


`Find out more about Bottle here... <https://bottlepy.org/docs/dev/>`_.


Using domonic with Sanic
--------------------------------

A lot of the examples in the repo use Sanic. It's like Flask and is async

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install sanic
    pip install domonic

now create a file called app.py

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


to run it do this:

.. code-block :: bash

    python app.py

and visit http://localhost:8000 in your browser

`Find out more about Sanic here... <https://sanic.readthedocs.io/en/stable/>`_.


Using domonic with Flask
--------------------------------

Flask comes with Jinja already but it's still possible...

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install flask
    pip install domonic

now create a file called app.py

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


to run it do this:

.. code-block :: bash

    python app.py

and visit http://localhost:5000 in your browser

`Find out more about Flask here... <https://flask.palletsprojects.com/en/2.0.x/>`_.


Using domonic with FastAPI
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install fastapi
    pip install uvicorn
    pip install domonic

now create a file called app.py

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


to run it do this:

.. code-block :: bash

    uvicorn app:app --reload

and visit http://localhost:8000 in your browser

`Find out more about FastAPI here... <https://fastapi.tiangolo.com/>`_.


Using domonic with Werkzeug
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install werkzeug
    pip install domonic

now create a file called app.py

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


to run it do this:

.. code-block :: bash

    python app.py

and visit http://localhost:4000/ in your browser

`Find out more about Werkzeug here... <https://werkzeug.palletsprojects.com/en/2.0.x/>`_.


Using domonic with Starlette
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install starlette
    pip install uvicorn
    pip install domonic

now create a file called app.py

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


to run it do this:

.. code-block :: bash

    uvicorn app:app --reload

and visit http://localhost:8000 in your browser

`Find out more about Starlette here... <https://www.starlette.io/>`_.


Using domonic with Tornado
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install tornado
    pip install domonic

now create a file called app.py

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


to run it do this:

.. code-block :: bash

    python app.py

and visit http://localhost:8888/ in your browser

`Find out more about Tornado here... <https://www.tornadoweb.org/en/stable/>`_.


Using domonic with Django
--------------------------------

Django already has some kind of Jinja but more restrictive.

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install django
    pip install domonic
    django-admin startproject mysite

now cd into mysite and edit urls.py

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


to run it do this from within mysite folder:

.. code-block :: bash

    python manage.py runserver

and visit http://localhost:8000/ in your browser

Note: Django didn't allow import * so there's a conflict somewhere. I resolved by importing what I needed.

`Find out more about Django here... <https://www.djangoproject.com/>`_.



Using domonic with aiohttp
--------------------------------

.. code-block :: bash

    python3 -m venv venv
    . venv/bin/activate
    pip install aiohttp
    pip install domonic

now create a file called app.py

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


to run it do this:

.. code-block :: bash

    python app.py

and visit http://localhost:8080/ in your browser

`Find out more about aiohttp here... <https://docs.aiohttp.org/en/stable/>`_.



and if that wasn't enough webservers to try out this isn't even `a more complete list!!! <https://github.com/tbicr/web-framework-rank>`_.



SPA's
--------------------------------

Now you have a framework you can use some simple javascript to call on endpoints to redraw parts of the dom.

.. code-block :: javascript

    function redraw(_id, endpoint) {
      fetch(endpoint)
        .then(function(response){return response.text();})
        .then(function(data){
                document.getElementById(_id).innerHTML = data;
            }
        )
    }

Checkout the 'templates and components' section to see how you can take your templating skills to the next level.

Another alternative to running a webserver is running a serverless function. See below for more details.


Using domonic with AWS lambda
--------------------------------

The original version of domonic was tags only and written to be used in an aws lambda function.

the original POC code for that is `here in the archive <https://github.com/byteface/domonic/blob/master/archive/poc.py>`_.

You can just create a file called tags.py alongside your lambda with the AWS GUI and paste in the tags then import and use them.

Alternatively to upload entire packages people tend to drop their lambda_function.py into the /site-packages folder of their virtualenv. 

Then zip and upload the whole thing.

`Find out more about AWS Lambda here... <https://aws.amazon.com/lambda/>`_.

or even try an ASGI adapter on your lambda with magnum!... <https://mangum.io/>`_.


Using domonic with Google Cloud Functions
----------------------------------------------

Google have 'cloud functions'.

Dealing with Package dependencies is here in their documentation.

https://cloud.google.com/functions/docs/writing/specifying-dependencies-python

`Find out more about Google Cloud Functions here... <https://cloud.google.com/functions>`_.


