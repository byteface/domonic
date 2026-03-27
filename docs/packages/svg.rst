svg
=================

Domonic ships a broad SVG tag surface that stays aligned with the rest of the DOM.

That means SVG nodes participate in the same tree, event, and manipulation APIs as HTML elements.

.. code-block:: python

    from domonic.svg import svg, circle

    icon = svg(
        circle(_cx="50", _cy="50", _r="40", _fill="gold"),
        _width="100",
        _height="100",
    )

    print(icon)

.. automodule:: domonic.svg
    :members:
    :noindex:
