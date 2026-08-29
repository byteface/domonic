"""
domonic.mathml
====================================

Generate MATHML using python 3

"""

from domonic.dom import MATHML_NAMESPACE, MathMLElement

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

math_ = type("math", (MathMLElement,), {"name": "math"})
maction = type("maction", (MathMLElement,), {"name": "maction"})
menclose = type("menclose", (MathMLElement,), {"name": "menclose"})
merror = type("merror", (MathMLElement,), {"name": "merror"})
mfenced = type("mfenced", (MathMLElement,), {"name": "mfenced"})
mfrac = type("mfrac", (MathMLElement,), {"name": "mfrac"})
mi = type("mi", (MathMLElement,), {"name": "mi"})
mmultiscripts = type("mmultiscripts", (MathMLElement,), {"name": "mmultiscripts"})
mn = type("mn", (MathMLElement,), {"name": "mn"})
mo = type("mo", (MathMLElement,), {"name": "mo"})
mover = type("mover", (MathMLElement,), {"name": "mover"})
mpadded = type("mpadded", (MathMLElement,), {"name": "mpadded"})
mphantom = type("mphantom", (MathMLElement,), {"name": "mphantom"})
mroot = type("mroot", (MathMLElement,), {"name": "mroot"})
mrow = type("mrow", (MathMLElement,), {"name": "mrow"})
ms = type("ms", (MathMLElement,), {"name": "ms"})
mspace = type("mspace", (MathMLElement,), {"name": "mspace"})
msqrt = type("msqrt", (MathMLElement,), {"name": "msqrt"})
mstyle = type("mstyle", (MathMLElement,), {"name": "mstyle"})
msub = type("msub", (MathMLElement,), {"name": "msub"})
msubsup = type("msubsup", (MathMLElement,), {"name": "msubsup"})
msup = type("msup", (MathMLElement,), {"name": "msup"})
mtable = type("mtable", (MathMLElement,), {"name": "mtable"})
mtd = type("mtd", (MathMLElement,), {"name": "mtd"})
mtext = type("mtext", (MathMLElement,), {"name": "mtext"})
mtr = type("mtr", (MathMLElement,), {"name": "mtr"})
munder = type("munder", (MathMLElement,), {"name": "munder"})
munderover = type("munderover", (MathMLElement,), {"name": "munderover"})
semantics = type("semantics", (MathMLElement,), {"name": "semantics"})
maligngroup = type("maligngroup", (MathMLElement,), {"name": "maligngroup"})
malignmark = type("malignmark", (MathMLElement,), {"name": "malignmark"})
msline = type("msline", (MathMLElement,), {"name": "msline"})
msgroup = type("msgroup", (MathMLElement,), {"name": "msgroup"})
mlongdiv = type("mlongdiv", (MathMLElement,), {"name": "mlongdiv"})
mstyle = type("mstyle", (MathMLElement,), {"name": "mstyle"})
mprescripts = type("mprescripts", (MathMLElement,), {"name": "mprescripts"})
mscarries = type("mscarries", (MathMLElement,), {"name": "mscarries"})
mscarry = type("mscarry", (MathMLElement,), {"name": "mscarry"})
munder = type("munder", (MathMLElement,), {"name": "munder"})
munderover = type("munderover", (MathMLElement,), {"name": "munderover"})
none = type("none", (MathMLElement,), {"name": "none"})
