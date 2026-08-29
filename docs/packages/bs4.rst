bs4
===

``domonic.bs4`` provides a Beautiful Soup 4 style compatibility layer without
creating wrapper tags or a second tree.

Importing ``domonic.bs4`` opt-in patches the convenience API onto domonic's
``Node``, ``Element``, ``Document``, ``DocumentFragment``, ``Text`` and
``Comment`` classes. Normal ``domonic`` imports are unchanged.

.. code-block:: python

   from domonic.bs4 import BeautifulSlop

   soup = BeautifulSlop(markup, "html.parser")

   for link in soup.find_all("a", class_="external"):
       print(link.get("href"))

   soup.find("aside").decompose()

   # These are still domonic nodes.
   soup.querySelectorAll("article > a")
   soup.find("article").setAttribute("data-ready", "yes")

Supported parser names include domonic's existing parser backends:
``markupever``, ``selectolax``, ``html5_parser``, ``html5lib``, ``justhtml`` and
``expat``. Familiar Beautiful Soup names such as ``html.parser`` and ``lxml``
are mapped onto suitable domonic parser backends.

.. automodule:: domonic.bs4
    :members:
    :no-index:
