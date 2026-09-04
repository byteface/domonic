svg
=================

.. meta::
   :description: Generate SVG with Python, build SVG icons, charts, paths, gradients, symbols, and inline vector markup using domonic.
   :keywords: Python SVG, SVG generator, inline SVG, SVG icons, vector graphics, create SVG with Python, SVG DOM

Domonic ships a broad SVG tag surface that stays aligned with the rest of the
DOM. SVG nodes render to markup and participate in the same tree, event, and
mutation APIs as HTML elements.

Basic SVG
---------

.. code-block:: python

    from domonic.svg import circle, svg

    icon = svg(
        circle(_cx="50", _cy="50", _r="40", _fill="gold"),
        _width="100",
        _height="100",
        _viewBox="0 0 100 100",
    )

    print(icon)
    # <svg width="100" height="100" viewBox="0 0 100 100"><circle cx="50" cy="50" r="40" fill="gold"></circle></svg>

Inline SVG Icon
---------------

.. code-block:: python

    from domonic.svg import path, svg

    check = svg(
        path(
            _d="M20 6L9 17l-5-5",
            _fill="none",
            _stroke="currentColor",
            **{"_stroke-width": "2", "_stroke-linecap": "round", "_stroke-linejoin": "round"},
        ),
        _viewBox="0 0 24 24",
        _width="24",
        _height="24",
        **{"_aria-hidden": "true"},
    )

    print(check)
    # <svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M20 6L9 17l-5-5" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"></path></svg>

A Python identifier can't contain a hyphen, so hyphenated attributes such as
``stroke-width`` or ``aria-hidden`` need the ``**{"_name": value}`` form (the
same pattern used for ``data-*`` attributes in :doc:`html`) -- a plain
``_stroke_width=`` keyword argument renders literally as ``stroke_width``,
which browsers do not recognise.

SVG Bar Chart
-------------

.. code-block:: python

    from domonic.svg import rect, svg, text

    values = [12, 30, 18]
    chart = svg(
        *[
            rect(_x=i * 32, _y=40 - value, _width=24, _height=value)
            for i, value in enumerate(values)
        ],
        text("Visits", _x=0, _y=58),
        _viewBox="0 0 120 64",
    )

    print(chart)
    # <svg viewBox="0 0 120 64"><rect x="0" y="28" width="24" height="12"></rect><rect x="32" y="10" width="24" height="30"></rect><rect x="64" y="22" width="24" height="18"></rect><text x="0" y="58">Visits</text></svg>

Mix SVG and HTML
----------------

.. code-block:: python

    from domonic.html import button
    from domonic.svg import circle, svg

    save_button = button(
        svg(circle(_cx=8, _cy=8, _r=6), _viewBox="0 0 16 16"),
        " Save",
        _type="button",
    )

    print(save_button)
    # <button type="button"><svg viewBox="0 0 16 16"><circle cx="8" cy="8" r="6"></circle></svg> Save</button>

Measuring Text and Geometry
---------------------------

``getBBox()`` works off the DOM. Leaf shapes read their attributes, ``<text>``
and ``<tspan>`` are measured with a bundled Helvetica metrics table (keyed by
the computed ``font-size`` / ``font-weight``), and containers such as ``<g>``
return the union of their descendants with each child ``transform`` applied.

.. code-block:: python

    from domonic.svg import g, text

    label = text("Alice", _x=0, _y=0)
    label.getBBox().width          # ~34.7 at the 16px default
    label.getComputedTextLength()  # advance width
    label.getSubStringLength(0, 3) # width of "Ali"

    box = g(label).getBBox()       # unions children

    label.getScreenCTM()           # composes ancestor transform attributes

``getScreenCTM()`` reads a ``transform`` attribute the same way a browser
parses it: each function in the list composes left-to-right into one
``DOMMatrix``:

.. code-block :: python

    from domonic.svg import g, text

    label = text("Alice", _x=0, _y=0)
    group = g(label, _transform="translate(10,20) rotate(90)")
    print(label.getScreenCTM())
    # matrix(0, 1, -1, 0, 10, 20)

Elements created via ``document.createElementNS(SVG_NAMESPACE, ...)`` or a
``d3.selection`` ``.append()`` get the same geometry API as the
``domonic.svg.*`` factories. The metrics are a sans-serif proxy, not a shaping
engine -- good enough for layout, not pixel-exact.

Related Examples
----------------

- :doc:`../guides/examples`
- `examples/svg.html <https://github.com/byteface/domonic/blob/master/examples/svg.html>`_
- `examples/mathml.py <https://github.com/byteface/domonic/blob/master/examples/mathml.py>`_
- `examples/aframe/hello.py <https://github.com/byteface/domonic/blob/master/examples/aframe/hello.py>`_

.. automodule:: domonic.svg
    :members:
    :noindex:
