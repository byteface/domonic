"""
test_domonic
~~~~~~~~~~~~
- unit tests for domonic.dom

"""

import os
import tempfile
import unittest

from domonic import *
from domonic.CDN import CDN_CSS
from domonic.dom import *
from domonic.events import FormDataEvent, InputEvent, ToggleEvent, TrackEvent
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
                            p(
                                "Welcome to the information age",
                                _class="headings-font-family text-uppercase lead",
                            ),
                            h1(
                                "We are",
                                span("COMPANY", _class="font-weight-bold d-block"),
                                _class="text-uppercase hero-text text-black",
                            ),
                            p(
                                "And this is our company website",
                                _class="headings-font-family text-uppercase lead",
                            ),
                        )
                    )
                ),
                header(_class="header sticky-top").html(
                    nav(
                        _class="navbar navbar-expand-lg bg-white border-bottom py-0"
                    ).html(
                        div(_class="container").html(
                            h6("website.com"),
                            div(
                                _id="navbarSupportedContent",
                                _class="collapse navbar-collapse",
                            ).html(
                                ul(_class="navbar-nav ml-auto px-3").html(
                                    li(
                                        a(
                                            "Home",
                                            _href="",
                                            _class="nav-link text-uppercase link-scroll",
                                        ),
                                        _class="nav-item active",
                                    ),
                                    li(
                                        a(
                                            "About",
                                            _href="#about",
                                            _class="nav-link text-uppercase link-scroll",
                                        ),
                                        _class="nav-item",
                                    ),
                                    li(
                                        a(
                                            "Services",
                                            _href="#services",
                                            _class="nav-link text-uppercase link-scroll",
                                        ),
                                        _class="nav-item",
                                    ),
                                    li(
                                        a(
                                            "Team",
                                            _href="#team",
                                            _class="nav-link text-uppercase link-scroll",
                                        ),
                                        _class="nav-item",
                                    ),
                                    li(
                                        a(
                                            "Contact",
                                            _href="#contact",
                                            _class="nav-link text-uppercase link-scroll",
                                        ),
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
                                p(
                                    "COMPANY can provide xxxxxx solutions. We have expertise in the following areas."
                                ),
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
                    _class="row text-white text-center",
                    _style="background: url(static/img/header.jpg); padding:20px;",
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
                                    h4(
                                        "Headline",
                                        _class="text-uppercase font-weight-bold",
                                    ),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4(
                                        "Headline",
                                        _class="text-uppercase font-weight-bold",
                                    ),
                                    p("Lorem ipsum.", _class="small text-gray"),
                                )
                            ),
                            div(_class="col-lg-4").html(
                                div(_class="bg-white mb-4 p-4").html(
                                    h3(i(_class="fas fa-desktop"), _class="icon mb-3"),
                                    h4(
                                        "Headline",
                                        _class="text-uppercase font-weight-bold",
                                    ),
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
                                        a(
                                            "Username",
                                            _href="#",
                                            _class="no-anchor-style",
                                        )
                                    ),
                                    p(
                                        "Director",
                                        _class="small text-gray text-uppercase",
                                    ),
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
                                        a(
                                            "user@website.com",
                                            _href="mailto:user@website.com",
                                        ),
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
                                p(
                                    "Copyright &copy; 2021 COMPANY. All rights Reserved.",
                                    _class="mb-0 text-gray",
                                ),
                            )
                        )
                    ),
                    script(_src="static/js/jquery.min.js"),
                    link(
                        _rel="stylesheet",
                        _href=CDN_CSS.FONTAWESOME,
                        _crossorigin="anonymous",
                    ),
                ),
            ),
        )

    def test_evaluate(self):
        # headings = self.page.evaluate("/html/body//h2", self.page)  #, None, XPathResult.ANY_TYPE, None);
        headings = self.page.evaluate(
            "//h1", self.page
        )  # , None, XPathResult.ANY_TYPE, None);
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
        somelist.forEach(
            lambda currentValue, currentIndex, listObj, **kwargs: seen.append(
                (currentValue, currentIndex, listObj)
            )
        )
        self.assertEqual(
            seen, [(kid1, 0, somelist), (kid2, 1, somelist), (kid3, 2, somelist)]
        )

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
        self.assertEqual(
            None, n.localName
        )  # obsolete if not a tag or attribute should return none
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

        self.assertEqual("div", d.nodeName)

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
        self.assertEqual(
            True, str(myobj) == '<div class="mytest" style="float:left;"></div>'
        )

        # print("NOW>>>>")
        mylist = li() / 10
        assert (
            str(mylist)
            == "<li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li>"
        )

        myobj = domonic.load(mylist)
        self.assertEqual(len(myobj), 10)

        myorderedlist = ol()
        myorderedlist += str(li() / 10)
        assert (
            str(myorderedlist)
            == "<ol><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li><li></li></ol>"
        )

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
        sometag.style.color = "red"
        self.assertEqual(sometag.style.color, "red")
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
        self.assertEqual(
            str(sometag), '<div id="someid">asdfasdf<div></div><div>yo</div></div>'
        )
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

        mydiv = div(
            "I like cake", div(_class="myclass").html(div("1"), div("2"), div("3"))
        )
        # print(mydiv)
        assert (
            str(mydiv)
            == '<div>I like cake<div class="myclass"><div>1</div><div>2</div><div>3</div></div></div>'
        )

        self.assertEqual(sometag.innerText(), "test2")
        sometag.textContent = ""

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
        dom1 = html(
            div(
                div(
                    div(
                        div(
                            div(
                                div(
                                    div(
                                        article(
                                            "asdfasdf", div(), div("yo"), _id="test"
                                        )
                                    )
                                )
                            )
                        )
                    )
                )
            )
        )
        result = dom1.getElementById("test")
        assert result.tagName == "article"
        self.assertIsNone(dom1.getElementById("missing"))

        doc = Document()
        doc.appendChild(div(_id="doc-hit"))
        self.assertEqual(doc.getElementById("doc-hit").tagName, "div")
        self.assertIsNone(doc.getElementById("missing"))
        self.assertEqual(len(result.childNodes), 3)
        self.assertEqual(len(result.children), 2)

    def test_remove(self):
        dom1 = html(
            div(
                div(
                    div(
                        div(
                            div(div(div(div("asdfasdf", div(), div("yo"), _id="test"))))
                        )
                    )
                )
            )
        )
        result = dom1.getElementById("test")
        # print("owner:", result.ownerDocument)
        assert result.ownerDocument == dom1
        result.remove()
        assert "asdfasdf" not in str(dom1)
        self.assertIsNone(result.parentNode)

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

    def test_lang(self):
        dom1 = div("Bonjour", _lang="fr")
        self.assertEqual(dom1.lang, "fr")
        dom1.lang = "fr-CA"
        self.assertEqual(dom1.getAttribute("lang"), "fr-CA")
        self.assertEqual(str(dom1), '<div lang="fr-CA">Bonjour</div>')

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
        self.assertEqual(wrapper.textContent, "Part 1 Part 2 Part 3")

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
                                        div(
                                            "asdfasdf",
                                            div(),
                                            div("yo"),
                                            _class="test this thing",
                                        ),
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
        assert dom1.getElementById("thing") is result

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
        assert len(dom1.getElementsByClassName("test this")) == 1
        assert len(dom1.querySelectorAll(".test.this")) == 1
        assert dom1.contains(dom1)

        scoped = div(div("child", _id="child", _class="box"), _id="root", _class="box")
        self.assertIsNone(scoped.querySelector("#root"))
        self.assertIsNone(scoped.getElementById("root"))
        self.assertEqual(scoped.querySelector("#child").id, "child")
        self.assertEqual(
            [element.id for element in scoped.getElementsByClassName("box")], ["child"]
        )
        self.assertEqual(
            [element.id for element in scoped.querySelectorAll("div")], ["child"]
        )
        self.assertEqual(
            [element.id for element in scoped.querySelectorAll("*")], ["child"]
        )

        links = self.page.querySelectorAll("a[rel=nofollow]")
        # for linky in links:
        #     print(linky.getAttribute("href"))
        assert len(links) == 1

        result = self.page.querySelectorAll("li[class='nav-item']")
        expected = ["About", "Services", "Team", "Contact"]
        for i, r in enumerate(result):
            assert r.textContent == expected[i]
        assert len(result) == 4

        result = self.page.querySelectorAll(
            "h4[class='font-weight-bold text-uppercase']"
        )
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

        result = self.page.querySelectorAll("a[href$='user/']")
        self.assertEqual(len(result), 1)

        result = self.page.querySelectorAll("a[href*='twitter']")
        self.assertEqual(len(result), 1)

        result = dom1.querySelectorAll(".fa-twitter")
        self.assertEqual(result, [])

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
                                        div(
                                            "asdfasdf",
                                            div(),
                                            div("yo"),
                                            _class="test this thing",
                                        ),
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

        result = dom1.getElementsBySelector(".test", dom1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].className, "test this thing")

        result = dom1.getElementsBySelector(".this", dom1)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0].className, "test this thing")

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

        result = self.page.getElementsBySelector(
            "h4[class='font-weight-bold text-uppercase']", self.page
        )
        self.assertEqual(len(result), 1)

        result = self.page.getElementsBySelector("li.nav-item", self.page)
        self.assertEqual(len(result), 5)

        result = self.page.getElementsBySelector("a[href='#services']", self.page)
        self.assertEqual(len(result), 1)

        result = self.page.getElementsBySelector("p.text-gray", self.page)
        self.assertEqual(len(result), 5)

        result = self.page.getElementsBySelector("a[href$='user/']", self.page)
        self.assertEqual(len(result), 1)

        result = self.page.getElementsBySelector("a[href*='twitter']", self.page)
        self.assertEqual(len(result), 1)

    def test_get_elements_by_selector_supports_commas_and_tagless_class(self):
        page = html(
            body(
                div("one", _class="card"),
                span("two", _class="card"),
                p("three", _id="hero"),
            )
        )

        class_matches = page.getElementsBySelector(".card", page)
        self.assertEqual(len(class_matches), 2)
        self.assertEqual([node.tagName for node in class_matches], ["div", "span"])

        combined = page.getElementsBySelector(".card, #hero", page)
        self.assertEqual(len(combined), 3)
        self.assertEqual([node.tagName for node in combined], ["div", "span", "p"])

    def test_class_selectors_match_literal_class_tokens(self):
        page = html(
            body(
                div("literal", _class="foo+bar widget"),
                div("plain", _class="foobar widget"),
                span("multi", _class="foo+bar active"),
            )
        )

        matches = page.querySelectorAll(".foo+bar")
        self.assertEqual([node.textContent for node in matches], ["literal", "multi"])
        self.assertEqual(
            [node.textContent for node in page.querySelectorAll("div.foo+bar")],
            ["literal"],
        )
        self.assertEqual(page.querySelectorAll(".foo+bar.missing"), [])

    def test_attribute_selectors_match_literal_tokens(self):
        page = html(
            body(
                div("literal", _class="foo+bar widget"),
                div("plain", _class="foobar widget"),
                p("base", _lang="en"),
                p("regional", _lang="en-US"),
                p("word", _lang="english"),
            )
        )

        self.assertEqual(
            [node.textContent for node in page.querySelectorAll("[class~=foo+bar]")],
            ["literal"],
        )
        self.assertEqual(page.querySelectorAll("[class~=foo]"), [])
        self.assertEqual(
            [node.textContent for node in page.querySelectorAll("[lang|=en]")],
            ["base", "regional"],
        )

    def test_get_elements_by_selector_supports_compound_attribute_selectors(self):
        page = html(
            body(
                a(
                    "Twitter",
                    _id="social",
                    _class="nav-link social",
                    _href="https://twitter.com/domonic",
                    _rel="external help",
                    _lang="en-GB",
                    **{"_data-state": "ready"},
                ),
                a("Docs", _class="nav-link", _href="/docs/index.html"),
                a("Home", _href="/"),
            )
        )

        self.assertEqual(
            [
                node.textContent
                for node in page.getElementsBySelector(
                    "a.nav-link[href*='twitter']", page
                )
            ],
            ["Twitter"],
        )
        self.assertEqual(
            [
                node.textContent
                for node in page.getElementsBySelector("[href^='/']", page)
            ],
            ["Docs", "Home"],
        )
        self.assertEqual(
            [
                node.textContent
                for node in page.getElementsBySelector("a[rel~=help]", page)
            ],
            ["Twitter"],
        )
        self.assertEqual(
            [
                node.textContent
                for node in page.getElementsBySelector("a[lang|=en]", page)
            ],
            ["Twitter"],
        )
        self.assertEqual(
            [
                node.textContent
                for node in page.getElementsBySelector("[data-state=ready]", page)
            ],
            ["Twitter"],
        )

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
        from unittest.mock import patch

        from domonic.dom import console as legacy_console
        from domonic.webapi.console import Console
        from domonic.window import Window as BrowserWindow

        win = BrowserWindow()
        self.assertIsInstance(win.console, Console)

        with patch("builtins.print") as print_mock:
            self.assertEqual(win.console.log("test this"), "test this")
        self.assertEqual(print_mock.call_args.args, ("test this",))
        self.assertIs(legacy_console, Console)

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
        page = html(
            body(input(_type="text", _id="first"), input(_type="text", _id="second"))
        )
        body_focus_events = []
        body_blur_events = []
        first = page.querySelector("#first")
        second = page.querySelector("#second")

        page.body.addEventListener(
            "focusin", lambda e: body_focus_events.append((e.type, e.relatedTarget))
        )
        page.body.addEventListener(
            "focusout", lambda e: body_blur_events.append((e.type, e.relatedTarget))
        )

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

        self.assertEqual(
            events, [("first", "focus"), ("first", "blur"), ("second", "focus")]
        )

    def test_domimplementation_create_html_document(self):
        impl = DOMImplementation()
        doc = impl.createHTMLDocument("hello")
        self.assertEqual(doc.querySelector("title").textContent, "hello")
        self.assertEqual(doc.body.tagName, "body")
        self.assertTrue(impl.hasFeatures(None))
        self.assertTrue(impl.hasFeature("XML", "1.0"))

    def test_domimplementation_create_document_and_doctype(self):
        impl = DOMImplementation()
        doctype = impl.createDocumentType("html", "", "")
        doc = impl.createDocument("http://www.w3.org/1999/xhtml", "html", doctype)

        self.assertIsInstance(doc, XMLDocument)
        self.assertEqual(str(doc.doctype), "<!DOCTYPE html>")
        self.assertEqual(doc.nodeType, Node.DOCUMENT_NODE)
        self.assertEqual(str(doctype), "<!DOCTYPE html>")
        self.assertEqual(doc.documentElement.tagName, "html")
        self.assertEqual(
            doc.documentElement.namespaceURI, "http://www.w3.org/1999/xhtml"
        )

    def test_domimplementation_create_xml_document(self):
        impl = DOMImplementation()
        doc = impl.createDocument("http://www.w3.org/2000/svg", "svg", None)

        self.assertIsInstance(doc, XMLDocument)
        self.assertEqual(doc.contentType, "application/xml")
        self.assertEqual(doc.documentElement.tagName, "svg")
        self.assertEqual(doc.documentElement.namespaceURI, "http://www.w3.org/2000/svg")

    def test_document_import_node_variants(self):
        page = html(body())
        imported_element = page.importNode(div(span("x"), _id="one"), deep=True)
        imported_comment = page.importNode(Comment("note"))
        imported_text = page.importNode(Text("hello"))
        imported_instruction = page.importNode(
            ProcessingInstruction("xml-stylesheet", 'href="style.css"')
        )
        imported_fragment = page.importNode(DocumentFragment())
        imported_attr = page.importNode(Attr("data-id", "7"))

        self.assertEqual(str(imported_element), '<div id="one"><span>x</span></div>')
        self.assertIs(imported_element.ownerDocument, page)
        self.assertEqual(str(imported_comment), "<!--note-->")
        self.assertIs(imported_comment.ownerDocument, page)
        self.assertEqual(str(imported_text), "hello")
        self.assertIs(imported_text.ownerDocument, page)
        self.assertEqual(
            str(imported_instruction), '<?xml-stylesheet href="style.css"?>'
        )
        self.assertIs(imported_instruction.ownerDocument, page)
        self.assertIsInstance(imported_fragment, DocumentFragment)
        self.assertEqual((imported_attr.name, imported_attr.value), ("data-id", "7"))

    def test_document_import_node_from_attached_tree_is_disconnected_clone(self):
        source_page = html(body(div(span("kid", _id="kid"), _id="source")))
        target_page = html(body())
        source = source_page.querySelector("#source")

        imported = target_page.importNode(source, deep=True)
        imported_child = imported.querySelector("#kid")

        self.assertIsNot(imported, source)
        self.assertIsNone(imported.parentNode)
        self.assertIs(imported.ownerDocument, target_page)
        self.assertFalse(imported.isConnected)
        self.assertIs(imported_child.parentNode, imported)
        self.assertIs(imported_child.ownerDocument, target_page)
        self.assertFalse(imported_child.isConnected)
        self.assertIs(source.parentNode, source_page.body)
        self.assertIs(source.ownerDocument, source_page)

    def test_document_import_node_deep_clones_document_fragment(self):
        page = html(body())
        fragment = Document.createDocumentFragment(
            Text("lead "), span("child", _id="child")
        )

        imported = page.importNode(fragment, deep=True)
        shallow = page.importNode(fragment, deep=False)

        self.assertEqual(str(imported), 'lead <span id="child">child</span>')
        self.assertIs(imported.ownerDocument, page)
        self.assertFalse(imported.isConnected)
        self.assertEqual(imported.childNodes.length, 2)
        self.assertEqual(
            [child.getAttribute("id") for child in imported.children], ["child"]
        )
        self.assertEqual(imported.childElementCount, 1)
        self.assertIs(imported.firstChild.ownerDocument, page)
        self.assertIs(imported.querySelector("#child").ownerDocument, page)
        self.assertEqual(str(fragment), 'lead <span id="child">child</span>')
        self.assertEqual(shallow.childNodes.length, 0)

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
        container = div(
            span("a", _id="first"), span("b", _id="second"), span("c", _id="third")
        )
        first = container.querySelector("#first")
        third = container.querySelector("#third")

        r = Range()
        r.setStartBefore(first)
        r.setEndAfter(third)

        self.assertEqual(
            r.toString(),
            '<span id="first">a</span><span id="second">b</span><span id="third">c</span>',
        )
        self.assertEqual(str(r.cloneContents()), str(r.extractContents()))
        self.assertEqual(str(container), "<div></div>")

    def test_range_intersects_and_invalid_compare_type(self):
        container = div(
            span("a", _id="first"), span("b", _id="second"), span("c", _id="third")
        )
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
        self.assertIsInstance(static, AbstractRange)
        with self.assertRaises(TypeError):
            static.setStart(text, 1)

    def test_range_boundary_validation_and_auto_ordering(self):
        text = Text("abcdef")
        r = Range()

        with self.assertRaises(ValueError):
            r.setStart(text, 99)

        r.setStart(text, 4)
        r.setEnd(text, 2)
        self.assertEqual((r.startOffset, r.endOffset), (2, 2))

        r.setStart(text, 1)
        r.setEnd(text, 5)
        with self.assertRaises(ValueError):
            r.comparePoint(text, 10)

    def test_range_collapse_defaults_to_end_boundary(self):
        text = Text("abcdef")
        r = Range()
        r.setStart(text, 1)
        r.setEnd(text, 4)

        r.collapse()
        self.assertEqual((r.startOffset, r.endOffset), (4, 4))
        self.assertTrue(r.collapsed)

        r.setStart(text, 1)
        r.setEnd(text, 4)
        r.collapse(True)
        self.assertEqual((r.startOffset, r.endOffset), (1, 1))

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
        self.assertIs(shadow_button.getRootNode(), shadow)
        self.assertIs(shadow_button.getRootNode({"composed": True}), page)
        self.assertEqual(
            shadow_selection.getRangeAt(0).toString(),
            '<button id="shadow-button" style="left:0px;top:0px;width:40px;height:20px;">go</button>',
        )

    def test_custom_elements_registry_and_upgrade(self):
        from domonic import domonic as domonic_module
        from domonic.window import window

        class MyWidget(HTMLElement):
            connected_count = 0

            def connectedCallback(self):
                self.connected_count += 1

        class MyLabel(Element):
            name = "my-label"

        promise = window.customElements.whenDefined("my-widget")
        self.assertEqual(promise.state, "pending")

        defined = window.customElements.define("my-widget", MyWidget)
        self.assertIs(defined, MyWidget)
        self.assertEqual(window.customElements.get("my-widget"), MyWidget)
        self.assertEqual(window.customElements.getName(MyWidget), "my-widget")
        self.assertEqual(promise.state, "fulfilled")

        widget = document.createElement("my-widget")
        self.assertIsInstance(widget, MyWidget)
        self.assertEqual(widget.tagName, "my-widget")

        with self.assertRaises(ValueError):
            window.customElements.define("my-widget", MyLabel)

        parsed = domonic_module.parseString("<my-widget></my-widget>")
        parsed_widget = parsed.querySelector("my-widget")
        self.assertIsInstance(parsed_widget, MyWidget)

    def test_custom_element_lifecycle_callbacks(self):
        from domonic.window import window

        class LifecycleWidget(HTMLElement):
            observedAttributes = ("data-state",)

            def __init__(self, *args, **kwargs):
                super().__init__(*args, **kwargs)
                self.connected_calls = 0
                self.disconnected_calls = 0
                self.attribute_changes = []
                self.adoptions = []

            def connectedCallback(self):
                self.connected_calls += 1

            def disconnectedCallback(self):
                self.disconnected_calls += 1

            def attributeChangedCallback(self, name, old_value, new_value):
                self.attribute_changes.append((name, old_value, new_value))

            def adoptedCallback(self, old_document, new_document):
                self.adoptions.append((old_document, new_document))

        if window.customElements.get("life-widget") is None:
            window.customElements.define("life-widget", LifecycleWidget)

        doc = Document()
        host = div()
        doc.appendChild(host)

        widget = document.createElement("life-widget")
        host.appendChild(widget)
        self.assertEqual(widget.connected_calls, 1)

        widget.setAttribute("data-state", "ready")
        self.assertEqual(widget.attribute_changes[-1], ("data-state", None, "ready"))

        host.removeChild(widget)
        self.assertEqual(widget.disconnected_calls, 1)

        other_doc = Document()
        imported = other_doc.importNode(widget, deep=True)
        self.assertEqual(len(imported.adoptions), 1)
        self.assertIs(imported.adoptions[-1][1], other_doc)

    def test_shadow_root_slots_assign_nodes_and_elements(self):
        host = div(_id="slot-host")
        doc = Document()
        doc.appendChild(host)

        shadow = host.attachShadow({"mode": "open"})
        default_slot = slot()
        named_slot = slot(_name="header")
        events = []
        default_slot.addEventListener(
            "slotchange", lambda event: events.append("default")
        )
        named_slot.addEventListener("slotchange", lambda event: events.append("header"))
        shadow.appendChild(named_slot)
        shadow.appendChild(default_slot)

        heading = h1("Title", _slot="header")
        body_copy = span("Body")
        host.appendChild(heading)
        host.appendChild(body_copy)

        self.assertEqual(named_slot.assignedElements(), [heading])
        self.assertEqual(default_slot.assignedElements(), [body_copy])
        self.assertIs(heading.assignedSlot, named_slot)
        self.assertIs(body_copy.assignedSlot, default_slot)
        self.assertIn("header", events)
        self.assertIn("default", events)

    def test_mutation_observer_child_list_records(self):
        target = div()
        delivered = []
        observer = MutationObserver(lambda records, obs: delivered.extend(records))
        observer.observe(target, {"childList": True})

        child = span("hello")
        target.appendChild(child)

        self.assertEqual(len(delivered), 1)
        record = delivered[0]
        self.assertEqual(record.type, "childList")
        self.assertIs(record.target, target)
        self.assertEqual(list(record.addedNodes), [child])
        self.assertEqual(list(record.removedNodes), [])
        self.assertEqual(observer.takeRecords(), [])

    def test_mutation_observer_attributes_and_filters(self):
        target = div()
        delivered = []
        observer = MutationObserver(lambda records, obs: delivered.extend(records))
        observer.observe(
            target,
            {
                "attributes": True,
                "attributeOldValue": True,
                "attributeFilter": ["data-id"],
            },
        )

        target.setAttribute("class", "skip")
        target.setAttribute("data-id", "1")
        target.setAttribute("data-id", "2")

        self.assertEqual(len(delivered), 2)
        self.assertEqual(
            [record.attributeName for record in delivered], ["data-id", "data-id"]
        )
        self.assertEqual(delivered[0].oldValue, None)
        self.assertEqual(delivered[1].oldValue, "1")

    def test_mutation_observer_character_data_and_subtree(self):
        target = div(Text("alpha"))
        delivered = []
        observer = MutationObserver(lambda records, obs: delivered.extend(records))
        observer.observe(
            target,
            {"subtree": True, "characterData": True, "characterDataOldValue": True},
        )

        text_node = target.firstChild
        text_node.replaceData(0, 5, "beta")

        self.assertEqual(len(delivered), 1)
        record = delivered[0]
        self.assertEqual(record.type, "characterData")
        self.assertIs(record.target, text_node)
        self.assertEqual(record.oldValue, "alpha")

    def test_document_normalize_and_stream_writes(self):
        page = html()
        page.args = (
            Text("alpha"),
            Text(""),
            Text("beta"),
        )
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

    def test_node_content_and_autoescape(self):
        node = div("hello", [" ", span("world")])
        self.assertEqual(node.content, "hello <span>world</span>")

        previous = DOMConfig.GLOBAL_AUTOESCAPE
        try:
            DOMConfig.GLOBAL_AUTOESCAPE = True
            escaped = div("<unsafe>")
            self.assertEqual(escaped.content, "&lt;unsafe&gt;")
        finally:
            DOMConfig.GLOBAL_AUTOESCAPE = previous

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
        self.assertEqual(selection.anchorNode, first)
        self.assertEqual(selection.anchorOffset, 2)
        self.assertEqual(selection.focusNode, second)
        self.assertEqual(selection.focusOffset, 3)

        selection.collapseToEnd()
        self.assertEqual(selection.focusOffset, 3)
        self.assertEqual(selection.anchorOffset, 3)

        selection.setBaseAndExtent(second, 1, first, 1)
        self.assertEqual(selection.anchorNode, second)
        self.assertEqual(selection.focusNode, first)

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

    def test_selection_anchor_focus_direction_and_range_order(self):
        first = Text("hello")
        second = Text("world")
        host = div(first, second)
        selection = Selection()

        selection.collapse(second, 3)
        selection.extend(first, 2)

        self.assertIs(selection.anchorNode, second)
        self.assertEqual(selection.anchorOffset, 3)
        self.assertIs(selection.focusNode, first)
        self.assertEqual(selection.focusOffset, 2)

        active = selection.getRangeAt(0)
        self.assertIs(active.startContainer, first)
        self.assertEqual(active.startOffset, 2)
        self.assertIs(active.endContainer, second)
        self.assertEqual(active.endOffset, 3)

    def test_popover_and_interest_reflected_properties(self):
        doc = Document()
        root = div()
        target = div(_id="menu")
        control = button("Open")
        interest = a("More")
        root.appendChild(target)
        root.appendChild(control)
        root.appendChild(interest)
        doc.appendChild(root)

        target.popover = True
        self.assertEqual(target.getAttribute("popover"), "auto")
        self.assertIs(target.showPopover(), target)
        self.assertTrue(target.hasAttribute("open"))
        self.assertIs(target.togglePopover(False), target)
        self.assertFalse(target.hasAttribute("open"))

        control.popoverTargetElement = target
        self.assertEqual(control.getAttribute("popovertarget"), "menu")
        self.assertIs(control.popoverTargetElement, target)
        control.popoverTargetAction = "show"
        self.assertEqual(control.getAttribute("popovertargetaction"), "show")

        interest.interestForElement = target
        self.assertEqual(interest.getAttribute("interestfor"), "menu")
        self.assertIs(interest.interestForElement, target)

        target.addEventListener("beforetoggle", lambda event: event.preventDefault())
        self.assertIs(target.showPopover(), target)
        self.assertFalse(target.hasAttribute("open"))

    def test_modern_dom_constructor_reflected_attributes(self):
        anchor = HTMLAnchorElement(
            "Docs",
            href="/docs",
            hreflang="en",
            ping="/log",
            referrerpolicy="no-referrer",
        )
        self.assertEqual(anchor.getAttribute("ping"), "/log")
        self.assertEqual(anchor.getAttribute("referrerpolicy"), "no-referrer")

        area_el = HTMLAreaElement(
            href="/map",
            alt="Map",
            download="map.png",
            ping="/area-log",
            rel="nofollow",
            referrerpolicy="origin",
        )
        self.assertEqual(area_el.getAttribute("download"), "map.png")
        self.assertEqual(area_el.getAttribute("rel"), "nofollow")

        iframe_el = HTMLIFrameElement(
            allow="fullscreen",
            credentialless=True,
            loading="lazy",
            referrerpolicy="no-referrer",
            srcdoc="<p>Hello</p>",
        )
        self.assertEqual(iframe_el.getAttribute("allow"), "fullscreen")
        self.assertEqual(iframe_el.getAttribute("credentialless"), True)
        self.assertEqual(iframe_el.getAttribute("srcdoc"), "<p>Hello</p>")

        image = HTMLImageElement(
            alt="Hero",
            decoding="async",
            fetchpriority="high",
            loading="lazy",
            referrerpolicy="no-referrer",
            src="/hero.avif",
        )
        self.assertEqual(image.getAttribute("decoding"), "async")
        self.assertEqual(image.getAttribute("fetchpriority"), "high")

        link_el = HTMLLinkElement(
            as_="script",
            blocking="render",
            fetchpriority="high",
            href="/app.js",
            imagesizes="100vw",
            imagesrcset="/app-small.js 1x",
            referrerpolicy="origin",
            rel="preload",
        )
        self.assertEqual(link_el.getAttribute("as"), "script")
        self.assertEqual(link_el.getAttribute("imagesrcset"), "/app-small.js 1x")

        script_el = HTMLScriptElement(
            async_=True,
            blocking="render",
            fetchpriority="high",
            nomodule=True,
            referrerpolicy="no-referrer",
            src="/legacy.js",
        )
        self.assertEqual(script_el.getAttribute("async"), True)
        self.assertEqual(script_el.getAttribute("nomodule"), True)

        source_el = HTMLSourceElement(
            srcset="/small.avif 1x", sizes="50vw", width="640", height="360"
        )
        self.assertEqual(source_el.getAttribute("srcset"), "/small.avif 1x")
        self.assertEqual(source_el.getAttribute("height"), "360")

        style_el = HTMLStyleElement(blocking="render", media="screen")
        self.assertEqual(style_el.getAttribute("blocking"), "render")

        template_el = HTMLTemplateElement(
            shadowrootmode="open",
            shadowrootdelegatesfocus=True,
            shadowrootserializable=True,
        )
        self.assertEqual(template_el.getAttribute("shadowrootmode"), "open")
        self.assertEqual(template_el.getAttribute("shadowrootserializable"), True)

        textarea_el = HTMLTextAreaElement(
            autocomplete="on", dirname="notes.dir", minlength=2
        )
        self.assertEqual(textarea_el.getAttribute("autocomplete"), "on")
        self.assertEqual(textarea_el.getAttribute("minlength"), 2)

        dialog_el = HTMLDialogElement(closedby="any")
        self.assertEqual(dialog_el.getAttribute("closedby"), "any")

        audio_el = HTMLAudioElement(crossorigin="anonymous", loading="lazy")
        self.assertEqual(audio_el.getAttribute("crossorigin"), "anonymous")
        self.assertEqual(audio_el.getAttribute("loading"), "lazy")

        video_el = HTMLVideoElement(
            controlslist="nodownload",
            crossorigin="anonymous",
            disablepictureinpicture=True,
            playsinline=True,
        )
        self.assertEqual(video_el.getAttribute("controlslist"), "nodownload")
        self.assertEqual(video_el.getAttribute("disablepictureinpicture"), True)
        self.assertEqual(video_el.getAttribute("playsinline"), True)

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
        self.assertIsInstance(caret.getClientRect(), DOMRect)

    def test_document_domain_and_event_factory_helpers(self):
        page = html(body(div("x")))
        page.URL = "https://example.com/path?q=1"

        self.assertEqual(page.domain(), "example.com")
        expected_types = {
            "AnimationEvent": "animationstart",
            "BeforeUnloadEvent": "beforeunload",
            "BlobEvent": "dataavailable",
            "ClipboardEvent": "copy",
            "CommandEvent": "command",
            "CompositionEvent": "compositionstart",
            "CustomEvent": "custom",
            "DeviceLightEvent": "devicelight",
            "DeviceMotionEvent": "devicemotion",
            "DeviceOrientationEvent": "deviceorientation",
            "DeviceProximityEvent": "deviceproximity",
            "DOMContentLoadedEvent": "DOMContentLoaded",
            "DragEvent": "drag",
            "ErrorEvent": "error",
            "Event": "",
            "ExtendableEvent": "extendable",
            "FetchEvent": "fetch",
            "FocusEvent": "focus",
            "FormDataEvent": "formdata",
            "GamePadEvent": "gamepadconnected",
            "HashChangeEvent": "hashchange",
            "InputEvent": "input",
            "KeyboardEvent": "keydown",
            "MessageEvent": "message",
            "MouseEvent": "click",
            "PageTransitionEvent": "pageshow",
            "PointerEvent": "pointerdown",
            "PopStateEvent": "popstate",
            "ProgressEvent": "progress",
            "SecurityPolicyViolationEvent": "securitypolicyviolation",
            "StorageEvent": "storage",
            "SubmitEvent": "submit",
            "SVGEvent": "load",
            "SyncEvent": "sync",
            "TimerEvent": "timer",
            "ToggleEvent": "toggle",
            "TrackEvent": "addtrack",
            "TransitionEvent": "transitionend",
            "UIEvent": "load",
            "WebGLContextEvent": "webglcontextlost",
            "WheelEvent": "wheel",
        }
        for event_name, expected_type in expected_types.items():
            with self.subTest(event_name=event_name):
                self.assertEqual(page.createEvent(event_name).type, expected_type)
        self.assertEqual(page.createEvent("CustomMadeEvent").type, "CustomMadeEvent")

    def test_insert_adjacent_element_positions(self):
        host = div(span("target", _id="target"), p("sibling", _id="sibling"))
        target = host.querySelector("#target")

        before = em("before", _id="before")
        returned = target.insertAdjacentElement("beforebegin", before)
        self.assertIs(returned, before)
        self.assertEqual(
            [child.getAttribute("id") for child in host.children],
            ["before", "target", "sibling"],
        )

        after_begin = strong("start", _id="start")
        target.insertAdjacentElement("AFTERBEGIN", after_begin)
        self.assertEqual(target.children[0].getAttribute("id"), "start")

        before_end = i("end", _id="end")
        target.insertAdjacentElement("beforeend", before_end)
        self.assertEqual(target.children[-1].getAttribute("id"), "end")

        after = b("after", _id="after")
        target.insertAdjacentElement("AfterEnd", after)
        self.assertEqual(
            [child.getAttribute("id") for child in host.children],
            ["before", "target", "after", "sibling"],
        )

    def test_insert_adjacent_html_and_text(self):
        host = div(span("target", _id="target"), p("sibling", _id="sibling"))
        target = host.querySelector("#target")

        target.insertAdjacentHTML("beforebegin", "<em id='before'></em>")
        target.insertAdjacentHTML("afterbegin", "<strong id='start'></strong>")
        target.insertAdjacentHTML("beforeend", "<i id='end'></i>")
        target.insertAdjacentHTML("afterend", "<b id='after'></b>")
        target.insertAdjacentText("afterbegin", "prefix-")
        target.insertAdjacentText("beforeend", "-suffix")

        self.assertEqual(
            [child.getAttribute("id") for child in host.children],
            ["before", "target", "after", "sibling"],
        )
        self.assertEqual(target.children[0].getAttribute("id"), "start")
        self.assertEqual(target.children[-1].getAttribute("id"), "end")
        self.assertEqual(
            str(target),
            '<span id="target">prefix-<strong id="start"></strong>target<i id="end"></i>-suffix</span>',
        )
        self.assertEqual(host.querySelector("#before").tagName, "em")
        self.assertEqual(host.querySelector("#after").tagName, "b")

    def test_innerhtml_and_outerhtml_parse_fragments(self):
        old_child = span("old", _id="old")
        host = div(old_child, _id="host")
        self.assertEqual(
            host.outerHTML, '<div id="host"><span id="old">old</span></div>'
        )

        host.innerHTML = "<span id='first'>A</span><span id='second'>B</span>"
        self.assertEqual(len(host.children), 2)
        self.assertEqual(host.children[0].getAttribute("id"), "first")
        self.assertEqual(host.children[1].textContent, "B")
        self.assertIsNone(old_child.parentNode)
        self.assertIs(host.children[0].parentNode, host)

        wrapper = div(host)
        host.outerHTML = (
            "<section id='replacement'>R</section><aside id='tail'>T</aside>"
        )
        self.assertEqual(
            [child.tagName for child in wrapper.children], ["section", "aside"]
        )
        self.assertEqual(wrapper.querySelector("#replacement").textContent, "R")
        self.assertEqual(wrapper.querySelector("#tail").textContent, "T")
        self.assertIsNone(host.parentNode)
        self.assertIs(wrapper.children[0].parentNode, wrapper)

    def test_html_helper_replaces_children_and_detaches_old_nodes(self):
        old_child = span("old", _id="old")
        host = div(old_child)
        new_child = strong("new", _id="new")

        returned = host.html(new_child, " tail")

        self.assertIs(returned, host)
        self.assertEqual(str(host), '<div><strong id="new">new</strong> tail</div>')
        self.assertIsNone(old_child.parentNode)
        self.assertIs(new_child.parentNode, host)

    def test_document_fragment_append_and_prepend_accept_multiple_nodes(self):
        frag = Document.createDocumentFragment()
        child = span("child", _id="child")

        frag.append("lead ", child)
        frag.prepend(strong("start", _id="start"), " ")

        self.assertEqual(
            str(frag),
            '<strong id="start">start</strong> lead <span id="child">child</span>',
        )
        self.assertIs(child.parentNode, frag)
        self.assertEqual(
            [node.getAttribute("id") for node in frag.children], ["start", "child"]
        )

        donor = Document.createDocumentFragment(em("donor", _id="donor"))
        frag.append(donor)

        self.assertEqual(donor.childNodes.length, 0)
        self.assertEqual(
            [node.getAttribute("id") for node in frag.children],
            ["start", "child", "donor"],
        )

    def test_fragment_before_after_and_replace_children_moves_nodes(self):
        host = div(span("target", _id="target"))
        target = host.querySelector("#target")
        before_fragment = Document.createDocumentFragment(
            em("one", _id="one"),
            strong("two", _id="two"),
        )
        after_fragment = Document.createDocumentFragment(p("three", _id="three"))

        target.before(before_fragment)
        target.after(after_fragment)

        self.assertEqual(before_fragment.childNodes.length, 0)
        self.assertEqual(after_fragment.childNodes.length, 0)
        self.assertEqual(
            [child.getAttribute("id") for child in host.children],
            ["one", "two", "target", "three"],
        )

        moved = host.querySelector("#two")
        replacement_fragment = Document.createDocumentFragment(
            span("replacement", _id="replacement")
        )
        host.replaceChildren([replacement_fragment, moved])

        self.assertEqual(replacement_fragment.childNodes.length, 0)
        self.assertEqual(
            [child.getAttribute("id") for child in host.children],
            ["replacement", "two"],
        )
        self.assertIs(moved.parentNode, host)
        self.assertIsNone(target.parentNode)

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
        self.assertIsNone(iterator.detach())
        self.assertEqual(iterator.nextNode(), None)

    def test_treewalker_and_nodeiterator_coerce_what_to_show(self):
        root = div("alpha", span("beta"))
        walker = TreeWalker(root, "4")

        self.assertEqual(walker.whatToShow, NodeFilter.SHOW_TEXT)
        self.assertEqual(walker.firstChild().nodeType, Node.TEXT_NODE)
        self.assertEqual(NodeIterator(root, -1).whatToShow, NodeFilter.SHOW_ALL)
        with self.assertRaisesRegex(TypeError, "whatToShow"):
            TreeWalker(root, "bad")

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

    def test_document_links_includes_anchor_and_area(self):
        page = html(
            body(
                a("home", _href="/"),
                area(_href="/map"),
                a("no href"),
            )
        )

        links = page.links
        self.assertEqual(len(links), 2)
        self.assertEqual([link.tagName for link in links], ["a", "area"])

    def test_attribute_namespace_helpers(self):
        node = div()
        attr = Attr("data-mode", "test")

        self.assertIs(node.setAttributeNodeNS(attr), node)
        fetched = node.getAttributeNodeNS("data-mode")
        self.assertIsNotNone(fetched)
        self.assertEqual((fetched.name, fetched.value), ("data-mode", "test"))
        direct_attr = node.getAttributeNode("data-mode")
        self.assertIsNotNone(direct_attr)
        self.assertEqual((direct_attr.name, direct_attr.value), ("data-mode", "test"))
        self.assertEqual(
            node.getAttributeNS("http://example.com/ns", "data-mode"), "test"
        )
        node.setAttributeNS("http://example.com/ns", "data-other", "x")
        self.assertEqual(node.getAttribute("data-other"), "x")

    def test_remove_attribute_node_accepts_attr_nodes(self):
        node = div(_title="hello", **{"_data-state": "ready"})
        attr = node.getAttributeNode("title")

        removed = node.removeAttributeNode(attr)

        self.assertEqual((removed.name, removed.value), ("title", "hello"))
        self.assertFalse(node.hasAttribute("title"))
        self.assertEqual(node.getAttribute("data-state"), "ready")
        self.assertIsNone(node.removeAttributeNode(attr))
        self.assertEqual(node.removeAttributeNode("_data-state").name, "data-state")
        self.assertFalse(node.hasAttribute("data-state"))

    def test_toggle_attribute(self):
        node = div()

        self.assertTrue(node.toggleAttribute("hidden"))
        self.assertTrue(node.hasAttribute("hidden"))
        self.assertEqual(node.getAttribute("hidden"), "")
        self.assertFalse(node.toggleAttribute("hidden"))
        self.assertFalse(node.hasAttribute("hidden"))

        self.assertTrue(node.toggleAttribute("hidden", True))
        self.assertTrue(node.hasAttribute("hidden"))
        self.assertTrue(node.toggleAttribute("hidden", True))
        self.assertFalse(node.toggleAttribute("hidden", False))
        self.assertFalse(node.hasAttribute("hidden"))

    def test_dataset_and_dom_string_map_helpers(self):
        node = div(**{"_data-user-id": "7", "_data-theme-name": "night"})
        dataset = node.dataset

        self.assertEqual(dataset.get("userId"), "7")
        self.assertEqual(dataset["themeName"], "night")
        self.assertIn("userId", dataset)
        self.assertEqual(len(dataset), 2)
        self.assertEqual(sorted(dataset.keys()), ["themeName", "userId"])
        self.assertEqual(sorted(dataset.values()), ["7", "night"])
        self.assertIn("userId", repr(dataset))

        self.assertTrue(dataset.set("mode", "demo"))
        self.assertEqual(dataset.get("mode"), "demo")
        self.assertEqual(
            sorted(dataset.items()),
            [("mode", "demo"), ("themeName", "night"), ("userId", "7")],
        )
        self.assertTrue(dataset.delete("mode"))
        self.assertFalse(dataset.delete("missing"))
        self.assertEqual(dataset.get("mode"), None)

    def test_dataset_reflects_element_data_attributes(self):
        node = div()
        dataset = node.dataset

        dataset.set("userId", "7")
        self.assertEqual(node.getAttribute("data-user-id"), "7")

        dataset["themeName"] = "night"
        self.assertEqual(node.getAttribute("data-theme-name"), "night")
        self.assertEqual(node.dataset["themeName"], "night")

        node.setAttribute("data-api-url", "/v1")
        self.assertEqual(dataset.get("apiUrl"), "/v1")
        self.assertEqual(sorted(dataset.keys()), ["apiUrl", "themeName", "userId"])

        self.assertTrue(dataset.delete("themeName"))
        self.assertIsNone(node.getAttribute("data-theme-name"))

    def test_node_operator_helpers(self):
        node = div(span("a"), _id="root")
        sibling = div("b")

        self.assertEqual(node["id"], "root")
        self.assertEqual(node[0].tagName, "span")

        clones = node * 2
        self.assertEqual(len(clones), 2)
        self.assertTrue(all(isinstance(clone, type(node)) for clone in clones))
        self.assertIsNot(clones[0], node)
        self.assertEqual(
            [str(clone) for clone in 2 * node], [str(clone) for clone in clones]
        )
        self.assertEqual(
            node / 2,
            '<div id="root"><span>a</span></div><div id="root"><span>a</span></div>',
        )

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
        self.assertEqual([child.tagName for child in node], ["span"])
        self.assertIn(node.firstChild, node)
        self.assertNotIn(div("x"), node)
        self.assertEqual(
            repr(node), '<div id="root" class="hero" data-role="banner" title="banner">'
        )
        self.assertEqual(node._repr_html_(), str(node))

    def test_node_attribute_rendering_configurations(self):
        button_node = button("Go", _disabled="", _data_value="7", _get="/api/items")
        media_node = video(
            _autoplay=True, _controls=True, _loop=True, _muted=True, _playsinline=True
        )
        unsafe_node = div(_title='a " b & < c')
        original_quotes = DOMConfig.ATTRIBUTE_QUOTES
        original_htmx = DOMConfig.HTMX_ENABLED
        original_autoescape = DOMConfig.GLOBAL_AUTOESCAPE
        try:
            DOMConfig.ATTRIBUTE_QUOTES = '"'
            DOMConfig.HTMX_ENABLED = False
            DOMConfig.GLOBAL_AUTOESCAPE = False
            rendered = button_node.__attributes__
            self.assertIn(" disabled", rendered)
            self.assertIn(' data_value="7"', rendered)
            self.assertIn(' get="/api/items"', rendered)

            DOMConfig.ATTRIBUTE_QUOTES = ""
            self.assertIn(" data_value=7", button_node.__attributes__)
            media_rendered = media_node.__attributes__
            self.assertIn(" autoplay", media_rendered)
            self.assertIn(" controls", media_rendered)
            self.assertIn(" loop", media_rendered)
            self.assertIn(" muted", media_rendered)
            self.assertIn(" playsinline", media_rendered)

            DOMConfig.ATTRIBUTE_QUOTES = '"'
            DOMConfig.HTMX_ENABLED = True
            htmx_rendered = button_node.__attributes__
            self.assertIn(" data-hx-get=", htmx_rendered)

            htmx_node = div(
                _get="/api/items",
                _swap_oob=True,
                _select_oob="#toast",
                _replace_url="true",
                _disabled_elt="this",
                _history="false",
                _inherit="*",
                _validate="true",
                _sse_connect="/events",
                _sse_swap="message",
                _sse_close="done",
                _ws_connect="/chat",
                _ws_send=True,
                _hx_action="/items",
                _hx_method="delete",
                _hx_config="timeout:1000",
                **{
                    "_on:click": "this.classList.toggle('active')",
                    "_on__after_request": "this.reset()",
                    "_hx-get": "/raw",
                },
            )
            htmx_rendered = htmx_node.__attributes__
            self.assertIn(' data-hx-get="/api/items"', htmx_rendered)
            self.assertIn(' data-hx-swap-oob="true"', htmx_rendered)
            self.assertIn(' data-hx-select-oob="#toast"', htmx_rendered)
            self.assertIn(' data-hx-replace-url="true"', htmx_rendered)
            self.assertIn(' data-hx-disabled-elt="this"', htmx_rendered)
            self.assertIn(' data-hx-history="false"', htmx_rendered)
            self.assertIn(' data-hx-inherit="*"', htmx_rendered)
            self.assertIn(' data-hx-validate="true"', htmx_rendered)
            self.assertIn(' sse-connect="/events"', htmx_rendered)
            self.assertIn(' sse-swap="message"', htmx_rendered)
            self.assertIn(' sse-close="done"', htmx_rendered)
            self.assertIn(' ws-connect="/chat"', htmx_rendered)
            self.assertIn(' ws-send="true"', htmx_rendered)
            self.assertIn(' data-hx-action="/items"', htmx_rendered)
            self.assertIn(' data-hx-method="delete"', htmx_rendered)
            self.assertIn(' data-hx-config="timeout:1000"', htmx_rendered)
            self.assertIn(
                " data-hx-on:click=\"this.classList.toggle('active')\"",
                htmx_rendered,
            )
            self.assertIn(' data-hx-on--after-request="this.reset()"', htmx_rendered)
            self.assertIn(' hx-get="/raw"', htmx_rendered)

            form_rendered = form(
                button("Save", _formaction="/button", _formmethod="dialog"),
                _action="/native",
                _method="post",
            ).__attributes__
            self.assertIn(' action="/native"', form_rendered)
            self.assertIn(' method="post"', form_rendered)
            self.assertIn(
                ' preload="metadata"', video(_preload="metadata").__attributes__
            )

            DOMConfig.ATTRIBUTE_QUOTES = '"'
            DOMConfig.HTMX_ENABLED = False
            DOMConfig.GLOBAL_AUTOESCAPE = True
            self.assertEqual(
                unsafe_node.__attributes__, ' title="a &quot; b &amp; &lt; c"'
            )
            self.assertEqual(
                str(unsafe_node), '<div title="a &quot; b &amp; &lt; c"></div>'
            )
        finally:
            DOMConfig.ATTRIBUTE_QUOTES = original_quotes
            DOMConfig.HTMX_ENABLED = original_htmx
            DOMConfig.GLOBAL_AUTOESCAPE = original_autoescape

    def test_node_autoescape_and_pyml_helpers(self):
        node = div(
            Text("<unsafe>"), span(Text("ok")), _data_label="x", **{"data-mode": "demo"}
        )
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
            escaped = div("<safe>")
            self.assertIn("&lt;safe&gt;", format(escaped, ""))
            self.assertIn("&lt;safe&gt;", format(escaped, ""))
            self.assertNotIn("&amp;lt;safe&amp;gt;", format(escaped, ""))
            self.assertEqual(escaped.args, ("<safe>",))
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
            (
                HTMLAnchorElement,
                {
                    "href": "/home",
                    "target": "_blank",
                    "rel": "noopener",
                    "download": "file.txt",
                    "type": "text/html",
                },
                {
                    "href": "/home",
                    "target": "_blank",
                    "rel": "noopener",
                    "download": "file.txt",
                    "type": "text/html",
                },
            ),
            (
                HTMLAreaElement,
                {
                    "href": "/map",
                    "target": "_self",
                    "alt": "Map",
                    "coords": "0,0,10,10",
                    "shape": "rect",
                },
                {
                    "href": "/map",
                    "target": "_self",
                    "alt": "Map",
                    "coords": "0,0,10,10",
                    "shape": "rect",
                },
            ),
            (
                HTMLAudioElement,
                {
                    "autoplay": True,
                    "controls": True,
                    "loop": True,
                    "muted": True,
                    "preload": "auto",
                    "src": "/song.mp3",
                },
                {
                    "autoplay": True,
                    "controls": True,
                    "loop": True,
                    "muted": True,
                    "preload": "auto",
                    "src": "/song.mp3",
                },
            ),
            (
                HTMLBaseElement,
                {"href": "https://example.com", "target": "_top"},
                {"href": "https://example.com", "target": "_top"},
            ),
            (
                HTMLBodyElement,
                {
                    "aLink": "red",
                    "background": "/bg.png",
                    "bgColor": "#fff",
                    "link": "blue",
                    "onload": "init()",
                    "onunload": "bye()",
                    "text": "black",
                    "vLink": "purple",
                },
                {
                    "aLink": "red",
                    "background": "/bg.png",
                    "bgColor": "#fff",
                    "link": "blue",
                    "onload": "init()",
                    "onunload": "bye()",
                    "text": "black",
                    "vLink": "purple",
                },
            ),
            (
                HTMLButtonElement,
                {
                    "disabled": True,
                    "form": "signup",
                    "formaction": "/submit",
                    "formenctype": "multipart/form-data",
                    "formmethod": "post",
                    "formnovalidate": True,
                    "formtarget": "_blank",
                    "name": "go",
                    "type": "submit",
                    "value": "Send",
                },
                {
                    "disabled": True,
                    "form": "signup",
                    "formaction": "/submit",
                    "formenctype": "multipart/form-data",
                    "formmethod": "post",
                    "formnovalidate": True,
                    "formtarget": "_blank",
                    "name": "go",
                    "type": "submit",
                    "value": "Send",
                },
            ),
            (
                HTMLCanvasElement,
                {"width": 320, "height": 240},
                {"width": 320, "height": 240},
            ),
            (HTMLDataElement, {"value": "42"}, {"value": "42"}),
            (HTMLDialogElement, {"open": True}, {"open": True}),
            (
                HTMLFormElement,
                {
                    "action": "/submit",
                    "autocomplete": "on",
                    "enctype": "multipart/form-data",
                    "method": "post",
                    "name": "signup",
                    "novalidate": True,
                    "target": "_blank",
                },
                {
                    "action": "/submit",
                    "autocomplete": "on",
                    "enctype": "multipart/form-data",
                    "method": "post",
                    "name": "signup",
                    "novalidate": True,
                    "target": "_blank",
                },
            ),
            (
                HTMLIFrameElement,
                {
                    "src": "/frame",
                    "name": "hero",
                    "sandbox": "allow-scripts",
                    "allowfullscreen": True,
                },
                {
                    "src": "/frame",
                    "name": "hero",
                    "sandbox": "allow-scripts",
                    "allowfullscreen": True,
                },
            ),
            (
                HTMLImageElement,
                {
                    "alt": "hero",
                    "src": "/hero.png",
                    "crossorigin": "anonymous",
                    "height": "100",
                    "ismap": True,
                    "longdesc": "/desc",
                    "sizes": "100vw",
                    "srcset": "/hero.png 1x",
                    "usemap": "#hero",
                    "width": "200",
                },
                {
                    "alt": "hero",
                    "src": "/hero.png",
                    "crossorigin": "anonymous",
                    "height": "100",
                    "ismap": True,
                    "longdesc": "/desc",
                    "sizes": "100vw",
                    "srcset": "/hero.png 1x",
                    "usemap": "#hero",
                    "width": "200",
                },
            ),
            (
                HTMLInputElement,
                {
                    "accept": "image/*",
                    "alt": "Upload",
                    "autocomplete": "on",
                    "autofocus": True,
                    "checked": True,
                    "dirname": "dir",
                    "disabled": True,
                    "form": "signup",
                    "formaction": "/submit",
                    "formenctype": "multipart/form-data",
                    "formmethod": "post",
                    "formnovalidate": True,
                    "formtarget": "_blank",
                    "height": "10",
                    "maxlength": "20",
                    "multiple": True,
                    "name": "avatar",
                    "pattern": ".*",
                    "placeholder": "Upload",
                    "readonly": True,
                    "required": True,
                    "size": "10",
                    "src": "/image.png",
                    "step": "2",
                    "type": "file",
                    "value": "x",
                    "width": "30",
                },
                {
                    "accept": "image/*",
                    "alt": "Upload",
                    "autocomplete": "on",
                    "autofocus": True,
                    "checked": True,
                    "dirname": "dir",
                    "disabled": True,
                    "form": "signup",
                    "formaction": "/submit",
                    "formenctype": "multipart/form-data",
                    "formmethod": "post",
                    "formnovalidate": True,
                    "formtarget": "_blank",
                    "height": "10",
                    "maxlength": "20",
                    "multiple": True,
                    "name": "avatar",
                    "pattern": ".*",
                    "placeholder": "Upload",
                    "readonly": True,
                    "required": True,
                    "size": "10",
                    "src": "/image.png",
                    "step": "2",
                    "type": "file",
                    "value": "x",
                    "width": "30",
                },
            ),
            (
                HTMLLinkElement,
                {
                    "rel": "stylesheet",
                    "href": "/app.css",
                    "type": "text/css",
                    "sizes": "32x32",
                },
                {
                    "rel": "stylesheet",
                    "href": "/app.css",
                    "type": "text/css",
                    "sizes": "32x32",
                },
            ),
            (
                HTMLMetaElement,
                {
                    "charset": "utf-8",
                    "content": "text/html",
                    "http_equiv": "content-type",
                    "name": "viewport",
                },
                {
                    "charset": "utf-8",
                    "content": "text/html",
                    "http-equiv": "content-type",
                    "name": "viewport",
                },
            ),
            (
                HTMLMeterElement,
                {
                    "value": "5",
                    "_min": "0",
                    "_max": "10",
                    "low": "2",
                    "high": "8",
                    "optimum": "6",
                },
                {
                    "value": "5",
                    "_min": "0",
                    "_max": "10",
                    "low": "2",
                    "high": "8",
                    "optimum": "6",
                },
            ),
            (
                HTMLOptionElement,
                {"disabled": True, "label": "Choice", "selected": True, "value": "1"},
                {"disabled": True, "label": "Choice", "selected": True, "value": "1"},
            ),
            (
                HTMLParamElement,
                {"name": "quality", "value": "high"},
                {"name": "quality", "value": "high"},
            ),
            (
                HTMLProgressElement,
                {"value": "30", "max": "100"},
                {"value": "30", "max": "100"},
            ),
            (
                HTMLQuoteElement,
                {"cite": "https://example.com"},
                {"cite": "https://example.com"},
            ),
            (
                HTMLTextAreaElement,
                {
                    "autofocus": True,
                    "cols": "40",
                    "disabled": True,
                    "form": "signup",
                    "maxlength": "100",
                    "name": "message",
                    "placeholder": "Write",
                    "readonly": True,
                    "required": True,
                    "rows": "5",
                    "wrap": "soft",
                },
                {
                    "autofocus": True,
                    "cols": "40",
                    "disabled": True,
                    "form": "signup",
                    "maxlength": "100",
                    "name": "message",
                    "placeholder": "Write",
                    "readonly": True,
                    "required": True,
                    "rows": "5",
                    "wrap": "soft",
                },
            ),
            (HTMLTimeElement, {"datetime": "2026-03-27"}, {"datetime": "2026-03-27"}),
            (
                HTMLTrackElement,
                {
                    "kind": "subtitles",
                    "label": "English",
                    "src": "/captions.vtt",
                    "srclang": "en",
                    "default": True,
                },
                {
                    "kind": "subtitles",
                    "label": "English",
                    "src": "/captions.vtt",
                    "srclang": "en",
                    "default": True,
                },
            ),
            (
                HTMLVideoElement,
                {
                    "autoplay": True,
                    "controls": True,
                    "height": "720",
                    "loop": True,
                    "muted": True,
                    "poster": "/poster.png",
                    "preload": "auto",
                    "src": "/movie.mp4",
                    "width": "1280",
                },
                {
                    "autoplay": True,
                    "controls": True,
                    "height": "720",
                    "loop": True,
                    "muted": True,
                    "poster": "/poster.png",
                    "preload": "auto",
                    "src": "/movie.mp4",
                    "width": "1280",
                },
            ),
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
            lambda node: (
                NodeFilter.FILTER_ACCEPT
                if String(node.nodeValue).trim() != ""
                else NodeFilter.FILTER_REJECT
            ),
            False,
        )
        seen = []
        node = walker.nextNode()
        while node is not None:
            seen.append(node.nodeValue)
            node = walker.nextNode()
        self.assertEqual(seen, ["a", "b", "c"])

    def test_treewalker_parent_and_sibling_helpers(self):
        page = html(
            body(
                div(
                    span("a", _id="one"),
                    span("b", _id="two"),
                    span("c", _id="three"),
                    _id="root",
                )
            )
        )
        root = page.getElementById("root")
        walker = page.createTreeWalker(root, NodeFilter.SHOW_ELEMENT, None, False)

        self.assertEqual(walker.firstChild().getAttribute("id"), "one")
        self.assertEqual(walker.nextSibling().getAttribute("id"), "two")
        self.assertEqual(walker.previousSibling().getAttribute("id"), "one")
        self.assertIs(walker.parentNode(), root)

    def test_domquad_get_bounds(self):
        quad = DOMQuad(
            type("P", (), {"x": 5, "y": 10})(),
            type("P", (), {"x": 25, "y": 10})(),
            type("P", (), {"x": 25, "y": 30})(),
            type("P", (), {"x": 5, "y": 30})(),
        )
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
        with self.assertRaises(IndexError):
            ranges.start(-1)
        with self.assertRaises(IndexError):
            ranges.end(2)
        with self.assertRaises(TypeError):
            ranges.start("0")

    def test_text_split_text_and_document_defaults(self):
        node = div(Text("hello"))
        text = node.firstChild
        sibling = text.splitText(2)

        self.assertEqual(text.data, "he")
        self.assertEqual(sibling.data, "llo")
        self.assertEqual(node.childNodes[1], sibling)
        self.assertIs(sibling.parentNode, node)
        self.assertIsNone(text.firstChild)

        orphan_parent = div()
        orphan = Text("orphan")
        orphan.parentNode = orphan_parent
        orphan_sibling = orphan.splitText(2)
        self.assertEqual(orphan.data, "or")
        self.assertEqual(orphan_sibling.data, "phan")
        self.assertIsNone(orphan_sibling.parentNode)
        self.assertNotIn(orphan_sibling, list(orphan_parent.childNodes))

        page = Document()
        self.assertEqual(page.URL, "")
        self.assertEqual(page.baseURI, "")

    def test_document_baseuri_uses_base_href_and_inherits_to_children(self):
        page = Document(
            html(
                head(base(_href="https://example.com/docs/")),
                body(div("content", _id="content")),
            )
        )
        content = page.getElementById("content")

        self.assertEqual(page.baseURI, "https://example.com/docs/")
        self.assertEqual(content.baseURI, "https://example.com/docs/")
        page.baseURI = "https://static.example.com/"
        self.assertEqual(content.baseURI, "https://static.example.com/")

    def test_node_iadd_accepts_document_fragments(self):
        items = DocumentFragment(li("one"), li("two"))
        target = ul()

        target += items

        self.assertEqual(
            [child.textContent for child in target.children], ["one", "two"]
        )
        self.assertEqual(items.childNodes.length, 0)
        self.assertIs(target.children[0].parentNode, target)
        self.assertIs(target.children[1].parentNode, target)

    def test_character_data_methods_validate_offsets(self):
        text = Text("abcdef")

        self.assertEqual(text.substringData(1, 3), "bcd")
        self.assertEqual(text.insertData(3, "X"), "abcXdef")
        self.assertEqual(text.deleteData(3, 1), "abcdef")
        self.assertEqual(text.replaceData(1, 2, "YY"), "aYYdef")

        for method, args in (
            (text.substringData, (-1, 1)),
            (text.substringData, (99, 1)),
            (text.substringData, (0, -1)),
            (text.insertData, (-1, "x")),
            (text.deleteData, (-1, 1)),
            (text.deleteData, (0, -1)),
            (text.replaceData, (-1, 1, "x")),
            (text.replaceData, (0, -1, "x")),
            (text.splitText, (-1,)),
            (text.splitText, (99,)),
        ):
            with self.assertRaises(IndexError):
                method(*args)

        for method, args in (
            (text.substringData, ("0", 1)),
            (text.insertData, ("0", "x")),
            (text.deleteData, (0, "1")),
            (text.replaceData, (0, "1", "x")),
            (text.splitText, ("0",)),
        ):
            with self.assertRaises(TypeError):
                method(*args)

    def test_entity_reference_ordinal(self):
        self.assertEqual(EntityReference.ordinal("A"), 65)
        with self.assertRaises(ValueError):
            EntityReference.ordinal("amp")

    def test_legacy_html_element_classes(self):
        basefont = HTMLBaseFontElement(color="red", face="Arial", size="4")
        self.assertEqual(basefont.tagName, "basefont")
        self.assertEqual(basefont.getAttribute("color"), "red")

        frameset = HTMLFrameSetElement(cols="50%,50%", rows="100")
        self.assertEqual(frameset.getAttribute("cols"), "50%,50%")
        self.assertEqual(frameset.getAttribute("rows"), "100")

        isindex = HTMLIsIndexElement(prompt="Search")
        self.assertEqual(isindex.tagName, "isindex")
        self.assertEqual(isindex.getAttribute("prompt"), "Search")

        media = HTMLMediaElement(src="/movie.mp4", controls=True, muted=True)
        self.assertEqual(media.getAttribute("src"), "/movie.mp4")
        self.assertTrue(media.getAttribute("controls"))
        self.assertTrue(media.getAttribute("muted"))

        template = HTMLTemplateElement(div("inside"))
        self.assertEqual(template.tagName, "template")
        self.assertEqual(str(template.content), "<div>inside</div>")

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

    def test_document_environment_properties(self):
        doc = HTMLDocument(
            html(
                head(script("console.log('one')"), script("console.log('two')")),
                body(),
            )
        )

        self.assertEqual(doc.designMode, "off")
        doc.designMode = "on"
        self.assertEqual(doc.designMode, "on")
        self.assertEqual(doc.currentScript.tagName, "script")

        first_script = doc.scripts[0]
        doc.currentScript = first_script
        self.assertIs(doc.currentScript, first_script)

        doc.cookie = "session=abc123; Path=/"
        doc.cookie = "theme=dark"
        self.assertIn("session=abc123", doc.cookie)
        self.assertIn("theme=dark", doc.cookie)

        self.assertIsInstance(doc.lastModified, str)
        doc.lastModified = "Sat, 27 Mar 2026 12:00:00 GMT"
        self.assertEqual(doc.lastModified, "Sat, 27 Mar 2026 12:00:00 GMT")

        doc.referrer = "https://ref.example"
        self.assertEqual(doc.referrer, "https://ref.example")

    def test_document_timeline_and_documenttimeline(self):
        doc = HTMLDocument(html(body()))

        timeline = doc.timeline
        self.assertIsInstance(timeline, DocumentTimeline)
        self.assertIs(timeline.document, doc)
        self.assertEqual(timeline.originTime, 0.0)

        first = timeline.currentTime
        second = doc.timeline.currentTime
        self.assertIs(doc.timeline, timeline)
        self.assertGreaterEqual(second, first)

    def test_form_submit_dispatches_submit_event(self):
        page = html(body(form(input(_name="email"), _id="signup")))
        signup = page.getElementById("signup")
        calls = []

        signup.addEventListener(
            "submit", lambda event: calls.append((event.type, event.submitter))
        )
        result = signup.submit()

        self.assertTrue(result)
        self.assertEqual(calls, [("submit", None)])

    def test_form_request_submit_and_button_click_dispatch_submitter(self):
        page = html(
            body(form(button("Send", _id="send", _type="submit"), _id="signup"))
        )
        signup = page.getElementById("signup")
        send = page.getElementById("send")
        calls = []

        signup.addEventListener(
            "submit", lambda event: calls.append((event.type, event.submitter))
        )
        signup.requestSubmit(send)
        send.click()

        self.assertEqual(calls[0], ("submit", send))
        self.assertEqual(calls[1], ("submit", send))

        send.addEventListener("click", lambda event: event.preventDefault())
        self.assertFalse(send.click())
        self.assertEqual(len(calls), 2)

    def test_form_submit_dispatches_formdata_after_uncanceled_submit(self):
        page = html(
            body(
                form(
                    input(_name="email", _value="me@example.com"),
                    input(_name="plan", _type="radio", _value="free"),
                    input(_name="plan", _type="radio", _value="pro", _checked=True),
                    textarea("hello", _name="notes"),
                    button(
                        "Send",
                        _id="send",
                        _type="submit",
                        _name="intent",
                        _value="save",
                    ),
                    _id="signup",
                )
            )
        )
        signup = page.getElementById("signup")
        send = page.getElementById("send")
        calls = []

        signup.addEventListener(
            "submit", lambda event: calls.append((event.type, event.submitter))
        )
        signup.addEventListener(
            "formdata",
            lambda event: calls.append(
                (event.type, isinstance(event, FormDataEvent), dict(event.formData))
            ),
        )

        self.assertTrue(signup.requestSubmit(send))
        self.assertEqual(calls[0], ("submit", send))
        self.assertEqual(
            calls[1],
            (
                "formdata",
                True,
                {
                    "email": "me@example.com",
                    "plan": "pro",
                    "notes": "hello",
                    "intent": "save",
                },
            ),
        )

        signup.addEventListener("submit", lambda event: event.preventDefault())
        self.assertFalse(signup.requestSubmit(send))
        self.assertEqual(len([call for call in calls if call[0] == "formdata"]), 1)

    def test_input_checkbox_and_radio_click_dispatch_events(self):
        page = html(
            body(
                form(
                    input(_id="check", _type="checkbox"),
                    input(_id="radio_a", _type="radio", _name="group"),
                    input(_id="radio_b", _type="radio", _name="group"),
                )
            )
        )
        checkbox = page.getElementById("check")
        radio_a = page.getElementById("radio_a")
        radio_b = page.getElementById("radio_b")
        events = []

        checkbox.addEventListener(
            "input", lambda event: events.append((event.type, checkbox.checked))
        )
        checkbox.addEventListener(
            "change", lambda event: events.append((event.type, checkbox.checked))
        )
        radio_a.addEventListener(
            "change", lambda event: events.append(("radio-a", radio_a.checked))
        )
        radio_b.addEventListener(
            "change", lambda event: events.append(("radio-b", radio_b.checked))
        )

        checkbox.click()
        radio_a.click()
        radio_b.click()

        self.assertTrue(checkbox.checked)
        self.assertFalse(radio_a.checked)
        self.assertTrue(radio_b.checked)
        self.assertEqual(events[:2], [("input", True), ("change", True)])
        self.assertIn(("radio-a", True), events)
        self.assertIn(("radio-b", True), events)

        blocked_checkbox = input(_type="checkbox")
        blocked_events = []
        blocked_checkbox.addEventListener("click", lambda event: event.preventDefault())
        blocked_checkbox.addEventListener(
            "input", lambda event: blocked_events.append(event.type)
        )
        blocked_checkbox.addEventListener(
            "change", lambda event: blocked_events.append(event.type)
        )

        self.assertFalse(blocked_checkbox.click())
        self.assertFalse(blocked_checkbox.checked)
        self.assertEqual(blocked_events, [])

    def test_select_and_textarea_value_helpers_dispatch_events(self):
        picker = select(
            option("One", value="1"), option("Two", value="2"), _name="choice"
        )
        notes = textarea("hello", _name="notes")
        events = []

        picker.addEventListener(
            "input", lambda event: events.append(("select-input", picker.value))
        )
        picker.addEventListener(
            "change", lambda event: events.append(("select-change", picker.value))
        )
        notes.addEventListener(
            "input", lambda event: events.append(("textarea-input", notes.value))
        )
        notes.addEventListener(
            "change", lambda event: events.append(("textarea-change", notes.value))
        )

        picker.selectIndex(1)
        notes.setValue("updated")

        self.assertEqual(picker.selectedIndex, 1)
        self.assertEqual(picker.value, "2")
        self.assertEqual(notes.value, "updated")
        self.assertEqual(
            events,
            [
                ("select-input", "2"),
                ("select-change", "2"),
                ("textarea-input", "updated"),
                ("textarea-change", "updated"),
            ],
        )

    def test_beforeinput_can_cancel_text_value_helpers(self):
        email = input(_name="email", _value="start@example.com")
        notes = textarea("hello", _name="notes")
        events = []

        email.addEventListener(
            "beforeinput",
            lambda event: events.append(
                (event.type, isinstance(event, InputEvent), event.data, event.inputType)
            ),
        )
        notes.addEventListener("beforeinput", lambda event: event.preventDefault())

        self.assertEqual(email.setValue("changed@example.com"), "changed@example.com")
        self.assertEqual(notes.setValue("blocked"), "hello")
        self.assertEqual(
            events,
            [
                (
                    "beforeinput",
                    True,
                    "changed@example.com",
                    "insertReplacementText",
                )
            ],
        )

    def test_common_form_value_properties_stringify_values(self):
        number_input = input(_value=0)
        checkbox = input(_type="checkbox")
        radio = input(_type="radio")
        zero_option = option("Zero", value=0)
        submitter = button("Save", value=0)

        self.assertEqual(number_input.type, "text")
        self.assertEqual(number_input.value, "0")
        self.assertEqual(checkbox.value, "on")
        self.assertEqual(radio.value, "on")
        self.assertEqual(zero_option.value, "0")
        self.assertEqual(submitter.value, "0")

        number_input.type = "email"
        submitter.value = 1
        self.assertEqual(number_input.type, "email")
        self.assertEqual(submitter.value, "1")

    def test_form_validity_invalid_events_and_formnovalidate(self):
        email = input(_name="email", _required=True, _id="email")
        submitter = button("Send", _type="submit", _id="send")
        signup = form(email, submitter, _id="signup")
        invalid_calls = []
        submit_calls = []

        email.addEventListener(
            "invalid", lambda event: invalid_calls.append(event.type)
        )
        signup.addEventListener("submit", lambda event: submit_calls.append(event.type))

        self.assertFalse(signup.requestSubmit(submitter))
        self.assertEqual(invalid_calls, ["invalid"])
        self.assertEqual(submit_calls, [])

        submitter.setAttribute("formnovalidate", True)
        self.assertTrue(signup.requestSubmit(submitter))
        self.assertEqual(submit_calls, ["submit"])

    def test_dialog_details_and_media_dispatch_events(self):
        dialog = HTMLDialogElement()
        details_el = HTMLDetailsElement()
        media = HTMLMediaElement(src="/movie.mp4")
        events = []

        dialog.addEventListener(
            "toggle",
            lambda event: events.append(
                (
                    "dialog-toggle",
                    isinstance(event, ToggleEvent),
                    event.oldState,
                    event.newState,
                    dialog.open,
                )
            ),
        )
        dialog.addEventListener(
            "close", lambda event: events.append(("dialog-close", event.reason))
        )
        details_el.addEventListener(
            "toggle",
            lambda event: events.append(
                (
                    "details-toggle",
                    isinstance(event, ToggleEvent),
                    event.oldState,
                    event.newState,
                    details_el.open,
                )
            ),
        )
        for event_name in (
            "loadstart",
            "loadedmetadata",
            "loadeddata",
            "play",
            "playing",
            "pause",
        ):
            media.addEventListener(
                event_name,
                lambda event, name=event_name: events.append(("media", name)),
            )
        media.addEventListener(
            "addtrack",
            lambda event: events.append(
                (
                    "track",
                    event.type,
                    isinstance(event, TrackEvent),
                    event.track["kind"],
                )
            ),
        )
        media.addEventListener(
            "removetrack",
            lambda event: events.append(
                (
                    "track",
                    event.type,
                    isinstance(event, TrackEvent),
                    event.track["kind"],
                )
            ),
        )

        dialog.showModal()
        dialog.close("done")
        details_el.toggle()
        details_el.toggle()
        media.load()
        self.assertTrue(media.play())
        self.assertIsNone(media.pause())
        captions = media.addTextTrack("captions", "English", "en")
        media.removeTextTrack(captions)

        self.assertIn(("dialog-toggle", True, "closed", "open", True), events)
        self.assertIn(("dialog-close", "done"), events)
        self.assertIn(("details-toggle", True, "closed", "open", True), events)
        self.assertIn(("details-toggle", True, "open", "closed", False), events)
        self.assertIn(("track", "addtrack", True, "captions"), events)
        self.assertIn(("track", "removetrack", True, "captions"), events)
        self.assertEqual(media.textTracks, [])
        self.assertEqual(
            [item for item in events if item[0] == "media"],
            [
                ("media", "loadstart"),
                ("media", "loadedmetadata"),
                ("media", "loadeddata"),
                ("media", "play"),
                ("media", "playing"),
                ("media", "pause"),
            ],
        )

    def test_form_reset_restores_default_control_state(self):
        email = input(_name="email", _value="start@example.com")
        accept = input(_type="checkbox", _checked=True)
        picker = select(
            option("One", value="1", selected=True), option("Two", value="2")
        )
        notes = textarea("hello")
        signup = form(email, accept, picker, notes)

        email.setValue("changed@example.com", dispatch_events=False)
        accept.checked = False
        picker.setValue("2", dispatch_events=False)
        notes.setValue("updated", dispatch_events=False)

        signup.reset()

        self.assertEqual(email.value, "start@example.com")
        self.assertTrue(accept.checked)
        self.assertEqual(picker.value, "1")
        self.assertEqual(notes.value, "hello")

    def test_control_validity_helpers_and_image_lifecycle_events(self):
        required_input = input(_required=True)
        required_select = select(
            option("Choose", value=""), option("One", value="1"), _required=True
        )
        required_textarea = textarea("", _required=True)
        image = HTMLImageElement(src="/hero.png")
        events = []

        image.addEventListener("loadstart", lambda event: events.append(event.type))
        image.addEventListener("load", lambda event: events.append(event.type))
        image.addEventListener("error", lambda event: events.append(event.type))
        image.addEventListener("abort", lambda event: events.append(event.type))

        self.assertFalse(required_input.checkValidity())
        self.assertFalse(required_input.reportValidity())
        self.assertFalse(required_select.checkValidity())
        self.assertFalse(required_textarea.checkValidity())

        required_input.value = "ok"
        required_select.value = "1"
        required_textarea.value = "hello"

        self.assertTrue(required_input.checkValidity())
        self.assertTrue(required_select.reportValidity())
        self.assertTrue(required_textarea.checkValidity())

        image.load()
        self.assertTrue(image.decode())
        self.assertIsNone(image.error())
        self.assertIsNone(image.abort())
        self.assertEqual(events, ["loadstart", "load", "load", "error", "abort"])

    def test_required_radio_group_validity_uses_group_checked_state(self):
        free = input(_type="radio", _name="plan", _value="free", _required=True)
        pro = input(_type="radio", _name="plan", _value="pro")
        signup = form(free, pro)

        self.assertFalse(signup.checkValidity())

        pro.checked = True
        self.assertTrue(signup.checkValidity())
        self.assertTrue(free.checkValidity())
        self.assertFalse(free.checked)
        self.assertTrue(pro.checked)

    def test_radio_groups_ignore_unnamed_inputs(self):
        first = input(_type="radio")
        second = input(_type="radio")
        required = input(_type="radio", _required=True)
        signup = form(first, second, required)

        first.checked = True
        second.checked = True

        self.assertTrue(first.checked)
        self.assertTrue(second.checked)
        self.assertFalse(signup.checkValidity())

        required.checked = True
        self.assertTrue(signup.checkValidity())

    def test_form_elements_returns_live_form_controls_collection(self):
        signup = form(
            input(_name="email", _id="email"),
            fieldset(input(_name="nested")),
            select(option("One", value="1"), _name="choice"),
            textarea("hello", _name="bio"),
            button("Save", _name="submitter"),
            div("ignored"),
            _id="signup",
        )

        controls = signup.elements
        self.assertIsInstance(controls, HTMLFormControlsCollection)
        self.assertEqual(controls.length, 6)
        self.assertEqual(controls.item(0).getAttribute("name"), "email")
        self.assertEqual(controls.namedItem("choice").tagName, "select")
        self.assertEqual(controls["submitter"].tagName, "button")

    def test_form_elements_named_item_returns_live_radio_node_list(self):
        free = input(_type="radio", _name="plan", _value="free")
        pro = input(_type="radio", _name="plan", _value="pro", _checked=True)
        signup = form(free, pro)

        group = signup.elements.namedItem("plan")

        self.assertIsInstance(group, RadioNodeList)
        self.assertEqual(group.length, 2)
        self.assertEqual(group.value, "pro")
        self.assertIs(group.item(0), free)

        group.value = "free"
        self.assertTrue(free.checked)
        self.assertFalse(pro.checked)
        self.assertEqual(group.value, "free")

        enterprise = input(_type="radio", _name="plan", _value="enterprise")
        signup.appendChild(enterprise)
        self.assertEqual(group.length, 3)
        self.assertEqual(list(group.values()), [free, pro, enterprise])

        empty = RadioNodeList("missing")
        self.assertEqual(empty.length, 0)
        self.assertEqual(empty.value, "")

    def test_html_collection_item_returns_none_for_invalid_indexes(self):
        items = ul(li("one"), li("two")).getElementsByTagName("li")

        self.assertIs(items.item(0), items[0])
        self.assertIsNone(items.item(-1))
        self.assertIsNone(items.item(2))

    def test_html_collection_named_item_skips_nodes_without_attributes(self):
        signup = form(input(_name="email"), _id="signup")
        dotted = div(_id="named.item.with.periods")
        items = HTMLCollection(
            [Text("loose"), div(_id="hit"), span(_name="named"), dotted, signup]
        )

        self.assertIs(items.namedItem("hit"), items[1])
        self.assertIs(items.namedItem("named"), items[2])
        self.assertIs(items["named.item.with.periods"], dotted)
        self.assertIs(
            items["signup.elements.email"], signup.elements.namedItem("email")
        )
        self.assertIsNone(items.namedItem("missing"))
        self.assertIsNone(items["signup.elements.missing"])

    def test_select_options_returns_live_options_collection(self):
        picker = select(
            option("One", value="1", _id="one"),
            optgroup(
                option("Two", value="2", _id="two"),
                option("Three", value="3"),
                _label="Group",
            ),
            _id="picker",
        )

        options = picker.options
        self.assertIsInstance(options, HTMLOptionsCollection)
        self.assertEqual(options.length, 3)
        self.assertEqual(options.item(1).getAttribute("value"), "2")
        self.assertEqual(options.namedItem("one").textContent, "One")

        options.add(option("Four", value="4"))
        self.assertEqual(options.length, 4)
        options.remove(0)
        self.assertEqual(options.length, 3)
        self.assertEqual(options.item(0).textContent, "Two")

        options.item(0).selected = True
        options.item(1).selected = True
        self.assertFalse(options.item(0).selected)
        self.assertTrue(options.item(1).selected)

    def test_range_get_client_rects_returns_domrectlist(self):
        container = div(span("a"), span("b"))
        rng = Range()
        rng.setStart(container, 0)
        rng.setEnd(container, 2)

        rects = rng.getClientRects()
        self.assertIsInstance(rects, DOMRectList)
        self.assertEqual(rects.length, 2)
        self.assertIsInstance(rects.item(0), DOMRect)
        self.assertIsNone(rects.item(10))

    def test_domrect_and_domrectreadonly_geometry_helpers(self):
        readonly = DOMRectReadOnly(10, 20, -5, 15)
        self.assertEqual(readonly.left, 5)
        self.assertEqual(readonly.right, 10)
        self.assertEqual(readonly.top, 20)
        self.assertEqual(readonly.bottom, 35)

        rect = DOMRect.fromRect(readonly)
        rect.x = 30
        rect.width = 12
        self.assertEqual(rect.left, 30)
        self.assertEqual(rect.right, 42)
        self.assertEqual(rect.toJSON()["width"], 12)

    def test_dommatrix_readonly_and_mutable_operations(self):
        readonly = DOMMatrixReadOnly(1, 0, 0, 1, 10, 20)
        self.assertTrue(readonly.is2D)
        self.assertFalse(readonly.isIdentity)
        self.assertEqual(
            (readonly.a, readonly.d, readonly.e, readonly.f), (1.0, 1.0, 10.0, 20.0)
        )

        point = readonly.transformPoint(DOMPoint(2, 3))
        self.assertEqual((point.x, point.y), (12.0, 23.0))

        matrix = DOMMatrix()
        matrix.translateSelf(5, 7).scaleSelf(2, 3)
        moved = matrix.transformPoint(DOMPoint(1, 1))
        self.assertEqual((moved.x, moved.y), (12.0, 24.0))

        inverse = DOMMatrix.fromMatrix(matrix).invertSelf()
        original = inverse.transformPoint(moved)
        self.assertAlmostEqual(original.x, 1.0)
        self.assertAlmostEqual(original.y, 1.0)

        multiplied = DOMMatrixReadOnly(1, 0, 0, 1, 1, 2).multiply(
            DOMMatrixReadOnly(1, 0, 0, 1, 3, 4)
        )
        self.assertEqual((multiplied.e, multiplied.f), (4.0, 6.0))

    def test_domquad_from_rect_uses_rect_bounds(self):
        quad = DOMQuad.fromRect(DOMRect(5, 10, 20, 30))
        bounds = DOMQuad.getBounds(quad)
        self.assertEqual(
            (bounds.left, bounds.top, bounds.width, bounds.height), (5, 10, 20, 30)
        )

    def test_resize_observer_reports_initial_and_changed_rects(self):
        target = div()
        target.style.width = "10px"
        target.style.height = "20px"

        entries = []
        observer = ResizeObserver(lambda records, obs: entries.extend(records))
        observer.observe(target)

        self.assertEqual(len(entries), 1)
        self.assertEqual(
            (entries[0].contentRect.width, entries[0].contentRect.height), (10, 20)
        )

        target.style.width = "30px"
        target.getBoundingClientRect()

        self.assertEqual(len(entries), 2)
        self.assertEqual(entries[-1].contentRect.width, 30)

    def test_intersection_observer_reports_visibility_changes(self):
        root = div()
        root.style.left = "0px"
        root.style.top = "0px"
        root.style.width = "100px"
        root.style.height = "100px"

        target = div()
        target.style.left = "10px"
        target.style.top = "10px"
        target.style.width = "20px"
        target.style.height = "20px"
        root.appendChild(target)

        entries = []
        observer = IntersectionObserver(
            lambda records, obs: entries.extend(records), {"root": root}
        )
        observer.observe(target)

        self.assertTrue(entries[-1].isIntersecting)
        self.assertGreater(entries[-1].intersectionRatio, 0)

        target.style.left = "200px"
        target.getBoundingClientRect()

        self.assertFalse(entries[-1].isIntersecting)
        self.assertEqual(entries[-1].intersectionRatio, 0.0)

    def test_performance_observer_reports_marks_and_measures(self):
        from domonic.javascript import performance

        performance.clearMarks()
        performance.clearMeasures()
        entries = []
        observer = PerformanceObserver(lambda records, obs: entries.extend(records))
        observer.observe({"entryTypes": ["mark", "measure"]})

        performance.mark("dom-start")
        performance.measure("dom-total", "dom-start")

        self.assertEqual([entry.entryType for entry in entries], ["mark", "measure"])
        self.assertEqual(entries[0].name, "dom-start")
        self.assertEqual(entries[1].name, "dom-total")

    def test_domonic_matches(self):
        content = ul(_id="birds").html(
            li("Orange-winged parrot"),
            li("Philippine eagle", _class="endangered"),
            li("Great white pelican"),
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
                assert (
                    "The " + bird.textContent + " is endangered!"
                    == "The Philippine eagle is endangered!"
                )
        assert birds[1].matches("li.endangered")
        assert birds[1].matches(".safe, .endangered")
        assert birds[1].closest("ul") is content
        assert content.closest("li") is None

    def test_matches_requires_all_class_tokens(self):
        partial = li("partial", _class="foo")
        complete = li("complete", _class="foo bar")

        self.assertFalse(partial.matches(".foo.bar"))
        self.assertFalse(partial.matches("li.foo.bar"))
        self.assertTrue(complete.matches(".foo.bar"))
        self.assertTrue(complete.matches("li.foo.bar"))

    def test_matches_supports_compound_attribute_selectors(self):
        link = a(
            "Twitter",
            _id="social",
            _class="nav-link social",
            _href="https://twitter.com/domonic",
            _rel="external help",
            _lang="en-GB",
            **{"_data-state": "ready"},
        )

        self.assertTrue(link.matches("a#social.nav-link[href*=twitter]"))
        self.assertTrue(link.matches("a[rel~=help]"))
        self.assertTrue(link.matches("a[lang|=en]"))
        self.assertTrue(link.matches("[data-state=ready]"))
        self.assertFalse(link.matches("a[href^='/']"))
        self.assertFalse(link.matches("a[rel~=hel]"))

    def test_getElementsByTagName(self):
        content = ul(_id="birds").html(
            li("Orange-winged parrot"),
            li("Philippine eagle", _class="endangered"),
            li("Great white pelican"),
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

    def test_private_get_tags_uses_exact_tag_name(self):
        page = Document(
            html(
                head(link(_rel="stylesheet", _href="/main.css")),
                body(ul(li("one")), input(_type="text")),
            )
        )

        self.assertEqual(page._get_tags("li"), ["<li>one</li>"])
        self.assertEqual(page._get_tags("input"), ['<input type="text"/>'])
        self.assertEqual(page._get_tags("links"), [])

    # def test_domonic_closest(self):

    def test_sanitize(self):
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
        assert (
            str(s3)
            == '<div style="cool"><span style="font-weight: bold">hello</span></div>'
        )

        # Drop <span id>: <span class='theclass' style='font-weight: bold'>...</span>
        s4 = Sanitizer({"dropAttributes": {"id": ["span"]}}).sanitize(sample)
        # print("4::::", s4)
        assert (
            str(s4)
            == '<div style="cool"><span class="theclass" style="font-weight: bold">hello</span></div>'
        )

        # Drop id, everywhere: <span class='theclass' style='font-weight: bold'>...</span>
        s5 = Sanitizer({"dropAttributes": {"id": ["*"]}}).sanitize(sample)
        assert (
            str(s5)
            == '<div style="cool"><span class="theclass" style="font-weight: bold">hello</span></div>'
        )

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
        assert str(comment("foo", "bar")) == "<!--foobar-->"

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

        doc = html(
            div(_id="contentarea").html(p("Some ", span("text")), b("Bold text"))
        )

        rootnode = doc.getElementById("contentarea")
        # print(rootnode)
        walker = doc.createTreeWalker(rootnode, NodeFilter.SHOW_ELEMENT, None, False)

        assert (
            str(walker.currentNode)
            == '<div id="contentarea"><p>Some <span>text</span></p><b>Bold text</b></div>'
        )
        # print(walker.firstChild())
        # print(walker.firstChild())
        # print(walker.firstChild())
        # print(walker.firstChild())

        visited = [walker.currentNode.tagName]

        # Step through and alert all child nodes
        # for n in walker.nextNode():
        while walker.nextNode():
            # print('+++', walker.nextNode())
            visited.append(walker.currentNode.tagName)

        self.assertEqual(visited, ["div", "p", "span", "b"])

        # //Go back to the first child node of the collection and alert it
        walker.currentNode = (
            rootnode  # //reset TreeWalker pointer to point to root node
        )
        # print('>>', walker.firstChild()) # calling it breaks it cos it moves it?. is it like an iterator then?
        assert walker.firstChild().tagName.lower() == "p"  # //alerts P

        return

        # test 2
        doc = html(ul(_id="mylist").html(li("List 1"), li("List 2"), li("List 3")))

        rootnode = doc.getElementById("mylist")
        walker = doc.createTreeWalker(rootnode, NodeFilter.SHOW_ELEMENT, None, False)

        window.alert(
            len(walker.currentNode.childNodes)
        )  # //alerts 7 (includes text nodes)
        window.alert(len(walker.currentNode.getElementsByTagName("*")))  # //alerts 3

        # test 3
        doc = html(
            div(_id="main").html(p("This is a ", span("paragraph")), b("Bold text"))
        )
        mainDiv = doc.getElementById("main")
        walker = doc.createTreeWalker(mainDiv, NodeFilter.SHOW_ELEMENT, None, False)
        console.log(walker)

        treeWalker = document.createTreeWalker(
            mainDiv,
            NodeFilter.SHOW_TEXT,
            lambda node: (
                NodeFilter.FILTER_ACCEPT
                if (String(node.nodeValue).trim() != "")
                else NodeFilter.FILTER_REJECT
            ),
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
                assert (
                    item.nextSibling is None
                ), f"nextSibling in position {i} should be None"
            else:
                assert (
                    item.nextSibling is node[i + 1]
                ), f"nextSibling in position {i} is incorrect ({item.nextSibling})"

        # Check previousSibling
        for i, item in enumerate(node):
            if i == 0:
                assert (
                    item.previousSibling is None
                ), f"previousSibling in position {i} should be None"
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
                    assert (
                        value.parentNode is node
                    ), f"parentNode is incorrect ({value.parentNode})"
                    self._checkPositions(value)

                elif isinstance(value, list):
                    for item in value:
                        assert (
                            getattr(item, "parentNode", node) is node
                        ), f"parentNode is incorrect ({item.parentNode})"
                        self._checkPositions(item)

                elif isinstance(value, dict):
                    for item in value.values():
                        assert (
                            getattr(item, "parentNode", node) is node
                        ), f"parentNode is incorrect ({item.parentNode})"
                        self._checkPositions(item)

    def test_truthiness(self):
        doc = Document()
        assert doc  # to support `if doc: ...`
        assert bool(doc)  # more explicitly

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
        text_parent = Document.createElement("node")
        text_parent.append("lead")
        assert text_parent.firstChild == "lead"
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

    def test_child_collections_are_live(self):
        node = div(span("one", _id="one"), " gap ")
        one = node.querySelector("#one")
        child_nodes = node.childNodes
        children = node.children
        two = p("two", _id="two")

        node.append(two)

        self.assertIsInstance(child_nodes, NodeList)
        self.assertEqual(child_nodes.length, 3)
        self.assertIs(child_nodes[-1], two)
        self.assertEqual(
            [child.getAttribute("id") for child in children], ["one", "two"]
        )
        self.assertEqual(node.childElementCount, 2)

        removed = child_nodes.pop()
        self.assertIs(removed, two)
        self.assertIsNone(two.parentNode)
        self.assertEqual([child.getAttribute("id") for child in children], ["one"])

        child_nodes.append(two)
        self.assertIs(two.parentNode, node)
        child_nodes.insert(0, "lead ")
        self.assertEqual(node.firstChild, "lead ")
        del child_nodes[0]
        self.assertIs(node.firstChild, one)

        children.clear()
        self.assertEqual(node.args, (" gap ",))
        self.assertIsNone(one.parentNode)
        self.assertIsNone(two.parentNode)

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

    def test_element_child_helpers_ignore_text_and_comments(self):
        node = div(
            "lead",
            span("one", _id="one"),
            Document.createTextNode("gap"),
            Comment("note"),
            p("two", _id="two"),
            "tail",
        )
        one = node.querySelector("#one")
        two = node.querySelector("#two")

        self.assertEqual(node.childElementCount, 2)
        self.assertEqual(node.children, [one, two])
        self.assertIs(node.firstElementChild(), one)
        self.assertIs(node.lastElementChild(), two)
        self.assertIs(one.nextElementSibling, two)
        self.assertIs(two.previousElementSibling, one)
        self.assertIsNone(two.nextElementSibling)
        self.assertIsNone(one.previousElementSibling)

    def test_childnode_text_helpers_insert_in_the_right_order(self):
        node = div(Document.createTextNode("one"), span("two", _id="two"))
        text_node = node.firstChild
        after = p("after", _id="after")
        before = strong("before", _id="before")

        text_node.after(" after text ", after)
        text_node.before(before, " before text ")

        self.assertEqual(
            str(node),
            '<div><strong id="before">before</strong> before text one after text '
            '<p id="after">after</p><span id="two">two</span></div>',
        )
        self.assertEqual(text_node.nextSibling, " after text ")
        self.assertEqual(after.previousSibling, " after text ")
        self.assertEqual(before.nextSibling, " before text ")

        replacement = em("replacement", _id="replacement")
        text_node.replaceWith("replacement text ", replacement)
        self.assertEqual(
            str(node),
            '<div><strong id="before">before</strong> before text replacement text '
            '<em id="replacement">replacement</em> after text '
            '<p id="after">after</p><span id="two">two</span></div>',
        )
        self.assertEqual(
            [getattr(child, "id", None) for child in node.children],
            ["before", "replacement", "after", "two"],
        )
        self.assertIs(replacement.parentNode, node)
        self.assertIsNone(text_node.parentNode)

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

        source = Document.createElement("source")
        target = Document.createElement("target")
        moved = Document.createElement("moved")
        old = Document.createElement("old")
        source.appendChild(moved)
        target.appendChild(old)
        result = target.replaceChild(moved, old)
        self.assertIs(result, old)
        self.assertEqual(source.childNodes.length, 0)
        self.assertIs(target.firstChild, moved)
        self.assertIs(moved.parentNode, target)
        self.assertIsNone(old.parentNode)

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

    def test_removeChild_only_removes_direct_children(self):
        inner = div(span("kid", _id="kid"), _id="inner")
        node = div(inner)
        kid = node.querySelector("#kid")

        self.assertIsNone(node.removeChild(kid))
        self.assertIs(kid.parentNode, inner)
        self.assertTrue(node.contains(kid))

        removed = inner.removeChild(kid)
        self.assertIs(removed, kid)
        self.assertIsNone(kid.parentNode)
        self.assertFalse(node.contains(kid))

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
        returned = node.appendChild(frag)
        # print(node)
        assert returned is frag, f'"{returned}" != "{frag}"'
        assert frag.childNodes.length == 0, f"{frag.childNodes.length} != 0"
        assert node[0] is one, f'"{node[0]}" != "{one}"'
        assert node[1] is two, f'"{node[1]}" != "{two}"'
        assert node[2] is three, f'"{node[2]}" != "{three}"'
        assert two.parentNode is node, f'"{two.parentNode}" != "{node}"'
        assert three.parentNode is node, f'"{three.parentNode}" != "{node}"'
        self._checkPositions(node)

    def test_appendChild_moves_existing_nodes_between_parents(self):
        old_parent = div(span("kid", _id="kid"))
        new_parent = div()
        kid = old_parent.querySelector("#kid")

        returned = new_parent.appendChild(kid)

        self.assertIs(returned, kid)
        self.assertEqual(old_parent.children, [])
        self.assertEqual(new_parent.children, [kid])
        self.assertIs(kid.parentNode, new_parent)
        self.assertFalse(old_parent.contains(kid))
        self.assertTrue(new_parent.contains(kid))

    def test_duplicate_node_insertion_arguments_keep_last_position(self):
        node = div(p("tail", _id="tail"))
        child = span("kid", _id="kid")

        node.append(child, " gap ", child)

        self.assertEqual(
            [getattr(child, "id", None) for child in node.childNodes],
            ["tail", None, "kid"],
        )
        self.assertEqual(node.childNodes.length, 3)
        self.assertIs(child.parentNode, node)

        node.prepend(child, child)

        self.assertEqual(
            [getattr(child, "id", None) for child in node.childNodes],
            ["kid", "tail", None],
        )
        self.assertEqual(node.childNodes.length, 3)

        node.replaceChildren(child, " mid ", child)

        self.assertEqual(
            [getattr(child, "id", None) for child in node.childNodes], [None, "kid"]
        )
        self.assertEqual(node.childNodes.length, 2)
        self.assertIs(child.parentNode, node)

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
        node.args = (
            node.args[:2] + (two,) + node.args[2:]
        )  # does same as node.insert(1, two)
        node.args = (
            node.args[:3] + (three,) + node.args[3:]
        )  # does same as node.insert(2, three)
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
        node.prepend(frag)

        assert frag.childNodes.length == 0, f"{frag.childNodes.length} != 0"
        assert node[0] is three, f'"{node[0]}" != "{three}"'
        assert node[1] is four, f'"{node[1]}" != "{four}"'
        assert node[2] is one, f'"{node[2]}" != "{one}"'
        assert node[3] is two, f'"{node[3]}" != "{two}"'
        assert three.parentNode is node, f'"{three.parentNode}" != "{node}"'
        assert four.parentNode is node, f'"{four.parentNode}" != "{node}"'
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
        one.setAttribute("id", "source")
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
        assert res[0].parentNode is res

        shallow = one.cloneNode(False)
        assert type(shallow) is type(one), f'"{type(shallow)}" != "{type(one)}"'
        assert shallow.getAttribute("id") == "source"
        assert len(shallow.childNodes) == 0
        assert shallow.parentNode is None

    def test_cloneNode_from_attached_tree_is_disconnected(self):
        page = html(body(div(span("kid", _id="kid"), _id="source")))
        source = page.querySelector("#source")

        deep_clone = source.cloneNode(deep=True)
        shallow_clone = source.cloneNode(False)

        self.assertIsNone(deep_clone.parentNode)
        self.assertIs(deep_clone.ownerDocument, page)
        self.assertFalse(deep_clone.isConnected)
        self.assertIs(deep_clone.firstChild.parentNode, deep_clone)
        self.assertIs(deep_clone.firstChild.ownerDocument, page)
        self.assertFalse(deep_clone.firstChild.isConnected)
        self.assertIsNone(shallow_clone.parentNode)
        self.assertIs(shallow_clone.ownerDocument, page)
        self.assertFalse(shallow_clone.isConnected)
        self.assertEqual(shallow_clone.childNodes.length, 0)
        self.assertIs(source.parentNode, page.body)

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

    def test_normalize_preserves_element_siblings_after_text(self):
        lead = Document.createTextNode("lead ")
        middle = span(
            Document.createTextNode("mid "),
            Document.createTextNode("text"),
            _id="middle",
        )
        tail = Document.createTextNode(" tail")
        node = div(lead, middle, tail, em("end", _id="end"))

        node.normalize()

        self.assertEqual(
            str(node),
            '<div>lead <span id="middle">mid text</span> tail<em id="end">end</em></div>',
        )
        self.assertIsNone(lead.parentNode)
        self.assertIsNone(tail.parentNode)
        self.assertIs(middle.parentNode, node)
        self.assertIs(node.querySelector("#end").parentNode, node)
        self.assertEqual(middle.args, ("mid text",))

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

    def test_namednodemap_live_attribute_operations(self):
        node = div(_id="hero", _class="banner")
        attrs = node.attributes

        self.assertEqual(attrs.length, 2)
        self.assertEqual(attrs.item(0).name, "id")
        self.assertEqual(attrs.item(1).name, "class")
        self.assertIsNone(attrs.item(5))
        self.assertEqual(attrs["id"].value, "hero")
        self.assertEqual(attrs.getNamedItem("class").value, "banner")
        self.assertIn("id", attrs)
        self.assertEqual(attrs.keys(), ["id", "class"])

        replaced = attrs.setNamedItem(Attr("title", "Hello"))
        self.assertIsNone(replaced)
        self.assertEqual(node.getAttribute("title"), "Hello")

        attrs["data-state"] = "ready"
        self.assertEqual(node.getAttribute("data-state"), "ready")

        removed = attrs.removeNamedItem("class")
        self.assertEqual(removed.name, "class")
        self.assertFalse(node.hasAttribute("class"))

    def test_namednodemap_namespace_helpers_and_parser_style_access(self):
        node = div()
        attrs = node.attributes

        attrs["xlink:href"] = Attr("xlink:href", "#icon")
        self.assertEqual(node.getAttribute("xlink:href"), "#icon")
        self.assertEqual(
            attrs.getNamedItemNS("http://www.w3.org/1999/xlink", "href").value,
            "#icon",
        )

        removed = attrs.removeNamedItemNS("http://www.w3.org/1999/xlink", "href")
        self.assertEqual(removed.name, "xlink:href")
        self.assertIsNone(attrs.getNamedItem("xlink:href"))

        attrs["role"] = Attr("role", "presentation")
        del attrs["role"]
        self.assertFalse(node.hasAttribute("role"))

    def test_aria_reflected_properties(self):
        node = button("X")
        node.role = "button"
        node.ariaLabel = "Close dialog"
        node.ariaMultiLine = "false"
        node.ariaValueMax = "10"
        node.ariaBrailleLabel = "cls"

        self.assertEqual(node.getAttribute("role"), "button")
        self.assertEqual(node.ariaLabel, "Close dialog")
        self.assertEqual(node.getAttribute("aria-multiline"), "false")
        self.assertEqual(node.getAttribute("aria-valuemax"), "10")
        self.assertIn('aria-braillelabel="cls"', str(node))

        del node.ariaLabel
        self.assertIsNone(node.ariaLabel)
        self.assertFalse(node.hasAttribute("aria-label"))

    def test_aria_element_reference_properties(self):
        target = div(_id="panel")
        label = span("Preferences", _id="label")
        control = button("Open", _id="control")
        root = div(label, control, target)

        control.ariaControlsElements = [target]
        control.ariaLabelledByElements = label
        control.ariaActiveDescendantElement = target

        self.assertEqual(control.getAttribute("aria-controls"), "panel")
        self.assertEqual(control.ariaControlsElements, [target])
        self.assertEqual(control.getAttribute("aria-labelledby"), "label")
        self.assertEqual(control.ariaLabelledByElements, [label])
        self.assertIs(control.ariaActiveDescendantElement, target)

        del control.ariaControlsElements
        self.assertEqual(root.getElementById("control"), control)
        self.assertFalse(control.hasAttribute("aria-controls"))

    def test_custom_state_set(self):
        states = CustomStateSet(["open", "active"])
        self.assertEqual(states.size, 2)
        self.assertTrue(states.has("open"))
        self.assertEqual(list(states), ["open", "active"])
        self.assertEqual(
            list(states.entries()), [("open", "open"), ("active", "active")]
        )

        self.assertIs(states.add("open"), states)
        self.assertEqual(states.size, 2)
        self.assertTrue(states.delete("open"))
        self.assertFalse(states.delete("missing"))
        self.assertEqual(list(states.keys()), ["active"])

        seen = []
        states.forEach(lambda value, key, owner: seen.append((value, key, owner)))
        self.assertEqual(seen, [("active", "active", states)])

        with self.assertRaises(ValueError):
            states.add(" ")

        states.clear()
        self.assertEqual(len(states), 0)

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
        self.assertEqual(node.nodeValue, expected)

        node.textContent = "plain"
        assert node.textContent == "plain"
        assert node.args == ("plain",)
        assert one.parentNode is None
        assert two.parentNode is None
        assert three.parentNode is two

    def test_nodeValue_replaces_children_and_detaches_old_nodes(self):
        node = div(span("old", _id="old"))
        old = node.querySelector("#old")

        node.nodeValue = "plain"

        self.assertEqual(node.nodeValue, "plain")
        self.assertEqual(node.args, ("plain",))
        self.assertIsNone(old.parentNode)

    def test_insert_before_missing_reference_gets_clear_error(self):
        parent = div(span("one"))
        missing = span("missing")

        with self.assertRaisesRegex(ValueError, "reference_node is not a child"):
            parent.insertBefore(em("new"), missing)

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

    def test_internal_subset(self):
        self.assertIsNone(self.dtype.internalSubset)
        self.dtype.internalSubset = "<!ELEMENT html ANY>"
        self.assertEqual(self.dtype.internalSubset, "<!ELEMENT html ANY>")

    def test_dtd_collections(self):
        dtype = DocumentType("root")
        entity = Entity("writer", publicId="pub", systemId="sys")
        notation = Notation("png", systemId="image/png")

        dtype.entities._seq.append(entity)
        dtype.notations._seq.append(notation)

        self.assertEqual(dtype.entities.length, 1)
        self.assertIs(dtype.entities.item(0), entity)
        self.assertIs(dtype.entities.getNamedItem("writer"), entity)
        self.assertEqual(entity.nodeType, Node.ENTITY_NODE)
        self.assertEqual(entity.nodeName, "writer")

        self.assertEqual(dtype.notations.length, 1)
        self.assertIs(dtype.notations.item(0), notation)
        self.assertIs(dtype.notations.getNamedItem("png"), notation)
        self.assertEqual(notation.nodeType, Node.NOTATION_NODE)
        self.assertEqual(notation.nodeName, "png")


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

        self.assertFalse(tokens.toggle("two"))
        self.assertFalse(tokens.contains("two"))
        self.assertTrue(tokens.toggle("three"))
        self.assertTrue(tokens.contains("three"))
        self.assertTrue(tokens.toggle("four", True))
        self.assertTrue(tokens.contains("four"))
        self.assertFalse(tokens.toggle("four", False))
        self.assertFalse(tokens.contains("four"))
        self.assertEqual(tokens.item(0), "one")
        self.assertEqual(tokens.item(10), None)
        self.assertEqual(tokens.toString(), "one three")
        self.assertEqual(sample.className, "one three")

    def test_class_list_empty_elements_are_mutable(self):
        sample = div()
        tokens = sample.classList

        self.assertIsInstance(tokens, DOMTokenList)
        self.assertEqual(tokens.toString(), "")

        tokens.add("ready", "active")

        self.assertEqual(tokens.toString(), "ready active")
        self.assertEqual(sample.className, "ready active")

    def test_class_list_normalizes_whitespace_and_duplicates(self):
        sample = div(_class="  one\t two\none  ")
        tokens = sample.classList

        self.assertEqual(list(tokens), ["one", "two"])
        tokens.add("two", "three")

        self.assertEqual(tokens.toString(), "one two three")
        self.assertEqual(tokens.value, "one two three")
        self.assertEqual(sample.className, "one two three")

        tokens.value = " three  four\tthree "

        self.assertEqual(list(tokens), ["three", "four"])
        self.assertEqual(tokens.value, "three four")
        self.assertEqual(sample.className, "three four")

    def test_class_list_rejects_invalid_tokens(self):
        sample = div(_class="one")
        tokens = sample.classList

        for method in (tokens.add, tokens.remove, tokens.toggle, tokens.contains):
            with self.assertRaises(ValueError):
                method("")
            with self.assertRaises(ValueError):
                method("two words")

    def test_replace_and_iteration_helpers(self):
        sample = div(_class="one two three")
        tokens = sample.classList

        self.assertTrue(tokens.replace("two", "deux"))
        self.assertEqual(list(tokens), ["one", "deux", "three"])
        self.assertEqual(sample.className, "one deux three")

        self.assertFalse(tokens.replace("missing", "unused"))
        self.assertTrue(tokens.replace("deux", "three"))
        self.assertEqual(list(tokens), ["one", "three"])
        self.assertEqual(sample.className, "one three")

        self.assertEqual(list(tokens.keys()), [0, 1])
        self.assertEqual(list(tokens.values()), ["one", "three"])
        self.assertEqual(list(tokens.entries()), [(0, "one"), (1, "three")])

        seen = []
        tokens.forEach(
            lambda currentValue, currentIndex, listObj: seen.append(
                (currentValue, currentIndex, listObj)
            )
        )
        self.assertEqual(seen, [("one", 0, tokens), ("three", 1, tokens)])

        with self.assertRaises(ValueError):
            tokens.replace("", "four")
        with self.assertRaises(ValueError):
            tokens.replace("one", "two words")

    def test_class_list_objects_remain_live_after_attribute_changes(self):
        sample = div(_class="one")
        tokens = sample.classList

        sample.className = "two three"
        self.assertEqual(list(tokens), ["two", "three"])
        self.assertEqual(tokens.length, 2)
        self.assertTrue(tokens.contains("two"))
        self.assertEqual(tokens.item(1), "three")

        tokens.add("four")
        self.assertEqual(sample.className, "two three four")

        sample.setAttribute("class", "five")
        self.assertEqual(tokens.toString(), "five")
        tokens.remove("five")
        self.assertEqual(sample.className, "")


if __name__ == "__main__":
    unittest.main()
