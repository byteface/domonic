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


class domonicTestCase(unittest.TestCase):

    # domonic.dQuery.º
    def test_dQuery_hello(self):
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

    def test_dQuery_add(self):
        # test = º('<p></p>').add('<h1>').add(div())
        # print(test)
        pass

    def test_dQuery_addBack(self):
        pass

    def test_dQuery_addClass(self):
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

    def test_dQuery_after(self):
        pass

    def test_dQuery_ajaxComplete(self):
        pass

    def test_dQuery_ajaxError(self):
        pass

    def test_dQuery_ajaxSend(self):
        pass

    def test_dQuery_ajaxStart(self):
        pass

    def test_dQuery_ajaxStop(self):
        pass

    def test_dQuery_ajaxSuccess(self):
        pass

    def test_dQuery_andSelf(self):
        pass

    def test_dQuery_animate(self):
        pass

    def test_dQuery_append(self):
        print("TEST APPEND")
        # doc = html()
        # º(doc)
        # doc.append("some text")
        # print(doc.html())
        # d = º('<div></div>').append("some text")
        # self.assertEqual(str(d), '<div>some text</div>')
        pass

    def test_dQuery_appendTo(self):
        pass

    def test_dQuery_attr(self):
        a = º('<div id="test2"></div>')
        a.addClass('one')
        assert str(a) == '<div id="test2" class="one"></div>'
        assert a.attr('id') == 'test2'
        assert a.attr('class') == 'one'
        a.attr('id', 'somethingelse')
        assert str(a) == '<div id="somethingelse" class="one"></div>'
        # print(a.elements[0])

    def test_dQuery_before(self):
        pass

    def test_dQuery_bind(self):
        pass

    def test_dQuery_blur(self):
        pass

    def test_dQuery_change(self):
        pass

    def test_dQuery_children(self):
        pass

    def test_dQuery_clearQueue(self):
        pass

    def test_dQuery_click(self):
        pass

    def test_dQuery_clone(self):
        pass

    def test_dQuery_closest(self):
        pass

    def test_dQuery_contents(self):
        pass

    def test_dQuery_context(self):
        pass

    def test_dQuery_contextmenu(self):
        pass

    def test_dQuery_css(self):
        pass

    def test_dQuery_data(self):
        pass

    def test_dQuery_dblclick(self):
        pass

    def test_dQuery_delay(self):
        pass

    def test_dQuery_delegate(self):
        pass

    def test_dQuery_dequeue(self):
        pass

    def test_dQuery_detach(self):
        pass

    def test_dQuery_die(self):
        pass

    def test_dQuery_each(self):
        pass

    def test_dQuery_empty(self):
        pass

    def test_dQuery_end(self):
        pass

    def test_dQuery_eq(self):
        pass

    def test_dQuery_error(self):
        pass

    def test_dQuery_even(self):
        pass

    def test_dQuery_fadeIn(self):
        pass

    def test_dQuery_fadeOut(self):
        pass

    def test_dQuery_fadeTo(self):
        pass

    def test_dQuery_fadeToggle(self):
        pass

    def test_dQuery_filter(self):
        pass

    def test_dQuery_find(self):
        pass

    def test_dQuery_finish(self):
        pass

    def test_dQuery_first(self):
        pass

    def test_dQuery_focus(self):
        pass

    def test_dQuery_focusin(self):
        pass

    def test_dQuery_focusout(self):
        pass

    def test_dQuery_get(self):
        pass

    def test_dQuery_has(self):
        pass

    def test_dQuery_hasClass(self):
        a = º('<div id="test2"></div>')
        a.addClass('one').addClass('two').addClass('three')
        assert a.hasClass('one') == True
        assert a.hasClass('five') == False

    def test_dQuery_height(self):
        pass

    def test_dQuery_hide(self):
        pass

    def test_dQuery_hover(self):
        pass

    def test_dQuery_html(self):
        pass

    def test_dQuery_index(self):
        pass

    def test_dQuery_innerHeight(self):
        pass

    def test_dQuery_innerWidth(self):
        pass

    def test_dQuery_insertAfter(self):
        pass

    def test_dQuery_insertBefore(self):
        pass

    # def test_dQuery_is(self):
        # pass

    def test_dQuery_keydown(self):
        pass

    def test_dQuery_keypress(self):
        pass

    def test_dQuery_keyup(self):
        pass

    def test_dQuery_last(self):
        things = º('<li></li><li></li><li></li><li></li><li data-tag="me"></li>')
        assert str(things.last()) == '<li data-tag="me"></li>'

    def test_dQuery_length(self):
        pass

    def test_dQuery_live(self):
        pass

    def test_dQuery_load(self):
        pass

    def test_dQuery_map(self):
        pass

    def test_dQuery_mousedown(self):
        pass

    def test_dQuery_mouseenter(self):
        pass

    def test_dQuery_mouseleave(self):
        pass

    def test_dQuery_mousemove(self):
        pass

    def test_dQuery_mouseout(self):
        pass

    def test_dQuery_mouseover(self):
        pass

    def test_dQuery_mouseup(self):
        pass

    def test_dQuery_next(self):
        pass

    def test_dQuery_nextAll(self):
        pass

    def test_dQuery_nextUntil(self):
        pass

    # def test_dQuery_not(self):
        # pass

    def test_dQuery_odd(self):
        pass

    def off(self, event):
        pass

    def test_dQuery_offset(self):
        pass

    def test_dQuery_offsetParent(self):
        pass

    def on(self, event, callback):
        pass

    def test_dQuery_one(self):
        pass

    def test_dQuery_outerHeight(self):
        pass

    def test_dQuery_outerWidth(self):
        pass

    def test_dQuery_parent(self):
        pass

    def test_dQuery_parents(self):
        pass

    def test_dQuery_parentsUntil(self):
        pass

    def test_dQuery_position(self):
        pass

    def prepend(self, html):
        pass

    def test_dQuery_prependTo(self):
        pass

    def test_dQuery_prev(self):
        pass

    def test_dQuery_prevAll(self):
        pass

    def test_dQuery_prevUntil(self):
        pass

    def test_dQuery_promise(self):
        pass

    def test_dQuery_prop(self):
        pass

    def test_dQuery_pushStack(self):
        pass

    def test_dQuery_queue(self):
        pass

    def test_dQuery_ready(self):
        pass

    def test_dQuery_remove(self):
        pass

    def test_dQuery_removeAttr(self):
        pass

    def test_dQuery_removeClass(self):
        a = º('<div id="test2"></div>')
        a.addClass('one').addClass('two').addClass('three')
        assert a.hasClass('one') == True
        a.removeClass('one')
        assert a.hasClass('one') == False

    def test_dQuery_removeData(self):
        pass

    def test_dQuery_removeProp(self):
        pass

    def test_dQuery_replaceAll(self):
        pass

    def test_dQuery_replaceWith(self):
        pass

    def test_dQuery_resize(self):
        pass

    def test_dQuery_scroll(self):
        pass

    def test_dQuery_scrollLeft(self):
        pass

    def test_dQuery_scrollTop(self):
        pass

    def test_dQuery_select(self):
        pass

    def test_dQuery_serialize(self):
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

    def test_dQuery_serializeArray(self):
        pass

    def test_dQuery_show(self):
        pass

    def test_dQuery_siblings(self):
        pass

    def test_dQuery_size(self):
        pass

    def test_dQuery_slice(self):
        pass

    def test_dQuery_slideDown(self):
        pass

    def test_dQuery_slideToggle(self):
        pass

    def test_dQuery_slideUp(self):
        pass

    def test_dQuery_stop(self):
        pass

    def test_dQuery_submit(self):
        pass

    def test_dQuery_text(self):
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

    def test_dQuery_toArray(self):
        pass

    def test_dQuery_toggle(self):
        pass

    def test_dQuery_toggleClass(self):
        pass

    def test_dQuery_trigger(self):
        pass

    def test_dQuery_triggerHandler(self):
        pass

    def test_dQuery_unbind(self):
        pass

    def test_dQuery_undelegate(self):
        pass

    def test_dQuery_unload(self):
        pass

    def test_dQuery_unwrap(self):
        pass

    def test_dQuery_val(self):
        pass

    def test_dQuery_width(self):
        pass

    def test_dQuery_wrap(self):
        pass

    def test_dQuery_wrapAll(self):
        pass

    def test_dQuery_wrapInner(self):
        pass

    def test_dQuery_staticmethods(self):
        print("test_dQuery_staticmethods::::::::::::::::::")

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
