"""
    test_dQuery
    ~~~~~~~~~~~~~~~
    unit tests for domonic.dQuery

"""

import json
import unittest
from contextlib import contextmanager
from unittest.mock import patch
from urllib.parse import parse_qs, urlparse

from domonic.dom import *
from domonic.dQuery import *
from domonic.html import *


_TEST_AJAX_EVENTS = (
    "ajaxStart",
    "ajaxSend",
    "ajaxSuccess",
    "ajaxError",
    "ajaxComplete",
    "ajaxStop",
)


class _DQueryResponse:
    def __init__(self, status_code=200, text="", reason="OK", payload=None):
        self.status_code = status_code
        self.reason = reason
        self.text = json.dumps(payload) if payload is not None else text
        self.content = self.text.encode("utf-8")

    def json(self):
        return json.loads(self.text)


class _DQuerySession:
    def __init__(self):
        self.calls = []

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        return None

    def request(self, method, url, **kwargs):
        method = method.upper()
        self.calls.append((method, url, kwargs))
        parsed = urlparse(url)
        if parsed.path == "/html":
            return _DQueryResponse(text="<strong>loaded</strong>")
        if parsed.path == "/fail":
            return _DQueryResponse(
                status_code=500, text="bad news", reason="Internal Server Error"
            )
        if method == "POST":
            raw_body = kwargs.get("data") or ""
            if isinstance(raw_body, bytes):
                raw_body = raw_body.decode("utf-8")
            form = {
                key: values[-1] if len(values) == 1 else values
                for key, values in parse_qs(str(raw_body)).items()
            }
            return _DQueryResponse(
                payload={"method": method, "path": parsed.path, "form": form}
            )
        query = dict(kwargs.get("params") or {})
        query.update(
            {
                key: values[-1] if len(values) == 1 else values
                for key, values in parse_qs(parsed.query).items()
            }
        )
        return _DQueryResponse(payload={"method": method, "query": query})


class _DQueryRequestsMock:
    def __enter__(self):
        self.session = _DQuerySession()
        self.patch = patch("requests.Session", return_value=self.session)
        self.patch.start()
        return self

    def __exit__(self, exc_type, exc, tb):
        self.patch.stop()

    def url(self, path):
        return f"https://example.test{path}"


