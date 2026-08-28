"""
test_templates
~~~~~~~~~~~~
tests for templates
"""

import unittest

from domonic.templates import (blank_page, maintenance_page, message_page,
                               redirect_page, runtime_page, status_page)


class TestTemplates(unittest.TestCase):
    def test_status_page_whole_page(self):
        page = str(status_page(404))
        self.assertIn("<title>404</title>", page)
        self.assertIn("<h1>404</h1>", page)
        self.assertIn("Not Found", page)

    def test_status_page_fragment(self):
        page = str(status_page(401, False))
        stripped = page.lstrip()
        self.assertTrue(stripped.startswith("<body>") or stripped.startswith("<div"))
        self.assertIn("Unauthorized", page)

    def test_blank_page(self):
        page = str(blank_page("Hello", "Hi there"))
        self.assertIn("<title>Hello</title>", page)
        self.assertIn("Hi there", page)

    def test_message_page(self):
        page = str(
            message_page("Heads Up", "Notice", "Something happened", "Traceback info")
        )
        self.assertIn("<title>Heads Up</title>", page)
        self.assertIn("Something happened", page)
        self.assertIn("Traceback info", page)

    def test_redirect_page(self):
        page = str(redirect_page("/next", 5))
        self.assertIn('http-equiv="refresh"', page)
        self.assertIn('content="5;url=/next"', page)
        self.assertIn("Redirecting", page)

    def test_maintenance_page(self):
        page = str(maintenance_page("10 minutes"))
        self.assertIn("Service Unavailable", page)
        self.assertIn("Retry after: 10 minutes", page)

    def test_runtime_page(self):
        page = str(runtime_page())
        self.assertIn("Runtime Information", page)
        self.assertIn("Working Directory", page)
        self.assertIn("Process ID", page)

    def test_runtime_page_with_environment(self):
        page = str(runtime_page(include_environment=True))
        self.assertIn("Environment", page)
        self.assertIn('id="environment-info"', page)


if __name__ == "__main__":
    unittest.main()
