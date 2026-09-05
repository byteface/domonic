geom
=================

.. meta::
   :description: Geometry helpers for Python games, SVG, canvas-style drawing, particles, shapes, vectors, Vec2 and Vec3 maths.
   :keywords: Python geometry, Vec2, Vec3, vector math, shapes, particles, SVG geometry, game math

``domonic.geom`` contains small geometry primitives used by games, animation,
SVG experiments, and canvas-style examples.

Vectors
-------

.. code-block :: python

	from domonic.geom.vec2 import vec2
	from domonic.geom.vec3 import vec3

	position = vec2(10, 20)
	velocity = vec2(2, -1)
	print(position + velocity)
	# 12 19

	point = vec3(1, 2, 3)
	print(point.distance(vec3(3, 2, 1)))
	# 2.8284271247461903

Shapes
------

.. code-block :: python

	from domonic.geom.shape import Circle, Rect

	hit_area = Rect(0, 0, 120, 40)
	cursor = Circle(24, 24, 10)

	print(hit_area.get_bottom_right())
	# (120, 40)
	print(cursor.area)
	# 314.1592653589793

Particles
---------

.. code-block :: python

	from domonic.geom.particles import Particle

	particle = Particle(size=2, x=10, y=20)
	particle.vx = 1
	particle.vy = -0.5
	particle.update()
	print(particle.x, particle.y)
	# 10.9 19.55

.. automodule:: domonic.geom
    :members:
    :noindex:

.. automodule:: domonic.geom.shape
    :members:
    :noindex:

.. automodule:: domonic.geom.vec2
    :members:
    :noindex:

.. automodule:: domonic.geom.vec3
    :members:
    :noindex:
