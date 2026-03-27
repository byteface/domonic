"""
    test_window
    ~~~~~~~~~~~~~~~~
"""

import unittest

from domonic.html import body, div
from domonic.events import CloseEvent
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
        close_events = []

        win.addEventListener("focus", lambda event: events.append(event.type))
        win.addEventListener("blur", lambda event: events.append(event.type))
        win.addEventListener("close", lambda event: close_events.append(event))
        win.focus()
        win.blur()
        win.name = "main"
        win.close()

        self.assertEqual(events, ["focus", "blur"])
        self.assertEqual(len(close_events), 1)
        self.assertIsInstance(close_events[0], CloseEvent)
        self.assertEqual(close_events[0].code, 1000)
        self.assertTrue(close_events[0].wasClean)
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
        self.assertEqual(win.document.referrer, "https://eventual.technology")
        self.assertEqual(win.history.state, "https://example.com")

    def test_document_metadata_properties_are_window_backed(self):
        win = Window()

        self.assertIs(win.document.defaultView, win)
        self.assertEqual(win.document.designMode, "off")

        win.document.designMode = "on"
        self.assertEqual(win.document.designMode, "on")

        win.document.cookie = "session=abc123"
        win.document.cookie = "theme=dark"
        self.assertIn("session=abc123", win.document.cookie)
        self.assertIn("theme=dark", win.document.cookie)

    def test_hashchange_and_popstate_events(self):
        win = Window()
        events = []

        win.addEventListener("hashchange", lambda event: events.append((event.type, event.oldURL, event.newURL)))
        win.addEventListener("popstate", lambda event: events.append((event.type, event.state)))

        win.location = "https://example.com#one"
        win.location = "https://example.com#two"
        win.history.back()

        self.assertIn(("hashchange", "https://example.com#one", "https://example.com#two"), events)
        self.assertIn(("popstate", "https://example.com#one"), events)

    def test_navigator_basic_specish_helpers(self):
        win = Window()

        self.assertEqual(win.navigator.registerProtocolHandler("mailto", "/compose", "Mail"), None)
        self.assertEqual(win.navigator.requestMediaKeySystemAccess("org.example", []), None)
        self.assertEqual(win.navigator.clearAppBadge(), None)
        self.assertEqual(win.navigator.getBattery()["level"], 1.0)
        self.assertFalse(win.navigator.vibrate([100]))


if __name__ == "__main__":
    unittest.main()
