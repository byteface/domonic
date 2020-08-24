from domonic.javascript import *
from domonic.JSON import *

# running a loop
'''
x=0

def hi(inc):
	global x
	x = (x+inc)
	print(x)

test = window.setInterval(1000, hi, 1)
import time
time.sleep(5)
window.clearInterval(test)
print(f"Final value of x:{x}")
'''

# parsing data
'''
jsons = '[{"id":"01","name": "some item"},{"id":"02","name": "some other item"}]'
json_data = JSON.parse(jsons)
mytable = JSON.tablify(json_data)
print(mytable)
'''


# rendering with vapory
'''
from vapory import *

camera = Camera( 'location', [0,2,-10], 'look_at', [0,1,2] )
light = LightSource( [2,4,-30], 'color', [1,1,1], 'shadowless' )
sphere = Sphere( [0,1,2], 2, Texture( Pigment( 'color', [1,0,1] )))
scene = Scene( camera, objects= [light, sphere])
x = 0

def randy(min,max):
	return Math.random()*min + Math.random()*max

def animate():
	global x, camera, light, scene
	x = (x+1)
	
	objects = [light]

	for i in range(0,10000):
		sphere = Sphere( [randy(-10,10),randy(-10,10),Math.random()*100], 0.01, Texture( Pigment( 'color', [1,1,1] )))
		objects.append(sphere)
	
	scene = Scene(camera, objects=objects)
	scene.render(f"spheres{x}.png", width=1200, height=780)


test = window.setInterval(0.0001, animate) # max_iterations
import time
time.sleep(10)
window.clearInterval(test)
'''
