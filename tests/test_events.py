"""
test_events
~~~~~~~~~~~~
- unit tests for events

"""

import asyncio
import unittest

from domonic import *
from domonic.dom import Range, document
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

    def test_modern_html_event_types(self):
        self.assertEqual(Event.ADDTRACK, "addtrack")
        self.assertEqual(Event.DATAAVAILABLE, "dataavailable")
        self.assertEqual(Event.BEFOREMATCH, "beforematch")
        self.assertEqual(Event.BEFORETOGGLE, "beforetoggle")
        self.assertEqual(Event.DEVICEMOTION, "devicemotion")
        self.assertEqual(Event.DEVICEORIENTATION, "deviceorientation")
        self.assertEqual(Event.DOMCONTENTLOADED, "DOMContentLoaded")
        self.assertEqual(Event.BEFOREINPUT, "beforeinput")
        self.assertEqual(Event.CURRENTENTRYCHANGE, "currententrychange")
        self.assertEqual(Event.COMMAND, "command")
        self.assertEqual(Event.CONTEXTLOST, "contextlost")
        self.assertEqual(Event.CONTEXTRESTORED, "contextrestored")
        self.assertEqual(Event.CLICK, "click")
        self.assertEqual(Event.MESSAGEERROR, "messageerror")
        self.assertEqual(Event.NAVIGATE, "navigate")
        self.assertEqual(Event.NAVIGATEERROR, "navigateerror")
        self.assertEqual(Event.NAVIGATESUCCESS, "navigatesuccess")
        self.assertEqual(Event.PAGEREVEAL, "pagereveal")
        self.assertEqual(Event.PAGESWAP, "pageswap")
        self.assertEqual(Event.REMOVETRACK, "removetrack")
        self.assertEqual(Event.SCROLLEND, "scrollend")
        self.assertEqual(Event.SLOTCHANGE, "slotchange")
        self.assertEqual(Event.TOOLACTIVATED, "toolactivated")
        self.assertEqual(Event.TOOLCANCEL, "toolcancel")
        self.assertEqual(Event.TOOLCHANGE, "toolchange")
        self.assertEqual(Event.WEBGLCONTEXTLOST, "webglcontextlost")
        self.assertIn("onbeforematch", GlobalEventHandler._handler_names)
        self.assertIn("onbeforetoggle", GlobalEventHandler._handler_names)
        self.assertIn("onbeforeinput", GlobalEventHandler._handler_names)
        self.assertIn("oncommand", GlobalEventHandler._handler_names)
        self.assertIn("oncurrententrychange", GlobalEventHandler._handler_names)
        self.assertIn("onmessageerror", GlobalEventHandler._handler_names)
        self.assertIn("onnavigate", GlobalEventHandler._handler_names)
        self.assertIn("onreadystatechange", GlobalEventHandler._handler_names)
        self.assertIn("onscrollend", GlobalEventHandler._handler_names)
        self.assertIn("onslotchange", GlobalEventHandler._handler_names)
        self.assertIn("ontoolactivated", GlobalEventHandler._handler_names)
        self.assertIn("ontoolcancel", GlobalEventHandler._handler_names)
        self.assertIn("ontoolchange", WindowEventHandler._handler_names)
        self.assertIn("ontoggle", GlobalEventHandler._handler_names)
        self.assertIn("onvisibilitychange", WindowEventHandler._handler_names)

        toggle_event = ToggleEvent(
            ToggleEvent.BEFORETOGGLE,
            oldState="closed",
            newState="open",
            source="button",
        )
        self.assertEqual(toggle_event.oldState, "closed")
        self.assertEqual(toggle_event.newState, "open")
        self.assertEqual(toggle_event.source, "button")

        command_event = CommandEvent(
            CommandEvent.COMMAND, command="show-modal", source="button"
        )
        self.assertEqual(command_event.command, "show-modal")
        self.assertEqual(command_event.source, "button")

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
        self.assertEqual(event.eventPhase, Event.NONE)
        self.assertFalse(event.bubbles)
        self.assertFalse(event.cancelable)

    def test_custom_event_properties(self):
        # Define custom event data
        event_data = {"message": "Hello, world!"}

        # Create a custom event
        event = Event("custom_event")
        event.custom_data = event_data

        # Test custom event properties
        self.assertEqual(event.type, "custom_event")
        self.assertFalse(event.bubbles)
        self.assertFalse(event.cancelable)
        self.assertEqual(event.eventPhase, Event.NONE)
        self.assertIsInstance(event.timeStamp, (int, float))
        self.assertEqual(event.custom_data, event_data)

    def test_prevent_default(self):
        event = Event("custom_event", {"cancelable": True})
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

        parent.addEventListener(
            "custom_event", lambda event: results.append(("parent", event.eventPhase))
        )
        child.addEventListener(
            "custom_event", lambda event: results.append(("child", event.eventPhase))
        )

        child.dispatchEvent(Event("custom_event", {"bubbles": True}))

        self.assertEqual(
            results, [("child", Event.AT_TARGET), ("parent", Event.BUBBLING_PHASE)]
        )

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
        expected_results = [
            "Capture Handler 1",
            "Capture Handler 2",
            "Capture Handler 3",
            "Bubble Handler",
        ]
        self.assertEqual(results, expected_results)

    def test_capture_and_bubble_order_across_path(self):
        root = EventTarget()
        parent = EventTarget()
        child = EventTarget()
        parent.parentNode = root
        child.parentNode = parent
        results = []

        root.addEventListener(
            "custom_event",
            lambda event: results.append("root-capture"),
            {"capture": True},
        )
        parent.addEventListener(
            "custom_event",
            lambda event: results.append("parent-capture"),
            {"capture": True},
        )
        child.addEventListener(
            "custom_event",
            lambda event: results.append("child-capture"),
            {"capture": True},
        )
        child.addEventListener(
            "custom_event", lambda event: results.append("child-bubble")
        )
        parent.addEventListener(
            "custom_event", lambda event: results.append("parent-bubble")
        )

        child.dispatchEvent(Event("custom_event", {"bubbles": True}))

        self.assertEqual(
            results,
            [
                "root-capture",
                "parent-capture",
                "child-capture",
                "child-bubble",
                "parent-bubble",
            ],
        )

    def test_once_listener_is_removed_after_first_dispatch(self):
        target = EventTarget()
        calls = []

        target.addEventListener(
            "custom_event", lambda event: calls.append(event.type), {"once": True}
        )

        target.dispatchEvent(Event("custom_event"))
        target.dispatchEvent(Event("custom_event"))

        self.assertEqual(calls, ["custom_event"])

    def test_event_target_listener_edge_cases(self):
        target = EventTarget()
        calls = []

        def listener(event):
            calls.append((event.type, event.eventPhase))

        target.addEventListener("custom_event", None)
        self.assertFalse(target.hasEventListener("custom_event"))

        target.addEventListener("custom_event", listener, {"capture": True})
        target.addEventListener("custom_event", listener)
        target.removeEventListener("custom_event", listener, {"capture": True})

        target.dispatchEvent("custom_event")
        target.dispatchEvent({"type": "custom_event"})

        self.assertEqual(
            calls,
            [
                ("custom_event", Event.AT_TARGET),
                ("custom_event", Event.AT_TARGET),
            ],
        )
        self.assertEqual(target.listeners["custom_event"], [listener])

        with self.assertRaises(TypeError):
            target.dispatchEvent(object())

    def test_once_listener_is_removed_even_when_it_raises(self):
        target = EventTarget()
        calls = []

        def boom(event):
            calls.append(event.type)
            raise RuntimeError("boom")

        target.addEventListener("custom_event", boom, {"once": True})

        with self.assertRaises(RuntimeError):
            target.dispatchEvent(Event("custom_event"))

        target.dispatchEvent(Event("custom_event"))
        self.assertEqual(calls, ["custom_event"])
        self.assertFalse(target.hasEventListener("custom_event"))

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
            "sourceCapabilities": "capabilities",
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
        event = SubmitEvent("submit", {"submitter": submitter, "agentInvoked": True})
        self.assertIs(event.submitter, submitter)
        self.assertTrue(event.agentInvoked)
        self.assertEqual(event.respondWith({"ok": True}), {"ok": True})
        self.assertEqual(event._responded_with, {"ok": True})

    def test_tool_event(self):
        event = ToolEvent(ToolEvent.TOOLACTIVATED, {"toolName": "search_site"})
        self.assertEqual(event.toolName, "search_site")

        target = EventTarget()
        seen = []
        target.addEventListener("toolactivated", lambda evt: seen.append(evt.toolName))
        target.dispatchEvent(event)
        self.assertEqual(seen, ["search_site"])

    def test_mouse_event_client_coordinates_and_modifiers(self):
        related = object()
        event = MouseEvent(
            "click",
            {
                "clientX": 10,
                "clientY": 20,
                "screenX": 30,
                "screenY": 40,
                "pageX": 50,
                "pageY": 60,
                "offsetX": 7,
                "offsetY": 8,
                "movementX": 2,
                "movementY": 3,
                "button": 2,
                "buttons": 2,
                "ctrlKey": True,
                "relatedTarget": related,
            },
        )
        self.assertEqual(event.clientX, 10)
        self.assertEqual(event.clientY, 20)
        self.assertEqual((event.x, event.y), (10, 20))
        self.assertEqual((event.screenX, event.screenY), (30, 40))
        self.assertEqual((event.pageX, event.pageY), (50, 60))
        self.assertEqual((event.offsetX, event.offsetY), (7, 8))
        self.assertEqual((event.movementX, event.movementY), (2, 3))
        self.assertEqual(event.button, 2)
        self.assertEqual(event.buttons, 2)
        self.assertEqual(event.which, 3)
        self.assertIs(event.relatedTarget, related)
        self.assertTrue(event.getModifierState("Control"))

    def test_document_create_event_specializations(self):
        self.assertIsInstance(document.createEvent("MouseEvent"), MouseEvent)
        self.assertIsInstance(document.createEvent("KeyboardEvent"), KeyboardEvent)
        self.assertIsInstance(document.createEvent("CustomEvent"), CustomEvent)
        self.assertIsInstance(document.createEvent("PointerEvent"), PointerEvent)
        self.assertIsInstance(document.createEvent("WheelEvent"), WheelEvent)
        self.assertIsInstance(document.createEvent("MessageEvent"), MessageEvent)
        self.assertIsInstance(document.createEvent("ErrorEvent"), ErrorEvent)
        self.assertIsInstance(document.createEvent("PopStateEvent"), PopStateEvent)
        self.assertIsInstance(document.createEvent("CloseEvent"), CloseEvent)
        self.assertIsInstance(document.createEvent("DragEvent"), DragEvent)
        self.assertIsInstance(document.createEvent("FormDataEvent"), FormDataEvent)
        self.assertIsInstance(document.createEvent("TrackEvent"), TrackEvent)
        self.assertIsInstance(document.createEvent("BlobEvent"), BlobEvent)
        self.assertIsInstance(
            document.createEvent("DeviceMotionEvent"), DeviceMotionEvent
        )
        self.assertIsInstance(
            document.createEvent("DeviceOrientationEvent"), DeviceOrientationEvent
        )
        self.assertIsInstance(
            document.createEvent("SecurityPolicyViolationEvent"),
            SecurityPolicyViolationEvent,
        )
        self.assertIsInstance(
            document.createEvent("WebGLContextEvent"), WebGLContextEvent
        )

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

    def test_abort_controller_signal_and_listener_options(self):
        controller = AbortController()
        signal = controller.signal
        events = []
        target = EventTarget()
        listener_calls = []

        signal.addEventListener(
            "abort", lambda event: events.append((event.type, signal.reason))
        )
        target.addEventListener(
            "custom_event",
            lambda event: listener_calls.append(event.type),
            {"signal": signal},
        )

        controller.abort("stop")
        target.dispatchEvent(Event("custom_event"))

        self.assertTrue(signal.aborted)
        self.assertEqual(signal.reason, "stop")
        self.assertEqual(events, [("abort", "stop")])
        self.assertEqual(listener_calls, [])

        already_aborted = AbortController()
        already_aborted.abort("done")
        target.addEventListener(
            "never",
            lambda event: listener_calls.append("never"),
            {"signal": already_aborted.signal},
        )
        self.assertFalse(target.hasEventListener("never"))

    def test_close_event_shape(self):
        event = CloseEvent("close", {"code": 1000, "reason": "bye", "wasClean": True})
        self.assertEqual(event.code, 1000)
        self.assertEqual(event.reason, "bye")
        self.assertTrue(event.wasClean)

    def test_long_tail_event_data_helpers(self):
        custom_event = CustomEvent("custom")
        custom_event.initCustomEvent(
            "customized", bubbles=False, cancelable=True, detail={"ok": True}
        )
        self.assertEqual(custom_event.type, "customized")
        self.assertEqual(custom_event.detail, {"ok": True})
        self.assertFalse(custom_event.bubbles)

        transition = TransitionEvent(
            "transitionend", {"propertyName": "opacity", "elapsedTime": 0.25}
        )
        self.assertEqual(transition.propertyName, "opacity")
        self.assertEqual(transition.elapsedTime, 0.25)

        request = type(
            "Request", (), {"url": "/a", "referrer": "/a", "clientId": "c1"}
        )()
        fetch_event = FetchEvent("fetch", {"request": request, "clientId": "c2"})
        self.assertTrue(fetch_event.isReload)
        self.assertTrue(fetch_event.replacesClientId)
        self.assertEqual(fetch_event.resultingClientId, "c2")
        self.assertEqual(fetch_event.respondWith("response"), "response")

        marker = object()
        extendable = ExtendableEvent("extendable")
        self.assertIs(extendable.waitUntil(marker), marker)
        self.assertEqual(extendable._pending_promises, [marker])

        promise_event = PromiseRejectionEvent(
            "unhandledrejection", {"reason": "boom", "isRejected": True}
        )
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

        mouse_event = MouseEvent("click").initMouseEvent(
            "mousedown",
            True,
            True,
            None,
            1,
            0,
            0,
            11,
            22,
            True,
            False,
            False,
            False,
            1,
            None,
        )
        self.assertEqual(mouse_event.type, "mousedown")
        self.assertEqual(mouse_event.clientX, 11)
        self.assertTrue(mouse_event.ctrlKey)

        relayed_mouse_event = MouseEvent("mousemove").initMouseEvent(
            from_json={"clientX": 44, "clientY": 55, "button": 2, "buttons": 2}
        )
        self.assertEqual(relayed_mouse_event.clientX, 44)
        self.assertEqual(relayed_mouse_event.clientY, 55)
        self.assertEqual(relayed_mouse_event.button, 2)
        self.assertEqual(relayed_mouse_event.buttons, 2)

        keyboard_event = KeyboardEvent("keydown").initKeyboardEvent(
            "keyup", True, True, None, 65, "A", 0, "", False
        )
        self.assertEqual(keyboard_event.type, "keyup")
        self.assertEqual(keyboard_event.key, "a")
        self.assertEqual(keyboard_event.charCode, 65)
        self.assertEqual(keyboard_event.code, "KeyA")
        self.assertEqual(keyboard_event.keyCode, 65)

        keyboard_with_modifiers = KeyboardEvent("keydown").initKeyboardEvent(
            "keydown", True, True, None, 65, "A", 1, "Alt Shift", True
        )
        self.assertTrue(keyboard_with_modifiers.altKey)
        self.assertTrue(keyboard_with_modifiers.shiftKey)
        self.assertEqual(keyboard_with_modifiers.location, 1)
        self.assertTrue(keyboard_with_modifiers.repeat)
        self.assertEqual(keyboard_with_modifiers.code, "KeyA")

    def test_keyboard_event_modern_key_code_and_location_defaults(self):
        keyboard_event = KeyboardEvent(
            "keydown",
            {
                "key": "Enter",
                "location": KeyboardEvent.DOM_KEY_LOCATION_NUMPAD,
                "capsLock": True,
                "repeat": True,
            },
        )

        self.assertEqual(keyboard_event.key, "Enter")
        self.assertEqual(keyboard_event.code, "NumpadEnter")
        self.assertEqual(keyboard_event.keyCode, 13)
        self.assertEqual(keyboard_event.location, KeyboardEvent.DOM_KEY_LOCATION_NUMPAD)
        self.assertTrue(keyboard_event.repeat)
        self.assertTrue(keyboard_event.getModifierState("CapsLock"))
        self.assertFalse(keyboard_event.getModifierState("Shift"))

        pointer_event = PointerEvent(
            "pointerdown", {"clientX": 5, "clientY": 6, "pointerId": 3}
        )
        self.assertEqual(pointer_event.clientX, 5)
        self.assertEqual(pointer_event.pointerId, 3)
        self.assertEqual(pointer_event.width, 1)
        self.assertEqual(pointer_event.height, 1)

        error_event = ErrorEvent(
            "error", {"message": "boom", "filename": "x.py", "lineno": 4, "colno": 2}
        )
        self.assertEqual(error_event.filename, "x.py")
        self.assertEqual(error_event.lineno, 4)

    def test_dispatch_does_not_swallow_listener_exceptions(self):
        target = EventTarget()

        def boom(event):
            raise RuntimeError("boom")

        target.addEventListener("custom_event", boom)
        with self.assertRaises(RuntimeError):
            target.dispatchEvent(Event("custom_event"))

    def test_cancel_bubble_and_return_value_semantics(self):
        event = Event("custom")
        event.cancelBubble = True
        self.assertTrue(event.cancelBubble)
        self.assertTrue(event._propagation_stopped)

        event = Event("custom")
        event.returnValue = False
        self.assertTrue(event.defaultPrevented)
        self.assertFalse(event.returnValue)

        event.returnValue = True
        self.assertFalse(event.defaultPrevented)
        self.assertTrue(event.returnValue)

        event = Event("custom", {"defaultPrevented": True})
        self.assertTrue(event.defaultPrevented)
        self.assertFalse(event.returnValue)

    def test_pointer_beforeunload_input_and_fetch_helpers(self):
        pointer = PointerEvent(
            "pointermove",
            {
                "coalescedEvents": [1, 2],
                "predictedEvents": [3],
                "altitudeAngle": 0.5,
                "azimuthAngle": 1.5,
                "persistentDeviceId": 42,
            },
        )
        self.assertEqual(pointer.getCoalescedEvents(), [1, 2])
        self.assertEqual(pointer.getPredictedEvents(), [3])
        self.assertEqual(pointer.altitudeAngle, 0.5)
        self.assertEqual(pointer.azimuthAngle, 1.5)
        self.assertEqual(pointer.persistentDeviceId, 42)

        beforeunload = BeforeUnloadEvent("beforeunload")
        beforeunload.returnValue = "Leave?"
        self.assertTrue(beforeunload.defaultPrevented)
        self.assertEqual(beforeunload.returnValue, "Leave?")
        beforeunload.returnValue = ""
        self.assertFalse(beforeunload.defaultPrevented)

        target = EventTarget()
        input_event = InputEvent("input", {"targetRanges": [Range()]})
        input_event.target = target
        self.assertEqual(len(input_event.getTargetRanges()), 1)

        wheel = WheelEvent("wheel", {"deltaMode": WheelEvent.DOM_DELTA_LINE})
        self.assertEqual(wheel.deltaMode, WheelEvent.DOM_DELTA_LINE)

        touch = TouchEvent("touchstart", {"touches": [1], "shiftKey": True})
        self.assertEqual(touch.touches, [1])
        self.assertTrue(touch.getModifierState("Shift"))

        drag = DragEvent("drag", {"clientX": 9, "dataTransfer": {"text": "hi"}})
        self.assertEqual(drag.clientX, 9)
        self.assertEqual(drag.dataTransfer, {"text": "hi"})

        request = type(
            "Request", (), {"url": "/a", "referrer": "/b", "clientId": "c1"}
        )()
        fetch_event = FetchEvent("fetch", {"request": request})
        marker = object()
        self.assertIs(fetch_event.waitUntil(marker), marker)
        self.assertEqual(fetch_event._pending_promises, [marker])

    def test_dispatch_resets_phase_and_current_target(self):
        target = EventTarget()
        event = Event("custom_event", {"bubbles": True, "cancelable": True})

        target.dispatchEvent(event)

        self.assertEqual(event.eventPhase, Event.NONE)
        self.assertIsNone(event.currentTarget)

    def test_init_event_defaults_and_noops_while_dispatching(self):
        event = Event("custom_event", {"bubbles": True, "cancelable": True})
        event.initEvent("reset_event")

        self.assertEqual(event.type, "reset_event")
        self.assertFalse(event.bubbles)
        self.assertFalse(event.cancelable)

        target = EventTarget()
        dispatched = Event("custom_event")

        def listener(evt):
            evt.initEvent("mutated", True, True)

        target.addEventListener("custom_event", listener)
        target.dispatchEvent(dispatched)

        self.assertEqual(dispatched.type, "custom_event")
        self.assertFalse(dispatched.bubbles)
        self.assertFalse(dispatched.cancelable)

    def test_modern_event_data_classes(self):
        marker = object()
        self.assertIs(FormDataEvent("formdata", {"formData": marker}).formData, marker)
        self.assertIs(TrackEvent("addtrack", {"track": marker}).track, marker)
        self.assertEqual(
            BlobEvent("dataavailable", {"data": b"x", "timecode": 12}).timecode,
            12,
        )

        motion = DeviceMotionEvent(
            "devicemotion",
            {
                "acceleration": {"x": 1},
                "accelerationIncludingGravity": {"z": 9.8},
                "rotationRate": {"alpha": 2},
                "interval": 16,
            },
        )
        self.assertEqual(motion.acceleration, {"x": 1})
        self.assertEqual(motion.accelerationIncludingGravity, {"z": 9.8})
        self.assertEqual(motion.rotationRate, {"alpha": 2})
        self.assertEqual(motion.interval, 16)

        orientation = DeviceOrientationEvent(
            "deviceorientation",
            {"absolute": True, "alpha": 1, "beta": 2, "gamma": 3},
        )
        self.assertTrue(orientation.absolute)
        self.assertEqual(
            (orientation.alpha, orientation.beta, orientation.gamma), (1, 2, 3)
        )

        light = DeviceLightEvent("devicelight", {"value": 50})
        self.assertEqual(light.value, 50)

        proximity = DeviceProximityEvent(
            "deviceproximity", {"value": 3, "min": 1, "max": 10}
        )
        self.assertEqual((proximity.value, proximity.min, proximity.max), (3, 1, 10))

        webgl = WebGLContextEvent("webglcontextlost", {"statusMessage": "context lost"})
        self.assertEqual(webgl.statusMessage, "context lost")

        violation = SecurityPolicyViolationEvent(
            "securitypolicyviolation",
            {
                "documentURI": "https://example.com",
                "referrer": "https://referrer.example",
                "blockedURI": "inline",
                "violatedDirective": "script-src",
                "effectiveDirective": "script-src-elem",
                "originalPolicy": "script-src 'self'",
                "disposition": "enforce",
                "sourceFile": "app.js",
                "statusCode": 200,
                "lineNumber": 4,
                "columnNumber": 8,
                "sample": "alert(1)",
            },
        )
        self.assertEqual(violation.documentURI, "https://example.com")
        self.assertEqual(violation.effectiveDirective, "script-src-elem")
        self.assertEqual(violation.statusCode, 200)
        self.assertFalse(hasattr(violation, "waitUntil"))

    def test_long_tail_event_shapes_and_legacy_helpers(self):
        options = EventListenerOptions(
            capture=True, once=True, passive=True, signal="signal"
        )
        self.assertEqual(
            options,
            {"capture": True, "once": True, "passive": True, "signal": "signal"},
        )

        base_event = Event("custom")
        self.assertEqual(
            base_event.msConvertURL("https://example.com"),
            'javascript:window.open("https://example.com");',
        )
        self.assertEqual(
            base_event.msConvertURL("mailto:test@example.com"),
            "mailto:test@example.com",
        )

        controller = AbortController()
        aborts = []
        controller.signal.onabort = lambda event: aborts.append(
            controller.signal.reason
        )
        controller.abort("stop")
        controller.abort("ignored")
        self.assertEqual(aborts, ["stop"])
        with self.assertRaises(RuntimeError):
            controller.signal.throwIfAborted()

        self.assertEqual(
            CompositionEvent("compositionupdate", {"data": "é", "locale": "fr"}).data,
            "é",
        )
        marker = object()
        self.assertIs(
            FocusEvent("focus", {"relatedTarget": marker}).relatedTarget, marker
        )

        animation = AnimationEvent(
            "animationend",
            {"animationName": "fade", "elapsedTime": 0.3, "pseudoElement": "::before"},
        )
        self.assertEqual(animation.animationName, "fade")
        self.assertEqual(animation.pseudoElement, "::before")

        clipboard = ClipboardEvent("copy", {"clipboardData": {"text/plain": "hi"}})
        self.assertEqual(clipboard.clipboardData, {"text/plain": "hi"})

        self.assertEqual(SVGEvent("load").type, "load")
        self.assertEqual(TimerEvent(TimerEvent.TIMER_COMPLETE).type, "timercomplete")
        self.assertTrue(PageTransitionEvent("pageshow", {"persisted": True}).persisted)
        self.assertEqual(PopStateEvent("popstate", {"state": {"x": 1}}).state, {"x": 1})

        storage = StorageEvent(
            "storage",
            {
                "key": "theme",
                "oldValue": "light",
                "newValue": "dark",
                "url": "https://example.com",
            },
        )
        self.assertEqual(
            (storage.key, storage.oldValue, storage.newValue),
            ("theme", "light", "dark"),
        )

        progress = ProgressEvent(
            "progress", {"lengthComputable": True, "loaded": 5, "total": 10}
        )
        self.assertTrue(progress.lengthComputable)
        self.assertEqual((progress.loaded, progress.total), (5, 10))

        loaded = DOMContentLoadedEvent("DOMContentLoaded", {"document": document})
        self.assertIs(loaded.document, document)

        sync = SyncEvent("sync", {"tag": "outbox", "lastChance": True})
        self.assertEqual(sync.tag, "outbox")
        self.assertTrue(sync.lastChance)

        tween = TweenEvent(
            TweenEvent.COMPLETE, source="animation", bubbles=True, cancelable=True
        )
        self.assertEqual(tween.source, "animation")
        self.assertTrue(tween.bubbles)
        self.assertTrue(tween.cancelable)

    def test_async_dispatch_path_and_handler_callback(self):
        async def runner():
            root = EventTarget()
            parent = EventTarget()
            child = EventTarget()
            parent.parentNode = root
            child.parentNode = parent
            calls = []

            async def root_capture(event):
                await asyncio.sleep(0)
                calls.append(("root", event.eventPhase))

            def parent_bubble(event):
                calls.append(("parent", event.eventPhase))

            async def child_handler(event):
                calls.append(("handler", event.eventPhase))
                return False

            root.addEventListener("custom", root_capture, {"capture": True})
            parent.addEventListener("custom", parent_bubble)
            child.oncustom = child_handler

            event = Event("custom", {"bubbles": True, "cancelable": True})
            result = await child.dispatchEventAsync(event)

            self.assertFalse(result)
            self.assertTrue(event.defaultPrevented)
            self.assertEqual(
                calls,
                [
                    ("root", Event.CAPTURING_PHASE),
                    ("handler", Event.AT_TARGET),
                    ("parent", Event.BUBBLING_PHASE),
                ],
            )

        asyncio.run(runner())

    def test_async_dispatch_respects_false_and_resets_state(self):
        async def runner():
            target = EventTarget()

            async def listener(event):
                await asyncio.sleep(0)
                return False

            target.addEventListener("custom_event", listener)
            event = Event("custom_event", {"cancelable": True})
            result = await target.dispatchEventAsync(event)
            self.assertFalse(result)
            self.assertTrue(event.defaultPrevented)
            self.assertEqual(event.eventPhase, Event.NONE)
            self.assertIsNone(event.currentTarget)

        asyncio.run(runner())

    def test_event_target_option_and_path_edge_cases(self):
        with self.assertRaises(NotImplementedError):
            EventListener().handleEvent(Event("custom"))

        signal = object()
        normalized = EventTarget._normalize_listener_options(
            capture=True, once=True, passive=True, signal=signal
        )
        self.assertEqual(
            normalized,
            {"capture": True, "once": True, "passive": True, "signal": signal},
        )

        target = EventTarget()
        calls = []

        def listener(event):
            calls.append(event.type)

        target.addEventListener("custom", listener)
        target.addEventListener("custom", listener)
        self.assertEqual(target.listeners["custom"], [listener])

        target.removeEventListener("missing", None)
        target.dispatchEvent(Event("custom"))
        self.assertEqual(calls, ["custom"])

        child = EventTarget()
        document_target = EventTarget()
        window_target = EventTarget()
        child.ownerDocument = document_target
        document_target.defaultView = window_target

        self.assertEqual(
            child._get_event_path(child), [child, document_target, window_target]
        )

    def test_sync_dispatch_cancelation_and_path_edge_cases(self):
        target = EventTarget()
        target.addEventListener("custom", lambda event: False)
        event = Event("custom", {"cancelable": True})
        self.assertFalse(target.dispatchEvent(event))
        self.assertTrue(event.defaultPrevented)

        handler_target = EventTarget()
        handler_target.oncustom = lambda event: False
        handler_event = Event("custom", {"cancelable": True})
        self.assertFalse(handler_target.dispatchEvent(handler_event))
        self.assertTrue(handler_event.defaultPrevented)

        root = EventTarget()
        parent = EventTarget()
        child = EventTarget()
        parent.parentNode = root
        child.parentNode = parent
        calls = []

        def root_capture(event):
            calls.append("root-capture")
            event.stopPropagation()

        root.addEventListener("custom", root_capture, {"capture": True})
        child.addEventListener("custom", lambda event: calls.append("child"))

        capture_event = Event("custom", {"bubbles": True})
        self.assertTrue(child.dispatchEvent(capture_event))
        self.assertEqual(calls, ["root-capture"])
        self.assertTrue(capture_event.cancelBubble)

        root = EventTarget()
        parent = EventTarget()
        child = EventTarget()
        parent.parentNode = root
        child.parentNode = parent
        calls = []

        def parent_bubble(event):
            calls.append("parent-bubble")
            event.stopPropagation()

        parent.addEventListener("custom", parent_bubble)
        root.addEventListener("custom", lambda event: calls.append("root-bubble"))

        self.assertTrue(child.dispatchEvent(Event("custom", {"bubbles": True})))
        self.assertEqual(calls, ["parent-bubble"])

        stringified = str(Event("custom"))
        self.assertTrue(stringified.startswith("custom:"))

        return_value_event = Event("custom", {"returnValue": False})
        self.assertFalse(return_value_event.returnValue)
        self.assertTrue(return_value_event.defaultPrevented)

        document_target = EventTarget()
        window_target = EventTarget()
        child = EventTarget()
        child.parentNode = document_target
        document_target.defaultView = window_target
        path_event = Event("custom")
        path_event.target = child
        self.assertEqual(
            path_event.composedPath(), [child, document_target, window_target]
        )

        dispatched = Event("custom", {"bubbles": True})
        child.dispatchEvent(dispatched)
        self.assertEqual(
            dispatched.composedPath(), [child, document_target, window_target]
        )

    def test_async_dispatch_edge_cases(self):
        async def runner():
            target = EventTarget()
            calls = []

            class AsyncHandler:
                async def handleEvent(self, event):
                    await asyncio.sleep(0)
                    calls.append("object")

            target.addEventListener("custom", AsyncHandler(), {"once": True})
            await target.dispatchEventAsync(Event("custom"))
            await target.dispatchEventAsync(Event("custom"))
            self.assertEqual(calls, ["object"])
            self.assertFalse(target.hasEventListener("custom"))

            target = EventTarget()
            calls = []

            def first(event):
                calls.append("first")
                event.stopImmediatePropagation()

            target.addEventListener("custom", first)
            target.addEventListener("custom", lambda event: calls.append("second"))
            await target.dispatchEventAsync(Event("custom"))
            self.assertEqual(calls, ["first"])

            root = EventTarget()
            parent = EventTarget()
            child = EventTarget()
            parent.parentNode = root
            child.parentNode = parent
            calls = []

            async def root_capture(event):
                await asyncio.sleep(0)
                calls.append("root-capture")
                event.stopPropagation()

            root.addEventListener("custom", root_capture, {"capture": True})
            child.addEventListener("custom", lambda event: calls.append("child"))
            self.assertTrue(
                await child.dispatchEventAsync(Event("custom", {"bubbles": True}))
            )
            self.assertEqual(calls, ["root-capture"])

            root = EventTarget()
            parent = EventTarget()
            child = EventTarget()
            parent.parentNode = root
            child.parentNode = parent
            calls = []

            def parent_bubble(event):
                calls.append("parent-bubble")
                event.stopPropagation()

            parent.addEventListener("custom", parent_bubble)
            root.addEventListener("custom", lambda event: calls.append("root-bubble"))

            self.assertTrue(
                await child.dispatchEventAsync(Event("custom", {"bubbles": True}))
            )
            self.assertEqual(calls, ["parent-bubble"])

        asyncio.run(runner())

    def test_event_data_branch_edge_cases(self):
        related = object()
        mouse_event = MouseEvent("mousemove").initMouseEvent(
            from_json={
                "screenX": 101,
                "screenY": 102,
                "ctrlKey": True,
                "altKey": True,
                "shiftKey": True,
                "metaKey": True,
                "relatedTarget": related,
            }
        )
        self.assertEqual((mouse_event.screenX, mouse_event.screenY), (101, 102))
        self.assertTrue(mouse_event.ctrlKey)
        self.assertTrue(mouse_event.altKey)
        self.assertTrue(mouse_event.shiftKey)
        self.assertTrue(mouse_event.metaKey)
        self.assertIs(mouse_event.relatedTarget, related)

        keyboard = KeyboardEvent(
            "keydown",
            {"key": "Enter", "ctrlKey": True, "altKey": True, "metaKey": True},
        )
        self.assertEqual(keyboard.charCode, 0)
        self.assertTrue(keyboard.ctrlKey)
        self.assertTrue(keyboard.altKey)
        self.assertTrue(keyboard.metaKey)
        self.assertEqual(keyboard.unicode, "Enter")
        self.assertEqual(KeyboardEvent("keypress", {"key": "a"}).charCode, 97)

        class Selection:
            rangeCount = 2

            def getRangeAt(self, index):
                return f"range-{index}"

        class SelectionTarget:
            def getSelection(self):
                return Selection()

        input_event = InputEvent("beforeinput")
        del input_event._targetRanges
        input_event.target = SelectionTarget()
        self.assertEqual(input_event.getTargetRanges(), ["range-0", "range-1"])

        input_event_without_selection = InputEvent("beforeinput")
        del input_event_without_selection._targetRanges
        input_event_without_selection.target = object()
        self.assertEqual(input_event_without_selection.getTargetRanges(), [])

        class EmptySelectionTarget:
            def getSelection(self):
                return None

        input_event_with_empty_selection = InputEvent("beforeinput")
        del input_event_with_empty_selection._targetRanges
        input_event_with_empty_selection.target = EmptySelectionTarget()
        self.assertEqual(input_event_with_empty_selection.getTargetRanges(), [])

        hash_change = HashChangeEvent(
            "hashchange", {"oldURL": "https://example.com/#old", "newURL": "#new"}
        )
        self.assertEqual(hash_change.oldURL, "https://example.com/#old")
        self.assertEqual(hash_change.newURL, "#new")

        gamepad = object()
        self.assertIs(
            GamePadEvent(GamePadEvent.START, {"gamepad": gamepad}).gamepad, gamepad
        )

        fetch_event = FetchEvent("fetch", {"clientId": "client-1"})
        self.assertFalse(fetch_event.isReload)
        self.assertFalse(fetch_event.replacesClientId)
        self.assertEqual(fetch_event.resultingClientId, "client-1")

        handler = GlobalEventHandler()
        handler._onclick_callback = lambda event: "handled"
        self.assertEqual(handler.onclick(Event("click")), "handled")


if __name__ == "__main__":
    unittest.main()
