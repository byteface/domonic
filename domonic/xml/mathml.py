"""
    domonic.mathml
    ====================================

    Generate MATHML using python 3

"""

from domonic.dom import Element


mathml_tags = [
    "mmultiscripts",
    "munderover",
    "semantics",
    "maligngroup",
    "malignmark",
    "mprescripts",
    "munderover",
    "mscarries",
    "maction",
    "menclose",
    "mphantom",
    "mpadded",
    "merror",
    "mfenced",
    "msgroup",
    "mlongdiv",
    "mfrac",
    "mover",
    "mroot",
    "mspace",
    "msqrt",
    "mstyle",
    "msubsup",
    "mtable",
    "mtext",
    "munder",
    "msline",
    "mstyle",
    "mscarry",
    "munder",
    "math",
    "mrow",
    "msub",
    "msup",
    "none",
    "mtr",
    "mtd",
    "ms",
    "mi",
    "mn",
    "mo",
]

# mathml_attributes = []

math_ = type("math", (Element,), {"name": "math"})
maction = type("maction", (Element,), {"name": "maction"})
menclose = type("menclose", (Element,), {"name": "menclose"})
merror = type("merror", (Element,), {"name": "merror"})
mfenced = type("mfenced", (Element,), {"name": "mfenced"})
mfrac = type("mfrac", (Element,), {"name": "mfrac"})
mi = type("mi", (Element,), {"name": "mi"})
mmultiscripts = type("mmultiscripts", (Element,), {"name": "mmultiscripts"})
mn = type("mn", (Element,), {"name": "mn"})
mo = type("mo", (Element,), {"name": "mo"})
mover = type("mover", (Element,), {"name": "mover"})
mpadded = type("mpadded", (Element,), {"name": "mpadded"})
mphantom = type("mphantom", (Element,), {"name": "mphantom"})
mroot = type("mroot", (Element,), {"name": "mroot"})
mrow = type("mrow", (Element,), {"name": "mrow"})
ms = type("ms", (Element,), {"name": "ms"})
mspace = type("mspace", (Element,), {"name": "mspace"})
msqrt = type("msqrt", (Element,), {"name": "msqrt"})
mstyle = type("mstyle", (Element,), {"name": "mstyle"})
msub = type("msub", (Element,), {"name": "msub"})
msubsup = type("msubsup", (Element,), {"name": "msubsup"})
msup = type("msup", (Element,), {"name": "msup"})
mtable = type("mtable", (Element,), {"name": "mtable"})
mtd = type("mtd", (Element,), {"name": "mtd"})
mtext = type("mtext", (Element,), {"name": "mtext"})
mtr = type("mtr", (Element,), {"name": "mtr"})
munder = type("munder", (Element,), {"name": "munder"})
munderover = type("munderover", (Element,), {"name": "munderover"})
semantics = type("semantics", (Element,), {"name": "semantics"})
maligngroup = type("maligngroup", (Element,), {"name": "maligngroup"})
malignmark = type("malignmark", (Element,), {"name": "malignmark"})
msline = type("msline", (Element,), {"name": "msline"})
msgroup = type("msgroup", (Element,), {"name": "msgroup"})
mlongdiv = type("mlongdiv", (Element,), {"name": "mlongdiv"})
mstyle = type("mstyle", (Element,), {"name": "mstyle"})
mprescripts = type("mprescripts", (Element,), {"name": "mprescripts"})
mscarries = type("mscarries", (Element,), {"name": "mscarries"})
mscarry = type("mscarry", (Element,), {"name": "mscarry"})
munder = type("munder", (Element,), {"name": "munder"})
munderover = type("munderover", (Element,), {"name": "munderover"})
none = type("none", (Element,), {"name": "none"})
