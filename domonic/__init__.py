# -*- coding: utf-8 -*-
"""
    domonic
    ~~~~~
    
    Generate HTML using python 3
"""

__version__ = "0.0.3"

from typing import *

from .html import *
from .dom import *
from .javascript import *

import requests

class domonic:

    @staticmethod
    def get(url:str):
        ''' downloads html and converts to domonic '''
        r = requests.get( url )
        return domonic.parse(r.text)

    @staticmethod
    def print(domonic) -> str :
        ''' outputs HTML str '''
        # TODO - prettify by using newlines in returned content to save installing this?
        # from html5print import HTMLBeautifier
        # render(HTMLBeautifier.beautify(render(output), 4), 'index.html')
        pass

    @staticmethod
    def parse(html:str) -> str :
        ''' HTML as input and returns domonic '''

        print("attempting to parse the page")

        # - TODO - should probs pretty it up first and strip want cant be
        # turn all tags into class definitions.
        # check closing tags. turn to closed bracks
        # create strings around content and remove white space
        # put underscores on attributes

        import re

        html = ''.join(html.split('<!DOCTYPE HTML>'))
        html = ''.join(html.split('<!doctype html>'))
        
        # html = "<html><body>some content</body></html>"

        # "style","script"

        htmltags = ["html","span","button","link","form","nav","details","summary","header","head","body","meta","title","div","footer","img","a","p","h1","h2","h3","h4","h5","h6","hr","ul","ol","li","time","template","label","input","small","strong","option","select"]

        for tag in htmltags:

            print(tag)

            reg = f"<{tag}>"
            pattern = re.compile(reg)
            html = re.sub( pattern, f'{tag}(', html )#, flags=re.IGNORECASE )

            # second pass. atrributed
            reg = f"<{tag}"
            pattern = re.compile(reg)
            html = re.sub( pattern, f'{tag}(', html )#, flags=re.IGNORECASE )
            
            reg = f"</{tag}>"
            pattern = re.compile(reg)
            html = re.sub( pattern, ')', html)#, flags=re.IGNORECASE )

            reg = f"/>"
            pattern = re.compile(reg)
            html = re.sub( pattern, ')', html)#, flags=re.IGNORECASE )

            # second pass. single no closed. i.e meta
            # reg = f">"
            # pattern = re.compile(reg)
            # html = re.sub( pattern, ')', html)#, flags=re.IGNORECASE )

            # need to get all the ( and )
            # count left and right. until it changes.
            # left > (((()
            # right > )(()



            # tags = re.findall(pattern,html)
            # if len(tags) < 1:
                # continue
            # print(tags)
            # for count,each in enumerate(tags):
                # print(count,each)
                # tags[count] = tag + "(" + each + ")"
            # html = ''.join(tags)
            # print(count, html)
        
        print(html)
        

        # close any tags that arent properly self closing
        flag=False
        for index,char in enumerate(html):
            if char=="(":flag=True
            if char==")":flag=False
            if char==">" and flag is True:
                html = f"{html[:index]},{html[index+1:]}" # replace it for a ','
                # TODO - if its self closing. replace for a ')' instead

        # strip any comments
        cleaned=[]
        for line in html.splitlines():
            print('smelly fanny!')
            if "<!" in line:
                continue
            cleaned.append(line)
        html = '\n'.join(cleaned)

        # return eval('print("test")')
        # return eval('Location()')
        # return eval('html()')
        return html

    # @staticmethod
    # def filtered_spit(self, domonic, exclude) -> str:
        ''' outputs HTML str without the elements passed '''
        # pass
