"""
    test_events
    ~~~~~~~~~~~~
    - unit tests for events

"""

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

        def async_test(evt, *args, **kwargs):
            async def delayed_assert():
                await asyncio.sleep(1)
                self.assertTrue(evt.target == somebody or evt.target == site)
            asyncio.run(delayed_assert())

        site.addEventListener("click", test)
        somebody.addEventListener("anything", test)

        site.dispatchEvent(Event("click"))
        somebody.dispatchEvent(Event("anything"))

        # Asynchronous event handling
        site.addEventListener("async_event", async_test)
        site.dispatchEventAsync(Event("async_event"))

    async def test_async_events(self):
        site = EventTarget()
        somebody = EventTarget()

        async def async_test(evt, *args, **kwargs):
            await asyncio.sleep(1)
            self.assertTrue(evt.target == somebody or evt.target == site)

        site.addEventListener("click", async_test)
        somebody.addEventListener("anything", async_test)

        await site.dispatchEventAsync(Event("click"))
        await somebody.dispatchEventAsync(Event("anything"))

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
        self.assertTrue(event.defaultPrevented)

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

if __name__ == '__main__':
    unittest.main()