import asyncio
import websockets # you gotta 'pip3 install websockets' for this example.
import json

import sys
sys.path.insert(0, '../..')

from domonic.javascript import *
from domonic.html import *
from domonic.particles import *

# run this first. python3 atoms3d.py
# then open and look at atoms3d.html while the socket is running

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
    p = Particle3D(Math.random()*2)
    p.grav = Math.random()*10
    p.maxSpeed = 1000
    p.damp = 0.4
    p.wander = 5

    p.x = Math.random()*WIDTH
    p.y = Math.random()*HEIGHT
    p.z = -100 + Math.random()*HEIGHT
    # p.vx = Math.random()*1000
    p.vy = Math.random()*10
    p.vz = Math.random()*100

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
    }

    function drawAtom(p,i){
      context.beginPath();
      
      context.fillStyle = 'white';
      context.arc(p.x, p.y, p.z, 0, 2 * Math.PI, false);
      
      // var gradient = context.createRadialGradient(p.x, p.y, p.width*p.z, p.x, p.y, 0);
      // gradient.addColorStop( 0, 'black' );
      // gradient.addColorStop( 1, 'white' );
      // context.fillStyle = gradient;

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
render( page, 'atoms3d.html' )


# run the socket server
async def update(websocket, path):
    while True:
        # msg = await websocket.recv()
        await websocket.send(json.dumps(atoms, default=vars))

server = websockets.serve(update, '0.0.0.0', 5555)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
