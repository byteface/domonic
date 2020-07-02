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
        sometag = div("asdfasdf", div(), div("yo"), _id="test")
        print(sometag.tagName)

        print(sometag)
        sometag.html('test')
        print(sometag)

        # sometag.innerText()

        print(sometag.getAttribute('_id'))
        print(sometag.getAttribute('id'))
        print(sometag.innerText())
        print(sometag.nodeName)
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


if __name__ == '__main__':
    unittest.main()
