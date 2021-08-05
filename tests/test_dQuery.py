"""
    test_dQuery
    ~~~~~~~~~~~~~~~
    unit tests for domonic.dQuery

"""

import time
import unittest
# import requests
# from mock import patch
# from domonic.javascript import Math

from domonic.dom import *
from domonic.html import *
from domonic.dQuery import *


class TestCase(unittest.TestCase):

    # domonic.dQuery.º
    def test_hello(self):
        d = html(head(body(li(_class='things'), div(_id="test"))))
        º(d)
        print('---** -')
        print(º('#test'))
        print('---** -')
        print(º('.things'))
        print('---** -')

        print('a::')
        a = º('<div class="test2"></div>')
        print(a)

        print('b::')
        b = º('#test').append(a)
        print(b)

        print(d)

        pass

    def test_add(self):
        # test = º('<p></p>').add('<h1>').add(div())
        # print(test)
        pass

    def test_addBack(self):
        pass

    def test_addClass(self):
        a = º('<div id="test2"></div><div id="test3"></div>')
        assert str(a) == '<div id="test2"></div><div id="test3"></div>'
        a.addClass('one')
        assert str(a) == '<div id="test2" class="one"></div><div id="test3" class="one"></div>'
        # print("1:",a)
        # print("2:",str(a))
        # print(str(a))
        a.addClass('one').addClass('two').addClass('three')
        assert str(a) == '<div id="test2" class="one one two three"></div><div id="test3" class="one one two three"></div>'
        # for el in a.elements:
            # print(el.getAttribute("class"))

    def test_after(self):
        # TODO - sort the parser... positional error on this as not multiline
        # tags = º('<div id="test1"><h1>asd</h1></div>')
        # print(tags)
        app = html(head(), body(div(span(), _id="test")))
        º(app)  # TODO _str is none?
        # print( 'wtf:??:', º('#test1') ) # TODO - better errors when passing wrong id name
        º('#test').after(p('hi'))
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
        # doc = html()
        # º(doc)
        # doc.append("some text")
        # print(doc.html())
        # d = º('<div></div>').append("some text")
        # self.assertEqual(str(d), '<div>some text</div>')
        pass

    def test_appendTo(self):
        pass

    def test_attr(self):
        a = º('<div id="test2"></div>')
        a.addClass('one')
        assert str(a) == '<div id="test2" class="one"></div>'
        assert a.attr('id') == 'test2'
        assert a.attr('class') == 'one'
        a.attr('id', 'somethingelse')
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
        pass

    def test_clearQueue(self):
        pass

    def test_click(self):
        pass

    def test_clone(self):
        pass

    def test_closest(self):
        pass

    def test_contents(self):
        pass

    def test_context(self):
        pass

    def test_contextmenu(self):
        pass

    def test_css(self):
        pass

    def test_data(self):
        pass

    def test_dblclick(self):
        pass

    def test_delay(self):
        pass

    def test_delegate(self):
        pass

    def test_dequeue(self):
        pass

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
        pass

    def test_find(self):
        pass

    def test_finish(self):
        pass

    def test_first(self):
        pass

    def test_focus(self):
        pass

    def test_focusin(self):
        pass

    def test_focusout(self):
        pass

    def test_get(self):
        pass

    def test_has(self):
        pass

    def test_hasClass(self):
        a = º('<div id="test2"></div>')
        a.addClass('one').addClass('two').addClass('three')
        assert a.hasClass('one') == True
        assert a.hasClass('five') == False

    def test_height(self):
        pass

    def test_hide(self):
        pass

    def test_hover(self):
        pass

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
        pass

    def test_nextAll(self):
        pass

    def test_nextUntil(self):
        pass

    # def test_not(self):
        # pass

    def test_odd(self):
        pass

    def off(self, event):
        pass

    def test_offset(self):
        pass

    def test_offsetParent(self):
        pass

    def on(self, event, callback):
        pass

    def test_one(self):
        pass

    def test_outerHeight(self):
        pass

    def test_outerWidth(self):
        pass

    def test_parent(self):
        pass

    def test_parents(self):
        pass

    def test_parentsUntil(self):
        pass

    def test_position(self):
        pass

    def prepend(self, html):
        pass

    def test_prependTo(self):
        pass

    def test_prev(self):
        pass

    def test_prevAll(self):
        pass

    def test_prevUntil(self):
        pass

    def test_promise(self):
        pass

    def test_prop(self):
        pass

    def test_pushStack(self):
        pass

    def test_queue(self):
        pass

    def test_ready(self):
        pass

    def test_remove(self):
        pass

    def test_removeAttr(self):
        pass

    def test_removeClass(self):
        a = º('<div id="test2"></div>')
        a.addClass('one').addClass('two').addClass('three')
        assert a.hasClass('one') == True
        a.removeClass('one')
        assert a.hasClass('one') == False

    def test_removeData(self):
        pass

    def test_removeProp(self):
        pass

    def test_replaceAll(self):
        pass

    def test_replaceWith(self):
        pass

    def test_resize(self):
        pass

    def test_scroll(self):
        pass

    def test_scrollLeft(self):
        pass

    def test_scrollTop(self):
        pass

    def test_select(self):
        pass

    def test_serialize(self):
        page = html(form(
            select(_name="single",).html(
                option("Single", _selected=True),
                option("Single2")
            ),
            br(),
            select(_name="multiple", _multiple="multiple").html(
                option("Multiple", _selected="selected"),
                option("Multiple2"),
                option("Multiple3", _selected="selected")
            ),
            input(_type="text", _id="lname", _name="lname")
        ))
        º(page)
        print(º('form').serialize())

    def test_serializeArray(self):
        pass

    def test_show(self):
        pass

    def test_siblings(self):
        pass

    def test_size(self):
        pass

    def test_slice(self):
        pass

    def test_slideDown(self):
        pass

    def test_slideToggle(self):
        pass

    def test_slideUp(self):
        pass

    def test_stop(self):
        pass

    def test_submit(self):
        pass

    def test_text(self):
        page = html(form(
                select(_name="single",).html(
                    option("a", _selected=True),
                    option("b")
                ),
            ),
            div('hi'),
            div(span('there'))
        )
        º(page)
        assert º('div').text() == ['hi', 'there']
        º('div').text('test')
        assert º('div').text() == ['test', 'test']
        assert str(page) == '<html><form><select name="single"><option selected="True">a</option><option>b</option></select></form><div>test</div><div>test</div></html>'

    def test_toArray(self):
        pass

    def test_toggle(self):
        pass

    def test_toggleClass(self):
        # page = html(form(
        #         select(_name="single",).html(
        #             option("a", _selected=True),
        #             option("b")
        #         ), _id='test'
        #     ),
        #     div('hi'),
        #     div(span('there'))
        # )
        # º(page)
        # print(page)
        # º('#test').toggleClass('someclass')
        # print(page)
        # º('#test').toggleClass('someclass')
        # print(page)
        pass

    def test_trigger(self):
        pass

    def test_triggerHandler(self):
        pass

    def test_unbind(self):
        pass

    def test_undelegate(self):
        pass

    def test_unload(self):
        pass

    def test_unwrap(self):
        pass

    def test_val(self):
        pass

    def test_width(self):
        pass

    def test_wrap(self):
        pass

    def test_wrapAll(self):
        pass

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
        
        obj1 = {'a':1,'b':2}
        obj2 = {'c':1,'b':5}
        print(º.extend(obj1,obj2))

        test = lambda x:x
        test2 = 1
        print("well?:",º.isFunction(test))
        print("well?:",º.isFunction(test2))

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


if __name__ == '__main__':
    unittest.main()
