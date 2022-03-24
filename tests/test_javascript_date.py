"""
    test_javascript_date
    ~~~~~~~~~~~~~~~
    unit tests for domonic.javascript.Date
"""

import time
import unittest
from inspect import stack
from unittest.mock import Mock

from domonic.javascript import *
from domonic.javascript import (URL, Array, Date, Global, Math, Object, String,
                                Window)

# import requests
# from mock import patch


class TestCase(unittest.TestCase):

    def test_javascript_date(self):

        print(Date.now())

        unixTimeZero = Date.parse('01 Jan 1970 00:00:00 GMT')
        assert unixTimeZero == 0
        javaScriptRelease = Date.parse('04 Dec 1995 00:12:00 GMT')
        assert javaScriptRelease == 818035920000

        d = Date()
        # set the date
        d.setTime(1546300800000)  # 2019-01-01
        # print('>>', d.getDate())
        assert d.getDate() == 1
        # print(d.getDay())
        assert d.getDay() == 1
        print(d.getMonth())
        assert d.getMonth() == 0
        # print(d.getFullYear())
        assert d.getFullYear() == 2019
        # print(d.getHours())
        assert d.getHours() == 0
        # print(d.getMilliseconds())
        assert d.getMilliseconds() == 0
        # print(d.getMinutes())
        assert d.getMinutes() == 0
        # print(d.getSeconds())
        assert d.getSeconds() == 0
        # print(d.getTime())
        assert d.getTime() == 1546300800000
        # print( d.getTimezoneOffset() )
        # print(d.getYear())
        assert d.getYear() == 2019

        print(d.setDate(1))

        # print(d.setFullYear('1982'))
        # try some different years i.e. 10,000 BC to 10,000 AD (turns out there's limits)
        # try some different years i.e. 1 to 9999
        years = [9999, 1, 1982, 1945, 1851, 2050]
        for year in years:
            d.setFullYear(year)
            # print(d.getFullYear(), year)
            assert d.getFullYear() == year

        d.setHours(2)
        assert d.getHours() == 2

        # print( d.setItem() )
        print(d.setMilliseconds(12345))

        d.setMinutes(10)
        assert d.getMinutes() == 10

        d.setMonth(0)
        assert d.getMonth() == 0

        d.setSeconds(10)
        assert d.getSeconds() == 10

        # print(d.setTime(1000))  # TODO - more dates

        # TODO - go back over all these methods
        print(d.getUTCDate())
        print(d.getUTCDay())
        print(d.getUTCFullYear())
        print(d.getUTCHours())
        print(d.getUTCMilliseconds())
        print(d.getUTCMinutes())
        print(d.getUTCMonth())
        print(d.getUTCSeconds())

        print(d.setUTCDate(1))
        print(d.setUTCFullYear(1928))
        print(d.setUTCHours(3))
        print(d.setUTCMilliseconds(54321))
        print(d.setUTCMinutes(50))
        print(d.setUTCMonth(3))
        print(d.setUTCSeconds(11))
        print(d.setYear(1987))
        print(d.toDateString())
        print(d.toGMTString())
        print(d.toJSON())
        print(d.toISOString())
        print(d.toLocaleDateString())
        print(d.toLocaleString())
        print(d.toLocaleTimeString())
        print(d.toTimeString())
        print(d.toUTCString())
        print(d.UTC())

        print(Date(1415988000))
        # print(Date(9999))
        # print(Date(99999))
        d = Date(1415988000)
        print(d.getFullYear())

        # do year 2048
        # millisecs = (2048 - 1970) * 365 * 24 * 60 * 60 * 1000
        # d = Date(millisecs)
        # print(d.getFullYear())


_intID = None
_results = []


if __name__ == '__main__':
    unittest.main()
