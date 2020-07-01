"""    
    test_domonic 
    ~~~~~~~~~~~~~~~~
    
    unit tests for domonic
    
    # TODO - tests for all bs5 pages

"""

import unittest
# import requests
# from mock import patch

from domonic import *
from domonic.css import *

class domonicTestCase(unittest.TestCase):

    def test_dom(self):
        
        sometag = div("asdfasdf")
        print(sometag.tagName)

        # assert(sometag.tagName, 'DIV') # TODO - i checked one site in chrome, was upper case. not sure if a standard?
        

if __name__ == '__main__':
    unittest.main()
