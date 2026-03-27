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
        print("---** -")
        print(º("#test"))
        print("---** -")
        print(º(".things"))
        print("---** -")

        print("a::")
        a = º('<div class="test2"></div>')
        print(a)

        print("b::")
        print(º("#test"))
        b = º("#test").append(a)
        print(b)

        print(d)

        pass

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
            str(a) == '<div id="test2" class="one one two three"></div><div id="test3" class="one one two three"></div>'
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
        print(app)
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
        print("TEST APPEND")
        d = º('<div></div>').append("some text")
        self.assertEqual(str(d), "<div>some text</div>")

    def test_appendTo(self):
        pass

    def test_attr(self):
        a = º('<div id="test2"></div>')
        a.addClass("one")
        assert str(a) == '<div id="test2" class="one"></div>'
        assert a.attr("id") == "test2"
        assert a.attr("class") == "one"
        a.attr("id", "somethingelse")
        assert str(a) == '<div id="somethingelse" class="one"></div>'
        # print(a.elements[0])

    def test_before(self):
        pass

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
        el = º('<div id="test"></div>')
        el.data("answer", 42)
        assert el.data("answer") == 42

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
        pass

    def test_empty(self):
        pass

    def test_end(self):
        pass

    def test_eq(self):
        pass

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
        pass

    def test_has(self):
        pass

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
        pass

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
        pass

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
        pass

    def test_removeAttr(self):
        pass

    def test_removeClass(self):
        a = º('<div id="test2"></div>')
        a.addClass("one").addClass("two").addClass("three")
        assert a.hasClass("one") == True
        a.removeClass("one")
        assert a.hasClass("one") == False

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
            )
        )
        º(page)
        assert º("form").serialize() == "single=Single&multiple=Multiple&multiple=Multiple3&lname="

    def test_serializeArray(self):
        page = html(form(input(_type="text", _name="lname", _value="smith")))
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
        pass

    def test_toggle(self):
        pass

    def test_toggleClass(self):
        a = º('<div id="test2"></div>')
        a.toggleClass("someclass")
        assert str(a) == '<div id="test2" class="someclass"></div>'
        a.toggleClass("someclass")
        assert str(a) == '<div id="test2"></div>'

    def test_trigger(self):
        pass

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
        pass

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
        print("test_staticmethods::::::::::::::::::")

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
        print(º.extend(obj1, obj2))

        test = lambda x: x
        test2 = 1
        print("well?:", º.isFunction(test))
        print("well?:", º.isFunction(test2))

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
        print(first)
        print(second)
        print(result)

        first = ["a", "b", "c"]
        second = ["d", "e", "f"]
        result = º.merge(first, second)
        print(first)
        print(second)
        print(result)

        # º.noConflict()
        # º.noop()

        print(º.now())

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
        print(º.trim("  some tst \n   TEST."))
        # º.type()
        # º.unique()
        # º.uniqueSort()
        # º.when()


if __name__ == "__main__":
    unittest.main()
