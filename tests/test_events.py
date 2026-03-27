"""
    test_events
    ~~~~~~~~~~~~
    - unit tests for events

"""

import asyncio
import unittest

from domonic import *
from domonic.dom import document
from domonic.events import *

class TestCase(unittest.TestCase):
    """Tests for the events classes"""

    def test_html_structure(self):
        site = html()
        somebody = document.createElement("div")
        site.appendChild(somebody)
        self.assertEqual(str(site), "<html><div></div></html>")

    def test_event_handling(self):
        site = html()
        somebody = document.createElement("div")
        site.appendChild(somebody)

        event_results = []

        def test(evt, *args, **kwargs):
            event_results.append(evt.target)

        site.addEventListener("click", test)
        somebody.addEventListener("anything", test)

        self.assertIn("click", site.listeners)
        self.assertEqual(site.listeners["click"], [test])

        site.dispatchEvent(Event("click"))
        somebody.dispatchEvent(Event("anything"))

        self.assertIn(somebody, event_results)
        self.assertIn(site, event_results)

    def test_events(self):
        site = EventTarget()
        somebody = EventTarget()

        def test(evt, *args, **kwargs):
            self.assertTrue(evt.target == somebody or evt.target == site)

        async def async_test(evt, *args, **kwargs):
            await asyncio.sleep(0)
            self.assertTrue(evt.target == somebody or evt.target == site)

        site.addEventListener("click", test)
        somebody.addEventListener("anything", test)

        site.dispatchEvent(Event("click"))
        somebody.dispatchEvent(Event("anything"))

        # Asynchronous event handling
        site.addEventListener("async_event", async_test)
        asyncio.run(site.dispatchEventAsync(Event("async_event")))

    def test_async_events(self):
        async def runner():
            site = EventTarget()
            somebody = EventTarget()

            async def async_test(evt, *args, **kwargs):
                await asyncio.sleep(0)
                self.assertTrue(evt.target == somebody or evt.target == site)

            site.addEventListener("click", async_test)
            somebody.addEventListener("anything", async_test)

            await site.dispatchEventAsync(Event("click"))
            await somebody.dispatchEventAsync(Event("anything"))

        asyncio.run(runner())

    def test_default_event_properties(self):
        event = Event("custom_event")
        self.assertIsNone(event.target)
        self.assertFalse(event.defaultPrevented)
        self.assertEqual(event.eventPhase, Event.AT_TARGET)

    def test_custom_event_properties(self):
        # Define custom event data
        event_data = {"message": "Hello, world!"}

        # Create a custom event
        event = Event("custom_event")
        event.custom_data = event_data

        # Test custom event properties
        self.assertEqual(event.type, "custom_event")
        self.assertTrue(event.bubbles)
        self.assertTrue(event.cancelable)
        self.assertEqual(event.eventPhase, Event.AT_TARGET)
        self.assertIsInstance(event.timeStamp, (int, float))
        self.assertEqual(event.custom_data, event_data)

    def test_prevent_default(self):
        event = Event("custom_event")
        event.preventDefault()
        self.assertTrue(event.defaultPrevented)

    def test_stop_propagation(self):
        event = Event("custom_event")
        event.stopImmediatePropagation()
        self.assertTrue(event.cancelBubble)

    def test_prevent_default_respects_cancelable(self):
        event = Event("custom_event", {"cancelable": False})
        event.preventDefault()
        self.assertFalse(event.defaultPrevented)

    def test_event_bubbling(self):
        # Create an event target and some event handlers
        target = EventTarget()
        results = []

        def event_handler1(event):
            results.append("Handler 1")

        def event_handler2(event):
            results.append("Handler 2")

        def event_handler3(event):
            results.append("Handler 3")

        # Add event listeners for a custom event
        target.addEventListener("custom_event", event_handler1)
        target.addEventListener("custom_event", event_handler2)
        target.addEventListener("custom_event", event_handler3)

        # Create a custom event
        event_data = {"message": "Hello, world!"}
        custom_event = Event("custom_event", data=event_data)

        # Dispatch the event
        target.dispatchEvent(custom_event)

        # Check if event bubbling occurred in the correct order
        expected_results = ["Handler 1", "Handler 2", "Handler 3"]
        self.assertEqual(results, expected_results)

    def test_event_bubbles_to_parent_targets(self):
        parent = EventTarget()
        child = EventTarget()
        child.parentNode = parent
        results = []

        parent.addEventListener("custom_event", lambda event: results.append(("parent", event.eventPhase)))
        child.addEventListener("custom_event", lambda event: results.append(("child", event.eventPhase)))

        child.dispatchEvent(Event("custom_event", {"bubbles": True}))

        self.assertEqual(results, [("child", Event.AT_TARGET), ("parent", Event.BUBBLING_PHASE)])

    def test_event_target_with_target_matching(self):
        # Create an event target and some event handlers
        target = EventTarget()
        results = []

        def event_handler1(event):
            results.append("Handler 1")

        def event_handler2(event):
            results.append("Handler 2")

        def event_handler3(event):
            results.append("Handler 3")

        def specific_target_handler(event):
            results.append("Specific Target Handler")

        # Add event listeners for custom events with different targets
        target.addEventListener("custom_event", event_handler1)
        target.addEventListener("custom_event", event_handler2)
        target.addEventListener("custom_event", event_handler3)

        specific_target = EventTarget()
        specific_target.addEventListener("custom_event", specific_target_handler)

        # Create a custom event with a specific target
        event_data = {"message": "Hello, world!"}
        custom_event = Event("custom_event", data=event_data)

        # Dispatch the event on the specific target
        specific_target.dispatchEvent(custom_event)

        # Check if the event only triggered the specific target handler
        expected_results = ["Specific Target Handler"]
        self.assertEqual(results, expected_results)

    def test_event_capture_phase(self):
        # Create an event target and some event handlers
        target = EventTarget()
        results = []

        def capture_handler1(event):
            results.append("Capture Handler 1")

        def capture_handler2(event):
            results.append("Capture Handler 2")

        def capture_handler3(event):
            results.append("Capture Handler 3")

        def bubble_handler(event):
            results.append("Bubble Handler")

        # Add event listeners for custom events with the capture phase
        target.addEventListener("custom_event", capture_handler1, use_capture=True)
        target.addEventListener("custom_event", capture_handler2, use_capture=True)
        target.addEventListener("custom_event", capture_handler3, use_capture=True)
        target.addEventListener("custom_event", bubble_handler)

        # Create a custom event
        event_data = {"message": "Hello, world!"}
        custom_event = Event("custom_event", data=event_data)

        # Dispatch the event
        target.dispatchEvent(custom_event)

        # Check if the event listeners in the capture phase were executed in order
        expected_results = ["Capture Handler 1", "Capture Handler 2", "Capture Handler 3", "Bubble Handler"]
        self.assertEqual(results, expected_results)

    def test_capture_and_bubble_order_across_path(self):
        root = EventTarget()
        parent = EventTarget()
        child = EventTarget()
        parent.parentNode = root
        child.parentNode = parent
        results = []

        root.addEventListener("custom_event", lambda event: results.append("root-capture"), {"capture": True})
        parent.addEventListener("custom_event", lambda event: results.append("parent-capture"), {"capture": True})
        child.addEventListener("custom_event", lambda event: results.append("child-capture"), {"capture": True})
        child.addEventListener("custom_event", lambda event: results.append("child-bubble"))
        parent.addEventListener("custom_event", lambda event: results.append("parent-bubble"))

        child.dispatchEvent(Event("custom_event", {"bubbles": True}))

        self.assertEqual(
            results,
            ["root-capture", "parent-capture", "child-capture", "child-bubble", "parent-bubble"],
        )

    def test_once_listener_is_removed_after_first_dispatch(self):
        target = EventTarget()
        calls = []

        target.addEventListener("custom_event", lambda event: calls.append(event.type), {"once": True})

        target.dispatchEvent(Event("custom_event"))
        target.dispatchEvent(Event("custom_event"))

        self.assertEqual(calls, ["custom_event"])

    def test_stop_immediate_propagation_stops_remaining_listeners(self):
        target = EventTarget()
        calls = []

        def first(event):
            calls.append("first")
            event.stopImmediatePropagation()

        def second(event):
            calls.append("second")

        target.addEventListener("custom_event", first)
        target.addEventListener("custom_event", second)

        target.dispatchEvent(Event("custom_event"))

        self.assertEqual(calls, ["first"])

    def test_ui_event_initialization(self):
        event_data = {
            "canBubble": True,
            "cancelable": True,
            "view": "main_window",
            "detail": "click_detail",
            "layerX": 10,
            "layerY": 20,
            "sourceCapabilities": "capabilities"
        }

        ui_event = UIEvent(Event.RESIZE, **event_data)

        self.assertEqual(ui_event.type, "resize")
        self.assertEqual(ui_event.canBubble, True)
        self.assertEqual(ui_event.cancelable, True)
        self.assertEqual(ui_event.view, "main_window")
        self.assertEqual(ui_event.detail, "click_detail")
        self.assertEqual(ui_event.layerX, 10)
        self.assertEqual(ui_event.layerY, 20)
        self.assertEqual(ui_event.sourceCapabilities, "capabilities")

    def test_composed_path(self):
        # Create an event target hierarchy
        root = EventTarget()
        parent = EventTarget()
        child = EventTarget()

        # Simulate the hierarchy
        child.parentNode = parent
        parent.parentNode = root

        # Create a UIEvent and set the target
        event_data = {"type": "click"}
        ui_event = UIEvent("click", options=event_data)
        ui_event.target = child

        # Get the composed path
        path = ui_event.composedPath()

        # Check if the path includes the expected elements in the correct order
        expected_path = [child, parent, root]
        self.assertEqual(path, expected_path)

    def test_custom_event_detail(self):
        event = CustomEvent("custom_event", {"detail": {"message": "hello"}})
        self.assertEqual(event.detail, {"message": "hello"})

    def test_submit_event_submitter(self):
        submitter = object()
        event = SubmitEvent("submit", {"submitter": submitter})
        self.assertIs(event.submitter, submitter)

    def test_mouse_event_client_coordinates_and_modifiers(self):
        event = MouseEvent("click", {"clientX": 10, "clientY": 20, "ctrlKey": True})
        self.assertEqual(event.clientX, 10)
        self.assertEqual(event.clientY, 20)
        self.assertTrue(event.getModifierState("Control"))

    def test_document_create_event_specializations(self):
        self.assertIsInstance(document.createEvent("MouseEvent"), MouseEvent)
        self.assertIsInstance(document.createEvent("KeyboardEvent"), KeyboardEvent)
        self.assertIsInstance(document.createEvent("CustomEvent"), CustomEvent)
        self.assertIsInstance(document.createEvent("PointerEvent"), PointerEvent)
        self.assertIsInstance(document.createEvent("WheelEvent"), WheelEvent)
        self.assertIsInstance(document.createEvent("MessageEvent"), MessageEvent)

    def test_handle_event_listener_object(self):
        target = EventTarget()
        calls = []

        class Handler:
            def handleEvent(self, event):
                calls.append(event.type)

        target.addEventListener("custom_event", Handler())
        target.dispatchEvent(Event("custom_event"))

        self.assertEqual(calls, ["custom_event"])

    def test_passive_listener_cannot_prevent_default(self):
        target = EventTarget()

        def listener(event):
            event.preventDefault()

        target.addEventListener("custom_event", listener, {"passive": True})
        event = Event("custom_event")
        target.dispatchEvent(event)

        self.assertFalse(event.defaultPrevented)

    def test_long_tail_event_data_helpers(self):
        custom_event = CustomEvent("custom")
        custom_event.initCustomEvent("customized", bubbles=False, cancelable=True, detail={"ok": True})
        self.assertEqual(custom_event.type, "customized")
        self.assertEqual(custom_event.detail, {"ok": True})
        self.assertFalse(custom_event.bubbles)

        transition = TransitionEvent("transitionend", {"propertyName": "opacity", "elapsedTime": 0.25})
        self.assertEqual(transition.propertyName, "opacity")
        self.assertEqual(transition.elapsedTime, 0.25)

        request = type("Request", (), {"url": "/a", "referrer": "/a", "clientId": "c1"})()
        fetch_event = FetchEvent("fetch", {"request": request, "clientId": "c2"})
        self.assertTrue(fetch_event.isReload)
        self.assertTrue(fetch_event.replacesClientId)
        self.assertEqual(fetch_event.resultingClientId, "c2")
        self.assertEqual(fetch_event.respondWith("response"), "response")

        marker = object()
        extendable = ExtendableEvent("extendable")
        self.assertIs(extendable.waitUntil(marker), marker)
        self.assertEqual(extendable._pending_promises, [marker])

        promise_event = PromiseRejectionEvent("unhandledrejection", {"reason": "boom", "isRejected": True})
        self.assertEqual(promise_event.reason, "boom")
        self.assertTrue(promise_event.isRejected)

        message = MessageEvent("message", {"data": "hi", "ports": [1, 2]})
        self.assertEqual(message.data, "hi")
        self.assertEqual(message.ports, [1, 2])

    def test_default_global_and_window_event_handlers_do_not_throw(self):
        global_handler = GlobalEventHandler()
        click_event = Event("click")
        self.assertIs(global_handler.onclick(click_event), click_event)
        self.assertEqual(global_handler.onkeydown(Event("keydown")).type, "keydown")

        win = WindowEventHandler(window=None)
        resize_event = Event("resize")
        self.assertIs(win.onresize(resize_event), resize_event)
        self.assertEqual(win._last_event.type, "resize")

    def test_event_init_helpers_and_subclass_shape(self):
        ui_event = UIEvent("resize").initUIEvent("scroll", True, False, "view", 2)
        self.assertEqual(ui_event.type, "scroll")
        self.assertTrue(ui_event.bubbles)
        self.assertFalse(ui_event.cancelable)

        mouse_event = MouseEvent("click").initMouseEvent("mousedown", True, True, None, 1, 0, 0, 11, 22, True, False, False, False, 1, None)
        self.assertEqual(mouse_event.type, "mousedown")
        self.assertEqual(mouse_event.clientX, 11)
        self.assertTrue(mouse_event.ctrlKey)

        keyboard_event = KeyboardEvent("keydown").initKeyboardEvent("keyup", True, True, None, 65, "A", 0, "", False)
        self.assertEqual(keyboard_event.type, "keyup")
        self.assertEqual(keyboard_event.key, "A")
        self.assertEqual(keyboard_event.charCode, 65)

        pointer_event = PointerEvent("pointerdown", {"clientX": 5, "clientY": 6, "pointerId": 3})
        self.assertEqual(pointer_event.clientX, 5)
        self.assertEqual(pointer_event.pointerId, 3)

        error_event = ErrorEvent("error", {"message": "boom", "filename": "x.py", "lineno": 4, "colno": 2})
        self.assertEqual(error_event.filename, "x.py")
        self.assertEqual(error_event.lineno, 4)

    def test_dispatch_does_not_swallow_listener_exceptions(self):
        target = EventTarget()

        def boom(event):
            raise RuntimeError("boom")

        target.addEventListener("custom_event", boom)
        with self.assertRaises(RuntimeError):
            target.dispatchEvent(Event("custom_event"))

if __name__ == '__main__':
    unittest.main()
