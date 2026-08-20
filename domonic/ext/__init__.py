"""
    domonic.ext
    ====================================

    This dir is for extending domonic to be useable with other python libs.

"""

from __future__ import annotations

# HELLO WORLDS - hello world code for other libs
# "django"
# "bottle"
# "pyramid"
# "werkzeug"
# "tornado"
# "aiohttp"
# "fastapi"
# "starlette"
# "blacksheep"
# "muffin"
# "falcon"
# "baize"
# "emmett"
# "quart"

# "falcon"
# "eve"
# "graphene"
# "httpx"
# "invenio"
# "jupyterhub"
# "klein"
# "kombu"
# "masonite"
# "motor"
# "pydantic"
# "quart"
# "sanic"
# "trio"


HELLO_BLACKSHEEP: str = """
import uvicorn
from domonic.html import *

from blacksheep.server import Application
from blacksheep.server.responses import html as HTMLResponse

app = Application()

@app.route("/")
async def home(request):
    return HTMLResponse(str(
        html(
        head(),
        body(
            div(span("Hello World!"))
            )
        )
    ))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

HELLO_FAST_API: str = """
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from domonic.html import *

app = FastAPI()

@app.get("/")
def read_root():
    return HTMLResponse(str(
        html(
        head(),
        body(
            div(span("Hello World!"))
            )
        )
    ))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

HELLO_STARLETTE: str = """
import uvicorn
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
        )
    ))

app = Starlette(routes=[Route("/", homepage)])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

HELLO_SANIC: str = """
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
"""

HELLO_FLASK: str = """
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
    app.run(host="127.0.0.1", port=5000)
"""

HELLO_CHERRYPY: str = """
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
"""


HELLO_BOTTLE: str = """
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
"""

HELLO_DJANGO: str = """
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path
from domonic.html import *

def index(request):
    page = html(head(), body(div(span("Hello World!"))))
    return HttpResponse(str(page))

urlpatterns = [path("", index)]

if not settings.configured:
    settings.configure(
        DEBUG=True,
        ROOT_URLCONF=__name__,
        SECRET_KEY="domonic-cli",
        ALLOWED_HOSTS=["*"],
        MIDDLEWARE=[],
        INSTALLED_APPS=[],
    )
    django.setup()

if __name__ == "__main__":
    execute_from_command_line(["app.py", "runserver", "127.0.0.1:8000"])
"""

HELLO_PYRAMID: str = """
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from domonic.html import *

def home(request):
    page = html(head(), body(div(span("Hello World!"))))
    return Response(str(page), content_type="text/html")

if __name__ == "__main__":
    with Configurator() as config:
        config.add_route("home", "/")
        config.add_view(home, route_name="home")
        app = config.make_wsgi_app()
    server = make_server("127.0.0.1", 6543, app)
    server.serve_forever()
"""

HELLO_AIOHTTP: str = """
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
"""

HELLO_TORNADO: str = """
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
"""

HELLO_WERKZEUG: str = """
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
"""

HELLO_FALCON: str = """
import falcon
from wsgiref.simple_server import make_server
from domonic.html import *

class HomeResource:

    def on_get(self, req, resp):
        page = html(head(), body(div(span("Hello World!"))))
        resp.content_type = "text/html"
        resp.text = str(page)

app = falcon.App()
app.add_route("/", HomeResource())

if __name__ == "__main__":
    server = make_server("127.0.0.1", 8000, app)
    server.serve_forever()
"""

HELLO_QUART: str = """
from quart import Quart
from domonic.html import *

app = Quart(__name__)

