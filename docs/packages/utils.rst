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
	# dataUserId
	print(Utils.case_snake("dataUserId"))
	# data_user_id
	print(Utils.case_kebab("dataUserId"))
	# data-user-id

Lists and Iterables
-------------------

.. code-block :: python

	from domonic.utils import Utils

	items = ["", "docs", None, "api", "docs"]
	print(Utils.clean(items))
	# ['docs', 'api', 'docs']
	print(Utils.unique(["a", "b", "a"]))
	# ['a', 'b']
	print(list(Utils.chunks([1, 2, 3, 4, 5], 2, tuple)))
	# [(1, 2), (3, 4), (5,)]

Numbers, Units, Bytes, and Ports
--------------------------------

.. code-block :: python

	from domonic.utils import NumberUtils

	print(NumberUtils.clamp(120, 0, 100))
	# 100
	print(NumberUtils.lerp(0, 10, 0.25))
	# 2.5
	print(NumberUtils.remap(50, 0, 100, 0, 1))
	# 0.5
	print(NumberUtils.parse_unit("1.5rem"))
	# NumberUnit(value=1.5, unit='rem')
	print(NumberUtils.parse_bytes("1.5 MiB"))
	# 1572864
	print(NumberUtils.format_bytes(1536, binary=True))
	# 1.5 KiB
	print(NumberUtils.is_port("8080", allow_zero=False))
	# True

DOM-Friendly Use
----------------

.. code-block :: python

	from domonic.html import li, ul
	from domonic.utils import Utils

	items = ["One", "Two", "Three"]
	page = ul(*(li(item, **{"_data-key": Utils.case_kebab(item)}) for item in items))
	print(page)
	# <ul><li data-key="one">One</li><li data-key="two">Two</li><li data-key="three">Three</li></ul>

Note the ``**{"_data-key": ...}`` form, not ``_data_key=`` -- a plain keyword
argument can't contain a hyphen, and a leading underscore alone does not turn
extra underscores into hyphens (see :doc:`html`).

URL-Safe Filenames
------------------

.. code-block :: python

	from domonic.utils import Utils

	cache_key = Utils.url2file("https://example.com/docs?q=domonic")
	print(cache_key)
	# https____example.com_docs%3Fq%3Ddomonic

.. automodule:: domonic.utils
    :members:
    :noindex:
