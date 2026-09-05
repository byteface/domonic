diffdom
=======

.. meta::
   :description: Python DOM diff and patch utilities for server-side rendering, WebSocket updates, live HTML, and JSON-safe DOM patches.
   :keywords: Python DOM diff, DOM patch, server-side rendering, WebSocket DOM updates, HTML diff, virtual DOM, morphdom, diffDOM

``domonic.diffdom`` compares two domonic DOM trees and returns a JSON-safe list
of patch operations. You can apply the patch to mutate an existing tree, undo it
later, or send the patch somewhere else.

This is useful for Python server-side rendering, live HTML, dashboard updates,
WebSocket DOM updates, DOM testing, and experiments that need a real mutable DOM
rather than a string diff.

Basic DOM Diff
--------------

.. code-block:: python

   from domonic.diffdom import DiffDOM
   from domonic.html import button, div, h1, p

   old = div(h1("Hello"), p("Version one"))
   new = div(h1("Hello"), p("Version two"), button("Save"))

   dd = DiffDOM()
   changes = dd.diff(old, new)

   for change in changes:
       print(change)

   dd.apply(old, changes)
   assert str(old) == str(new)
   # [{'action': 'modifyTextElement', 'route': [1, 0], 'oldValue': 'Version one', 'newValue': 'Version two'},
   #  {'action': 'addElement', 'route': [2], 'element': {'nodeName': 'button', ...}}]

Send DOM Patches Over a WebSocket
---------------------------------

The diff is plain data, so it can be serialized as JSON and streamed to another
process, a browser, or a test harness.

.. code-block:: python

   import json

   from domonic.diffdom import DiffDOM
   from domonic.html import div, h1, p

   old = div(h1("Hello"), p("Version one"))
   new = div(h1("Hello"), p("Version two"))

   changes = DiffDOM().diff(old, new)
   payload = json.dumps(changes)

   # websocket.send(payload)
   print(payload)
   # [{"action": "modifyTextElement", "route": [1, 0], "oldValue": "Version one", "newValue": "Version two"}]

Undo a Patch
------------

.. code-block:: python

   from domonic.diffdom import DiffDOM
   from domonic.html import div, h1, p

   old = div(h1("Hello"), p("Version one"))
   new = div(h1("Hello"), p("Version two"))
   dd = DiffDOM()

   before = str(old)
   changes = dd.diff(old, new)

   dd.apply(old, changes)
   dd.undo(old, changes)

   assert str(old) == before

Compare Rendered Components
---------------------------

.. code-block:: python

   from domonic.diffdom import DiffDOM
   from domonic.html import article, h2, p

   def card(title, body):
       return article(h2(title), p(body), _class="card")

   current = card("Status", "Queued")
   next_render = card("Status", "Shipped")

   changes = DiffDOM().diff(current, next_render)
   assert changes[0]["action"] == "modifyTextElement"

Use Cases
---------

- Python server-side DOM rendering with minimal browser updates
- HTML-over-WebSocket apps and live dashboards
- Snapshot tests for generated HTML and component rendering
- JSON-safe DOM patches that can be logged, stored, replayed, or undone

Related Examples and Guides
---------------------------

- :doc:`../guides/live-dom-updates`
- `examples/diffdom.py <https://github.com/byteface/domonic/blob/master/examples/diffdom.py>`_
- `examples/sockets/diffdom_socket.py <https://github.com/byteface/domonic/blob/master/examples/sockets/diffdom_socket.py>`_

.. automodule:: domonic.diffdom
    :members:
    :no-index:
