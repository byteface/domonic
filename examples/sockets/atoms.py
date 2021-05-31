import asyncio
import websockets # you gotta 'pip3 install websockets' for this example.
import json

import sys
sys.path.insert(0, '../..')

from domonic.javascript import *
from domonic.html import *
from domonic.particles import *

# run this first. python3 atoms.py
# then open and look at atoms.html while the socket is running

# create and animate some particles

WIDTH = 1000
HEIGHT = 600
ATOM_COUNT = 100
atoms=[]
      
def init():
  atoms=[]
  for each in range(ATOM_COUNT):
    creatAtom()

def creatAtom():
    p = Particle(Math.random()*2)
    p.grav = Math.random()*10
    p.maxSpeed = 1000
    p.damp = 0.4
    p.wander = 5

    p.x = Math.random()*WIDTH
    p.y = Math.random()*HEIGHT
    # p.vx = Math.random()*1000
    p.vy = Math.random()*10
    p.set_bounds({'xMin':0, 'yMin':0, 'xMax':WIDTH, 'yMax':HEIGHT})
    atoms.append( p )

def update_atoms():
    for atom in atoms:
        atom.update()

# run the update loop from here.
init()
loop = window.setInterval(update_atoms, 10) # update on own clock. clients see state if request via animfram



# create webpage with a socket connection back to our server so it can get the atom data
page = html(

# make a canvas
style('''
    canvas {
        background: #131c35 linear-gradient(black,#192853, black);
        display:block; position:absolute;
        top:0; left:0; right:0; bottom:0;
    }
    ''',
    _type="text/css"
),

body(canvas(_id="canvas", _width="1000", _height="600")),

# listen on the socket and call draw when we get a message
script('''
const socket = new WebSocket('ws://0.0.0.0:5555');
socket.onmessage = function(event) { atoms = JSON.parse(event.data); draw(); };
'''),

# draw the atoms
script('''
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var WIDTH=canvas.width;
    var HEIGHT=canvas.height;

    function resizeCanvas(){
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      WIDTH=canvas.width;
      HEIGHT=canvas.height;
    }

    function animate() {
        socket.send('!'); // send any old message to trigger socket response. so i can control the framerate
        // draw();
    }

    function draw() {
        context.clearRect(0, 0, WIDTH, HEIGHT);
        // context.globalCompositeOperation = "source-over";
        var i, point;
        for(i = 0; i < atoms.length; i++ ) {
            point = atoms[i];
            context.save();
            context.translate(point.x,point.y);
            context.rotate( point.rotation );
            context.restore();
            // window.console.log(point);
            drawAtom(point,i);
        }
        // context.shadowBlur = 10;
        // context.shadowColor = 'white'
        // context.globalAlpha = 0.1;
        // context.filter = 'blur(2px)';
        // window.requestAnimationFrame(animate);
    }

    function drawAtom(p,i){
      context.beginPath();
      
      context.fillStyle = 'white';
      context.arc(p.x, p.y, 1, 0, 2 * Math.PI, false);
      context.lineWidth = 2;
      context.strokeStyle = '#000';
      context.stroke();
      context.fill();
    }

    var intID;
    function setFramerate(val){
      clearInterval(this.intID)
      this.intID = setInterval( function(){ animate(); }, 1000/val );
      // window.requestAnimationFrame(animate);
    }
    setFramerate(60);
    resizeCanvas();

''')

)

# render a page of particles you can open an look at while the socket server is running
render( page, 'atoms.html' )


# run the socket server
async def update(websocket, path):
    while True:
        # msg = await websocket.recv()
        await websocket.send(json.dumps(atoms, default=vars))

server = websockets.serve(update, '0.0.0.0', 5555)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()



'''
# see if a gevent server is better

from geventwebsocket import WebSocketServer, WebSocketApplication, Resource
class Echo(WebSocketApplication):
    # def on_open(self):
    # print "Connection opened"
    def on_message(self, message):
        self.ws.send(json.dumps(atoms, default=vars))
    # self.ws.send(message)
    # def on_close(self, reason):
    # print reason


WebSocketServer(('0.0.0.0', 5555), Resource({'/': Echo})).serve_forever()
'''


'''
# see if flask-threaded server allows better concurrency. for other windows and devices

from flask import Flask
from flask_threaded_sockets import Sockets, ThreadedWebsocketServer


app = Flask(__name__)
sockets = Sockets(app)


@sockets.route('/')
def echo_socket(ws):
    while not ws.closed:
        message = ws.receive()
        ws.send(json.dumps(atoms, default=vars))


if __name__ == "__main__":
    srv = ThreadedWebsocketServer("0.0.0.0", 5555, app)
    srv.serve_forever()
'''