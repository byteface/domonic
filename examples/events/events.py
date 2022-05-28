import asyncio
import websockets  # you gotta 'pip3 install websockets' for this example.
import json

import sys

sys.path.insert(0, "../..")

from domonic.javascript import *
from domonic.html import *
from domonic.events import *


# create webpage with a socket connection back to our server so it can get mouse events
page = html(
    body(h1("somepage"), div("Move the mouse around and click to see output on the server.", _id="content")),
    # listen on the socket and call draw when we get a message
    script(
        """
const socket = new WebSocket('ws://0.0.0.0:5555');
//socket.onmessage = function(event) { atoms = JSON.parse(event.data); draw(); };
"""
    ),
    # track all mouse events
    script(
        """
var eventCount = 0;
var eventProperty = [];
var TrackMouse = function (mouseEvent) {
    console.log(mouseEvent);
    eventProperty[eventCount++] = {
        type: 'mouse', ts: Date.now(),
        x: mouseEvent.x, y: mouseEvent.y
    };
    socket.send( '{"x":' + mouseEvent.x + ', "y":' + mouseEvent.y + '}' );
};

document.addEventListener('click', TrackMouse);
"""
    ),
)

# render a page to capture events on
render(page, "events.html")


def on_page_clicked(evt):
    print("the page was just clicked", evt)
    print("mouseX", evt.x)
    print("mouseY", evt.y)
    # content = page.getElementById('content')
    # print(content)
    # content.append( f"mouseX:{evt.x} mouseY:{evt.y}" )
    # TODO - send msg so js can redraw the div
    # mything = {'x':0,'y':0}
    # twn = Tween( mything, { 'x':evt.x, 'y':evt.y }, 3 )
    # twn.equations = Linear.easeOut
    # twn.start()


page.addEventListener(MouseEvent.CLICK, on_page_clicked)


# run the socket server
async def update(websocket, path):
    while True:
        msg = await websocket.recv()
        print(msg)

        # catch an event from the browser via a socket
        # dispatch it on our own 'server dom'
        m = MouseEvent(MouseEvent.CLICK)
        event = json.loads(msg)
        m.x = event["x"]
        m.y = event["y"]
        page.dispatchEvent(m)

        await websocket.send("event receieved")


server = websockets.serve(update, "0.0.0.0", 5555)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()


"""
# dont really need a socket for events. can just create and endpoint and capture them i.e
# then in the js make an ajax request to the endpoint

from flask import Flask
app = Flask(__name__)

@route('/events')
def events(evt):
    // do stuff

"""
