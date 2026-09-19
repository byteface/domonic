"""
test_window
~~~~~~~~~~~~~~~~
"""

import threading
import time
import unittest
from unittest.mock import patch

from domonic.events import CloseEvent
from domonic.dom import Document
from domonic.html import body, div
from domonic.webapi.crypto import Crypto
from domonic.webapi.scheduler import Scheduler
from domonic.window import IdleDeadline, MediaQueryList, Window


class TestCase(unittest.TestCase):
    def test_window_core_properties(self):
        win = Window()

        self.assertIs(win.document.defaultView, win)
        self.assertEqual(win.location.href, "https://eventual.technology")
        self.assertEqual(win.innerWidth, win.screen.width)
        self.assertEqual(win.innerHeight, win.screen.height)
        self.assertFalse(win.closed)
        self.assertIsInstance(win.crypto, Crypto)
        self.assertIsInstance(win.scheduler, Scheduler)

    def test_window_attach_rewires_document_relationships(self):
        win = Window()
        old_doc = win.document
        new_doc = Document()

        self.assertIs(win.attach(new_doc), new_doc)
        self.assertIs(win.document, new_doc)
        self.assertIs(new_doc.defaultView, win)
        self.assertIsNone(old_doc.defaultView)

        other = Window()
        self.assertIs(other.attach(new_doc), new_doc)
        self.assertIs(other.document, new_doc)
        self.assertIs(new_doc.defaultView, other)
        self.assertIsNone(win.document)

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

        computed = win.getComputedStyle(el)
        # a distinct, read-only declaration that resolves through the cascade
        self.assertIsNot(computed, el.style)
        self.assertEqual(computed.getPropertyValue("width"), "120px")
        self.assertEqual(computed.getPropertyValue("display"), "inline")
        with self.assertRaises(Exception):
            computed.setProperty("width", "10px")
        self.assertIs(win.getSelection(), win.document.getSelection())

    def test_match_media_and_position_helpers(self):
        win = Window()
        query = win.matchMedia("(min-width: 800px)")

        self.assertIsInstance(query, MediaQueryList)
        self.assertTrue(query.matches)

    def test_match_media_range_and_preference_features(self):
        win = Window()
        win.resizeTo(800, 600)

        self.assertTrue(win.matchMedia("(width >= 800px)").matches)
        self.assertFalse(win.matchMedia("(width > 800px)").matches)
        self.assertTrue(win.matchMedia("(400px <= width <= 900px)").matches)
        self.assertFalse(win.matchMedia("(400px <= width < 800px)").matches)

        # discrete preference features default to a typical desktop browser
        self.assertTrue(win.matchMedia("(prefers-color-scheme: light)").matches)
        self.assertFalse(win.matchMedia("(prefers-color-scheme: dark)").matches)
        self.assertTrue(
            win.matchMedia("(prefers-reduced-motion: no-preference)").matches
        )
        self.assertFalse(win.matchMedia("(hover: none)").matches)

        # ...and are overridable per session
        win.mediaFeatures["prefers-color-scheme"] = "dark"
        self.assertTrue(win.matchMedia("(prefers-color-scheme: dark)").matches)

        win.devicePixelRatio = 2
        self.assertTrue(win.matchMedia("(min-resolution: 2dppx)").matches)
        self.assertTrue(win.matchMedia("(resolution >= 96dpi)").matches)

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

        win.addEventListener(
            "hashchange",
            lambda event: events.append((event.type, event.oldURL, event.newURL)),
        )
        win.addEventListener(
            "popstate", lambda event: events.append((event.type, event.state))
        )

        win.location = "https://example.com#one"
        win.location = "https://example.com#two"
        win.history.back()

        self.assertIn(
            ("hashchange", "https://example.com#one", "https://example.com#two"), events
        )
        self.assertIn(("popstate", "https://example.com#one"), events)

    def test_navigator_basic_specish_helpers(self):
        win = Window()

        self.assertEqual(
            win.navigator.registerProtocolHandler("mailto", "/compose", "Mail"), None
        )
        self.assertEqual(
            win.navigator.requestMediaKeySystemAccess("org.example", []), None
        )
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
        query.addEventListener(
            "change", lambda event: changes.append((event.matches, event.media))
        )
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
        self.assertEqual(
            changes, [(False, "(min-width: 700px) and (orientation: landscape)")]
        )

        scroll_events = []
        win.addEventListener(
            "scroll", lambda event: scroll_events.append((win.scrollX, win.scrollY))
        )
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
        win.onmessage = lambda event: messages.append(
            (event.data, event.origin, event.source)
        )
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
        win.queueMicrotask(
            lambda: (
                order.append("second"),
                win.queueMicrotask(lambda: order.append("third")),
            )
        )
        self.assertEqual(order, ["first", "second", "third"])

        raf_done = threading.Event()
        raf_times = []
        win.requestAnimationFrame(
            lambda timestamp: (raf_times.append(timestamp), raf_done.set())
        )
        self.assertTrue(raf_done.wait(0.25))
        self.assertEqual(len(raf_times), 1)
        self.assertGreaterEqual(raf_times[0], 0)

        cancelled = []
        request_id = win.requestAnimationFrame(
            lambda timestamp: cancelled.append(timestamp)
        )
        win.cancelAnimationFrame(request_id)
        time.sleep(0.05)
        self.assertEqual(cancelled, [])

        idle_done = threading.Event()
        idle_deadlines = []
        win.requestIdleCallback(
            lambda deadline: (idle_deadlines.append(deadline), idle_done.set())
        )
        self.assertTrue(idle_done.wait(0.25))
        self.assertIsInstance(idle_deadlines[0], IdleDeadline)
        self.assertGreaterEqual(idle_deadlines[0].timeRemaining(), 0)

        idle_cancelled = []
        callback_id = win.requestIdleCallback(
            lambda deadline: idle_cancelled.append(deadline)
        )
        win.cancelIdleCallback(callback_id)
        time.sleep(0.05)
        self.assertEqual(idle_cancelled, [])

    def test_attach_host_calls_attach_and_exposes_native(self):
        win = Window()
        calls = []

        class Host:
            def attach(self, window):
                calls.append(("attach", window))

            def detach(self, window):
                calls.append(("detach", window))

        host = Host()
        self.assertIs(win.attach_host(host), host)
        self.assertIs(win.native, host)
        self.assertEqual(calls, [("attach", win)])

        # re-attaching the same host is a no-op
        self.assertIs(win.attach_host(host), host)
        self.assertEqual(calls, [("attach", win)])

        self.assertIs(win.detach_host(), host)
        self.assertIsNone(win.native)
        self.assertEqual(calls, [("attach", win), ("detach", win)])

        # detaching again is a no-op
        self.assertIsNone(win.detach_host())
        self.assertEqual(calls, [("attach", win), ("detach", win)])

    def test_attach_host_swap_detaches_previous_host(self):
        win = Window()
        calls = []

        class Host:
            def __init__(self, name):
                self.name = name

            def attach(self, window):
                calls.append(("attach", self.name))

            def detach(self, window):
                calls.append(("detach", self.name))

        first, second = Host("first"), Host("second")
        win.attach_host(first)
        win.attach_host(second)

        self.assertIs(win.native, second)
        self.assertEqual(calls, [("attach", "first"), ("detach", "first"), ("attach", "second")])

    def test_attach_host_rolls_back_on_attach_failure(self):
        win = Window()

        class BadHost:
            def attach(self, window):
                raise RuntimeError("boom")

        with self.assertRaises(RuntimeError):
            win.attach_host(BadHost())
        self.assertIsNone(win.native)

    def test_close_focus_blur_delegate_to_host(self):
        win = Window()
        calls = []

        class Host:
            def close(self):
                calls.append("close")

            def focus(self):
                calls.append("focus")

            def blur(self):
                calls.append("blur")

        win.attach_host(Host())

        events = []
        win.addEventListener("close", lambda event: events.append(event.type))
        win.addEventListener("focus", lambda event: events.append(event.type))
        win.addEventListener("blur", lambda event: events.append(event.type))

        win.close()
        win.focus()
        win.blur()

        self.assertEqual(calls, ["close", "focus", "blur"])
        # close() falls back to dispatching synchronously when the host
        # never confirms via _host_closed(); focus()/blur() do not, since a
        # host that owns focus is expected to report back itself
        self.assertEqual(events, ["close"])
        self.assertTrue(win.closed)

    def test_close_falls_back_when_host_never_confirms(self):
        win = Window()

        class SilentHost:
            def close(self):
                pass  # never calls window._host_closed()

        win.attach_host(SilentHost())
        events = []
        win.addEventListener("close", lambda event: events.append(event.type))

        win.close()

        self.assertEqual(events, ["close"])
        self.assertTrue(win.closed)

    def test_resize_and_move_delegate_to_host(self):
        win = Window()
        calls = []

        class Host:
            def resize(self, width, height):
                calls.append(("resize", width, height))

            def move_to(self, x, y):
                calls.append(("move_to", x, y))

        win.attach_host(Host())
        resize_events = []
        win.addEventListener("resize", lambda event: resize_events.append(event.type))

        win.resizeTo(640, 480)
        win.moveTo(20, 30)

        self.assertEqual(calls, [("resize", 640, 480), ("move_to", 20, 30)])
        # the host owns dispatching resize; Domonic does not act until the
        # host reports back via _host_resized()
        self.assertEqual(resize_events, [])
        self.assertEqual(win.innerWidth, win.screen.width)

        win._host_resized(640, 480)
        self.assertEqual((win.innerWidth, win.innerHeight), (640, 480))
        self.assertEqual(resize_events, ["resize"])

        win._host_moved(20, 30)
        self.assertEqual((win.screenLeft, win.screenTop), (20, 30))

    def test_animation_frame_and_open_delegate_to_host(self):
        win = Window()
        calls = []

        class Host:
            def request_animation_frame(self, callback):
                calls.append(("request_animation_frame", callback))
                return 99

            def cancel_animation_frame(self, request_id):
                calls.append(("cancel_animation_frame", request_id))

            def open_window(self, url, target, features, replace, opener):
                calls.append(("open_window", url, target))
                return "child-from-host"

        win.attach_host(Host())

        request_id = win.requestAnimationFrame(lambda timestamp: None)
        self.assertEqual(request_id, 99)
        win.cancelAnimationFrame(request_id)

        self.assertEqual(win.open("https://example.com", "_blank"), "child-from-host")
        self.assertEqual(calls[0][0], "request_animation_frame")
        self.assertEqual(calls[1], ("cancel_animation_frame", 99))
        self.assertEqual(calls[2], ("open_window", "https://example.com", "_blank"))

    def test_host_focus_blur_close_callbacks_dispatch_once(self):
        win = Window()
        events = []
        win.addEventListener("focus", lambda event: events.append(event.type))
        win.addEventListener("blur", lambda event: events.append(event.type))
        win.addEventListener("close", lambda event: events.append(event.type))

        # already focused by default; a redundant focus callback dispatches nothing
        win._host_focused()
        self.assertEqual(events, [])

        win._host_blurred()
        win._host_blurred()  # repeated callback is de-duplicated
        self.assertEqual(events, ["blur"])

        win._host_focused()
        self.assertEqual(events, ["blur", "focus"])

        win._host_closed()
        win._host_closed()  # repeated callback is de-duplicated
        self.assertEqual(events, ["blur", "focus", "close"])
        self.assertTrue(win.closed)

    def test_host_scale_changed_updates_device_pixel_ratio(self):
        win = Window()
        win.resizeTo(800, 600)

        self.assertFalse(win.matchMedia("(min-resolution: 2dppx)").matches)
        win._host_scale_changed(2.0)
        self.assertEqual(win.devicePixelRatio, 2.0)
        self.assertTrue(win.matchMedia("(min-resolution: 2dppx)").matches)


if __name__ == "__main__":
    unittest.main()
