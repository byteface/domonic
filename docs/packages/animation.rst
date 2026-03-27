animation
=================

Domonic includes a practical first pass of the Web Animations surface.

That includes:

- ``Animation``
- ``AnimationPlaybackEvent``
- ``EffectTiming``
- ``ComputedEffectTiming``
- ``AnimationEffect``
- ``KeyframeEffect``
- ``DocumentTimeline`` on the document side
- ``Element.animate(...)`` wired into the DOM

Quick example:

.. code-block:: python

    from domonic.html import div

    box = div(_id="box")
    animation = box.animate(
        [
            {"opacity": 0, "transform": "translateX(0px)"},
            {"opacity": 1, "transform": "translateX(100px)"},
        ],
        {"duration": 1000, "fill": "forwards"},
    )

    animation.play()

.. automodule:: domonic.animation
    :members:
    :noindex:
