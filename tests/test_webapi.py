"""
test_webapi
~~~~~~~~~~~~~~~~
"""

import json
import os
import tempfile
import threading
import time
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from domonic.dom import *
from domonic.events import AbortController
from domonic.html import *
from domonic.javascript import *
from domonic.webapi.clipboard import Clipboard, ClipboardItem
from domonic.webapi import *
from domonic.webapi.console import Console, console
from domonic.webapi.cookiestore import CookieChangeEvent, CookieListItem, CookieStore
from domonic.webapi.canvas import (
    CanvasRenderingContext2D,
    ImageData,
    WebGL2RenderingContext,
    WebGLRenderingContext,
)
from domonic.webapi.credentials import (
    Credential,
    CredentialsContainer,
    FederatedCredential,
    PasswordCredential,
)
from domonic.webapi.cssfontloading import FontFace, FontFaceSet
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
from domonic.webapi.crypto import Crypto, CryptoKey, SubtleCrypto, crypto
from domonic.webapi.file import Blob, File, FileList, FileReader, FileReaderSync
from domonic.webapi.dragndrop import DataTransfer
from domonic.webapi.gamepad import Gamepad, GamepadButton, GamepadManager
from domonic.webapi.geo import Geolocation, GeolocationCoordinates, GeolocationPosition
from domonic.webapi.mediacapabilities import MediaCapabilities
from domonic.webapi.mediadevices import (
    InputDeviceInfo,
    MediaDeviceInfo,
    MediaDevices,
    MediaStream,
    MediaStreamTrack,
)
from domonic.webapi.mediasession import MediaSession
from domonic.webapi.messaging import BroadcastChannel, MessageChannel, MessagePort
from domonic.webapi.netinfo import NetworkInformation
from domonic.webapi.notifications import Notification
from domonic.webapi.permissions import Permissions, PermissionStatus
from domonic.webapi.sanitizer import Sanitizer
from domonic.webapi.scheduler import (
    Scheduler,
    TaskController,
    TaskPriorityChangeEvent,
    TaskSignal,
    scheduler,
)
from domonic.webapi.serviceworker import (
    ServiceWorker,
    ServiceWorkerContainer,
    ServiceWorkerRegistration,
)
from domonic.webapi.sse import EventSource
from domonic.webapi.streams import (
    CompressionStream,
    DecompressionStream,
    ReadableStream,
    TransformStream,
    WritableStream,
)
from domonic.webapi.url import URL, URLSearchParams
from domonic.webapi.urlpattern import URLPattern
from domonic.webapi.webstorage import Storage
from domonic.webapi.webworkers import (
    DedicatedWorkerGlobalScope,
    Worker as WebWorker,
    get_current_worker_scope,
)
from domonic.webapi.xhr import FormData, XMLHttpRequest
from domonic.window import Window as BrowserWindow

# from domonic.decorators import silence


def _debug_print(*args, **kwargs):
    return None


