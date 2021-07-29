"""
    domonic.constants.entities
    ====================================

"""


class Entity():

    def __init__(self, entity: str):
        self.entity = entity

    def __str__(self):
        import html
        return html.unescape(self.character)


class Char():

    def __init__(self, character: str):
        self.character = character

    def __str__(self):
        import html
        return html.escape(self.character)

    # def __repr__(self):
    #     return self.character

    # web
    # ASCII Characters (Printable)
    SPACE = '&#32;'
    EXCLAMATION_MARK = '&#33;'  #: !
    QUOTATION_MARK = '&#34;'  #: "
    NUMBER_SIGN = '&#35;'  #: #
    DOLLAR_SIGN = '&#36;'  #: $
    PERCENT_SIGN = '&#37;'  #: %
    AMPERSAND = '&amp;'  #: &
    APOSTROPHE = '&#39;'  #: '
    OPENING_PARENTHESIS = '&#40;'  #: (
    LEFT_PARENTHESIS = '&#40;'  #: (
    CLOSING_PARENTHESIS = '&#41;'  #: )
    RIGHT_PARENTHESIS = '&#41;'  #: )
    ASTERISK = '&#42;'  #: *
    PLUS_SIGN = '&#43;'  #: +
    COMMA = '&#44;'  #: ,
    HYPHEN = '&#45;'  #: -
    PERIOD = '&#46;'  #: .
    SLASH = '&#47;'  #: /
    ZERO = '&#48;'  #: 0
    ONE = '&#49;'  #: 1
    TWO = '&#50;'  #: 2
    THREE = '&#51;'  #: 3
    FOUR = '&#52;'  #: 4
    FIVE = '&#53;'  #: 5
    SIX = '&#54;'  #: 6
    SEVEN = '&#55;'  #: 7
    EIGHT = '&#56;'  #: 8
    NINE = '&#57;'  #: 9

    COLON = '&#58;'  #: :
    SEMICOLON = '&#59;'  #: ;
    LESS_THAN = '&lt;'  #: <
    EQUALS_SIGN = '&#61;'  #: =
    GREATER_THAN = '&gt;'  #: >
    QUESTION_MARK = '&#63;'  #: ?
    AT_SIGN = '&#64;'  #: @

    UPPERCASE_A = '&#65;'  #: A
    UPPERCASE_B = '&#66;'  #: B
    UPPERCASE_C = '&#67;'  #: C
    UPPERCASE_D = '&#68;'  #: D
    UPPERCASE_E = '&#69;'  #: E
    UPPERCASE_F = '&#70;'  #: F
    UPPERCASE_G = '&#71;'  #: G
    UPPERCASE_H = '&#72;'  #: H
    UPPERCASE_I = '&#73;'  #: I
    UPPERCASE_J = '&#74;'  #: J
    UPPERCASE_K = '&#75;'  #: K
    UPPERCASE_L = '&#76;'  #: L
    UPPERCASE_M = '&#77;'  #: M
    UPPERCASE_N = '&#78;'  #: N
    UPPERCASE_O = '&#79;'  #: O
    UPPERCASE_P = '&#80;'  #: P
    UPPERCASE_Q = '&#81;'  #: Q
    UPPERCASE_R = '&#82;'  #: R
    UPPERCASE_S = '&#83;'  #: S
    UPPERCASE_T = '&#84;'  #: T
    UPPERCASE_U = '&#85;'  #: U
    UPPERCASE_V = '&#86;'  #: V
    UPPERCASE_W = '&#87;'  #: W
    UPPERCASE_X = '&#88;'  #: X
    UPPERCASE_Y = '&#89;'  #: Y
    UPPERCASE_Z = '&#90;'  #: Z

    OPENING_SQUARE_BRACKET = '&#91;'  #: [
    BACKSLASH = '&#92;'  #: \
    CLOSING_SQUARE_BRACKET = '&#93;'  #: ]
    CARET = '&#94;'  #: ^
    UNDERSCORE = '&#95;'  #: _
    GRAVE_ACCENT = '&#96;'  #:
    LOWERCASE_A = '&#97;'  #: a
    LOWERCASE_B = '&#98;'  #: b
    LOWERCASE_C = '&#99;'  #: c
    LOWERCASE_D = '&#100;'  #: d
    LOWERCASE_E = '&#101;'  #: e
    LOWERCASE_F = '&#102;'  #: f
    LOWERCASE_G = '&#103;'  #: g
    LOWERCASE_H = '&#104;'  #: h
    LOWERCASE_I = '&#105;'  #: i
    LOWERCASE_J = '&#106;'  #: j
    LOWERCASE_K = '&#107;'  #: k
    LOWERCASE_L = '&#108;'  #: l
    LOWERCASE_M = '&#109;'  #: m
    LOWERCASE_N = '&#110;'  #: n
    LOWERCASE_O = '&#111;'  #: o
    LOWERCASE_P = '&#112;'  #: p
    LOWERCASE_Q = '&#113;'  #: q
    LOWERCASE_R = '&#114;'  #: r
    LOWERCASE_S = '&#115;'  #: s
    LOWERCASE_T = '&#116;'  #: t
    LOWERCASE_U = '&#117;'  #: u
    LOWERCASE_V = '&#118;'  #: v
    LOWERCASE_W = '&#119;'  #: w
    LOWERCASE_X = '&#120;'  #: x
    LOWERCASE_Y = '&#121;'  #: y
    LOWERCASE_Z = '&#122;'  #: z

    OPENING_CURLY_BRACE = '&#123;'  #: {
    LEFT_CURLY_BRACE = '&#123;'  #: {
    VERTICAL_BAR = '&#124;'  #: |
    CLOSING_CURLY_BRACE = '&#125;'  #: }
    RIGHT_CURLY_BRACE = '&#125;'  #: }
    TILDE = '&#126;'  #: ~

    # ISO-8859-1 Characters
    AGRAVE = '&Agrave;'  #: À
    AACUTE = '&Aacute;'  #: Á
    ACIRC = '&Acirc;'  #: Â
    ATILDE = '&Atilde;'  #: Ã
    AUML = '&Auml;'  #: Ä
    ARING = '&Aring;'  #: Å
    AELIG = '&AElig;'  #: Æ
    CCEDIL = '&Ccedil;'  #: Ç
    EGRAVE = '&Egrave;'  #: È
    EACUTE = '&Eacute;'  #: É
    ECIRC = '&Ecirc;'  #: Ê
    EUML = '&Euml;'  #: Ë
    IGRAVE = '&Igrave;'  #: Ì
    IACUTE = '&Iacute;'  #: Í
    ICIRC = '&Icirc;'  #: Î
    IUML = '&Iuml;'  #: Ï
    ETH = '&ETH;'  #: Ð
    NTILDE = '&Ntilde;'  #: Ñ
    OGRAVE = '&Ograve;'  #: Ò
    OACUTE = '&Oacute;'  #: Ó
    OCIRC = '&Ocirc;'  #: Ô
    OTILDE = '&Otilde;'  #: Õ
    OUML = '&Ouml;'  #: Ö
    OSLASH = '&Oslash;'  #: Ø
    UGRAVE = '&Ugrave;'  #: Ù
    UACUTE = '&Uacute;'  #: Ú
    UCIRC = '&Ucirc;'  #: Û
    UUML = '&Uuml;'  #: Ü
    YACUTE = '&Yacute;'  #: Ý
    THORN = '&THORN;'  #: Þ
    SZLIG = '&szlig;'  #: ß
    AGRAVE = '&agrave;'  #: à
    AACUTE = '&aacute;'  #: á
    ACIRC = '&acirc;'  #: â
    ATILDE = '&atilde;'  #: ã
    AUML = '&auml;'  #: ä
    ARING = '&aring;'  #: å
    AELIG = '&aelig;'  #: æ
    CCEDIL = '&ccedil;'  #: ç
    EGRAVE = '&egrave;'  #: è
    EACUTE = '&eacute;'  #: é
    ECIRC = '&ecirc;'  #: ê
    EUML = '&euml;'  #: ë
    IGRAVE = '&igrave;'  #: ì
    IACUTE = '&iacute;'  #: í
    ICIRC = '&icirc;'  #: î
    IUML = '&iuml;'  #: ï
    ETH = '&eth;'  #: ð
    NTILDE = '&ntilde;'  #: ñ
    OGRAVE = '&ograve;'  #: ò
    OACUTE = '&oacute;'  #: ó
    OCIRC = '&ocirc;'  #: ô
    OTILDE = '&otilde;'  #: õ
    OUML = '&ouml;'  #: ö
    OSLASH = '&oslash;'  #: ø
    UGRAVE = '&ugrave;'  #: ù
    UACUTE = '&uacute;'  #: ú
    UCIRC = '&ucirc;'  #: û
    UUML = '&uuml;'  #: ü
    YACUTE = '&yacute;'  #: ý
    THORN = '&thorn;'  #: þ
    YUML = '&yuml;'  #: ÿ

    # ISO-8859-1 Symbols
    NBSP = '&nbsp;'  #:
    IEXCL = '&iexcl;'  #: ¡
    CENT = '&cent;'  #: ¢
    POUND = '&pound;'  #: £
    CURREN = '&curren;'  #: ¤
    YEN = '&yen;'  #: ¥
    BRVBAR = '&brvbar;'  #: ¦
    SECT = '&sect;'  #: §
    UML = '&uml;'  #: ¨
    COPY = '&copy;'  #: ©
    COPYRIGHT = '&copy;'  #: ©
    ORDF = '&ordf;'  #: ª
    LAQUO = '&laquo;'  #: «
    NOT = '&not;'  #: ¬
    # ­   &shy;   &#173;  Soft hyphen
    REG = '&reg;'  #: ®
    MACR = '&macr;'  #: ¯
    DEG = '&deg;'  #: °
    PLUSMN = '&plusmn;'  #: ±
    SUP2 = '&sup2;'  #: ²
    SUP3 = '&sup3;'  #: ³
    ACUTE = '&acute;'  #: ´
    MICRO = '&micro;'  #: µ
    PARA = '&para;'  #: ¶
    CEDIL = '&cedil;'  #: ¸
    SUP1 = '&sup1;'  #: ¹
    ORDM = '&ordm;'  #: º
    RAQUO = '&raquo;'  #: »
    FRAC14 = '&frac14;'  #: ¼
    FRAC12 = '&frac12;'  #: ½
    FRAC34 = '&frac34;'  #: ¾
    IQUEST = '&iquest;'  #: ¿
    TIMES = '&times;'  #: ×
    DIVIDE = '&divide;'  #: ÷

    # Math Symbols
    FORALL = '&forall;'  #: ∀
    PART = '&part;'  #: ∂
    EXIST = '&exist;'  #: ∃
    EMPTY = '&empty;'  #: ∅
    NABLA = '&nabla;'  #: ∇
    ISIN = '&isin;'  #: ∈
    NOTIN = '&notin;'  #: ∉
    NI = '&ni;'  #: ∋
    PROD = '&prod;'  #: ∏
    SUM = '&sum;'  #: ∑
    MINUS = '&minus;'  #: −
    LOWAST = '&lowast;'  #: ∗
    RADIC = '&radic;'  #: √
    PROP = '&prop;'  #: ∝
    INFIN = '&infin;'  #: ∞
    ANG = '&ang;'  #: ∠
    AND = '&and;'  #: ∧
    OR = '&or;'  #: ∨
    CAP = '&cap;'  #: ∩
    CUP = '&cup;'  #: ∪
    INT = '&int;'  #: ∫
    THERE4 = '&there4;'  #: ∴
    SIM = '&sim;'  #: ∼
    CONG = '&cong;'  #: ≅
    ASYMP = '&asymp;'  #: ≈
    NE = '&ne;'  #: ≠
    EQUIV = '&equiv;'  #: ≡
    LE = '&le;'  #: ≤
    GE = '&ge;'  #: ≥
    SUB = '&sub;'  #: ⊂
    SUP = '&sup;'  #: ⊃
    NSUB = '&nsub;'  #: ⊄
    SUBE = '&sube;'  #: ⊆
    SUPE = '&supe;'  #: ⊇
    OPLUS = '&oplus;'  #: ⊕
    OTIMES = '&otimes;'  #: ⊗
    PERP = '&perp;'  #: ⊥
    SDOT = '&sdot;'  #: ⋅

    # Greek Letters
    ALPHA = '&Alpha;'  #: Α
    BETA = '&Beta;'  #: Β
    GAMMA = '&Gamma;'  #: Γ
    DELTA = '&Delta;'  #: Δ
    EPSILON = '&Epsilon;'  #: Ε
    ZETA = '&Zeta;'  #: Ζ
    ETA = '&Eta;'  #: Η
    THETA = '&Theta;'  #: Θ
    IOTA = '&Iota;'  #: Ι
    KAPPA = '&Kappa;'  #: Κ
    LAMBDA = '&Lambda;'  #: Λ
    MU = '&Mu;'  #: Μ
    NU = '&Nu;'  #: Ν
    XI = '&Xi;'  #: Ξ
    OMICRON = '&Omicron;'  #: Ο
    PI = '&Pi;'  #: Π
    RHO = '&Rho;'  #: Ρ
    SIGMA = '&Sigma;'  #: Σ
    TAU = '&Tau;'  #: Τ
    UPSILON = '&Upsilon;'  #: Υ
    PHI = '&Phi;'  #: Φ
    CHI = '&Chi;'  #: Χ
    PSI = '&Psi;'  #: Ψ
    OMEGA = '&Omega;'  #: Ω
    ALPHA = '&alpha;'  #: α
    BETA = '&beta;'  #: β
    GAMMA = '&gamma;'  #: γ
    DELTA = '&delta;'  #: δ
    EPSILON = '&epsilon;'  #: ε
    ZETA = '&zeta;'  #: ζ
    ETA = '&eta;'  #: η
    THETA = '&theta;'  #: θ
    IOTA = '&iota;'  #: ι
    KAPPA = '&kappa;'  #: κ
    LAMBDA = '&lambda;'  #: λ
    MU = '&mu;'  #: μ
    NU = '&nu;'  #: ν
    XI = '&xi;'  #: ξ
    OMICRON = '&omicron;'  #: ο
    PI = '&pi;'  #: π
    RHO = '&rho;'  #: ρ
    SIGMAF = '&sigmaf;'  #: ς
    SIGMA = '&sigma;'  #: σ
    TAU = '&tau;'  #: τ
    UPSILON = '&upsilon;'  #: υ
    PHI = '&phi;'  #: φ
    CHI = '&chi;'  #: χ
    PSI = '&psi;'  #: ψ
    OMEGA = '&omega;'  #: ω
    THETASYM = '&thetasym;'  #: ϑ
    UPSIH = '&upsih;'  #: ϒ
    PIV = '&piv;'  #: ϖ

    OELIG = '&OElig;'  #: Œ
    oeLIG = '&oelig;'  #: œ
    SCARON = '&Scaron;'  #: Š
    Scaron = '&Scaron;'  #: Š
    scaron = '&scaron;'  #: š
    YUML = '&Yuml;'  #: Ÿ
    FNOF = '&fnof;'  #: ƒ
    CIRC = '&circ;'  #: ˆ
    TILDE = '&tilde;'  #: ˜

    #     &ensp;  &#8194; En space
    #     &emsp;  &#8195; Em space
    #     &thinsp;    &#8201; Thin space
    # ‌   &zwnj;  &#8204; Zero width non-joiner
    # ‍   &zwj;   &#8205; Zero width joiner
    # ‎   &lrm;   &#8206; Left-to-right mark
    # ‏   &rlm;   &#8207; Right-to-left mark

    NDASH = '&ndash;'  #: –
    MDASH = '&mdash;'  #: —
    LSQUO = '&lsquo;'  #: ‘
    RSQUO = '&rsquo;'  #: ’
    SBQUO = '&sbquo;'  #: ‚
    LDQUO = '&ldquo;'  #: “
    RDQUO = '&rdquo;'  #: ”
    BDQUO = '&bdquo;'  #: „
    DAGGER = '&dagger;'  #: †
    DAGGER = '&Dagger;'  #: ‡
    BULL = '&bull;'  #: •
    HELLIP = '&hellip;'  #: …
    PERMIL = '&permil;'  #: ‰
    PRIME = '&prime;'  #: ′
    PRIME = '&Prime;'  #: ″
    LSAQUO = '&lsaquo;'  #: ‹
    RSAQUO = '&rsaquo;'  #: ›
    OLINE = '&oline;'  #: ‾
    EURO = '&euro;'  #: €
    TRADE = '&trade;'  #: ™
    TRADEMARK = '&trade;'  #: ™

    # ARROWS
    LARR = '&larr;'  #: ←
    LEFT = '&larr;'  #: ←
    UARR = '&uarr;'  #: ↑
    UP = '&uarr;'  #: ↑
    RARR = '&rarr;'  #: →
    RIGHT = '&rarr;'  #: →
    DARR = '&darr;'  #: ↓
    DOWN = '&darr;'  #: ↓

    HARR = '&harr;'  #: ↔
    CRARR = '&crarr;'  #: ↵
    LCEIL = '&lceil;'  #: ⌈
    RCEIL = '&rceil;'  #: ⌉
    LFLOOR = '&lfloor;'  #: ⌊
    RFLOOR = '&rfloor;'  #: ⌋
    LOZ = '&loz;'  #: ◊

    SPADES = '&spades;'  #: ♠
    CLUBS = '&clubs;'  #: ♣
    HEARTS = '&hearts;'  #: ♥
    DIAMS = '&diams;'  #: ♦
    DIAMONDS = '&diams;'  #: ♦

    SUNG = '&sung;'  #: ♪
    FLAT = '&flat;'  #: ♭
    NATUR = '&natur;'  #: ♮
    NATURAL = '&natural;'  #: ♮
    SHARP = '&sharp;'  #: ♯

    CHECK = "&check;"  #: ✓
    CHECKMARK = "&checkmark;"  #: ✓
    TICK = "&check;"  #: ✓
    CROSS = "&cross;"  #: ✗

    OHM = '&ohm;'  #: Ω
    MHO = '&mho;'  #: ℧

    FRAC13 = '&frac13;'  #: ⅓
    FRAC23 = '&frac23;'  #: ⅔
    FRAC15 = '&frac15;'  #: ⅕
    FRAC25 = '&frac25;'  #: ⅖
    FRAC35 = '&frac35;'  #: ⅗
    FRAC45 = '&frac45;'  #: ⅘
    FRAC16 = '&frac16;'  #: ⅙
    FRAC56 = '&frac56;'  #: ⅚
    FRAC18 = '&frac18;'  #: ⅛
    FRAC38 = '&frac38;'  #: ⅜
    FRAC58 = '&frac58;'  #: ⅝
    FRAC78 = '&frac78;'  #: ⅞

    STAR = "&star;"  #: ☆
    STARF = "&starf;"  #: ★
    BIGSTAR = "&bigstar;"
    PHONE = "&phone;"  #: ☎
    FEMALE = "&female;"  #: ♀
    MALE = "&male;"  #: ♂
