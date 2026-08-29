bs4
===

``domonic.bs4`` gives you a Beautiful Soup 4 style API while keeping a real
domonic DOM underneath.

The important bit is that returned objects are ordinary domonic nodes. They are
not wrapper ``Tag`` objects and there is no second parsed tree.

Importing ``domonic.bs4`` installs the compatibility methods as an opt-in patch
onto domonic's ``Node``, ``Element``, ``Document``, ``DocumentFragment``,
``Text`` and ``Comment`` classes. A normal ``import domonic`` does not install
these methods.

Parse
-----

.. code-block:: python

   from domonic.bs4 import BeautifulSlop

   markup = """
   <main id="site">
     <article class="post featured">
       <h1>Hello</h1>
       <p>Read <a href="/docs" class="external">the docs</a>.</p>
     </article>
   </main>
   """

   soup = BeautifulSlop(markup, "html.parser")

``BeautifulSlop`` accepts domonic parser names:

.. code-block:: python

   BeautifulSlop(markup, "html5lib")
   BeautifulSlop(markup, "markupever")
   BeautifulSlop(markup, "selectolax")
   BeautifulSlop(markup, "html5_parser")
   BeautifulSlop(markup, "justhtml")
   BeautifulSlop(markup, "expat")

It also accepts familiar Beautiful Soup names where they map cleanly onto
domonic parser backends:

.. code-block:: python

   BeautifulSlop(markup, "html.parser")  # Python stdlib parser
   BeautifulSlop(markup, "lxml")         # maps to lxml_html

Find Tags
---------

.. code-block:: python

   first_link = soup.find("a")
   all_links = soup.find_all("a")

   article = soup.find("article", id="main")
   external = soup.find_all("a", class_="external")
   text_inputs = soup.find_all("input", {"type": "text"})

   for link in all_links:
       print(link.get("href"))

Limit results:

.. code-block:: python

   first_two_links = soup.find_all("a", limit=2)

Search only direct children:

.. code-block:: python

   article.find("a", recursive=False)
   article.find_child("h1")
   article.find_children()

Filter Values
-------------

String filters:

.. code-block:: python

   soup.find("a", href="/docs")
   soup.find("article", class_="post featured")

List filters:

.. code-block:: python

   soup.find_all(["article", "aside"])
   soup.find_all("p", {"class": ["lede", "summary"]})

Regular expression filters:

.. code-block:: python

   import re

   soup.find(re.compile("^art"))
   soup.find("a", href=re.compile(r"docs$"))
   soup.find("p", class_=re.compile("featured"))

Callable filters:

.. code-block:: python

   soup.find(lambda tag: tag.name == "article")
   soup.find("a", href=lambda value: value and value.startswith("/"))
   soup.find("p", class_=lambda value: value == "featured")

Presence and absence filters:

.. code-block:: python

   soup.find_all("a", href=True)
   soup.find_all("img", alt=None)

Text Search
-----------

Use ``string=`` for Beautiful Soup style text matching:

.. code-block:: python

   title_text = soup.find(string="Hello")
   docs_text = soup.find(string=re.compile("docs"))
   heading = soup.find("h1", string="Hello")

The older ``text=`` alias is also accepted:

.. code-block:: python

   heading = soup.find("h1", text="Hello")

domonic may return ``Text`` nodes for parsed text. They render as text and still
remain part of the real domonic DOM:

.. code-block:: python

   print(str(title_text))

CSS Selectors
-------------

``select`` and ``select_one`` delegate to domonic's selector engine:

.. code-block:: python

   soup.select("article a.external")
   soup.select_one("article > p")

Navigation
----------

.. code-block:: python

   link = soup.find("a")

   link.parent
   list(link.parents)

   link.next_sibling
   list(link.next_siblings)

   link.previous_sibling
   list(link.previous_siblings)

   link.next_element
   list(link.next_elements)

   link.previous_element
   list(link.previous_elements)

Search relative to a node:

.. code-block:: python

   link.find_parent("article")
   link.find_parents()
   link.find_next("p")
   link.find_all_next("a")
   link.find_previous("h1")
   link.find_all_previous()
   link.find_next_sibling("aside")
   link.find_previous_sibling("p")

Attributes
----------

.. code-block:: python

   link = soup.find("a")

   link.attrs
   link.get("href")
   link.get("missing", "fallback")
   link.has_attr("href")

   link["href"] = "/new-url"
   print(link["href"])
   del link["href"]

The old ``has_key`` alias is available for compatibility:

.. code-block:: python

   link.has_key("href")

Text Extraction
---------------

.. code-block:: python

   article = soup.find("article")

   article.text
   article.get_text()
   article.get_text(" | ", strip=True)

   list(article.strings)
   list(article.stripped_strings)

Mutation
--------

Use familiar Beautiful Soup methods, backed by domonic's DOM operations:

.. code-block:: python

   article = soup.find("article")

   badge = soup.new_tag("span", class_="badge")
   badge.append("new")

   article.find("h1").insert_after(badge)
   article.append(soup.new_tag("footer"))

Remove nodes:

.. code-block:: python

   aside = soup.find("aside")
   removed = aside.extract()

   soup.find("script").decompose()
   soup.find("article").clear()

Replace or wrap nodes:

.. code-block:: python

   old = soup.find("b")
   strong = soup.new_tag("strong")
   strong.append(old.text)
   old.replace_with(strong)

   paragraph = soup.find("p")
   wrapper = soup.new_tag("section", class_="copy")
   paragraph.wrap(wrapper)
   wrapper.unwrap()

Smooth adjacent text nodes:

.. code-block:: python

   p = soup.find("p")
   p.append(soup.new_string(" more"))
   p.smooth()

Create Nodes
------------

.. code-block:: python

   tag = soup.new_tag("a", href="/hello", class_="external")
   tag.append("hello")

   text = soup.new_string("plain text")

These return domonic ``Element`` and ``Text`` objects.

Still Domonic
-------------

Because ``BeautifulSlop`` returns normal domonic nodes, the DOM API remains
available:

.. code-block:: python

   article = soup.find("article")

   soup.querySelectorAll("article > a")
   article.parentNode
   article.setAttribute("data-ready", "yes")
   article.getAttribute("data-ready")

Render
------

.. code-block:: python

   print(soup)
   print(soup.prettify())

Compatibility Notes
-------------------

This layer targets the common Beautiful Soup workflows: search, navigation,
attributes, text extraction, creation, mutation and rendering. It does not try
to clone Beautiful Soup internals such as builders, formatter objects, encoding
detection, result set subclasses or ``NavigableString``.

.. automodule:: domonic.bs4
    :members:
    :no-index:
