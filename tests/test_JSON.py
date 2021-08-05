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
from domonic.JSON import *


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
        # data = JSON.parse(SOMEJSON)
        # print(data)

        t = JSON.tablify(TestCase.SOMEJSON2)
        print(t)

        t = JSON.tablify(json.loads(TestCase.SOMEJSON2))
        print(t)

        t = JSON.tablify(TestCase.SOMEJSON)
        print(t)

        # t = JSON.csvify(TestCase.SOMEJSON)
        # print(t)

        # t = JSON.csv2json("data.csv")
        # print(t)

        @return_json
        def yo():
            myObj = {"hi": [1, 2, 3]}
            return myObj

        print('goat')
        print(yo())

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
