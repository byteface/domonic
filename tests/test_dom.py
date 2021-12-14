"""
    test_domonic
    ~~~~~~~~~~~~
    - unit tests for domonic.dom

"""

import unittest
# import requests
# from mock import patch

from domonic.html import *
from domonic.style import *
from domonic.dom import *
from domonic import *


class TestCase(unittest.TestCase):
    """ Tests for the dom package """

    def setUp(self):
        # can be used by all tests
        self.page = html(
            head(
                meta(_charset="utf-8"),
                meta(**{"_http-equiv": "X-UA-Compatible"}, _content="IE=edge"),
                title('website.com'),
                meta(_name="description", _content=""),
                meta(_name="viewport", _content="width=device-width, initial-scale=1"),
                meta(_name="robots", _content="all,follow"),
                link(_rel="stylesheet", _href="static/css/bootstrap.min.css"),
                link(_rel="shortcut icon", _href="favicon.png")
            ),
            body(
                div(_class="overlay").html(
                    div(_class="content h-100 d-flex align-items-center").html(
                        div(_class="container text-center text-black").html(
                            p("Welcome to the information age", _class="headings-font-family text-uppercase lead"),
                            h1("We are", span("COMPANY", _class="font-weight-bold d-block"), _class="text-uppercase hero-text text-black"),
                            p("And this is our company website", _class="headings-font-family text-uppercase lead")
                        )
                    )
                ),
                header(_class="header sticky-top").html(
                    nav(_class="navbar navbar-expand-lg bg-white border-bottom py-0").html(
                        div(_class="container").html(
                            h6("website.com"),
                            div(_id="navbarSupportedContent", _class="collapse navbar-collapse").html(
                                ul(_class="navbar-nav ml-auto px-3").html(
                                    li(a("Home", _href="", _class="nav-link text-uppercase link-scroll"), _class="nav-item active"),
                                    li(a("About", _href="#about", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                    li(a("Services", _href="#services", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                    li(a("Team", _href="#team", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                    li(a("Contact", _href="#contact", _class="nav-link text-uppercase link-scroll"), _class="nav-item"),
                                )
                            )
                        )
                    )
                ),
                section(_id="about", _class="about").html(
                    div(_class="container").html(
                        div(_class="row mb-5").html(
                            div(_class="col-lg-12").html(
                                header(_style="padding-top:20px;").html(
                                    h6("About us", _class="lined text-uppercase"),
                                ),
                                p("Specialists in xxxxx.", _class="lead"),
                                p("COMPANY can provide xxxxxx solutions. We have expertise in the following areas."),
                                div(_class="row").html(
                                    div(_class="col-lg-6").html(
                                        ul(_class="mb-0").html(
                                            li("A"),
                                            li("B"),
                                            li("C"),
                                        )
                                    ),
                                    div(_class="col-lg-6").html(
                                        ul(_class="mb-0").html(
                                            li("1"),
                                            li("2"),
                                            li("3"),
                                        )
                                    )
                                )
                            )
                        )
                    )
                ),
                div(_class="row text-white text-center", _style="background: url(static/img/header.jpg); padding:20px;").html(
                    div(_class="col-lg-12").html(
                        h5(_class="text-uppercase font-weight-bold").html(
                            i(_class="far fa-image mr-2", ), "Headline."),
                        p("Lorem ipsum."),
                    ),
                    div(_class="col-lg-12").html(
                        h5(_class="text-uppercase font-weight-bold").html(
                            i(_class="far fa-image mr-2", ), "Headline."),
                        p("Lorem ipsum."),
                    ),

                ),
                section(_id="services", _class="bg-gray").html(
                    div(_class="container").html(
                        header(_class="text-center mb-5").html(
                            #  h2("Services", _class="lined text-uppercase"),
                        ),
                        div(_class="row text-center").html(
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4("Headline", _class="text-uppercase font-weight-bold"),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4("Headline", _class="text-uppercase font-weight-bold"),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4("Headline", _class="text-uppercase font-weight-bold"),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                        )
                    ),
                    section(_id="team").html(
                        div(_class="container").html(
                            header(_class="text-center mb-5").html(
                                # h2("Our team", _class="text-uppercase lined"),
                            ),
                            div(_class="row text-center").html(
                                # div(_class="col-lg-3 col-md-6 mb-4").html(
                                div(_class="col-lg-12").html(
                                    img(_src="static/img/gol.gif", _alt="Username", _class="img-fluid mb-4", _width="300px;", _height="300px;"),
                                    h4(_class="font-weight-bold text-uppercase").html(
                                        a("Username", _href="#", _class="no-anchor-style")
                                    ),
                                    p("Director", _class="small text-gray text-uppercase"),
                                ),
                            )
                        )
                    ),
                    section(_id="contact").html(
                        div(_class="container").html(
                            header(_class="text-center mb-5").html(
                                #  h2("Contact", _class="text-uppercase lined"),
                            ),
                            div(_class="row").html(
                                div(_class="col-lg-12 text-center").html(
                                    p(
                                        "Email : ",
                                        a("user@website.com", _href="mailto:user@website.com"),
                                        br(),
                                        "or Call us on : ",
                                        a("123456789", _href="tel:123456789")
                                    ),
                                    ul(_class="mb-0 list-inline text-center").html(
                                        li(a(i(_class="fab fa-twitter"), _href="https://twitter.com/user", _class="social-link social-link-twitter"), _class="list-inline-item"),
                                        li(a(i(_class="fab fa-linkedin"), _rel="nofollow", _href="https://www.linkedin.com/in/user/", _class="social-link social-link-instagram"), _class="list-inline-item"),
                                        li(a(i(_class="fas fa-envelope"), _href="mailto:user@website.com", _class="social-link social-link-email"), _class="list-inline-item")
                                    )
                                )
                            )
                        )
                    ),
                    footer(_style="padding:20px;").html(
                        div(_class="row text-center").html(
                            div(_class="col-lg-12 text-center").html(
                                p("Copyright &copy; 2021 COMPANY. All rights Reserved.", _class="mb-0 text-gray"),
                            )
                        )
                    ),
                    script(_src="static/js/jquery.min.js"),
                    link(_rel="stylesheet", _href="https://use.fontawesome.com/releases/v5.7.1/css/all.css", _integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr", _crossorigin="anonymous")
                )
            )
        )

    def test_NodeList(self):
        nlist = self.page.body.childNodes
        assert isinstance(nlist, NodeList)
        # assert len(nlist) == 1
        # test Nodelist methods and properties. foreach, entries, keys, values
        node = document.createElement("div")
        kid1 = document.createElement("p")
        kid2 = document.createTextNode("hey")
        kid3 = document.createElement("span")
        node.appendChild(kid1)
        node.appendChild(kid2)
        node.appendChild(kid3)
        somelist = node.childNodes
        for each in somelist.values():
            print(each)
        # <p>
        # #text "hey"
        # <span>
        # https://developer.mozilla.org/en-US/docs/Web/API/NodeList/values
        # TODO - output should be no close tag and a hash say text?
        for each in somelist.keys():
            print(each)
        somelist.forEach(
            lambda currentValue, currentIndex, listObj, **kwargs: print(currentValue, currentIndex, kwargs),
            'myThisArg'
        )
        for each in somelist.entries():
            print(each)
        # Array [ 0, <p> ]
        # Array [ 1, #text "hey" ]
        # Array [ 2, <span> ]
        # print(somelist.item(0))
        # print(somelist.item(1))
        # print(somelist.item(2))
        assert somelist.item(0) == kid1
        assert somelist.item(1) == kid2
        assert somelist.item(2) == kid3

    def test_Node(self):

        n = Node()
        self.assertIsInstance(n, Node)
        # n.assertEqual(str(sometag), '<div id="someid">asdfasdf<div></div><div>yo</div></div>')
        # n.baseURI = 'eventual.technology'
        # n.baseURIObject = None
        # n.isConnected = True
        # n.namespaceURI = "http://www.w3.org/1999/xhtml"
        # n.nodePrincipal = None
        # n.outerText = None
        # n.ownerDocument = None
        # n.prefix = None  # 🗑️
        # n.rootNode = None

        b = Node()
        n.appendChild(b)
        # note this was fixed from being a property to a method in 6.6.7
        self.assertEqual(True, n.hasChildNodes())

        c = Node()
        n.appendChild(c)
        self.assertEqual(c, n.lastChild)
        self.assertEqual(b, n.firstChild)
        self.assertEqual(2, n.childElementCount)
        self.assertEqual(True, b in n.childNodes)
        self.assertEqual(True, c in n.childNodes)
        self.assertEqual(None, n.localName)  # obsolete if not a tag or attribute should return none
        self.assertEqual(2, len(n.children))
        self.assertEqual(None, n.nodeValue)

        # test all props on Node
        # self.assertEqual(None, n.baseURI)
        # self.assertEqual(None, n.baseURIObject)
        # self.assertEqual(None, n.childNodes)
        # self.assertEqual(None, n.firstChild)
        # self.assertEqual(None, n.isConnected)
        # self.assertEqual(None, n.isDefaultNamespace)
        # self.assertEqual(None, n.isEqualNode)
        # self.assertEqual(None, n.isSameNode)
        # self.assertEqual(None, n.isSupported)
        # self.assertEqual(None, n.lastChild)
        # self.assertEqual(None, n.localName)
        # self.assertEqual(None, n.namespaceURI)
        # self.assertEqual(None, n.nextSibling)
        # self.assertEqual(None, n.nodeName)
        # self.assertEqual(None, n.nodeType)
        # self.assertEqual(None, n.nodeValue)
        # self.assertEqual(None, n.ownerDocument)
        # self.assertEqual(None, n.parentElement)
        # self.assertEqual(None, n.parentNode)
        # self.assertEqual(None, n.prefix)
        # self.assertEqual(None, n.previousSibling)
        # self.assertEqual(None, n.textContent)

        # print(n.nodeType())
        d = div("test")
        # print(type(d))
        # print(d.nodeName)

        # TODO - i thought had to be uppercase. but this breaks on html5lib treeparser
        # line 1681ish html5parser.py  says... assert node.name == "script"
        # which stops that parser working with domonic
        #
        # self.assertEqual("DIV", d.nodeName)

        self.assertEqual("test", d.nodeValue)
        self.assertEqual(True, n.contains(c))

        n.insertBefore(d, c)
        self.assertEqual(True, n.children[1] == d)

        self.assertEqual(True, n.contains(c))
        n.removeChild(c)
        self.assertEqual(False, n.contains(c))

        # print( n.replaceChild(self, newChild, oldChild) )
        n2 = n.cloneNode()
        # print(len(n2.children))
        self.assertEqual(True, len(n2.children) == 2)
        self.assertEqual(False, n.children == n2.children)
        self.assertEqual(True, n.isSameNode(n))
        self.assertEqual(False, n.isSameNode(n2))
        a1 = div("hi")
        a2 = div("hi")
        self.assertEqual(True, a1.isEqualNode(a2))

        print(a1.nodeValue)
        self.assertEqual(True, a1.nodeValue == "hi")

        a1.nodeValue = "something else"
        self.assertEqual(True, a1.nodeValue == "something else")
        # print(a1.nodeValue)

        a1.textContent = "something new"
        self.assertEqual(True, a1.textContent == "something new")
        # print(a1.textContent)

        myobj = domonic.domonify('div(_class="mytest")')
        # print('---')
        # print(type(myobj))
        myobj.style.float = "left"
        # myobj.style.zIndex = "1"
        # print('---')
        print(myobj)
        print(str(myobj))
        self.assertEqual(True, str(myobj) == '<div class="mytest" style="float:left;"></div>')

        # print("NOW>>>>")
        mylist = li() / 10
        assert str(mylist) == '<li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li>'

        myobj = domonic.load(mylist)
        print(myobj)

        myorderedlist = ol()
        myorderedlist += str(li() / 10)
        assert str(myorderedlist) == '<ol><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li></ol>'

        # TODO - tests
        # compareDocumentPosition()
        # getRootNode()
        # isDefaultNamespace()
        # lookupNamespaceURI()
        # lookupPrefix()
        # normalize()
        # def isSupported(self): return False #  🗑
        # getUserData() 🗑️
        # setUserData() 🗑️

    def test_node(self):
        sometag = div("asdfasdf", div(), div("yo"), _id="test", _thingy="test22")
        somenewdiv = div('im new')
        sometag.appendChild(somenewdiv)

        assert str(somenewdiv.parentNode) == '<div id="test" thingy="test22">asdfasdf<div></div><div>yo</div><div>im new</div></div>'
        assert isinstance(somenewdiv.parentNode, div)
        assert somenewdiv.parentNode.id == "test"
        # print(somenewdiv.parentElement)
        # print(somenewdiv.previousSibling)
        assert str(somenewdiv.previousSibling.nextSibling) == "<div>im new</div>"

        mylist = ul(li(1), li(2), li(3))
        assert str(mylist[1]) == "<li>2</li>"

        mylist = ul(li(), li(), li())
        # print(*mylist)
        assert str(mylist) == '<ul><li></li><li></li><li></li></ul>'

        a1, b1, c1 = ul(li(1), li(2), li(3))
        # print(a1)
        assert str(a1) == '<li>1</li>'

        a1, b1, c1, d1, e1 = button() * 5
        # print(a1, b1, c1, d1, e1)
        assert str(a1) == '<button></button>'
        assert str(b1) == '<button></button>'
        assert str(c1) == '<button></button>'
        assert str(d1) == '<button></button>'
        assert str(e1) == '<button></button>'

        # print(mylist[1] != mylist[1])
        a1 = img()
        a1 >> {'_src': "http://www.someurl.com"}
        # print(a1)
        assert str(a1) == '<img src="http://www.someurl.com"/>'

        a1 = button()
        a1 += "hi"
        a1 += "how"
        a1 += "are"
        a1 += "you"
        assert str(a1) == "<button>hihowareyou</button>"
        a1 -= "hi"
        assert str(a1) == "<button>howareyou</button>"

        # print(div(_test="1", **{"_data-test": ""}))

        assert sometag.id == 'test'
        # print(sometag.style.color)  # TODO - get on style
        assert sometag._thingy == 'test22'
        assert sometag.thingy == 'test22'

        # print(10/sometag)
        # print('>>>>', sometag.args[0])
        # print('>>>>',sometag)
        # print('>>>>', sometag.lastChild())
        # print('>>>>', sometag.content)

        # import gc
        # import pprint
        # for r in gc.get_referents(somenewdiv):
        #     pprint.pprint(r)

        # for r in gc.get_referents(sometag):
        #     pprint.pprint(r)

    def test_body(self):
        somebody = body("test", _class="why")  # .html("wn")
        assert str(somebody) == '<body class="why">test</body>'
        # replacing content
        somebody = body("test", _class="why").html("nope")
        assert str(somebody) == '<body class="why">nope</body>'

    def test_dom(self):
        # test div html and innerhtml update content
        sometag = div("asdfasdf", div(), div("yo"), _id="someid")
        self.assertEqual(sometag.tagName, 'div')
        self.assertEqual(str(sometag), '<div id="someid">asdfasdf<div></div><div>yo</div></div>')
        sometag.html('test')
        self.assertEqual(str(sometag), '<div id="someid">test</div>')
        sometag.innerHTML = 'test2'
        self.assertEqual(str(sometag), '<div id="someid">test2</div>')

        # same test on body tag
        bodytag = body("test", _class="why")
        self.assertEqual(str(bodytag), '<body class="why">test</body>')
        # print(bodytag)

        bodytag.html("bugs bunny")
        self.assertEqual(str(bodytag), '<body class="why">bugs bunny</body>')
        # print('THIS:',bodytag)

        # sometag.innerText()
        # print(sometag.getAttribute('_id'))
        self.assertEqual(sometag.getAttribute('_id'), 'someid')
        # print(sometag.getAttribute('id'))
        # self.assertEqual(sometag.getAttribute('_id'), 'someid')

        mydiv = div("I like cake", div(_class='myclass').html(div("1"), div("2"), div("3")))
        # print(mydiv)
        assert str(mydiv) == '<div>I like cake<div class="myclass"><div>1</div><div>2</div><div>3</div></div></div>'

        print(sometag.innerText())

        # return
        # print(sometag.nodeName)
        # assert(sometag.nodeName, 'DIV') # TODO - i checked one site in chrome, was upper case. not sure if a standard?

        sometag.setAttribute('id', 'newid')
        assert sometag.getAttribute('id') == 'newid'
        assert str(sometag) == '<div id="newid"></div>'
        assert sometag.lastChild == sometag.firstChild
        assert sometag.hasChildNodes() == False

        sometag.removeAttribute('id')
        assert str(sometag) == '<div></div>'

        sometag.appendChild(footer('test'))
        assert str(sometag) == '<div><footer>test</footer></div>'

        assert sometag.children[0].tagName == 'footer'
        assert str(sometag.children[0]) == '<footer>test</footer>'

        # print(sometag.firstChild)
        assert str(sometag.firstChild) == '<footer>test</footer>'

        htmltag = html()
        assert htmltag.tagName == 'html'
        assert str(htmltag) == '<html></html>'
        htmltag.write('sup!')
        # print("?????", htmltag)
        assert str(htmltag) == '<html>sup!</html>'
        htmltag.className = "my_cool_css"
        # print(htmltag)
        assert str(htmltag) == '<html class="my_cool_css">sup!</html>'
        # print(htmltag)
        # print('-END-')

    def test_create(self):
        # print(html().documentElement)
        # print(html().URL)
        somebody = document.createElement('sometag')
        # print(str(somebody))
        assert str(somebody) == '<sometag></sometag>'
        comm = document.createComment('hi there here is a comment')
        # print(comm)
        assert str(comm) == '<!--hi there here is a comment-->'

        # print(html().createElement('sometag'))
        # somebody = document.createElement('sometag')
        # print(str(somebody()))
        assert str(somebody) == '<sometag></sometag>'

    def test_events(self):
        # print(html().documentElement)
        # print(html().URL)
        site = html()
        somebody = document.createElement('div')
        site.appendChild(somebody)
        # print(site)
        assert str(site) == '<html><div></div></html>'

        def test(evt, *args, **kwargs):
            # print('test ran!')
            # print(evt)
            # print(evt.target)
            assert evt.target == somebody or evt.target == site

        site.addEventListener('click', test)
        somebody.addEventListener('anything', test)
        # print(site.listeners)
        assert site.listeners['click'] == [test]
        # site.removeEventListener('click', test)
        # print( site.listeners )

        site.dispatchEvent(Event('click'))
        somebody.dispatchEvent(Event('anything'))

        # document.getElementById("myBtn").addEventListener("click", function(){
        #   document.getElementById("demo").innerHTML = "Hello World";
        # });

    def test_contains(self):
        site = html()
        somebody = document.createElement('div')
        site.appendChild(somebody)
        # print(site)
        assert str(site) == '<html><div></div></html>'
        another_div = div()
        # print(site.contains(somebody))
        assert site.contains(somebody)
        another_div = div()
        # print(site.contains(another_div))
        assert not site.contains(another_div)
        another_div = document.createElement('div')
        # print(site.contains(another_div))
        assert not site.contains(another_div)
        third_div = document.createElement('div')
        another_div.appendChild(third_div)
        assert another_div.contains(third_div)
        assert not site.contains(document.createElement('div'))
        site.appendChild(another_div)
        assert site.contains(third_div)
        # print(site.contains(third_div))
        assert site.contains(another_div)

    def test_getElementById(self):
        dom1 = html(div(div(div(div(div(div(div(article("asdfasdf", div(), div("yo"), _id="test")))))))))
        result = dom1.getElementById('test')
        assert result.tagName == 'article'
        # print(result)
        # print(len(result.children))
        # assert len(result.children) == 3  # TODO - does a text node count?

    def test_remove(self):
        dom1 = html(div(div(div(div(div(div(div(div("asdfasdf", div(), div("yo"), _id="test")))))))))
        result = dom1.getElementById('test')
        # print("owner:", result.ownerDocument)
        assert result.ownerDocument == dom1
        result.remove()
        assert "asdfasdf" not in str(dom1)
        pass

    # def test_getElementByClassName(self):
    #     dom1 = html(div(div(div(div(div(div(div(div("asdfasdf", div(), div("yo"), _class="test this thing")))))))))
    #     result = dom1.getElementByClassName('thing')
    #     print('--')
    #     print(result)
    #     print('--')
    #     pass

    def test_dir(self):
        dom1 = div(div(), _dir="rtl")
        assert dom1.dir == "rtl"

    def test_normalize(self):
        wrapper = Document.createElement("div")
        wrapper.appendChild(Document.createTextNode("Part 1 "))
        wrapper.appendChild(Document.createTextNode("Part 2 "))
        wrapper.appendChild("Part 3")
        assert len(wrapper.childNodes) == 3
        wrapper.normalize()
        assert len(wrapper.childNodes) == 1
        # print(wrapper)
        assert str(wrapper) == '<div>Part 1 Part 2 Part 3</div>'
        pass

    # def test_Node():
        # TODO - tests all below
        # contains - probably need more recursive testing
        # replaceChild
        # anchors

    def test_querySelector(self):
        dom1 = html(div(div(div(div(div(div(div(div(_id="thing"), span(_id="fun"), div("asdfasdf", div(), div("yo"), _class="test this thing")))))))))

        result = dom1.querySelector('#thing')
        # print('--')
        # print("RESULT>>>>>", result)
        # print('--')
        assert result.id == 'thing'

        result = dom1.querySelector('span')
        # print('--')
        # print("RESULT>>>>>", result)
        assert result.id == 'fun'

        result = dom1.querySelector('.test')
        # print('--')
        # print("RESULT>>>>>", result)
        assert result.className == 'test this thing'

        result = dom1.getElementsByClassName('this')
        # print('--')
        # print("RESULT>>>>>", result)
        assert len(result) == 1
        assert result[0].className == 'test this thing'

        links = self.page.querySelectorAll("a[rel=nofollow]")
        for linky in links:
            print(linky.getAttribute("href"))
        assert len(links) == 1

        result = self.page.querySelectorAll("li[class='nav-item']")
        expected = ["About", "Services", "Team", "Contact"]
        for i, r in enumerate(result):
            assert r.textContent == expected[i]
        assert len(result) == 4

        result = self.page.querySelectorAll("h4[class='font-weight-bold text-uppercase']")
        # print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # fails

        result = self.page.querySelectorAll("li.nav-item")
        # print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.querySelectorAll("a[href='#services']")
        # print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.querySelectorAll("p.text-gray")
        # print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.querySelectorAll("a[href$='technology']")
        # print(result)
        for r in result:
            print(r)

        print('>>>>>>>>>')  # works

        result = self.page.querySelectorAll("a[href*='twitter']")
        # print(result)
        for r in result:
            print(r)

        print('>>>>>>>>>')  # works

        result = dom1.querySelectorAll('.fa-twitter')
        print('--')
        print("z RESULT>>>>>", result)
        # TODO - failing. however this is now running through qselectorall
        # return
        # assert result.className == 'test this thing'


    def test_getElementsBySelector(self):
        dom1 = html(div(div(div(div(div(div(div(div(_id="thing"), span(_id="fun"), div("asdfasdf", div(), div("yo"), _class="test this thing")))))))))

        result = dom1.getElementsBySelector('#thing', dom1)[0]
        # print("RESULT>>>>>", result)
        # print('--')
        # return
        assert result.id == 'thing'

        result = dom1.getElementsBySelector('span', dom1)[0]
        # print('--')
        # print("RESULT>>>>>", result)
        assert result.id == 'fun'

        # result = dom1.getElementsBySelector('.test', dom1)#[0]  # [0] #?? no class called test?
        # print('--')
        # print("RESULT>>>>>", result)
        # TODO - failing. however this is now running through qselectorall
        # return
        # assert result.className == 'test this thing'

        # result = dom1.getElementsBySelector('.this', dom1)[0]
        # print('--')
        # print("RESULT>>>>>", result)
        # assert len(result) == 1
        # assert result[0].className == 'test this thing'

        from domonic.dQuery import º
        º(self.page)

        # print(º('a'))
        # print(str(page.getElementsBySelector("a[rel=nofollow]", page)[0]))
        # print(str(page.getElementsBySelector("a", page)))

        # print(º('#team'))
        print('xxxxxxxxxxxxxxxxxxxxxxxx')
        node = str(self.page.getElementsBySelector("#team", self.page)[0])
        assert node.startswith('<section id="team"')

        # print(º('a[rel=nofollow]'))
        # print(str(page.getElementsBySelector("a[rel=nofollow]", page)[0]))

        # print(º('.fab'))
        # print(str(page.getElementsBySelector(".fab", page)))

        # print(º('.far'))
        # print(º('a'))
        # print(str(page.getElementsBySelector(".fab", page)))

        # if there's a rule.
        # if its a tag

        # if just class regular seems better
        #  circular reerence if i use it in query selector for tags.

        # if True:
        # return

        # render( page, 'index.html' )

        links = self.page.getElementsBySelector("a[rel=nofollow]", self.page)
        for linky in links:
            print(linky.getAttribute("href"))
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("li[class='nav-item']", self.page)
        # print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("h4[class='font-weight-bold text-uppercase']", self.page)
        # print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # fails

        result = self.page.getElementsBySelector("li.nav-item", self.page)
        # print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("a[href='#services']", self.page)
        # print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("p.text-gray", self.page)
        # print(result)
        for r in result:
            print(r)
        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("a[href$='technology']", self.page)
        # print(result)
        for r in result:
            print(r)

        print('>>>>>>>>>')  # works

        result = self.page.getElementsBySelector("a[href*='twitter']", self.page)
        # print(result)
        for r in result:
            print(r)

        print('>>>>>>>>>')  # works

    def test_decorators(self):
        from domonic.decorators import el

        @el(html)
        @el(body)
        @el(div)
        def test():
            return 'hi!'
        # print(test())
        assert str(test()) == '<html><body><div>hi!</div></body></html>'
        # print('decorators work!')

        @el(html, True)
        @el(body, True)
        @el(div, True)
        def test():
            return 'hi!'
        assert test() == '<html><body><div>hi!</div></body></html>'
        # print('decorators work2!')

        @el('html')
        @el('body')
        @el('div')
        def test():
            return 'hi!'
        # print(test())
        assert str(test()) == '<html><body><div>hi!</div></body></html>'
        # print('decorators work3!')

        @el(html, True)
        @el(body)
        @el('div')
        def test():
            return 'hi!'
        print(test())
        # print('decorators work4!')
        assert str(test()) == '<html><body><div>hi!</div></body></html>'

    def test_domonic_window_console_log(self):
        # note originally dom had everything from document
        # this will likely move later versions

        # window = Window()
        # Window().console.log("test this")
        # window.console.log("test this")

        # c = Console()
        # c.log()
        # Console.log('test')
        # someObject = { 'str': "Some text", 'id': 5 }
        # Console.log(someObject)

        # [09:27:13.475] ({str:"Some text", id:5})

        count = 5
        Console.log('--count: %d', count)
        assert Console.log('count: %d', count) == "count: 5"
        Console.log('--count:', count)
        assert Console.log('count:', count) == "count: 5"

        console.time("answer time")
        console.timeLog("answer time")
        console.timeEnd("answer time")

        errorMsg = 'the # is not even'
        for number in range(2, 5):
            console.log('the # is ' + str(number))
            console.assert_(number % 2 == 0, {'number': number, 'errorMsg': errorMsg})

        console.info('test2')
        console.warn('test3')
        pass


    def test_domonic_matches(self):
        content = ul(_id="birds").html(
            li("Orange-winged parrot"),
            li("Philippine eagle", _class="endangered"),
            li("Great white pelican")
        )
        birds = content.getElementsByTagName('li')
        # print(type(birds))
        assert len(birds) == 3
        assert birds[1] == content.getElementsBySelector('li.endangered', content)[0]
        assert birds[1].className == 'endangered'
        assert birds[1].classList == ['endangered']
        for bird in birds:
            if bird.matches('.endangered'):
                # print('The ' + bird.textContent + ' is endangered!')
                assert 'The ' + bird.textContent + ' is endangered!' == 'The Philippine eagle is endangered!'


    def test_getElementsByTagName(self):
        content = ul(_id="birds").html(
            li("Orange-winged parrot"),
            li("Philippine eagle", _class="endangered"),
            li("Great white pelican")
        )
        birds = content.getElementsByTagName('li')
        assert len(birds) == 3
        assert birds[1] == content.getElementsBySelector('li.endangered', content)[0]
        assert birds[1].className == 'endangered'
        assert birds[1].classList == ['endangered']

        a = self.page.getElementsByTagName('a')
        assert len(a) == 11
        # print(a)
        assert a[1].href == "#about"
        assert a[1].textContent == "About"

        titletag = self.page.getElementsByTagName('h1')
        assert len(titletag) == 1
        # print(titletag[0].textContent)
        assert titletag[0].textContent == "We areCOMPANY"

    # def test_domonic_closest(self):

    def test_sanitize(self):

        # our input string to clean
        # stringToClean = 'Some text <b><i>with</i></b> <blink>tags</blink>, including a rogue script <script>alert(1)</script> def. # TODO - failing due to blink tag

        # TODO - parser is stripping last space off the string
        # stringToClean = 'Some text <b><i>with</i></b> <p>tags</p>, including a rogue script <script>alert(1)</script> def.'
        # result = Sanitizer().sanitizeToString(stringToClean)
        # console.log("result::", result)
        # assert result == "Some text <b><i>with</i></b> <blink>tags</blink>, including a rogue script def."
        # return

        sample = "<div style='cool'><span id='span1' class='theclass' style='font-weight: bold'>hello</span></div>"
        # sample = '<div style="cool"><span id="span1" class="theclass" style="font-weight: bold">hello</span></div>'

        # Allow only <span style>: <span style='font-weight: bold'>...</span>
        s1 = Sanitizer({'allowAttributes': {"style": ["span"]}}).sanitize(sample)
        # print(type(s1))
        # print(s1)
        assert str(s1) == '<div><span style="font-weight: bold">hello</span></div>'

        # Allow style, but not on span: <span>...</span>
        s2 = Sanitizer({'allowAttributes': {"style": ["div"]}}).sanitize(sample)
        # print(s2)
        assert str(s2) == '<div style="cool"><span>hello</span></div>'

        # Allow style on any elements: <span style='font-weight: bold'>...</span>
        s3 = Sanitizer({'allowAttributes': {"style": ["*"]}}).sanitize(sample)
        # print("3::::", s3)
        # print(str(s3))
        # Note - check why is id/class not a default config?
        assert str(s3) == '<div style="cool"><span style="font-weight: bold">hello</span></div>'

        # Drop <span id>: <span class='theclass' style='font-weight: bold'>...</span>
        s4 = Sanitizer({'dropAttributes': {"id": ["span"]}}).sanitize(sample)
        # print("4::::", s4)
        assert str(s4) == '<div style="cool"><span class="theclass" style="font-weight: bold">hello</span></div>'

        # Drop id, everywhere: <span class='theclass' style='font-weight: bold'>...</span>
        s5 = Sanitizer({'dropAttributes': {"id": ["*"]}}).sanitize(sample)
        print("5::::", s5)
        print(s5)
        assert str(s5) == '<div style="cool"><span class="theclass" style="font-weight: bold">hello</span></div>'

        # Comments will be dropped by default.
        # comment = to_node("Hello  World!")
        # Sanitizer().sanitize(comment)  # "Hello  World!"
        # Sanitizer({'allowComments': True}).sanitize(comment)  # Same as comment.

        # Does the default config allow script elements?
        # Sanitizer.getDefaultConfiguration().allowElements.includes("script")  # false

        # We found a Sanitizer instance. Does it have an allow-list configured?
        # a_sanitizer = ...;
        # !!a_sanitizer.getConfiguration().allowElements # true, if an allowElements list is configured

        # If it does have an allow elements list, does it include the <div> element?
        # a_sanitizer.getConfiguration().allowElements.includes("div")  # true, if "div" is in allowElements.

        # Note that the getConfiguration method might do some normalization. E.g., it won’t
        # contain key/value pairs that are not declare in the IDL.
        # Object.keys(new Sanitizer({madeUpDictionaryKey: "Hello"}).getConfiguration())  # []

        # As a Sanitizer’s config describes its operation, a new sanitizer with
        # another instance’s configuration should behave identically.
        # (For illustration purposes only. It would make more sense to just use a directly.)
        # a = /* ... a Sanitizer we found somewhere ... */;
        # b = Sanitizer(a.getConfiguration());  // b should behave the same as a.

        # getDefaultConfiguration() and new Sanitizer().getConfiguration should be the same.
        # (For illustration purposes only. There are better ways of implementing
        # object equality in JavaScript.)
        # JSON.stringify(Sanitizer.getDefaultConfiguration()) == JSON.stringify(new Sanitizer().getConfiguration());  // true

    def test_comment(self):
        from domonic.html import comment
        # https://github.com/byteface/domonic/issues/38
        com = f"{html(head(),body(comment('foo')))}"
        # print(com)
        com = comment('foo')
        # print(f'{com}')
        assert str(com) == '<!--foo-->'
        from domonic.dom import Comment
        # https://github.com/byteface/domonic/issues/38
        com = f"{html(head(),body(Comment('foo')))}"
        print(com)
        # not able to recreate. Comment was updated to a Node in 6.1
        # this may have been due to that
        # TODO - mulitple arguments to comment

    def test_body(self):
        print('im running1')
        aNewBodyElement = document.createElement("body")
        aNewBodyElement.id = "newBodyElement"
        page = html()
        page.body = aNewBodyElement
        print('im running2')
        assert page.body.id == "newBodyElement"

    def test_head(self):
        aNewHeadElement = document.createElement("head")
        aNewHeadElement.id = "newHeadElement"
        page = html()
        page.head = aNewHeadElement
        assert page.head.id == "newHeadElement"
        assert page.head.nodeName == "head"
        assert page.head.nodeType == Node.ELEMENT_NODE

    def test_title(self):
        aNewTitleElement = document.createElement("title")
        aNewTitleElement.textContent = "newTitleElement"
        page = html()
        page.title = aNewTitleElement
        assert page.title == "newTitleElement"

    def test_anchors(self):
        mydoc = html(body('test'))
        mydoc.body.append(a(name='foo'))
        mydoc.body.append(a(name='bar'))
        mydoc.body.append(a(href='#test'))
        assert len(mydoc.anchors) == 2

    def test_treewalker(self):

        from domonic.dom import Comment
        from domonic.dom import TreeWalker

        doc = html(
            div(_id="contentarea").html(
            p("Some ", span("text")),
            b("Bold text")
        )
        )

        rootnode = doc.getElementById("contentarea")
        # print(rootnode)
        walker = doc.createTreeWalker(rootnode, NodeFilter.SHOW_ELEMENT, None, False)

        print(walker.currentNode)
        assert str(walker.currentNode) == '<div id="contentarea"><p>Some <span>text</span></p><b>Bold text</b></div>'
        # print(walker.firstChild())
        # print(walker.firstChild())
        # print(walker.firstChild())
        # print(walker.firstChild())

        # //Alert the starting node Tree Walker currently points to (root node)
        window.alert(walker.currentNode.tagName)  # alerts DIV (with id=contentarea)
        # assert walker.currentNode.tagName == 'DIV'

        # Step through and alert all child nodes
        # for n in walker.nextNode():
        print('---')
        while walker.nextNode():
            # print('+++', walker.nextNode())
            window.alert(walker.currentNode)  # //alerts P, SPAN, and B.
        print('---')

        # //Go back to the first child node of the collection and alert it
        walker.currentNode = rootnode  # //reset TreeWalker pointer to point to root node
        print(walker.currentNode)
        # print('>>', walker.firstChild()) # calling it breaks it cos it moves it?. is it like an iterator then?
        assert walker.firstChild().tagName.lower() == 'p'   # //alerts P

        return

        # test 2
        doc = html(
            ul(_id="mylist").html(
                    li("List 1"),
                    li("List 2"),
                    li("List 3")
                )
            )

        rootnode = doc.getElementById("mylist")
        walker = doc.createTreeWalker(rootnode, NodeFilter.SHOW_ELEMENT, None, False)

        window.alert(len(walker.currentNode.childNodes))  # //alerts 7 (includes text nodes)
        window.alert(len(walker.currentNode.getElementsByTagName("*")))  # //alerts 3

        # test 3
        doc = html(
            div(_id="main").html(
            p("This is a ", span("paragraph")),
            b("Bold text")
        )
        )
        mainDiv = doc.getElementById("main")
        walker = doc.createTreeWalker(mainDiv, NodeFilter.SHOW_ELEMENT, None, False)
        console.log(walker)

        treeWalker = document.createTreeWalker(
            mainDiv,
            NodeFilter.SHOW_TEXT,
            lambda node: NodeFilter.FILTER_ACCEPT if (String(node.nodeValue).trim() != "") else NodeFilter.FILTER_REJECT,
            False
            )

        # //Alert the starting node Tree Walker currently points to (root node)
        # //displays DIV (with id=main)
        console.log(walker.currentNode.tagName)

        # //Step through and alert all child nodes
        while (walker.nextNode()):
            # //displays P, SPAN, and B.
            console.log(walker.currentNode.tagName)

        # //Go back to the first child node of the collection and display it
        # //to do that, we must reset TreeWalker pointer to point to main DIV
        walker.currentNode = mainDiv
        # //displays P
        console.log(walker.firstChild().tagName)

        # //reset TreeWalker pointer to point to main DIV
        walker.currentNode = mainDiv

        # test 4
        # https://gist.github.com/bennadel/10545473

        # test 5
        # https://paul.kinlan.me/dom-treewalker/


class NodeTest(TestCase):
    # found these unit tests for a 17 yr old dom implementation. modded them to work on domonic.
    # helped me fix lots of bugs and edge cases and quirky(expected) behaviors.
    # https://github.com/nibrahim/PlasTeX/tree/21875f4da0ae7639d2205260d2e5cb1b65539296/unittests/DOM
    # LICENSE https://github.com/nibrahim/PlasTeX/blob/21875f4da0ae7639d2205260d2e5cb1b65539296/LICENSE
    # looks like the actual project is here. still supported... https://github.com/plastex/plastex

    def _checkPositions(self, node):
        """ Check the postions of all contained nodes """
        if isinstance(node, CharacterData):
            return

        if not(isinstance(node, Node)):
            return

        maxidx = len(node) - 1

        # Check firstChild and lastChild
        if node.childNodes:
            assert node.firstChild is node[0], 'firstChild is incorrect'
            assert node.lastChild is node[maxidx], 'lastChild is incorrect'

        # Check nextSibling
        for i, item in enumerate(node):
            if i == maxidx:
                assert item.nextSibling is None, \
                       'nextSibling in position %s should be None' % i
            else:
                assert item.nextSibling is node[i+1], \
                       'nextSibling in position %s is incorrect (%s)' % \
                       (i, item.nextSibling)

        # Check previousSibling
        for i, item in enumerate(node):
            if i == 0:
                assert item.previousSibling is None, \
                       'previousSibling in position %s should be None' % i
            else:
                # print('HERE::::', item, item.previousSibling, node[i-1])
                assert item.previousSibling is node[i-1], \
                       'previousSibling in position %s is incorrect (%s)' % \
                       (i, item.previousSibling)

        # Check parentNode
        for i, item in enumerate(node):
            assert item.parentNode is node, \
                   'parentNode in position %s is incorrect' % i

        # Check ownerDocument
        for i, item in enumerate(node):
            assert item.ownerDocument is node.ownerDocument, \
                   'ownerDocument in position %s (%s) is incorrect: %s' % (i, item.ownerDocument, node.ownerDocument)

        # Check attributes
        if node.attributes:
            for key, value in node.attributes.items():
                if isinstance(value, Node):
                    assert value.parentNode is node, \
                           'parentNode is incorrect (%s)' % value.parentNode
                    self._checkPositions(value)

                elif isinstance(value, list):
                    for item in value:
                        assert getattr(item, 'parentNode', node) is node, \
                               'parentNode is incorrect (%s)' % item.parentNode
                        self._checkPositions(item)

                elif isinstance(value, dict):
                    for item in value.values():
                        assert getattr(item, 'parentNode', node) is node, \
                               'parentNode is incorrect (%s)' % item.parentNode
                        self._checkPositions(item)

    def test_Document(self):
        # There should be one-- and preferably only one --obvious way to do it.
        doc = Document()
        one = doc.createElement('one')
        two = document.createElement('two')
        three = Document.createElement('three')
        node = Document().createElement('top')
        # node.extend([one, two, three])
        node += [one, two, three]
        expected = [one, two, three]
        for i, item in enumerate(node):
            assert item is expected[i], '"%s" != "%s"' % (item, expected[i])
        self._checkPositions(node)

    def test_firstChild(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createElement('two')
        assert node.firstChild is None, '"%s" != None' % node.firstChild
        node.append(one)
        assert node.firstChild is one, '"%s" != "%s"' % (node.firstChild, one)
        # node.insert(0, two)
        node.prepend(two)
        assert node.firstChild is two, '"%s" != "%s"' % (node.firstChild, two)
        self._checkPositions(node)

    def test_lastChild(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createElement('two')
        assert node.lastChild is None, '"%s" != None' % node.lastChild
        node.append(one)
        assert node.lastChild is one, '"%s" != "%s"' % (node.lastChild, one)
        node.append(two)
        assert node.lastChild is two, '"%s" != "%s"' % (node.lastChild, two)
        self._checkPositions(node)

    def test_childNodes(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        node.append(one)
        node.append(two)
        node.append(three)
        assert node[0] is one, '"%s" != "%s"' % (node[0], one)
        assert node[1] is two, '"%s" != "%s"' % (node[1], two)
        assert node[2] is three, '"%s" != "%s"' % (node[2], three)
        assert node.childNodes[0] is one, '"%s" != "%s"' % (node.childNodes[0], one)
        assert node.childNodes[1] is two, '"%s" != "%s"' % (node.childNodes[1], two)
        assert node.childNodes[2] is three, '"%s" != "%s"' % (node.childNodes[2], three)
        self._checkPositions(node)

    def test_previousSibling(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        node.append(one)
        node.append(two)
        node.append(three)
        assert None is one.previousSibling, 'None != "%s"' % one.previousSibling
        assert one is two.previousSibling, '"%s" != "%s"' % (one, two.previousSibling)
        assert two is three.previousSibling, '"%s" != "%s"' % (two, three.previousSibling)

    def test_nextSibling(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        node.append(one)
        node.append(two)
        node.append(three)
        assert two is one.nextSibling, '"%s" != "%s"' % (two, one.nextSibling)
        assert three is two.nextSibling, '"%s" != "%s"' % (three, two.nextSibling)
        assert None is three.nextSibling, 'None != "%s"' % three.nextSibling

    def test_compareDocumentPosition(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        four = Document.createElement('four')
        node.append(one)
        node.append(two)
        node.append(three)
        three.append(four)
        five = Document.createElement('five')

        expected = Node.DOCUMENT_POSITION_FOLLOWING
        rc = one.compareDocumentPosition(four)
        # print(rc, expected)
        assert rc == expected, '"%s" != "%s"' % (rc, expected)

        expected = Node.DOCUMENT_POSITION_PRECEDING
        rc = four.compareDocumentPosition(one)
        assert rc == expected, '"%s" != "%s"' % (rc, expected)

        expected = Node.DOCUMENT_POSITION_CONTAINED_BY
        rc = node.compareDocumentPosition(four)
        assert rc == expected, '"%s" != "%s"' % (rc, expected)

        expected = Node.DOCUMENT_POSITION_CONTAINS
        rc = four.compareDocumentPosition(node)
        assert rc == expected, '"%s" != "%s"' % (rc, expected)

        expected = Node.DOCUMENT_POSITION_DISCONNECTED
        rc = five.compareDocumentPosition(node)
        assert rc == expected, '"%s" != "%s"' % (rc, expected)

    def test_insertBefore(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        node.append(one)
        node.append(two)
        node.insertBefore(three, two)
        # print('>>', node)
        assert node[1] is three, '"%s" != "%s"' % (node[1], three)
        node.insertBefore(three, one)
        # print(node)
        # print(node[2], two)
        assert node[0] is three, '"%s" != "%s"' % (node[0], three)
        assert node[1] is one, '"%s" != "%s"' % (node[1], one)
        assert node[2] is two, '"%s" != "%s"' % (node[2], two)
        # print(node)
        self._checkPositions(node)

    def test_replaceChild(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        node.append(one)
        node.append(two)
        node.replaceChild(three, two)
        assert node[0] is one, '"%s" != "%s"' % (node[0], one)
        assert node[1] is three, '"%s" != "%s"' % (node[1], three)
        assert len(node) == 2, '%s != %s' % (len(node), 2)
        self._checkPositions(node)

    def test_removeChild(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        node.append(one)
        node.append(two)
        res = node.removeChild(one)
        assert res is one, '"%s" != "%s"' % (res, one)
        assert len(node) == 1, '%s != %s' % (len(node), 1)
        assert node[0] is two, '"%s" != "%s"' % (node[0], two)
        self._checkPositions(node)
        res = node.removeChild(two)
        assert res is two, '"%s" != "%s"' % (res, two)
        assert len(node) == 0, '%s != %s' % (len(node), 0)

    def test_appendChild(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        node.appendChild(one)
        # print(node)
        frag = Document.createDocumentFragment()
        frag.appendChild(two)
        frag.appendChild(three)
        node.appendChild(frag)
        # print(node)
        assert node[0] is one, '"%s" != "%s"' % (node[0], one)
        assert node[1] is two, '"%s" != "%s"' % (node[1], two)
        assert node[2] is three, '"%s" != "%s"' % (node[2], three)
        self._checkPositions(node)

    def test_insert(self):
        """ Insert into empty node """
        one = Document.createElement('one')
        two = Document.createElement('two')
        three = Document.createElement('three')
        node = Document.createElement('top')
        # node.insert(0, one)
        # node.insert(1, two)
        # node.insert(2, three)
        node += one
        # node.insertBefore(two, one)
        # node.insertBefore(three, two)
        # TODO - just add an optional positional parameter to append?
        node.args = node.args[:2] + (two,) + node.args[2:]  # does same as node.insert(1, two)
        node.args = node.args[:3] + (three,) + node.args[3:]  # does same as node.insert(2, three)
        # print(node)
        expected = [one, two, three]
        for i, item in enumerate(node):
            assert item is expected[i], '"%s" != "%s"' % (item, expected[i])
        self._checkPositions(node)

    def test_insert2(self):
        """ Insert into populated node """
        one = Document.createElement('one')
        two = Document.createElement('two')
        three = Document.createElement('three')
        node = Document.createElement('top')
        # node.extend([one, two, three])
        node += [one, two, three]
        # print("cool?", node)
        # node += 2
        # node += 3
        i0 = Document.createElement('i0')
        i3 = Document.createTextNode('i3')
        # node.insert(0, i0)
        node.prepend(i0)
        # node.insert(3, i3) # TODO - consider an insertAt non standard addition to node? (although then where do you stop. grep/moveTo/find_at/every list method?. etc)
        node.args = node.args[:3] + (i3,) + node.args[3:]  # does same as insert(3, i3)
        # print("cool2?", node)
        expected = [i0, one, two, i3, three]
        for i, item in enumerate(node):
            assert item is expected[i], '"%s" != "%s"' % (item, expected[i])
        self._checkPositions(node)

    def test_Element_prepend(self):
        """ Insert document fragment """
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        four = Document.createElement('four')
        node.appendChild(one)
        node.appendChild(two)
        frag = Document.createDocumentFragment()
        frag.appendChild(three)
        frag.appendChild(four)
        # node.insert(1, frag)
        # node.args = (args).extend(self.args)
        # add frag at nodes position 1
        # TODO - what is expected behaviour for prepending frags?.
        # as appendChild says to break it apart and add each child?. not sure with append/prepend
        node.prepend(frag)
        # print(node)
        print("TODO.test_Element_prepend")
        return
        assert node[0] is one, '"%s" != "%s"' % (node[0], one)
        assert node[1] is three, '"%s" != "%s"' % (node[1], three)
        assert node[2] is four, '"%s" != "%s"' % (node[2], four)
        assert node[3] is two, '"%s" != "%s"' % (node[3], two)
        self._checkPositions(node)

    # TODO - item assignment - bring dunders over from tag now? - or we bringing all over for v8?
    # def testSetItem(self):
    #     doc = Document()
    #     node = doc.createElement('node')
    #     one = doc.createElement('one')
    #     two = doc.createTextNode('two')
    #     three = doc.createElement('three')
    #     four = doc.createElement('four')
    #     five = doc.createElement('five')
    #     node.appendChild(one)
    #     node.appendChild(two)
    #     node.appendChild(three)

    #     node[1] = four
    #     assert node[0] is one, '"%s" != "%s"' % (node[0], one)
    #     assert node[1] is four, '"%s" != "%s"' % (node[1], four)
    #     assert node[2] is three, '"%s" != "%s"' % (node[2], three)
    #     assert len(node) == 3, '%s != %s' % (len(node), 3)
    #     self._checkPositions(node)

    #     node[2] = five
    #     assert node[0] is one, '"%s" != "%s"' % (node[0], one)
    #     assert node[1] is four, '"%s" != "%s"' % (node[1], four)
    #     assert node[2] is five, '"%s" != "%s"' % (node[2], five)
    #     assert len(node) == 3, '%s != %s' % (len(node), 3)
    #     self._checkPositions(node)

    def test_extend(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createElement('three')
        four = Document.createElement('four')
        five = Document.createElement('five')
        node.appendChild(one)
        # node.extend([two, three])
        node += [two, three]
        assert node[0] is one, '"%s" != "%s"' % (node[0], one)
        assert node[1] is two, '"%s" != "%s"' % (node[1], two)
        assert node[2] is three, '"%s" != "%s"' % (node[2], three)
        assert len(node) == 3, '%s != %s' % (len(node), 3)
        self._checkPositions(node)
        node += [four, five]
        assert node[3] is four, '"%s" != "%s"' % (node[3], four)
        assert node[4] is five, '"%s" != "%s"' % (node[4], five)
        assert len(node) == 5, '%s != %s' % (len(node), 5)
        self._checkPositions(node)

    def test_hasChildNodes(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        assert not node.hasChildNodes()
        node.appendChild(one)
        node.appendChild(two)
        assert node.hasChildNodes()

    def test_cloneNode(self):
        one = Document.createElement('one')
        two = Document.createElement('two')
        three = Document.createTextNode('three')
        two.append(three)
        one.append(two)
        res = one.cloneNode(1)
        assert type(res) is type(one), '"%s" != "%s"' % (type(res), type(one))
        assert type(res[0]) is type(one[0])
        # print(one, res)
        # print(type(one), type(res))
        assert str(one) == str(res)
        assert one is not res
        assert one[0] is not res[0]

    def test_normalize(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createTextNode('two')
        three = Document.createTextNode('three')
        four = Document.createTextNode('four')
        node.appendChild(one)
        node.appendChild(two)
        node.appendChild(three)
        node.appendChild(four)
        # node.extend([one, two, three, four])
        # print(node)
        node.normalize()
        # print(node)
        assert len(node) == 2, '"%s" != "%s"' % (len(node), 2)
        assert node[1] == 'twothreefour', '"%s" != "%s"' % (node[1], 'twothreefour')

    def test_hasAttributes(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        assert not node.hasAttributes()
        # node.attributes['one'] = one
        # print(str(node.attributes))
        # print(len(node.attributes))
        # node._test2 = 'test1'  # TODO - still need to sort
        # node.test2 = 'test2'  # TODO - still need to sort
        # node['test'] = 'test3' # TODO - auto-underscore?. (problem is expectation on getters. think back to the broken branch)
        node['_test4'] = 'test4'
        # node >> {"_test":'test'}
        # print(node)
        # print(node.attributes)
        # print(len(node.attributes))
        # print(node._test4)
        # print(node['_test4'])
        assert node.hasAttributes()

    def test_textContent(self):
        node = Document.createElement('node')
        one = Document.createTextNode('one')
        two = Document.createElement('two')
        three = Document.createTextNode('three')
        four = Document.createTextNode('four')
        node.append(one)
        node.append(two)
        # two.extend([three, four])
        two.append(three)
        two.append(four)
        res = node.textContent
        expected = 'onethreefour'
        assert res == expected, '"%s" != "%s"' % (res, expected)

    def test_isSameNode(self):
        node = Document.createElement('node')
        assert node.isSameNode(node)
        clone = node.cloneNode()
        assert not node.isSameNode(clone)

    def test_isEqualNode(self):
        node = Document.createElement('node')
        one = Document.createElement('one')
        two = Document.createElement('two')
        # node.extend([one, two])
        node += 1
        node += 2
        node2 = node.cloneNode(deep=True)
        assert node.isEqualNode(node2)

    # TODO - support legacy methods if they don't break anything?
    # def testGetSetUserData(self):
    #     doc = Document()
    #     node = doc.createElement('node')
    #     node.setUserData('foo', 'bar')
    #     res = node.getUserData('foo')
    #     assert res == 'bar'


if __name__ == '__main__':
    unittest.main()
