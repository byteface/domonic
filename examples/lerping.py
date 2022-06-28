import sys

sys.path.insert(0, "..")

import time

from domonic.lerpy.easing import *
from domonic.lerpy.tween import *

someObj = {"x": 0, "y": 0, "z": 0}

# tween our object to have these values over 8 seconds
twn = Tween(someObj, {"x": 10, "y": 5, "z": 3}, 6, Linear.easeIn)

# user the Linear.easeOut equation
# twn.equations = Linear.easeNone

# twn.equations = Back.easeIn
# twn.equations = Bounce.easeIn
# twn.equations = Circ.easeIn
# twn.equations = Cubic.easeIn
# twn.equations = Elastic.easeIn
# twn.equations = Expo.easeIn
# twn.equations = Linear.easeIn
# twn.equations = Quad.easeIn
# twn.equations = Quart.easeIn
# twn.equations = Quint.easeIn
# twn.equations = Sine.easeIn

# twn.equations = Back.easeOut
# twn.equations = Bounce.easeOut
# twn.equations = Circ.easeOut
# twn.equations = Cubic.easeOut
# twn.equations = Elastic.easeOut
# twn.equations = Expo.easeOut
# twn.equations = Linear.easeOut
# twn.equations = Quad.easeOut
# twn.equations = Quart.easeOut
# twn.equations = Quint.easeOut
# twn.equations = Sine.easeOut

# twn.equations = Back.easeInOut
# twn.equations = Bounce.easeInOut
# twn.equations = Circ.easeInOut
# twn.equations = Cubic.easeInOut
# twn.equations = Elastic.easeInOut
# twn.equations = Expo.easeInOut
# twn.equations = Linear.easeInOut
# twn.equations = Quad.easeInOut
# twn.equations = Quart.easeInOut
# twn.equations = Quint.easeInOut
# twn.equations = Sine.easeInOut

# the x prop uses Expo.easeOut y and z use Expo.easeIn
# twn.equations = [ Expo.easeOut, Expo.easeIn ]

# each has own easing. z has a complex equation assigned
# twn.equations = [ Expo.easeOut, Expo.easeIn, { ease:Back.easeOut, a:0.5, b:1.5 } ]

print(twn)

# twn.loop = True

twn.start()
# print(twn)

print("===")

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

print("===")
