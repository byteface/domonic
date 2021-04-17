import sys
sys.path.insert(0, '..')

from domonic.lerpy.tween import *
from domonic.lerpy.easing import *

import time

someObj = {'x':0,'y':0,'z':0}

# tween our object to have these values over 8 seconds
twn = Tween( someObj, { 'x':10, 'y':5, 'z':3 }, 8 )

# user the Linear.easeOut equation
twn.equations = Linear.easeNone
# twn.equations = Cubic.easeInOut


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

twn.pause()

time.sleep(1)
print(someObj)
time.sleep(1)

twn.unpause()

print(someObj)
time.sleep(1)
print(someObj)
time.sleep(1)
print(someObj)

print("===")