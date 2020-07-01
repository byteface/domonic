"""    
    test_domonic 
    ~~~~~~~~~~~~~~~~
    
    unit tests for css
    

"""

import unittest
# import requests
# from mock import patch

from domonic import *
from domonic.css import *

class domonicTestCase(unittest.TestCase):
    def test_domonic_css(self):
        # h = html()
        # print(h)
        
        atag = a("linky", _href="https://eventual.technology")
        print(atag.style.alignContent)

        sometag = div("asdfasdf", _id="test")
        print(sometag.style)
        sometag.style.alignContent = None
        print(sometag.style.alignContent)

        # dom.select('#test' ).doshit() # TODO - 

        # print(sometag.style)

        # print(sometag.tagName)
        
        # s = Style(_href="https://somesite.com:8000/blog/article-one#some-hash")
        
        # print(sometag)


if __name__ == '__main__':
    unittest.main()
