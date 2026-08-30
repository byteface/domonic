Live DOM Updates
================

.. meta::
   :description: Send minimal DOM updates from Python using domonic diffdom, JSON patches, server-side rendering, WebSocket messages, and browser DOM patching.
   :keywords: Python live DOM, WebSocket DOM updates, DOM patch JSON, server-side DOM diff, diffDOM Python, HTML over WebSocket

``domonic.diffdom`` can compare two rendered DOM trees and produce JSON-safe
patch data. That gives you a practical starting point for live HTML updates:
render on the server, diff against the previous tree, send only the changes.

Create a Patch
--------------

.. code-block:: python

   import json

   from domonic.diffdom import DiffDOM
   from domonic.html import button, div, h1, p

   old = div(h1("Inbox"), p("0 messages"))
   new = div(h1("Inbox"), p("1 message"), button("Open"))

   dd = DiffDOM()
   changes = dd.diff(old, new)

   print(json.dumps(changes, indent=2))

Apply a Patch
-------------

.. code-block:: python

   dd.apply(old, changes)
   assert str(old) == str(new)

Undo a Patch
------------

.. code-block:: python

   dd.undo(old, changes)
   print(old)

WebSocket Shape
---------------

The server-side shape is intentionally plain.

.. code-block:: python

   import json

   async def publish_dom_update(websocket, previous, current):
       changes = DiffDOM().diff(previous, current)
       await websocket.send(json.dumps(changes))

Browser Receiver
----------------

On the browser side you can apply the patch with a small JavaScript patcher that
understands the same change data.

.. code-block:: javascript

   const socket = new WebSocket("ws://localhost:8765");

   socket.addEventListener("message", event => {
     const changes = JSON.parse(event.data);
     applyPatches(document.body, changes);
   });

See ``examples/sockets/diffdom_socket.py`` for a complete Python example.

