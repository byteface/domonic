"""
test_dialog_popover
~~~~~~~~~~~~~~~~~~~

<dialog> (https://html.spec.whatwg.org/#the-dialog-element) and the popover
API (https://html.spec.whatwg.org/#the-popover-attribute).
"""

import unittest

from domonic.dom import DOMException
from domonic.html import body, dialog, div, html


class TestDialog(unittest.TestCase):
    def setUp(self):
        self.page = html(body(dialog("Hi", _id="d")))
        self.dialog = self.page.querySelector("#d")

    def test_open_property_writes_an_empty_attribute(self):
        self.dialog.open = True
        self.assertEqual(self.dialog.getAttribute("open"), "")
        self.dialog.open = False
        self.assertFalse(self.dialog.hasAttribute("open"))

    def test_show_modal_is_modal(self):
        self.dialog.showModal()
        self.assertTrue(self.dialog.open)
        self.assertIs(self.page.querySelector(":modal"), self.dialog)
        self.assertEqual(self.dialog.closedBy, "closerequest")
        self.dialog.showModal()  # already modal: no error
        self.dialog.close()
        self.assertIsNone(self.page.querySelector(":modal"))

    def test_show_is_not_modal(self):
        self.dialog.show()
        self.assertTrue(self.dialog.open)
        self.assertIsNone(self.page.querySelector(":modal"))
        self.assertEqual(self.dialog.closedBy, "none")

    def test_mixing_modes_throws(self):
        self.dialog.show()
        with self.assertRaises(DOMException) as caught:
            self.dialog.showModal()
        self.assertEqual(caught.exception.name, "InvalidStateError")
        self.dialog.close()
        self.dialog.showModal()
        with self.assertRaises(DOMException):
            self.dialog.show()

    def test_return_value(self):
        self.assertEqual(self.dialog.returnValue, "")
        self.dialog.show()
        self.dialog.close("ok")
        self.assertEqual(self.dialog.returnValue, "ok")
        self.dialog.show()
        self.dialog.close()  # no argument: unchanged
        self.assertEqual(self.dialog.returnValue, "ok")

    def test_close_when_closed_does_nothing(self):
        closes = []
        self.dialog.addEventListener("close", lambda event: closes.append(event.type))
        self.dialog.close("x")
        self.assertEqual((closes, self.dialog.returnValue), ([], ""))
        self.dialog.show()
        self.dialog.close("x")
        self.assertEqual(closes, ["close"])

    def test_request_close_can_be_cancelled(self):
        self.dialog.showModal()
        self.dialog.addEventListener("cancel", lambda event: event.preventDefault())
        self.dialog.requestClose("nope")
        self.assertTrue(self.dialog.open)

        fresh = html(body(dialog(_id="e"))).querySelector("#e")
        fresh.showModal()
        fresh.requestClose("done")
        self.assertFalse(fresh.open)
        self.assertEqual(fresh.returnValue, "done")

    def test_closed_by_attribute(self):
        self.assertEqual(dialog(_closedby="ANY").closedBy, "any")
        self.assertEqual(dialog(_closedby="bogus").closedBy, "none")


class TestPopover(unittest.TestCase):
    def setUp(self):
        self.page = html(body(div("menu", _id="p", _popover="")))
        self.popover = self.page.querySelector("#p")

    def test_showing_adds_no_attribute(self):
        self.popover.showPopover()
        self.assertFalse(self.popover.hasAttribute("open"))
        self.assertIs(self.page.querySelector(":popover-open"), self.popover)
        self.assertEqual(str(self.popover), '<div id="p" popover="">menu</div>')
        self.popover.hidePopover()
        self.assertIsNone(self.page.querySelector(":popover-open"))

    def test_toggle_returns_whether_it_is_showing(self):
        self.assertTrue(self.popover.togglePopover())
        self.assertFalse(self.popover.togglePopover())
        self.assertTrue(self.popover.togglePopover(True))
        self.assertTrue(self.popover.togglePopover(True))

    def test_toggle_events(self):
        events = []
        for name in ("beforetoggle", "toggle"):
            self.popover.addEventListener(name, lambda e, name=name: events.append((name, e.oldState, e.newState)))
        self.popover.showPopover()
        self.popover.showPopover()  # already showing: no events
        self.popover.hidePopover()
        self.assertEqual(
            events,
            [
                ("beforetoggle", "closed", "open"),
                ("toggle", "closed", "open"),
                ("beforetoggle", "open", "closed"),
                ("toggle", "open", "closed"),
            ],
        )

    def test_only_showing_can_be_cancelled(self):
        self.popover.addEventListener("beforetoggle", lambda event: event.preventDefault())
        self.popover.showPopover()
        self.assertIsNone(self.page.querySelector(":popover-open"))
        self.popover.__dict__["_popover_open"] = True
        self.popover.hidePopover()  # hiding ignores preventDefault
        self.assertIsNone(self.page.querySelector(":popover-open"))

    def test_needs_the_popover_attribute(self):
        with self.assertRaises(DOMException) as caught:
            div().showPopover()
        self.assertEqual(caught.exception.name, "NotSupportedError")


if __name__ == "__main__":
    unittest.main()
