animation
=================

.. meta::
   :description: Web Animations API style helpers in Python with Animation, KeyframeEffect, timelines, playback events, and Element.animate.
   :keywords: Python animation, Web Animations API, Element animate, KeyframeEffect, DOM animation

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

Inspect Timing
--------------

.. code-block:: python

    from domonic.animation import KeyframeEffect
    from domonic.html import div

    effect = KeyframeEffect(
        div(_id="panel"),
        [{"opacity": 0}, {"opacity": 1}],
        {"duration": 250, "delay": 50},
    )

    print(effect.getTiming().duration)
    print(effect.getComputedTiming().endTime)

.. automodule:: domonic.animation
    :members:
    :noindex:
