"""
    test_components
    ~~~~~~~~~~~~
    tests for components
"""

import unittest
import json

from domonic.components import DomonicJS, ProgressBar, Websocket
from domonic.events import KeyboardEvent, WheelEvent
from domonic.html import *
from domonic.JSON import *


class TestCase(unittest.TestCase):
    def test_domonicjs_renders_script(self):
        rendered = str(DomonicJS("9.9.9"))

        self.assertIn("<script>", rendered)
        self.assertIn("window.domonic = window.domonic || {};", rendered)
        self.assertIn('window.domonic.version = "9.9.9";', rendered)
        self.assertIn("function* enumerate", rendered)

    def test_progress_bar_defaults_and_updates(self):
        progress = ProgressBar()

        self.assertEqual(progress.value, 100)
        self.assertEqual(progress.percent, 100)
        self.assertIn('role="progressbar"', str(progress))
        self.assertIn('aria-valuenow="100"', str(progress))
        self.assertIn('style="width:100%"', str(progress))

        progress = ProgressBar(value=25, max=200, _id="health", label="Health")
        self.assertEqual(progress.value, 25)
        self.assertEqual(progress.percent, 12.5)
        rendered = str(progress)
        self.assertIn('id="health"', rendered)
        self.assertIn('<label for="health">Health</label>', rendered)
        self.assertIn('aria-valuemax="200"', rendered)
        self.assertIn('style="width:12.5%"', rendered)

        progress.increment(300)
        self.assertEqual(progress.value, 200)
        self.assertEqual(progress.percent, 100)
        progress.decrement(250)
        self.assertEqual(progress.value, 0)
        self.assertEqual(progress.percent, 0)

        with self.assertRaises(ValueError):
            ProgressBar(max=0)

    def test_websocket_uses_native_event_listeners(self):
        websocket = Websocket(
            reference="gameSocket",
            address="ws://localhost:9999",
            target="#stage",
            mouse_events=True,
            keyboard_events=False,
            wheel_events=True,
            clipboard_events=True,
            hashchange_events=True,
        )

        rendered = str(websocket)
        self.assertIn('const gameSocket = new WebSocket("ws://localhost:9999");', rendered)
        self.assertIn("function attach_domonic_listener", rendered)
        self.assertIn('attach_domonic_listener("#stage", "mousedown");', rendered)
        self.assertIn('attach_domonic_listener("window", "wheel");', rendered)
        self.assertIn('attach_domonic_listener("window", "copy");', rendered)
        self.assertIn('attach_domonic_listener("window", "hashchange");', rendered)
        self.assertIn("gameSocket.send(stringify_object(event));", rendered)
        self.assertNotIn("$(", rendered)

    def test_websocket_get_event(self):
        event = Websocket.get_event(
            json.dumps(
                {
                    "type": "keydown",
                    "keyCode": 65,
                    "charCode": 65,
                    "code": "KeyA",
                    "key": "a",
                }
            )
        )
        self.assertIsInstance(event, KeyboardEvent)
        self.assertEqual(event.key, "a")
        self.assertEqual(event.keyCode, 65)

        event = Websocket.get_event(
            json.dumps(
                {
                    "type": "wheel",
                    "deltaX": 1,
                    "deltaY": 2,
                    "deltaZ": 0,
                    "deltaMode": 0,
                }
            )
        )
        self.assertIsInstance(event, WheelEvent)
        self.assertEqual(event.deltaY, 2)

        self.assertIsNone(Websocket.get_event("not json"))
