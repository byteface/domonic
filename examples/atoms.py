import asyncio
import websockets # you gotta 'pip3 install websockets' for this example.
# import ujson as json # test if ujson can dump json faster
import json

import sys
sys.path.insert(0, '..')

from domonic.javascript import *
from domonic.html import *

# run this first. python3 atoms.py
# then open and look at atoms.html while the socket is running

class Particle():

    def __init__(self):
        self.x=0
        self.y=0
        self.width=0
        self.height=0
        self.rotation=0
        self.vx=0
        self.vy=0
        self.damp=0.9
        self.bounce=-0.5
        self.grav=0
        self.wander=0
        self._k=0.2
        self.edges="wrap"
        self._drag=False
        self._oldx=None
        self._oldy=None
        self._turnToPath=False
        self._bounds = {}
        self.set_bounds( {'xMin':0, 'yMin':0, 'yMax': 800, 'xMax': 800} )
        self.maxSpeed = Number.MAX_VALUE

    def set_bounds( self, oBounds ):
        self._bounds['top'] = oBounds['yMin']
        self._bounds['bottom'] = oBounds['yMax']
        self._bounds['left'] = oBounds['xMin']
        self._bounds['right'] = oBounds['xMax']

    def turnToPath( self, bTurn ):
        self._turnToPath = bTurn

    def update( self ):
        if self._drag:
            self.vx = self.x - self._oldx
            self.vy = self.y - self._oldy
            self._oldx = self.x
            self._oldy = self.y

        else:
            self.vx += Math.random() * self.wander - self.wander / 2
            self.vy += Math.random() * self.wander - self.wander / 2
            self.vy += self.grav
            self.vx *= self.damp
            self.vy *= self.damp

            speed = Math.sqrt(self.vx * self.vx + self.vy * self.vy)
            if speed > self.maxSpeed:
                self.vx = self.maxSpeed * self.vx / speed
                self.vy = self.maxSpeed * self.vy / speed

            if self._turnToPath:
                self.rotation = Math.atan2(self.vy, self.vx)

            self.x += self.vx
            self.y += self.vy
            if self.edges == "wrap":
                if self.x > (self._bounds['right'] + self.width/2):
                    self.x = self._bounds['left'] - self.width/2
                elif self.x<self._bounds['left'] - self.width/2:
                    self.x = self._bounds['right'] + self.width/2

                if( self.y > self._bounds['bottom'] + self.height/2):
                    self.y = self._bounds['top'] - self.height/2
                elif (self.y<self._bounds['top'] - self.height/2):
                    self.y = self._bounds['bottom'] + self.height/2

            elif self.edges == "bounce":
                if self.x > (self._bounds['right'] - self.width/2):                   
                    self.x = self._bounds['right'] - self.width/2
                    self.vx *= self.bounce
                elif self.x<(self._bounds['left'] + self.width/2):
                    self.x = self._bounds['left'] + self.width/2
                    self.vx *= self.bounce

                if self.y >(self._bounds['bottom'] - self.height/2):                                 
                    self.y = self._bounds['bottom'] - self.height/2
                    self.vy *= self.bounce
                elif self.y<(self._bounds['top'] + self.height/2):
                    self.y = self._bounds['top'] + self.height/2
                    self.vy *= self.bounce

            # else if self.edges == "remove":
            #     if( self.x > self._bounds.right + self.width/2 || self.x<self._bounds.left - self.width/2 ||
            #        self.y > self._bounds.bottom + self.height/2 || self.y<self._bounds.top - self.height/2){
        
        if Global.isNaN(self.x):
            self.x=self.y=self.vx=self.vy=0




# create and animate some particles

WIDTH = 1000
HEIGHT = 600
ATOM_COUNT = 1000
atoms=[]
      
def init():
  atoms=[]
  for each in range(ATOM_COUNT):
    creatAtom()

def creatAtom():
    p = Particle()
    p.width = Math.random()*1
    p.height = Math.random()*1
    p.grav = Math.random()*150
    p.maxSpeed = 100
    p.damp = 0.1
    p.wander = 30

    p.x = Math.random()*WIDTH
    p.y = Math.random()*HEIGHT
    # p.vx = Math.random()*1000
    p.vy = Math.random()*1000
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
const socket = new WebSocket('ws://192.168.1.134:5555');
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
      context.arc(p.x, p.y, p.width, 0, 2 * Math.PI, false);
      
      // var gradient = context.createRadialGradient(p.x, p.y, p.width, p.x, p.y, 0);
      // gradient.addColorStop( 0, 'black' );
      // gradient.addColorStop( 1, 'white' );
      // context.fillStyle = gradient;

      // context.lineWidth = 1;
      // context.strokeStyle = '#000';
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