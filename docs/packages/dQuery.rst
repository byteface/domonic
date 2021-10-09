dQuery
=================

dQuery is for querying and manipulating your server-side dom.


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



You can quickly access returned elements as if it were a list...

.. code-block :: python

	somehtml = º('<html><table id="mytable" class="one"></table></html>')
	str(º('html')[0])



But you don't need a DOM fragment to use dquery. It also contains useful static methods. i.e.


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


.. automodule:: domonic.dQuery
    :members:
    :noindex:

