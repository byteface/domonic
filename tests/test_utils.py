"""
test_utils
~~~~~~~~~~
unit tests for domonic.utils
"""

import unittest

from domonic import NumberUtils as RootNumberUtils
from domonic.utils import NumberUnit, NumberUtils, Utils


class TestCase(unittest.TestCase):
    def test_root_export(self):
        self.assertIs(RootNumberUtils, NumberUtils)

    def test_existing_string_helpers(self):
        self.assertEqual(Utils.case_camel("data-user-id"), "dataUserId")
        self.assertEqual(Utils.case_snake("dataUserId"), "data_user_id")
        self.assertEqual(Utils.case_kebab("dataUserId"), "data-user-id")
        self.assertEqual(Utils.digits("size: 1,280px"), "1280")
        self.assertEqual(Utils.numberToBase(255, 16), [15, 15])
        self.assertRegex(Utils.random_color(), r"^#[0-9A-F]{6}$")

    def test_parse_unit(self):
        self.assertEqual(NumberUtils.parse_unit("12px"), NumberUnit(12.0, "px"))
        self.assertEqual(NumberUtils.parse_unit("  -1.5rem "), NumberUnit(-1.5, "rem"))
        self.assertEqual(NumberUtils.parse_unit(".75turn"), NumberUnit(0.75, "turn"))
        self.assertEqual(NumberUtils.parse_unit("1,024.5px").number, 1024.5)
        self.assertEqual(NumberUtils.parse_unit("1_024").number, 1024)

        with self.assertRaises(ValueError):
            NumberUtils.parse_unit(True)

        with self.assertRaises(ValueError):
            NumberUtils.parse_unit("12 px px")

    def test_to_number_and_is_number(self):
        self.assertTrue(NumberUtils.is_number(3))
        self.assertTrue(NumberUtils.is_number(3.5))
        self.assertFalse(NumberUtils.is_number(True))
        self.assertFalse(NumberUtils.is_number(float("inf")))
        self.assertFalse(NumberUtils.is_number("3"))

        self.assertEqual(NumberUtils.to_number("1,234px"), 1234)
        self.assertEqual(NumberUtils.to_number("12.5%"), 12.5)
        self.assertIsNone(NumberUtils.to_number("nope"))
        self.assertEqual(NumberUtils.to_number("nope", default=0), 0)

    def test_clamp_normalize_lerp_and_remap(self):
        self.assertEqual(NumberUtils.clamp("12px", 0, 10), 10)
        self.assertEqual(NumberUtils.clamp(-5, 0), 0)
        self.assertEqual(NumberUtils.clamp(3, max_value=2), 2)
        self.assertEqual(NumberUtils.normalize(50, 0, 100), 0.5)
        self.assertEqual(NumberUtils.normalize(150, 0, 100, clamp_result=True), 1.0)
        self.assertEqual(NumberUtils.lerp(10, 20, 0.25), 12.5)
        self.assertEqual(NumberUtils.remap(5, 0, 10, 0, 100), 50)
        self.assertEqual(NumberUtils.remap(15, 0, 10, 0, 100, clamp_result=True), 100)

        with self.assertRaises(ValueError):
            NumberUtils.clamp(1, 10, 0)

        with self.assertRaises(ValueError):
            NumberUtils.normalize(1, 1, 1)

    def test_percent_helpers(self):
        self.assertEqual(NumberUtils.percent(25, 200), 12.5)
        self.assertEqual(NumberUtils.percent(1, 4, scale=1), 0.25)
        self.assertEqual(NumberUtils.parse_percent("25%", total=200), 50)
        self.assertEqual(NumberUtils.parse_percent(0.25), 0.25)

        with self.assertRaises(ValueError):
            NumberUtils.percent(1, 0)

        with self.assertRaises(ValueError):
            NumberUtils.parse_percent("10px")

    def test_byte_helpers(self):
        self.assertEqual(NumberUtils.parse_bytes("1KB"), 1000)
        self.assertEqual(NumberUtils.parse_bytes("1 KiB"), 1024)
        self.assertEqual(NumberUtils.parse_bytes("1.5MB"), 1500000)
        self.assertEqual(NumberUtils.format_bytes(999), "999 B")
        self.assertEqual(NumberUtils.format_bytes(1500), "1.5 KB")
        self.assertEqual(NumberUtils.format_bytes(1536, binary=True), "1.5 KiB")

        with self.assertRaises(ValueError):
            NumberUtils.parse_bytes("10 parsecs")

        with self.assertRaises(ValueError):
            NumberUtils.format_bytes(1024, precision=-1)

    def test_port_helpers(self):
        self.assertTrue(NumberUtils.is_port("0"))
        self.assertTrue(NumberUtils.is_port("443"))
        self.assertFalse(NumberUtils.is_port("0", allow_zero=False))
        self.assertFalse(NumberUtils.is_port("65536"))
        self.assertFalse(NumberUtils.is_port(True))
        self.assertEqual(NumberUtils.to_port("8080"), 8080)
        self.assertEqual(NumberUtils.to_port("nope", default=8000), 8000)


if __name__ == "__main__":
    unittest.main()
