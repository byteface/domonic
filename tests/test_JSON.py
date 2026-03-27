"""
    test_domonic
    ~~~~~~~~~~~~
    unit tests for JSON helpers
"""

import json
import os
import tempfile
import unittest

import domonic.JSON as JSON  # do this to use same way as previous versions of domonic
from domonic.decorators import as_json
from domonic.html import Element


class TestCase(unittest.TestCase):
    SOMEJSON = """
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
    """
    SOMEJSON2 = """
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
    """

    def test_tablify(self):
        table_from_string = JSON.tablify(TestCase.SOMEJSON2)
        self.assertIsInstance(table_from_string, Element)
        self.assertEqual(table_from_string.tagName, "table")

        table_from_dict = JSON.tablify({"id": 1, "name": "test"})
        self.assertIsInstance(table_from_dict, Element)
        self.assertEqual(table_from_dict.tagName, "table")

        table_from_list = JSON.tablify(JSON.parse(TestCase.SOMEJSON2))
        self.assertEqual(table_from_list.getElementsByTagName("td")[0].textContent, "01")

        nested_table = JSON.tablify(JSON.parse(TestCase.SOMEJSON)["items"])
        self.assertEqual(nested_table.getElementsByTagName("td")[0].textContent, "01")
        self.assertIn("extra", str(table_from_string))

        with self.assertRaises(ValueError):
            JSON.tablify([1, 2, 3])

    def test_table2json(self):
        table_node = JSON.tablify(
            [
                {"id": "01", "name": "Java"},
                {"id": "07", "name": "C++"},
            ]
        )
        self.assertEqual(
            JSON.table2json(table_node),
            [
                {"id": "01", "name": "Java"},
                {"id": "07", "name": "C++"},
            ],
        )

        with self.assertRaises(ValueError):
            JSON.table2json("not-a-table")

    def test_parse_and_parse_file(self):
        parsed = JSON.parse(TestCase.SOMEJSON)
        self.assertEqual(parsed["items"][1]["name"], "C++")

        parsed_bytes = JSON.parse(TestCase.SOMEJSON.encode("utf-8"))
        self.assertEqual(parsed_bytes["items"][0]["id"], "01")

        with tempfile.NamedTemporaryFile("w+", suffix=".json", delete=False) as handle:
            handle.write('{"hello": "world"}')
            temp_path = handle.name

        try:
            self.assertEqual(JSON.parse_file(temp_path), {"hello": "world"})
        finally:
            os.unlink(temp_path)

    def test_stringify(self):
        payload = {"hi": [1, 2, 3]}
        text = JSON.stringify(payload, sort_keys=True)
        self.assertEqual(text, '{"hi": [1, 2, 3]}')

        with tempfile.NamedTemporaryFile("r", suffix=".json", delete=False) as handle:
            temp_path = handle.name

        try:
            written = JSON.stringify(payload, filepath=temp_path, sort_keys=True)
            self.assertEqual(written, '{"hi": [1, 2, 3]}')
            with open(temp_path, encoding="utf-8") as saved_file:
                self.assertEqual(saved_file.read(), written)
        finally:
            os.unlink(temp_path)

    def test_csvify_and_csv2json(self):
        data = [
            {"id": "01", "name": "Java"},
            {"name": "C++", "id": "07", "extra": "yes"},
        ]

        with tempfile.NamedTemporaryFile("r", suffix=".csv", delete=False) as handle:
            csv_path = handle.name

        try:
            returned_path = JSON.csvify(data, csv_path)
            self.assertEqual(returned_path, csv_path)
            with open(csv_path, encoding="utf-8") as csv_file:
                csv_text = csv_file.read()
            self.assertIn("id,name,extra", csv_text)
            self.assertIn("01,Java,", csv_text)
            self.assertIn("07,C++,yes", csv_text)

            payload = JSON.csv2json(csv_path)
            self.assertEqual(json.loads(payload)[1]["extra"], "yes")
        finally:
            os.unlink(csv_path)

    def test_flatten(self):
        flattened = JSON.flatten({"user": {"name": "domonic", "meta": {"role": "admin"}}})
        self.assertEqual(
            flattened,
            {"user__name": "domonic", "user__meta__role": "admin"},
        )

    def test_is_json(self):
        self.assertTrue(JSON.is_json('{"a": 1}'))
        self.assertTrue(JSON.is_json("[1, 2, 3]"))
        self.assertTrue(JSON.is_json(" true "))
        self.assertFalse(JSON.is_json("not json"))
        self.assertFalse(JSON.is_json(""))
        self.assertFalse(JSON.is_json(123))

    def test_as_json_decorator(self):
        @as_json
        def yo():
            return {"hi": [1, 2, 3]}

        self.assertEqual(yo(), '{"hi": [1, 2, 3]}')


if __name__ == "__main__":
    unittest.main()
