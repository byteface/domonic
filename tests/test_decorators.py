"""
    test_decorators
    ~~~~~~~~~~~~
    unit tests for the decorator methods
"""

import unittest
from unittest.mock import Mock
from domonic.decorators import (
    el,
    called,
    accepts,
    silence,
    check,
    log,
    instead,
    deprecated,
    as_json
)


class TestDecorators(unittest.TestCase):

    def test_el_decorator(self):
        @el("span")
        def return_text():
            return "Hello"
        
        result = return_text()
        self.assertTrue(result.startswith("<span>"))
        self.assertTrue(result.endswith("</span>"))
        self.assertIn("Hello", result)
    
    def test_el_with_string(self):
        @el("div", string=True)
        def return_text():
            return "Hello"
        
        result = return_text()
        self.assertTrue(result.startswith("<div>"))
        self.assertTrue(result.endswith("</div>"))
        self.assertIn("Hello", result)
    
    def test_called_decorator(self):
        before = Mock()
        after = Mock()

        @called(before=before, error=after)
        def simple_function():
            return "Done"

        result = simple_function()
        self.assertEqual(result, "Done")
        before.assert_called_once()
        after.assert_not_called()

    def test_called_with_error(self):
        before = Mock()
        error_handler = Mock()

        @called(before=before, error=error_handler)
        def function_with_error():
            raise ValueError("Error occurred")

        with self.assertRaises(ValueError):
            function_with_error()
        
        before.assert_called_once()
        error_handler.assert_called_once()

    def test_accepts_decorator(self):
        @accepts(int, str)
        def accept_types(x, y):
            return x, y
        
        result = accept_types(10, "Hello")
        self.assertEqual(result, (10, "Hello"))
        
        with self.assertRaises(AssertionError):
            accept_types("string", 10)

    def test_silence_decorator(self):
        @silence()
        def noisy_function():
            print("This should not print")
        
        noisy_function()  # Should not raise an exception or print anything

    def test_check_decorator(self):
        @check
        def sample_function():
            return "Checking"
        
        with self.assertLogs(level='INFO') as log:
            result = sample_function()
            self.assertIn("Entering", log.output[0])
            self.assertIn("Exited", log.output[1])

    def test_log_decorator(self):
        logger = Mock()
        @log(logger, level="warning")
        def simple_function():
            return "Logged"
        
        simple_function()
        logger.warning.assert_called_once_with("simple_function")

    def test_instead_decorator(self):
        @instead("Default Value")
        def function_that_fails():
            raise ValueError("This is an error")

        result = function_that_fails()
        self.assertEqual(result, "Default Value")

    def test_deprecated_decorator(self):
        @deprecated
        def deprecated_function():
            return "This is deprecated"

        with self.assertRaises(Warning):
            deprecated_function()

    def test_as_json_decorator(self):
        @as_json
        def return_dict():
            return {"key": "value"}
        
        result = return_dict()
        self.assertEqual(result, '{"key": "value"}')

    def test_empty_function(self):
        @el("div")
        def empty_function():
            pass

        result = empty_function()
        self.assertEqual(result, "<div></div>")


if __name__ == "__main__":
    unittest.main()
