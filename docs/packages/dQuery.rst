dQuery
=================

dQuery is for querying and manipulating your server-side DOM.


querying
----------------

dQuery uses the º symbol (alt+0).

.. code-block :: python

	from domonic.html import *
	from domonic.dQuery import º

    d = html(head(body(li(_class='things'), div(_id="test"))))
    
    º(d) # you need to init a dom first. i.e. a html element

    # now you can use it
    print( º('#test') )
    print( º('.things') )
    a = º('<div class="test2"></div>')
    print( a )

    b = º('#test').append(a)
    print(b)



You can quickly access returned elements as if they were a list:

.. code-block :: python

	somehtml = º('<html><table id="mytable" class="one"></table></html>')
	str(º('html')[0])



You do not need a DOM fragment to use dQuery. It also contains useful static methods:


.. code-block :: python

    first = ["a", "b", "c"]
    second = ["d", "e", "f"]
    result = º.merge(first, second)
    print(result)

    obj1 = {'a':1,'b':2}
    obj2 = {'c':1,'b':5}
    print(º.extend(obj1,obj2))

    print(º.trim("  some tst \n   TEST."))

    print(º.now())


Ajax helpers
----------------

``º.ajax()``, ``º.get()``, ``º.getJSON()`` and ``º.post()`` wrap ``requests`` with
jQuery-like callbacks and global Ajax events.

.. code-block :: python

    from domonic.dQuery import º

    º.ajaxStart(lambda event: print("loading"))
    º.ajaxStop(lambda event: print("done"))

    data = º.getJSON("https://example.com/api", {"q": "domonic"})
    º.post("https://example.com/save", {"name": "Ada"})


.. automodule:: domonic.dQuery
    :members:
    :noindex:
