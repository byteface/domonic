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


class domonicTestCase(unittest.TestCase):

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

        mydiv = div("I like cake", div(_class='myclass').html(div("1"),div("2"),div("3")))
        print(mydiv)

        # print(sometag.innerText())
        # print(sometag.nodeName)
        # assert(sometag.nodeName, 'DIV') # TODO - i checked one site in chrome, was upper case. not sure if a standard?

        print(sometag.setAttribute('id','newid'))
        print(sometag)

        print(sometag.lastChild())
        print(sometag.hasChildNodes())
        # print('>>',sometag.textContent()) # TODO - will have a think. either strip or render tagless somehow

        sometag.removeAttribute('id')
        print(sometag)

        sometag.appendChild(footer('test'))
        print(sometag)

        print(sometag.children())
        print(sometag.firstChild())

        htmltag = html()
        print(htmltag)
        htmltag.write('sup!')
        htmltag.className = "my_cool_css"
        print(htmltag)

        print('-END-')

    def test_dom_node(self):
        sometag = div("asdfasdf", div(), div("yo"), _id="test")
        somenewdiv = div('im new')
        sometag.appendChild(somenewdiv)
        print('>>>>',sometag.args[0])
        # print('>>>>',sometag)
        print('>>>>',sometag.lastChild())
        print('>>>>',sometag.content)
        
        import gc
        import pprint
        for r in gc.get_referents(somenewdiv):
            pprint.pprint(r)

        for r in gc.get_referents(sometag):
            pprint.pprint(r)



    def test_dom_node_again(self):
        somebody = body("test", _class="why")#.html("wn")
        print(somebody)

        somebody = body("test", _class="why").html("nope")
        print(somebody)



if __name__ == '__main__':
    unittest.main()
