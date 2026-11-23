"""
test_cookies
~~~~~~~~~~~~

document.cookie on a page in a window reads and writes the window's cookie jar
(https://html.spec.whatwg.org/#dom-document-cookie, RFC 6265).
"""

import unittest

from domonic.dom import Document
from domonic.window import Window


class TestDocumentCookie(unittest.TestCase):
    def setUp(self):
        self.win = Window(doc=Document(), url="https://example.com/shop/cart")
        self.doc = self.win.document
        self.jar = self.win._http_session().cookies

    def test_set_and_read(self):
        self.doc.cookie = "a=1"
        self.doc.cookie = "b=2; Path=/"
        self.assertEqual(self.doc.cookie, "a=1; b=2")
        self.assertEqual(
            {(c.name, c.domain, c.path) for c in self.jar}, {("a", "example.com", "/shop"), ("b", "example.com", "/")}
        )

    def test_path_scoping_and_order(self):
        self.doc.cookie = "deep=1; Path=/shop/cart"
        self.doc.cookie = "top=1; Path=/"
        self.doc.cookie = "other=1; Path=/blog"
        self.assertEqual(self.doc.cookie, "deep=1; top=1")  # longest path first

    def test_max_age_and_expires_delete(self):
        self.doc.cookie = "a=1; Path=/"
        self.doc.cookie = "a=; Path=/; Max-Age=0"
        self.assertEqual(self.doc.cookie, "")
        self.doc.cookie = "b=1; Path=/"
        self.doc.cookie = "b=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT"
        self.assertEqual(self.doc.cookie, "")
        self.doc.cookie = "c=1; Max-Age=3600"
        self.assertEqual(self.doc.cookie, "c=1")

    def test_domain(self):
        self.doc.cookie = "wide=1; Domain=example.com; Path=/"
        self.doc.cookie = "foreign=1; Domain=other.org"  # not this site: dropped
        self.doc.cookie = "tld=1; Domain=com"
        self.assertEqual(self.doc.cookie, "wide=1")
        sub = Window(doc=Document(), url="https://shop.example.com/")
        sub.__dict__["_requests_session"] = self.win._http_session()  # the same jar
        self.assertEqual(sub.document.cookie, "wide=1")

    def test_secure_and_http_only(self):
        self.doc.cookie = "s=1; Secure; Path=/"
        self.doc.cookie = "h=1; HttpOnly; Path=/"  # a script can't set these
        self.assertEqual(self.doc.cookie, "s=1")
        plain = Window(doc=Document(), url="http://example.com/")
        plain.__dict__["_requests_session"] = self.win._http_session()
        self.assertEqual(plain.document.cookie, "")  # Secure: https only
        plain.document.cookie = "t=1; Secure"  # an http page can't set one
        self.assertEqual(plain.document.cookie, "")

    def test_cookie_store_shares_the_jar(self):
        self.doc.cookie = "a=1; Path=/"
        self.assertEqual(self.win.cookieStore.get("a").data.value, "1")
        self.win.cookieStore.set("b", "2")
        self.assertIn("b=2", self.doc.cookie)
        self.win.cookieStore.delete("a")
        self.assertEqual(self.doc.cookie, "b=2")
        self.assertEqual([item.name for item in self.win.cookieStore.getAll().data], ["b"])

    def test_documents_without_an_http_window_keep_their_own(self):
        doc = Document()
        doc.cookie = "a=1; Path=/"
        self.assertEqual((doc.cookie, doc._cookie_store), ("a=1", {"a": "1"}))
        blank = Window(doc=Document())
        blank.document.cookie = "b=2"
        self.assertEqual(blank.document.cookie, "b=2")
        self.assertEqual(list(blank._http_session().cookies), [])


if __name__ == "__main__":
    unittest.main()
