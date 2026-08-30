tween
=================

.. meta::
   :description: Python tweening and easing equations with Robert Penner easing, timers, animation helpers, and game-style interpolation.
   :keywords: Python tween, easing equations, Robert Penner, animation interpolation, game tweening, lerp, setInterval

For tweening, domonic includes a port of Robert Penner's easing equations and helpers to use them.

.. code-block :: python

    import time

    from domonic.lerpy.easing import *
    from domonic.lerpy.tween import *

    someObj = {'x':0,'y':0,'z':0}
    twn = Tween( someObj, { 'x':10, 'y':5, 'z':3 }, 6, Linear.easeIn )
    twn.start()

    time.sleep(1)
    print(someObj)
    time.sleep(1)
    print(someObj)
    time.sleep(1)
    print(someObj)
    # twn.pause()
    time.sleep(1)
    print(someObj)
    time.sleep(1)
    # twn.unpause()
    print(someObj)
    time.sleep(1)
    print(someObj)
    time.sleep(1)
    print(someObj)


``equations`` can be an array with different tweens per property::

    # twn.equations = [Expo.easeOut, Expo.easeIn, {ease: Back.easeOut, a: 0.5, b: 1.5}]

Note: tweens use domonic's ``setInterval``, which runs on a thread and is not affected by ``sleep``.



Easing equations you can pass in:
---------------------------------

Back.easeIn
Bounce.easeIn
Circ.easeIn
Cubic.easeIn
Elastic.easeIn
Expo.easeIn
Linear.easeIn
Quad.easeIn
Quart.easeIn
Quint.easeIn
Sine.easeIn

Back.easeOut
Bounce.easeOut
Circ.easeOut
Cubic.easeOut
Elastic.easeOut
Expo.easeOut
Linear.easeOut
Quad.easeOut
Quart.easeOut
Quint.easeOut
Sine.easeOut

Back.easeInOut
Bounce.easeInOut
Circ.easeInOut
Cubic.easeInOut
Elastic.easeInOut
Expo.easeInOut
Linear.easeInOut
Quad.easeInOut
Quart.easeInOut
Quint.easeInOut
Sine.easeInOut


get_timer
---------------------------------

The tween engine uses a timer method that shows how long the game has been running.

.. code-block :: python

    from domonic.lerpy import get_timer
    print(get_timer())



.. automodule:: domonic.lerpy.tween
    :members:
    :noindex:


.. automodule:: domonic.lerpy.easing
    :members:
    :noindex:
