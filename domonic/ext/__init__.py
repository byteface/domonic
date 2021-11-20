"""
    domonic.ext
    ====================================

    This dir is for extending domonic to be useable with other python libs.

"""

# HELLO WORLDS - hello world code for other libs

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
    app.run()
"""

HELLO_CHERRYPY: str = """
import cherrypy
from domonic.html import *

class HelloWorld(object):

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


def get_hello_world(server):
    hello_words = {
        'flask': HELLO_FLASK,
        'cherrypy': HELLO_CHERRYPY,
        'sanic': HELLO_SANIC,
        'bottle': HELLO_BOTTLE,
        'aiohttp': HELLO_AIOHTTP,
        'tornado': HELLO_TORNADO,
        'werkzeug': HELLO_WERKZEUG
    }
    if server in hello_words:
        return hello_words[server]
    else:
        return None
