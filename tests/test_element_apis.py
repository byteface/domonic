"""
test_element_apis
~~~~~~~~~~~~~~~~~

Smaller DOM/HTML APIs: HTMLElement global attributes, ElementInternals and
form-associated custom elements, getElementsByTagNameNS, createAttributeNS,
moveBefore, checkVisibility / getClientRects, element scrolling, shadow-root
options and manual slot assignment.
"""

import unittest

from domonic.dom import Document, DOMException, DOMParser, HTMLElement, _construct_form_data
from domonic.html import a, div, form, img, input, label, p, slot, span, template
from domonic.window import CustomElementRegistry, window

XHTML = "http://www.w3.org/1999/xhtml"


class TestGlobalAttributes(unittest.TestCase):
    def test_defaults(self):
        el = div()
        self.assertFalse(el.inert or el.autofocus)
        self.assertEqual((el.accessKey, el.inputMode, el.enterKeyHint, el.autocapitalize, el.nonce), ("",) * 5)
        self.assertTrue(el.translate and el.spellcheck)
        self.assertFalse(el.draggable)

    def test_reflection(self):
        el = div(_inert="", _accesskey="s", _inputmode="NUMERIC", _enterkeyhint="go", _autocapitalize="off")
        self.assertTrue(el.inert)
        self.assertEqual(
            (el.accessKey, el.inputMode, el.enterKeyHint, el.autocapitalize), ("s", "numeric", "go", "none")
        )
        self.assertEqual(div(_inputmode="nope").inputMode, "")
        self.assertEqual(div(_autocapitalize="nope").autocapitalize, "sentences")
        el.inert = False
        self.assertFalse(el.hasAttribute("inert"))

    def test_translate_and_spellcheck_inherit(self):
        page = div(p(span()), _translate="no", _spellcheck="false")
        inner = page.querySelector("span")
        self.assertFalse(inner.translate)
        self.assertFalse(inner.spellcheck)
        inner.translate = True
        self.assertEqual(inner.getAttribute("translate"), "yes")
        self.assertTrue(inner.translate)

    def test_draggable(self):
        self.assertTrue(img().draggable)
        self.assertTrue(a(_href="/x").draggable)
        self.assertFalse(a().draggable)
        self.assertFalse(img(_draggable="false").draggable)
        el = div()
        el.draggable = True
        self.assertEqual(el.getAttribute("draggable"), "true")

    def test_nonce_is_not_written_back(self):
        el = div(_nonce="abc")
        self.assertEqual(el.nonce, "abc")
        el.nonce = "xyz"
        self.assertEqual((el.nonce, el.getAttribute("nonce")), ("xyz", "abc"))


class TestElementInternals(unittest.TestCase):
    def setUp(self):
        self._registry = window.customElements
        window.customElements = CustomElementRegistry()

        class StarRating(HTMLElement):
            formAssociated = True

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.internals = self.attachInternals()
                self.resets = 0

            def formResetCallback(self):
                self.resets += 1

        class PlainElement(HTMLElement):
            pass

        window.customElements.define("star-rating", StarRating)
        window.customElements.define("plain-element", PlainElement)
        self.StarRating = StarRating
        self.PlainElement = PlainElement

    def tearDown(self):
        window.customElements = self._registry

    def test_attach_internals_rules(self):
        internals = self.PlainElement().attachInternals()
        self.assertEqual(internals.states.size, 0)
        self.assertIsNone(internals.shadowRoot)
        for make in (div, lambda: self.StarRating()):
            el = make()
            with self.assertRaises(DOMException) as caught:
                el.attachInternals()  # not custom / already attached
            self.assertEqual(caught.exception.name, "NotSupportedError")

    def test_form_api_needs_form_associated(self):
        internals = self.PlainElement().attachInternals()
        with self.assertRaises(DOMException):
            internals.setFormValue("x")
        with self.assertRaises(DOMException):
            internals.form

    def test_takes_part_in_the_form(self):
        rating = self.StarRating(_name="stars")
        sheet = form(input(_name="q", _value="x"), label("Rate", rating))
        rating.internals.setFormValue("4")
        self.assertIs(rating.internals.form, sheet)
        self.assertIs(list(sheet.elements)[-1], rating)
        self.assertEqual(_construct_form_data(sheet), {"q": "x", "stars": "4"})
        self.assertIs(sheet.querySelector("label").control, rating)
        self.assertEqual(len(rating.internals.labels), 1)

    def test_entries_value(self):
        rating = self.StarRating(_name="ignored")
        sheet = form(rating)
        rating.internals.setFormValue({"low": "1", "high": "5"})
        self.assertEqual(_construct_form_data(sheet), {"low": "1", "high": "5"})

    def test_validity(self):
        rating = self.StarRating()
        sheet = form(rating)
        internals = rating.internals
        self.assertTrue(internals.validity.valid)
        internals.setValidity({"valueMissing": True}, "Pick a rating")
        self.assertTrue(internals.validity.valueMissing)
        self.assertEqual(internals.validationMessage, "Pick a rating")
        self.assertFalse(internals.checkValidity())
        self.assertFalse(sheet.checkValidity())
        with self.assertRaises(TypeError):
            internals.setValidity({"valueMissing": True})  # a message is required
        internals.setValidity({})
        self.assertTrue(sheet.checkValidity())

    def test_reset_calls_back(self):
        rating = self.StarRating()
        form(rating).reset()
        self.assertEqual(rating.resets, 1)

    def test_custom_states(self):
        internals = self.PlainElement().attachInternals()
        internals.states.add("checked")
        self.assertTrue(internals.states.has("checked"))


