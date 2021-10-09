"""
    test_domonic
    ~~~~~~~~~~~~
    domonic core tests for __init__.py at the root of the domonic package

    (previously no tests. was using examples/parsing/page.py to drive dev)

"""

import unittest
# import requests
# from mock import patch

# from domonic.dom import *
from domonic import domonic


class TestCase(unittest.TestCase):
    """ Tests for the domonic """

    def test_load(self):
        t1 = domonic.load('<html></html>')
        print(t1)

    def test_loads(self):
        # t1 = domonic.loads('<html></html>')
        # print(t1)
        pass

    def parse(self):
        t1 = domonic.parse('<html></html>')
        assert t1 == "html(),"  # hmm wondering if parse is correct term. as returns pyml strings

        # t2 = domonic.parse('<html><body></body></html>')
        # print(t2)
        # t3 = domonic.parse('<html><body><p></p></body></html>')
        # print(t3)

        pass

    def evaluate(self):
        t1 = domonic.evaluate('<html></html>')
        print(t1)

    def test_hacked_expat_parser(self):
        # test the  hacked version of the xpat parser
        print("test!>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
        # t1 = domonic.parseString('<html></html>')
        # print(t1)
        t1 = domonic.parseString('''<html><head><link rel="stylesheet" href="https://unpkg.com/marx-css/css/marx.min.css" /><script src="https://code.jquery.com/jquery-3.5.1.min.js"></script><script>
	function add(){
		$('#results').html( Number($('#a').val()) + Number($('#b').val()) )};
</script></head><body><article><div><label>Add numbers:</label><input id="a" /><span>+</span><input id="b" /><button id="calculate_button" onclick="add();">Calculate</button><div>Result:<div id="results"></div></div></div></article></body></html>''')
        print('RES:', t1)
        print('RES:', type(t1))
        print('RES:', str(t1))
        print(t1.getElementById('a'))

        # print(t1)
        return
#         return

        # print( ':FIRE:', type(t1))
        # return
        # print(str(t1))
        # from domonic import render
        # print( render( t1 ) )

        print("test222!")
        t1 = domonic.parseString('<div></div>')
        print(t1)
        print(str(t1))
        # from domonic import render
        # print( render( t1 ) )


if __name__ == '__main__':
    unittest.main()
