"""
    test_window
    ~~~~~~~~~~~~~~~~
"""

import unittest

from domonic.html import body, div
from domonic.window import MediaQueryList, Window


class TestCase(unittest.TestCase):
    def test_window_core_properties(self):
        win = Window()

        self.assertIs(win.document.defaultView, win)
        self.assertEqual(win.location.href, "https://eventual.technology")
        self.assertEqual(win.innerWidth, win.screen.width)
        self.assertEqual(win.innerHeight, win.screen.height)
        self.assertFalse(win.closed)

    def test_window_focus_close_and_name(self):
        win = Window()
        events = []

        win.addEventListener("focus", lambda event: events.append(event.type))
        win.addEventListener("blur", lambda event: events.append(event.type))
        win.focus()
        win.blur()
        win.name = "main"
        win.close()

        self.assertEqual(events, ["focus", "blur"])
        self.assertEqual(win.name, "main")
        self.assertTrue(win.closed)

    def test_window_computed_style_and_selection(self):
        win = Window()
        el = div()
        el.style.width = "120px"
        win.document.body = body(el)

        self.assertIs(win.getComputedStyle(el), el.style)
        self.assertIs(win.getSelection(), win.document.getSelection())

    def test_match_media_and_position_helpers(self):
        win = Window()
        query = win.matchMedia("(min-width: 800px)")

        self.assertIsInstance(query, MediaQueryList)
        self.assertTrue(query.matches)

        win.moveTo(5, 10)
        self.assertEqual((win.screenLeft, win.screenTop), (5, 10))

        win.moveBy(3, 4)
        self.assertEqual((win.screenLeft, win.screenTop), (8, 14))

    def test_location_assignment_without_network(self):
        win = Window()

        win.location = "example.com"

        self.assertEqual(win.location.href, "https://example.com")
        self.assertEqual(win.document.URL, "https://example.com")
        self.assertEqual(win.history.state, "https://example.com")


if __name__ == "__main__":
    unittest.main()
