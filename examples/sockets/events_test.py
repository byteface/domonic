import asyncio
import websockets  # you gotta 'pip3 install websockets' for this example.
import json

import sys

sys.path.insert(0, "../..")

from domonic.javascript import *
from domonic.html import *
from domonic.components import Websocket
from domonic.events import *
from domonic.CDN import *


# generate the webpage that makes the socket connection back to our server
page = html(
    head(title("Test Capturing Browser Events")),
    script(_src="https://code.jquery.com/jquery-3.5.1.min.js"),
    body(
        Websocket(drag_events=True, hashchange_events=True, wheel_events=True, clipboard_events=True),
        # canvas(_id="canvas", _width="500", _height="500"),
        div(_class="dropzone",).html(
            div(
                _id="draggable",
                _draggable="true",
                _ondragstart="event.dataTransfer.setData('text/plain',null)",
            ).html("This div is draggable")
        ),
        div(_class="dropzone"),
    ),
)
# render the page you need to visit while the socket server is running
render(page, "events.html")


# run an update loop from here.
somedata = {}
# def update():
#     somedata = {}
# loop = window.setInterval(update, 15)


class BrowserEventHandler(EventDispatcher, GlobalEventHandler):
    def __init__(self):
        super().__init__(self)
        self.addEventListener(KeyboardEvent.KEYDOWN, self.on_keydown)
        self.addEventListener(KeyboardEvent.KEYUP, self.on_keyup)

        self.addEventListener(MouseEvent.MOUSEMOVE, self.on_mousemove)
        self.addEventListener(MouseEvent.MOUSEDOWN, self.on_mousedown)
        self.addEventListener(MouseEvent.MOUSEUP, self.on_mouseup)

        self.addEventListener(DragEvent.DRAG, self.ondrag)
        self.addEventListener(DragEvent.END, self.ondragend)
        self.addEventListener(DragEvent.ENTER, self.ondragenter)
        self.addEventListener(DragEvent.EXIT, self.ondragexit)
        self.addEventListener(DragEvent.LEAVE, self.ondragleave)
        self.addEventListener(DragEvent.OVER, self.ondragover)
        self.addEventListener(DragEvent.START, self.ondragstart)
        self.addEventListener(DragEvent.DROP, self.ondrop)

        self.addEventListener(WheelEvent.WHEEL, self.onwheel)

        self.addEventListener(HashChangeEvent.CHANGE, self.onhashchange)

        # self.addEventListener(ClipboardEvent.CUT, self.oncut)
        # self.addEventListener(ClipboardEvent.COPY, self.oncopy)
        # self.addEventListener(ClipboardEvent.PASTE, self.onpaste)

    # def oncut(self, event):
    #     print(event)

    # def oncopy(self, event):
    #     print(event)

    # def onpaste(self, event):
    #     print(event.clipboardData)

    def onwheel(self, event):
        if event.deltaY > 0:
            print("scrolling up")
        else:
            print("scrolling down")

    def onhashchange(self, event):
        print("The url used to be:", event.oldURL)
        print("Now the url is:", event.newURL)

    def ondrag(self, event):
        print(event)
        pass

    def ondragend(self, event):
        print(event)
        pass

    def ondragenter(self, event):
        print(event)
        pass

    def ondragexit(self, event):
        print(event)
        pass

    def ondragleave(self, event):
        print(event)
        pass

    def ondragover(self, event):
        print(event)
        pass

    def ondragstart(self, event):
        print(event)
        pass

    def ondrop(self, event):
        print(event)
        pass

    def on_keydown(self, event):
        print("a key was pressed", event)
        print(event.key)

    def on_keyup(self, event):
        print("a key was released")
        print(event.key)

    def on_mousemove(self, event):
        # print('mousemove', event, event.x, event.y)
        pass

    def on_mousedown(self, event):
        print("mousedown", event, event.x, event.y)

    def on_mouseup(self, event):
        print("on_mouseup", event, event.x, event.y)


# create a handler for the browser events
event_handler = BrowserEventHandler()


# run the socket server
async def update(websocket, path):
    while True:
        msg = await websocket.recv()
        evt = Websocket.get_event(msg)
        if evt is not None:
            global event_handler
            event_handler.dispatchEvent(evt)
        await websocket.send(json.dumps(somedata, default=vars))


server = websockets.serve(update, "0.0.0.0", 5555)
asyncio.get_event_loop().run_until_complete(server)
asyncio.get_event_loop().run_forever()
