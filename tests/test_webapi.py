"""
    test_webapi
    ~~~~~~~~~~~~~~~~
"""

import unittest

from domonic.dom import *
from domonic.javascript import *
from domonic.webapi import *
# from domonic.decorators import silence


class TestCase(unittest.TestCase):

    def test_encodingAPI(self):
        # utf8decoder = TextDecoder()  # default 'utf-8' or 'utf8'

        # u8arr = Uint8Array([240, 160, 174, 183])
        # i8arr = Int8Array([-16, -96, -82, -73])
        # u16arr = Uint16Array([41200, 47022])
        # i16arr = Int16Array([-24336, -18514])
        # i32arr = Int32Array([-1213292304])

        # console.log(utf8decoder.decode(u8arr))
        # console.log(utf8decoder.decode(i8arr))
        # console.log(utf8decoder.decode(u16arr))
        # console.log(utf8decoder.decode(i16arr))
        # console.log(utf8decoder.decode(i32arr))

        # win1251decoder = TextDecoder('windows-1251')
        # b = Uint8Array([207, 240, 232, 226, 229, 242, 44, 32, 236, 232, 240, 33])
        # console.log(win1251decoder.decode(b))  # // Привет, мир!
        pass

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
        pass

    def test_gamepad(self):
        pass

    def test_geolocation(self):
        pass

    def test_history(self):
        pass

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

    def test_xhr(self):
        from domonic.html import form, input, button, br, hr, div
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

        myform = form(action='/', method='post')
        myform += input(type='text', name='name', placeholder='Name')
        myform += input(type='text', name='email', placeholder='Email')
        myform += input(type='text', name='phone', placeholder='Phone')
        myform += input(type='text', name='message', placeholder='Message')
        # myform += button(type='submit', value='Submit')

        f = FormData(myform)
        print(f)

        # f.append('name', 'John')
        # f.append('age', '25')
        # f.append('email', '

        print('***')

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


    def test_xpath(self):

        from domonic import domonic
        from domonic.webapi.xpath import XPathEvaluator, XPathResult

        # api unit test based on mdn example
        # https://developer.mozilla.org/en-US/docs/Web/API/XPathEvaluator

        somehtml = '''
        <div>XPath example</div>
        <div>Number of &lt;div&gt;s: <output></output></div>
        '''
        page = domonic.parseString(somehtml)  # NOTE - probably requries html5lib install
        evaluator = XPathEvaluator()
        expression = evaluator.createExpression("//div")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        assert result.snapshotLength == 2
        # print(result.nodes)

        import requests
        r = requests.get("http://eventual.technology")
        page = domonic.parseString(r.content.decode("utf-8"))

        ## Selectors

        evaluator = XPathEvaluator()
        expression = evaluator.createExpression("//h1")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        assert str(result.nodes[0]) == '<h1 class="text-uppercase hero-text text-black">We are<span class="font-weight-bold d-block">Eventual Technology</span></h1>'

        expression = evaluator.createExpression("//div//p")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        assert str(result.nodes[0]) == '<p class="headings-font-family text-uppercase lead">Welcome to the information age</p>'

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

        expression = evaluator.createExpression('//*[@_class="social-link social-link-instagram"]')  # NOTE - requires all classes to match
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes))

        # expression = evaluator.createExpression("//input[@type='submit']")
        # result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        # print(str(result.nodes))

        expression = evaluator.createExpression("//a[contains(@_href, 'twitter')]")
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes[0]))
        # wow. nice!

        expression = evaluator.createExpression('//*[last()][name()="a"]')
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes[0]))
        # so cool this all works out of the box!

        expression = evaluator.createExpression('//span/text()')
        result = expression.evaluate(page, XPathResult.ORDERED_NODE_SNAPSHOT_TYPE)
        print(str(result.nodes[0]))

        '''
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
        '''


if __name__ == '__main__':
    unittest.main()
