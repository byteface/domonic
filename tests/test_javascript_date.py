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
        d.setTime(1546300800000)  # 2019-01-01, was on a Tuesday
        # print('>>', d.getDate())
        assert d.getDate() == 1

        # print("d.getDay():", d.getDay())  # Tuesday. so, 2
        assert d.getDay() == 2

        # print(d.getMonth())
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

        print("d.getTime()", d.getTime())
        # assert d.getTime() == 1546300800000 # ??
        # print( d.getTimezoneOffset() )
        # print(d.getYear())
        assert d.getYear() == 2019

        # print(d.setDate(1))

        # print(d.setFullYear('1982'))
        # try some different years i.e. 10,000 BC to 10,000 AD (turns out there's limits)
        # try some different years i.e. 1 to 9999
        years = [9999, 1, 1982, 1945, 1851, 2050]
        for year in years:
            d.setFullYear(year)
            # print(d.getFullYear(), year)
            assert d.getFullYear() == year

        d.setHours(2)  # TODO - returns?
        assert d.getHours() == 2

        # print( d.setItem() )
        print(d.setMilliseconds(123))

        d.setMinutes(10)  # TODO - returns?
        assert d.getMinutes() == 10

        d.setMonth(0)  # TODO - returns?
        assert d.getMonth() == 0

        d.setSeconds(10)  # TODO - returns?
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

        # TODO - i think all these setters have supposed to have returns...
        print(d.setUTCDate(1))
        print(d.setUTCFullYear(1928))
        print(d.setUTCHours(3))
        print(d.setUTCMilliseconds(123))
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

    def test_getDate(self):
        Xmas95 = Date('December 25, 1995 23:15:30')
        day = Xmas95.getDate()
        assert day == 25

    def test_getDay(self):
        birthday = Date('August 19, 1975 23:15:30')
        day1 = birthday.getDay()
        # Sunday - Saturday : 0 - 6
        assert day1 == 2

    def test_getFullYear(self):
        today = Date()
        year = today.getFullYear()
        assert isinstance(year, int)

    def test_getHours(self):
        birthday = Date('March 13, 08 04:20')
        assert birthday.getHours() == 4

    def test_getMilliseconds(self):
        moonLanding = Date('July 20, 69 00:20:18')
        moonLanding.setMilliseconds(123)
        # print("moonLanding.getMilliseconds():",moonLanding.getMilliseconds())
        assert moonLanding.getMilliseconds() == 123

    def test_getMinutes(self):
        birthday = Date('March 13, 08 04:20')
        assert birthday.getMinutes() == 20

    def test_getMonth(self):
        moonLanding = Date('July 20, 69 00:20:18')
        assert moonLanding.getMonth() == 6
        Xmas95 = Date('December 25, 1995 23:15:30')
        assert Xmas95.getMonth() == 11

    def test_getSeconds(self):
        moonLanding = Date('July 20, 69 00:20:18')
        assert moonLanding.getSeconds() == 18
        Xmas95 = Date('December 25, 1995 23:15:30')
        assert Xmas95.getSeconds() == 30

    def test_getTime(self):
        # if no century is supplied the browser guesses with anything under 1950 being in the 21st century
        # python datetuil was ticking over at 50 years. so that's been reduced with parserinfo to 30 years to mirror js
        # https://stackoverflow.com/questions/38577076/customize-dateutil-parser-century-inference-logic
        moonLanding = Date('July 20, 69 20:17:40 GMT+00:00')
        assert moonLanding.getTime() == -14182940000

        # // Since month is zero based, birthday will be January 10, 1995
        birthday = Date(1994, 12, 10)
        acopy = Date()
        acopy.setTime(birthday.getTime())
        assert acopy.getTime() == birthday.getTime()

    # def test_getTimezoneOffset(self):
    #     date1 = Date('August 19, 1975 23:15:30 GMT+07:00')
    #     date2 = Date('August 19, 1975 23:15:30 GMT-02:00')
    #     # console.log(date1.getTimezoneOffset());
    #     # // expected output: your local timezone offset in minutes
    #     # // (eg -120). NOT the timezone offset of the date object.
    #     assert date1.getTimezoneOffset() == -420
    #     assert date1.getTimezoneOffset() == date2.getTimezoneOffset()

    def setMinutes(self):
        event = Date('August 19, 1975 23:15:30')
        event.setMinutes(45)
        assert event.getMinutes() == 45
        print(event)
        # // expected output: Tue Aug 19 1975 23:45:30 GMT+0200 (CEST)

    def setSeconds(self):
        event = Date('August 19, 1975 23:15:30')
        event.setSeconds(42)
        assert event.getSeconds() == 42
        print(event)
        # // Sat Apr 19 1975 23:15:42 GMT+0100 (CET)

    def setTime(self):
        event1 = Date('July 1, 1999')
        event2 = Date()
        event2.setTime(event1.getTime())
        print(event1)
        # // expected output: Thu Jul 01 1999 00:00:00 GMT+0200 (CEST)
        print(event2)
        # // expected output: Thu Jul 01 1999 00:00:00 GMT+0200 (CEST)

    def setDate(self):
        event = Date('August 19, 1975 23:15:30')
        event.setDate(24)
        print(event.getDate())
        assert event.getDate() == 24
        # // expected output: 24
        event.setDate(32)
        # // Only 31 days in August!
        print(event.getDate())
        assert event.getDate() == 31
        # // expected output: 1

        # TODO - make these work as described in the spec
        # theBigDay = Date(1962, 6, 7, 12)  # noon of 1962-07-07 (7th of July 1962,  month is 0-indexed)
        # theBigDay2 = Date(theBigDay).setDate(24)  # 1962-07-24 (24th of July 1962)
        # theBigDay3 = Date(theBigDay).setDate(32)  # 1962-08-01 (1st of August 1962)
        # theBigDay4 = Date(theBigDay).setDate(22)  # 1962-07-22 (22nd of July 1962)
        # theBigDay5 = Date(theBigDay).setDate(0)  # 1962-06-30 (30th of June 1962)
        # theBigDay6 = Date(theBigDay).setDate(98)  # 1962-10-06 (6th of October 1962)
        # theBigDay7 = Date(theBigDay).setDate(-50)  # 1962-05-11 (11th of May 1962)

    def setHours(self):
        event = Date('August 19, 1975 23:15:30')
        event.setHours(20)
        print(event)
        assert event.getHours() == 20
        # // expected output: Tue Aug 19 1975 20:15:30 GMT+0200 (CEST)
        event.setHours(20, 21, 22)
        print(event)
        assert event.getHours() == 20
        # // expected output: Tue Aug 19 1975 20:21:22 GMT+0200 (CEST)


    def test_Intl(self):
        from domonic.javascript import Intl
        mydtf = Intl.DateTimeFormat()


if __name__ == '__main__':
    unittest.main()
