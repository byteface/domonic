"""
    test_window
    ~~~~~~~~~~~~~~~~
"""

import threading
import time
import unittest

from domonic.events import CloseEvent
from domonic.html import body, div
from domonic.webapi.crypto import Crypto
from domonic.window import IdleDeadline, MediaQueryList, Window

from unittest.mock import patch

class TestCase(unittest.TestCase):
    def test_window_core_properties(self):
        win = Window()

        self.assertIs(win.document.defaultView, win)
        self.assertEqual(win.location.href, "https://eventual.technology")
        self.assertEqual(win.innerWidth, win.screen.width)
        self.assertEqual(win.innerHeight, win.screen.height)
        self.assertFalse(win.closed)
        self.assertIsInstance(win.crypto, Crypto)

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

            with patch.object(win, "_fetch_document", return_value=None):
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

    def test_window_identity_viewport_scroll_and_media_queries(self):
        win = Window()
        self.assertIs(win.window, win)
        self.assertIs(win.self, win)
        self.assertIs(win.frames, win)
        self.assertIs(win.parent, win)
        self.assertIs(win.top, win)
        self.assertEqual(win.length, 0)
        self.assertTrue(win.isSecureContext)
        self.assertIs(win.clientInformation, win.navigator)

        changes = []
        query = win.matchMedia("(min-width: 700px) and (orientation: landscape)")
        query.addEventListener("change", lambda event: changes.append((event.matches, event.media)))
        self.assertTrue(query.matches)

        resize_events = []
        win.addEventListener("resize", lambda event: resize_events.append(event.type))
        win.resizeTo(500, 800)
        self.assertEqual(win.innerWidth, 500)
        self.assertEqual(win.innerHeight, 800)
        self.assertEqual(win.outerWidth, 500)
        self.assertEqual(win.outerHeight, 800)
        self.assertEqual(resize_events, ["resize"])
        self.assertFalse(query.matches)
        self.assertEqual(changes, [(False, "(min-width: 700px) and (orientation: landscape)")])

        scroll_events = []
        win.addEventListener("scroll", lambda event: scroll_events.append((win.scrollX, win.scrollY)))
        win.scrollTo({"left": 10, "top": 20})
        win.scrollBy(5, -10)
        win.scrollByLines(1)
        self.assertEqual(win.scrollX, 15)
        self.assertEqual(win.scrollY, 50)
        self.assertEqual(win.pageXOffset, 15)
        self.assertEqual(win.pageYOffset, 50)
        self.assertEqual(scroll_events, [(10, 20), (15, 10), (15, 50)])

    def test_window_messaging_print_open_and_status(self):
        win = Window()
        messages = []
        printed = []
        win.onmessage = lambda event: messages.append((event.data, event.origin, event.source))
        win.addEventListener("beforeprint", lambda event: printed.append(event.type))
        win.addEventListener("afterprint", lambda event: printed.append(event.type))

        win.postMessage({"hello": "world"}, win.origin)
        self.assertEqual(messages, [({"hello": "world"}, win.origin, win)])

        win.print()
        self.assertEqual(printed, ["beforeprint", "afterprint"])

        win.status = "Ready"
        win.defaultStatus = "Idle"
        self.assertEqual(win.status, "Ready")
        self.assertEqual(win.defaultStatus, "Idle")

        child = win.open("about:blank")
        self.assertIs(child.opener, win)
        self.assertIs(child.parent, win)
        self.assertIs(child.top, win)
        self.assertEqual(child.location.href, "about:blank")
        self.assertIs(win.open("https://example.com", "_self"), win)
        self.assertEqual(win.location.href, "https://example.com")

    def test_window_microtask_animation_frame_and_idle_callbacks(self):
        win = Window()
        order = []
        win.queueMicrotask(lambda: order.append("first"))
        win.queueMicrotask(lambda: (order.append("second"), win.queueMicrotask(lambda: order.append("third"))))
        self.assertEqual(order, ["first", "second", "third"])

        raf_done = threading.Event()
        raf_times = []
        win.requestAnimationFrame(lambda timestamp: (raf_times.append(timestamp), raf_done.set()))
        self.assertTrue(raf_done.wait(0.25))
        self.assertEqual(len(raf_times), 1)
        self.assertGreaterEqual(raf_times[0], 0)

        cancelled = []
        request_id = win.requestAnimationFrame(lambda timestamp: cancelled.append(timestamp))
        win.cancelAnimationFrame(request_id)
        time.sleep(0.05)
        self.assertEqual(cancelled, [])

        idle_done = threading.Event()
        idle_deadlines = []
        win.requestIdleCallback(lambda deadline: (idle_deadlines.append(deadline), idle_done.set()))
        self.assertTrue(idle_done.wait(0.25))
        self.assertIsInstance(idle_deadlines[0], IdleDeadline)
        self.assertGreaterEqual(idle_deadlines[0].timeRemaining(), 0)

        idle_cancelled = []
        callback_id = win.requestIdleCallback(lambda deadline: idle_cancelled.append(deadline))
        win.cancelIdleCallback(callback_id)
        time.sleep(0.05)
        self.assertEqual(idle_cancelled, [])


if __name__ == "__main__":
    unittest.main()