@app.route("/")
async def hello():
    return str(
        html(
        head(),
        body(
            div(span("Hello World!"))
            )
        )
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
"""

HELLO_MUFFIN: str = """
import muffin
import uvicorn
from domonic.html import *

app = muffin.Application()

@app.route("/")
async def hello(request):
    return str(
        html(
        head(),
        body(
            div(span("Hello World!"))
            )
        )
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

HELLO_BAIZE: str = """
import uvicorn
from baize.asgi import HTMLResponse, request_response
from domonic.html import *

@request_response
async def app(request):
    page = html(head(), body(div(span("Hello World!"))))
    return HTMLResponse(str(page))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

HELLO_EMMETT: str = """
from emmett import App
from domonic.html import *

app = App(__name__)

@app.route("/")
async def index():
    return str(
        html(
        head(),
        body(
            div(span("Hello World!"))
            )
        )
    )

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
"""

HELLO_LITESTAR: str = """
import uvicorn
from litestar import Litestar, get
from domonic.html import *

@get("/")
async def index() -> str:
    return str(
        html(
        head(),
        body(
            div(span("Hello World!"))
            )
        )
    )

app = Litestar(route_handlers=[index])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""

HELLO_ROBYN: str = """
from robyn import Robyn
from domonic.html import *

app = Robyn(__file__)

@app.get("/")
async def index(request):
    return str(
        html(
        head(),
        body(
            div(span("Hello World!"))
            )
        )
    )

app.start(port=8080)
"""


SERVER_SCAFFOLDS: dict[str, dict[str, object]] = {
    "none": {"packages": [], "template": None},
    "sanic": {"packages": ["sanic==25.12.1"], "template": HELLO_SANIC},
    "flask": {"packages": ["Flask==3.1.3"], "template": HELLO_FLASK},
    "cherrypy": {"packages": ["CherryPy==18.10.0"], "template": HELLO_CHERRYPY},
    "django": {
        "packages": [
            'Django==5.2.17; python_version < "3.12"',
            'Django==6.1; python_version >= "3.12"',
        ],
        "template": HELLO_DJANGO,
    },
    "bottle": {"packages": ["bottle==0.13.4"], "template": HELLO_BOTTLE},
    "pyramid": {"packages": ["pyramid==2.1"], "template": HELLO_PYRAMID},
    "werkzeug": {"packages": ["Werkzeug==3.1.8"], "template": HELLO_WERKZEUG},
    "tornado": {"packages": ["tornado==6.5.8"], "template": HELLO_TORNADO},
    "aiohttp": {"packages": ["aiohttp==3.14.3"], "template": HELLO_AIOHTTP},
    "fastapi": {"packages": ["fastapi==0.141.1", "uvicorn==0.52.4"], "template": HELLO_FAST_API},
    "starlette": {"packages": ["starlette==1.6.0", "uvicorn==0.52.4"], "template": HELLO_STARLETTE},
    "blacksheep": {"packages": ["blacksheep==2.6.3", "uvicorn==0.52.4"], "template": HELLO_BLACKSHEEP},
    "muffin": {"packages": ["muffin==2.0.2", "uvicorn==0.52.4"], "template": HELLO_MUFFIN},
    "falcon": {"packages": ["falcon==4.3.1"], "template": HELLO_FALCON},
    "baize": {"packages": ["baize==0.23.1", "uvicorn==0.52.4"], "template": HELLO_BAIZE},
    "emmett": {"packages": ["emmett==2.8.1"], "template": HELLO_EMMETT},
    "litestar": {"packages": ["litestar==2.24.0", "uvicorn==0.52.4"], "template": HELLO_LITESTAR},
    "quart": {"packages": ["Quart==0.22.0", "Hypercorn==0.18.0"], "template": HELLO_QUART},
    "robyn": {"packages": ["robyn==0.88.0"], "template": HELLO_ROBYN},
}


def get_supported_servers() -> list[str]:
    return list(SERVER_SCAFFOLDS.keys())


def get_server_requirements(server: str) -> list[str]:
    scaffold = SERVER_SCAFFOLDS.get(server, {})
    return list(scaffold.get("packages", []))


def get_hello_world(server: str) -> str | None:
    scaffold = SERVER_SCAFFOLDS.get(server, {})
    return scaffold.get("template")
