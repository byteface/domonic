"""
    test_domonic
    ~~~~~~~~~~~~
    - unit tests for domonic.dom

"""

import unittest
# import requests
# from mock import patch

from domonic.html import *
from domonic.style import *
from domonic.dom import *
from domonic import *


class domonicTestCase(unittest.TestCase):
    """ Tests for the dom package """

    def test_dom_Node(self):

        n = Node()
        # print(n)
        self.assertIsInstance(n, Node)
        # n.assertEqual(str(sometag), '<div id="someid">asdfasdf<div></div><div>yo</div></div>')
        # n.baseURI = 'eventual.technology'
        # n.baseURIObject = None
        # n.isConnected = True
        # n.namespaceURI = "http://www.w3.org/1999/xhtml"
        # n.nodePrincipal = None
        # n.outerText = None
        # n.ownerDocument = None
        # n.prefix = None  # 🗑️
        # n.rootNode = None

        b = Node()
        n.appendChild(b)
        self.assertEqual(True, n.hasChildNodes)

        c = Node()
        n.appendChild(c)
        self.assertEqual(c, n.lastChild)
        self.assertEqual(b, n.firstChild)
        self.assertEqual(2, n.childElementCount)
        self.assertEqual(True, b in n.childNodes)
        self.assertEqual(True, c in n.childNodes)
        self.assertEqual(None, n.localName)  # obsolete if not a tag or attribute should return none
        self.assertEqual(2, len(n.children))
        self.assertEqual(None, n.nodeValue)
        # print(n.nodeType())
        d = div("test")
        # print(type(d))
        # print(d.nodeName)
        self.assertEqual("DIV", d.nodeName)
        self.assertEqual("test", d.nodeValue)
        self.assertEqual(True, n.contains(c))

        n.insertBefore(d, c)
        self.assertEqual(True, n.children[1] == d)

        self.assertEqual(True, n.contains(c))
        n.removeChild(c)
        self.assertEqual(False, n.contains(c))

        # print( n.replaceChild(self, newChild, oldChild) )
        n2 = n.cloneNode()
        # print(len(n2.children))
        self.assertEqual(True, len(n2.children) == 2)
        self.assertEqual(False, n.children == n2.children)
        self.assertEqual(True, n.isSameNode(n))
        self.assertEqual(False, n.isSameNode(n2))
        a1 = div("hi")
        a2 = div("hi")
        self.assertEqual(True, a1.isEqualNode(a2))

        print(a1.nodeValue)
        self.assertEqual(True, a1.nodeValue == "hi")

        a1.nodeValue = "something else"
        self.assertEqual(True, a1.nodeValue == "something else")
        print(a1.nodeValue)

        a1.textContent = "something new"
        self.assertEqual(True, a1.textContent == "something new")
        print(a1.textContent)

        myobj = domonic.domonify('div(_class="mytest")')
        print('---')
        print(type(myobj))
        myobj.style.float = "left"
        print('---')
        print(myobj)
        self.assertEqual(True, str(myobj) == '<div class="mytest" style="float:left;"></div>')

        mylist = li() / 10
        myobj = domonic.domonify(domonic.parse(mylist))
        print(myobj)

        myorderedlist = ol()
        myorderedlist += str(li() / 10)
        print(myorderedlist)

        # compareDocumentPosition()
        # getRootNode()
        # isDefaultNamespace()
        # lookupNamespaceURI()
        # lookupPrefix()
        # normalize()
        # def isSupported(self): return False #  🗑
        # getUserData() 🗑️
        # setUserData() 🗑️

    def test_dom_node(self):
        sometag = div("asdfasdf", div(), div("yo"), _id="test", _thingy="test22")
        somenewdiv = div('im new')
        sometag.appendChild(somenewdiv)

        print("parent tests")
        print(somenewdiv.parentNode)
        print(type(somenewdiv.parentNode))
        print(somenewdiv.parentNode.id)
        print(somenewdiv.parentElement)
        print(somenewdiv.previousSibling)
        print(somenewdiv.previousSibling.nextSibling)

        mylist = ul(li(1), li(2), li(3))
        print(mylist[1])

        mylist = ul(li(), li(), li())
        print(*mylist)

        a1, b1, c1 = ul(li(1), li(2), li(3))
        print(a1)

        a1, b1, c1, d1, e1 = button() * 5
        print(a1, b1, c1, d1, e1)

        # print(mylist[1] != mylist[1])
        a1 = img()
        a1 >> {'_src': "http://www.someurl.com"}
        print(a1)

        a1 = button()
        a1 += "hi"
        a1 += "how"
        a1 += "are"
        a1 += "you"
        print(a1)
        a1 -= "hi"
        # print(a1)
        # print(div(_test="1", **{"_data-test": ""}))

        print(sometag.id)
        # print(sometag.style.color)  # TODO - get on style

        print(sometag._thingy)
        print(sometag.thingy)
        # print(10/sometag)

        # print('>>>>', sometag.args[0])
        # print('>>>>',sometag)
        # print('>>>>', sometag.lastChild())
        # print('>>>>', sometag.content)

        # import gc
        # import pprint
        # for r in gc.get_referents(somenewdiv):
        #     pprint.pprint(r)

        # for r in gc.get_referents(sometag):
        #     pprint.pprint(r)

    def test_dom_node_again(self):
        somebody = body("test", _class="why")  # .html("wn")
        print(somebody)

        somebody = body("test", _class="why").html("nope")
        print(somebody)

    def test_dom(self):

        # test div html and innerhtml update content
        sometag = div("asdfasdf", div(), div("yo"), _id="someid")
        self.assertEqual(sometag.tagName, 'div')
        self.assertEqual(str(sometag), '<div id="someid">asdfasdf<div></div><div>yo</div></div>')
        sometag.html('test')
        self.assertEqual(str(sometag), '<div id="someid">test</div>')
        sometag.innerHTML = 'test2'
        self.assertEqual(str(sometag), '<div id="someid">test2</div>')

        # same test on body tag
        bodytag = body("test", _class="why")
        self.assertEqual(str(bodytag), '<body class="why">test</body>')
        # print(bodytag)

        bodytag.html("bugs bunny")
        self.assertEqual(str(bodytag), '<body class="why">bugs bunny</body>')
        # print('THIS:',bodytag)

        # sometag.innerText()
        print(sometag.getAttribute('_id'))
        self.assertEqual(sometag.getAttribute('_id'), 'someid')
        print(sometag.getAttribute('id'))
        self.assertEqual(sometag.getAttribute('_id'), 'someid')

        mydiv = div("I like cake", div(_class='myclass').html(div("1"), div("2"), div("3")))
        print(mydiv)

        # print(sometag.innerText())
        # print(sometag.nodeName)
        # assert(sometag.nodeName, 'DIV') # TODO - i checked one site in chrome, was upper case. not sure if a standard?

        print(sometag.setAttribute('id', 'newid'))
        print(sometag)

        print(sometag.lastChild)
        print(sometag.hasChildNodes)
        # print('>>',sometag.textContent()) # TODO - will have a think. either strip or render tagless somehow

        sometag.removeAttribute('id')
        print(sometag)

        sometag.appendChild(footer('test'))
        print(sometag)

        print(sometag.children)
        print(sometag.firstChild)

        htmltag = html()
        print(htmltag)
        htmltag.write('sup!')
        htmltag.className = "my_cool_css"
        print(htmltag)
        print('-END-')

    def test_dom_create(self):
        print(html().documentElement)
        print(html().URL)
        somebody = document.createElement('sometag')
        print(str(somebody))
        comm = document.createComment('hi there here is a comment')
        print(comm)

        print(html().createElement('sometag'))
        # somebody = document.createElement('sometag')
        # print(str(somebody()))

    def test_dom_events(self):
        print(html().documentElement)
        print(html().URL)
        site = html()
        somebody = document.createElement('div')
        site.appendChild(somebody)
        print(site)

        def test(evt, *args, **kwargs):
            print('test ran!')
            print(evt)
            print(evt.target)

        site.addEventListener('click', test)
        somebody.addEventListener('anything', test)
        print(site.listeners)
        # site.removeEventListener('click', test)
        # print( site.listeners )

        site.dispatchEvent(Event('click'))
        somebody.dispatchEvent(Event('anything'))

        # document.getElementById("myBtn").addEventListener("click", function(){
        #   document.getElementById("demo").innerHTML = "Hello World";
        # });

    def test_dom_contains(self):
        site = html()
        somebody = document.createElement('div')
        site.appendChild(somebody)
        print(site)
        another_div = div()
        print(site.contains(somebody))
        another_div = div()
        print(site.contains(another_div))
        another_div = document.createElement('div')
        print(site.contains(another_div))
        third_div = document.createElement('div')
        another_div.appendChild(third_div)
        site.appendChild(another_div)
        print(site.contains(third_div))

    def test_dom_getElementById(self):
        pass


    # def test_dom_Node():
        # TODO - tests all below
        # contains - probably need more recursive testing
        # replaceChild
        # anchors


if __name__ == '__main__':
    unittest.main()
