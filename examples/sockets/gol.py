import asyncio
import websockets # you gotta 'pip3 install websockets' for this example.
import json

import sys
sys.path.insert(0, '../..')

from domonic.javascript import *
from domonic.html import *

WIDTH = 75
HEIGHT = 75

randboo = lambda : 1 if Math.round(Math.random() * 2) == 1 else 0

gridOld = [[randboo()] * WIDTH for n in range(HEIGHT)]
gridNew = [[randboo()] * WIDTH for n in range(HEIGHT)]

xPos = 0
yPos = 0


def update_cell(grid, x, y):  # apply the rules
    score = 0
    for ny in range(y - 1, y + 2):
        for nx in range(x - 1, x + 2):
            if(ny >= 0 and nx >= 0 and ny < WIDTH and nx < HEIGHT and (ny != y or nx != x)):
                if(grid[ny][nx] == 1):
                    score += 1
    if(grid[y][x] == 1):
        return 1 if (score == 2 or score == 3) else 0
    return 1 if (score == 3) else 0


def update_grid():
    yPos=-1  # Putting the new squares in girdNew based off of gridOld
    for y in gridOld:
        yPos+=1
        xPos=-1
        for x in y:
            xPos+=1
            gridNew[yPos][xPos] = update_cell(gridOld, xPos, yPos)
    yPos=-1
    for y in gridNew:
        yPos += 1
        xPos =- 1
        for x in y:
            xPos+=1
            gridOld[yPos][xPos] = gridNew[yPos][xPos]

# run the update loop from here.
# loop = window.setInterval(update_grid, 15)  # update on own clock. clients see state if request via animfram


# create webpage with a socket connection back to our server so it can get the atom data
page = html(
head(title("Conway's Game of Life")),
style('''
    canvas {
        display:block; position:absolute;
        top:0; left:0; right:0; bottom:0;
    }
    ''',
    _type="text/css"
),

body(
    canvas(_id="canvas", _width="500", _height="500"),

# listen on the socket and call draw when we get a message
script('''
const socket = new WebSocket('ws://0.0.0.0:5555');
socket.onmessage = function(event) { grid = JSON.parse(event.data); draw(); };
socket.send('!');
'''),

# draw the grid
script('''
    var canvas = document.getElementById('canvas');
    var context = canvas.getContext('2d');
    var WIDTH=canvas.width;
    var HEIGHT=canvas.height;

    var CELLSIZE = 5;

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
        //console.log(grid);
        var x, y;
        for(x = 0; x < grid.length; x++) {
            row = grid[x];
            for(y = 0; y<row.length; y++) {
                //drawRect(x*CELLSIZE,y*CELLSIZE, grid[x][y]);
                drawCell(x*CELLSIZE,y*CELLSIZE, grid[x][y]);

            }
        }
        socket.send('!');
    }

    /*
    function drawRect(x, y, state){
        context.beginPath();
        if(state === 1){
            context.fillStyle = 'black';
        }else{
            context.fillStyle = 'white';
        }
        //context.lineWidth = 2;
        //context.strokeStyle = '#000';
        //context.stroke();
        //context.stroke();
        //context.rect(x, y, CELLSIZE, CELLSIZE);
        context.fillRect(x, y, CELLSIZE, CELLSIZE);
        context.fill();
    }
    */

    function drawCell(x, y, state){
        context.beginPath();
        if(state === 1){
            context.fillStyle = 'black';
        }else{
            context.fillStyle = 'white';
        }
        context.arc(x, y, 1, 0, 2 * Math.PI, false);
        context.lineWidth = 2;
        context.strokeStyle = '#000';
        context.stroke();
        context.fill();
    }

    /*
    var intID;
    function setFramerate(val){
      clearInterval(this.intID)
      this.intID = setInterval( function(){ animate(); }, 1000/val );
      // window.requestAnimationFrame(animate);
    }
    setFramerate(60);
    resizeCanvas();
    */

''')

)
)

# render the page you need to visit while the socket server is running
render(page, 'gol.html')

# run the socket server
async def update(websocket, path):
    while True:
        update_grid()
        await websocket.send(json.dumps(gridNew, default=vars))
        msg = await websocket.recv()
        await websocket.send(json.dumps(gridNew, default=vars))

server = websockets.serve(update, '0.0.0.0', 5555)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
