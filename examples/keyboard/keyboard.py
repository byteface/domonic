import sys

sys.path.insert(0, "../..")

from domonic.html import *
from domonic.CDN import CDN_CSS

MARGIN = 3

# set some data
keyboard = [
    ["q", "w", "e", "r", "t", "y", "u", "i", "o", "p"],
    ["a", "s", "d", "f", "g", "h", "j", "k", "l"],
    ["shift", "z", "x", "c", "v", "b", "n", "m", "backspace"],
    ["numerals", "comma", "space", "period", "enter"],
]

# create a template
key_tmpl = lambda key: div(_style=f"display:inline;margin:{MARGIN}px;").html(
    button(key, _style="background-color:white;color:black;")
)

# generate keyboard
kb = div()
for rows in keyboard:
    row = div(_style=f"margin:{MARGIN*2}px;")
    for key in rows:
        row.appendChild(key_tmpl(key))
    kb.appendChild(str(row))


# generate a piano - lol - copilot is funny
# piano = div( _style="width:100%;height:100%;")
# piano.appendChild(img(src=CDN_CSS.piano, _style="width:100%;height:100%;"))


# render webpage
css = link(_rel="stylesheet", _href=CDN_CSS.MARX)
content = html(head(css), body(kb, _style="background-color:#d1d5db;"))
render(f"{content}", "keyboard.html")