class TestCase(unittest.TestCase):
    def test_eventsource_blocking_dispatches_messages_and_state(self):
        class FakeSSEClient:
            def __init__(self, url, **kwargs):
                self.url = url
                self.kwargs = kwargs
                self.events = [
                    SimpleNamespace(data="hello", event="message", id="1", retry=None),
                    SimpleNamespace(data="ready", event="status", id="2", retry=1500),
                    SimpleNamespace(data="reset", event="message", id="", retry=0),
                ]

            def __iter__(self):
                return iter(self.events)

        opened = []
        states = []
        messages = []
        custom = []

        with patch("domonic.webapi.sse.SSEClient", FakeSSEClient):
            source = EventSource(
                "/events",
                {
                    "auto_start": False,
                    "lastEventId": "0",
                    "onopen": lambda event: opened.append(event.type),
                    "onmessage": lambda event: messages.append(("handler", event.data)),
                    "onreadystatechange": lambda event: states.append(source.readyState),
                },
                timeout=10,
            )
            source.addEventListener(
                "message",
                lambda event: messages.append(
                    ("listener", event.data, event.lastEventId)
                ),
            )
            source.addEventListener(
                "status", lambda event: custom.append((event.data, event.lastEventId))
            )

            source.start(blocking=True)

        self.assertEqual(opened, ["open"])
        self.assertIn(EventSource.OPEN, states)
        self.assertEqual(states[-1], EventSource.CLOSED)
        self.assertEqual(
            messages,
            [
                ("listener", "hello", "1"),
                ("handler", "hello"),
                ("listener", "reset", ""),
                ("handler", "reset"),
            ],
        )
        self.assertEqual(custom, [("ready", "2")])
        self.assertEqual(source._lastEventId, "")
        self.assertEqual(source._retry, 0)
        self.assertEqual(source._client.kwargs["last_id"], "0")
        self.assertEqual(source._client.kwargs["timeout"], 10)

    def test_eventsource_error_callback_gets_exception(self):
        class BrokenSSEClient:
            def __init__(self, *args, **kwargs):
                raise RuntimeError("stream broke")

        errors = []

        with patch("domonic.webapi.sse.SSEClient", BrokenSSEClient):
            source = EventSource(
                "/events",
                {
                    "auto_start": False,
                    "onerror": lambda event: errors.append(event.error),
                },
            )
            source.start(blocking=True)

        self.assertEqual(str(errors[0]), "stream broke")
        self.assertEqual(source.readyState, EventSource.CLOSED)

    def test_sanitizer_api(self):
        dirty = (
            '<p onclick="evil()">Hello <script>alert(1)</script>'
            '<a href="javascript:alert(1)" data-id="7">link</a></p>'
        )
        self.assertEqual(Sanitizer().sanitizeToString(dirty), "<p>Hello <a>link</a></p>")

        empty = Sanitizer({})
        self.assertIn("<script>alert(1)</script>", empty.sanitizeToString(dirty))
        self.assertIn('onclick="evil()"', empty.sanitizeToString(dirty))

        configured = (
            Sanitizer({"elements": ["div", "span", "b"], "attributes": ["id"]})
            .replaceElementWithChildren("b")
            .allowElement("em")
            .setComments(True)
        )
        self.assertEqual(
            configured.sanitizeToString(
                '<div><span id="ok" class="drop">safe</span><b>bold</b>'
                "<em>yes</em><!--kept--><script>bad</script></div>"
            ),
            '<div><span id="ok">safe</span>bold<em>yes</em><!--kept--></div>',
        )

        remover = Sanitizer({"removeElements": ["span"]}).removeAttribute("lang")
        self.assertEqual(
            remover.sanitizeToString('<p lang="en">a<span>b</span><i lang="fr">c</i></p>'),
            "<p>a<i>c</i></p>",
        )

        data_attrs = Sanitizer().setDataAttributes(True)
        self.assertEqual(
            data_attrs.sanitizeToString('<div data-id="1" onclick="x()">ok</div>'),
            '<div data-id="1">ok</div>',
        )

        legacy = Sanitizer({"allowAttributes": {"style": ["span"]}})
        self.assertEqual(
            legacy.sanitizeToString(
                "<div style='cool'><span id='x' style='font-weight: bold'>ok</span></div>"
            ),
            '<div><span style="font-weight: bold">ok</span></div>',
        )

        with self.assertRaises(TypeError):
            Sanitizer({"elements": ["p"], "removeElements": ["script"]})

        with self.assertRaises(TypeError):
            Sanitizer({"attributes": ["id"], "removeAttributes": ["class"]})

    def test_sanitizer_dom_integration(self):
        target = div()
        target.setHTML('<p onclick="evil()">ok<script>bad</script></p>')
        self.assertEqual(str(target), "<div><p>ok</p></div>")

        target.setHTMLUnsafe('<p onclick="evil()">ok<script>bad</script></p>')
        self.assertEqual(
            str(target), '<div><p onclick="evil()">ok<script>bad</script></p></div>'
        )

        target.setHTMLUnsafe(
            '<p onclick="evil()">ok<script>bad</script></p>',
            {"sanitizer": {"removeElements": ["script"], "removeAttributes": ["onclick"]}},
        )
        self.assertEqual(str(target), "<div><p>ok</p></div>")

        document = Document.parseHTML(
            '<main onclick="evil()">ok<script>bad</script>'
            '<a href="javascript:bad()">x</a></main>'
        )
        self.assertEqual(
            str(document),
            '<html><head></head><body><main>ok<a>x</a></main></body></html>',
        )
        self.assertEqual(document.body.querySelector("main").textContent, "okx")

        unsafe_document = Document.parseHTMLUnsafe("<section><script>bad</script></section>")
        self.assertEqual(
            str(unsafe_document),
            "<html><head></head><body><section><script>bad</script></section></body></html>",
        )

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

    def test_streams_api(self):
        source = ReadableStream(b"hello")
        self.assertEqual(source.getReader(), b"hello")
        self.assertEqual(source.read(2), b"he")
        self.assertEqual(source.read(), b"llo")

        writable = WritableStream()
        source = ReadableStream(b"stored")
        self.assertEqual(source.pipeTo(writable), b"stored")
        self.assertEqual(writable.read(), b"stored")

        upper = TransformStream(lambda chunk: chunk.upper())
        self.assertEqual(ReadableStream(b"ok").pipeThrough(upper).read(), b"OK")

        payload = b"domonic streams " * 32
        for format in ("gzip", "deflate", "deflate-raw"):
            with self.subTest(format=format):
                compressed = CompressionStream(format).compress(payload)
                self.assertEqual(
                    DecompressionStream(format).decompress(compressed),
                    payload,
                )

                compressor = CompressionStream(format)
                compressor.write(payload[:18])
                compressor.write(payload[18:])
                compressor.close()

                decompressor = DecompressionStream(format)
                compressed_payload = compressor.read()
                decompressor.write(compressed_payload[:7])
                decompressor.write(compressed_payload[7:])
                decompressor.close()
                self.assertEqual(decompressor.read(), payload)

        gzip_stream = ReadableStream("hello compression").pipeThrough(
            CompressionStream("gzip")
        )
        self.assertEqual(
            DecompressionStream("gzip").decompress(gzip_stream.read()),
            b"hello compression",
        )

        with self.assertRaises(TypeError):
            CompressionStream("brotli")

    def test_scheduler_api(self):
        immediate = scheduler.postTask(lambda: "ready")
        self.assertEqual(immediate.state, "fulfilled")
        self.assertEqual(immediate.data, "ready")
        self.assertEqual(scheduler.yield_().state, "fulfilled")
        self.assertEqual(getattr(scheduler, "yield")().state, "fulfilled")

        queued = Scheduler(auto_run=False)
        order = []
        visible = queued.postTask(
            lambda: order.append("visible") or "visible"
        )
        background = queued.postTask(
            lambda: order.append("background") or "background",
            {"priority": "background"},
        )
        blocking = queued.postTask(
            lambda: order.append("blocking") or "blocking",
            {"priority": "user-blocking"},
        )

        self.assertEqual(visible.state, "pending")
        self.assertEqual(queued.run(), ["blocking", "visible", "background"])
        self.assertEqual(order, ["blocking", "visible", "background"])
        self.assertEqual(blocking.data, "blocking")
        self.assertEqual(background.data, "background")

        controller = TaskController({"priority": "user-blocking"})
        self.assertIsInstance(controller.signal, TaskSignal)
        changes = []
        controller.signal.addEventListener(
            "prioritychange",
            lambda event: changes.append(
                (event.previousPriority, event.target.priority, type(event))
            ),
        )

        queued = Scheduler(auto_run=False)
        mutable = queued.postTask(
            lambda: order.append("mutable") or "mutable",
            {"signal": controller.signal},
        )
        controller.setPriority("background")
        self.assertEqual(
            changes,
            [("user-blocking", "background", TaskPriorityChangeEvent)],
        )
        queued.run()
        self.assertEqual(mutable.data, "mutable")

        controller = TaskController()
        aborted = Scheduler(auto_run=False)
        promise = aborted.postTask(lambda: "never", {"signal": controller.signal})
        controller.abort("stop")
        aborted.run()
        self.assertEqual(promise.state, "rejected")
        self.assertEqual(promise.data, "stop")

        with self.assertRaises(TypeError):
            scheduler.postTask(None)
        with self.assertRaises(TypeError):
            TaskController({"priority": "urgent"})

        delayed = Scheduler()
        done = threading.Event()
        promise = delayed.postTask(
            lambda: done.set() or "later",
            {"delay": 1},
        )
        self.assertTrue(done.wait(1))
        time.sleep(0.01)
        self.assertEqual(promise.state, "fulfilled")
        self.assertEqual(promise.data, "later")

    def test_canvas(self):
        surface = canvas(width=320, height=150)
        ctx = surface.getContext("2d")

        self.assertIsInstance(ctx, CanvasRenderingContext2D)
        self.assertIs(surface.getContext("2d"), ctx)
        self.assertEqual((ctx.width, ctx.height), (320, 150))

        ctx.fillStyle = "#f00"
        ctx.fillRect(0, 0, 10, 10)
        ctx.beginPath()
        ctx.moveTo(0, 0)
        ctx.lineTo(10, 10)
        ctx.stroke()
        ctx.fillText("domonic", 5, 20)

        self.assertEqual(ctx.commands[-1]["name"], "fillText")
        self.assertGreater(ctx.measureText("domonic").width, 0)
        self.assertIsInstance(ctx.createImageData(2, 1), ImageData)
        self.assertEqual(len(ctx.getImageData(0, 0, 2, 2).data), 16)
        self.assertIsNone(surface.getContext("webgl"))

        blob = surface.toBlob()
        self.assertIsInstance(blob, Blob)
        self.assertEqual(blob.type, "image/png")
        self.assertTrue(surface.toDataURL().startswith("data:image/png;base64,"))

        captured = surface.captureStream(30)
        self.assertEqual(captured.getVideoTracks()[0].label, "Canvas capture")

        offscreen = surface.transferControlToOffscreen()
        self.assertEqual((offscreen.width, offscreen.height), (320, 150))
        self.assertIsInstance(offscreen.getContext("2d"), CanvasRenderingContext2D)

    def test_clipboard(self):
        clipboard = Clipboard()

        with patch("domonic.webapi.clipboard.pyperclip", None):
            self.assertEqual(clipboard.writeText("hello"), "hello")
            self.assertEqual(clipboard.readText(), "hello")

            self.assertEqual(clipboard.writeHTML("<b>hi</b>"), "<b>hi</b>")
            self.assertEqual(clipboard.readHTML(), "<b>hi</b>")

            image = b"\x89PNG"
            self.assertEqual(clipboard.writeImage(image), image)
            self.assertEqual(clipboard.readImage(), image)

            self.assertEqual(clipboard.writeBuffer(bytearray(b"abc")), b"abc")
            self.assertEqual(clipboard.readBuffer(), b"abc")

            item = ClipboardItem(
                {"text/plain": "plain", "application/json": '{"ok": true}'}
            )
            self.assertEqual(item.types, ["text/plain", "application/json"])
            self.assertEqual(item.getType("application/json"), '{"ok": true}')
            self.assertTrue(ClipboardItem.supports("text/html"))

            clipboard.write([item])
            [read_item] = clipboard.read()
            self.assertIsInstance(read_item, ClipboardItem)
            self.assertEqual(read_item.getType("text/plain"), "plain")
            self.assertEqual(
                clipboard.readData("application/json"),
                '{"ok": true}',
            )

        win = BrowserWindow()
        self.assertIsInstance(win.navigator.clipboard, Clipboard)

    def test_cookiestore(self):
        store = CookieStore()
        changes = []
        store.addEventListener(
            "change",
            lambda event: changes.append((event.changed, event.deleted)),
        )

        self.assertEqual(store.set("theme", "dark").state, "fulfilled")
        cookie = store.get("theme").data
        self.assertIsInstance(cookie, CookieListItem)
        self.assertEqual(cookie.name, "theme")
        self.assertEqual(cookie.value, "dark")
        self.assertEqual(cookie.path, "/")
        self.assertIsInstance(changes[-1][0][0], CookieListItem)

        store.set({"name": "session", "value": "abc", "secure": True})
        self.assertEqual(
            [cookie.name for cookie in store.getAll().data],
            ["theme", "session"],
        )
        self.assertTrue(store.get({"name": "session"}).data.secure)

        self.assertEqual(store.delete("theme").state, "fulfilled")
        self.assertIsNone(store.get("theme").data)
        self.assertEqual(changes[-1][1][0].name, "theme")
        self.assertIsInstance(CookieChangeEvent("change"), CookieChangeEvent)

        win = BrowserWindow()
        win.document.cookie = "token=xyz; path=/"
        self.assertEqual(win.cookieStore.get("token").data.value, "xyz")
        win.cookieStore.set("mode", "test")
        self.assertIn("mode=test", win.document.cookie)

        replacement = Document()
        win.document = replacement
        win.cookieStore.set("fresh", "yes")
        self.assertIn("fresh=yes", replacement.cookie)

    def test_credentialmanagement(self):
        credentials = CredentialsContainer()
        created = credentials.create(
            {"password": {"id": "ada", "name": "Ada", "password": "lovelace"}}
        )
        self.assertEqual(created.state, "fulfilled")
        self.assertIsInstance(created.data, PasswordCredential)
        self.assertEqual(created.data.type, "password")

        stored = credentials.store(created.data)
        self.assertIs(stored.data, created.data)

        fetched = credentials.get({"password": True, "id": "ada"})
        self.assertIs(fetched.data, created.data)

        federated = credentials.create(
            {"federated": {"id": "grace", "provider": "https://id.example"}}
        ).data
        self.assertIsInstance(federated, FederatedCredential)
        credentials.store(federated)
        self.assertIs(
            credentials.get({"federated": True, "id": "grace"}).data,
            federated,
        )

        self.assertIsInstance(Credential("guest"), Credential)
        credentials.preventSilentAccess()
        self.assertIsNone(credentials.get({"password": True}).data)
        self.assertIs(
            credentials.get({"password": True, "mediation": "required"}).data,
            created.data,
        )
        with self.assertRaises(TypeError):
            credentials.store({"id": "not-a-credential"})

    def test_crypto(self):
        with patch(
            "domonic.webapi.crypto.secrets.token_bytes",
            side_effect=lambda size: bytes(range(size)),
        ):
            random_bytes = Uint8Array(16)
            result = crypto.getRandomValues(random_bytes)
            self.assertIs(result, random_bytes)
            self.assertEqual(random_bytes.byteLength, 16)
            self.assertEqual(
                [random_bytes[i] for i in range(random_bytes.length)],
                list(range(16)),
            )

            random_words = Uint32Array(4)
            Crypto.getRandomValues(random_words)
            self.assertEqual(random_words.byteLength, 16)
            self.assertEqual(bytes(random_words.buffer.buffer), bytes(range(16)))

            raw = bytearray(8)
            Crypto.getRandomValues(raw)
            self.assertEqual(raw, bytearray(range(8)))

        with self.assertRaises(TypeError):
            Crypto.getRandomValues(Float32Array(2))
        with self.assertRaises(DOMException):
            Crypto.getRandomValues(Uint8Array(65537))

        uuid_value = crypto.randomUUID()
        self.assertRegex(
            uuid_value,
            r"^[0-9a-f]{8}-[0-9a-f]{4}-4[0-9a-f]{3}-[89ab][0-9a-f]{3}-[0-9a-f]{12}$",
        )

        digest = crypto.subtle.digest("SHA-256", b"hello")
        self.assertEqual(digest.state, "fulfilled")
        self.assertEqual(
            digest.data.hex(),
            "2cf24dba5fb0a30e26e83b2ac5b9e29e"
            "1b161e5c1fa7425e73043362938b9824",
        )

        buffer = ArrayBuffer(5)
        Uint8Array(buffer).set([104, 101, 108, 108, 111], 0)
        self.assertEqual(
            SubtleCrypto.digestSync({"name": "SHA-1"}, buffer).hex(),
            "aaf4c61ddcc5e8a2dabede0f3b482cd9aea9434d",
        )
        self.assertEqual(
            crypto.subtle.digest("SHA-512", Uint8Array(buffer)).data,
            SubtleCrypto.digestSync("SHA-512", b"hello"),
        )
        self.assertEqual(
            crypto.subtle.digest("SHA-384", DataView(buffer, 1, 3)).data,
            SubtleCrypto.digestSync("SHA-384", b"ell"),
        )

        rejected = crypto.subtle.digest("MD5", b"nope")
        self.assertEqual(rejected.state, "rejected")
        self.assertIsInstance(rejected.data, DOMException)

        key = CryptoKey(
            "secret",
            True,
            {"name": "HMAC", "hash": "SHA-256"},
            ["sign", "verify"],
        )
        self.assertEqual(key.type, "secret")
        self.assertTrue(key.extractable)
        self.assertEqual(key.algorithm["name"], "HMAC")
        self.assertEqual(key.usages, ("sign", "verify"))

    def test_cssfontloading(self):
        face = FontFace(
            "Domonic Sans",
            'url("/fonts/domonic.woff2")',
            {"weight": "700", "display": "swap"},
        )
        loaded = []
        face.addEventListener("load", lambda event: loaded.append(event.target.status))

        self.assertEqual(face.status, "unloaded")
        self.assertEqual(face.load().state, "fulfilled")
        self.assertEqual(face.status, "loaded")
        self.assertEqual(loaded, ["loaded"])
        self.assertIn("font-display: swap", face.toCSS())

        fonts = FontFaceSet([face])
        events = []
        fonts.addEventListener(
            "loadingdone", lambda event: events.append(event.fontfaces)
        )

        self.assertTrue(fonts.check('700 16px "Domonic Sans"'))
        self.assertEqual(fonts.load("16px Domonic Sans").data, [face])
        self.assertEqual(events, [[face]])
        self.assertEqual(fonts.ready.data, fonts)

        seen = []
        fonts.forEach(lambda value, key, owner: seen.append((value, key, owner)))
        self.assertEqual(seen, [(face, face, fonts)])
        self.assertTrue(fonts.delete(face))
        self.assertFalse(fonts.check("16px Domonic Sans"))

        doc = Document()
        self.assertIsInstance(doc.fonts, FontFaceSet)

    def test_dragndrop(self):
        transfer = DataTransfer()
        file = File([b"hello"], "hello.txt")
        image = div("drag preview")

        item = transfer.items.add(file)
        transfer.setData("text/plain", "dragged")
        transfer.setDragImage(image, 12, 8)

        self.assertEqual(item.kind, "file")
        self.assertIs(item.getAsFile(), file)
        self.assertEqual(transfer.files.length, 1)
        self.assertIs(transfer.files.item(0), file)
        self.assertIn("Files", transfer.types)
        self.assertEqual(transfer.items.item(1).getAsString(), "dragged")
        self.assertIn("text/plain", transfer.types)
        self.assertEqual(transfer.getData("missing/type"), "")
        self.assertIs(transfer.dragImage, image)
        self.assertEqual((transfer.dragImageX, transfer.dragImageY), (12, 8))

        seen = []
        self.assertEqual(transfer.items.item(1).getAsString(seen.append), "dragged")
        self.assertEqual(seen, ["dragged"])

        transfer.setData("text/plain", "updated")
        self.assertEqual(transfer.getData("text/plain"), "updated")
        self.assertEqual(
            [item.type for item in transfer.items if item.kind == "string"],
            ["text/plain"],
        )

        drag_source = div("source")
        self.assertIs(transfer.addElement(drag_source), drag_source)
        self.assertIs(transfer.dragElement, drag_source)

        transfer.clearData("text/plain")
        self.assertNotIn("text/plain", transfer.types)
        self.assertEqual(transfer.files.length, 1)

        transfer.clearData()
        self.assertEqual(transfer.types, ["Files"])
        self.assertEqual(transfer.items.length, 1)

        self.assertIsNone(transfer.items.remove(99))
        removed = transfer.items.remove(0)
        self.assertIs(removed.getAsFile(), file)
        self.assertEqual(transfer.files.length, 0)
        self.assertNotIn("Files", transfer.types)

    def test_filereader(self):
        blob = Blob(["hello", b" ", bytearray(b"world")], {"type": "text/plain"})
        self.assertEqual(blob.size, 11)
        self.assertEqual(blob.type, "text/plain")
        self.assertEqual(blob.text(), "hello world")
        self.assertEqual(blob.slice(6, None).text(), "world")
        self.assertEqual(blob.slice(-5, -1).text(), "worl")

        file = File([blob, "!"], "greeting.txt", {"lastModified": 1234})
        self.assertIsInstance(file, Blob)
        self.assertEqual(file.name, "greeting.txt")
        self.assertEqual(file.type, "text/plain")
        self.assertEqual(file.lastModified, 1234)
        self.assertEqual(file.text(), "hello world!")

        with tempfile.NamedTemporaryFile("wb", suffix=".txt") as handle:
            handle.write(b"from disk")
            handle.flush()
            disk_file = File.fromPath(handle.name)
        self.assertEqual(disk_file.name, os.path.basename(handle.name))
        self.assertEqual(disk_file.text(), "from disk")

        files = FileList([file])
        self.assertEqual(files.length, 1)
        self.assertIs(files.item(0), file)
        self.assertIsNone(files.item(99))

        reader = FileReader()
        events = []
        reader.addEventListener("loadstart", lambda event: events.append(event.type))
        reader.onprogress = lambda event: events.append((event.type, event.loaded))
        reader.onload = lambda event: events.append((event.type, reader.result))
        reader.onloadend = lambda event: events.append(event.type)
        reader.readAsText(file)

        self.assertEqual(reader.readyState, FileReader.DONE)
        self.assertEqual(reader.result, "hello world!")
        self.assertEqual(events[0], "loadstart")
        self.assertIn(("progress", file.size), events)
        self.assertIn(("load", "hello world!"), events)
        self.assertEqual(events[-1], "loadend")

        reader.readAsArrayBuffer(file)
        self.assertEqual(reader.result, b"hello world!")
        reader.readAsDataURL(Blob([b"ok"], {"type": "text/plain"}))
        self.assertEqual(reader.result, "data:text/plain;base64,b2s=")

        sync = FileReaderSync()
        self.assertEqual(sync.readAsBinaryString(Blob([b"\xff"])), "ÿ")

        object_url = URL.createObjectURL(file)
        fetched = fetch(object_url).data
        self.assertEqual(fetched.blob().text(), "hello world!")
        URL.revokeObjectURL(object_url)
        self.assertEqual(fetch(object_url).state, "rejected")

        data_response = fetch("data:text/plain,hello%20data").data
        self.assertEqual(data_response.text(), "hello data")

    def test_filesysmte(self):
        storage = Storage()
        storage.setItem("theme", "dark")
        storage["count"] = 2
        storage.flag = True

        self.assertEqual(storage.getItem("theme"), "dark")
        self.assertEqual(storage["count"], "2")
        self.assertEqual(storage.flag, "True")
        self.assertEqual(storage.length, 3)
        self.assertEqual(storage.key(0), "theme")
        self.assertIsNone(storage.key(99))
        self.assertIn("count", storage)
        self.assertEqual(storage.toJSON()["flag"], "True")

        storage.removeItem("count")
        self.assertIsNone(storage.getItem("count"))
        storage.clear()
        self.assertEqual(storage.length, 0)

        with tempfile.NamedTemporaryFile("w", delete=False) as handle:
            path = handle.name
        try:
            persisted = Storage(path)
            persisted.setItem("token", "abc")
            self.assertEqual(Storage(path).getItem("token"), "abc")
            persisted.clear()
            self.assertEqual(Storage(path).length, 0)
        finally:
            os.unlink(path)

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

        upload = File([b"report"], "report.txt", {"type": "text/plain"})
        file_form = form(input(type="file", name="upload"))
        file_form.querySelector("input").files = FileList([upload])
        file_data = FormData(file_form)
        self.assertIs(file_data.get("upload"), upload)
        self.assertEqual(str(file_data), "upload=report.txt")
        self.assertEqual(list(file_data.entryDetails()), [("upload", upload, "report.txt")])

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
        button = GamepadButton(0.25, pressed=True, touched=True)
        pad = Gamepad(
            "Test Pad",
            axes=[0, 1],
            buttons=[button, {"value": 1, "pressed": True}],
            mapping="standard",
        )
        manager = GamepadManager()
        events = []
        manager.addEventListener(
            "gamepadconnected",
            lambda event: events.append(("connect", event.gamepad.id)),
        )
        manager.addEventListener(
            "gamepaddisconnected",
            lambda event: events.append(("disconnect", event.gamepad.id)),
        )

        manager.connect(pad, index=1)
        self.assertTrue(pad.connected)
        self.assertEqual(manager.getGamepads(), [None, pad])

        pad.update(axes=[-1, 1], buttons=[0.5])
        self.assertEqual(pad.axes, [-1.0, 1.0])
        self.assertEqual(pad.buttons[0].value, 0.5)
        self.assertTrue(pad.vibrationActuator.pulse(1, 25).data)

        manager.disconnect(1)
        self.assertFalse(pad.connected)
        self.assertEqual(
            events, [("connect", "Test Pad"), ("disconnect", "Test Pad")]
        )

        win = BrowserWindow()
        window_events = []
        win.addEventListener(
            "gamepadconnected",
            lambda event: window_events.append(event.gamepad.id),
        )
        win.navigator.connectGamepad(Gamepad("Window Pad"))
        self.assertEqual(window_events, ["Window Pad"])
        self.assertEqual(win.navigator.getGamepads()[0].id, "Window Pad")

    def test_geolocation(self):
        geo = Geolocation(GeolocationCoordinates(latitude=51.5, longitude=-0.12))
        positions = []
        geo.getCurrentPosition(lambda position: positions.append(position))
        self.assertIsInstance(positions[0], GeolocationPosition)
        self.assertEqual(positions[0].coords.latitude, 51.5)

        watch_id = geo.watchPosition(lambda position: positions.append(position))
        updated = geo.setPosition({"latitude": 40.7, "longitude": -74.0})
        self.assertEqual(updated.coords.longitude, -74.0)
        self.assertEqual(positions[-1].coords.latitude, 40.7)

        geo.clearWatch(watch_id)
        geo.setPosition({"latitude": 1, "longitude": 2})
        self.assertEqual(positions[-1].coords.latitude, 40.7)

        win = BrowserWindow()
        self.assertIsInstance(win.navigator.geolocation, Geolocation)

        with self.assertRaises(TypeError):
            geo.getCurrentPosition(None)

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
        surface = canvas(width=64, height=64)
        gl = surface.getContext("webgl", {"alpha": False})

        self.assertIsInstance(gl, WebGLRenderingContext)
        self.assertEqual(gl.getContextAttributes()["alpha"], False)
        self.assertEqual(gl.getParameter(gl.VIEWPORT), (0, 0, 64, 64))

        gl.viewport(0, 0, 32, 32)
        gl.clearColor(0.1, 0.2, 0.3, 1)
        gl.clear(gl.COLOR_BUFFER_BIT)

        buffer = gl.createBuffer()
        gl.bindBuffer(gl.ARRAY_BUFFER, buffer)
        gl.bufferData(gl.ARRAY_BUFFER, [0, 1, 2, 3], gl.STATIC_DRAW)
        self.assertEqual(buffer.data, b"\x00\x01\x02\x03")

        vertex = gl.createShader(gl.VERTEX_SHADER)
        fragment = gl.createShader(gl.FRAGMENT_SHADER)
        gl.shaderSource(vertex, "void main() {}")
        gl.shaderSource(fragment, "void main() {}")
        gl.compileShader(vertex)
        gl.compileShader(fragment)
        self.assertTrue(gl.getShaderParameter(vertex, gl.COMPILE_STATUS))

        program = gl.createProgram()
        gl.attachShader(program, vertex)
        gl.attachShader(program, fragment)
        gl.linkProgram(program)
        self.assertTrue(gl.getProgramParameter(program, gl.LINK_STATUS))
        gl.useProgram(program)
        self.assertEqual(gl.commands[-1]["name"], "useProgram")
        self.assertIsNone(surface.getContext("2d"))

        gl2 = canvas().getContext("webgl2")
        self.assertIsInstance(gl2, WebGL2RenderingContext)
        self.assertIn("WebGL 2.0", gl2.getParameter(gl2.VERSION))

    def test_intersectobserver(self):
        root = div()
        root.style.left = "0px"
        root.style.top = "0px"
        root.style.width = "100px"
        root.style.height = "100px"

        target = div()
        target.style.left = "20px"
        target.style.top = "20px"
        target.style.width = "20px"
        target.style.height = "20px"
        root.appendChild(target)

        entries = []
        observer = IntersectionObserver(
            lambda records, obs: entries.extend(records), {"root": root}
        )
        observer.observe(target)

        self.assertTrue(entries[-1].isIntersecting)
        self.assertEqual(entries[-1].intersectionRatio, 1.0)
        self.assertEqual(observer.takeRecords(), [])

        target.style.left = "200px"
        target.getBoundingClientRect()
        self.assertFalse(entries[-1].isIntersecting)
        self.assertEqual(entries[-1].intersectionRatio, 0.0)

        observer.unobserve(target)
        target.style.left = "10px"
        target.getBoundingClientRect()
        self.assertFalse(entries[-1].isIntersecting)

        with self.assertRaises(TypeError):
            IntersectionObserver(None)

    def test_mediacapabilities(self):
        capabilities = MediaCapabilities()
        result = capabilities.decodingInfo(
            {"video": {"contentType": 'video/webm; codecs="vp9"'}}
        )
        self.assertEqual(
            result,
            {
                "supported": True,
                "smooth": True,
                "powerEfficient": True,
                "keySystemAccess": None,
            },
        )
        self.assertFalse(capabilities.encodingInfo({})["supported"])
        self.assertIsInstance(
            BrowserWindow().navigator.mediaCapabilities,
            MediaCapabilities,
        )

    def test_mediasession(self):
        session = MediaSession()
        seen = []
        session.metadata = {"title": "Track"}
        session.playbackState = "playing"
        session.setActionHandler("play", lambda details: seen.append(details) or "ok")
        session.setPositionState({"duration": 120, "position": 10})

        self.assertEqual(session.dispatchAction("play", {"fastSeek": False}), "ok")
        self.assertEqual(seen, [{"fastSeek": False}])
        self.assertEqual(session.positionState["duration"], 120)
        self.assertEqual(session.metadata["title"], "Track")
        self.assertEqual(session.playbackState, "playing")

        session.setActionHandler("play", None)
        self.assertIsNone(session.dispatchAction("play"))
        with self.assertRaises(TypeError):
            session.setActionHandler("pause", "not-callable")
        self.assertIsInstance(BrowserWindow().navigator.mediaSession, MediaSession)

    def test_mediastream(self):
        devices = MediaDevices()
        listed = devices.enumerateDevices()
        self.assertEqual(listed.state, "fulfilled")
        self.assertTrue(any(device.kind == "audioinput" for device in listed.data))
        self.assertEqual(
            MediaDeviceInfo("id", "videoinput", "Camera").toJSON()["label"],
            "Camera",
        )
        self.assertEqual(
            InputDeviceInfo(capabilities={"width": 1280}).getCapabilities()["width"],
            1280,
        )

        changes = []
        devices.addEventListener(
            "devicechange", lambda event: changes.append(event.type)
        )
        custom = devices.addDevice(
            MediaDeviceInfo("virtual-cam", "videoinput", "Virtual camera")
        )
        self.assertIs(devices.removeDevice(custom.deviceId), custom)
        self.assertEqual(changes, ["devicechange", "devicechange"])

        stream = devices.getUserMedia(
            {"audio": {"echoCancellation": True}, "video": {"width": 1280}}
        ).data
        self.assertIsInstance(stream, MediaStream)
        self.assertTrue(stream.active)
        self.assertEqual(len(stream.getAudioTracks()), 1)
        self.assertEqual(len(stream.getVideoTracks()), 1)

        video_track = stream.getVideoTracks()[0]
        self.assertIsInstance(video_track, MediaStreamTrack)
        self.assertEqual(video_track.getConstraints(), {"width": 1280})
        self.assertIs(stream.getTrackById(video_track.id), video_track)

        track_events = []
        stream.addEventListener(
            "removetrack", lambda event: track_events.append(event.track)
        )
        stream.removeTrack(video_track)
        self.assertEqual(track_events, [video_track])

        clone = stream.clone()
        self.assertIsInstance(clone, MediaStream)
        self.assertNotEqual(clone.id, stream.id)
        self.assertNotEqual(clone.getTracks()[0].id, stream.getTracks()[0].id)

        ended = []
        audio_track = stream.getAudioTracks()[0]
        audio_track.addEventListener("ended", lambda event: ended.append(event.type))
        audio_track.stop()
        self.assertEqual(audio_track.readyState, "ended")
        self.assertEqual(ended, ["ended"])
        self.assertFalse(stream.active)

        display = devices.getDisplayMedia().data
        self.assertEqual(
            display.getVideoTracks()[0].getSettings()["displaySurface"],
            "monitor",
        )
        self.assertEqual(
            devices.getUserMedia({"audio": False, "video": False}).state,
            "rejected",
        )
        self.assertIsInstance(BrowserWindow().navigator.mediaDevices, MediaDevices)

    def test_messaging(self):
        channel = MessageChannel()
        queued = []

        channel.port1.addEventListener("message", lambda event: queued.append(event.data))
        original = {"count": 1, "items": ["a"]}
        channel.port2.postMessage(original)
        original["items"].append("mutated")

        self.assertEqual(queued, [])
        channel.port1.start()
        self.assertEqual(queued, [{"count": 1, "items": ["a"]}])

        replies = []
        channel.port2.onmessage = lambda event: replies.append(
            (event.data, event.source, event.ports)
        )
        extra_port = MessagePort()
        channel.port1.postMessage("hello", [extra_port])
        self.assertEqual(replies, [("hello", channel.port1, [extra_port])])

        channel.port2.close()
        channel.port1.postMessage("ignored")
        self.assertEqual(replies, [("hello", channel.port1, [extra_port])])

        class Uncloneable:
            def __deepcopy__(self, memo):
                raise TypeError("no clone")

        errors = []
        error_channel = MessageChannel()
        error_channel.port2.onmessageerror = lambda event: errors.append(
            (event.data, event.source, type(event.error))
        )
        bad_message = Uncloneable()
        error_channel.port1.postMessage(bad_message)
        self.assertEqual(errors, [(bad_message, error_channel.port1, TypeError)])

    def test_broadcast_channel(self):
        first = BroadcastChannel("domonic-test")
        second = BroadcastChannel("domonic-test")
        third = BroadcastChannel("domonic-test")
        other = BroadcastChannel("other")
        seen = []

        first.onmessage = lambda event: seen.append(("first", event.data))
        second.addEventListener(
            "message", lambda event: seen.append(("second", event.data))
        )
        third.onmessage = lambda event: seen.append(("third", event.data))
        other.onmessage = lambda event: seen.append(("other", event.data))

        payload = {"ready": True}
        first.postMessage(payload)
        payload["ready"] = False
        self.assertCountEqual(
            seen,
            [("second", {"ready": True}), ("third", {"ready": True})],
        )

        third.close()
        second.postMessage("ping")
        self.assertEqual(len(seen), 3)
        self.assertIn(("first", "ping"), seen)

        errors = []
        second.onmessageerror = lambda event: errors.append(type(event.error))

        class Uncloneable:
            def __deepcopy__(self, memo):
                raise TypeError("no broadcast clone")

        first.postMessage(Uncloneable())
        self.assertEqual(errors, [TypeError])

        first.close()
        second.close()
        other.close()

    def test_webworker_callable(self):
        def worker_main(scope):
            self.assertIsInstance(scope, DedicatedWorkerGlobalScope)
            self.assertIs(get_current_worker_scope(), scope)
            self.assertIsInstance(scope.scheduler, Scheduler)

            def handle(event):
                data = event.data
                data["worker"] = scope.name
                scope.postMessage(data, {"transfer": event.ports})

            scope.onmessage = handle

        worker = WebWorker(worker_main, {"name": "callable-worker"})
        received = []
        ready = threading.Event()

        worker.onmessage = lambda event: (
            received.append((event.data, event.source, event.ports)),
            ready.set(),
        )

        transfer_port = MessagePort()
        payload = {"items": ["original"]}
        worker.postMessage(payload, [transfer_port])
        payload["items"].append("mutated")

        self.assertTrue(ready.wait(2))
        self.assertEqual(
            received,
            [
                (
                    {"items": ["original"], "worker": "callable-worker"},
                    worker.scope,
                    [transfer_port],
                )
            ],
        )

        worker.terminate()
        self.assertTrue(worker.join(2))

    def test_webworker_script(self):
        source = """
def handle(event):
    if event.data == "close":
        close()
    else:
        postMessage({"reply": event.data, "name": self.name})

onmessage = handle
"""
        with tempfile.NamedTemporaryFile(
            "w", suffix=".py", delete=False
        ) as worker_file:
            worker_file.write(source)
            worker_path = worker_file.name

        worker = None
        try:
            worker = WebWorker(worker_path, {"name": "script-worker"})
            received = []
            ready = threading.Event()
            worker.addEventListener(
                "message",
                lambda event: (
                    received.append((event.data, event.source)),
                    ready.set(),
                ),
            )

            worker.postMessage("hello")

            self.assertTrue(ready.wait(2))
            self.assertEqual(
                received,
                [({"reply": "hello", "name": "script-worker"}, worker.scope)],
            )

            worker.postMessage("close")
            self.assertTrue(worker.join(2))
            self.assertTrue(worker.closed)
        finally:
            if worker is not None:
                worker.terminate()
                worker.join(2)
            os.unlink(worker_path)

    def test_webworker_errors(self):
        class Uncloneable:
            def __deepcopy__(self, memo):
                raise TypeError("no worker clone")

        def worker_main(scope):
            scope.onmessageerror = lambda event: scope.postMessage(
                {
                    "messageerror": type(event.error).__name__,
                    "source": event.source is worker,
                }
            )

            def handle(event):
                if event.data == "explode":
                    raise ValueError("boom")
                if event.data == "bad-reply":
                    scope.postMessage(Uncloneable())

            scope.onmessage = handle

        worker = WebWorker(worker_main)
        messages = []
        errors = []
        message_errors = []
        message_ready = threading.Event()
        error_ready = threading.Event()
        message_error_ready = threading.Event()

        worker.onmessage = lambda event: (
            messages.append(event.data),
            message_ready.set(),
        )
        worker.onerror = lambda event: (
            errors.append((event.message, type(event.error))),
            error_ready.set(),
        )
        worker.onmessageerror = lambda event: (
            message_errors.append((event.data, type(event.error), event.source)),
            message_error_ready.set(),
        )

        worker.postMessage(Uncloneable())
        self.assertTrue(message_ready.wait(2))
        self.assertEqual(messages, [{"messageerror": "TypeError", "source": True}])

        worker.postMessage("explode")
        self.assertTrue(error_ready.wait(2))
        self.assertEqual(errors, [("boom", ValueError)])

        worker.postMessage("bad-reply")
        self.assertTrue(message_error_ready.wait(2))
        self.assertEqual(len(message_errors), 1)
        self.assertIsInstance(message_errors[0][0], Uncloneable)
        self.assertEqual(message_errors[0][1], TypeError)
        self.assertIs(message_errors[0][2], worker.scope)

        worker.terminate()
        self.assertTrue(worker.join(2))
        self.assertTrue(worker.terminated)

    def test_serviceworker(self):
        container = ServiceWorkerContainer("https://example.com/app/")
        changes = []
        container.addEventListener(
            "controllerchange", lambda event: changes.append(event.type)
        )

        registered = container.register("sw.py", {"scope": "/app/"})
        self.assertEqual(registered.state, "fulfilled")
        registration = registered.data
        self.assertIsInstance(registration, ServiceWorkerRegistration)
        self.assertIsInstance(registration.active, ServiceWorker)
        self.assertEqual(registration.scope, "/app/")
        self.assertEqual(
            registration.active.scriptURL,
            "https://example.com/app/sw.py",
        )
        self.assertEqual(changes, ["controllerchange"])
        self.assertIs(container.controller, registration.active)

        messages = []
        registration.active.addEventListener(
            "message", lambda event: messages.append(event.data)
        )
        container.postMessage({"hello": "worker"})
        self.assertEqual(messages, [{"hello": "worker"}])

        updates = []
        registration.addEventListener(
            "updatefound", lambda event: updates.append(event.type)
        )
        self.assertIs(registration.update().data, registration)
        self.assertEqual(updates, ["updatefound"])
        self.assertIsNone(registration.installing)
        self.assertEqual(registration.waiting.state, ServiceWorker.INSTALLED)

        self.assertIs(container.ready.data, registration)
        self.assertIs(container.getRegistration("/app/page").data, registration)
        self.assertEqual(container.getRegistrations().data, [registration])

        self.assertTrue(registration.unregister().data)
        self.assertIsNone(container.controller)
        self.assertEqual(container.getRegistrations().data, [])
        self.assertIsInstance(
            BrowserWindow().navigator.serviceWorker,
            ServiceWorkerContainer,
        )

    def test_networkinfo(self):
        info = NetworkInformation({"effectiveType": "3g", "downlink": 1.5})
        changes = []
        info.addEventListener("change", lambda event: changes.append(event.target))
        returned = info.update(effectiveType="4g", rtt=50)

        self.assertIs(returned, info)
        self.assertEqual(changes, [info])
        self.assertEqual(info.effectiveType, "4g")
        self.assertEqual(info.rtt, 50)
        self.assertIn("effectiveType: 4g", str(info))
        self.assertIsInstance(BrowserWindow().navigator.connection, NetworkInformation)

        with self.assertRaises(AttributeError):
            info.update(nope=True)

    def test_notifications(self):
        previous_permission = Notification.permission
        try:
            Notification.setPermission("default")
            callback_permissions = []
            granted = Notification.requestPermission(callback_permissions.append)

            self.assertEqual(granted.data, "granted")
            self.assertEqual(callback_permissions, ["granted"])

            notice = Notification(
                "Build finished",
                {
                    "body": "Tests passed",
                    "tag": "ci",
                    "data": {"sha": "abc"},
                    "actions": [
                        {"action": "open"},
                        {"action": "dismiss"},
                        {"action": "extra"},
                    ],
                },
            )
            events = []
            notice.addEventListener("show", lambda event: events.append(event.type))
            notice.addEventListener("click", lambda event: events.append(event.type))
            notice.addEventListener("close", lambda event: events.append(event.type))

            self.assertTrue(notice.show())
            notice.click()
            notice.close()

            self.assertEqual(events, ["show", "click", "close"])
            self.assertTrue(notice.closed)
            self.assertEqual(len(notice.actions), Notification.maxActions)
            self.assertEqual(notice.toJSON()["data"], {"sha": "abc"})
            self.assertIs(BrowserWindow().Notification, Notification)

            with self.assertRaises(ValueError):
                Notification.setPermission("maybe")

            Notification.setPermission("denied")
            denied = Notification("Blocked")
            errors = []
            denied.addEventListener("error", lambda event: errors.append(event.type))
            self.assertFalse(denied.show())
            self.assertEqual(errors, ["error"])
        finally:
            Notification.setPermission(previous_permission)

    def test_performance(self):
        performance.clearMarks()
        performance.clearMeasures()

        entries = []
        observer = PerformanceObserver(lambda records, obs: entries.extend(records))
        observer.observe({"entryTypes": ["mark", "measure"]})

        mark = performance.mark("webapi-start")
        measure = performance.measure("webapi-total", "webapi-start")

        self.assertEqual(mark.toJSON()["entryType"], "mark")
        self.assertEqual(measure.entryType, "measure")
        self.assertEqual(
            [entry.name for entry in entries], ["webapi-start", "webapi-total"]
        )
        self.assertIn("mark", PerformanceObserver.supportedEntryTypes)
        self.assertIs(BrowserWindow().performance, performance)

        buffered = []
        buffered_observer = PerformanceObserver(
            lambda records, obs: buffered.extend(records)
        )
        buffered_observer.observe({"entryTypes": ["mark"], "buffered": True})
        self.assertIn("webapi-start", [entry.name for entry in buffered])

        with self.assertRaises(TypeError):
            PerformanceObserver(None)
        with self.assertRaises(TypeError):
            PerformanceObserver(lambda records, obs: None).observe({})

    def test_permissions(self):
        permissions = Permissions()
        status = permissions.query({"name": "geolocation"})
        self.assertIsInstance(status, PermissionStatus)
        self.assertEqual(status.state, "prompt")

        changes = []
        status.addEventListener(
            "change", lambda event: changes.append(event.target.state)
        )
        status.state = "granted"
        self.assertEqual(changes, ["granted"])

        granted = permissions.request({"name": "clipboard-read"})
        self.assertEqual(str(granted), "granted")
        self.assertEqual(permissions.query("clipboard-read").state, "granted")

        revoked = permissions.revoke({"name": "clipboard-read"})
        self.assertEqual(revoked.state, "prompt")

        requested = permissions.requestAll(
            [{"name": "camera"}, {"name": "microphone"}]
        )
        self.assertEqual(requested["camera"].state, "granted")
        self.assertEqual(permissions.revokeAll()["camera"].state, "prompt")

        win = BrowserWindow()
        self.assertIsInstance(win.navigator.permissions, Permissions)

    def test_serversentevents(self):
        from domonic.ext.sseclient import Event as ServerSentEvent

        parsed = ServerSentEvent.parse(
            ": keepalive\nid:\nevent: update\nretry: 0\ndata: one\ndata: two"
        )
        self.assertEqual(parsed.id, "")
        self.assertEqual(parsed.event, "update")
        self.assertEqual(parsed.retry, 0)
        self.assertEqual(parsed.data, "one\ntwo")

        invalid_retry = ServerSentEvent.parse("retry: nope\ndata: ok")
        self.assertIsNone(invalid_retry.retry)
        self.assertEqual(invalid_retry.data, "ok")

        self.assertEqual(
            ServerSentEvent("payload", event="tick", id="42", retry=10).dump(),
            "id: 42\nevent: tick\nretry: 10\ndata: payload\n\n",
        )
        with self.assertRaises(TypeError):
            ServerSentEvent(b"not text")

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
        from domonic.webapi.xpath import (
            XPathEvaluator,
            XPathException,
            XPathNSResolver,
            XPathResult,
        )

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

        page = html(
            body(
                h1(
                    "We are",
                    span("Eventual Technology", _class="font-weight-bold d-block"),
                    _class="text-uppercase hero-text text-black",
                ),
                div(
                    p(
                        "Welcome to the information age",
                        _class="headings-font-family text-uppercase lead",
                    )
                ),
                div(
                    ul(
                        li(a("Home", _href="/")),
                        li(
                            a(
                                "Twitter",
                                _href="https://twitter.com/eventualtech",
                                _class="social-link social-link-instagram",
                            )
                        ),
                    ),
                    _id="contact",
                ),
            )
        )

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
        self.assertEqual([node.tagName for node in result.nodes], ["li", "li"])

        expression = evaluator.createExpression("//ul/li/a")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual([node.textContent for node in result.nodes], ["Home", "Twitter"])

        expression = evaluator.createExpression("//div/*")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual([node.tagName for node in result.nodes], ["p", "ul"])

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
        self.assertEqual(result.nodes[0].getAttribute("id"), "contact")

        expression = evaluator.createExpression(
            '//*[@_class="social-link social-link-instagram"]'
        )  # NOTE - requires all classes to match
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual(result.nodes[0].textContent, "Twitter")

        # expression = evaluator.createExpression("//input[@type='submit']")
        # result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        # print(str(result.nodes))

        expression = evaluator.createExpression("//a[contains(@_href, 'twitter')]")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual(result.nodes[0].textContent, "Twitter")

        expression = evaluator.createExpression("//a[contains(@href, 'twitter')]")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual(result.nodes[0].textContent, "Twitter")

        expression = evaluator.createExpression("//a[last()]")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual(result.nodes[-1].textContent, "Twitter")

        expression = evaluator.createExpression("//span/text()")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual(str(result.nodes[0]), "Eventual Technology")

        somepage = html(
            head(), body(h1("some title"), p("some text"), div("some more text"))
        )

        expression = evaluator.createExpression("//div/text()")
        result = expression.evaluate(somepage, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual(str(result.nodes[0]), "some more text")

        expression = evaluator.createExpression("//a")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual(result.snapshotItem(0).textContent, "Home")
        self.assertEqual(result.snapshotItem(1).textContent, "Twitter")
        self.assertIsNone(result.snapshotItem(-1))
        self.assertIsNone(result.snapshotItem(99))

        result = expression.evaluate(page, XPathResult.ORDERED_NODE_ITERATOR_TYPE)
        self.assertEqual(result.iterateNext().textContent, "Home")
        self.assertEqual(result.iterateNext().textContent, "Twitter")
        self.assertIsNone(result.iterateNext())

        result = evaluator.evaluate(
            "//a", page, None, XPathResult.FIRST_ORDERED_NODE_TYPE
        )
        self.assertEqual(result.singleNodeValue.textContent, "Home")

        reusable = XPathResult([], XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        result = expression.evaluate(
            page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE, reusable
        )
        self.assertIs(result, reusable)
        self.assertEqual(result.snapshotLength, 2)

        self.assertEqual(XPathResult("hello", XPathResult.ANY_TYPE).stringValue, "hello")
        self.assertFalse(XPathResult(False, XPathResult.ANY_TYPE).booleanValue)
        self.assertEqual(XPathResult(3, XPathResult.ANY_TYPE).numberValue, 3.0)
        with self.assertRaises(XPathException):
            XPathResult([], 999)
        with self.assertRaises(XPathException) as raised:
            evaluator.createExpression("")
        self.assertEqual(raised.exception.code, XPathException.INVALID_EXPRESSION_ERR)

        resolver_node = div(
            "namespaced",
            **{"_xmlns:site": "https://example.com/site"},
        )
        resolver = XPathNSResolver(resolver_node)
        self.assertEqual(
            resolver.lookupNamespaceURI("site"), "https://example.com/site"
        )
        self.assertEqual(resolver.lookupNamespaceURI("svg"), "http://www.w3.org/2000/svg")
        self.assertEqual(
            XPathEvaluator({"custom": "urn:custom"})
            .createNSResolver({"other": "urn:other"})
            .lookupNamespaceURI("other"),
            "urn:other",
        )

        fallback = evaluator.createExpression("//a[1]")
        fallback.selector = None
        result = fallback.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual([node.textContent for node in result.nodes], ["Home"])

        fallback = evaluator.createExpression("//a[position()=2]")
        fallback.selector = None
        result = fallback.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual([node.textContent for node in result.nodes], ["Twitter"])

        fallback = evaluator.createExpression("//a[starts-with(@href, '/')]")
        fallback.selector = None
        result = fallback.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual([node.textContent for node in result.nodes], ["Home"])

        fallback = evaluator.createExpression("//a[ends-with(@href, 'eventualtech')]")
        fallback.selector = None
        result = fallback.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        self.assertEqual([node.textContent for node in result.nodes], ["Twitter"])

        """
        XPath reference notes for future coverage ideas.

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
