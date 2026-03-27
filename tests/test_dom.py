"""
    test_domonic
    ~~~~~~~~~~~~
    - unit tests for domonic.dom

"""

import os
import tempfile
import unittest

from domonic import *
from domonic.dom import *
from domonic.html import *
from domonic.style import *


class DOMTest(unittest.TestCase):
    """Tests for the dom package"""

    @classmethod
    def setUpClass(cls):
        # can be used by all tests
        cls.page = html(
            head(
                meta(_charset="utf-8"),
                meta(**{"_http-equiv": "X-UA-Compatible"}, _content="IE=edge"),
                title("website.com"),
                meta(_name="description", _content=""),
                meta(_name="viewport", _content="width=device-width, initial-scale=1"),
                meta(_name="robots", _content="all,follow"),
                link(_rel="stylesheet", _href="static/css/bootstrap.min.css"),
                link(_rel="shortcut icon", _href="favicon.png"),
            ),
            body(
                div(_class="overlay").html(
                    div(_class="content h-100 d-flex align-items-center").html(
                        div(_class="container text-center text-black").html(
                            p("Welcome to the information age", _class="headings-font-family text-uppercase lead"),
                            h1(
                                "We are",
                                span("COMPANY", _class="font-weight-bold d-block"),
                                _class="text-uppercase hero-text text-black",
                            ),
                            p("And this is our company website", _class="headings-font-family text-uppercase lead"),
                        )
                    )
                ),
                header(_class="header sticky-top").html(
                    nav(_class="navbar navbar-expand-lg bg-white border-bottom py-0").html(
                        div(_class="container").html(
                            h6("website.com"),
                            div(_id="navbarSupportedContent", _class="collapse navbar-collapse").html(
                                ul(_class="navbar-nav ml-auto px-3").html(
                                    li(
                                        a("Home", _href="", _class="nav-link text-uppercase link-scroll"),
                                        _class="nav-item active",
                                    ),
                                    li(
                                        a("About", _href="#about", _class="nav-link text-uppercase link-scroll"),
                                        _class="nav-item",
                                    ),
                                    li(
                                        a("Services", _href="#services", _class="nav-link text-uppercase link-scroll"),
                                        _class="nav-item",
                                    ),
                                    li(
                                        a("Team", _href="#team", _class="nav-link text-uppercase link-scroll"),
                                        _class="nav-item",
                                    ),
                                    li(
                                        a("Contact", _href="#contact", _class="nav-link text-uppercase link-scroll"),
                                        _class="nav-item",
                                    ),
                                )
                            ),
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
                                    ),
                                ),
                            )
                        )
                    )
                ),
                div(
                    _class="row text-white text-center", _style="background: url(static/img/header.jpg); padding:20px;"
                ).html(
                    div(_class="col-lg-12").html(
                        h5(_class="text-uppercase font-weight-bold").html(
                            i(
                                _class="far fa-image mr-2",
                            ),
                            "Headline.",
                        ),
                        p("Lorem ipsum."),
                    ),
                    div(_class="col-lg-12").html(
                        h5(_class="text-uppercase font-weight-bold").html(
                            i(
                                _class="far fa-image mr-2",
                            ),
                            "Headline.",
                        ),
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
                        ),
                    ),
                    section(_id="team").html(
                        div(_class="container").html(
                            header(_class="text-center mb-5").html(
                                # h2("Our team", _class="text-uppercase lined"),
                            ),
                            div(_class="row text-center").html(
                                # div(_class="col-lg-3 col-md-6 mb-4").html(
                                div(_class="col-lg-12").html(
                                    img(
                                        _src="static/img/gol.gif",
                                        _alt="Username",
                                        _class="img-fluid mb-4",
                                        _width="300px;",
                                        _height="300px;",
                                    ),
                                    h4(_class="font-weight-bold text-uppercase").html(
                                        a("Username", _href="#", _class="no-anchor-style")
                                    ),
                                    p("Director", _class="small text-gray text-uppercase"),
                                ),
                            ),
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
                                        a("123456789", _href="tel:123456789"),
                                    ),
                                    ul(_class="mb-0 list-inline text-center").html(
                                        li(
                                            a(
                                                i(_class="fab fa-twitter"),
                                                _href="https://twitter.com/user",
                                                _class="social-link social-link-twitter",
                                            ),
                                            _class="list-inline-item",
                                        ),
                                        li(
                                            a(
                                                i(_class="fab fa-linkedin"),
                                                _rel="nofollow",
                                                _href="https://www.linkedin.com/in/user/",
                                                _class="social-link social-link-instagram",
                                            ),
                                            _class="list-inline-item",
                                        ),
                                        li(
                                            a(
                                                i(_class="fas fa-envelope"),
                                                _href="mailto:user@website.com",
                                                _class="social-link social-link-email",
                                            ),
                                            _class="list-inline-item",
                                        ),
                                    ),
                                )
                            ),
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
                    link(
                        _rel="stylesheet",
                        _href="https://use.fontawesome.com/releases/v5.7.1/css/all.css",
                        _integrity="sha384-fnmOCqbTlWIlj8LyTjo7mOUStjsKC4pOpQbqyi7RrhN7udi9RwhKkMHpvLbHG9Sr",
                        _crossorigin="anonymous",
                    ),
                ),
            ),
        )

    def test_evaluate(self):
        # headings = self.page.evaluate("/html/body//h2", self.page)  #, None, XPathResult.ANY_TYPE, None);
        headings = self.page.evaluate("//h1", self.page)  # , None, XPathResult.ANY_TYPE, None);
        assert len(headings) == 1, f'"{len(headings)}" != "{1}"'

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
        self.assertEqual(list(somelist.values()), [kid1, kid2, kid3])
        self.assertEqual(list(somelist.keys()), [0, 1, 2])
        self.assertEqual(list(somelist.entries()), [(0, kid1), (1, kid2), (2, kid3)])

        seen = []
        somelist.forEach(lambda currentValue, currentIndex, listObj, **kwargs: seen.append((currentValue, currentIndex, listObj)))
        self.assertEqual(seen, [(kid1, 0, somelist), (kid2, 1, somelist), (kid3, 2, somelist)])

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
        self.assertEqual(True, str(myobj) == '<div class="mytest" style="float:left;"></div>')

        # print("NOW>>>>")
        mylist = li() / 10
        assert (
            str(mylist) == "<li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li>"
        )

        myobj = domonic.load(mylist)
        self.assertEqual(len(myobj), 10)

        myorderedlist = ol()
        myorderedlist += str(li() / 10)
        assert (
            str(myorderedlist)
            == "<ol><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li></ol>"
        )

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
        somenewdiv = div("im new")
        sometag.appendChild(somenewdiv)

        assert (
            str(somenewdiv.parentNode)
            == '<div id="test" thingy="test22">asdfasdf<div></div><div>yo</div><div>im new</div></div>'
        )
        assert isinstance(somenewdiv.parentNode, div)
        assert somenewdiv.parentNode.id == "test"
        # print(somenewdiv.parentElement)
        # print(somenewdiv.previousSibling)
        assert str(somenewdiv.previousSibling.nextSibling) == "<div>im new</div>"

        mylist = ul(li(1), li(2), li(3))
        assert str(mylist[1]) == "<li>2</li>"

        mylist = ul(li(), li(), li())
        # print(*mylist)
        assert str(mylist) == "<ul><li></li><li></li><li></li></ul>"

        a1, b1, c1 = ul(li(1), li(2), li(3))
        # print(a1)
        assert str(a1) == "<li>1</li>"

        a1, b1, c1, d1, e1 = button() * 5
        # print(a1, b1, c1, d1, e1)
        assert str(a1) == "<button></button>"
        assert str(b1) == "<button></button>"
        assert str(c1) == "<button></button>"
        assert str(d1) == "<button></button>"
        assert str(e1) == "<button></button>"

        # print(mylist[1] != mylist[1])
        a1 = img()
        a1 >> {"_src": "http://www.someurl.com"}
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

        assert sometag.id == "test"
        # print(sometag.style.color)  # TODO - get on style
        assert sometag._thingy == "test22"
        assert sometag.thingy == "test22"

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
        self.assertEqual(sometag.tagName, "div")
        self.assertEqual(str(sometag), '<div id="someid">asdfasdf<div></div><div>yo</div></div>')
        sometag.html("test")
        self.assertEqual(str(sometag), '<div id="someid">test</div>')
        sometag.innerHTML = "test2"
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
        self.assertEqual(sometag.getAttribute("_id"), "someid")
        # print(sometag.getAttribute('id'))
        # self.assertEqual(sometag.getAttribute('_id'), 'someid')

        mydiv = div("I like cake", div(_class="myclass").html(div("1"), div("2"), div("3")))
        # print(mydiv)
        assert str(mydiv) == '<div>I like cake<div class="myclass"><div>1</div><div>2</div><div>3</div></div></div>'

        self.assertEqual(sometag.innerText(), "test2")
        sometag.textContent = ""

        # return
        # print(sometag.nodeName)
        # assert(sometag.nodeName, 'DIV') # TODO - i checked one site in chrome, was upper case. not sure if a standard?

        sometag.setAttribute("id", "newid")
        assert sometag.getAttribute("id") == "newid"
        assert str(sometag) == '<div id="newid"></div>'
        assert sometag.lastChild == sometag.firstChild
        assert sometag.hasChildNodes() == False

        sometag.removeAttribute("id")
        assert str(sometag) == "<div></div>"

        sometag.appendChild(footer("test"))
        assert str(sometag) == "<div><footer>test</footer></div>"

        assert sometag.children[0].tagName == "footer"
        assert str(sometag.children[0]) == "<footer>test</footer>"

        # print(sometag.firstChild)
        assert str(sometag.firstChild) == "<footer>test</footer>"

        htmltag = html()
        assert htmltag.tagName == "html"
        assert str(htmltag) == "<html></html>"
        htmltag.write("sup!")
        # print("?????", htmltag)
        assert str(htmltag) == "<html>sup!</html>"
        htmltag.className = "my_cool_css"
        # print(htmltag)
        assert str(htmltag) == '<html class="my_cool_css">sup!</html>'
        # print(htmltag)
        # print('-END-')

    def test_create(self):
        # print(html().documentElement)
        # print(html().URL)
        somebody = document.createElement("sometag")
        # print(str(somebody))
        assert str(somebody) == "<sometag></sometag>"
        comm = document.createComment("hi there here is a comment")
        # print(comm)
        assert str(comm) == "<!--hi there here is a comment-->"

        # print(html().createElement('sometag'))
        # somebody = document.createElement('sometag')
        # print(str(somebody()))
        assert str(somebody) == "<sometag></sometag>"

    def test_events(self):
        # print(html().documentElement)
        # print(html().URL)
        site = html()
        somebody = document.createElement("div")
        site.appendChild(somebody)
        # print(site)
        assert str(site) == "<html><div></div></html>"

        def test(evt, *args, **kwargs):
            # print('test ran!')
            # print(evt)
            # print(evt.target)
            assert evt.target == somebody or evt.target == site

        site.addEventListener("click", test)
        somebody.addEventListener("anything", test)
        # print(site.listeners)
        assert site.listeners["click"] == [test]
        # site.removeEventListener('click', test)
        # print( site.listeners )

        site.dispatchEvent(Event("click"))
        somebody.dispatchEvent(Event("anything"))

        # document.getElementById("myBtn").addEventListener("click", function(){
        #   document.getElementById("demo").innerHTML = "Hello World";
        # });

    def test_contains(self):
        site = html()
        somebody = document.createElement("div")
        site.appendChild(somebody)
        # print(site)
        assert str(site) == "<html><div></div></html>"
        another_div = div()
        # print(site.contains(somebody))
        assert site.contains(somebody)
        another_div = div()
        # print(site.contains(another_div))
        assert not site.contains(another_div)
        another_div = document.createElement("div")
        # print(site.contains(another_div))
        assert not site.contains(another_div)
        third_div = document.createElement("div")
        another_div.appendChild(third_div)
        assert another_div.contains(third_div)
        assert not site.contains(document.createElement("div"))
        site.appendChild(another_div)
        assert site.contains(third_div)
        # print(site.contains(third_div))
        assert site.contains(another_div)

    def test_getElementById(self):
        dom1 = html(div(div(div(div(div(div(div(article("asdfasdf", div(), div("yo"), _id="test")))))))))
        result = dom1.getElementById("test")
        assert result.tagName == "article"
        # print(result)
        # print(len(result.children))
        # assert len(result.children) == 3  # TODO - does a text node count?

    def test_remove(self):
        dom1 = html(div(div(div(div(div(div(div(div("asdfasdf", div(), div("yo"), _id="test")))))))))
        result = dom1.getElementById("test")
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
        assert str(wrapper) == "<div>Part 1 Part 2 Part 3</div>"
        pass

    # def test_Node():
    # TODO - tests all below
    # contains - probably need more recursive testing
    # replaceChild
    # anchors

    def test_querySelector(self):
        dom1 = html(
            div(
                div(
                    div(
                        div(
                            div(
                                div(
                                    div(
                                        div(_id="thing"),
                                        span(_id="fun"),
                                        div("asdfasdf", div(), div("yo"), _class="test this thing"),
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

        result = dom1.querySelector("#thing")
        # print('--')
        # print("RESULT>>>>>", result)
        # print('--')
        assert result.id == "thing"

        result = dom1.querySelector("span")
        # print('--')
        # print("RESULT>>>>>", result)
        assert result.id == "fun"

        result = dom1.querySelector(".test")
        # print('--')
        # print("RESULT>>>>>", result)
        assert result.className == "test this thing"

        result = dom1.getElementsByClassName("this")
        # print('--')
        # print("RESULT>>>>>", result)
        assert len(result) == 1
        assert result[0].className == "test this thing"

        links = self.page.querySelectorAll("a[rel=nofollow]")
        # for linky in links:
        #     print(linky.getAttribute("href"))
        assert len(links) == 1

        result = self.page.querySelectorAll("li[class='nav-item']")
        expected = ["About", "Services", "Team", "Contact"]
        for i, r in enumerate(result):
            assert r.textContent == expected[i]
        assert len(result) == 4

        result = self.page.querySelectorAll("h4[class='font-weight-bold text-uppercase']")
        # for r in result:
        #     print(r)
        assert len(result) == 1

        result = self.page.querySelectorAll("li.nav-item")
        # print(result)
        # for r in result:
        #     print(r)
        assert len(result) == 5

        result = self.page.querySelectorAll("a[href='#services']")
        self.assertEqual(len(result), 1)

        result = self.page.querySelectorAll("p.text-gray")
        # print(result)
        # for r in result:
        #     print(r)
        assert len(result) == 5

        result = self.page.querySelectorAll("a[href$='technology']")
        self.assertEqual(len(result), 1)

        result = self.page.querySelectorAll("a[href*='twitter']")
        self.assertEqual(len(result), 1)

        result = dom1.querySelectorAll(".fa-twitter")
        self.assertEqual(result, [])
        # TODO - failing. however this is now running through qselectorall
        # return
        # assert result.className == 'test this thing'

    def test_getElementsBySelector(self):
        dom1 = html(
            div(
                div(
                    div(
                        div(
                            div(
                                div(
                                    div(
                                        div(_id="thing"),
                                        span(_id="fun"),
                                        div("asdfasdf", div(), div("yo"), _class="test this thing"),
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )

        result = dom1.getElementsBySelector("#thing", dom1)[0]
        # print("RESULT>>>>>", result)
        # print('--')
        # return
        assert result.id == "thing"

        result = dom1.getElementsBySelector("span", dom1)[0]
        # print('--')
        # print("RESULT>>>>>", result)
        assert result.id == "fun"

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
        self.assertEqual(len(links), 1)

        result = self.page.getElementsBySelector("li[class='nav-item']", self.page)
        self.assertEqual(len(result), 4)

        result = self.page.getElementsBySelector("h4[class='font-weight-bold text-uppercase']", self.page)
        self.assertEqual(len(result), 1)

        result = self.page.getElementsBySelector("li.nav-item", self.page)
        self.assertEqual(len(result), 5)

        result = self.page.getElementsBySelector("a[href='#services']", self.page)
        self.assertEqual(len(result), 1)

        result = self.page.getElementsBySelector("p.text-gray", self.page)
        self.assertEqual(len(result), 5)

        result = self.page.getElementsBySelector("a[href$='technology']", self.page)
        self.assertEqual(len(result), 1)

        result = self.page.getElementsBySelector("a[href*='twitter']", self.page)
        self.assertEqual(len(result), 1)

    def test_decorators(self):
        from domonic.decorators import el

        @el(html)
        @el(body)
        @el(div)
        def test():
            return "hi!"

        # print(test())
        assert str(test()) == "<html><body><div>hi!</div></body></html>"
        # print('decorators work!')

        @el(html, True)
        @el(body, True)
        @el(div, True)
        def test():
            return "hi!"

        assert test() == "<html><body><div>hi!</div></body></html>"
        # print('decorators work2!')

        @el("html")
        @el("body")
        @el("div")
        def test():
            return "hi!"

        # print(test())
        assert str(test()) == "<html><body><div>hi!</div></body></html>"
        # print('decorators work3!')

        @el(html, True)
        @el(body)
        @el("div")
        def test():
            return "hi!"

        assert str(test()) == "<html><body><div>hi!</div></body></html>"

    def test_domonic_window_console_log(self):
        # note originally dom had everything from document
        # this will likely move later versions

        # window = Window()
        pass

    def test_element_geometry_helpers(self):
        el = div("x")
        el.style.width = "100px"
        el.style.height = "50px"
        el.style.paddingLeft = 5
        el.style.paddingRight = 5
        el.style.paddingTop = 2
        el.style.paddingBottom = 3
        el.style.borderLeftWidth = 1
        el.style.borderRightWidth = 1
        el.style.borderTopWidth = 4
        el.style.borderBottomWidth = 4
        el.style.left = "12px"
        el.style.top = "8px"

        self.assertEqual(el.clientWidth, 110)
        self.assertEqual(el.clientHeight, 55)
        self.assertEqual(el.offsetWidth(), 112)
        self.assertEqual(el.offsetHeight(), 63)
        self.assertEqual(el.offsetLeft(), 12)
        self.assertEqual(el.offsetTop(), 8)

        rect = el.getBoundingClientRect()
        self.assertEqual(rect.left, 12)
        self.assertEqual(rect.top, 8)
        self.assertEqual(rect.width, 112)
        self.assertEqual(rect.height, 63)

    def test_element_scroll_helpers(self):
        el = div("x")
        el.style.width = "20px"
        el.style.height = "10px"
        self.assertEqual(el.scrollWidth(), 20)
        self.assertEqual(el.scrollHeight(), 10)
        self.assertEqual(el.scrollLeft(), 0)
        self.assertEqual(el.scrollTop(), 0)

    def test_element_focus_blur(self):
        el = input(_type="text")
        focus_calls = []
        blur_calls = []
        el.addEventListener("focus", lambda e: focus_calls.append(e.type))
        el.addEventListener("blur", lambda e: blur_calls.append(e.type))
        el.focus()
        el.blur()
        self.assertEqual(focus_calls, ["focus"])
        self.assertEqual(blur_calls, ["blur"])

    def test_focus_event_related_targets_and_bubbling_helpers(self):
        page = html(body(input(_type="text", _id="first"), input(_type="text", _id="second")))
        body_focus_events = []
        body_blur_events = []
        first = page.querySelector("#first")
        second = page.querySelector("#second")

        page.body.addEventListener("focusin", lambda e: body_focus_events.append((e.type, e.relatedTarget)))
        page.body.addEventListener("focusout", lambda e: body_blur_events.append((e.type, e.relatedTarget)))

        first.focus()
        second.focus()
        second.blur()

        self.assertEqual(body_focus_events[0][0], "focusin")
        self.assertIsNone(body_focus_events[0][1])
        self.assertIs(body_focus_events[1][1], first)
        self.assertIs(body_blur_events[0][1], second)

    def test_document_focus_tracking(self):
        page = html(body(input(_type="text", _id="first"), button("go", _id="second")))
        first = page.querySelector("#first")
        second = page.querySelector("#second")

        self.assertIs(page.activeElement, page.body)
        self.assertFalse(page.hasFocus())

        events = []
        first.addEventListener("focus", lambda e: events.append(("first", e.type)))
        first.addEventListener("blur", lambda e: events.append(("first", e.type)))
        second.addEventListener("focus", lambda e: events.append(("second", e.type)))

        first.focus()
        self.assertIs(page.activeElement, first)
        self.assertTrue(page.hasFocus())

        second.focus()
        self.assertIs(page.activeElement, second)
        self.assertFalse(getattr(first, "_focused", False))
        self.assertTrue(getattr(second, "_focused", False))

        second.blur()
        self.assertIs(page.activeElement, page.body)
        self.assertFalse(page.hasFocus())

        self.assertEqual(events, [("first", "focus"), ("first", "blur"), ("second", "focus")])

    def test_domimplementation_create_html_document(self):
        impl = DOMImplementation()
        doc = impl.createHTMLDocument("hello")
        self.assertEqual(doc.querySelector("title").textContent, "hello")
        self.assertEqual(doc.body.tagName, "body")
        self.assertTrue(impl.hasFeatures(None))

    def test_domimplementation_create_document_and_doctype(self):
        impl = DOMImplementation()
        doctype = impl.createDocumentType("html", "", "")
        doc = impl.createDocument("http://www.w3.org/1999/xhtml", "html", doctype)

        self.assertEqual(str(doc.doctype), "<!DOCTYPE html>")
        self.assertEqual(doc.nodeType, Node.DOCUMENT_NODE)
        self.assertEqual(str(doctype), "<!DOCTYPE html>")

    def test_document_import_node_variants(self):
        page = html(body())
        imported_element = page.importNode(div(span("x"), _id="one"), deep=True)
        imported_comment = page.importNode(Comment("note"))
        imported_text = page.importNode(Text("hello"))
        imported_instruction = page.importNode(ProcessingInstruction("xml-stylesheet", 'href="style.css"'))
        imported_fragment = page.importNode(DocumentFragment())
        imported_attr = page.importNode(Attr("data-id", "7"))

        self.assertEqual(str(imported_element), '<div id="one"><span>x</span></div>')
        self.assertIs(imported_element.ownerDocument, page)
        self.assertEqual(str(imported_comment), "<!--note-->")
        self.assertEqual(str(imported_text), "hello")
        self.assertEqual(str(imported_instruction), '<?xml-stylesheet href="style.css"?>')
        self.assertIsInstance(imported_fragment, DocumentFragment)
        self.assertEqual((imported_attr.name, imported_attr.value), ("data-id", "7"))

    def test_document_elements_from_point(self):
        one = div("one", _id="one")
        one.style.left = "0px"
        one.style.top = "0px"
        one.style.width = "50px"
        one.style.height = "50px"
        two = div("two", _id="two")
        two.style.left = "10px"
        two.style.top = "10px"
        two.style.width = "20px"
        two.style.height = "20px"
        page = html(body(one, two))
        hits = page.elementsFromPoint(15, 15)
        self.assertTrue(any(hit.getAttribute("id") == "one" for hit in hits))
        self.assertTrue(any(hit.getAttribute("id") == "two" for hit in hits))
        self.assertEqual(page.elementFromPoint(15, 15).getAttribute("id"), "one")

    def test_range_basic_operations(self):
        container = div(span("a"), span("b"), span("c"))
        r = Range()
        r.setStart(container, 1)
        r.setEnd(container, 3)
        self.assertEqual(r.toString(), "<span>b</span><span>c</span>")

        clone = r.cloneContents()
        self.assertEqual(str(clone), "<span>b</span><span>c</span>")

        extracted = r.extractContents()
        self.assertEqual(str(extracted), "<span>b</span><span>c</span>")
        self.assertEqual(str(container), "<div><span>a</span></div>")

        fragment = r.createContextualFragment("<em>x</em>")
        self.assertEqual(str(fragment), "<em>x</em>")

    def test_range_text_and_compare_helpers(self):
        text = Text("abcdef")
        host = p(text)
        host.style.left = "10px"
        host.style.top = "20px"
        host.style.width = "80px"
        host.style.height = "10px"

        r = Range()
        r.setStart(text, 1)
        r.setEnd(text, 4)
        self.assertEqual(r.toString(), "bcd")
        self.assertEqual(r.comparePoint(text, 0), -1)
        self.assertEqual(r.comparePoint(text, 2), 0)
        self.assertEqual(r.comparePoint(text, 5), 1)
        self.assertEqual(len(r.getClientRects()), 1)
        self.assertEqual(r.getBoundingClientRect().left, 10)

        extracted = r.extractContents()
        self.assertEqual(str(extracted), "bcd")
        self.assertEqual(text.textContent, "aef")

        r2 = Range()
        r2.selectNodeContents(text)
        self.assertEqual(r2.toString(), "aef")

    def test_range_cross_container_helpers(self):
        container = div(span("a", _id="first"), span("b", _id="second"), span("c", _id="third"))
        first = container.querySelector("#first")
        third = container.querySelector("#third")

        r = Range()
        r.setStartBefore(first)
        r.setEndAfter(third)

        self.assertEqual(r.toString(), '<span id="first">a</span><span id="second">b</span><span id="third">c</span>')
        self.assertEqual(str(r.cloneContents()), str(r.extractContents()))
        self.assertEqual(str(container), "<div></div>")

    def test_range_intersects_and_invalid_compare_type(self):
        container = div(span("a", _id="first"), span("b", _id="second"), span("c", _id="third"))
        first = container.querySelector("#first")
        second = container.querySelector("#second")
        third = container.querySelector("#third")

        r = Range()
        r.setStartBefore(first)
        r.setEndAfter(second)

        self.assertTrue(r.intersectsNode(first))
        self.assertTrue(r.intersectsNode(second))
        self.assertFalse(r.intersectsNode(third))

        with self.assertRaises(ValueError):
            r.compareBoundaryPoints(99, Range())

    def test_range_data_helpers_and_static_range(self):
        text = Text("abcdef")
        host = div(text)
        r = Range()
        r.setStart(text, 1)
        r.setEnd(text, 4)

        self.assertEqual(r.getStart(), (text, 1))
        self.assertEqual(r.getEnd(), (text, 4))
        self.assertEqual(r.getData(1, 3), "bcd")
        self.assertEqual(r.extractData(2, 2), "cd")
        self.assertEqual(text.textContent, "abef")

        r.replaceData(1, 2, "ZZ")
        self.assertEqual(text.textContent, "aZZf")
        r.setData("hello")
        self.assertEqual(text.textContent, "hello")

        r.setStart(text, 1)
        r.setEnd(text, 1)
        r.expand("character")
        self.assertEqual(r.toString(), "e")
        self.assertTrue(r.isPointInRange(text, 1))

        static = StaticRange(text, 0, text, 5)
        self.assertEqual(static.toString(), "hello")
        self.assertEqual(static.toRange().toString(), "hello")
        with self.assertRaises(TypeError):
            static.setStart(text, 1)

    def test_document_and_shadow_selection_helpers(self):
        host = div(_id="host")
        page = html(body(host))
        shadow = host.attachShadow({"mode": "open"})
        shadow_button = button("go", _id="shadow-button")
        shadow_button.style.left = "0px"
        shadow_button.style.top = "0px"
        shadow_button.style.width = "40px"
        shadow_button.style.height = "20px"
        shadow.appendChild(shadow_button)

        doc_selection = page.getSelection()
        shadow_selection = shadow.getSelection()
        self.assertEqual(doc_selection.rangeCount, 0)
        self.assertEqual(shadow_selection.rangeCount, 0)

        r = Range()
        r.selectNode(shadow_button)
        shadow_selection.addRange(r)
        self.assertEqual(shadow_selection.rangeCount, 1)
        self.assertEqual(
            shadow_selection.getRangeAt(0).toString(),
            '<button id="shadow-button" style="left:0px;top:0px;width:40px;height:20px;">go</button>',
        )

        self.assertEqual(shadow.elementFromPoint(5, 5), shadow_button)
        self.assertEqual(shadow.caretPositionFromPoint(5, 5).offset, 0)

    def test_document_normalize_and_stream_writes(self):
        page = html()
        page.args = (Text("alpha"), Text(""), Text("beta"),)
        for child in page.args:
            child.parentNode = page

        page.normalizeDocument()
        self.assertEqual(len(page.childNodes), 1)
        self.assertEqual(page.textContent, "alphabeta")

        fd, path = tempfile.mkstemp(prefix="domonic_doc_", suffix=".html")
        os.close(fd)
        os.remove(path)
        try:
            page.open(path)
            page.write("<p>one</p>")
            self.assertEqual(str(page), "<html><p>one</p></html>")
            page.writeln("<p>two</p>")
            self.assertEqual(str(page), "<html><p>two</p>\n</html>")

            with open(path, "r", encoding="utf-8") as handle:
                self.assertEqual(handle.read(), "<p>one</p><p>two</p>\n")
        finally:
            if os.path.exists(path):
                os.remove(path)

    def test_selection_core_helpers(self):
        first = Text("hello")
        second = Text("world")
        host = div(first, second)

        selection = Selection()
        self.assertEqual(selection.type, "None")
        self.assertTrue(selection.isCollapsed)

        selection.selectAllChildren(host)
        self.assertEqual(selection.type, "Range")
        self.assertEqual(selection.anchorNode, host)
        self.assertEqual(selection.anchorOffset, 0)
        self.assertEqual(selection.focusNode, host)
        self.assertEqual(selection.focusOffset, 2)
        self.assertTrue(selection.containsNode(first))
        self.assertTrue(selection.containsNode(second, allowPartialContainment=True))

        selection.collapse(first, 2)
        self.assertEqual(selection.type, "Caret")
        self.assertTrue(selection.isCollapsed)
        self.assertEqual(selection.anchorNode, first)
        self.assertEqual(selection.anchorOffset, 2)

        selection.extend(second, 3)
        self.assertEqual(selection.type, "Range")
        self.assertEqual(selection.focusNode, second)
        self.assertEqual(selection.focusOffset, 3)

        selection.collapseToEnd()
        self.assertEqual(selection.focusOffset, 3)

        selection.setBaseAndExtent(second, 1, first, 1)
        self.assertEqual(selection.anchorNode, first)
        self.assertEqual(selection.focusNode, second)

        selection.deleteFromDocument()
        self.assertEqual(first.textContent, "hello")
        self.assertEqual(selection.rangeCount, 0)

        selection.selectAllChildren(host)
        selection.collapseToStart()
        self.assertEqual(selection.anchorNode, host)
        self.assertEqual(selection.anchorOffset, 0)

        selection.empty()
        self.assertEqual(selection.rangeCount, 0)

        with self.assertRaises(IndexError):
            selection.getRangeAt(0)

    def test_document_caret_position_from_point(self):
        target = div("hello", _id="target")
        target.style.left = "5px"
        target.style.top = "5px"
        target.style.width = "30px"
        target.style.height = "10px"
        page = html(body(target))

        caret = page.caretPositionFromPoint(10, 10)
        self.assertIsNotNone(caret)
        self.assertGreaterEqual(caret.offset, 0)
        self.assertLessEqual(caret.offset, len("hello"))
        self.assertIn(caret.offsetNode, [target, target.firstChild])

    def test_document_domain_and_event_factory_helpers(self):
        page = html(body(div("x")))
        page.URL = "https://example.com/path?q=1"

        self.assertEqual(page.domain(), "example.com")
        expected_types = {
            "FocusEvent": "focus",
            "InputEvent": "input",
            "ClipboardEvent": "copy",
            "MouseEvent": "click",
            "KeyboardEvent": "keydown",
            "SubmitEvent": "submit",
        }
        for event_name, expected_type in expected_types.items():
            with self.subTest(event_name=event_name):
                self.assertEqual(page.createEvent(event_name).type, expected_type)

    def test_insert_adjacent_element_positions(self):
        host = div(span("target", _id="target"), p("sibling", _id="sibling"))
        target = host.querySelector("#target")

        before = em("before", _id="before")
        returned = target.insertAdjacentElement("beforebegin", before)
        self.assertIs(returned, before)
        self.assertEqual([child.getAttribute("id") for child in host.children], ["before", "target", "sibling"])

        after_begin = strong("start", _id="start")
        target.insertAdjacentElement("AFTERBEGIN", after_begin)
        self.assertEqual(target.children[0].getAttribute("id"), "start")

        before_end = i("end", _id="end")
        target.insertAdjacentElement("beforeend", before_end)
        self.assertEqual(target.children[-1].getAttribute("id"), "end")

        after = b("after", _id="after")
        target.insertAdjacentElement("AfterEnd", after)
        self.assertEqual([child.getAttribute("id") for child in host.children], ["before", "target", "after", "sibling"])

    def test_insert_adjacent_html_and_text(self):
        host = div(span("target", _id="target"), p("sibling", _id="sibling"))
        target = host.querySelector("#target")

        target.insertAdjacentHTML("beforebegin", "<em id='before'></em>")
        target.insertAdjacentHTML("afterbegin", "<strong id='start'></strong>")
        target.insertAdjacentHTML("beforeend", "<i id='end'></i>")
        target.insertAdjacentHTML("afterend", "<b id='after'></b>")
        target.insertAdjacentText("afterbegin", "prefix-")
        target.insertAdjacentText("beforeend", "-suffix")

        self.assertEqual([child.getAttribute("id") for child in host.children], ["before", "target", "after", "sibling"])
        self.assertEqual(target.children[0].getAttribute("id"), "start")
        self.assertEqual(target.children[-1].getAttribute("id"), "end")
        self.assertEqual(str(target), '<span id="target">prefix-<strong id="start"></strong>target<i id="end"></i>-suffix</span>')
        self.assertEqual(host.querySelector("#before").tagName, "em")
        self.assertEqual(host.querySelector("#after").tagName, "b")

    def test_insert_adjacent_invalid_position(self):
        target = span("target")
        with self.assertRaises(ValueError):
            target.insertAdjacentText("middle", "x")

    def test_node_iterator_next_node(self):
        page = html(body(div(span("a"), p("b"), _id="root")))
        iterator = page.createNodeIterator(page.body)
        seen = []
        node = iterator.nextNode()
        while node is not None:
            seen.append(getattr(node, "tagName", getattr(node, "nodeName", "")))
            node = iterator.nextNode()
        self.assertIn("body", seen)
        self.assertIn("div", seen)
        self.assertIn("span", seen)
        self.assertIn("p", seen)

    def test_document_get_elements_by_name(self):
        page = html(
            body(
                input(_type="text", _name="email"),
                form(
                    input(_type="text", _name="email"),
                    input(_type="text", _name="username"),
                ),
            )
        )

        matches = page.getElementsByName("email")
        self.assertEqual(len(matches), 2)
        self.assertTrue(all(match.getAttribute("name") == "email" for match in matches))

    def test_attribute_namespace_helpers(self):
        node = div()
        attr = Attr("data-mode", "test")

        self.assertIs(node.setAttributeNodeNS(attr), node)
        fetched = node.getAttributeNodeNS("data-mode")
        self.assertIsNotNone(fetched)
        self.assertEqual((fetched.name, fetched.value), ("data-mode", "test"))
        self.assertEqual(node.getAttributeNS("http://example.com/ns", "data-mode"), "test")
        node.setAttributeNS("http://example.com/ns", "data-other", "x")
        self.assertEqual(node.getAttribute("data-other"), "x")

    def test_dataset_and_dom_string_map_helpers(self):
        node = div(**{"_data-user-id": "7", "_data-theme-name": "night"})
        dataset = node.dataset

        self.assertEqual(dataset.get("userId"), "7")
        self.assertEqual(dataset["themeName"], "night")
        self.assertIn("userId", dataset)

        self.assertTrue(dataset.set("mode", "demo"))
        self.assertEqual(dataset.get("mode"), "demo")
        self.assertEqual(sorted(dataset.items()), [("mode", "demo"), ("themeName", "night"), ("userId", "7")])
        self.assertTrue(dataset.delete("mode"))
        self.assertFalse(dataset.delete("missing"))
        self.assertEqual(dataset.get("mode"), None)

    def test_node_operator_helpers(self):
        node = div(span("a"), _id="root")
        sibling = div("b")

        self.assertEqual(node["id"], "root")
        self.assertEqual(node[0].tagName, "span")

        clones = node * 2
        self.assertEqual(len(clones), 2)
        self.assertTrue(all(isinstance(clone, type(node)) for clone in clones))
        self.assertIsNot(clones[0], node)
        self.assertEqual([str(clone) for clone in 2 * node], [str(clone) for clone in clones])
        self.assertEqual(node / 2, '<div id="root"><span>a</span></div><div id="root"><span>a</span></div>')

        node += sibling
        self.assertIs(sibling.parentNode, node)
        self.assertEqual(len(node.args), 2)
        node -= sibling
        self.assertEqual(len(node.args), 1)

        updated = node >> {"_class": "hero", "_data-role": "banner"}
        self.assertIs(updated, node)
        self.assertEqual(node.getAttribute("class"), "hero")
        self.assertEqual(node.getAttribute("data-role"), "banner")
        self.assertIs(node | False, node)
        self.assertEqual(node | "fallback", "fallback")
        self.assertEqual(node.__div__(2), str(node) * 2)
        self.assertEqual(node.__rdiv__(2), str(node) * 2)
        self.assertEqual(node.__rtruediv__(2), str(node) * 2)
        self.assertIs(node.__setitem__("_title", "banner"), node)
        self.assertEqual(node.getAttribute("title"), "banner")

    def test_node_attribute_rendering_configurations(self):
        button_node = button("Go", _disabled="", _data_value="7", _get="/api/items")
        original_quotes = DOMConfig.ATTRIBUTE_QUOTES
        original_htmx = DOMConfig.HTMX_ENABLED
        try:
            DOMConfig.ATTRIBUTE_QUOTES = '"'
            DOMConfig.HTMX_ENABLED = False
            rendered = button_node.__attributes__
            self.assertIn(" disabled", rendered)
            self.assertIn(' data_value="7"', rendered)
            self.assertIn(' get="/api/items"', rendered)

            DOMConfig.ATTRIBUTE_QUOTES = ""
            self.assertIn(" data_value=7", button_node.__attributes__)

            DOMConfig.HTMX_ENABLED = True
            htmx_rendered = button_node.__attributes__
            self.assertIn(" data-hx-get=", htmx_rendered)
        finally:
            DOMConfig.ATTRIBUTE_QUOTES = original_quotes
            DOMConfig.HTMX_ENABLED = original_htmx

    def test_node_autoescape_and_pyml_helpers(self):
        node = div(Text("<unsafe>"), span(Text("ok")), _data_label="x", **{"data-mode": "demo"})
        original_autoescape = DOMConfig.GLOBAL_AUTOESCAPE
        try:
            DOMConfig.GLOBAL_AUTOESCAPE = True
            self.assertIn("&lt;unsafe&gt;", node.content)
        finally:
            DOMConfig.GLOBAL_AUTOESCAPE = original_autoescape

        pyml = node.__pyml__()
        self.assertIn('div(_data_label="x"', pyml)
        self.assertIn('**{"_data-mode":demo}', pyml)
        self.assertIn('"<unsafe>"', pyml)
        self.assertIn('span("ok")', pyml)

    def test_context_manager_and_format_helpers(self):
        with div(_id="outer") as outer:
            span("child")

        self.assertEqual(len(outer.args), 1)
        self.assertEqual(outer.firstChild.tagName, "span")

        original_optional = DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS
        try:
            DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS = True
            formatted = format(outer, "")
            self.assertIn('<div id="outer">', formatted)
            self.assertIn("<span>child</span>", formatted)
        finally:
            DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS = original_optional

    def test_format_helpers_for_closed_and_optional_tags(self):
        original_optional = DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS
        original_autoescape = DOMConfig.GLOBAL_AUTOESCAPE
        try:
            DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS = False
            DOMConfig.GLOBAL_AUTOESCAPE = True
            self.assertEqual(format(li("item"), ""), "\n<li>item")
            self.assertEqual(format(br(), ""), "\n<br />")
            self.assertIn("&lt;safe&gt;", format(div("<safe>"), ""))
        finally:
            DOMConfig.RENDER_OPTIONAL_CLOSING_TAGS = original_optional
            DOMConfig.GLOBAL_AUTOESCAPE = original_autoescape

    def test_document_value_type_helpers(self):
        instruction = ProcessingInstruction("xml-stylesheet", 'href="style.css"')
        comment = Comment("hello")
        cdata = CDATASection("<tag/>")
        entity = EntityReference("&amp;")

        self.assertEqual(str(instruction), '<?xml-stylesheet href="style.css"?>')
        self.assertEqual(str(comment), "<!--hello-->")
        self.assertEqual(str(cdata), "<![CDATA[<tag/>]]>")
        self.assertEqual(comment.length, 5)
        self.assertEqual(cdata.length, 6)
        self.assertEqual(str(entity), "&amp;")
        self.assertEqual(EntityReference.fromOrdinal(38), "&")

    def test_dom_html_element_constructor_helpers(self):
        cases = [
            (HTMLAnchorElement, {"href": "/home", "target": "_blank", "rel": "noopener", "download": "file.txt", "type": "text/html"}, {"href": "/home", "target": "_blank", "rel": "noopener", "download": "file.txt", "type": "text/html"}),
            (HTMLAreaElement, {"href": "/map", "target": "_self", "alt": "Map", "coords": "0,0,10,10", "shape": "rect"}, {"href": "/map", "target": "_self", "alt": "Map", "coords": "0,0,10,10", "shape": "rect"}),
            (HTMLAudioElement, {"autoplay": True, "controls": True, "loop": True, "muted": True, "preload": "auto", "src": "/song.mp3"}, {"autoplay": True, "controls": True, "loop": True, "muted": True, "preload": "auto", "src": "/song.mp3"}),
            (HTMLBaseElement, {"href": "https://example.com", "target": "_top"}, {"href": "https://example.com", "target": "_top"}),
            (HTMLBodyElement, {"aLink": "red", "background": "/bg.png", "bgColor": "#fff", "link": "blue", "onload": "init()", "onunload": "bye()", "text": "black", "vLink": "purple"}, {"aLink": "red", "background": "/bg.png", "bgColor": "#fff", "link": "blue", "onload": "init()", "onunload": "bye()", "text": "black", "vLink": "purple"}),
            (HTMLButtonElement, {"disabled": True, "form": "signup", "formaction": "/submit", "formenctype": "multipart/form-data", "formmethod": "post", "formnovalidate": True, "formtarget": "_blank", "name": "go", "type": "submit", "value": "Send"}, {"disabled": True, "form": "signup", "formaction": "/submit", "formenctype": "multipart/form-data", "formmethod": "post", "formnovalidate": True, "formtarget": "_blank", "name": "go", "type": "submit", "value": "Send"}),
            (HTMLCanvasElement, {"width": 320, "height": 240}, {"width": 320, "height": 240}),
            (HTMLDataElement, {"value": "42"}, {"value": "42"}),
            (HTMLDialogElement, {"open": True}, {"open": True}),
            (HTMLFormElement, {"action": "/submit", "autocomplete": "on", "enctype": "multipart/form-data", "method": "post", "name": "signup", "novalidate": True, "target": "_blank"}, {"action": "/submit", "autocomplete": "on", "enctype": "multipart/form-data", "method": "post", "name": "signup", "novalidate": True, "target": "_blank"}),
            (HTMLIFrameElement, {"src": "/frame", "name": "hero", "sandbox": "allow-scripts", "allowfullscreen": True}, {"src": "/frame", "name": "hero", "sandbox": "allow-scripts", "allowfullscreen": True}),
            (HTMLImageElement, {"alt": "hero", "src": "/hero.png", "crossorigin": "anonymous", "height": "100", "ismap": True, "longdesc": "/desc", "sizes": "100vw", "srcset": "/hero.png 1x", "usemap": "#hero", "width": "200"}, {"alt": "hero", "src": "/hero.png", "crossorigin": "anonymous", "height": "100", "ismap": True, "longdesc": "/desc", "sizes": "100vw", "srcset": "/hero.png 1x", "usemap": "#hero", "width": "200"}),
            (HTMLInputElement, {"accept": "image/*", "alt": "Upload", "autocomplete": "on", "autofocus": True, "checked": True, "dirname": "dir", "disabled": True, "form": "signup", "formaction": "/submit", "formenctype": "multipart/form-data", "formmethod": "post", "formnovalidate": True, "formtarget": "_blank", "height": "10", "maxlength": "20", "multiple": True, "name": "avatar", "pattern": ".*", "placeholder": "Upload", "readonly": True, "required": True, "size": "10", "src": "/image.png", "step": "2", "type": "file", "value": "x", "width": "30"}, {"accept": "image/*", "alt": "Upload", "autocomplete": "on", "autofocus": True, "checked": True, "dirname": "dir", "disabled": True, "form": "signup", "formaction": "/submit", "formenctype": "multipart/form-data", "formmethod": "post", "formnovalidate": True, "formtarget": "_blank", "height": "10", "maxlength": "20", "multiple": True, "name": "avatar", "pattern": ".*", "placeholder": "Upload", "readonly": True, "required": True, "size": "10", "src": "/image.png", "step": "2", "type": "file", "value": "x", "width": "30"}),
            (HTMLLinkElement, {"rel": "stylesheet", "href": "/app.css", "type": "text/css", "sizes": "32x32"}, {"rel": "stylesheet", "href": "/app.css", "type": "text/css", "sizes": "32x32"}),
            (HTMLMetaElement, {"charset": "utf-8", "content": "text/html", "http_equiv": "content-type", "name": "viewport"}, {"charset": "utf-8", "content": "text/html", "http-equiv": "content-type", "name": "viewport"}),
            (HTMLMeterElement, {"value": "5", "_min": "0", "_max": "10", "low": "2", "high": "8", "optimum": "6"}, {"value": "5", "_min": "0", "_max": "10", "low": "2", "high": "8", "optimum": "6"}),
            (HTMLOptionElement, {"disabled": True, "label": "Choice", "selected": True, "value": "1"}, {"disabled": True, "label": "Choice", "selected": True, "value": "1"}),
            (HTMLParamElement, {"name": "quality", "value": "high"}, {"name": "quality", "value": "high"}),
            (HTMLProgressElement, {"value": "30", "max": "100"}, {"value": "30", "max": "100"}),
            (HTMLQuoteElement, {"cite": "https://example.com"}, {"cite": "https://example.com"}),
            (HTMLTextAreaElement, {"autofocus": True, "cols": "40", "disabled": True, "form": "signup", "maxlength": "100", "name": "message", "placeholder": "Write", "readonly": True, "required": True, "rows": "5", "wrap": "soft"}, {"autofocus": True, "cols": "40", "disabled": True, "form": "signup", "maxlength": "100", "name": "message", "placeholder": "Write", "readonly": True, "required": True, "rows": "5", "wrap": "soft"}),
            (HTMLTimeElement, {"datetime": "2026-03-27"}, {"datetime": "2026-03-27"}),
            (HTMLTrackElement, {"kind": "subtitles", "label": "English", "src": "/captions.vtt", "srclang": "en", "default": True}, {"kind": "subtitles", "label": "English", "src": "/captions.vtt", "srclang": "en", "default": True}),
            (HTMLVideoElement, {"autoplay": True, "controls": True, "height": "720", "loop": True, "muted": True, "poster": "/poster.png", "preload": "auto", "src": "/movie.mp4", "width": "1280"}, {"autoplay": True, "controls": True, "height": "720", "loop": True, "muted": True, "poster": "/poster.png", "preload": "auto", "src": "/movie.mp4", "width": "1280"}),
        ]

        for constructor, kwargs, expected in cases:
            with self.subTest(constructor=constructor.__name__):
                element = constructor(**kwargs)
                for attr_name, attr_value in expected.items():
                    self.assertEqual(element.getAttribute(attr_name), attr_value)

    def test_br_render_modes(self):
        original_slash = DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH
        original_space = DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH
        try:
            DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH = True
            DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH = False
            self.assertEqual(str(HTMLBRElement()), "<br/>")

            DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH = True
            self.assertEqual(str(HTMLBRElement()), "<br />")

            DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH = False
            self.assertEqual(str(HTMLBRElement()), "<br >")
        finally:
            DOMConfig.RENDER_OPTIONAL_CLOSING_SLASH = original_slash
            DOMConfig.SPACE_BEFORE_OPTIONAL_CLOSING_SLASH = original_space

    def test_fullscreen_and_scroll_helpers(self):
        page = html(body(div(_id="hero"), section(_id="content")))
        hero = page.getElementById("hero")

        self.assertIsNone(page.fullscreenElement())
        self.assertEqual(hero.requestFullscreen(), hero)
        self.assertEqual(page.fullscreenElement(), hero)
        self.assertIsNone(hero.exitFullscreen())
        self.assertIsNone(page.fullscreenElement())

        self.assertEqual(hero.scrollIntoView(), hero)
        self.assertTrue(getattr(hero, "_scrolled_into_view", False))
        self.assertEqual(hero.namespaceURI, "http://www.w3.org/1999/xhtml")

    def test_treewalker_text_filter(self):
        page = html(body(div("a", span("b"), "c", _id="root")))
        root = page.getElementById("root")
        walker = page.createTreeWalker(
            root,
            NodeFilter.SHOW_TEXT,
            lambda node: NodeFilter.FILTER_ACCEPT if String(node.nodeValue).trim() != "" else NodeFilter.FILTER_REJECT,
            False,
        )
        seen = []
        node = walker.nextNode()
        while node is not None:
            seen.append(node.nodeValue)
            node = walker.nextNode()
        self.assertEqual(seen, ["a", "b", "c"])

    def test_treewalker_parent_and_sibling_helpers(self):
        page = html(body(div(span("a", _id="one"), span("b", _id="two"), span("c", _id="three"), _id="root")))
        root = page.getElementById("root")
        walker = page.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, None, False)

        self.assertEqual(walker.firstChild().getAttribute("id"), "one")
        self.assertEqual(walker.nextSibling().getAttribute("id"), "two")
        self.assertEqual(walker.previousSibling().getAttribute("id"), "one")
        self.assertIs(walker.parentNode(), root)

    def test_domquad_get_bounds(self):
        quad = DOMQuad(type("P", (), {"x": 5, "y": 10})(), type("P", (), {"x": 25, "y": 10})(), type("P", (), {"x": 25, "y": 30})(), type("P", (), {"x": 5, "y": 30})())
        rect = DOMQuad.getBounds(quad)
        self.assertEqual(rect.left, 5)
        self.assertEqual(rect.top, 10)
        self.assertEqual(rect.width, 20)
        self.assertEqual(rect.height, 20)

    def test_time_ranges(self):
        ranges = TimeRanges((0, 5), (10, 20))
        self.assertEqual(len(ranges), 2)
        self.assertEqual(ranges.start(0), 0)
        self.assertEqual(ranges.end(1), 20)

    def test_location_assign_replace_reload(self):
        loc = Location("https://example.com/one?q=1")
        self.assertEqual(str(loc), "https://example.com/one?q=1")
        self.assertIn("example.com", loc.origin())
        self.assertEqual(loc.search(), "?q=1")

        self.assertIsNone(loc.assign("https://example.com/two"))
        self.assertEqual(loc.href, "https://example.com/two")
        self.assertEqual(loc.reload(), "https://example.com/two")

        self.assertIsNone(loc.replace("https://example.com/three"))
        self.assertEqual(loc.href, "https://example.com/three")

    def test_form_submit_dispatches_submit_event(self):
        page = html(body(form(input(_name="email"), _id="signup")))
        signup = page.getElementById("signup")
        calls = []

        signup.addEventListener("submit", lambda event: calls.append((event.type, event.submitter)))
        result = signup.submit()

        self.assertTrue(result)
        self.assertEqual(calls, [("submit", None)])

    def test_domonic_matches(self):
        content = ul(_id="birds").html(
            li("Orange-winged parrot"), li("Philippine eagle", _class="endangered"), li("Great white pelican")
        )
        birds = content.getElementsByTagName("li")
        # print(type(birds))
        assert len(birds) == 3
        assert birds[1] == content.getElementsBySelector("li.endangered", content)[0]
        assert birds[1].className == "endangered"
        assert birds[1].classList == ["endangered"]
        for bird in birds:
            if bird.matches(".endangered"):
                # print('The ' + bird.textContent + ' is endangered!')
                assert "The " + bird.textContent + " is endangered!" == "The Philippine eagle is endangered!"

    def test_getElementsByTagName(self):
        content = ul(_id="birds").html(
            li("Orange-winged parrot"), li("Philippine eagle", _class="endangered"), li("Great white pelican")
        )
        birds = content.getElementsByTagName("li")
        assert len(birds) == 3
        assert birds[1] == content.getElementsBySelector("li.endangered", content)[0]
        assert birds[1].className == "endangered"
        assert birds[1].classList == ["endangered"]

        a = self.page.getElementsByTagName("a")
        assert len(a) == 11
        # print(a)
        assert a[1].href == "#about"
        assert a[1].textContent == "About"

        titletag = self.page.getElementsByTagName("h1")
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
        s1 = Sanitizer({"allowAttributes": {"style": ["span"]}}).sanitize(sample)
        # print(type(s1))
        # print(s1)
        assert str(s1) == '<div><span style="font-weight: bold">hello</span></div>'

        # Allow style, but not on span: <span>...</span>
        s2 = Sanitizer({"allowAttributes": {"style": ["div"]}}).sanitize(sample)
        # print(s2)
        assert str(s2) == '<div style="cool"><span>hello</span></div>'

        # Allow style on any elements: <span style='font-weight: bold'>...</span>
        s3 = Sanitizer({"allowAttributes": {"style": ["*"]}}).sanitize(sample)
        # print("3::::", s3)
        # print(str(s3))
        # Note - check why is id/class not a default config?
        assert str(s3) == '<div style="cool"><span style="font-weight: bold">hello</span></div>'

        # Drop <span id>: <span class='theclass' style='font-weight: bold'>...</span>
        s4 = Sanitizer({"dropAttributes": {"id": ["span"]}}).sanitize(sample)
        # print("4::::", s4)
        assert str(s4) == '<div style="cool"><span class="theclass" style="font-weight: bold">hello</span></div>'

        # Drop id, everywhere: <span class='theclass' style='font-weight: bold'>...</span>
        s5 = Sanitizer({"dropAttributes": {"id": ["*"]}}).sanitize(sample)
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
        com = comment("foo")
        # print(f'{com}')
        assert str(com) == "<!--foo-->"
        from domonic.dom import Comment

        # https://github.com/byteface/domonic/issues/38
        com = f"{html(head(),body(Comment('foo')))}"
        assert "<!--foo-->" in com
        # not able to recreate. Comment was updated to a Node in 6.1
        # this may have been due to that
        # TODO - mulitple arguments to comment

    def test_body_two(self):
        aNewBodyElement = document.createElement("body")
        aNewBodyElement.id = "newBodyElement"
        page = html()
        page.body = aNewBodyElement
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
        mydoc = html(body("test"))
        mydoc.body.append(a(name="foo"))
        mydoc.body.append(a(name="bar"))
        mydoc.body.append(a(href="#test"))
        assert len(mydoc.anchors) == 2

    def test_treewalker(self):

        from domonic.dom import Comment, TreeWalker

        doc = html(div(_id="contentarea").html(p("Some ", span("text")), b("Bold text")))

        rootnode = doc.getElementById("contentarea")
        # print(rootnode)
        walker = doc.createTreeWalker(rootnode, NodeFilter.SHOW_ELEMENT, None, False)

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
        while walker.nextNode():
            # print('+++', walker.nextNode())
            window.alert(walker.currentNode)  # //alerts P, SPAN, and B.

        # //Go back to the first child node of the collection and alert it
        walker.currentNode = rootnode  # //reset TreeWalker pointer to point to root node
        # print('>>', walker.firstChild()) # calling it breaks it cos it moves it?. is it like an iterator then?
        assert walker.firstChild().tagName.lower() == "p"  # //alerts P

        return

        # test 2
        doc = html(ul(_id="mylist").html(li("List 1"), li("List 2"), li("List 3")))

        rootnode = doc.getElementById("mylist")
        walker = doc.createTreeWalker(rootnode, NodeFilter.SHOW_ELEMENT, None, False)

        window.alert(len(walker.currentNode.childNodes))  # //alerts 7 (includes text nodes)
        window.alert(len(walker.currentNode.getElementsByTagName("*")))  # //alerts 3

        # test 3
        doc = html(div(_id="main").html(p("This is a ", span("paragraph")), b("Bold text")))
        mainDiv = doc.getElementById("main")
        walker = doc.createTreeWalker(mainDiv, NodeFilter.SHOW_ELEMENT, None, False)
        console.log(walker)

        treeWalker = document.createTreeWalker(
            mainDiv,
            NodeFilter.SHOW_TEXT,
            lambda node: NodeFilter.FILTER_ACCEPT
            if (String(node.nodeValue).trim() != "")
            else NodeFilter.FILTER_REJECT,
            False,
        )

        # //Alert the starting node Tree Walker currently points to (root node)
        # //displays DIV (with id=main)
        console.log(walker.currentNode.tagName)

        # //Step through and alert all child nodes
        while walker.nextNode():
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


class NodeTest(unittest.TestCase):
    # found these unit tests for a 17 yr old dom implementation. modded them to work on domonic.
    # helped me fix lots of bugs and edge cases and quirky(expected) behaviors.
    # https://github.com/nibrahim/PlasTeX/tree/21875f4da0ae7639d2205260d2e5cb1b65539296/unittests/DOM
    # LICENSE https://github.com/nibrahim/PlasTeX/blob/21875f4da0ae7639d2205260d2e5cb1b65539296/LICENSE
    # looks like the actual project is here. still supported... https://github.com/plastex/plastex

    def _checkPositions(self, node):
        """Check the postions of all contained nodes"""
        if isinstance(node, CharacterData):
            return

        if not (isinstance(node, Node)):
            return

        maxidx = len(node) - 1

        # Check firstChild and lastChild
        if node.childNodes:
            assert node.firstChild is node[0], "firstChild is incorrect"
            assert node.lastChild is node[maxidx], "lastChild is incorrect"

        # Check nextSibling
        for i, item in enumerate(node):
            if i == maxidx:
                assert item.nextSibling is None, f"nextSibling in position {i} should be None"
            else:
                assert item.nextSibling is node[i + 1], f"nextSibling in position {i} is incorrect ({item.nextSibling})"

        # Check previousSibling
        for i, item in enumerate(node):
            if i == 0:
                assert item.previousSibling is None, f"previousSibling in position {i} should be None"
            else:
                # print('HERE::::', item, item.previousSibling, node[i-1])
                assert (
                    item.previousSibling is node[i - 1]
                ), f"previousSibling in position {i} is incorrect ({item.previousSibling})"

        # Check parentNode
        for i, item in enumerate(node):
            assert item.parentNode is node, f"parentNode in position {i} is incorrect"

        # Check ownerDocument
        for i, item in enumerate(node):
            assert (
                item.ownerDocument is node.ownerDocument
            ), f"ownerDocument in position {i} ({item.ownerDocument}) is incorrect: {node.ownerDocument}"

        # Check attributes
        if node.attributes:
            for key, value in node.attributes.items():
                if isinstance(value, Node):
                    assert value.parentNode is node, f"parentNode is incorrect ({value.parentNode})"
                    self._checkPositions(value)

                elif isinstance(value, list):
                    for item in value:
                        assert getattr(item, "parentNode", node) is node, f"parentNode is incorrect ({item.parentNode})"
                        self._checkPositions(item)

                elif isinstance(value, dict):
                    for item in value.values():
                        assert getattr(item, "parentNode", node) is node, f"parentNode is incorrect ({item.parentNode})"
                        self._checkPositions(item)

    def test_Document(self):
        # There should be one-- and preferably only one --obvious way to do it.
        doc = Document()
        one = doc.createElement("one")
        two = document.createElement("two")
        three = Document.createElement("three")
        node = Document().createElement("top")
        # node.extend([one, two, three])
        node += [one, two, three]
        expected = [one, two, three]
        for i, item in enumerate(node):
            assert item is expected[i], f'"{item}" != "{expected[i]}"'
        self._checkPositions(node)

    def test_firstChild(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createElement("two")
        assert node.firstChild is None, f'"{node.firstChild}" != None'
        node.append(one)
        assert node.firstChild is one, f'"{node.firstChild}" != "{one}"'
        # node.insert(0, two)
        node.prepend(two)
        assert node.firstChild is two, f'"{node.firstChild}" != "{two}"'
        self._checkPositions(node)

    def test_lastChild(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createElement("two")
        assert node.lastChild is None, f'"{node.lastChild}" != None'
        node.append(one)
        assert node.lastChild is one, f'"{node.lastChild}" != "{one}"'
        node.append(two)
        assert node.lastChild is two, f'"{node.lastChild}" != "{two}"'
        self._checkPositions(node)

    def test_childNodes(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        node.append(one)
        node.append(two)
        node.append(three)
        assert node[0] is one, f'"{node[0]}" != "{one}"'
        assert node[1] is two, f'"{node[1]}" != "{two}"'
        assert node[2] is three, f'"{node[2]}" != "{three}"'
        assert node.childNodes[0] is one, f'"{node.childNodes[0]}" != "{one}"'
        assert node.childNodes[1] is two, f'"{node.childNodes[1]}" != "{two}"'
        assert node.childNodes[2] is three, f'"{node.childNodes[2]}" != "{three}"'
        self._checkPositions(node)

    def test_previousSibling(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        node.append(one)
        node.append(two)
        node.append(three)
        assert None is one.previousSibling, f'None != "{one.previousSibling}"'
        assert one is two.previousSibling, f'"{one}" != "{two.previousSibling}"'
        assert two is three.previousSibling, f'"{two}" != "{three.previousSibling}"'

    def test_nextSibling(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        node.append(one)
        node.append(two)
        node.append(three)
        assert two is one.nextSibling, '"%s" != "%s"' % (two, one.nextSibling)
        assert three is two.nextSibling, '"%s" != "%s"' % (three, two.nextSibling)
        assert None is three.nextSibling, 'None != "%s"' % three.nextSibling

    def test_compareDocumentPosition(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        four = Document.createElement("four")
        node.append(one)
        node.append(two)
        node.append(three)
        three.append(four)
        five = Document.createElement("five")

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
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        node.append(one)
        node.append(two)
        node.insertBefore(three, two)
        # print('>>', node)
        assert node[1] is three, '"%s" != "%s"' % (node[1], three)
        node.insertBefore(three, one)
        # print(node)
        # print(node[2], two)
        assert node[0] is three, f'"{node[0]}" != "{three}"'
        assert node[1] is one, f'"{node[1]}" != "{one}"'
        assert node[2] is two, f'"{node[2]}" != "{two}"'
        # print(node)
        self._checkPositions(node)

    def test_replaceChild(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        node.append(one)
        node.append(two)
        node.replaceChild(three, two)
        assert node[0] is one, f'"{node[0]}" != "{one}"'
        assert node[1] is three, f'"{node[1]}" != "{three}"'
        assert len(node) == 2, f"{len(node)} != {2}"
        self._checkPositions(node)

    def test_removeChild(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        node.append(one)
        node.append(two)
        res = node.removeChild(one)
        assert res is one, f'"{res}" != "{one}"'
        assert len(node) == 1, f"{len(node)} != {1}"
        assert node[0] is two, f'"{node[0]}" != "{two}"'
        self._checkPositions(node)
        res = node.removeChild(two)
        assert res is two, f'"{res}" != "{two}"'
        assert len(node) == 0, f"{len(node)} != {0}"

    def test_appendChild(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        node.appendChild(one)
        # print(node)
        frag = Document.createDocumentFragment()
        frag.appendChild(two)
        frag.appendChild(three)
        node.appendChild(frag)
        # print(node)
        assert node[0] is one, f'"{node[0]}" != "{one}"'
        assert node[1] is two, f'"{node[1]}" != "{two}"'
        assert node[2] is three, f'"{node[2]}" != "{three}"'
        self._checkPositions(node)

    def test_insert(self):
        """Insert into empty node"""
        one = Document.createElement("one")
        two = Document.createElement("two")
        three = Document.createElement("three")
        node = Document.createElement("top")
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
            assert item is expected[i], f'"{item}" != "{expected[i]}"'
        self._checkPositions(node)

    def test_insert2(self):
        """Insert into populated node"""
        one = Document.createElement("one")
        two = Document.createElement("two")
        three = Document.createElement("three")
        node = Document.createElement("top")
        # node.extend([one, two, three])
        node += [one, two, three]
        # print("cool?", node)
        # node += 2
        # node += 3
        i0 = Document.createElement("i0")
        i3 = Document.createTextNode("i3")
        # node.insert(0, i0)
        node.prepend(i0)
        # node.insert(3, i3) # TODO - consider an insertAt non standard addition to node? (although then where do you stop. grep/moveTo/find_at/every list method?. etc)
        node.args = node.args[:3] + (i3,) + node.args[3:]  # does same as insert(3, i3)
        # print("cool2?", node)
        expected = [i0, one, two, i3, three]
        for i, item in enumerate(node):
            assert item is expected[i], f'"{item}" != "{expected[i]}"'
        self._checkPositions(node)

    def test_Element_prepend(self):
        """Insert document fragment"""
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        four = Document.createElement("four")
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
        assert node[0] is one, f'"{node[0]}" != "{one}"'
        assert node[1] is three, f'"{node[1]}" != "{three}"'
        assert node[2] is four, f'"{node[2]}" != "{four}"'
        assert node[3] is two, f'"{node[3]}" != "{two}"'
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
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createElement("three")
        four = Document.createElement("four")
        five = Document.createElement("five")
        node.appendChild(one)
        # node.extend([two, three])
        node += [two, three]
        assert node[0] is one, f'"{node[0]}" != "{one}"'
        assert node[1] is two, f'"{node[1]}" != "{two}"'
        assert node[2] is three, f'"{node[2]}" != "{three}"'
        assert len(node) == 3, f"{len(node)} != {3}"
        self._checkPositions(node)
        node += [four, five]
        assert node[3] is four, f'"{node[3]}" != "{four}"'
        assert node[4] is five, f'"{node[4]}" != "{five}"'
        assert len(node) == 5, f"{len(node)} != {5}"
        self._checkPositions(node)

    def test_hasChildNodes(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        assert not node.hasChildNodes()
        node.appendChild(one)
        node.appendChild(two)
        assert node.hasChildNodes()

    def test_cloneNode(self):
        one = Document.createElement("one")
        two = Document.createElement("two")
        three = Document.createTextNode("three")
        two.append(three)
        one.append(two)
        res = one.cloneNode(1)
        assert type(res) is type(one), f'"{type(res)}" != "{type(one)}"'
        assert type(res[0]) is type(one[0])
        # print(one, res)
        # print(type(one), type(res))
        assert str(one) == str(res)
        assert one is not res
        assert one[0] is not res[0]

    def test_normalize(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createTextNode("two")
        three = Document.createTextNode("three")
        four = Document.createTextNode("four")
        node.appendChild(one)
        node.appendChild(two)
        node.appendChild(three)
        node.appendChild(four)
        # node.extend([one, two, three, four])
        # print(node)
        node.normalize()
        # print(node)
        assert len(node) == 2, f'"{len(node)}" != "{2}"'
        assert node[1] == "twothreefour", f'"{node[1]}" != "{"twothreefour"}"'

    def test_hasAttributes(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        assert not node.hasAttributes()
        # node.attributes['one'] = one
        # print(str(node.attributes))
        # print(len(node.attributes))
        # node._test2 = 'test1'  # TODO - still need to sort
        # node.test2 = 'test2'  # TODO - still need to sort
        # node['test'] = 'test3' # TODO - auto-underscore?. (problem is expectation on getters. think back to the broken branch)
        node["_test4"] = "test4"
        # node >> {"_test":'test'}
        # print(node)
        # print(node.attributes)
        # print(len(node.attributes))
        # print(node._test4)
        # print(node['_test4'])
        assert node.hasAttributes()

    def test_textContent(self):
        node = Document.createElement("node")
        one = Document.createTextNode("one")
        two = Document.createElement("two")
        three = Document.createTextNode("three")
        four = Document.createTextNode("four")
        node.append(one)
        node.append(two)
        # two.extend([three, four])
        two.append(three)
        two.append(four)
        res = node.textContent
        expected = "onethreefour"
        assert res == expected, f'"{res}" != "{expected}"'

    def test_isSameNode(self):
        node = Document.createElement("node")
        assert node.isSameNode(node)
        clone = node.cloneNode()
        assert not node.isSameNode(clone)

    def test_isEqualNode(self):
        node = Document.createElement("node")
        one = Document.createElement("one")
        two = Document.createElement("two")
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


class CommentTest(unittest.TestCase):
    def setUp(self):
        self.c = Comment("comment")
        self.elm = p()

    def test_node_type(self):
        self.assertEqual(self.c.nodeType, self.c.COMMENT_NODE)
        self.assertEqual(self.c.nodeName, "#comment")

    def test_length(self):
        self.assertEqual(self.c.length, 7)

    def test_html(self):
        self.assertEqual("<!--comment-->", str(self.c))

    def test_append_comment(self):
        self.elm.appendChild(self.c)
        self.assertTrue(self.elm.hasChildNodes())
        self.assertEqual(self.elm.length, 1)
        self.assertEqual("<!--comment-->", str(self.elm.firstChild))


class TestDocumentType(unittest.TestCase):
    def setUp(self):
        self.dtype = DocumentType()
        self.node = Node()

    def test_nodename(self):
        self.assertEqual(self.dtype.nodeName, "html")
        self.assertEqual(self.dtype.name, "html")

    def test_parent(self):
        self.node.appendChild(self.dtype)
        self.assertIs(self.node, self.dtype.parentNode)

    def test_html(self):
        self.assertEqual(str(self.dtype), "<!DOCTYPE html>")


class TestNodeList(unittest.TestCase):
    def setUp(self):
        super().setUp()
        self.nl = NodeList(list(range(3)))

    def test_length(self):
        self.assertEqual(self.nl.length, 3)
        self.assertEqual(len(self.nl), 3)

    def test_index_access(self):
        self.assertEqual(self.nl[1], 1)
        self.assertEqual(self.nl[-1], 2)
        self.assertEqual(self.nl[1:2], [1])
        with self.assertRaises(IndexError):
            self.nl[5]

    def test_item(self):
        self.assertEqual(self.nl.item(1), 1)
        self.assertEqual(self.nl.item(-1), None)
        self.assertEqual(self.nl.item(5), None)
        with self.assertRaises(TypeError):
            self.nl.item(slice(1, 2))

    def test_contains(self):
        self.assertIn(1, self.nl)
        self.assertNotIn(5, self.nl)

    def test_iteration(self):
        l1 = [0, 1, 2]
        for n in self.nl:
            self.assertEqual(n, l1.pop(0))
        l2 = [2, 1, 0]
        for n in reversed(self.nl):
            self.assertEqual(n, l2.pop(0))

    def test_index(self):
        self.assertEqual(self.nl.index(0), 0)
        self.assertEqual(self.nl.index(1), 1)
        self.assertEqual(self.nl.index(2), 2)


class TestDomTokenList(unittest.TestCase):
    def setUp(self):
        super().setUp()

    def test_classList(self):
        sample = div(_class="theclass theclass2 theclass3")
        # print(sample.classList)
        assert sample.classList.contains("theclass")
        # print(sample.classList.contains('theclass'))
        sample.classList.add("theclass4")
        # print(sample.classList)
        assert sample.classList.contains("theclass4")
        # print(type(sample.classList))
        # sample.classList += 'theclass5' # TODO - dunders
        # print(sample.classList)
        sample.classList.remove("theclass")
        # print(sample.classList)
        assert not sample.classList.contains("theclass")
        # print(len(sample.classList))
        assert len(sample.classList) == 3

    def test_toggle_item_and_string_helpers(self):
        sample = div(_class="one two")
        tokens = sample.classList

        tokens.toggle("two")
        self.assertFalse(tokens.contains("two"))
        tokens.toggle("three")
        self.assertTrue(tokens.contains("three"))
        tokens.toggle("four", True)
        self.assertTrue(tokens.contains("four"))
        tokens.toggle("four", False)
        self.assertFalse(tokens.contains("four"))
        self.assertEqual(tokens.item(0), "one")
        self.assertEqual(tokens.item(10), None)
        self.assertEqual(tokens.toString(), "one three")
        self.assertEqual(sample.className, "one three")


if __name__ == "__main__":
    unittest.main()
