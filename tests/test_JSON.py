"""
    test_domonic
    ~~~~~~~~~~~~
    unit tests for css
"""

import unittest

import json
# import requests
# from mock import patch

from domonic.html import *

from domonic.decorators import as_json
import domonic.JSON as JSON  # do this to use same way as previous versions of domonic


class TestCase(unittest.TestCase):

    SOMEJSON = '''
    { "items": [
        {
            "id":"01",
            "name": "Java",
            "thing":{},
            "list":[]
        },
        {
            "id":"07",
            "name": "C++",
            "thing":{},
            "list":[]
        }
    ]}
    '''
    SOMEJSON2 = '''
    [
        {
            "id":"01",
            "name": "Java",
            "thing":{},
            "list":[]
        },
        {
            "id":"07",
            "name": "C++",
            "thing":{},
            "list":[]
        },
        {
            "id":"08",
            "name": "DDD",
            "thing":{},
            "list":[],
            "extra":23
        }
    ]
    '''

    def test_domonic_JSON(self):
        t = JSON.tablify(TestCase.SOMEJSON2)
        assert isinstance(t, Element)
        assert t.tagName == 'table'
        t = JSON.tablify({'id': 1, 'name': 'test'})
        assert isinstance(t, Element)
        assert t.tagName == 'table'
        t = JSON.tablify(JSON.parse(TestCase.SOMEJSON2))
        assert isinstance(t, Element)
        assert t.tagName == 'table'
        assert t.getElementsByTagName('td')[0].textContent == '01'
        t = JSON.tablify(JSON.parse(TestCase.SOMEJSON)['items'])
        assert t.getElementsByTagName('td')[0].textContent == '01'

        # t = JSON.csvify(TestCase.SOMEJSON)
        # print(t)

        # t = JSON.csv2json("data.csv")
        # print(t)

        @as_json
        def yo():
            myObj = {"hi": [1, 2, 3]}
            return myObj
        assert yo() == '{"hi": [1, 2, 3]}'

        # json_data = JSON.parse_file('surveys.json')
        # mytable = JSON.tablify(json_data)
        # print(mytable)

        # with JSON( data, 'items') as item:
        # print(item)
        # print(item.id)

        # iterator = JSON( data, 'items.age', lambda i: i<30 )

        # @JSON
        # def somefunc():
        #     returns pyobj


if __name__ == '__main__':
    unittest.main()
