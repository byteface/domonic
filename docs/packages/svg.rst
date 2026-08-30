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

Inline SVG Icon
---------------

.. code-block:: python

    from domonic.svg import path, svg

    check = svg(
        path(
            _d="M20 6L9 17l-5-5",
            _fill="none",
            _stroke="currentColor",
            _stroke_width="2",
            _stroke_linecap="round",
            _stroke_linejoin="round",
        ),
        _viewBox="0 0 24 24",
        _width="24",
        _height="24",
        _aria_hidden="true",
    )

    print(check)

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

Related Examples
----------------

- :doc:`../guides/examples`
- `examples/svg.html <https://github.com/byteface/domonic/blob/master/examples/svg.html>`_
- `examples/mathml.py <https://github.com/byteface/domonic/blob/master/examples/mathml.py>`_
- `examples/aframe/hello.py <https://github.com/byteface/domonic/blob/master/examples/aframe/hello.py>`_

.. automodule:: domonic.svg
    :members:
    :noindex:
