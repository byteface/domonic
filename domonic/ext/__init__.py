"""
domonic.ext
====================================

This dir is for extending domonic to be useable with other python libs.

"""

from __future__ import annotations

from typing import Any


HELLO_BLACKSHEEP: str = (
    """
import uvicorn
from blacksheep import Application, get, html as html_response
from domonic.ext.lander import page

app = Application()


@get("/")
async def home():
    return html_response(str(page()))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
)

HELLO_FAST_API: str = (
    """
import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from domonic.ext.lander import page

app = FastAPI()


@app.get("/", response_class=HTMLResponse)
async def read_root():
    return str(page())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
)

HELLO_FASTHTML: str = (
    """
from fasthtml.common import FastHTML, serve
from domonic.ext.lander import page

app = FastHTML()


@app.get("/")
def home():
    return str(page())

if __name__ == "__main__":
    serve(host="127.0.0.1", port=8000)
"""
)

HELLO_STARLETTE: str = (
    """
import uvicorn
from starlette.applications import Starlette
from starlette.responses import HTMLResponse
from starlette.routing import Route
from domonic.ext.lander import page


async def homepage(request):
    return HTMLResponse(str(page()))

app = Starlette(routes=[Route("/", homepage)])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
)

HELLO_SANIC: str = (
    """
from sanic import Sanic
from sanic import response
from domonic.ext.lander import page

app = Sanic("domonic_sanic")


@app.get("/")
async def index(request):
    return response.html(str(page()))

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
"""
)

HELLO_FLASK: str = (
    """
from flask import Flask
from domonic.ext.lander import page

app = Flask(__name__)


@app.route("/")
def index():
    return str(page())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
"""
)

HELLO_API_FLASK: str = (
    """
from apiflask import APIFlask
from flask import Response
from domonic.ext.lander import page

app = APIFlask(__name__, title="domonic + APIFlask", version="1.0.0")


@app.get("/")
def index():
    return Response(str(page()), mimetype="text/html")

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
"""
)

HELLO_CHERRYPY: str = (
    """
import cherrypy
from domonic.ext.lander import page


class HelloWorld:

    @cherrypy.expose
    def index(self):
        cherrypy.response.headers["Content-Type"] = "text/html; charset=utf-8"
        return str(page())

if __name__ == "__main__":
    cherrypy.config.update({"server.socket_host": "127.0.0.1", "server.socket_port": 8000})
    cherrypy.quickstart(HelloWorld())
"""
)


HELLO_BOTTLE: str = (
    """
from bottle import route, run
from domonic.ext.lander import page


@route("/")
def index():
    return str(page())

if __name__ == "__main__":
    run(host="127.0.0.1", port=8000)
"""
)

HELLO_DJANGO: str = (
    """
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path
from domonic.ext.lander import page


def index(request):
    return HttpResponse(str(page()), content_type="text/html")

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
)

HELLO_DJANGO_NINJA: str = (
    """
import django
from django.conf import settings
from django.core.management import execute_from_command_line
from django.http import HttpResponse
from django.urls import path
from domonic.ext.lander import page

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

from ninja import NinjaAPI

api = NinjaAPI(title="domonic + Django Ninja")


def index(request):
    return HttpResponse(str(page()), content_type="text/html")

@api.get("/hello")
def hello(request):
    return "Hello from Django Ninja!"

urlpatterns = [
    path("", index),
    path("api/", api.urls),
]

if __name__ == "__main__":
    execute_from_command_line(["app.py", "runserver", "127.0.0.1:8000"])
"""
)

HELLO_PYRAMID: str = (
    """
from wsgiref.simple_server import make_server
from pyramid.config import Configurator
from pyramid.response import Response
from domonic.ext.lander import page


def home(request):
    return Response(str(page()), content_type="text/html")

if __name__ == "__main__":
    with Configurator() as config:
        config.add_route("home", "/")
        config.add_view(home, route_name="home")
        app = config.make_wsgi_app()
    server = make_server("127.0.0.1", 6543, app)
    server.serve_forever()
"""
)

HELLO_AIOHTTP: str = (
    """
from aiohttp import web
from domonic.ext.lander import page


async def handle(request):
    return web.Response(text=str(page()), content_type="text/html")

app = web.Application()
app.add_routes([web.get("/", handle)])

if __name__ == "__main__":
    web.run_app(app, host="127.0.0.1", port=8000)
"""
)

HELLO_TORNADO: str = (
    """
import tornado.ioloop
import tornado.web
from domonic.ext.lander import page


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.set_header("Content-Type", "text/html; charset=utf-8")
        self.write(str(page()))

def make_app():
    return tornado.web.Application([
        (r"/", MainHandler),
    ])

if __name__ == "__main__":
    app = make_app()
    app.listen(8000, address="127.0.0.1")
    tornado.ioloop.IOLoop.current().start()
"""
)

HELLO_WERKZEUG: str = (
    """
from werkzeug.wrappers import Request, Response
from domonic.ext.lander import page


@Request.application
def application(request):
    return Response(str(page()), mimetype="text/html")

if __name__ == "__main__":
    from werkzeug.serving import run_simple
    run_simple("127.0.0.1", 8000, application)
"""
)

HELLO_FALCON: str = (
    """
import falcon
from wsgiref.simple_server import make_server
from domonic.ext.lander import page


class HomeResource:

    def on_get(self, req, resp):
        resp.content_type = "text/html"
        resp.text = str(page())

app = falcon.App()
app.add_route("/", HomeResource())

if __name__ == "__main__":
    server = make_server("127.0.0.1", 8000, app)
    server.serve_forever()
"""
)

HELLO_QUART: str = (
    """
from quart import Quart
from domonic.ext.lander import page

app = Quart(__name__)


@app.route("/")
async def index():
    return str(page())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
"""
)

HELLO_MUFFIN: str = (
    """
import muffin
import uvicorn
from domonic.ext.lander import page

app = muffin.Application()


@app.route("/")
async def index(request):
    return str(page())

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
)

HELLO_BAIZE: str = (
    """
import uvicorn
from baize.asgi import HTMLResponse, request_response
from domonic.ext.lander import page


@request_response
async def app(request):
    return HTMLResponse(str(page()))

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
)

HELLO_ESMERALD: str = (
    """
import uvicorn
from esmerald import Esmerald, EsmeraldSettings, Gateway, Response, get
from esmerald.conf import monkay
from domonic.ext.lander import page

class DomonicSettings(EsmeraldSettings):
    model_config = {**EsmeraldSettings.model_config, "env_prefix": "DOMONIC_ESMERALD_"}

monkay.settings = DomonicSettings()


@get()
async def homepage() -> Response:
    return Response(str(page()), media_type="text/html")

app = Esmerald(routes=[Gateway("/", handler=homepage)], settings_module=DomonicSettings)

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
)

HELLO_GRANIAN: str = (
    """
from granian import Granian
from domonic.ext.lander import page


async def app(scope, receive, send):
    if scope["type"] == "lifespan":
        while True:
            message = await receive()
            if message["type"] == "lifespan.startup":
                await send({"type": "lifespan.startup.complete"})
            elif message["type"] == "lifespan.shutdown":
                await send({"type": "lifespan.shutdown.complete"})
                return
        return

    if scope["type"] != "http":
        return

    body_bytes = str(page()).encode("utf-8")
    await send(
        {
            "type": "http.response.start",
            "status": 200,
            "headers": [
                (b"content-type", b"text/html; charset=utf-8"),
                (b"content-length", str(len(body_bytes)).encode("ascii")),
            ],
        }
    )
    await send({"type": "http.response.body", "body": body_bytes})

if __name__ == "__main__":
    Granian("app:app", interface="asgi", host="127.0.0.1", port=8000).serve()
"""
)

HELLO_EMMETT: str = (
    """
from emmett import App
from domonic.ext.lander import page

app = App(__name__)


@app.route("/")
async def index():
    return str(page())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
"""
)

HELLO_LITESTAR: str = (
    """
import uvicorn
from litestar import Litestar, MediaType, get
from domonic.ext.lander import page


@get("/", media_type=MediaType.HTML)
async def index() -> str:
    return str(page())

app = Litestar(route_handlers=[index])

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
"""
)

HELLO_ROBYN: str = (
    """
from robyn import Robyn
from domonic.ext.lander import page

app = Robyn(__file__)


@app.get("/")
async def index(request):
    return str(page())

if __name__ == "__main__":
    app.start(host="127.0.0.1", port=8000)
"""
)

HELLO_EVE: str = (
    """
from eve import Eve
from domonic.ext.lander import page

settings = {"DOMAIN": {}}
app = Eve(settings=settings)


@app.route("/hello")
def index():
    return str(page())

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=8000)
"""
)

HELLO_KLEIN: str = (
    """
from klein import Klein
from domonic.ext.lander import page

app = Klein()


@app.route("/")
def index(request):
    request.setHeader(b"content-type", b"text/html; charset=utf-8")
    return str(page())

if __name__ == "__main__":
    app.run("127.0.0.1", 8000)
"""
)


SERVER_SCAFFOLDS: dict[str, dict[str, Any]] = {
    "none": {"packages": [], "template": None},
    "sanic": {"packages": ["sanic==25.12.1"], "template": HELLO_SANIC},
    "flask": {"packages": ["Flask==3.1.3"], "template": HELLO_FLASK},
    "apiflask": {"packages": ["APIFlask==3.1.1"], "template": HELLO_API_FLASK},
    "cherrypy": {"packages": ["CherryPy==18.10.0"], "template": HELLO_CHERRYPY},
    "django": {
        "packages": [
            'Django==5.2.17; python_version < "3.12"',
            'Django==6.1; python_version >= "3.12"',
        ],
        "template": HELLO_DJANGO,
    },
    "django-ninja": {
        "packages": [
            'Django==5.2.17; python_version < "3.12"',
            'Django==6.1; python_version >= "3.12"',
            "django-ninja==1.6.3",
        ],
        "template": HELLO_DJANGO_NINJA,
    },
    "bottle": {"packages": ["bottle==0.13.4"], "template": HELLO_BOTTLE},
    "pyramid": {"packages": ["pyramid==2.1"], "template": HELLO_PYRAMID},
    "werkzeug": {"packages": ["Werkzeug==3.1.8"], "template": HELLO_WERKZEUG},
    "tornado": {"packages": ["tornado==6.5.8"], "template": HELLO_TORNADO},
    "aiohttp": {"packages": ["aiohttp==3.14.3"], "template": HELLO_AIOHTTP},
    "fastapi": {
        "packages": ["fastapi==0.141.1", "uvicorn==0.52.4"],
        "template": HELLO_FAST_API,
    },
    "fasthtml": {"packages": ["python-fasthtml==0.14.12"], "template": HELLO_FASTHTML},
    "starlette": {
        "packages": ["starlette==1.6.0", "uvicorn==0.52.4"],
        "template": HELLO_STARLETTE,
    },
    "blacksheep": {
        "packages": ["blacksheep==2.6.3", "uvicorn==0.52.4"],
        "template": HELLO_BLACKSHEEP,
    },
    "muffin": {
        "packages": ["muffin==2.0.2", "uvicorn==0.52.4"],
        "template": HELLO_MUFFIN,
    },
    "falcon": {"packages": ["falcon==4.3.1"], "template": HELLO_FALCON},
    "baize": {
        "packages": ["baize==0.23.1", "uvicorn==0.52.4"],
        "template": HELLO_BAIZE,
    },
    "esmerald": {
        "packages": ["esmerald==3.9.4", "lilya==0.23.3", "uvicorn==0.52.4"],
        "template": HELLO_ESMERALD,
    },
    "granian": {"packages": ["granian==2.8.1"], "template": HELLO_GRANIAN},
    "emmett": {"packages": ["emmett==2.8.1"], "template": HELLO_EMMETT},
    "eve": {"packages": ["Eve==2.3.1"], "template": HELLO_EVE},
    "klein": {"packages": ["klein==24.8.0"], "template": HELLO_KLEIN},
    "litestar": {
        "packages": ["litestar==2.24.0", "uvicorn==0.52.4"],
        "template": HELLO_LITESTAR,
    },
    "quart": {
        "packages": ["Quart==0.22.0", "Hypercorn==0.18.0"],
        "template": HELLO_QUART,
    },
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
