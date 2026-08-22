"""
test_webapi
~~~~~~~~~~~~~~~~
"""

import json
import os
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from domonic.dom import *
from domonic.events import AbortController
from domonic.html import *
from domonic.javascript import *
from domonic.webapi import *
from domonic.webapi.console import Console, console
from domonic.webapi.encoding import (
    TextDecoder,
    TextDecoderStream,
    TextEncoder,
    TextEncoderStream,
)
from domonic.webapi.fetch import (
    Headers,
    Request,
    Response,
    fetch,
    fetch_pooled,
    fetch_set,
    fetch_threaded,
)
from domonic.webapi.url import URL, URLSearchParams
from domonic.webapi.urlpattern import URLPattern
from domonic.webapi.xhr import FormData, XMLHttpRequest

# from domonic.decorators import silence


class TestCase(unittest.TestCase):
    def test_console_api_surface(self):
        Console.reset()
        self.assertIs(console, Console)

        with patch("builtins.print"):
            self.assertEqual(Console.log("Hello %s", "World"), "Hello World")
            self.assertEqual(Console.log("Hello %s", substitute="again"), "Hello again")
            self.assertEqual(Console.log("value", 1, {"x": 2}), "value 1 {'x': 2}")
            self.assertEqual(
                Console.log(
                    "num=%d float=%f obj=%o %% %cstyled",
                    "4",
                    "2.5",
                    {"ok": True},
                    "color:red",
                ),
                "num=4 float=2.5 obj={'ok': True} % styled",
            )
            self.assertEqual(Console.info("info"), "info")
            self.assertEqual(Console.debug("debug"), "debug")
            self.assertEqual(Console.warn("warn"), "warn")
            self.assertEqual(Console.error(ValueError("bad")), "ValueError: bad")
            self.assertEqual(Console.exception("boom"), "boom")

            self.assertIsNone(Console.assert_(True, "hidden"))
            self.assertEqual(
                Console.assert_(False, "no %d", 4), "Assertion failed: no 4"
            )
            self.assertEqual(
                getattr(Console, "assert")(False, "alias"), "Assertion failed: alias"
            )

            self.assertEqual(Console.count(), 1)
            self.assertEqual(Console.count(), 2)
            self.assertEqual(Console.count("route"), 1)
            self.assertEqual(Console.countReset(), 0)
            self.assertEqual(Console.count(), 1)

            Console.time("load")
            self.assertIn("load:", Console.timeLog("load", "halfway"))
            self.assertIn("halfway", Console.timeLog("load", "halfway"))
            self.assertIn("load:", Console.timeEnd("load"))
            self.assertEqual(Console.timeLog("load"), "Timer 'load' does not exist")

            self.assertEqual(Console.group("outer"), "outer")
            self.assertEqual(Console.log("inside"), "  inside")
            self.assertEqual(Console.groupCollapsed("inner"), "inner")
            self.assertEqual(Console.log("deep"), "    deep")
            Console.groupEnd()
            self.assertEqual(Console.log("inside again"), "  inside again")
            Console.groupEnd()
            self.assertEqual(Console.log("outside"), "outside")

            self.assertIn("'a': 1", Console.dir({"a": 1}))
            self.assertIn("<div>hello</div>", Console.dirxml(div("hello")))

            table = Console.table(
                [{"name": "Ada", "lang": "Python"}, {"name": "Grace", "lang": "COBOL"}],
                ["name"],
            )
            self.assertIn("(index)", table)
            self.assertIn("Ada", table)
            self.assertIn("Grace", table)
            self.assertNotIn("Python", table)

            self.assertIn("Trace label", Console.trace("Trace %s", "label"))
            self.assertEqual(Console.timeStamp("paint"), "Timestamp: paint")
            Console.profile("render")
            self.assertIn("Profile 'render':", Console.profileEnd("render"))
            self.assertEqual(
                Console.profileEnd("render"), "Profile 'render' does not exist"
            )

    def test_encodingAPI(self):
        decoder = TextDecoder()
        self.assertEqual(decoder.encoding, "utf-8")
        self.assertFalse(decoder.fatal)
        self.assertFalse(decoder.ignoreBOM)

        self.assertEqual(decoder.decode(Uint8Array([240, 160, 174, 183])), "𠮷")
        self.assertEqual(decoder.decode(Int8Array([-16, -96, -82, -73])), "𠮷")
        self.assertEqual(decoder.decode(ArrayBuffer(0)), "")
        self.assertEqual(decoder.decode(bytearray([0xEF, 0xBB, 0xBF, 65])), "A")
        self.assertEqual(
            TextDecoder("utf-8", {"ignoreBOM": True}).decode(
                bytearray([0xEF, 0xBB, 0xBF, 65])
            ),
            "\ufeffA",
        )

        self.assertEqual(TextDecoder().decode(b"\xff"), "\ufffd")
        with self.assertRaises(UnicodeDecodeError):
            TextDecoder("utf-8", {"fatal": True}).decode(b"\xff")

        partial = TextDecoder()
        self.assertEqual(partial.decode(b"\xf0\x9f", {"stream": True}), "")
        self.assertEqual(partial.decode(b"\x92\xa9"), "💩")

        split_bom = TextDecoder()
        self.assertEqual(split_bom.decode(b"\xef", {"stream": True}), "")
        self.assertEqual(split_bom.decode(b"\xbb\xbfA"), "A")
        self.assertEqual(TextDecoder("utf-16").decode(b"\xff\xfeA\x00"), "A")

        win1251decoder = TextDecoder("windows-1251")
        b = Uint8Array([207, 240, 232, 226, 229, 242, 44, 32, 236, 232, 240, 33])
        self.assertEqual(win1251decoder.decode(b), "Привет, мир!")
        self.assertEqual(TextDecoder("iso-8859-1").decode(b"\x80"), "€")

        encoder = TextEncoder()
        self.assertEqual(encoder.encoding, "utf-8")
        self.assertEqual(encoder.encode("hello 💩"), b"hello \xf0\x9f\x92\xa9")
        with self.assertRaises(LookupError):
            TextEncoder("utf-16")

        dest = Uint8Array(8)
        result = encoder.encodeInto("A💩Z", dest)
        self.assertEqual(result["read"], 4)
        self.assertEqual(result.written, 6)
        self.assertEqual(
            bytes(dest.buffer.buffer[: result.written]), b"A\xf0\x9f\x92\xa9Z"
        )

        buffer = ArrayBuffer(4)
        view = DataView(buffer, 1, 2)
        result = encoder.encodeInto("é", view)
        self.assertEqual(result, {"read": 1, "written": 2})
        self.assertEqual(TextDecoder().decode(view), "é")
        self.assertEqual(list(buffer.buffer), [0, 0xC3, 0xA9, 0])

        tight = bytearray(4)
        result = encoder.encodeInto("A💩", tight)
        self.assertEqual(result, {"read": 1, "written": 1})
        self.assertEqual(tight, bytearray(b"A\x00\x00\x00"))

        decoder_stream = TextDecoderStream()
        self.assertEqual(decoder_stream.write(b"\xf0\x9f"), "")
        self.assertEqual(decoder_stream.write(b"\x92\xa9"), "💩")
        self.assertEqual(decoder_stream.read(), "💩")
        self.assertEqual(repr(decoder_stream), "<TextDecoderStream encoding=utf-8>")

        encoder_stream = TextEncoderStream()
        self.assertEqual(encoder_stream.write("ok"), b"ok")
        self.assertEqual(encoder_stream.read(), b"ok")
        self.assertEqual(repr(encoder_stream), "<TextEncoderStream encoding=utf-8>")

    def test_canvas(self):
        pass

    def test_clipboard(self):
        pass

    def test_cookiestore(self):
        pass

    def test_credentialmanagement(self):
        pass

    def test_crypto(self):
        pass

    def test_cssfontloading(self):
        pass

    def test_dragndrop(self):
        pass

    def test_filereader(self):
        pass

    def test_filesysmte(self):
        pass

    def test_fetch(self):
        headers = Headers("Content-Type: text/plain\r\nX-Test: one")
        headers.append("X-Test", "two")
        headers.append("Set-Cookie", "a=1")
        headers.append("Set-Cookie", "b=2")

        self.assertEqual(headers.get("CONTENT-TYPE"), "text/plain")
        self.assertEqual(headers.get("x-test"), "one, two")
        self.assertEqual(headers.get("missing", "fallback"), "fallback")
        self.assertEqual(headers.getSetCookie(), ["a=1", "b=2"])
        self.assertTrue(headers.has("content-type"))
        self.assertIn("x-test", headers)
        self.assertEqual(headers["X-Test"], "one, two")
        headers.set("X-Test", "three")
        self.assertEqual(headers.get("x-test"), "three")
        headers.delete("x-test")
        self.assertFalse(headers.has("x-test"))
        self.assertEqual(headers.keys(), ["content-type", "set-cookie"])
        self.assertEqual(
            headers.entries(),
            [("content-type", "text/plain"), ("set-cookie", "a=1, b=2")],
        )
        seen = []
        headers.forEach(lambda value, name, target: seen.append((name, value, target)))
        self.assertEqual(seen[0], ("content-type", "text/plain", headers))
        self.assertEqual(
            headers.reduce(lambda acc, value, name, target: acc + [name], []),
            ["content-type", "set-cookie"],
        )

        response = Response(
            '{"ok": true}',
            {"status": 201, "headers": {"Content-Type": "application/json"}},
        )
        clone = response.clone()
        self.assertEqual(response.status, 201)
        self.assertTrue(response.ok)
        self.assertEqual(response.headers.get("content-type"), "application/json")
        self.assertEqual(clone.json(), {"ok": True})
        self.assertFalse(response.bodyUsed)
        self.assertEqual(response.text(), '{"ok": true}')
        self.assertTrue(response.bodyUsed)
        with self.assertRaises(TypeError):
            response.clone()

        json_response = Response.json({"hello": "world"}, {"status": 202})
        self.assertEqual(json_response.status, 202)
        self.assertEqual(json_response.headers.get("content-type"), "application/json")
        self.assertEqual(json_response.json(), {"hello": "world"})
        redirect_response = Response.redirect("https://example.com/next", 303)
        self.assertTrue(redirect_response.redirected)
        self.assertEqual(
            redirect_response.headers.get("location"), "https://example.com/next"
        )
        self.assertEqual(Response.error().type, "error")
        with self.assertRaises(ValueError):
            Response.redirect("https://example.com/nope", 200)

        request = Request(
            "https://example.com/api",
            {
                "method": "POST",
                "headers": {"Content-Type": "application/x-www-form-urlencoded"},
                "body": "name=Ada",
                "credentials": "include",
            },
        )
        request_clone = request.clone()
        self.assertEqual(request.method, "POST")
        self.assertEqual(
            request.headers.get("content-type"), "application/x-www-form-urlencoded"
        )
        self.assertEqual(request.formData(), {"name": "Ada"})
        self.assertEqual(request_clone.text(), "name=Ada")
        with self.assertRaises(TypeError):
            Request("https://example.com/api", {"body": "not allowed"})
        json_request = Request(
            "https://example.com/api", {"method": "POST", "json": {"ok": True}}
        )
        self.assertEqual(json_request.headers.get("content-type"), "application/json")
        self.assertEqual(json_request.json(), {"ok": True})

        def fake_request(method, url, **kwargs):
            body = {"url": url, "method": method, "headers": kwargs.get("headers")}
            return SimpleNamespace(
                url=url,
                status_code=200,
                reason="OK",
                headers={"Content-Type": "application/json"},
                content=json.dumps(body).encode("utf-8"),
                history=[],
            )

        with patch("requests.request", side_effect=fake_request) as request_mock:
            promise = fetch(
                "https://example.com/data",
                init={"headers": {"Accept": "application/json"}},
            )
            self.assertEqual(promise.state, "fulfilled")
            self.assertIsInstance(promise.data, Response)
            self.assertEqual(promise.data.json()["url"], "https://example.com/data")
            self.assertEqual(
                request_mock.call_args.kwargs["headers"], {"accept": "application/json"}
            )

        with patch("requests.request", side_effect=fake_request):
            urls = ["https://example.com/one", "https://example.com/two"]
            self.assertEqual(
                fetch_set(urls, lambda response: response.json()["url"]).results, urls
            )
            self.assertEqual(
                fetch_threaded(urls, lambda response: response.json()["url"]).results,
                urls,
            )
            self.assertEqual(
                fetch_pooled(urls, lambda response: response.json()["url"]).results,
                urls,
            )

        with patch("requests.request", side_effect=RuntimeError("boom")):
            result = fetch_set(
                "https://example.com/fail",
                error_handler=lambda error: f"caught:{error}",
            )
            self.assertEqual(result.results, ["caught:boom"])

        controller = AbortController()
        controller.abort("stop")
        aborted = fetch(
            Request("https://example.com/never", {"signal": controller.signal})
        )
        self.assertEqual(aborted.state, "rejected")
        self.assertEqual(aborted.data, "stop")

    def test_url_and_urlsearchparams_edges(self):
        url = URL("/docs/page?one=1", "https://user:pass@example.com/base/")
        self.assertEqual(url.href, "https://user:pass@example.com/docs/page?one=1")
        self.assertEqual(url.username, "user")
        self.assertEqual(url.password, "pass")
        self.assertEqual(url.origin, "https://example.com")

        url.username = "ada"
        url.password = "secret"
        url.searchParams.append("two", "2")
        self.assertEqual(
            url.href, "https://ada:secret@example.com/docs/page?one=1&two=2"
        )
        self.assertEqual(url.search, "?one=1&two=2")
        self.assertEqual(url.searchParams.size, 2)
        self.assertTrue(url.searchParams.has("two", "2"))
        url.searchParams.delete("one", "1")
        self.assertEqual(url.href, "https://ada:secret@example.com/docs/page?two=2")

        params = URLSearchParams({"b": [2, 3], "a": "1"})
        self.assertEqual(list(params.pairs()), [("b", "2"), ("b", "3"), ("a", "1")])
        params.sort()
        self.assertEqual(params.toString(), "a=1&b=2&b=3")
        called = []
        params.forEach(lambda value, key, target: called.append((key, value, target)))
        self.assertEqual(called[0], ("a", "1", params))

        self.assertTrue(URL.canParse("/next", "https://example.com"))
        self.assertIsInstance(URL.parse("/next", "https://example.com"), URL)
        self.assertFalse(URL.canParse("/next"))
        self.assertEqual(URL.domainToASCII("mañana.com"), "xn--maana-pta.com")
        self.assertEqual(URL.domainToUnicode("xn--maana-pta.com"), "mañana.com")
        file_url = URL.pathToFileURL("README.md")
        self.assertEqual(URL.fileURLToPath(file_url), os.path.abspath("README.md"))

    def test_urlpattern(self):
        pattern = URLPattern(
            {"hostname": "*.example.com", "pathname": "/books/:id(\\d+)"}
        )
        self.assertTrue(pattern.hasRegExpGroups)
        self.assertTrue(pattern.test("https://store.example.com/books/123"))
        self.assertFalse(pattern.test("https://store.example.com/books/abc"))
        match = pattern.exec_("https://store.example.com/books/123")
        self.assertEqual(match["hostname"]["groups"]["0"], "store")
        self.assertEqual(match["pathname"]["groups"]["id"], "123")

        relative = URLPattern({"pathname": "/foo/*"})
        self.assertTrue(relative.test({"pathname": "/foo/bar"}))
        relative_match = relative.exec_("/foo/bar", "https://example.com/base")
        self.assertEqual(relative_match["pathname"]["groups"]["0"], "bar")
        self.assertEqual(
            relative_match["inputs"], ["/foo/bar", "https://example.com/base"]
        )

        typed = URLPattern({"pathname": "/:type(foo|bar)"})
        self.assertTrue(typed.test({"pathname": "/foo"}))
        self.assertFalse(typed.test({"pathname": "/baz"}))
        self.assertEqual(
            typed.exec_({"pathname": "/bar"})["pathname"]["groups"]["type"], "bar"
        )

    def test_xmlhttprequest_lifecycle_and_formdata(self):
        form_el = form(action="/", method="post")
        form_el += input(type="text", name="name", value="Ada")
        form_el += input(
            type="checkbox", name="subscribe", value="yes", checked="checked"
        )
        form_el += textarea("hello", name="bio")

        data = FormData(form_el)
        self.assertEqual(data.get("name"), "Ada")
        self.assertEqual(data.getAll("subscribe"), ["yes"])
        data.append("name", "Grace")
        self.assertEqual(data.getAll("name"), ["Ada", "Grace"])
        data.set("name", "Lin")
        self.assertEqual(data.get("name"), "Lin")
        self.assertTrue(data.has("bio"))
        self.assertEqual(list(data.keys()), ["subscribe", "bio", "name"])
        self.assertEqual(list(data.values()), ["yes", "hello", "Lin"])
        self.assertEqual(str(data), "subscribe=yes&bio=hello&name=Lin")
        data.delete("bio")
        self.assertFalse(data.has("bio"))

        events = []

        def fake_request(method, url, **kwargs):
            return SimpleNamespace(
                url=url,
                status_code=201,
                reason="Created",
                headers={"Content-Type": "application/json", "X-Test": "ok"},
                text='{"saved": true}',
                content=b'{"saved": true}',
                encoding="utf-8",
            )

        xhr = XMLHttpRequest(responseType="json")
        xhr.onreadystatechange = lambda event: events.append(("state", xhr.readyState))
        xhr.onload = lambda event: events.append(("load", xhr.status))
        xhr.onloadend = lambda event: events.append(("end", xhr.readyState))
        xhr.onprogress = lambda event: events.append(("progress", event.loaded))

        xhr.open("POST", "https://example.com/api")
        xhr.setRequestHeader("X-Test", "yes")
        with patch("requests.request", side_effect=fake_request) as request_mock:
            xhr.send("payload")

        self.assertEqual(xhr.readyState, XMLHttpRequest.DONE)
        self.assertEqual(xhr.status, 201)
        self.assertEqual(xhr.statusText, "Created")
        self.assertEqual(xhr.response, {"saved": True})
        self.assertEqual(xhr.getResponseHeader("x-test"), "ok")
        self.assertIn("content-type: application/json", xhr.getAllResponseHeaders())
        self.assertEqual(
            request_mock.call_args.args[:2], ("POST", "https://example.com/api")
        )
        self.assertEqual(request_mock.call_args.kwargs["headers"], {"x-test": "yes"})
        self.assertIn(("load", 201), events)
        self.assertIn(("end", XMLHttpRequest.DONE), events)

        errored = []
        xhr_error = XMLHttpRequest(
            onerror=lambda event: errored.append(str(event.error))
        )
        xhr_error.open("GET", "https://example.com/fail")
        with patch("requests.request", side_effect=RuntimeError("boom")):
            xhr_error.send()
        self.assertEqual(xhr_error.readyState, XMLHttpRequest.DONE)
        self.assertEqual(errored, ["boom"])

    def test_gamepad(self):
        pass

    def test_geolocation(self):
        pass

    def test_history(self):
        from domonic.window import Window

        win = Window(url="https://example.com/start")
        events = []
        win.addEventListener(
            "popstate", lambda event: events.append((event.type, event.state))
        )

        with patch.object(win, "_fetch_document", return_value=None):
            win.location = "https://example.com/one"
            win.location = "https://example.com/two"
            win.location = "https://example.com/three"

            self.assertEqual(win.history.length, 4)
            self.assertEqual(win.history.state, "https://example.com/three")

            self.assertEqual(win.history.back(), 2)
            self.assertEqual(win.location.href, "https://example.com/two")
            self.assertEqual(win.history.state, "https://example.com/two")

            self.assertEqual(win.history.forward(), 3)
            self.assertEqual(win.location.href, "https://example.com/three")

            self.assertEqual(win.history.go(-99), 3)
            self.assertEqual(win.location.href, "https://example.com/three")

            win.history.back()
            win.location = "https://example.com/four"
            self.assertEqual(win.history.states[-1], "https://example.com/four")
            self.assertNotIn("https://example.com/three", win.history.states)

            original_state = {"page": 1, "items": ["a"]}
            win.history.pushState(original_state, "Page 1", "/page-1")
            original_state["page"] = 99

            self.assertEqual(win.location.href, "https://example.com/page-1")
            self.assertEqual(win.history.state, {"page": 1, "items": ["a"]})
            self.assertEqual(win.history.entries[-1]["title"], "Page 1")

            win.history.state["items"].append("mutated")
            self.assertEqual(win.history.state, {"page": 1, "items": ["a"]})

            before_replace = win.history.length
            win.history.replaceState({"page": 2}, "Page 2", "?page=2")
            self.assertEqual(win.history.length, before_replace)
            self.assertEqual(win.location.href, "https://example.com/page-1?page=2")
            self.assertEqual(win.history.state, {"page": 2})

            win.history.scrollRestoration = "manual"
            self.assertEqual(win.history.scrollRestoration, "manual")
            with self.assertRaises(ValueError):
                win.history.scrollRestoration = "sometimes"

            win.history.back()
            self.assertEqual(win.location.href, "https://example.com/four")
            win.history.forward()
            self.assertEqual(win.history.state, {"page": 2})

        self.assertIn(("popstate", "https://example.com/two"), events)
        self.assertIn(("popstate", {"page": 2}), events)

    def test_gl(self):
        pass

    def test_intersectobserver(self):
        pass

    def test_mediacapabilities(self):
        pass

    def test_mediasession(self):
        pass

    def test_mediastream(self):
        pass

    def test_networkinfo(self):
        pass

    def test_notifications(self):
        pass

    def test_performance(self):
        pass

    def test_permissions(self):
        pass

    def test_serversentevents(self):
        # from domonic.webapi.sse import EventSource
        # es = EventSource('/sse')
        # es.onmessage = lambda event: print(event.data)
        # es.onopen = lambda event: print('open')
        # es.onclose = lambda event: print('close')
        # es.onerror = lambda event: print('error')
        # es.send('Hello')

        # TESTING - useage example... clone this and point at the stream
        # https://github.com/byteface/SSELoggerDemo
        pass

    def test_xhr(self):
        from domonic.html import br, button, div, form, hr, input
        from domonic.javascript import Global

        # def on_submit(event):
        #     event.preventDefault()
        #     alert("Form submitted")
        # def on_load(event):
        #     event.preventDefault()
        #     alert("Page loaded")
        # def on_error(event):
        #     event.preventDefault()
        #     alert("Page error")
        from domonic.webapi.xhr import FormData

        myform = form(action="/", method="post")
        myform += input(type="text", name="name", placeholder="Name")
        myform += input(type="text", name="email", placeholder="Email")
        myform += input(type="text", name="phone", placeholder="Phone")
        myform += input(type="text", name="message", placeholder="Message")
        # myform += button(type='submit', value='Submit')

        f = FormData(myform)
        self.assertEqual(str(f), "name=&email=&phone=&message=")

        # f.append('name', 'John')
        # f.append('age', '25')
        # f.append('email', '

        # myform = """
        # <form action="/">
        #     <input type="text" name="name" placeholder="Name">
        #     <input type="text" name="email" placeholder="Email">
        #     <input type="text" name="phone" placeholder="Phone">
        #     <input type="submit" value="Submit">
        # </form>
        # """
        # f = FormData(myform)
        # print(f)

    from domonic.decorators import silence

    @silence
    def test_xpath(self):

        from domonic import domonic
        from domonic.webapi.xpath import XPathEvaluator, XPathResult

        # api unit test based on mdn example
        # https://developer.mozilla.org/en-US/docs/Web/API/XPathEvaluator

        somehtml = """
        <div>XPath example</div>
        <div>Number of &lt;div&gt;s: <output></output></div>
        """
        try:
            page = domonic.parseString(
                somehtml
            )  # NOTE - probably requries html5lib install
        except Exception as exc:
            self.skipTest(
                f"domonic.parseString requires optional HTML parsing support: {exc}"
            )
        if page is None:
            self.skipTest("domonic.parseString requires optional HTML parsing support")
        evaluator = XPathEvaluator()
        expression = evaluator.createExpression("//div")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        assert result.snapshotLength == 2
        # print(result.nodes)

        try:
            import requests
        except ModuleNotFoundError:
            self.skipTest("requests is not installed")

        # TODO - dont eventual.technology to parse against
        try:
            r = requests.get("http://eventual.technology")
        except requests.exceptions.RequestException as exc:
            self.skipTest(f"external network is unavailable: {exc}")
        page = domonic.parseString(r.content.decode("utf-8"))

        # Selectors

        evaluator = XPathEvaluator()
        expression = evaluator.createExpression("//h1")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        assert (
            str(result.nodes[0])
            == '<h1 class="text-uppercase hero-text text-black">We are<span class="font-weight-bold d-block">Eventual Technology</span></h1>'
        )

        expression = evaluator.createExpression("//div//p")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        assert (
            str(result.nodes[0])
            == '<p class="headings-font-family text-uppercase lead">Welcome to the information age</p>'
        )

        expression = evaluator.createExpression("//ul/li")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes))

        expression = evaluator.createExpression("//ul/li/a")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes))

        expression = evaluator.createExpression("//ul/li/a")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes))

        expression = evaluator.createExpression("//ul/li/a")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes))

        expression = evaluator.createExpression("//div/*")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes))

        # root fails?
        # expression = evaluator.createExpression("/")
        # result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        # print(str(result.nodes[0]))

        # expression = evaluator.createExpression("/body")
        # result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        # print(str(result.nodes[0]))

        # NOTE - attributes reqiures underscores
        expression = evaluator.createExpression('//*[@_id="contact"]')
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes))

        expression = evaluator.createExpression(
            '//*[@_class="social-link social-link-instagram"]'
        )  # NOTE - requires all classes to match
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes))

        # expression = evaluator.createExpression("//input[@type='submit']")
        # result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        # print(str(result.nodes))

        expression = evaluator.createExpression("//a[contains(@_href, 'twitter')]")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes[0]))
        # wow. nice!

        expression = evaluator.createExpression("//a[contains(@href, 'twitter')]")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print("NO UNDERSCORE", str(result.nodes[0]))

        expression = evaluator.createExpression('//*[last()][name()="a"]')
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes[0]))
        # so cool this all works out of the box!

        expression = evaluator.createExpression("//span/text()")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes[0]))

        somepage = html(
            head(), body(h1("some title"), p("some text"), div("some more text"))
        )

        expression = evaluator.createExpression("//div/text()")
        result = expression.evaluate(somepage, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes[0]))

        """
        TODO - unit tests for the following so i know what works

        Descendant selectors
        h1	//h1	?
        div p	//div//p	?
        ul > li	//ul/li	?
        ul > li > a	//ul/li/a
        div > *	//div/*
        :root	/	?
        :root > body	/body

        Attribute selectors
        #id	//*[@id="id"]	?
        .class	//*[@class="class"] …kinda
        input[type="submit"]	//input[@type="submit"]
        a#abc[for="xyz"]	//a[@id="abc"][@for="xyz"]	?
        a[rel]	//a[@rel]
        a[href^='/']	//a[starts-with(@href, '/')]	?
        a[href$='pdf']	//a[ends-with(@href, '.pdf')]
        a[href*='://']	//a[contains(@href, '://')]
        a[rel~='help']	//a[contains(@rel, 'help')] …kinda

        Order selectors
        ul > li:first-of-type	//ul/li[1]	?
        ul > li:nth-of-type(2)	//ul/li[2]
        ul > li:last-of-type	//ul/li[last()]
        li#id:first-of-type	//li[1][@id="id"]	?
        a:first-child	//*[1][name()="a"]
        a:last-child	//*[last()][name()="a"]

        Siblings
        h1 ~ ul	//h1/following-sibling::ul	?
        h1 + ul	//h1/following-sibling::ul[1]
        h1 ~ #id	//h1/following-sibling::[@id="id"]

        jQuery
        $('ul > li').parent()	//ul/li/..	?
        $('li').closest('section')	//li/ancestor-or-self::section
        $('a').attr('href')	//a/@href	?
        $('span').text()	//span/text()

        Other things
        h1:not([id])	//h1[not(@id)]	?

        Text match	//button[text()="Submit"]	?
        Text match (substring)	//button[contains(text(),"Go")]

        Arithmetic	//product[@price > 2.50]

        Has children	//ul[*]
        Has children (specific)	//ul[li]
        Or logic	//a[@name or @href]	?
        Union (joins results)	//a | //div	?
        Class check
        //div[contains(concat(' ',normalize-space(@class),' '),' foobar ')]
        Xpath doesn’t have the “check if part of space-separated list” operator, so this is the workaround (source).

        #Expressions
        Steps and axes
        //	ul	/	a[@id='link']
        Axis	Step	Axis	Step
        Prefixes
        Prefix	Example	What
        //	//hr[@class='edge']	Anywhere
        ./	./a	Relative
        /	/html/body/div	Root
        Begin your expression with any of these.

        Axes
        Axis	Example	What
        /	//ul/li/a	Child
        //	//[@id="list"]//a	Descendant
        Separate your steps with /. Use two (//) if you don’t want to select direct children.

        Steps
        //div
        //div[@name='box']
        //[@id='link']
        A step may have an element name (div) and predicates ([...]). Both are optional. They can also be these other things:

        //a/text()     #=> "Go home"
        //a/@href      #=> "index.html"
        //a/*          #=> All a's child elements
        #Predicates
        Predicates
        //div[true()]
        //div[@class="head"]
        //div[@class="head"][@id="top"]
        Restricts a nodeset only if some condition is true. They can be chained.

        Operators
        # Comparison
        //a[@id = "xyz"]
        //a[@id != "xyz"]
        //a[@price > 25]
        # Logic (and/or)
        //div[@id="head" and position()=2]
        //div[(x and y) or not(z)]
        Use comparison and logic operators to make conditionals.

        Using nodes
        # Use them inside functions
        //ul[count(li) > 2]
        //ul[count(li[@class='hide']) > 0]
        # This returns `<ul>` that has a `<li>` child
        //ul[li]
        You can use nodes inside predicates.

        Indexing
        //a[1]                  # first <a>
        //a[last()]             # last <a>
        //ol/li[2]              # second <li>
        //ol/li[position()=2]   # same as above
        //ol/li[position()>1]   # :not(:first-of-type)
        Use [] with a number, or last() or position().

        Chaining order
        a[1][@href='/']
        a[@href='/'][1]
        Order is significant, these two are different.

        Nesting predicates
        //section[.//h1[@id='hi']]
        This returns <section> if it has an <h1> descendant with id='hi'.

        #Functions
        Node functions
        name()                     # //[starts-with(name(), 'h')]
        text()                     # //button[text()="Submit"]
                                # //button/text()
        lang(str)
        namespace-uri()
        count()                    # //table[count(tr)=1]
        position()                 # //ol/li[position()=2]
        Boolean functions
        not(expr)                  # button[not(starts-with(text(),"Submit"))]
        String functions
        contains()                 # font[contains(@class,"head")]
        starts-with()              # font[starts-with(@class,"head")]
        ends-with()                # font[ends-with(@class,"head")]
        concat(x,y)
        substring(str, start, len)
        substring-before("01/02", "/")  #=> 01
        substring-after("01/02", "/")   #=> 02
        translate()
        normalize-space()
        string-length()
        Type conversion
        string()
        number()
        boolean()
        #Axes
        Using axes
        //ul/li                       # ul > li
        //ul/child::li                # ul > li (same)
        //ul/following-sibling::li    # ul ~ li
        //ul/descendant-or-self::li   # ul li
        //ul/ancestor-or-self::li     # $('ul').closest('li')
        Steps of an expression are separated by /, usually used to pick child nodes. That’s not always true: you can specify a different “axis” with ::.

        //	ul	/child::	li
        Axis	Step	Axis	Step
        Child axis
        # both the same
        //ul/li/a
        //child::ul/child::li/child::a
        child:: is the default axis. This makes //a/b/c work.

        # both the same
        # this works because `child::li` is truthy, so the predicate succeeds
        //ul[li]
        //ul[child::li]
        # both the same
        //ul[count(li) > 2]
        //ul[count(child::li) > 2]
        Descendant-or-self axis
        # both the same
        //div//h4
        //div/descendant-or-self::h4
        // is short for the descendant-or-self:: axis.

        # both the same
        //ul//[last()]
        //ul/descendant-or-self::[last()]
        Other axes
        Axis	Abbrev	Notes
        ancestor
        ancestor-or-self
        attribute	@	@href is short for attribute::href
        child	div is short for child::div
        descendant
        descendant-or-self	//	// is short for /descendant-or-self::node()/
        namespace
        self	.	. is short for self::node()
        parent	..	.. is short for parent::node()
        following
        following-sibling
        preceding
        preceding-sibling
        There are other axes you can use.

        Unions
        //a | //span
        Use | to join two expressions.

        #More examples
        Examples
        //*                 # all elements
        count(//*)          # count all elements
        (//h1)[1]/text()    # text of the first h1 heading
        //li[span]          # find a <li> with an <span> inside it
                            # ...expands to //li[child::span]
        //ul/li/..          # use .. to select a parent
        Find a parent
        //section[h1[@id='section-name']]
        Finds a <section> that directly contains h1#section-name

        //section[//h1[@id='section-name']]
        Finds a <section> that contains h1#section-name. (Same as above, but uses descendant-or-self instead of child)

        Closest
        ./ancestor-or-self::[@class="box"]
        Works like jQuery’s $().closest('.box').

        Attributes
        //item[@price > 2*@discount]
        """


if __name__ == "__main__":
    unittest.main()
