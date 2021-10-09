"""
    test_domonic
    ~~~~~~~~~~~~
    unit tests for css
"""

import unittest
# import requests
# from mock import patch

from domonic.html import *
from domonic.style import *
from domonic.dom import *


class TestCase(unittest.TestCase):

    def test_domonic_css(self):

        atag = a("linky", _href="https://eventual.technology")
        print(atag.style.alignContent)

        sometag = div("asdfasdf", _id="test")
        print(sometag.style)
        sometag.style.alignContent = None
        print(sometag.style.alignContent)

        sometag.style.backgroundColor = "black"
        sometag.style.fontSize = "12px"

        # huh = document.createAttribute("test")
        # huh.value = "wtf"
        # sometag.setAttributeNode(huh)
        print(sometag.style.fontSize)
        print(sometag)

        # dom.select('#test' ).dostuff() # TODO -
        # print(sometag.style)
        # print(sometag.tagName)
        # s = Style()
        # print(sometag)


    # create some failing tests

    # def test_css_style_declaration(self):
        # styleObj = document.styleSheets[0].cssRules[0].style
        # print(styleObj.cssText)

    # def test_css_style_rules(self):
        # myRules = document.styleSheets[0].cssRules # Returns a CSSRuleList
        # print(myRules)

        # myRules = document.styleSheets[0].cssRules
        # print(myRules[0]); # a CSSStyleRule representing the h1.

    #def test_css_styledpropertymap(self):
        # pass






if __name__ == '__main__':
    unittest.main()
