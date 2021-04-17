Domonic: tween
=================

For tweening there's now a port of the penner equations and function to use them.

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


 equations can be an array with different tweens per property
 # twn.equations = [ Expo.easeOut, Expo.easeIn, { ease:Back.easeOut, a:0.5, b:1.5 } ]


Note* Tweens use a domonic 'setInterval' which runs on a thread so won't be affected by sleep.



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


.. automodule:: domonic.lerpy.tween
    :members:
    :noindex:


.. automodule:: domonic.lerpy.easing
    :members:
    :noindex:
