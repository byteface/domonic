"""Ported from wpt/dom/events/ -- EventTarget-add-remove-listener.html,
Event-dispatch-bubbles.html, Event-dispatch-order.html,
Event-dispatch-propagation-stopped.html, AddEventListenerOptions-once.html and
EventListener-handleEvent.html.
https://dom.spec.whatwg.org/#interface-eventtarget
"""

import unittest

from domonic.dom import Document
from domonic.events import CustomEvent, Event, EventTarget

document = Document()


class EventTargetAddRemove(unittest.TestCase):
    def test_a_duplicate_listener_is_registered_once(self):
        t = EventTarget()
        calls = []
        fn = lambda e: calls.append(1)  # noqa: E731
        t.addEventListener("x", fn)
        t.addEventListener("x", fn)
        t.dispatchEvent(Event("x"))
        self.assertEqual(calls, [1])

    def test_capture_and_bubble_registrations_are_distinct(self):
        t = EventTarget()
        calls = []
        fn = lambda e: calls.append(e["phase"] if isinstance(e, dict) else 1)  # noqa: E731
        t.addEventListener("x", lambda e: calls.append("capture"), True)
        t.addEventListener("x", lambda e: calls.append("bubble"), False)
        t.dispatchEvent(Event("x"))
        self.assertEqual(sorted(calls), ["bubble", "capture"])

    def test_removeEventListener_stops_future_delivery(self):
        t = EventTarget()
        calls = []
        fn = lambda e: calls.append(1)  # noqa: E731
        t.addEventListener("x", fn)
        t.dispatchEvent(Event("x"))
        t.removeEventListener("x", fn)
        t.dispatchEvent(Event("x"))
        self.assertEqual(calls, [1])

    def test_a_listener_removed_mid_dispatch_is_not_called(self):
        t = EventTarget()
        calls = []

        def first(e):
            calls.append("first")
            t.removeEventListener("x", second)

        def second(e):
            calls.append("second")

        t.addEventListener("x", first)
        t.addEventListener("x", second)
        t.dispatchEvent(Event("x"))
        self.assertEqual(calls, ["first"])

    def test_handleEvent_objects_are_supported(self):
        t = EventTarget()
        seen = []

        class Handler:
            def handleEvent(self, event):
                seen.append(event.type)

        t.addEventListener("ping", Handler())
        t.dispatchEvent(Event("ping"))
        self.assertEqual(seen, ["ping"])


class EventDispatch(unittest.TestCase):
    def _tree(self):
        grandparent = document.createElement("gp")
        parent = document.createElement("p")
        child = document.createElement("c")
        grandparent.appendChild(parent)
        parent.appendChild(child)
        document.appendChild(grandparent)
        return grandparent, parent, child

    def test_capture_target_bubble_order_and_phases(self):
        gp, p, c = self._tree()
        log = []
        gp.addEventListener("e", lambda ev: log.append(("gp", ev.eventPhase)), True)
        p.addEventListener("e", lambda ev: log.append(("p", ev.eventPhase)), True)
        c.addEventListener("e", lambda ev: log.append(("c", ev.eventPhase)))
        p.addEventListener("e", lambda ev: log.append(("p-bubble", ev.eventPhase)))
        gp.addEventListener("e", lambda ev: log.append(("gp-bubble", ev.eventPhase)))
        c.dispatchEvent(Event("e", {"bubbles": True}))
        self.assertEqual(
            log,
            [
                ("gp", Event.CAPTURING_PHASE),
                ("p", Event.CAPTURING_PHASE),
                ("c", Event.AT_TARGET),
                ("p-bubble", Event.BUBBLING_PHASE),
                ("gp-bubble", Event.BUBBLING_PHASE),
            ],
        )

    def test_non_bubbling_event_stops_at_the_target(self):
        gp, p, c = self._tree()
        log = []
        gp.addEventListener("e", lambda ev: log.append("gp-bubble"))
        c.addEventListener("e", lambda ev: log.append("c"))
        c.dispatchEvent(Event("e", {"bubbles": False}))
        self.assertEqual(log, ["c"])

    def test_stopPropagation_prevents_bubbling(self):
        gp, p, c = self._tree()
        log = []
        c.addEventListener("e", lambda ev: (log.append("c"), ev.stopPropagation()))
        p.addEventListener("e", lambda ev: log.append("p"))
        c.dispatchEvent(Event("e", {"bubbles": True}))
        self.assertEqual(log, ["c"])

    def test_stopImmediatePropagation_prevents_later_listeners_on_the_same_target(self):
        t = EventTarget()
        log = []
        t.addEventListener("e", lambda ev: (log.append("a"), ev.stopImmediatePropagation()))
        t.addEventListener("e", lambda ev: log.append("b"))
        t.dispatchEvent(Event("e"))
        self.assertEqual(log, ["a"])

    def test_preventDefault_on_a_cancelable_event(self):
        t = EventTarget()
        t.addEventListener("e", lambda ev: ev.preventDefault())
        ev = Event("e", {"cancelable": True})
        result = t.dispatchEvent(ev)
        self.assertFalse(result)
        self.assertTrue(ev.defaultPrevented)

    def test_preventDefault_is_ignored_when_not_cancelable(self):
        t = EventTarget()
        t.addEventListener("e", lambda ev: ev.preventDefault())
        ev = Event("e", {"cancelable": False})
        result = t.dispatchEvent(ev)
        self.assertTrue(result)
        self.assertFalse(ev.defaultPrevented)


class AddEventListenerOnce(unittest.TestCase):
    def test_once_listener_fires_at_most_one_time(self):
        t = EventTarget()
        calls = []
        t.addEventListener("e", lambda ev: calls.append(1), {"once": True})
        t.dispatchEvent(Event("e"))
        t.dispatchEvent(Event("e"))
        self.assertEqual(calls, [1])


class CustomEventTest(unittest.TestCase):
    def test_detail_defaults_to_none_and_is_carried_through(self):
        self.assertIsNone(CustomEvent("x").detail)
        ev = CustomEvent("x", {"detail": {"k": 1}, "bubbles": True})
        self.assertEqual(ev.detail, {"k": 1})
        self.assertTrue(ev.bubbles)
        self.assertIsInstance(ev, Event)


if __name__ == "__main__":
    unittest.main()
