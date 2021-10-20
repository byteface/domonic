import sys
sys.path.insert(0, '../..')

from domonic.html import *
from domonic.CDN import CDN_CSS

MARGIN = 3

# set some data
table = [
    ["H","","","","","","","","","","","","","","","","","He"],
    ["Li","Be","","","","","","","","","","","B","C","N","O","F","Ne"],
    ["Na","Mg","","","","","","","","","","","Al","Si","P","S","Cl","Ar"],
    ["K","Ca","Sc","Ti","V","Cr","Mn","Fe","Co","Ni","Cu","Zn","Ga","Ge","As","Se","Br","Kr"],
    ["Rb","Sr","Y","Zr","Nb","Mo","Tc","Ru","Rh","Pd","Ag","Cd","In","Sn","Sb","Te","I","Xe"],
    ["Cs","Ba","La","Hf","Ta","W","Re","Os","Ir","Pt","Au","Hg","Tl","Pb","Bi","Po","At","Rn"],
    ["Fr","Ra","Ac","Rf","Db","Sg","Bh","Hs","Mt","Ds","Rg","Cn","Nh","Fl","Mc","Lv","Ts","Og"],
    ["","","","Ce","Pr","Nd","Pm","Sm","Eu","Gd","Tb","Dy","Ho","Er","Tm","Yb","Lu",""],
    ["","","","Th","Pa","U","Np","Pu","Am","Cm","Bk","Cf","Es","Fm","Md","No","Lr",""]
]

# create a template
key_tmpl = lambda key: div(_style=f"display:inline;margin:{MARGIN}px;").html(
    button(key, _style="background-color:white;color:black;width:50px;")
)

# generate table
kb = div()
for rows in table:
    row = div(_style=f"margin:{MARGIN*2}px;")
    for key in rows:
        row.appendChild(key_tmpl(key))
    kb.appendChild(str(row))

# render webpage
css = link(_rel="stylesheet", _href=CDN_CSS.MARX)
content = html(head(css), body(kb, _style="background-color:#d1d5db;"))
render(f"{content}", "table.html")
