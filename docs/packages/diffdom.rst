diffdom
=======

``domonic.diffdom`` compares two domonic DOM trees and returns a JSON-safe list
of changes that can be applied or undone later.

This is useful when a server-side render produces a new tree and you only want
to send the structural changes somewhere else.

.. code-block:: python

   from domonic.diffdom import DiffDOM
   from domonic.html import button, div, h1, p

   old = div(h1("Hello"), p("Version one"))
   new = div(h1("Hello"), p("Version two"), button("Save"))

   dd = DiffDOM()
   changes = dd.diff(old, new)

   dd.apply(old, changes)
   assert str(old) == str(new)

.. automodule:: domonic.diffdom
    :members:
    :no-index:
