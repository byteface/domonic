import asyncio
import json
import sys

import websockets  # you gotta 'pip3 install websockets' for this example.

sys.path.insert(0, "../..")

from domonic.CDN import *
from domonic.components import Websocket
from domonic.events import *
from domonic.html import *
from domonic.javascript import *

# generate the webpage that makes the socket connection back to our server
page = html(
    head(title("Test Capturing Browser Events")),
    script(_src=CDN_JS.JQUERY),
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

    def record(self, event, name=None):
        event_name = name or getattr(event, "type", event.__class__.__name__)
        counts = somedata.setdefault("counts", {})
        counts[event_name] = counts.get(event_name, 0) + 1
        somedata["last_event"] = event_name

    # def oncut(self, event):
    #     print(event)

    # def oncopy(self, event):
    #     print(event)

    # def onpaste(self, event):
    #     print(event.clipboardData)

    def onwheel(self, event):
        self.record(event)
        if event.deltaY > 0:
            print("scrolling up")
        else:
            print("scrolling down")

    def onhashchange(self, event):
        self.record(event)
        somedata["hash"] = {"old": event.oldURL, "new": event.newURL}
        print("The url used to be:", event.oldURL)
        print("Now the url is:", event.newURL)

    def ondrag(self, event):
        self.record(event)
        print(event)

    def ondragend(self, event):
        self.record(event)
        print(event)

    def ondragenter(self, event):
        self.record(event)
        print(event)

    def ondragexit(self, event):
        self.record(event)
        print(event)

    def ondragleave(self, event):
        self.record(event)
        print(event)

    def ondragover(self, event):
        self.record(event)
        print(event)

    def ondragstart(self, event):
        self.record(event)
        print(event)

    def ondrop(self, event):
        self.record(event)
        print(event)

    def on_keydown(self, event):
        self.record(event)
        print("a key was pressed", event)
        print(event.key)

    def on_keyup(self, event):
        self.record(event)
        print("a key was released")
        print(event.key)

    def on_mousemove(self, event):
        somedata["mouse"] = {"x": event.x, "y": event.y}

    def on_mousedown(self, event):
        self.record(event)
        print("mousedown", event, event.x, event.y)

    def on_mouseup(self, event):
        self.record(event)
        print("on_mouseup", event, event.x, event.y)


# create a handler for the browser events
event_handler = BrowserEventHandler()


# run the socket server
async def update(websocket):
    while True:
        msg = await websocket.recv()
        evt = Websocket.get_event(msg)
        if evt is not None:
            global event_handler
            event_handler.dispatchEvent(evt)
        await websocket.send(json.dumps(somedata, default=vars))

async def main():
    async with websockets.serve(update, "0.0.0.0", 5555):
        await asyncio.Future()


asyncio.run(main())
