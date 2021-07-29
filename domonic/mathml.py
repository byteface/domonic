"""
    domonic.mathml
    ====================================
    Generate MATHML using python 3

"""

from domonic.html import tag
from domonic.dom import Node


mathml_tags = ["math", "maction", "math", "menclose", "merror", "mfenced", "mfrac", "mi", "mmultiscripts", "mn", "mo", "mover", "mpadded", "mphantom", "mroot", "mrow",
                "ms", "mspace", "msqrt", "mstyle", "msub", "msubsup", "msup", "mtable", "mtd", "mtext", "mtr", "munder", "munderover", "semantics", "maligngroup",
                "malignmark", "msline", "msgroup", "mlongdiv", "mstyle", "mprescripts", "mscarries", "mscarry", "munder", "munderover", "none"]

# mathml_attributes = []


def mathml_init(self, *args, **kwargs):
    tag.__init__(self, *args, **kwargs)
    Node.__init__(self, *args, **kwargs)


math_ = type('math', (tag, Node), {'name': 'math', '__init__': mathml_init})
maction = type('maction', (tag, Node), {'name': 'maction', '__init__': mathml_init})
menclose = type('menclose', (tag, Node), {'name': 'menclose', '__init__': mathml_init})
merror = type('merror', (tag, Node), {'name': 'merror', '__init__': mathml_init})
mfenced = type('mfenced', (tag, Node), {'name': 'mfenced', '__init__': mathml_init})
mfrac = type('mfrac', (tag, Node), {'name': 'mfrac', '__init__': mathml_init})
mi = type('mi', (tag, Node), {'name': 'mi', '__init__': mathml_init})
mmultiscripts = type('mmultiscripts', (tag, Node), {'name': 'mmultiscripts', '__init__': mathml_init})
mn = type('mn', (tag, Node), {'name': 'mn', '__init__': mathml_init})
mo = type('mo', (tag, Node), {'name': 'mo', '__init__': mathml_init})
mover = type('mover', (tag, Node), {'name': 'mover', '__init__': mathml_init})
mpadded = type('mpadded', (tag, Node), {'name': 'mpadded', '__init__': mathml_init})
mphantom = type('mphantom', (tag, Node), {'name': 'mphantom', '__init__': mathml_init})
mroot = type('mroot', (tag, Node), {'name': 'mroot', '__init__': mathml_init})
mrow = type('mrow', (tag, Node), {'name': 'mrow', '__init__': mathml_init})
ms = type('ms', (tag, Node), {'name': 'ms', '__init__': mathml_init})
mspace = type('mspace', (tag, Node), {'name': 'mspace', '__init__': mathml_init})
msqrt = type('msqrt', (tag, Node), {'name': 'msqrt', '__init__': mathml_init})
mstyle = type('mstyle', (tag, Node), {'name': 'mstyle', '__init__': mathml_init})
msub = type('msub', (tag, Node), {'name': 'msub', '__init__': mathml_init})
msubsup = type('msubsup', (tag, Node), {'name': 'msubsup', '__init__': mathml_init})
msup = type('msup', (tag, Node), {'name': 'msup', '__init__': mathml_init})
mtable = type('mtable', (tag, Node), {'name': 'mtable', '__init__': mathml_init})
mtd = type('mtd', (tag, Node), {'name': 'mtd', '__init__': mathml_init})
mtext = type('mtext', (tag, Node), {'name': 'mtext', '__init__': mathml_init})
mtr = type('mtr', (tag, Node), {'name': 'mtr', '__init__': mathml_init})
munder = type('munder', (tag, Node), {'name': 'munder', '__init__': mathml_init})
munderover = type('munderover', (tag, Node), {'name': 'munderover', '__init__': mathml_init})
semantics = type('semantics', (tag, Node), {'name': 'semantics', '__init__': mathml_init})
maligngroup = type('maligngroup', (tag, Node), {'name': 'maligngroup', '__init__': mathml_init})
malignmark = type('malignmark', (tag, Node), {'name': 'malignmark', '__init__': mathml_init})
msline = type('msline', (tag, Node), {'name': 'msline', '__init__': mathml_init})
msgroup = type('msgroup', (tag, Node), {'name': 'msgroup', '__init__': mathml_init})
mlongdiv = type('mlongdiv', (tag, Node), {'name': 'mlongdiv', '__init__': mathml_init})
mstyle = type('mstyle', (tag, Node), {'name': 'mstyle', '__init__': mathml_init})
mprescripts = type('mprescripts', (tag, Node), {'name': 'mprescripts', '__init__': mathml_init})
mscarries = type('mscarries', (tag, Node), {'name': 'mscarries', '__init__': mathml_init})
mscarry = type('mscarry', (tag, Node), {'name': 'mscarry', '__init__': mathml_init})
munder = type('munder', (tag, Node), {'name': 'munder', '__init__': mathml_init})
munderover = type('munderover', (tag, Node), {'name': 'munderover', '__init__': mathml_init})
none = type('none', (tag, Node), {'name': 'none', '__init__': mathml_init})
