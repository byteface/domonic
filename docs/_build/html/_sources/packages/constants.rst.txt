Domonic: constants
==================

domonic.constants contains references to make your life a little easier.


Color
----------------

.. code-block :: python

	from domonic.constants.color import Color
	print(Color.shit)

Color is also a util with a few methods...

.. code-block :: python

	c1 = Color('#ff00ff')
	print(c1)

	c2 = Color(255,255,255)
	print(c1)


.. autoclass:: domonic.constants.color.Color
    :members:
    :noindex:


Char
----------------

.. code-block :: python

	from domonic.constants.entities import Char
	print(Char.AMPERSAND)


.. autoclass:: domonic.constants.entities.Char
    :members:
    :noindex:


KeyCode
----------------

.. code-block :: python

	from domonic.constants.keyboard import KeyCode
	print(KeyCode.DOWN)
	print(KeyCode.ENTER)


.. autoclass:: domonic.constants.keyboard.KeyCode
    :members:
    :noindex:
