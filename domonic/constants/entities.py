"""
domonic.constants.entities
====================================

"""

import html


class Entity:

    # __slots__ = ('entity',)

    def __init__(self, entity: str) -> None:
        self.entity = entity

    def __str__(self) -> str:
        return html.unescape(self.entity)

    def __repr__(self) -> str:
        return f"Entity({self.entity!r})"


class Char:
    def __init__(self, character: str) -> None:
        self.character = character

    def __str__(self) -> str:
        return html.escape(self.character)

    # def __repr__(self):
    #     return self.character

    # web
    # ASCII Characters (Printable)
    SPACE: str = "&#32;"
    EXCLAMATION_MARK: str = "&#33;"  #: !
    QUOTATION_MARK: str = "&#34;"  #: "
    NUMBER_SIGN: str = "&#35;"  #: #
    DOLLAR_SIGN: str = "&#36;"  #: $
    PERCENT_SIGN: str = "&#37;"  #: %
    AMPERSAND: str = "&amp;"  #: &
    APOSTROPHE: str = "&#39;"  #: '
    OPENING_PARENTHESIS: str = "&#40;"  #: (
    LEFT_PARENTHESIS: str = "&#40;"  #: (
    CLOSING_PARENTHESIS: str = "&#41;"  #: )
    RIGHT_PARENTHESIS: str = "&#41;"  #: )
    ASTERISK: str = "&#42;"  #: *
    PLUS_SIGN: str = "&#43;"  #: +
    COMMA: str = "&#44;"  #: ,
    HYPHEN: str = "&#45;"  #: -
    PERIOD: str = "&#46;"  #: .
    SLASH: str = "&#47;"  #: /
    ZERO: str = "&#48;"  #: 0
    ONE: str = "&#49;"  #: 1
    TWO: str = "&#50;"  #: 2
    THREE: str = "&#51;"  #: 3
    FOUR: str = "&#52;"  #: 4
    FIVE: str = "&#53;"  #: 5
    SIX: str = "&#54;"  #: 6
    SEVEN: str = "&#55;"  #: 7
    EIGHT: str = "&#56;"  #: 8
    NINE: str = "&#57;"  #: 9

    COLON: str = "&#58;"  #: :
    SEMICOLON: str = "&#59;"  #: ;
    LESS_THAN: str = "&lt;"  #: <
    EQUALS_SIGN: str = "&#61;"  # :: str =
    GREATER_THAN: str = "&gt;"  #: >
    QUESTION_MARK: str = "&#63;"  #: ?
    AT_SIGN: str = "&#64;"  #: @

    UPPERCASE_A: str = "&#65;"  #: A
    UPPERCASE_B: str = "&#66;"  #: B
    UPPERCASE_C: str = "&#67;"  #: C
    UPPERCASE_D: str = "&#68;"  #: D
    UPPERCASE_E: str = "&#69;"  #: E
    UPPERCASE_F: str = "&#70;"  #: F
    UPPERCASE_G: str = "&#71;"  #: G
    UPPERCASE_H: str = "&#72;"  #: H
    UPPERCASE_I: str = "&#73;"  #: I
    UPPERCASE_J: str = "&#74;"  #: J
    UPPERCASE_K: str = "&#75;"  #: K
    UPPERCASE_L: str = "&#76;"  #: L
    UPPERCASE_M: str = "&#77;"  #: M
    UPPERCASE_N: str = "&#78;"  #: N
    UPPERCASE_O: str = "&#79;"  #: O
    UPPERCASE_P: str = "&#80;"  #: P
    UPPERCASE_Q: str = "&#81;"  #: Q
    UPPERCASE_R: str = "&#82;"  #: R
    UPPERCASE_S: str = "&#83;"  #: S
    UPPERCASE_T: str = "&#84;"  #: T
    UPPERCASE_U: str = "&#85;"  #: U
    UPPERCASE_V: str = "&#86;"  #: V
    UPPERCASE_W: str = "&#87;"  #: W
    UPPERCASE_X: str = "&#88;"  #: X
    UPPERCASE_Y: str = "&#89;"  #: Y
    UPPERCASE_Z: str = "&#90;"  #: Z

    OPENING_SQUARE_BRACKET: str = "&#91;"  #: [
    BACKSLASH: str = "&#92;"  #: \
    CLOSING_SQUARE_BRACKET: str = "&#93;"  #: ]
    CARET: str = "&#94;"  #: ^
    UNDERSCORE: str = "&#95;"  #: _
    GRAVE_ACCENT: str = "&#96;"  #:
    LOWERCASE_A: str = "&#97;"  #: a
    LOWERCASE_B: str = "&#98;"  #: b
    LOWERCASE_C: str = "&#99;"  #: c
    LOWERCASE_D: str = "&#100;"  #: d
    LOWERCASE_E: str = "&#101;"  #: e
    LOWERCASE_F: str = "&#102;"  #: f
    LOWERCASE_G: str = "&#103;"  #: g
    LOWERCASE_H: str = "&#104;"  #: h
    LOWERCASE_I: str = "&#105;"  #: i
    LOWERCASE_J: str = "&#106;"  #: j
    LOWERCASE_K: str = "&#107;"  #: k
    LOWERCASE_L: str = "&#108;"  #: l
    LOWERCASE_M: str = "&#109;"  #: m
    LOWERCASE_N: str = "&#110;"  #: n
    LOWERCASE_O: str = "&#111;"  #: o
    LOWERCASE_P: str = "&#112;"  #: p
    LOWERCASE_Q: str = "&#113;"  #: q
    LOWERCASE_R: str = "&#114;"  #: r
    LOWERCASE_S: str = "&#115;"  #: s
    LOWERCASE_T: str = "&#116;"  #: t
    LOWERCASE_U: str = "&#117;"  #: u
    LOWERCASE_V: str = "&#118;"  #: v
    LOWERCASE_W: str = "&#119;"  #: w
    LOWERCASE_X: str = "&#120;"  #: x
    LOWERCASE_Y: str = "&#121;"  #: y
    LOWERCASE_Z: str = "&#122;"  #: z

    OPENING_CURLY_BRACE: str = "&#123;"  #: {
    LEFT_CURLY_BRACE: str = "&#123;"  #: {
    VERTICAL_BAR: str = "&#124;"  #: |
    CLOSING_CURLY_BRACE: str = "&#125;"  #: }
    RIGHT_CURLY_BRACE: str = "&#125;"  #: }
    TILDE: str = "&#126;"  #: ~

    # ISO-8859-1 Characters
    AGRAVE: str = "&Agrave;"  #: À
    AACUTE: str = "&Aacute;"  #: Á
    ACIRC: str = "&Acirc;"  #: Â
    ATILDE: str = "&Atilde;"  #: Ã
    AUML: str = "&Auml;"  #: Ä
    ARING: str = "&Aring;"  #: Å
    AELIG: str = "&AElig;"  #: Æ
    CCEDIL: str = "&Ccedil;"  #: Ç
    EGRAVE: str = "&Egrave;"  #: È
    EACUTE: str = "&Eacute;"  #: É
    ECIRC: str = "&Ecirc;"  #: Ê
    EUML: str = "&Euml;"  #: Ë
    IGRAVE: str = "&Igrave;"  #: Ì
    IACUTE: str = "&Iacute;"  #: Í
    ICIRC: str = "&Icirc;"  #: Î
    IUML: str = "&Iuml;"  #: Ï
    ETH: str = "&ETH;"  #: Ð
    NTILDE: str = "&Ntilde;"  #: Ñ
    OGRAVE: str = "&Ograve;"  #: Ò
    OACUTE: str = "&Oacute;"  #: Ó
    OCIRC: str = "&Ocirc;"  #: Ô
    OTILDE: str = "&Otilde;"  #: Õ
    OUML: str = "&Ouml;"  #: Ö
    OSLASH: str = "&Oslash;"  #: Ø
    UGRAVE: str = "&Ugrave;"  #: Ù
    UACUTE: str = "&Uacute;"  #: Ú
    UCIRC: str = "&Ucirc;"  #: Û
    UUML: str = "&Uuml;"  #: Ü
    YACUTE: str = "&Yacute;"  #: Ý
    THORN: str = "&THORN;"  #: Þ
    SZLIG: str = "&szlig;"  #: ß
    AGRAVE: str = "&agrave;"  # type: ignore[no-redef]  #: à
    AACUTE: str = "&aacute;"  # type: ignore[no-redef]  #: á
    ACIRC: str = "&acirc;"  # type: ignore[no-redef]  #: â
    ATILDE: str = "&atilde;"  # type: ignore[no-redef]  #: ã
    AUML: str = "&auml;"  # type: ignore[no-redef]  #: ä
    ARING: str = "&aring;"  # type: ignore[no-redef]  #: å
    AELIG: str = "&aelig;"  # type: ignore[no-redef]  #: æ
    CCEDIL: str = "&ccedil;"  # type: ignore[no-redef]  #: ç
    EGRAVE: str = "&egrave;"  # type: ignore[no-redef]  #: è
    EACUTE: str = "&eacute;"  # type: ignore[no-redef]  #: é
    ECIRC: str = "&ecirc;"  # type: ignore[no-redef]  #: ê
    EUML: str = "&euml;"  # type: ignore[no-redef]  #: ë
    IGRAVE: str = "&igrave;"  # type: ignore[no-redef]  #: ì
    IACUTE: str = "&iacute;"  # type: ignore[no-redef]  #: í
    ICIRC: str = "&icirc;"  # type: ignore[no-redef]  #: î
    IUML: str = "&iuml;"  # type: ignore[no-redef]  #: ï
    ETH: str = "&eth;"  # type: ignore[no-redef]  #: ð
    NTILDE: str = "&ntilde;"  # type: ignore[no-redef]  #: ñ
    OGRAVE: str = "&ograve;"  # type: ignore[no-redef]  #: ò
    OACUTE: str = "&oacute;"  # type: ignore[no-redef]  #: ó
    OCIRC: str = "&ocirc;"  # type: ignore[no-redef]  #: ô
    OTILDE: str = "&otilde;"  # type: ignore[no-redef]  #: õ
    OUML: str = "&ouml;"  # type: ignore[no-redef]  #: ö
    OSLASH: str = "&oslash;"  # type: ignore[no-redef]  #: ø
    UGRAVE: str = "&ugrave;"  # type: ignore[no-redef]  #: ù
    UACUTE: str = "&uacute;"  # type: ignore[no-redef]  #: ú
    UCIRC: str = "&ucirc;"  # type: ignore[no-redef]  #: û
    UUML: str = "&uuml;"  # type: ignore[no-redef]  #: ü
    YACUTE: str = "&yacute;"  # type: ignore[no-redef]  #: ý
    THORN: str = "&thorn;"  # type: ignore[no-redef]  #: þ
    YUML: str = "&yuml;"  #: ÿ

    # ISO-8859-1 Symbols
    NBSP: str = "&nbsp;"  #:
    IEXCL: str = "&iexcl;"  #: ¡
    CENT: str = "&cent;"  #: ¢
    POUND: str = "&pound;"  #: £
    CURREN: str = "&curren;"  #: ¤
    YEN: str = "&yen;"  #: ¥
    BRVBAR: str = "&brvbar;"  #: ¦
    SECT: str = "&sect;"  #: §
    UML: str = "&uml;"  #: ¨
    COPY: str = "&copy;"  #: ©
    COPYRIGHT: str = "&copy;"  #: ©
    ORDF: str = "&ordf;"  #: ª
    LAQUO: str = "&laquo;"  #: «
    NOT: str = "&not;"  #: ¬
    # ­   &shy;   &#173;  Soft hyphen
    REG: str = "&reg;"  #: ®
    MACR: str = "&macr;"  #: ¯
    DEG: str = "&deg;"  #: °
    PLUSMN: str = "&plusmn;"  #: ±
    SUP2: str = "&sup2;"  #: ²
    SUP3: str = "&sup3;"  #: ³
    ACUTE: str = "&acute;"  #: ´
    MICRO: str = "&micro;"  #: µ
    PARA: str = "&para;"  #: ¶
    CEDIL: str = "&cedil;"  #: ¸
    SUP1: str = "&sup1;"  #: ¹
    ORDM: str = "&ordm;"  #: º
    RAQUO: str = "&raquo;"  #: »
    FRAC14: str = "&frac14;"  #: ¼
    FRAC12: str = "&frac12;"  #: ½
    FRAC34: str = "&frac34;"  #: ¾
    IQUEST: str = "&iquest;"  #: ¿
    TIMES: str = "&times;"  #: ×
    DIVIDE: str = "&divide;"  #: ÷

    # Math Symbols
    FORALL: str = "&forall;"  #: ∀
    PART: str = "&part;"  #: ∂
    EXIST: str = "&exist;"  #: ∃
    EMPTY: str = "&empty;"  #: ∅
    NABLA: str = "&nabla;"  #: ∇
    ISIN: str = "&isin;"  #: ∈
    NOTIN: str = "&notin;"  #: ∉
    NI: str = "&ni;"  #: ∋
    PROD: str = "&prod;"  #: ∏
    SUM: str = "&sum;"  #: ∑
    MINUS: str = "&minus;"  #: −
    LOWAST: str = "&lowast;"  #: ∗
    RADIC: str = "&radic;"  #: √
    PROP: str = "&prop;"  #: ∝
    INFIN: str = "&infin;"  #: ∞
    ANG: str = "&ang;"  #: ∠
    AND: str = "&and;"  #: ∧
    OR: str = "&or;"  #: ∨
    CAP: str = "&cap;"  #: ∩
    CUP: str = "&cup;"  #: ∪
    INT: str = "&int;"  #: ∫
    THERE4: str = "&there4;"  #: ∴
    SIM: str = "&sim;"  #: ∼
    CONG: str = "&cong;"  #: ≅
    ASYMP: str = "&asymp;"  #: ≈
    NE: str = "&ne;"  #: ≠
    EQUIV: str = "&equiv;"  #: ≡
    LE: str = "&le;"  #: ≤
    GE: str = "&ge;"  #: ≥
    SUB: str = "&sub;"  #: ⊂
    SUP: str = "&sup;"  #: ⊃
    NSUB: str = "&nsub;"  #: ⊄
    SUBE: str = "&sube;"  #: ⊆
    SUPE: str = "&supe;"  #: ⊇
    OPLUS: str = "&oplus;"  #: ⊕
    OTIMES: str = "&otimes;"  #: ⊗
    PERP: str = "&perp;"  #: ⊥
    SDOT: str = "&sdot;"  #: ⋅

    # Greek Letters
    ALPHA: str = "&Alpha;"  #: Α
    BETA: str = "&Beta;"  #: Β
    GAMMA: str = "&Gamma;"  #: Γ
    DELTA: str = "&Delta;"  #: Δ
    EPSILON: str = "&Epsilon;"  #: Ε
    ZETA: str = "&Zeta;"  #: Ζ
    ETA: str = "&Eta;"  #: Η
    THETA: str = "&Theta;"  #: Θ
    IOTA: str = "&Iota;"  #: Ι
    KAPPA: str = "&Kappa;"  #: Κ
    LAMBDA: str = "&Lambda;"  #: Λ
    MU: str = "&Mu;"  #: Μ
    NU: str = "&Nu;"  #: Ν
    XI: str = "&Xi;"  #: Ξ
    OMICRON: str = "&Omicron;"  #: Ο
    PI: str = "&Pi;"  #: Π
    RHO: str = "&Rho;"  #: Ρ
    SIGMA: str = "&Sigma;"  #: Σ
    TAU: str = "&Tau;"  #: Τ
    UPSILON: str = "&Upsilon;"  #: Υ
    PHI: str = "&Phi;"  #: Φ
    CHI: str = "&Chi;"  #: Χ
    PSI: str = "&Psi;"  #: Ψ
    OMEGA: str = "&Omega;"  #: Ω
    ALPHA: str = "&alpha;"  # type: ignore[no-redef]  #: α
    BETA: str = "&beta;"  # type: ignore[no-redef]  #: β
    GAMMA: str = "&gamma;"  # type: ignore[no-redef]  #: γ
    DELTA: str = "&delta;"  # type: ignore[no-redef]  #: δ
    EPSILON: str = "&epsilon;"  # type: ignore[no-redef]  #: ε
    ZETA: str = "&zeta;"  # type: ignore[no-redef]  #: ζ
    ETA: str = "&eta;"  # type: ignore[no-redef]  #: η
    THETA: str = "&theta;"  # type: ignore[no-redef]  #: θ
    IOTA: str = "&iota;"  # type: ignore[no-redef]  #: ι
    KAPPA: str = "&kappa;"  # type: ignore[no-redef]  #: κ
    LAMBDA: str = "&lambda;"  # type: ignore[no-redef]  #: λ
    MU: str = "&mu;"  # type: ignore[no-redef]  #: μ
    NU: str = "&nu;"  # type: ignore[no-redef]  #: ν
    XI: str = "&xi;"  # type: ignore[no-redef]  #: ξ
    OMICRON: str = "&omicron;"  # type: ignore[no-redef]  #: ο
    PI: str = "&pi;"  # type: ignore[no-redef]  #: π
    RHO: str = "&rho;"  # type: ignore[no-redef]  #: ρ
    SIGMAF: str = "&sigmaf;"  #: ς
    SIGMA: str = "&sigma;"  # type: ignore[no-redef]  #: σ
    TAU: str = "&tau;"  # type: ignore[no-redef]  #: τ
    UPSILON: str = "&upsilon;"  # type: ignore[no-redef]  #: υ
    PHI: str = "&phi;"  # type: ignore[no-redef]  #: φ
    CHI: str = "&chi;"  # type: ignore[no-redef]  #: χ
    PSI: str = "&psi;"  # type: ignore[no-redef]  #: ψ
    OMEGA: str = "&omega;"  # type: ignore[no-redef]  #: ω
    THETASYM: str = "&thetasym;"  #: ϑ
    UPSIH: str = "&upsih;"  #: ϒ
    PIV: str = "&piv;"  #: ϖ

    OELIG: str = "&OElig;"  #: Œ
    oeLIG: str = "&oelig;"  #: œ
    SCARON: str = "&Scaron;"  #: Š
    Scaron: str = "&Scaron;"  #: Š
    scaron: str = "&scaron;"  #: š
    YUML: str = "&Yuml;"  # type: ignore[no-redef]  #: Ÿ
    FNOF: str = "&fnof;"  #: ƒ
    CIRC: str = "&circ;"  #: ˆ
    TILDE: str = "&tilde;"  # type: ignore[no-redef]  #: ˜

    #     &ensp;  &#8194; En space
    #     &emsp;  &#8195; Em space
    #     &thinsp;    &#8201; Thin space
    # ‌   &zwnj;  &#8204; Zero width non-joiner
    # ‍   &zwj;   &#8205; Zero width joiner
    # U+200E &lrm;   &#8206; Left-to-right mark
    # U+200F &rlm;   &#8207; Right-to-left mark

    NDASH: str = "&ndash;"  #: –
    MDASH: str = "&mdash;"  #: —
    LSQUO: str = "&lsquo;"  #: ‘
    RSQUO: str = "&rsquo;"  #: ’
    SBQUO: str = "&sbquo;"  #: ‚
    LDQUO: str = "&ldquo;"  #: “
    RDQUO: str = "&rdquo;"  #: ”
    BDQUO: str = "&bdquo;"  #: „
    DAGGER: str = "&dagger;"  #: †
    DAGGER: str = "&Dagger;"  # type: ignore[no-redef]  #: ‡
    BULL: str = "&bull;"  #: •
    HELLIP: str = "&hellip;"  #: …
    PERMIL: str = "&permil;"  #: ‰
    PRIME: str = "&prime;"  #: ′
    PRIME: str = "&Prime;"  # type: ignore[no-redef]  #: ″
    LSAQUO: str = "&lsaquo;"  #: ‹
    RSAQUO: str = "&rsaquo;"  #: ›
    OLINE: str = "&oline;"  #: ‾
    EURO: str = "&euro;"  #: €
    TRADE: str = "&trade;"  #: ™
    TRADEMARK: str = "&trade;"  #: ™

    # ARROWS
    LARR: str = "&larr;"  #: ←
    LEFT: str = "&larr;"  #: ←
    UARR: str = "&uarr;"  #: ↑
    UP: str = "&uarr;"  #: ↑
    RARR: str = "&rarr;"  #: →
    RIGHT: str = "&rarr;"  #: →
    DARR: str = "&darr;"  #: ↓
    DOWN: str = "&darr;"  #: ↓

    HARR: str = "&harr;"  #: ↔
    CRARR: str = "&crarr;"  #: ↵
    LCEIL: str = "&lceil;"  #: ⌈
    RCEIL: str = "&rceil;"  #: ⌉
    LFLOOR: str = "&lfloor;"  #: ⌊
    RFLOOR: str = "&rfloor;"  #: ⌋
    LOZ: str = "&loz;"  #: ◊

    SPADES: str = "&spades;"  #: ♠
    CLUBS: str = "&clubs;"  #: ♣
    HEARTS: str = "&hearts;"  #: ♥
    DIAMS: str = "&diams;"  #: ♦
    DIAMONDS: str = "&diams;"  #: ♦

    SUNG: str = "&sung;"  #: ♪
    FLAT: str = "&flat;"  #: ♭
    NATUR: str = "&natur;"  #: ♮
    NATURAL: str = "&natural;"  #: ♮
    SHARP: str = "&sharp;"  #: ♯

    CHECK: str = "&check;"  #: ✓
    CHECKMARK: str = "&checkmark;"  #: ✓
    TICK: str = "&check;"  #: ✓
    CROSS: str = "&cross;"  #: ✗

    OHM: str = "&ohm;"  #: Ω
    MHO: str = "&mho;"  #: ℧

    FRAC13: str = "&frac13;"  #: ⅓
    FRAC23: str = "&frac23;"  #: ⅔
    FRAC15: str = "&frac15;"  #: ⅕
    FRAC25: str = "&frac25;"  #: ⅖
    FRAC35: str = "&frac35;"  #: ⅗
    FRAC45: str = "&frac45;"  #: ⅘
    FRAC16: str = "&frac16;"  #: ⅙
    FRAC56: str = "&frac56;"  #: ⅚
    FRAC18: str = "&frac18;"  #: ⅛
    FRAC38: str = "&frac38;"  #: ⅜
    FRAC58: str = "&frac58;"  #: ⅝
    FRAC78: str = "&frac78;"  #: ⅞

    STAR: str = "&star;"  #: ☆
    STARF: str = "&starf;"  #: ★
    BIGSTAR: str = "&bigstar;"
    PHONE: str = "&phone;"  #: ☎
    FEMALE: str = "&female;"  #: ♀
    MALE: str = "&male;"  #: ♂


# A handful of HTML entity names differ only by case (&Agrave; / &agrave;,
# &Alpha; / &alpha;, ...) and share one bare Char.NAME above (the second,
# case-insensitively identical, assignment in the class body intentionally
# overwrites the first -- ``# type: ignore[no-redef]`` there marks that on
# purpose, not oversight). Both variants stay reachable: the bare name
# resolves to whichever was assigned last, and a fully-disambiguated alias
# for each is set below.
_CHAR_DISAMBIGUATED_ALIASES = {
    "LATIN_CAPITAL_A_GRAVE": "&Agrave;",
    "LATIN_CAPITAL_A_ACUTE": "&Aacute;",
    "LATIN_CAPITAL_A_CIRCUMFLEX": "&Acirc;",
    "LATIN_CAPITAL_A_TILDE": "&Atilde;",
    "LATIN_CAPITAL_A_UMLAUT": "&Auml;",
    "LATIN_CAPITAL_A_RING": "&Aring;",
    "LATIN_CAPITAL_AE": "&AElig;",
    "LATIN_CAPITAL_C_CEDILLA": "&Ccedil;",
    "LATIN_CAPITAL_E_GRAVE": "&Egrave;",
    "LATIN_CAPITAL_E_ACUTE": "&Eacute;",
    "LATIN_CAPITAL_E_CIRCUMFLEX": "&Ecirc;",
    "LATIN_CAPITAL_E_UMLAUT": "&Euml;",
    "LATIN_CAPITAL_I_GRAVE": "&Igrave;",
    "LATIN_CAPITAL_I_ACUTE": "&Iacute;",
    "LATIN_CAPITAL_I_CIRCUMFLEX": "&Icirc;",
    "LATIN_CAPITAL_I_UMLAUT": "&Iuml;",
    "LATIN_CAPITAL_ETH": "&ETH;",
    "LATIN_CAPITAL_N_TILDE": "&Ntilde;",
    "LATIN_CAPITAL_O_GRAVE": "&Ograve;",
    "LATIN_CAPITAL_O_ACUTE": "&Oacute;",
    "LATIN_CAPITAL_O_CIRCUMFLEX": "&Ocirc;",
    "LATIN_CAPITAL_O_TILDE": "&Otilde;",
    "LATIN_CAPITAL_O_UMLAUT": "&Ouml;",
    "LATIN_CAPITAL_O_STROKE": "&Oslash;",
    "LATIN_CAPITAL_U_GRAVE": "&Ugrave;",
    "LATIN_CAPITAL_U_ACUTE": "&Uacute;",
    "LATIN_CAPITAL_U_CIRCUMFLEX": "&Ucirc;",
    "LATIN_CAPITAL_U_UMLAUT": "&Uuml;",
    "LATIN_CAPITAL_Y_ACUTE": "&Yacute;",
    "LATIN_CAPITAL_THORN": "&THORN;",
    "GREEK_CAPITAL_ALPHA": "&Alpha;",
    "GREEK_CAPITAL_BETA": "&Beta;",
    "GREEK_CAPITAL_GAMMA": "&Gamma;",
    "GREEK_CAPITAL_DELTA": "&Delta;",
    "GREEK_CAPITAL_EPSILON": "&Epsilon;",
    "GREEK_CAPITAL_ZETA": "&Zeta;",
    "GREEK_CAPITAL_ETA": "&Eta;",
    "GREEK_CAPITAL_THETA": "&Theta;",
    "GREEK_CAPITAL_IOTA": "&Iota;",
    "GREEK_CAPITAL_KAPPA": "&Kappa;",
    "GREEK_CAPITAL_LAMBDA": "&Lambda;",
    "GREEK_CAPITAL_MU": "&Mu;",
    "GREEK_CAPITAL_NU": "&Nu;",
    "GREEK_CAPITAL_XI": "&Xi;",
    "GREEK_CAPITAL_OMICRON": "&Omicron;",
    "GREEK_CAPITAL_PI": "&Pi;",
    "GREEK_CAPITAL_RHO": "&Rho;",
    "GREEK_CAPITAL_SIGMA": "&Sigma;",
    "GREEK_CAPITAL_TAU": "&Tau;",
    "GREEK_CAPITAL_UPSILON": "&Upsilon;",
    "GREEK_CAPITAL_PHI": "&Phi;",
    "GREEK_CAPITAL_CHI": "&Chi;",
    "GREEK_CAPITAL_PSI": "&Psi;",
    "GREEK_CAPITAL_OMEGA": "&Omega;",
    "SINGLE_DAGGER": "&dagger;",
    "DOUBLE_DAGGER": "&Dagger;",
    "SINGLE_PRIME": "&prime;",
    "DOUBLE_PRIME": "&Prime;",
    "ASCII_TILDE": "&#126;",
    "LATIN_SMALL_Y_UMLAUT": "&yuml;",
    "LATIN_CAPITAL_Y_UMLAUT": "&Yuml;",
}

for _alias_name, _alias_value in _CHAR_DISAMBIGUATED_ALIASES.items():
    setattr(Char, _alias_name, _alias_value)


__all__ = ["Char", "Entity"]
