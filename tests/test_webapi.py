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


if __name__ == '__main__':
    unittest.main()
