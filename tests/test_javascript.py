"""
    test_javascript
    ~~~~~~~~~~~~~~~
    unit tests for domonic.javascript
"""

import time
import unittest
# import requests
# from mock import patch

from domonic.javascript import Object
from domonic.javascript import Math
from domonic.javascript import Global
from domonic.javascript import Window
from domonic.javascript import Date
from domonic.javascript import URL
from domonic.javascript import Array
from domonic.javascript import String

from domonic.javascript import *


from inspect import stack


class TestCase(unittest.TestCase):

    # domonic.javascript.Math

    def test_object(self):

        o = Object()
        print(o)
        print(type(o))

        myObj = Object()
        string = 'myString'
        rand = Math.random()
        obj1 = Object()
        myObj.type = 'Dot syntax'
        myObj['date created'] = 'String with space'
        myObj[string] = 'String value'
        myObj[rand] = 'Random Number'
        myObj[obj1] = 'Object'
        myObj[''] = 'Even an empty string'


        assert myObj.type == 'Dot syntax'
        assert myObj['date created'] == 'String with space'
        assert myObj[string] == 'String value'
        assert myObj[rand] == 'Random Number'
        # assert myObj[obj1] == 'Object' # TODO - does js do this?
        assert myObj[''] == 'Even an empty string'

        assert o is not myObj

        myCar = Object()
        propertyName = 'make'
        myCar[propertyName] = 'Ford'
        assert myCar[propertyName] == 'Ford'
        propertyName = 'model'
        myCar[propertyName] = 'Mustang'
        assert myCar[propertyName] == 'Mustang'

        def showProps(obj, objName):
            result = ''
            for i in obj:
                if obj.hasOwnProperty(i):
                    result += objName + "." + str(i) + "= " + obj[i] + "\n"
            return result

        showProps(myCar, "myCar")
        # print(showProps(myCar, "myCar"))

        obj = {'a': 1}
        copy = Object.assign({}, obj)
        assert copy == {'a': 1}

        # print(Object().fromEntries())
        arr = [['0', 'a'], ['1', 'b'], ['2', 'c']]
        obj = Object.fromEntries(arr)
        print(obj)
        assert obj == {'0': "a", '1': "b", '2': "c"}

        obj = {'foo': 'bar', 'baz': 42}
        print(Object.entries(obj))
        assert Object.entries(obj) == [['foo', 'bar'], ['baz', 42]]

        # array like object
        obj = {'0': 'a', '1': 'b', '2': 'c'}
        assert Object.entries(obj) == [['0', 'a'], ['1', 'b'], ['2', 'c']]

        # def listAllProperties(o):
        #     result = []
        #     objectToInspect = o
        #     while objectToInspect != None:
        #         print(objectToInspect)
        #         objectToInspect = Object.getPrototypeOf(objectToInspect)
        #         result = Array(result).concat(Object.getOwnPropertyNames(objectToInspect))

        #     return result
        # print(listAllProperties(myCar))


        # array like object with random key ordering
        # anObj = {'100': 'a', '2': 'b', '7': 'c'}
        # print(anObj)
        # print(Object.entries(anObj))
        # assert Object.entries(anObj) == [['2', 'b'], ['7', 'c'], ['100', 'a']]

        # returns an empty array for any primitive type
        assert Object.entries(100) == []

        # iterate through key-value gracefully
        obj = {'a': 5, 'b': 7, 'c': 9}
        for key, value in Object.entries(obj):
            print(f'{key} {value}')  # "a 5", "b 7", "c 9"

        # class Car(Object):
        #     def __init__(self, make, model, year):
        #         super().__init__()
        #         self.make = make
        #         self.model = model
        #         self.year = year
        #         # super().__init__()

        # mycar = Car('Eagle', 'Talon TSi', 1993)
        # print(mycar)
        # print(mycar.make)
        # print(mycar.__attribs__)

    # Animal properties and method encapsulation


    # TODO - to get reference back to self. in a dict it needs to readd the method and pass self
    Animal = {
        'type': 'Invertebrates',  # Default value of properties
        # 'displayType': lambda self: print("STACK!!!!!",stack()[1].function)  # Method which will display type of Animal
        'displayType': lambda self: print(self.type)
    }
    animal1 = Object.create(Animal)
    print(animal1)
    # print(animal1['type'])
    print(animal1.__dict__)
    animal1.displayType(animal1)  # Output:Invertebrates #TODO - need to work without passing self

    fish = Object.create(Animal)
    fish.type = 'Fishes'
    fish.displayType(animal1)  # Output:Fishes



    def test_domonic_abs(self):
        # python -m unittest tests.test_javascript.TestCase.test_domonic_abs

        self.assertEqual(Math.abs('-1'), 1)
        self.assertEqual(Math.abs(-2), 2)
        self.assertEqual(Math.abs(None), 0)
        self.assertEqual(Math.abs(''), 0)
        self.assertEqual(Math.abs([]), 0)
        self.assertEqual(Math.abs([2]), 2)
        self.assertEqual(Math.abs([1, 2]), None)
        self.assertEqual(Math.abs({}), None)
        self.assertEqual(Math.abs('string'), None)
        self.assertEqual(Math.abs(), None)

        self.assertEqual(100, Math.abs(-100.0))

    def test_domonic_LN2(self):
        print("test_domonic_LN2:::")
        print(Math.LN2)

    def test_domonic_LOG2E(self):
        print("test_domonic_LOG2E:::")
        print(Math.LOG2E)

    def test_domonic_LOG10E(self):
        print("test_domonic_LOG10E:::")
        print(Math.LOG10E)

    def test_domonic_PI(self):
        print("test_domonic_PI:::")
        print(Math.PI)

    def test_domonic_SQRT1_2(self):
        print("test_domonic_SQRT1_2:::")
        print(Math.SQRT1_2)

    def test_domonic_SQRT2(self):
        print("test_domonic_SQRT2:::")
        print(Math.SQRT2)

    def test_domonic_acos(self):
        print("test_domonic_acos:::")
        # print( Math.acos(-100) ) # TODO - fails numbers greater than 1 or lower than -1 - raise Error?
        print(Math.acos(0.5))

    def test_domonic_acosh(self):
        print("test_domonic_acosh:::")
        # print( Math.acosh(-100) ) # TODO - fails under zero - rause error?
        print(Math.acosh(100))

    def test_domonic_asin(self):
        print("test_domonic_asin:::")
        # print( Math.asin(-100) ) # TODO - fails numbers greater than 1 or lower than -1 - raise Error?
        print(Math.asin(0.5))

    def test_domonic_asinh(self):
        print("test_domonic_asinh:::")
        print(Math.asinh(-100))

    def test_domonic_atan(self):
        print("test_domonic_atan:::")
        print(Math.atan(-100))

    def test_domonic_atan2(self):
        print("test_domonic_atan2:::")
        print(Math.atan2(-100, 100))

    def test_domonic_atanh(self):
        print("test_domonic_atanh:::")
        # print( Math.atanh(-100) ) # TODO - fails numbers greater than 1 or lower than -1 - raise Error?
        print(Math.atanh(0.5))

    def test_domonic_cbrt(self):
        print("test_domonic_cbrt:::")
        # print( Math.cbrt(-100) ) # TODO - fails on negative numbers - raise Error?
        print(Math.cbrt(100))

    def test_domonic_ceil(self):
        print("test_domonic_ceil:::")
        print(Math.ceil(-100))

    def test_domonic_cos(self):
        print("test_domonic_cos:::")
        print(Math.cos(-100))

    def test_domonic_cosh(self):
        print("test_domonic_cosh:::")
        print(Math.cosh(-100))

    def test_domonic_E(self):
        self.assertEqual(2.718281828459045, Math.E)

    def test_domonic_exp(self):
        print("test_domonic_exp:::")
        print(Math.exp(-100))

    def test_domonic_floor(self):
        print("test_domonic_floor:::")
        print(Math.floor(-100))

    def test_domonic_LN10(self):
        self.assertEqual(2.302585092994046, Math.LN10)

    def test_domonic_log(self):
        print("test_domonic_log:::")
        # print( Math.log(-100,100) ) # TODO - fails on negative numbers - raise Error?
        print(Math.log(100, 10))

    def test_domonic_max(self):
        print("test_domonic_max:::")
        print(Math.max(-100, 100))

    def test_domonic_min(self):
        print("test_domonic_min:::")
        print(Math.min(-100, 100))

    def test_domonic_random(self):
        print("test_domonic_random:::")
        print(Math.random())

    def test_domonic_round(self):
        print("test_domonic_round:::")
        print(Math.round(-100))

    def test_domonic_pow(self):
        print("test_domonic_pow:::")
        print(Math.pow(100, 10))

    def test_domonic_sin(self):
        print("test_domonic_sin:::")
        print(Math.sin(-100))

    def test_domonic_sinh(self):
        print("test_domonic_sinh:::")
        print(Math.sinh(-100))

    def test_domonic_sqrt(self):
        print("test_domonic_sqrt:::")
        # print( Math.sqrt(-100) ) # TODO - fails on negative numbers - raise Error? check js behaviour
        print(Math.sqrt(100))

    def test_domonic_tan(self):
        print("test_domonic_tan:::")
        print(Math.tan(-100))

    def test_domonic_tanh(self):
        print("test_domonic_tanh:::")
        print(Math.tanh(-100))

    def test_domonic_trunc(self):
        print("test_domonic_trunc:::")
        print(Math.trunc(-100))

    # def test_domonic_math_test(self):
    #   print("test_domonic_math_test:::")
    #   print( Math.abs(-100)*Math.random()*10 )

    # domonic.javascript.Global

    def test_domonic_isNaN(self):
        self.assertEqual(True, Global.isNaN("yo"))
        self.assertEqual(False, Global.isNaN(1))

    def test_domonic_Number(self):
        self.assertEqual(1, Global.Number(1))
        self.assertEqual("NaN", Global.Number("test"))
        self.assertEqual(2, Global.Number("1") + Global.Number("1.0"))

    def test_domonic_window_console_log(self):
        # window = Window()
        # Window().console.log("test this")
        # window.console.log("test this")

        # c = Console()
        # c.log()
        # Console.log('test')
        pass

    def test_domonic_window_alert(self):
        # Window().alert("test this 2")
        window = Window()
        window.alert("test this 2")

    def test_domonic_window_document_baseURI(self):
        # Window().alert("test this 2")
        # window = Window()
        # window.alert("test this 2")
        # print(window.document.baseURI)
        # window.document.baseURI = "eventual.technology"
        # print("=",window.document.baseURI)

        pass

    '''
    def test_domonic_window_location(self):
        # Window().alert("test this 2")
        window = Window()
        # window.alert("test this 2")
        print("window.location")
        print(window.location)
        window.location = "eventual.technology"
        print("window.location.uri")
        print(window.location)
        print(str(window.location))
        print(window.location.href)
    '''

    def test_domonic_global_encodeURIComponent(self):

        msg = "Test encoding this string! 123 aweseome"
        enc_msg = Global.encodeURIComponent(msg)
        print(enc_msg)
        # print( Global.decodeURIComponent(bytes(enc_msg, encoding="UTF-8")))
        print(Global.decodeURIComponent(enc_msg))

        # Window().alert("test this 2")
        # window = Window()
        # window.alert("test this 2")
        # print(window.document.baseURI)
        # window.document.baseURI = "eventual.technology"
        # print("=",window.document.baseURI)
        pass

    def test_javascript_date(self):
        print("test_javascript_date::::::::::::::::::")
        d = Date()
        print(d.getDate())
        print(d.getDay())
        print(d.getFullYear())
        print(d.getHours())
        print(d.getMilliseconds())
        print(d.getMinutes())
        print(d.getMonth())
        print(d.getSeconds())
        print(d.getTime())
        # print( d.getTimezoneOffset() )
        print(d.getUTCDate())
        print(d.getUTCDay())
        print(d.getUTCFullYear())
        print(d.getUTCHours())
        print(d.getUTCMilliseconds())
        print(d.getUTCMinutes())
        print(d.getUTCMonth())
        print(d.getUTCSeconds())
        print(d.getYear())
        print(d.now())
        # print( d.onstorage() )
        # print( d.ontimeupdate() )
        print(d.parse("July 1981"))
        print(d.setDate(1))
        print(d.setFullYear('1982'))
        print(d.setHours(2))
        # print( d.setItem() )
        print(d.setMilliseconds(12345))
        print(d.setMinutes(10))
        print(d.setMonth(10))
        print(d.setSeconds(10))
        print(d.setTime(1000))
        print(d.setUTCDate(1))
        print(d.setUTCFullYear(1928))
        print(d.setUTCHours(3))
        print(d.setUTCMilliseconds(54321))
        print(d.setUTCMinutes(50))
        print(d.setUTCMonth(3))
        print(d.setUTCSeconds(11))
        print(d.setYear(1987))
        print(d.toDateString())
        print(d.toGMTString())
        print(d.toJSON())
        print(d.toISOString())
        print(d.toLocaleDateString())
        print(d.toLocaleString())
        print(d.toLocaleTimeString())
        print(d.toTimeString())
        print(d.toUTCString())
        print(d.UTC())

    # def test_domonic_parse(self):
        # page = domonic.parse("<html><body>'some content'</body></html>")
        # page = domonic.parse("<html><body></body></html>")
        # print(page)

    # def test_domonic_get(self):
    #     print("test_domonic_get-----------=-----------=-----------=-----------=-----------=-----------=-----------=")
    #     page = eval(domonic.get("http://eventual.technology"))
    #     dir(page)

    def test_javascript_url(self):
        url = URL('https://somesite.com/blog/article-one#some-hash')
        print('TESTS:')
        print(url)
        print(url.toString())
        print(url.href)
        print(url.protocol)
        url.protocol = "http"
        print(url.protocol)
        print(url.host)
        print(url.pathname)
        print(url.hash)

        # print(url.origin)

        url = URL('https://somesite.com:8000/blog/article-one#some-hash')
        print(url.protocol)
        print(url.host)
        print(url.hostname)
        print(url.pathname)
        print(url.hash)
        print(url.port)

        url.host = 'test.com'
        print('host:', url.host)
        print('href:', url.href)
        print(url.hostname)
        print(url.pathname)
        print(url.hash)
        print(url.port)
        url.port = 8983
        print(url.toString())

    # def test_javascript_window(self):
        # print('asdf')
        # print(window)
        # print(window.location)

        # window.location = "https://google.com"
        # print(window.location.href)
        # pass

    def test_javascript_array(self):
        print("test_javascript_array")
        myarr = Array("1", "2", 3, {"4": "four"}, 5, [6])
        print(myarr)
        print(type(myarr))
        print(myarr.length)
        print(myarr.includes("1"))
        print(myarr.includes(3))
        print(myarr.includes(10))
        print(myarr.indexOf(10))
        print(myarr.indexOf("1"))
        print(myarr.indexOf([6]))
        print(myarr[1])
        print(len(myarr))
        print(myarr.join('---'))  #  TODO - test some js ones
        print(myarr.lastIndexOf("1"))
        print(myarr.lastIndexOf(3))
        print(myarr.reverse())
        print(myarr.slice(0, 1))
        print(myarr.splice(1))
        # print(myarr.splice(2))
        # print(myarr.splice(3))
        # print(myarr.splice(4))
        print(myarr.splice(3, 3, "a", "b", "c"))
        print(myarr)
        print(myarr.pop())
        print(myarr)
        myarr.push(7)
        print(myarr)
        print(myarr.unshift('z'))
        print(myarr)
        print(myarr.shift())
        print(myarr)
        # print(myarr.concat())

        # myarr.sort()
        # myarr.fill()
        # myarr.isArray()?
        # myarr.map()
        # myarr.reduce()
        # myarr.reduceRight()
        # myarr.some()
        pass

    def test_javascript_interval(self):

        def hi():
            print('hi')
            pass

        test = window.setInterval(hi, 1)
        print('im going to do some stuff in the background')

        # keep the test open to see if the intervals fire
        time.sleep(2)

        print('running')
        window.clearInterval(test)
        print('ran')

    def test_javascript_Number(self):
        print(Number.MAX_VALUE)
        pass

    def test_javascript_fetch(self):

        TEST_DOMAIN = 'http://eventual.technology'
        urls = ['http://google.com', 'http://linkedin.com', 'http://eventual.technology']  # use your own domains

        print('run 1')
        results = window.fetch(TEST_DOMAIN)
        results.then(lambda r: print(r.text))
        print('run 1 FINISHED')

        def somefunc(response):
            print("I'm a callback", response.ok)
            return response

        mydata = window.fetch(TEST_DOMAIN).then(somefunc)
        print(mydata)
        print(mydata.data)
        print(mydata.data.text)

        print('run 1111')
        results = window.fetch_set(urls)
        print(results)
        print(list(results))
        for r in results:
            if r is not None:
                print(r.ok)
                # print(r.text)

        print('run 2')
        results = window.fetch_threaded(urls)
        print(results)
        print(list(results))
        for r in results:
            if r is not None:
                print(r.ok)
                # print(r.text)

        print('run 3')
        results = window.fetch_pooled(urls, timeout=2)
        print(results)
        for r in results:
            if r is not None:
                print(r.ok)
                # print(r.text)

        print('run 4')
        results = window.fetch(urls[0])
        print(results)
        results.then(lambda r: print(r.text) if r is not None else None)

        print('ran ===')
        # return

        # TEST REGULAR

        global _results

        def get_things():
            global _results
            _results = window.fetch(urls[0])
            print('sup::', _results)

        print('BEFORE')
        test = window.setInterval(get_things, 2000)
        print('AFTER')
        print(_results)
        time.sleep(4)
        print('LATER')
        print(_results)

        print('MAKE SURE TO CLEAR INTERVAL AND RESET RESULTS!')
        window.clearInterval(test)
        _results = []

        # TEST - Threaded interval triggering a CPU pool
        def get_things():
            global _results
            _results = window.fetch_pooled(urls)
            print('sup::', _results)

        print('Are you ready')
        test = window.setInterval(get_things, 1000)
        print("wait, where my results?")
        print(_results)
        time.sleep(4)
        print("Ahhh nice")
        print(_results)
        for r in _results:
            print(r.ok)
            # print(r.text)

        window.clearInterval(test)

        # nice 😎

    def test_javascript_promise(self):
        def do_test(resolve, reject):
            global _intID
            _intID = window.setInterval(resolve, 2000, 'amazing!')
            resolve("once!")
        myPromise = Promise(lambda resolve, reject: do_test(resolve, reject))
        myPromise.then(lambda successMessage: str(successMessage))
        time.sleep(3)
        window.clearInterval(_intID)
        myPromise.then(lambda successMessage: print("Yay! " + str(successMessage)))

    def test_javascript_string(self):
        print("test_javascript_string")
        mystr = String("Some String")

        assert(mystr.toLowerCase() == "some string")
        assert(mystr.toUpperCase() == "SOME STRING")

        print(type(mystr))
        print(mystr.length)
        assert(mystr.length == 11)

        assert(mystr.repeat(2) == "Some StringSome String")
        print(mystr)
        print(mystr)
        print(mystr)
        assert(mystr.startsWith('S'))
        # assert(mystr.endsWith('g'))

        print(">>", mystr.substr(1))
        assert(mystr.substr(1) == 'ome String')

        # def substring
        # slice
        # trim
        # charAt
        # charCodeAt
        # fromCharCode
        # test
        # replace
        # localeCompare
        # search
        # substr
        # toLocaleLowerCase
        # toLocaleUpperCase
        # compile
        # lastIndex
        # test


    def test_javascript_URLSearchParams(self):
        print("test_javascript_URLSearchParams")

        paramsString = "q=test&topic=api"
        searchParams = URLSearchParams(paramsString)

        # Iterate the search parameters.
        for p in searchParams:
            print(p)

        assert searchParams.has("topic") == True  # True
        # print( searchParams.get("topic") )
        assert searchParams.get("topic") == "api"  # True
        # searchParams.getAll("topic"); # ["api"]
        assert searchParams.get("foo") is None  # true
        print(searchParams.toString())
        searchParams.append("topic", "webdev")
        print(searchParams.toString())
        assert searchParams.toString() == "q=test&topic=api&topic=webdev"
        searchParams.set("topic", "More webdev")
        assert searchParams.toString() == "q=test&topic=More+webdev"
        searchParams.delete("topic")
        assert searchParams.toString() == "q=test"

        # GOTCHAS

        paramsString1 = "http://example.com/search?query=%40"
        searchParams1 = URLSearchParams(paramsString1)

        assert searchParams1.has("query") == False
        assert searchParams1.has("http://example.com/search?query") == True

        assert searchParams1.get("query") == None
        searchParams1.get("http://example.com/search?query")  # "@" (equivalent to decodeURIComponent('%40'))

        paramsString2 = "?query=value"
        searchParams2 = URLSearchParams(paramsString2)
        print(searchParams2)
        assert searchParams2.has("query") == True

        url = URL("http://example.com/search?query=%40")

        searchParams3 = URLSearchParams(url.search)

        print(searchParams3)
        # print(str(searchParams3))
        # assert searchParams3.has("query") == True

        base64 = window.btoa(String.fromCharCode(19, 224, 23, 64, 31, 128))  # base64 is "E+AXQB+A"
        print(base64)
        searchParams = URLSearchParams("q=foo&bin=" + str(base64))  # q=foo&bin=E+AXQB+A
        # getBin = searchParams.get("bin")  # "E AXQB A" + char is replaced by spaces
        # print(getBin)
        # window.btoa(window.atob(getBin))  # "EAXQBA==" no error thrown
        # window.btoa(String.fromCharCode(16, 5, 208, 4))  # "EAXQBA==" decodes to wrong binary value
        # getBin.replace(r'/ /g', "+")  # "E+AXQB+A" is one solution

        # or use set to add the parameter, but this increases the query string length
        # searchParams.set("bin2", base64)  # "q=foo&bin=E+AXQB+A&bin2=E%2BAXQB%2BA" encodes + as %2B
        # searchParams.get("bin2")  # "E+AXQB+A"

    def test_javascript_FormData(self):
        print("test_javascript_FormData")
        # f = form(input(_type="text", _name="test", _id="test"))
        # d = FormData(f)
        # print(d)
        pass

    def test_javascript_Worker(self):
        print("test_javascript_Worker")
        # myWorker = Worker('/worker.py')
        # first = document.querySelector('input#number1')
        # second = document.querySelector('input#number2')
        # first.onchange = lambda evt : \
        #     myWorker.postMessage([first.value, second.value])
        #     print('Message posted to worker')
        pass

    def test_javascript_at(self):
        print("test_javascript_at")
        myarr = Array(['a', 'b', 'c', 'd'])
        assert myarr.at(-1) == 'd'
        myarr = ['a', 'b', 'c', 'd']
        myarr = Array(myarr)
        assert myarr.at(-1) == 'd'
        myarr = Array('a', 'b', 'c', 'd')
        assert myarr.at(-1) == 'd'


    # def test_javascript_Node(self):
        # url = require('url');        
        # console.log(url.domainToASCII('español.com'))
        # console.log(url.domainToASCII('??.com'))
        # console.log(url.domainToASCII('xn--iñvalid.com'))
        # console.log(url.domainToUnicode('español.com'))
        # console.log(url.domainToUnicode('??.com'))
        # console.log(url.domainToUnicode('xn--iñvalid.com'))


    # def test_javascript_call(self):

    #     class Product():
    #         def __init__(self, name, price):
    #             self.name = name
    #             self.price = price

    #     class Food():
    #         def __init__(self, name, price):
    #             Function(Product).call(self, name, price)
    #             self.category = 'food'

    #     class Toy():
    #         def __init__(self, name, price):
    #             Function(Product).call(self, name, price)
    #             self.category = 'toy'

    #     cheese = Food('feta', 5)
    #     fun = Toy('robot', 40)

    #     print(cheese)
    #     print(fun)

    def test_javascript_called(self):

        from domonic.decorators import called
        from domonic.dQuery import º, dQuery_el

        # import time
        # @called(lambda:time.sleep(2))
        # def anon( data=None ):
        #     print("func you")
        #     print(data)

        # import time
        # @called(time.sleep(2)) # calls right away without lambda. but doesnt pass data. can i detect it?
        # def anon( data=None ):
        #     print("func you")
        #     print(data)

        @called(
            lambda: º.ajax('https://www.google.com'),
            lambda err: print('error:', err))
        def success(data=None):
            print("sweet!")
            print(data.text)

        from domonic.decorators import iife

        @iife()
        def sup():
            print("sup!")
            return True


    def test_javascript_numbersandstrings(self):
        print("test_javascript_numbersnstrings")

        n = Number(1)
        n2 = Number(2)
        print(n + n2)

        s = String('a')
        s2 = String('b')
        print(s + s2)
        print(s * n2)

        test = String("test")
        # print(test - 2) # considering allowing this

        print(test[0:1])

        print(test.toUpperCase())
        print(test.toLowerCase())
        print(test.toLocaleLowerCase())
        print(test.toLocaleUpperCase())




_intID = None
_results = []


if __name__ == '__main__':
    unittest.main()
