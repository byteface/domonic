"""
Send domonic diffDOM patches over a WebSocket.

Run this file, then open the generated ``diffdom_socket.html`` in a browser.
The server keeps rendering new domonic trees and sends only the DOM patches.
"""

import asyncio
import json
import sys
from pathlib import Path

import websockets

sys.path.insert(0, str(Path(__file__).resolve().parents[2]))

from domonic.diffdom import DiffDOM
from domonic.html import (
    body,
    button,
    div,
    h1,
    head,
    html,
    li,
    p,
    pre,
    script,
    span,
    title,
    ul,
)

HOST = "127.0.0.1"
PORT = 5555
OUTPUT = Path(__file__).with_suffix(".html")


def view(count=0):
    return div(
        h1("Live domonic patch stream"),
        p(
            "Server render ",
            span(str(count), _class="count"),
            _class="lede",
        ),
        ul(
            li("Diffs are plain JSON"),
            li("The browser applies only the changed nodes"),
            li("The original domonic tree stays useful server-side"),
        ),
        button(f"Save #{count}", _type="button", _class="primary"),
        _id="app-root",
        _class="panel",
        **{"_data-count": str(count)},
    )


CLIENT_PATCHER = """
const socket = new WebSocket("ws://127.0.0.1:5555");
const app = document.getElementById("app");
const log = document.getElementById("log");

function nodeFromObj(data) {
    if (data.nodeName === "#text") {
        return document.createTextNode(data.data || "");
    }
    if (data.nodeName === "#comment") {
        return document.createComment(data.data || "");
    }
    const node = data.namespaceURI
        ? document.createElementNS(data.namespaceURI, data.nodeName)
        : document.createElement(data.nodeName);
    Object.entries(data.attributes || {}).forEach(([name, value]) => {
        node.setAttribute(name, value);
    });
    (data.childNodes || []).forEach((child) => {
        node.appendChild(nodeFromObj(child));
    });
    return node;
}

function targetFromRoute(root, route) {
    return route.reduce((node, index) => node.childNodes[index], root);
}

function replaceRoot(root, replacement) {
    root.replaceWith(replacement);
    return replacement;
}

function applyPatch(root, change) {
    const route = change.route || [];
    let currentRoot = root;

    if (change.action === "addAttribute" || change.action === "modifyAttribute") {
        targetFromRoute(currentRoot, route).setAttribute(
            change.name,
            change.value ?? change.newValue ?? ""
        );
    } else if (change.action === "removeAttribute") {
        targetFromRoute(currentRoot, route).removeAttribute(change.name);
    } else if (change.action === "modifyTextElement") {
        targetFromRoute(currentRoot, route).textContent = change.newValue;
    } else if (change.action === "modifyComment") {
        targetFromRoute(currentRoot, route).data = change.newValue;
    } else if (change.action === "replaceElement") {
        const replacement = nodeFromObj(change.newValue);
        if (route.length === 0) {
            currentRoot = replaceRoot(currentRoot, replacement);
        } else {
            const parent = targetFromRoute(currentRoot, route.slice(0, -1));
            parent.replaceChild(replacement, parent.childNodes[route[route.length - 1]]);
        }
    } else if (change.action === "addElement" || change.action === "addTextElement") {
        const parent = targetFromRoute(currentRoot, route.slice(0, -1));
        const child = nodeFromObj(change.element);
        parent.insertBefore(child, parent.childNodes[route[route.length - 1]] || null);
    } else if (change.action === "removeElement" || change.action === "removeTextElement") {
        const parent = targetFromRoute(currentRoot, route.slice(0, -1));
        parent.removeChild(parent.childNodes[route[route.length - 1]]);
    }

    return currentRoot;
}

socket.addEventListener("message", (event) => {
    const message = JSON.parse(event.data);
    if (message.type !== "patches") {
        return;
    }
    let root = app.firstElementChild;
    message.patches.forEach((patch) => {
        root = applyPatch(root, patch);
    });
    log.textContent = JSON.stringify(message.patches, null, 2);
});
"""


def render_page():
    page = html(
        head(
            title("domonic diffDOM socket demo"),
        ),
        body(
            div(view(0), _id="app"),
            p(
                "Waiting for patches from ws://127.0.0.1:5555",
                _class="status",
            ),
            pre(_id="log"),
            script(CLIENT_PATCHER),
        ),
    )
    OUTPUT.write_text(str(page), encoding="utf-8")
    return OUTPUT


async def stream_patches(websocket):
    dd = DiffDOM()
    current = view(0)
    count = 0
    while True:
        await asyncio.sleep(1.5)
        count += 1
        next_view = view(count)
        patches = dd.diff(current, next_view)
        dd.apply(current, patches)
        await websocket.send(json.dumps({"type": "patches", "patches": patches}))


async def main():
    output = render_page()
    print(f"Open {output.resolve()} in a browser.")
    print(f"Streaming patches on ws://{HOST}:{PORT}")
    async with websockets.serve(stream_patches, HOST, PORT):
        await asyncio.Future()


if __name__ == "__main__":
    asyncio.run(main())
