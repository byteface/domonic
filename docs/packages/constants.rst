constants
==================

.. meta::
   :description: Named constants and helpers for Python HTML entities, CSS colors, keyboard codes, HTTP status codes, and web-platform values.
   :keywords: Python constants, HTML entities, CSS colors, keyboard key codes, HTTP status codes, web constants

``domonic.constants`` contains named values and helpers for common web work:
character entities, keyboard codes, HTTP status codes, color conversion, and
small lookup tables.

Color Helpers
-------------

.. code-block :: python

	from domonic.constants.color import Color

	print(Color.random_hex())
	print(Color.hex2rgb("#ff00ff"))
	print(Color.rgb2hex(255, 0, 255))

Use generated colors in HTML:

.. code-block :: python

	from domonic.constants.color import Color
	from domonic.html import div

	badge = div("Live")
	badge.style.backgroundColor = Color.rgb2hex(16, 185, 129)
	badge.style.color = "#ffffff"
	print(badge)

Character Entities
------------------

.. code-block :: python

	from domonic.constants.entities import Char

	print(Char.AMPERSAND)
	print(Char.COPYRIGHT)

Keyboard Codes
--------------

.. code-block :: python

	from domonic.constants.keyboard import KeyCode

	print(KeyCode.DOWN)
	print(KeyCode.ENTER)

HTTP Status Codes
-----------------

.. code-block :: python

	from domonic.constants import HTTPStatus

	print(HTTPStatus.OK)
	print(HTTPStatus.NOT_FOUND)

.. autoclass:: domonic.constants.color.Color
    :members:
    :noindex:

.. autoclass:: domonic.constants.entities.Char
    :members:
    :noindex:

.. autoclass:: domonic.constants.keyboard.KeyCode
    :members:
    :noindex:
