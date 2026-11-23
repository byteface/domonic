"""
test_navigation
~~~~~~~~~~~~~~~

Form submission and link following navigate the window
(https://html.spec.whatwg.org/#form-submission-algorithm,
https://html.spec.whatwg.org/#following-hyperlinks), against a local server.
"""

import threading
import unittest
import urllib.parse
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

from domonic.html import a, body, button, dialog, form, html, input
from domonic.webapi.file import File
from domonic.window import Window

PAGE = """<!doctype html><html><body>
<h1>Start</h1>
<form id="search" action="/search"><input name="q" value="hello"><button id="go">Go</button></form>
<form id="login" action="/login" method="post">
  <input name="user" value="ann"><input name="secret" type="password" value="p w">
  <button id="in">Log in</button>
  <button id="alt" formaction="/echo" formmethod="post" name="via" value="alt">Alt</button>
</form>
<form id="upload" action="/echo" method="post" enctype="multipart/form-data">
  <input name="note" value="hi"><input id="file" name="doc" type="file"><button id="send">Send</button>
</form>
<form id="plain" action="/echo" method="post" enctype="text/plain"><input name="a" value="1"><button id="p">P</button></form>
<form id="mail" action="mailto:someone@example.com"><button id="m">M</button></form>
<form id="blank" action="/search" target="_blank"><button id="b">B</button></form>
<a id="next" href="/next">next</a>
<a id="frag" href="#section">jump</a>
<a id="dl" href="/file.zip" download>download</a>
<a id="mailto" href="mailto:someone@example.com">mail</a>
</body></html>"""


class _Handler(BaseHTTPRequestHandler):
    requests_seen: list = []

    def log_message(self, *args):
        pass

    def _send(self, status, text, headers=()):
        payload = text.encode()
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(payload)))
        for key, value in headers:
            self.send_header(key, value)
        self.end_headers()
        self.wfile.write(payload)

    def _record(self, body=b""):
        _Handler.requests_seen.append(
            {
                "method": self.command,
                "path": self.path,
                "body": body,
                "content_type": self.headers.get("Content-Type", ""),
                "referer": self.headers.get("Referer"),
                "origin": self.headers.get("Origin"),
                "cookie": self.headers.get("Cookie"),
            }
        )

    def do_GET(self):
        self._record()
        path = urllib.parse.urlsplit(self.path)
        if path.path == "/start":
            self._send(200, PAGE)
        elif path.path == "/search":
            query = urllib.parse.parse_qs(path.query)
            self._send(200, f"<p id=result>search:{query.get('q', [''])[0]}</p>")
        elif path.path == "/home":
            self._send(200, f"<p id=result>home:{self.headers.get('Cookie', '')}</p>")
        elif path.path == "/next":
            self._send(200, "<p id=result>next</p>")
        elif path.path == "/api":
            self._send(200, '{"answer": 42}')
        elif path.path == "/set":
            self._send(200, "ok", headers=[("Set-Cookie", "fetched=1; Path=/")])
        else:
            self._send(404, "<p>missing</p>")

    def do_POST(self):
        length = int(self.headers.get("Content-Length", 0))
        body = self.rfile.read(length)
        self._record(body)
        if self.path == "/login":
            self._send(303, "", headers=[("Location", "/home"), ("Set-Cookie", "session=s3cret; Path=/")])
        else:
            self._send(200, "<p id=result>echo</p>")


def _serve():
    server = ThreadingHTTPServer(("127.0.0.1", 0), _Handler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    return server, f"http://127.0.0.1:{server.server_address[1]}"


class _LocalServer(unittest.TestCase):
    """A window on /start of a local server; ``other`` is a second origin."""

    @classmethod
    def setUpClass(cls):
        cls.server, cls.base = _serve()
        cls.other_server, cls.other = _serve()

    @classmethod
    def tearDownClass(cls):
        for server in (cls.server, cls.other_server):
            server.shutdown()
            server.server_close()

    def setUp(self):
        _Handler.requests_seen.clear()
        self.win = Window()
        self.win.location = self.base + "/start"
        self.assertEqual(self.win.document.querySelector("h1").textContent, "Start")
        _Handler.requests_seen.clear()

    def q(self, selector):
        return self.win.document.querySelector(selector)

    def last_request(self):
        return _Handler.requests_seen[-1]

    def result(self):
        return self.q("#result").textContent


class TestNavigation(_LocalServer):

    # -- forms --------------------------------------------------------------------

    def test_get_form_puts_the_entries_in_the_query(self):
        self.q("#go").click()
        self.assertEqual(self.win.location.href, self.base + "/search?q=hello")
        self.assertEqual(self.result(), "search:hello")
        self.assertEqual(self.last_request()["referer"], self.base + "/start")

    def test_post_follows_the_redirect_and_keeps_the_cookie(self):
        self.q("#in").click()
        login, home = _Handler.requests_seen
        self.assertEqual((login["method"], login["path"]), ("POST", "/login"))
        self.assertEqual(urllib.parse.parse_qs(login["body"].decode()), {"user": ["ann"], "secret": ["p w"]})
        self.assertEqual(login["content_type"], "application/x-www-form-urlencoded")
        self.assertEqual(login["origin"], self.base)
        self.assertEqual(self.win.location.href, self.base + "/home")
        self.assertEqual(self.result(), "home:session=s3cret")
        self.win.location = self.base + "/home"  # the cookie stays with the window
        self.assertEqual(self.last_request()["cookie"], "session=s3cret")

    def test_submitter_overrides_and_value(self):
        self.q("#alt").click()
        sent = self.last_request()
        self.assertEqual(sent["path"], "/echo")
        self.assertEqual(urllib.parse.parse_qs(sent["body"].decode())["via"], ["alt"])

    def test_request_submit_and_submit_navigate(self):
        self.q("#search").requestSubmit()
        self.assertEqual(self.result(), "search:hello")
        self.win.location = self.base + "/start"
        self.q("#search").submit()
        self.assertEqual(self.result(), "search:hello")

    def test_multipart_upload(self):
        self.q("#file").files = [File([b"file body"], "notes.txt", {"type": "text/plain"})]
        self.q("#send").click()
        sent = self.last_request()
        self.assertTrue(sent["content_type"].startswith("multipart/form-data; boundary="))
        self.assertIn(b'name="note"', sent["body"])
        self.assertIn(b'filename="notes.txt"', sent["body"])
        self.assertIn(b"file body", sent["body"])

    def test_text_plain(self):
        self.q("#p").click()
        sent = self.last_request()
        self.assertEqual(sent["body"], b"a=1\r\n")
        self.assertTrue(sent["content_type"].startswith("text/plain"))

    def test_cancelled_submit_does_not_navigate(self):
        self.q("#search").addEventListener("submit", lambda event: event.preventDefault())
        self.q("#go").click()
        self.assertEqual(_Handler.requests_seen, [])
        self.assertEqual(self.win.location.href, self.base + "/start")

    def test_non_http_action_and_blank_target_stay(self):
        self.q("#m").click()
        self.q("#b").click()  # opens a new window, which loads /search; this one stays
        self.assertEqual(self.win.location.href, self.base + "/start")
        self.assertEqual([r["path"].rstrip("?") for r in _Handler.requests_seen], ["/search"])

    # -- links ----------------------------------------------------------------------

    def test_link_click_navigates(self):
        self.q("#next").click()
        self.assertEqual(self.win.location.href, self.base + "/next")
        self.assertEqual(self.result(), "next")

    def test_cancelled_click_does_not_navigate(self):
        link = self.q("#next")
        link.addEventListener("click", lambda event: event.preventDefault())
        link.click()
        self.assertEqual(_Handler.requests_seen, [])

    def test_fragment_link_stays_on_the_document(self):
        changes = []
        self.win.addEventListener("hashchange", lambda event: changes.append(event.newURL))
        document = self.win.document
        self.q("#frag").click()
        self.assertEqual(self.win.location.href, self.base + "/start#section")
        self.assertIs(self.win.document, document)
        self.assertEqual(changes, [self.base + "/start#section"])
        self.assertEqual(_Handler.requests_seen, [])

    def test_download_and_mailto_links_stay(self):
        self.q("#dl").click()
        self.q("#mailto").click()
        self.assertEqual(_Handler.requests_seen, [])

    def test_old_document_no_longer_navigates(self):
        old_link = self.q("#next")
        self.q("#go").click()
        _Handler.requests_seen.clear()
        old_link.click()
        self.assertEqual(_Handler.requests_seen, [])


class TestWindowFetch(_LocalServer):
    def test_relative_url_and_a_fetch_response(self):
        response = self.win.fetch("api").data  # relative to /start
        self.assertEqual((response.status, response.type, response.json()), (200, "basic", {"answer": 42}))
        self.assertEqual(self.last_request()["path"], "/api")
        self.assertEqual(self.last_request()["referer"], self.base + "/start")
        self.assertIsNone(self.last_request()["origin"])

    def test_same_origin_fetch_shares_the_window_cookies(self):
        self.q("#in").click()  # logs in: session=s3cret
        self.win.fetch("/api")
        self.assertEqual(self.last_request()["cookie"], "session=s3cret")
        self.win.fetch("/set")  # the response's cookie is kept for the next navigation
        self.win.location = self.base + "/home"
        self.assertEqual(self.result(), "home:session=s3cret; fetched=1")

    def test_credentials(self):
        self.q("#in").click()
        self.win.fetch("/api", {"credentials": "omit"})
        self.assertIsNone(self.last_request()["cookie"])
        self.win.fetch(self.other + "/api")  # cross-origin: same-origin credentials send none
        self.assertIsNone(self.last_request()["cookie"])
        self.win.fetch(self.other + "/api", {"credentials": "include"})
        self.assertEqual(self.last_request()["cookie"], "session=s3cret")

    def test_cross_origin_headers(self):
        response = self.win.fetch(self.other + "/api").data
        sent = self.last_request()
        self.assertEqual((sent["referer"], sent["origin"]), (self.base + "/", self.base))
        self.assertEqual(response.type, "cors")

    def test_post_sends_origin_and_referrer_policy(self):
        self.win.fetch("/echo", {"method": "POST", "body": "x=1", "referrerPolicy": "no-referrer"})
        sent = self.last_request()
        self.assertEqual((sent["method"], sent["body"]), ("POST", b"x=1"))
        self.assertIsNone(sent["referer"])
        self.assertEqual(sent["origin"], "null")

    def test_a_network_error_rejects(self):
        promise = self.win.fetch("http://127.0.0.1:9/nothing", timeout=1)
        self.assertEqual(promise.state, "rejected")


class TestNoWindow(unittest.TestCase):
    def test_documents_without_a_window_go_nowhere(self):
        page = html(body(form(input(_name="q"), button("Go", _id="go"), _action="http://127.0.0.1:9/x")))
        self.assertTrue(page.querySelector("#go").click())  # events only, no request
        self.assertTrue(a("x", _href="http://127.0.0.1:9/").click())

    def test_dialog_method_closes_the_dialog(self):
        page = html(body(dialog(form(button("OK", _id="ok", _value="yes"), _method="dialog"), _id="d")))
        box = page.querySelector("#d")
        box.showModal()
        page.querySelector("#ok").click()
        self.assertFalse(box.open)
        self.assertEqual(box.returnValue, "yes")


if __name__ == "__main__":
    unittest.main()