class TestCase(unittest.TestCase):
    @contextmanager
    def _ajax_handlers_isolated(self):
        handlers = {
            event: list(callbacks)
            for event, callbacks in getattr(º, "_ajax_event_handlers", {}).items()
        }
        prefilters = list(getattr(º, "_ajax_prefilters", []))
        settings = getattr(º, "ajaxSettings", {}).copy()
        active = getattr(º, "_ajax_active", 0)
        º._ajax_event_handlers = {event: [] for event in _TEST_AJAX_EVENTS}
        º._ajax_prefilters = []
        º._ajax_active = 0
        try:
            yield
        finally:
            º._ajax_event_handlers = handlers
            º._ajax_prefilters = prefilters
            º.ajaxSettings = settings
            º._ajax_active = active

    def _assert_simple_event(self, method_name, event_name=None):
        event_name = event_name or method_name
        page = html(body(div("x", _id="target")))
        º(page)
        calls = []
        target = º("#target")
        getattr(target, method_name)(lambda event: calls.append(event.type))
        getattr(target, method_name)()
        self.assertEqual(calls, [event_name])

    # domonic.dQuery.º
    def test_hello(self):
        d = html(head(body(li(_class="things"), div(_id="test"))))
        º(d)
        a = º('<div class="test2"></div>')
        b = º("#test").append(a)
        self.assertIn('class="test2"', str(a))
        self.assertIn('id="test"', str(b))
        self.assertIn('class="things"', str(d))

    def test_add(self):
        test = º('<p></p>').add('<h1></h1>').add(div())
        assert str(test) == "<p></p><h1></h1><div></div>"

    def test_addBack(self):
        things = º(
            '<li class="keep">a</li><li>b</li><li class="keep">c</li>'
        )
        selected = things.eq(1)

        self.assertEqual(
            str(selected.addBack(".keep")),
            '<li class="keep">a</li><li class="keep">c</li>',
        )

    def test_addClass(self):
        a = º('<div id="test2"></div><div id="test3"></div>')
        assert str(a) == '<div id="test2"></div><div id="test3"></div>'
        a.addClass("one")
        assert str(a) == '<div id="test2" class="one"></div><div id="test3" class="one"></div>'
        # print("1:",a)
        # print("2:",str(a))
        # print(str(a))
        a.addClass("one").addClass("two").addClass("three")
        assert (
            str(a) == '<div id="test2" class="one two three"></div><div id="test3" class="one two three"></div>'
        )
        # for el in a.elements:
        # print(el.getAttribute("class"))

    def test_after(self):
        # TODO - sort the parser... positional error on this as not multiline
        # tags = º('<div id="test1"><h1>asd</h1></div>')
        # print(tags)
        app = html(head(), body(div(span(), _id="test")))
        º(app)  # TODO _str is none?
        # print( 'wtf:??:', º('#test1') ) # TODO - better errors when passing wrong id name
        º("#test").after(p("hi"))
        self.assertIn("<p>hi</p>", str(app))
        # pass

    def test_ajaxComplete(self):
        with self._ajax_handlers_isolated():
            with _DQueryRequestsMock() as server:
                events = []
                target = º("<div></div>")
                target.ajaxStart(lambda event: events.append(event.type))
                target.ajaxSend(
                    lambda event, xhr, settings: events.append(settings["type"])
                )
                target.ajaxSuccess(
                    lambda event, xhr, settings, data: events.append(data["query"]["q"])
                )
                target.ajaxComplete(
                    lambda event, xhr, settings: events.append(event.type)
                )
                target.ajaxStop(lambda event: events.append(event.type))

                success = []
                complete = []
                response = º.ajax(
                    {
                        "url": server.url("/echo"),
                        "data": {"q": "domonic"},
                        "dataType": "json",
                        "success": lambda data, status, xhr: success.append(
                            (data["method"], status, xhr.status_code)
                        ),
                        "complete": lambda xhr, status: complete.append(status),
                    }
                )

                self.assertEqual(response.status_code, 200)
                self.assertEqual(response.data["query"], {"q": "domonic"})
                self.assertEqual(success, [("GET", "success", 200)])
                self.assertEqual(complete, ["success"])
                self.assertEqual(
                    events,
                    ["ajaxStart", "GET", "domonic", "ajaxComplete", "ajaxStop"],
                )

    def test_ajaxError(self):
        with self._ajax_handlers_isolated():
            with _DQueryRequestsMock() as server:
                errors = []
                events = []
                º("<div></div>").ajaxError(
                    lambda event, xhr, settings, thrown: events.append(
                        (event.type, xhr.status_code, thrown)
                    )
                )

                response = º.ajax(
                    {
                        "url": server.url("/fail"),
                        "error": lambda xhr, status, thrown: errors.append(
                            (xhr.status_code, status, thrown)
                        ),
                    }
                )

                self.assertEqual(response.status_code, 500)
                self.assertEqual(errors, [(500, "error", "Internal Server Error")])
                self.assertEqual(
                    events, [("ajaxError", 500, "Internal Server Error")]
                )

    def test_ajaxSend(self):
        with self._ajax_handlers_isolated():
            target = º("<div></div>")
            handler = lambda event: event
            self.assertIs(target.ajaxSend(handler), target)
            self.assertEqual(º._ajax_event_handlers["ajaxSend"], [handler])

    def test_ajaxStart(self):
        with self._ajax_handlers_isolated():
            target = º("<div></div>")
            handler = lambda event: event
            self.assertIs(target.ajaxStart(handler), target)
            class_handler = lambda event: event
            self.assertIs(º.ajaxStart(class_handler), class_handler)
            self.assertEqual(
                º._ajax_event_handlers["ajaxStart"], [handler, class_handler]
            )

    def test_ajaxStop(self):
        with self._ajax_handlers_isolated():
            target = º("<div></div>")
            handler = lambda event: event
            self.assertIs(target.ajaxStop(handler), target)
            self.assertEqual(º._ajax_event_handlers["ajaxStop"], [handler])

    def test_ajaxSuccess(self):
        with self._ajax_handlers_isolated():
            target = º("<div></div>")
            handler = lambda event: event
            self.assertIs(target.ajaxSuccess(handler), target)
            self.assertEqual(º._ajax_event_handlers["ajaxSuccess"], [handler])

    def test_andSelf(self):
        things = º("<li>a</li><li>b</li>")
        selected = things.eq(1).andSelf()

        self.assertEqual(str(selected), "<li>b</li><li>a</li>")

    def test_animate(self):
        pass

    def test_append(self):
        d = º('<div></div>').append("some text")
        self.assertEqual(str(d), "<div>some text</div>")

    def test_appendTo(self):
        page = html(body(div(_id="target")))
        º(page)
        º("<span>last</span>").appendTo("#target")
        º("<b>first</b>").prependTo("#target")
        assert str(º("#target")) == '<div id="target"><b>first</b><span>last</span></div>'

    def test_attr(self):
        a = º('<div id="test2"></div>')
        a.addClass("one")
        assert str(a) == '<div id="test2" class="one"></div>'
        assert a.attr("id") == "test2"
        assert a.attr("class") == "one"
        a.attr("id", "somethingelse")
        assert str(a) == '<div id="somethingelse" class="one"></div>'
        a.attr({"role": "button", "data-count": "3"})
        assert a.attr("role") == "button"
        assert a.data("count") == 3
        a.attr("role", None)
        assert a.attr("role") is None
        # print(a.elements[0])

    def test_before(self):
        page = html(body(div("middle", _id="target")))
        º(page)
        º("#target").before("<p>before</p>").after("<p>after</p>")
        assert str(page) == '<html><body><p>before</p><div id="target">middle</div><p>after</p></body></html>'

    def test_bind(self):
        page = html(body(button("go", _id="btn")))
        º(page)
        called = []
        º("#btn").bind("click", lambda event: called.append(event.type)).click()
        self.assertEqual(called, ["click"])

    def test_blur(self):
        self._assert_simple_event("blur")

    def test_change(self):
        self._assert_simple_event("change")

    def test_children(self):
        page = html(body(div(span("one"), b("two"), _id="test")))
        º(page)
        children = º("#test").children()
        assert str(children) == "<span>one</span><b>two</b>"

    def test_clearQueue(self):
        el = º('<div id="test"></div>')
        el.delay(10)
        self.assertEqual(len(el.queue()), 1)
        self.assertIs(el.clearQueue(), el)
        self.assertEqual(el.queue(), [])

    def test_click(self):
        page = html(body(button("go", _id="btn")))
        º(page)
        called = []
        º("#btn").click(lambda e: called.append(e.type))
        º("#btn").click(None)
        assert called == ["click"]

    def test_clone(self):
        original = º('<div id="test"><span>x</span></div>')
        cloned = original.clone()

        cloned.find("span").text("y")
        self.assertEqual(str(original), '<div id="test"><span>x</span></div>')
        self.assertEqual(str(cloned), "<span>y</span>")

    def test_closest(self):
        page = html(body(div(span("x", _id="child"), _class="wrapper")))
        º(page)
        assert str(º("#child").closest(".wrapper")) == '<div class="wrapper"><span id="child">x</span></div>'

    def test_contents(self):
        page = html(body(div("hi", span("there"), _id="test")))
        º(page)
        assert len(º("#test").contents().toArray()) == 2

    def test_context(self):
        page = html(body(div(_id="target")))
        º(page)
        self.assertIs(º("#target").context, page)

    def test_contextmenu(self):
        self._assert_simple_event("contextmenu")

    def test_css(self):
        el = º('<div id="test"></div>')
        self.assertIs(el.css("width", "20px"), el)
        self.assertEqual(el.css("width"), "20px")
        el.css({"height": "10px", "display": "block"})
        self.assertEqual(el.css("height"), "10px")
        self.assertEqual(el.css("display"), "block")

    def test_data(self):
        el = º('<div id="test" data-enabled="true"></div>')
        el.data("answer", 42)
        assert el.data("answer") == 42
        assert el.data("enabled") is True
        el.data({"one": 1, "two": 2})
        assert el.data() == {"answer": 42, "enabled": True, "one": 1, "two": 2}

    def test_dblclick(self):
        self._assert_simple_event("dblclick")

    def test_delay(self):
        pass

    def test_delegate(self):
        pass

    def test_dequeue(self):
        el = º('<div id="test"></div>')
        calls = []
        el.delay(10)
        el.elements[0]._dquery_queue.append(lambda: calls.append("ran"))
        el.dequeue()
        el.dequeue()
        assert calls == ["ran"]

    def test_detach(self):
        page = html(body(div("keep", _id="keep"), div("drop", _id="drop")))
        º(page)
        detached = º("#drop").detach()

        self.assertEqual(
            str(page), '<html><body><div id="keep">keep</div></body></html>'
        )
        self.assertEqual(str(detached), '<div id="drop">drop</div>')
        self.assertIsNone(detached[0].parentNode)

    def test_die(self):
        pass

    def test_each(self):
        things = º("<li>a</li><li>b</li>")
        seen = []
        things.each(lambda index, el: seen.append((index, el.textContent)))
        assert seen == [(0, "a"), (1, "b")]

    def test_empty(self):
        page = html(body(div(span("x"), _id="target")))
        º(page)
        º("#target").empty()
        assert str(º("#target")) == '<div id="target"></div>'

    def test_end(self):
        things = º("<li>a</li><li>b</li><li>c</li>")
        self.assertEqual(str(things.eq(1).end()), "<li>a</li><li>b</li><li>c</li>")

    def test_eq(self):
        things = º("<li>a</li><li>b</li><li>c</li>")
        assert str(things.eq(1)) == "<li>b</li>"
        assert things.eq(99).length == 0
        assert things.eq(1).end().length == 3

    def test_error(self):
        self._assert_simple_event("error")

    def test_even(self):
        things = º("<li>a</li><li>b</li><li>c</li><li>d</li>")
        self.assertEqual(str(things.even()), "<li>a</li><li>c</li>")

    def test_fadeIn(self):
        pass

    def test_fadeOut(self):
        pass

    def test_fadeTo(self):
        pass

    def test_fadeToggle(self):
        pass

    def test_filter(self):
        things = º('<li class="keep"></li><li></li><li class="keep"></li>')
        assert str(things.filter(".keep")) == '<li class="keep"></li><li class="keep"></li>'

    def test_find(self):
        page = html(body(div(span("a"), p("b"), _id="test")))
        º(page)
        assert str(º("#test").find("span")) == "<span>a</span>"

    def test_finish(self):
        pass

    def test_first(self):
        things = º("<li>a</li><li>b</li>")
        self.assertEqual(str(things.first()), "<li>a</li>")

    def test_focus(self):
        page = html(body(input(_id="field")))
        º(page)
        called = []
        º("#field").on("focus", lambda e: called.append(e.type))
        º("#field").focus()
        assert called == ["focus"]

    def test_focusin(self):
        page = html(body(input(_id="field")))
        º(page)
        called = []
        º("#field").on("focusin", lambda e: called.append(e.type))
        º("#field").focusin()
        assert called == ["focusin"]

    def test_focusout(self):
        page = html(body(input(_id="field")))
        º(page)
        called = []
        º("#field").on("focusout", lambda e: called.append(e.type))
        º("#field").focusout()
        assert called == ["focusout"]

    def test_get(self):
        things = º("<li>a</li><li>b</li>")
        assert [el.textContent for el in things.get()] == ["a", "b"]
        assert things.get(-1).textContent == "b"
        assert things.get(99) is None

        with self._ajax_handlers_isolated():
            with _DQueryRequestsMock() as server:
                success = []
                data = º.get(
                    server.url("/echo"),
                    {"q": "hello"},
                    "json",
                    lambda payload: success.append(payload["query"]["q"]),
                )
                self.assertEqual(data["query"], {"q": "hello"})
                self.assertEqual(success, ["hello"])

                callback_shape = []
                data = º.get(
                    server.url("/echo"),
                    {"q": "callback"},
                    lambda payload, status: callback_shape.append(
                        (payload["query"]["q"], status)
                    ),
                    "json",
                )
                self.assertEqual(data["query"], {"q": "callback"})
                self.assertEqual(callback_shape, [("callback", "success")])

    def test_has(self):
        things = º('<div><span class="hit">x</span></div><div><b>y</b></div>')
        assert str(things.has(".hit")) == '<div><span class="hit">x</span></div>'

    def test_hasClass(self):
        a = º('<div id="test2"></div>')
        a.addClass("one").addClass("two").addClass("three")
        assert a.hasClass("one") == True
        assert a.hasClass("five") == False

    def test_height(self):
        el = º('<div id="test"></div>')
        el.elements.style.height = "25px"
        assert el.height() == 25

    def test_hide(self):
        el = º('<div id="test"></div>')
        self.assertIs(el.hide(), el)
        self.assertEqual(el.css("display"), "none")

    def test_hover(self):
        page = html(body(div("x", _id="test")))
        º(page)
        calls = []
        º("#test").hover(lambda e: calls.append("in"), lambda e: calls.append("out"))
        º("#test").mouseenter()
        º("#test").mouseleave()
        assert calls == ["in", "out"]

    def test_html(self):
        el = º("<div></div>")
        el.html("<span>x</span>")
        assert el.html() == "<span>x</span>"

    def test_index(self):
        page = html(body(div("zero"), div("one", _id="target"), div("two")))
        º(page)
        self.assertEqual(º("#target").index(), 1)
        self.assertEqual(º("<span></span>").index(), 0)

    def test_innerHeight(self):
        el = º('<div id="test"></div>')
        el.css({"height": "20px", "paddingTop": "2px", "paddingBottom": "3px"})
        self.assertEqual(el.innerHeight(), 25)

    def test_innerWidth(self):
        el = º('<div id="test"></div>')
        el.css({"width": "20px", "paddingLeft": "2px", "paddingRight": "3px"})
        self.assertEqual(el.innerWidth(), 25)

    def test_insertAfter(self):
        page = html(body(div("one", _id="one"), div("three", _id="three")))
        º(page)
        º("<span>two</span>").insertAfter("#one")
        self.assertEqual(
            str(page),
            '<html><body><div id="one">one</div><span>two</span><div id="three">three</div></body></html>',
        )

    def test_insertBefore(self):
        page = html(body(div("one", _id="one"), div("three", _id="three")))
        º(page)
        º("<span>two</span>").insertBefore("#three")
        self.assertEqual(
            str(page),
            '<html><body><div id="one">one</div><span>two</span><div id="three">three</div></body></html>',
        )

    # def test_is(self):
    # pass

    def test_is_and_not(self):
        things = º('<li class="keep"></li><li class="drop"></li>')
        assert things.is_(".keep") is True
        assert str(things.not_(".drop")) == '<li class="keep"></li>'

    def test_input_and_keyboard_events(self):
        page = html(body(input(_id="field")))
        º(page)
        calls = []
        field = º("#field")
        field.input(lambda e: calls.append((e.type, e.data)))
        field.change(lambda e: calls.append((e.type, None)))
        field.keydown(lambda e: calls.append((e.type, e.key)))
        field.val("quiet")
        assert calls == []
        field.trigger("input", {"data": "x"})
        field.change()
        field.trigger("keydown", {"key": "Enter"})
        assert calls == [("input", "x"), ("change", None), ("keydown", "Enter")]

    def test_keydown(self):
        self._assert_simple_event("keydown")

    def test_keypress(self):
        self._assert_simple_event("keypress")

    def test_keyup(self):
        self._assert_simple_event("keyup")

    def test_last(self):
        things = º('<li></li><li></li><li></li><li></li><li data-tag="me"></li>')
        assert str(things.last()) == '<li data-tag="me"></li>'

    def test_length(self):
        self.assertEqual(º("<li>a</li><li>b</li>").length, 2)

    def test_live(self):
        pass

    def test_load(self):
        with self._ajax_handlers_isolated():
            with _DQueryRequestsMock() as server:
                target = º("<div></div>")
                complete = []
                target.load(
                    server.url("/html"),
                    lambda response, status: complete.append((response, status)),
                )
                self.assertEqual(str(target), "<div><strong>loaded</strong></div>")
                self.assertEqual(complete, [("<strong>loaded</strong>", "success")])

    def test_map(self):
        things = º("<li>a</li><li>b</li>")
        mapped = things.map(lambda index, el: span(f"{index}:{el.textContent}"))

        self.assertEqual(str(mapped), "<span>0:a</span><span>1:b</span>")
        self.assertEqual(str(mapped.end()), "<li>a</li><li>b</li>")

    def test_mousedown(self):
        self._assert_simple_event("mousedown")

    def test_mouseenter(self):
        self._assert_simple_event("mouseenter")

    def test_mouseleave(self):
        self._assert_simple_event("mouseleave")

    def test_mousemove(self):
        self._assert_simple_event("mousemove")

    def test_mouseout(self):
        self._assert_simple_event("mouseout")

    def test_mouseover(self):
        self._assert_simple_event("mouseover")

    def test_mouseup(self):
        self._assert_simple_event("mouseup")

    def test_next(self):
        page = html(body(div("one", _id="first"), div("two", _id="second"), div("three", _id="third")))
        º(page)
        assert str(º("#first").next()) == '<div id="second">two</div>'
        assert str(º("#first").next("#third")) == ""

    def test_nextAll(self):
        page = html(body(div("one", _id="first"), div("two", _class="match"), div("three", _class="match")))
        º(page)
        assert str(º("#first").nextAll(".match")) == '<div class="match">two</div><div class="match">three</div>'

    def test_nextUntil(self):
        page = html(body(div("one", _id="first"), div("two"), div("stop", _id="stop"), div("three")))
        º(page)
        assert str(º("#first").nextUntil("#stop")) == "<div>two</div>"

    # def test_not(self):
    # pass

    def test_odd(self):
        things = º("<li>a</li><li>b</li><li>c</li><li>d</li>")
        self.assertEqual(str(things.odd()), "<li>b</li><li>d</li>")

    def off(self, event):
        pass

    def test_offset(self):
        el = º('<div id="test"></div>')
        el.offset({"top": "12px", "left": "5px"})
        assert el.offset() == {"top": 12, "left": 5}

    def test_offsetParent(self):
        page = html(body(div(span("x", _id="child"), _id="parent")))
        º(page)
        assert º("#child").offsetParent().getAttribute("id") == "parent"

    def on(self, event, callback):
        pass

    def test_on_multiple_handlers_namespaces_and_off_callback(self):
        page = html(body(button("go", _id="btn")))
        º(page)
        calls = []

        def first(e):
            calls.append("first")

        def second(e):
            calls.append("second")

        btn = º("#btn")
        btn.on("click.release keyup", first)
        btn.on("click", second)
        btn.trigger("click")
        assert calls == ["first", "second"]
        btn.off(".release")
        btn.trigger("click")
        assert calls == ["first", "second", "second"]
        btn.off("click", second)
        btn.trigger("click")
        assert calls == ["first", "second", "second"]

    def test_on_delegated_event_with_data(self):
        page = html(body(ul(li("x", _id="child", _class="item"), _id="list")))
        º(page)
        calls = []

        º("#list").on(
            "click",
            ".item",
            {"source": "delegated"},
            lambda e: calls.append(
                (
                    e.target.getAttribute("id"),
                    e.currentTarget.getAttribute("id"),
                    e.delegateTarget.getAttribute("id"),
                    e.data["source"],
                )
            ),
        )
        º("#child").trigger("click")
        assert calls == [("child", "child", "list", "delegated")]

    def test_one(self):
        page = html(body(button("go", _id="btn")))
        º(page)
        called = []
        º("#btn").one("click", lambda e: called.append(e.type))
        º("#btn").click()
        º("#btn").click()
        assert called == ["click"]

    def test_outerHeight(self):
        el = º('<div id="test"></div>')
        el.css(
            {
                "height": "20px",
                "paddingTop": "2px",
                "paddingBottom": "3px",
                "borderTopWidth": "4px",
                "borderBottomWidth": "5px",
            }
        )
        self.assertEqual(el.outerHeight(), 34)

    def test_outerWidth(self):
        el = º('<div id="test"></div>')
        el.css(
            {
                "width": "20px",
                "paddingLeft": "2px",
                "paddingRight": "3px",
                "borderLeftWidth": "4px",
                "borderRightWidth": "5px",
            }
        )
        self.assertEqual(el.outerWidth(), 34)

    def test_parent(self):
        page = html(body(div(span("x", _id="child"), _id="parent")))
        º(page)
        assert str(º("#child").parent()) == '<div id="parent"><span id="child">x</span></div>'

    def test_parents(self):
        page = html(body(div(section(span("x", _id="child"), _id="inner"), _id="outer")))
        º(page)
        assert str(º("#child").parents("#outer")) == '<div id="outer"><section id="inner"><span id="child">x</span></section></div>'

    def test_parentsUntil(self):
        page = html(body(div(section(span("x", _id="child"), _id="inner"), _id="outer")))
        º(page)
        assert str(º("#child").parentsUntil("#outer")) == '<section id="inner"><span id="child">x</span></section>'

    def test_position(self):
        el = º('<div id="test"></div>')
        el.offset({"top": "3px", "left": "7px"})
        assert el.position() == {"top": 3, "left": 7}

    def prepend(self, html):
        pass

    def test_prependTo(self):
        page = html(body(div(span("tail"), _id="target")))
        º(page)
        º("<b>head</b>").prependTo("#target")
        self.assertEqual(
            str(º("#target")), '<div id="target"><b>head</b><span>tail</span></div>'
        )

    def test_prev(self):
        page = html(body(div("one", _id="first"), div("two", _id="second"), div("three", _id="third")))
        º(page)
        assert str(º("#third").prev()) == '<div id="second">two</div>'

    def test_prevAll(self):
        page = html(body(div("one", _class="match"), div("two"), div("three", _id="third"), div("four", _class="match")))
        º(page)
        assert str(º("#third").prevAll(".match")) == '<div class="match">one</div>'

    def test_prevUntil(self):
        page = html(body(div("one", _id="stop"), div("two"), div("three", _id="third")))
        º(page)
        assert str(º("#third").prevUntil("#stop")) == "<div>two</div>"

    def test_promise(self):
        el = º('<div id="test"></div>')
        assert el.promise()["state"] == "resolved"

    def test_prop(self):
        el = º('<input id="field" value="old"></input>')
        assert el.prop("value") == "old"
        el.prop("value", "new")
        assert el.val() == "new"

    def test_pushStack(self):
        things = º("<li>a</li><li>b</li>")
        stacked = things.pushStack([span("x")])

        self.assertEqual(str(stacked), "<span>x</span>")
        self.assertEqual(str(stacked.end()), "<li>a</li><li>b</li>")

    def test_queue(self):
        el = º('<div id="test"></div>')
        el.delay(10)
        assert len(el.queue()) == 1

    def test_ready(self):
        calls = []
        º('<div></div>').ready(lambda: calls.append("ready"))
        assert calls == ["ready"]

    def test_remove(self):
        page = html(body(div("keep", _id="keep"), div("drop", _id="drop")))
        º(page)
        º("div").remove("#drop")
        assert str(page) == '<html><body><div id="keep">keep</div></body></html>'

    def test_removeAttr(self):
        el = º('<div id="test" role="button"></div>')
        self.assertIs(el.removeAttr("role"), el)
        self.assertIsNone(el.attr("role"))

    def test_removeClass(self):
        a = º('<div id="test2"></div>')
        a.addClass("one").addClass("two").addClass("three")
        assert a.hasClass("one") == True
        a.removeClass("one")
        assert a.hasClass("one") == False
        a.removeClass()
        assert a.attr("class") is None

    def test_removeData(self):
        el = º('<div id="test"></div>')
        el.data("answer", 42).removeData("answer")
        assert el.data("answer") is None

    def test_removeProp(self):
        el = º('<input id="field" value="old"></input>')
        el.prop("customFlag", True)
        self.assertTrue(el.prop("customFlag"))
        self.assertIs(el.removeProp("customFlag"), el)
        self.assertIsNone(el.prop("customFlag"))

    def test_replaceAll(self):
        page = html(body(div("one", _class="target"), div("two", _class="target")))
        º(page)
        º("<span>new</span>").replaceAll(".target")
        self.assertEqual(
            str(page), "<html><body><span>new</span><span>new</span></body></html>"
        )

    def test_replaceWith(self):
        page = html(body(div("old", _id="target")))
        º(page)
        removed = º("#target").replaceWith("<span>new</span>")

        self.assertEqual(str(page), "<html><body><span>new</span></body></html>")
        self.assertEqual(str(removed), '<div id="target">old</div>')

    def test_resize(self):
        page = html(body(div("x", _id="test")))
        º(page)
        calls = []
        º("#test").resize(lambda e: calls.append(e.type))
        º("#test").resize()
        assert calls == ["resize"]

    def test_scroll(self):
        page = html(body(div("x", _id="test")))
        º(page)
        calls = []
        º("#test").scroll(lambda e: calls.append(e.type))
        º("#test").scroll()
        assert calls == ["scroll"]

    def test_scrollLeft(self):
        el = º('<div id="test"></div>')
        el.scrollLeft(11)
        assert el.scrollLeft() == 11

    def test_scrollTop(self):
        el = º('<div id="test"></div>')
        el.scrollTop(13)
        assert el.scrollTop() == 13

    def test_select(self):
        page = html(body(input(_id="field")))
        º(page)
        calls = []
        º("#field").select(lambda e: calls.append(e.type))
        º("#field").select()
        assert calls == ["select"]

    def test_serialize(self):
        page = html(
            form(
                select(
                    _name="single",
                ).html(option("Single", _selected=True), option("Single2")),
                br(),
                select(_name="multiple", _multiple="multiple").html(
                    option("Multiple", _selected="selected"),
                    option("Multiple2"),
                    option("Multiple3", _selected="selected"),
                ),
                input(_type="text", _id="lname", _name="lname"),
                input(_type="checkbox", _name="agree", _value="yes", _checked=True),
                input(_type="checkbox", _name="skip", _value="no"),
                input(_type="submit", _name="submitter", _value="send"),
            )
        )
        º(page)
        assert º("form").serialize() == "single=Single&multiple=Multiple&multiple=Multiple3&lname=&agree=yes"

    def test_serializeArray(self):
        page = html(
            form(
                input(_type="text", _name="lname", _value="smith"),
                input(_type="checkbox", _name="unchecked", _value="no"),
            )
        )
        º(page)
        assert º("form").serializeArray() == [{"name": "lname", "value": "smith"}]

    def test_show(self):
        el = º('<div id="test"></div>')
        el.hide()
        self.assertEqual(el.css("display"), "none")
        self.assertIs(el.show(), el)
        self.assertEqual(el.css("display"), "")

    def test_siblings(self):
        page = html(body(div("one", _class="match"), div("two", _id="target"), div("three", _class="match")))
        º(page)
        assert str(º("#target").siblings(".match")) == '<div class="match">one</div><div class="match">three</div>'

    def test_size(self):
        self.assertEqual(º("<li>a</li><li>b</li>").size(), 2)

    def test_slice(self):
        things = º("<li>a</li><li>b</li><li>c</li>")
        assert str(things.slice(1, 3)) == "<li>b</li><li>c</li>"

    def test_slideDown(self):
        pass

    def test_slideToggle(self):
        pass

    def test_slideUp(self):
        pass

    def test_stop(self):
        pass

    def test_submit(self):
        page = html(body(form(input(_name="x"), _id="form1")))
        º(page)
        called = []
        º("#form1").on("submit", lambda e: called.append(e.type))
        º("#form1").submit()
        assert called == ["submit"]

    def test_text(self):
        page = html(
            form(
                select(
                    _name="single",
                ).html(option("a", _selected=True), option("b")),
            ),
            div("hi"),
            div(span("there")),
        )
        º(page)
        assert º("div").text() == ["hi", "there"]
        º("div").text("test")
        assert º("div").text() == ["test", "test"]
        assert (
            str(page)
            == '<html><form><select name="single"><option selected="true">a</option><option>b</option></select></form><div>test</div><div>test</div></html>'
        )

    def test_toArray(self):
        things = º("<li>a</li><li>b</li>")
        assert [el.textContent for el in things.toArray()] == ["a", "b"]

    def test_toggle(self):
        el = º('<div id="test"></div>')
        el.toggle()
        self.assertEqual(el.css("display"), "none")
        el.toggle()
        self.assertEqual(el.css("display"), "")

    def test_toggleClass(self):
        a = º('<div id="test2"></div>')
        a.toggleClass("someclass")
        assert str(a) == '<div id="test2" class="someclass"></div>'
        a.toggleClass("someclass")
        assert str(a) == '<div id="test2"></div>'

    def test_trigger(self):
        page = html(body(button("go", _id="btn")))
        º(page)
        details = []
        º("#btn").on("build", lambda e: details.append(e.detail["id"]))
        º("#btn").trigger("build", {"detail": {"id": 7}})
        assert details == [7]

    def test_triggerHandler(self):
        page = html(body(button("go", _id="btn")))
        º(page)
        called = []
        º("#btn").on("click", lambda e: called.append(e.type))
        event = º("#btn").triggerHandler("click")
        assert called == ["click"]
        assert event.type == "click"

    def test_unbind(self):
        page = html(body(button("go", _id="btn")))
        º(page)
        called = []
        º("#btn").on("click", lambda e: called.append(e.type))
        º("#btn").unbind("click")
        º("#btn").triggerHandler("click")
        assert called == []

    def test_undelegate(self):
        pass

    def test_unload(self):
        page = html(body(div("x", _id="test")))
        º(page)
        calls = []
        º("#test").unload(lambda e: calls.append(e.type))
        º("#test").unload()
        assert calls == ["unload"]

    def test_unwrap(self):
        page = html(body(div(span("a", _class="item"), span("b"), _id="wrapper")))
        º(page)
        º(".item").unwrap()
        self.assertEqual(
            str(page),
            '<html><body><span class="item">a</span><span>b</span></body></html>',
        )

    def test_val(self):
        el = º('<input id="field" value="old"></input>')
        assert el.val() == "old"
        assert str(el.val("new")) == '<input id="field" value="new"/>'

    def test_wrap_dom_node_keeps_selector_context(self):
        page = html(body(div(_id="target")))
        º(page)
        target = º("#target")[0]
        º(target).append("<span>x</span>")
        assert str(º("#target")) == '<div id="target"><span>x</span></div>'

    def test_width(self):
        el = º('<div id="test"></div>')
        el.elements.style.width = "30px"
        assert el.width() == 30

    def test_wrap(self):
        page = html(body(span("x", _id="target")))
        º(page)
        º("#target").wrap('<section class="wrap"><article></article></section>')
        self.assertEqual(
            str(page),
            '<html><body><section class="wrap"><article><span id="target">x</span></article></section></body></html>',
        )

    def test_wrapAll(self):
        page = html(body(span("a", _class="item"), span("b", _class="item")))
        º(page)
        º(".item").wrapAll("div")
        assert str(page) == '<html><body><div><span class="item">a</span><span class="item">b</span></div></body></html>'

    def test_wrapInner(self):
        page = html(body(div(span("x"), b("y"), _id="target")))
        º(page)
        º("#target").wrapInner("<section></section>")
        self.assertEqual(
            str(page),
            '<html><body><div id="target"><section><span>x</span><b>y</b></section></div></body></html>',
        )

    def test_staticmethods(self):
        d = html()
        º(d)

        d.appendChild(body())

        # º.boxModel
        # º.browser
        # º.cssHooks
        # º.cssNumber
        # º.ready
        # º.speed
        # º.support

        # º.ajax()
        # º.ajaxPrefilter()
        # º.ajaxSetup()
        # º.ajaxTransport()
        # º.Callbacks()

        # print(d)
        # print('el:', d.documentElement)
        # print('bod:', d.body)
        assert º.contains(d.documentElement, d.body) == True  # true
        assert º.contains(d.body, d.documentElement) == False  # false

        # º.data()
        # º.Deferred()
        # º.dequeue()
        each_seen = []
        º.each(["a", "b"], lambda value: each_seen.append(value.upper()))
        self.assertEqual(each_seen, ["A", "B"])

        with self.assertRaisesRegex(Exception, "boom"):
            º.error("boom")

        self.assertEqual(º.escapeSelector("a.b#c[d]"), "a\\.b\\#c\\[d\\]")

        obj1 = {"a": 1, "b": 2}
        obj2 = {"c": 1, "b": 5}
        self.assertEqual(º.extend(obj1, obj2), {"a": 1, "b": 5, "c": 1})

        test = lambda x: x
        test2 = 1
        self.assertTrue(º.isFunction(test))
        self.assertFalse(º.isFunction(test2))

        # º.get()
        # º.getJSON()
        # º.getScript()
        self.assertEqual(º.globalEval("1 + 2"), 3)
        self.assertEqual(º.grep([1, 2, 3, 4], lambda value: value % 2 == 0), [2, 4])
        # º.hasData()
        # º.holdReady()
        # º.htmlPrefilter()
        # º.inArray()
        # º.isArray()
        # º.isEmptyObject()
        # º.isNumeric()
        # º.isPlainObject()
        # º.isWindow()
        # º.isXMLDoc()
        # º.makeArray()
        # º.map()

        first = ["a", "b", "c"]
        second = ["d", "e", "f"]
        result = º.merge(º.merge([], first), second)
        self.assertEqual(result, ["a", "b", "c", "d", "e", "f"])

        first = ["a", "b", "c"]
        second = ["d", "e", "f"]
        result = º.merge(first, second)
        self.assertEqual(result, ["a", "b", "c", "d", "e", "f"])

        # º.noConflict()
        # º.noop()

        self.assertIsInstance(º.now(), int)

        node = div()
        assert º.data(node, "k", "v") == "v"
        assert º.data(node, "k") == "v"
        assert º.hasData(node) == True
        º.removeData(node, "k")
        assert º.hasData(node) == False

        cb_calls = []
        cbs = º.Callbacks()
        cbs.add(lambda value: cb_calls.append(value)).fire("ok")
        assert cb_calls == ["ok"]

        deferred_calls = []
        dfd = º.Deferred()
        dfd.done(lambda value: deferred_calls.append(value)).resolve("done")
        assert deferred_calls == ["done"]

        assert º.parseJSON('{"a":1}') == {"a": 1}
        assert º.htmlPrefilter("<div></div>") == "<div></div>"
        assert º.param({"a": 1, "b": ["x", "y"]}) == "a=1&b=x&b=y"
        assert º.param([{"name": "q", "value": "hello world"}]) == "q=hello%20world"

        with self._ajax_handlers_isolated():
            with _DQueryRequestsMock() as server:
                º.ajaxSetup({"headers": {"X-Test": "yes"}})
                º.ajaxPrefilter(lambda settings: settings["data"].update({"pf": "1"}))

                json_seen = []
                payload = º.getJSON(
                    server.url("/echo"),
                    {"q": "json"},
                    lambda data: json_seen.append(data["query"]),
                )
                self.assertEqual(payload["query"], {"q": "json", "pf": "1"})
                self.assertEqual(json_seen, [{"q": "json", "pf": "1"}])

                posted = º.post(server.url("/echo"), {"name": "Ada"}, dataType="json")
                self.assertEqual(
                    posted,
                    {
                        "method": "POST",
                        "path": "/echo",
                        "form": {"name": "Ada", "pf": "1"},
                    },
                )

        # º.param()
        # º.parseHTML()
        # º.parseJSON()
        # º.parseXML()
        # º.post()
        # º.proxy()
        # º.queue()
        # º.readyException()
        # º.removeData()
        # º.sub()
        self.assertEqual(º.trim("  some tst \n   TEST."), "some tst    TEST.")
        # º.type()
        self.assertEqual(set(º.unique(["a", "a", "b"])), {"a", "b"})
        self.assertEqual(º.uniqueSort([3, 1, 3, 2]), [1, 2, 3])
        self.assertEqual(º.when().state(), "resolved")


if __name__ == "__main__":
    unittest.main()