class TestNamespacedLookups(unittest.TestCase):
    def test_get_elements_by_tag_name_ns(self):
        tree = div(span(), p(span()))
        self.assertEqual(len(tree.getElementsByTagNameNS(XHTML, "span")), 2)
        self.assertEqual(len(tree.getElementsByTagNameNS("*", "*")), 3)
        self.assertEqual(len(tree.getElementsByTagNameNS(None, "span")), 0)
        self.assertEqual(len(tree.getElementsByTagNameNS(XHTML, "SPAN")), 0)  # case-sensitive
        found = tree.getElementsByTagNameNS(XHTML, "span")
        tree.appendChild(span())
        self.assertEqual(len(found), 3)  # live

    def test_create_attribute_ns(self):
        attr = Document.createAttributeNS("http://www.w3.org/1999/xlink", "xlink:href")
        self.assertEqual(
            (attr.namespaceURI, attr.prefix, attr.localName), ("http://www.w3.org/1999/xlink", "xlink", "href")
        )
        self.assertIsNone(Document.createAttributeNS(None, "plain").namespaceURI)
        for namespace, name in (
            (None, "x:y"),
            ("urn:x", "xml:a"),
            ("urn:x", "xmlns"),
            ("http://www.w3.org/2000/xmlns/", "a"),
        ):
            with self.assertRaises(DOMException) as caught:
                Document.createAttributeNS(namespace, name)
            self.assertEqual(caught.exception.name, "NamespaceError", name)


class TestMoveBefore(unittest.TestCase):
    def test_moves_within_the_tree(self):
        parent = div(span("a"), span("b"))
        first, second = parent.querySelectorAll("span")
        parent.moveBefore(second, first)
        self.assertEqual(str(parent), "<div><span>b</span><span>a</span></div>")
        parent.moveBefore(second, None)
        self.assertEqual(str(parent), "<div><span>a</span><span>b</span></div>")

    def test_checks(self):
        parent = div(span())
        with self.assertRaises(DOMException) as caught:
            parent.moveBefore(div(), None)  # another tree
        self.assertEqual(caught.exception.name, "HierarchyRequestError")
        with self.assertRaises(DOMException) as caught:
            parent.querySelector("span").moveBefore(parent, None)  # into itself
        self.assertEqual(caught.exception.name, "HierarchyRequestError")
        with self.assertRaises(DOMException) as caught:
            parent.moveBefore(parent.querySelector("span"), p())
        self.assertEqual(caught.exception.name, "NotFoundError")

    def test_fragment(self):
        doc = DOMParser().parseFromString("<p>x</p>", "text/html")
        fragment = doc.createDocumentFragment()
        one, two = doc.createElement("i"), doc.createElement("b")
        fragment.append(one, two)
        fragment.moveBefore(two, one)
        self.assertEqual([node.localName for node in fragment.childNodes], ["b", "i"])


class TestVisibilityAndGeometry(unittest.TestCase):
    def setUp(self):
        self.doc = DOMParser().parseFromString(
            "<!doctype html><html><head><style>.gone{display:none}</style></head>"
            "<body><div id=box><span>v</span></div><p class=gone><b>x</b></p><script>1</script></body></html>",
            "text/html",
        )

    def test_check_visibility(self):
        box = self.doc.querySelector("#box")
        inner = box.querySelector("span")
        self.assertTrue(inner.checkVisibility())
        self.assertFalse(self.doc.querySelector("b").checkVisibility())  # ancestor display: none
        self.assertFalse(self.doc.querySelector("script").checkVisibility())  # UA hidden
        self.assertFalse(div().checkVisibility())  # not in a document
        box.setAttribute("hidden", "")
        self.assertFalse(inner.checkVisibility())
        box.removeAttribute("hidden")
        box.style.opacity = "0"
        self.assertTrue(inner.checkVisibility())
        self.assertFalse(inner.checkVisibility({"opacityProperty": True}))
        box.style.opacity = ""
        box.style.visibility = "hidden"
        self.assertFalse(inner.checkVisibility({"visibilityProperty": True}))

    def test_get_client_rects(self):
        self.assertEqual(len(self.doc.querySelector("#box").getClientRects()), 1)
        self.assertEqual(len(self.doc.querySelector("b").getClientRects()), 0)

    def test_scrolling(self):
        el = div()
        events = []
        el.addEventListener("scroll", lambda event: events.append((el.scrollLeft(), el.scrollTop())))
        el.scrollTo(10, 20)
        el.scrollBy({"top": 5})
        el.scroll({"left": 10, "top": 25})  # no change: no event
        el.scrollBy(-50, 0)  # clamps at 0
        self.assertEqual(events, [(10, 20), (10, 25), (0, 25)])


class TestShadowRootOptions(unittest.TestCase):
    def test_options_are_recorded(self):
        root = div().attachShadow({"mode": "closed", "delegatesFocus": True, "clonable": True, "serializable": True})
        self.assertEqual(
            (root.mode, root.delegatesFocus, root.clonable, root.serializable), ("closed", True, True, True)
        )
        self.assertEqual(root.slotAssignment, "named")
        with self.assertRaises(TypeError):
            div().attachShadow({"mode": "open", "slotAssignment": "auto"})

    def test_only_clonable_roots_are_cloned(self):
        plain = div()
        plain.attachShadow({"mode": "open"})
        self.assertIsNone(plain.cloneNode(True).shadowRoot)
        self.assertIsNone(plain.cloneNode(False).shadowRoot)
        host = div()
        root = host.attachShadow({"mode": "open", "clonable": True})
        root.appendChild(span("inside"))
        for deep in (True, False):
            copied = host.cloneNode(deep).shadowRoot
            self.assertIsNotNone(copied)
            self.assertIsNot(copied, root)
            self.assertEqual(str(copied.firstChild), "<span>inside</span>")

    def test_manual_slot_assignment(self):
        host = div(span("one", _slot="named"), span("two"))
        root = host.attachShadow({"mode": "open", "slotAssignment": "manual"})
        target = slot()
        root.appendChild(target)
        one, two = host.querySelectorAll("span")
        self.assertEqual(target.assignedNodes(), [])  # nothing until assign()
        target.assign(two, one)
        self.assertEqual(target.assignedNodes(), [two, one])
        self.assertIs(one.assignedSlot, target)
        other = slot()
        root.appendChild(other)
        other.assign(one)
        self.assertEqual(target.assignedNodes(), [two])
        host.removeChild(two)
        self.assertEqual(target.assignedNodes(), [])

    def test_template_reflects_declarative_shadow_root_attributes(self):
        el = template(_shadowrootmode="OPEN", _shadowrootclonable="")
        self.assertEqual(el.shadowRootMode, "open")
        self.assertTrue(el.shadowRootClonable)
        self.assertFalse(el.shadowRootDelegatesFocus or el.shadowRootSerializable)
        self.assertEqual(template(_shadowrootmode="x").shadowRootMode, "")


if __name__ == "__main__":
    unittest.main()
