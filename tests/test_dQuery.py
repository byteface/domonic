"""
    test_dQuery
    ~~~~~~~~~~~~~~~
    unit tests for domonic.dQuery

"""

import time
import unittest

from domonic.dom import *
from domonic.dQuery import *
from domonic.html import *


class TestCase(unittest.TestCase):

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
        pass

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
        pass

    def test_ajaxError(self):
        pass

    def test_ajaxSend(self):
        pass

    def test_ajaxStart(self):
        pass

    def test_ajaxStop(self):
        pass

    def test_ajaxSuccess(self):
        pass

    def test_andSelf(self):
        pass

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
        pass

    def test_blur(self):
        pass

    def test_change(self):
        pass

    def test_children(self):
        page = html(body(div(span("one"), b("two"), _id="test")))
        º(page)
        children = º("#test").children()
        assert str(children) == "<span>one</span><b>two</b>"

    def test_clearQueue(self):
        pass

    def test_click(self):
        page = html(body(button("go", _id="btn")))
        º(page)
        called = []
        º("#btn").click(lambda e: called.append(e.type))
        º("#btn").click(None)
        assert called == ["click"]

    def test_clone(self):
        pass

    def test_closest(self):
        page = html(body(div(span("x", _id="child"), _class="wrapper")))
        º(page)
        assert str(º("#child").closest(".wrapper")) == '<div class="wrapper"><span id="child">x</span></div>'

    def test_contents(self):
        page = html(body(div("hi", span("there"), _id="test")))
        º(page)
        assert len(º("#test").contents().toArray()) == 2

    def test_context(self):
        pass

    def test_contextmenu(self):
        pass

    def test_css(self):
        pass

    def test_data(self):
        el = º('<div id="test" data-enabled="true"></div>')
        el.data("answer", 42)
        assert el.data("answer") == 42
        assert el.data("enabled") is True
        el.data({"one": 1, "two": 2})
        assert el.data() == {"answer": 42, "enabled": True, "one": 1, "two": 2}

    def test_dblclick(self):
        pass

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
        pass

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
        pass

    def test_eq(self):
        things = º("<li>a</li><li>b</li><li>c</li>")
        assert str(things.eq(1)) == "<li>b</li>"
        assert things.eq(99).length == 0
        assert things.eq(1).end().length == 3

    def test_error(self):
        pass

    def test_even(self):
        pass

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
        pass

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
        pass

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
        pass

    def test_innerHeight(self):
        pass

    def test_innerWidth(self):
        pass

    def test_insertAfter(self):
        pass

    def test_insertBefore(self):
        pass

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
        pass

    def test_keypress(self):
        pass

    def test_keyup(self):
        pass

    def test_last(self):
        things = º('<li></li><li></li><li></li><li></li><li data-tag="me"></li>')
        assert str(things.last()) == '<li data-tag="me"></li>'

    def test_length(self):
        pass

    def test_live(self):
        pass

    def test_load(self):
        pass

    def test_map(self):
        pass

    def test_mousedown(self):
        pass

    def test_mouseenter(self):
        pass

    def test_mouseleave(self):
        pass

    def test_mousemove(self):
        pass

    def test_mouseout(self):
        pass

    def test_mouseover(self):
        pass

    def test_mouseup(self):
        pass

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
        pass

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
        pass

    def test_outerWidth(self):
        pass

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
        pass

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
        pass

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
        pass

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
        pass

    def test_replaceAll(self):
        pass

    def test_replaceWith(self):
        pass

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
        pass

    def test_siblings(self):
        page = html(body(div("one", _class="match"), div("two", _id="target"), div("three", _class="match")))
        º(page)
        assert str(º("#target").siblings(".match")) == '<div class="match">one</div><div class="match">three</div>'

    def test_size(self):
        pass

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
        pass

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
        pass

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
        pass

    def test_wrapAll(self):
        page = html(body(span("a", _class="item"), span("b", _class="item")))
        º(page)
        º(".item").wrapAll("div")
        assert str(page) == '<html><body><div><span class="item">a</span><span class="item">b</span></div></body></html>'

    def test_wrapInner(self):
        pass

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
        # º.each()
        # º.error()
        # º.escapeSelector()

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
        # º.globalEval()
        # º.grep()
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
        # º.unique()
        # º.uniqueSort()
        # º.when()


if __name__ == "__main__":
    unittest.main()
