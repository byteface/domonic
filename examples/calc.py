# -*- coding: utf-8 -*-
import sys

sys.path.insert(0, "..")

from domonic.html import *
from domonic.CDN import CDN_CSS, CDN_JS
from domonic.javascript import Math

classless_css = link(_rel="stylesheet", _href=CDN_CSS.MARX)
jquery = script(_src=CDN_JS.JQUERY)

code = script(
    """
	function add(){
		$('#results').html( Number($('#a').val()) + Number($('#b').val()) )};
"""
)

calc = article(
    div(
        label("Add numbers:"),
        input(_id="a"),
        span("+"),
        input(_id="b"),
        button("Calculate", _id="calculate_button", _onclick="add();"),
        div("Result:", div(_id="results")),
    )
)

mycalc = html(head(classless_css, jquery, code), body(calc))

render(f"{mycalc}", "calc.html")

try:
    import os
    import webbrowser

    webbrowser.open("file://" + os.path.realpath(".") + "/calc.html")
except Exception as e:
    print("view calc.html in the browser")
    pass

# To serve the generated file instead, run: python3 -m http.server

# from domonic.terminal import ls, touch
# import time
# ls( "| open .")
# touch( "1.hi")
# time.sleep(1)
# touch( "2.how")
# time.sleep(1)
# touch( "3.are")
# time.sleep(1)
# touch( "4.you")
