"""
test_javascript_date
~~~~~~~~~~~~~~~
unit tests for domonic.javascript.Date
"""

import datetime
import time
import unittest
from inspect import stack
from unittest.mock import Mock

from domonic.javascript import *
from domonic.javascript import URL, Array, Date, Global, Math, Object, String, Window


def _debug_print(*args, **kwargs):
    return None


class TestCase(unittest.TestCase):
    def test_javascript_date(self):

        _debug_print(Date.now())

        unixTimeZero = Date.parse("01 Jan 1970 00:00:00 GMT")
        assert unixTimeZero == 0
        javaScriptRelease = Date.parse("04 Dec 1995 00:12:00 GMT")
        assert javaScriptRelease == 818035920000

        d = Date()
        # set the date
        d.setTime(1546300800000, timezone.utc)  # 2019-01-01, was on a Tuesday
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

        _debug_print("d.getTime()", d.getTime())
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

        self.assertEqual(d.setHours(2), d.getTime())
        assert d.getHours() == 2

        # print( d.setItem() )
        self.assertEqual(d.setMilliseconds(123), d.getTime())

        self.assertEqual(d.setMinutes(10), d.getTime())
        assert d.getMinutes() == 10

        self.assertEqual(d.setMonth(0), d.getTime())
        assert d.getMonth() == 0

        self.assertEqual(d.setSeconds(10), d.getTime())
        assert d.getSeconds() == 10

        self.assertEqual(d.setTime(1000, timezone.utc), 1000)
        self.assertEqual(d.getTime(), 1000)

        _debug_print(d.getUTCDate())
        _debug_print(d.getUTCDay())
        _debug_print(d.getUTCFullYear())
        _debug_print(d.getUTCHours())
        _debug_print(d.getUTCMilliseconds())
        _debug_print(d.getUTCMinutes())
        _debug_print(d.getUTCMonth())
        _debug_print(d.getUTCSeconds())

        self.assertEqual(d.setUTCDate(1), d.getTime())
        self.assertEqual(d.setUTCFullYear(1928), d.getTime())
        self.assertEqual(d.setUTCHours(3), d.getTime())
        self.assertEqual(d.setUTCMilliseconds(123), d.getTime())
        self.assertEqual(d.setUTCMinutes(50), d.getTime())
        self.assertEqual(d.setUTCMonth(3), d.getTime())
        self.assertEqual(d.setUTCSeconds(11), d.getTime())
        self.assertEqual(d.setYear(1987), d.getTime())
        self.assertEqual(d.getFullYear(), 1987)

        _debug_print(d.toDateString())
        _debug_print(d.toGMTString())
        _debug_print(d.toJSON())
        _debug_print(d.toISOString())
        _debug_print(d.toLocaleDateString())
        _debug_print(d.toLocaleString())
        _debug_print(d.toLocaleTimeString())
        _debug_print(d.toTimeString())
        _debug_print(d.toUTCString())
        _debug_print(Date.UTC(2026, 0, 1))

        _debug_print(Date(1415988000))
        # print(Date(9999))
        # print(Date(99999))
        d = Date(1415988000)
        _debug_print(d.getFullYear())

        # do year 2048
        # millisecs = (2048 - 1970) * 365 * 24 * 60 * 60 * 1000
        # d = Date(millisecs)
        # print(d.getFullYear())

    def test_getDate(self):
        Xmas95 = Date("December 25, 1995 23:15:30")
        day = Xmas95.getDate()
        assert day == 25

    def test_getDay(self):
        birthday = Date("August 19, 1975 23:15:30")
        day1 = birthday.getDay()
        # Sunday - Saturday : 0 - 6
        assert day1 == 2

    def test_getFullYear(self):
        today = Date()
        year = today.getFullYear()
        assert isinstance(year, int)

    def test_getHours(self):
        birthday = Date("March 13, 08 04:20")
        assert birthday.getHours() == 4

    def test_getMilliseconds(self):
        moonLanding = Date("July 20, 69 00:20:18")
        moonLanding.setMilliseconds(123)
        # print("moonLanding.getMilliseconds():",moonLanding.getMilliseconds())
        assert moonLanding.getMilliseconds() == 123

    def test_getMinutes(self):
        birthday = Date("March 13, 08 04:20")
        assert birthday.getMinutes() == 20

    def test_getMonth(self):
        moonLanding = Date("July 20, 69 00:20:18")
        assert moonLanding.getMonth() == 6
        Xmas95 = Date("December 25, 1995 23:15:30")
        assert Xmas95.getMonth() == 11

    def test_getSeconds(self):
        moonLanding = Date("July 20, 69 00:20:18")
        assert moonLanding.getSeconds() == 18
        Xmas95 = Date("December 25, 1995 23:15:30")
        assert Xmas95.getSeconds() == 30

    def test_getTime(self):
        # if no century is supplied the browser guesses with anything under 1950 being in the 21st century
        # python datetuil was ticking over at 50 years. so that's been reduced with parserinfo to 30 years to mirror js
        # https://stackoverflow.com/questions/38577076/customize-dateutil-parser-century-inference-logic
        moonLanding = Date("July 20, 69 20:17:40 GMT+00:00")
        assert moonLanding.getTime() == -14182940000

        # // Since month is zero based, birthday will be January 10, 1995
        birthday = Date(1994, 12, 10)
        acopy = Date()
        acopy.setTime(birthday.getTime(), timezone.utc)
        assert acopy.getTime() == birthday.getTime()

    def test_date_comparison_and_valueOf(self):
        older = Date("January 1, 2020 00:00:00 GMT+00:00")
        same = Date("January 1, 2020 00:00:00 GMT+00:00")
        newer = Date("January 2, 2020 00:00:00 GMT+00:00")

        self.assertEqual(older, same)
        self.assertNotEqual(older, newer)
        self.assertLess(older, newer)
        self.assertLessEqual(older, same)
        self.assertGreater(newer, older)
        self.assertGreaterEqual(same, older)
        self.assertEqual(older.valueOf(), older.getTime())
        self.assertEqual(
            older,
            datetime.datetime(2020, 1, 1, 0, 0, 0, tzinfo=timezone.utc),
        )
        self.assertFalse(older == "2020-01-01")

    # def test_getTimezoneOffset(self):
    #     date1 = Date('August 19, 1975 23:15:30 GMT+07:00')
    #     date2 = Date('August 19, 1975 23:15:30 GMT-02:00')
    #     # console.log(date1.getTimezoneOffset());
    #     # // expected output: your local timezone offset in minutes
    #     # // (eg -120). NOT the timezone offset of the date object.
    #     assert date1.getTimezoneOffset() == -420
    #     assert date1.getTimezoneOffset() == date2.getTimezoneOffset()
    def test_getTimezoneOffset(self):
        date1 = Date("August 19, 1975 23:15:30 GMT+07:00")
        date2 = Date("August 19, 1975 23:15:30 GMT-02:00")
        self.assertIsInstance(date1.getTimezoneOffset(), int)
        self.assertEqual(date1.getTimezoneOffset(), date2.getTimezoneOffset())

    def test_date_setters_and_string_helpers(self):
        event = Date("August 19, 1975 23:15:30")
        event.setMinutes(45)
        self.assertEqual(event.getMinutes(), 45)

        event.setSeconds(42)
        self.assertEqual(event.getSeconds(), 42)

        event.setTime(Date("1999-07-01 00:00:00").getTime())
        self.assertEqual(event.getFullYear(), 1999)
        self.assertEqual(event.getMonth(), 6)
        self.assertEqual(event.getDate(), 1)

        event.setDate(24)
        self.assertEqual(event.getDate(), 24)

        event.setHours(20, 21, 22)
        self.assertEqual(event.getHours(), 20)
        self.assertEqual(event.getMinutes(), 21)
        self.assertEqual(event.getSeconds(), 22)

        event.setUTCDate(1)
        event.setUTCFullYear(1928)
        event.setUTCHours(3)
        event.setUTCMilliseconds(123)
        event.setUTCMinutes(50)
        event.setUTCMonth(3)
        event.setUTCSeconds(11)
        event.setYear(1987)
        self.assertEqual(event.getFullYear(), 1987)
        self.assertEqual(event.getHours(), 3)
        self.assertEqual(event.getMilliseconds(), 123)
        self.assertEqual(event.getMinutes(), 50)
        self.assertEqual(event.getMonth(), 3)
        self.assertEqual(event.getSeconds(), 11)

        self.assertIn("-", event.toDateString())
        self.assertEqual(event.toGMTString(), event.toUTCString())
        self.assertEqual(event.toJSON(), event.toISOString())
        self.assertIn("-", event.toISOString())
        self.assertTrue(event.toISOString().endswith("Z"))
        self.assertIsInstance(event.toLocaleDateString(), str)
        self.assertIsInstance(event.toLocaleString(), str)
        self.assertIsInstance(event.toLocaleTimeString(), str)
        self.assertIsInstance(event.toTimeString(), str)
        self.assertIn(":", event.toUTCString())
        self.assertEqual(Date.UTC(1970, 0, 1), 0)
        self.assertIsInstance(Date.UTC(2026, 5, 15), int)

    def test_date_setters_with_rollover(self):
        event = Date("January 31, 2020 23:30:00")
        event.setMonth(13)
        self.assertEqual(event.getFullYear(), 2021)
        self.assertEqual(event.getMonth(), 1)

        event.setMonth(-1)
        self.assertEqual(event.getFullYear(), 2020)
        self.assertEqual(event.getMonth(), 11)

        event.setMinutes(61)
        self.assertEqual(event.getHours(), 0)
        self.assertEqual(event.getMinutes(), 1)

    def test_date_toISOString_includes_time_and_utc_suffix(self):
        import datetime

        event = Date()
        event.date = datetime.datetime(2026, 9, 4, 12, 34, 56, 789000)
        self.assertEqual(event.toISOString(), "2026-09-04T12:34:56.789Z")
        self.assertEqual(event.toJSON(), event.toISOString())

        aware = Date()
        aware.date = datetime.datetime(
            2026, 9, 4, 12, 34, 56, 789000, tzinfo=datetime.timezone.utc
        )
        self.assertEqual(aware.toISOString(), "2026-09-04T12:34:56.789Z")

    def setMinutes(self):
        event = Date("August 19, 1975 23:15:30")
        event.setMinutes(45)
        assert event.getMinutes() == 45
        _debug_print(event)
        # // expected output: Tue Aug 19 1975 23:45:30 GMT+0200 (CEST)

    def setSeconds(self):
        event = Date("August 19, 1975 23:15:30")
        event.setSeconds(42)
        assert event.getSeconds() == 42
        _debug_print(event)
        # // Sat Apr 19 1975 23:15:42 GMT+0100 (CET)

    def setTime(self):
        event1 = Date("July 1, 1999")
        event2 = Date()
        event2.setTime(event1.getTime())
        _debug_print(event1)
        # // expected output: Thu Jul 01 1999 00:00:00 GMT+0200 (CEST)
        _debug_print(event2)
        # // expected output: Thu Jul 01 1999 00:00:00 GMT+0200 (CEST)

    def test_setDate_rolls_across_month_boundaries(self):
        event = Date("August 19, 1975 23:15:30")
        self.assertEqual(event.setDate(24), event.getTime())
        self.assertEqual(event.getDate(), 24)

        event.setDate(32)
        self.assertEqual(event.getMonth(), 8)
        self.assertEqual(event.getDate(), 1)

        cases = [
            (24, (1962, 6, 24)),
            (32, (1962, 7, 1)),
            (22, (1962, 6, 22)),
            (0, (1962, 5, 30)),
            (98, (1962, 9, 6)),
            (-50, (1962, 4, 11)),
        ]
        for value, expected in cases:
            with self.subTest(value=value):
                big_day = Date("July 7, 1962 12:00:00")
                big_day.setDate(value)
                self.assertEqual(
                    (big_day.getFullYear(), big_day.getMonth(), big_day.getDate()),
                    expected,
                )

    def setHours(self):
        event = Date("August 19, 1975 23:15:30")
        event.setHours(20)
        _debug_print(event)
        assert event.getHours() == 20
        # // expected output: Tue Aug 19 1975 20:15:30 GMT+0200 (CEST)
        event.setHours(20, 21, 22)
        _debug_print(event)
        assert event.getHours() == 20
        # // expected output: Tue Aug 19 1975 20:21:22 GMT+0200 (CEST)

    def test_Intl(self):
        from domonic.javascript import Intl

        mydtf = Intl.DateTimeFormat()
        event = Date("January 2, 2020 03:04:05 GMT+00:00")
        self.assertEqual(mydtf.format(event), "01/02/20")

        readable = Intl.DateTimeFormat(
            "en-us", {"dateStyle": "medium", "timeStyle": "short"}
        )
        self.assertEqual(readable.format(event), "Jan 02, 2020, 03:04")
        self.assertEqual(readable.resolvedOptions()["locale"], "en-US")
        self.assertEqual(
            Intl.DateTimeFormat.supportedLocalesOf(["en-us", "fr-fr"]),
            ["en-US", "fr-FR"],
        )
        self.assertEqual(
            Intl.DateTimeFormat("en-US", {"timeStyle": "medium"}).format(
                datetime.datetime(2020, 1, 2, 3, 4, 5)
            ),
            "03:04:05",
        )
        self.assertEqual(
            Intl.DateTimeFormat("en-US", {"dateStyle": "short"}).format(1577934245000),
            "01/02/20",
        )


if __name__ == "__main__":
    unittest.main()
