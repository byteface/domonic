utils
=================

.. meta::
   :description: Utility helpers for Python web, DOM, text, numbers, units, byte sizes, ports, URLs, and iterable workflows in domonic.
   :keywords: Python utilities, number utilities, text helpers, web utilities, DOM helpers, byte size parser, port validation

The ``domonic.utils`` package contains helpers used across DOM-related
workflows: text casing, iterable helpers, number and unit helpers, byte-size
formatting, URL-safe filenames, and small conveniences used by other modules.

String Case Helpers
-------------------

.. code-block :: python

	from domonic.utils import Utils

	print(Utils.case_camel("data-user-id"))
	print(Utils.case_snake("dataUserId"))
	print(Utils.case_kebab("dataUserId"))

Lists and Iterables
-------------------

.. code-block :: python

	from domonic.utils import Utils

	items = ["", "docs", None, "api", "docs"]
	print(Utils.clean(items))
	print(Utils.unique(["a", "b", "a"]))
	print(list(Utils.chunks([1, 2, 3, 4, 5], 2, tuple)))

Numbers, Units, Bytes, and Ports
--------------------------------

.. code-block :: python

	from domonic.utils import NumberUtils

	print(NumberUtils.clamp(120, 0, 100))
	print(NumberUtils.lerp(0, 10, 0.25))
	print(NumberUtils.remap(50, 0, 100, 0, 1))
	print(NumberUtils.parse_unit("1.5rem"))
	print(NumberUtils.parse_bytes("1.5 MiB"))
	print(NumberUtils.format_bytes(1536, binary=True))
	print(NumberUtils.is_port("8080", allow_zero=False))

DOM-Friendly Use
----------------

.. code-block :: python

	from domonic.html import li, ul
	from domonic.utils import Utils

	items = ["One", "Two", "Three"]
	page = ul(*(li(item, _data_key=Utils.case_kebab(item)) for item in items))
	print(page)

URL-Safe Filenames
------------------

.. code-block :: python

	from domonic.utils import Utils

	cache_key = Utils.url2file("https://example.com/docs?q=domonic")
	print(cache_key)

.. automodule:: domonic.utils
    :members:
    :noindex:
