from domonic.html import *
from domonic.CDN import CDN_CSS

MARGIN = 3

# set some data
keyboard = [
    ['q','w','e','r','t','y','u','i','o','p'],
    ['a','s','d','f','g','h','j','k','l'],
    ['shift','z','x','c','v','b','n','m','backspace'],
    ['numerals','comma','space','period','enter']
]

# create a template
key_tmpl = lambda key: div( _style=f"display:inline;margin:{MARGIN}px;").html(
    button(key, _style="background-color:white;color:black;")
)

# generate keyboard
col = div()
for rows in keyboard:
    row = div(_style=f"margin:{MARGIN*2}px;")
    for key in rows:
        row.appendChild(key_tmpl(key))
    col.appendChild(str(row))

# render webpage
css = link(_rel="stylesheet", _href=CDN_CSS.MARX)
render( html(
        head(css),
        body(col, _style="background-color:#d1d5db;") ),
    "keyboard.html" )
