"""
    domonic.constants.entities
    ====================================

"""


class Entity():

    # __slots__ = ('entity',)

    def __init__(self, entity: str) -> None:
        self.entity = entity

    def __str__(self) -> str:
        import html
        return html.unescape(self.character)


class Char():

    def __init__(self, character: str) -> None:
        self.character = character

    def __str__(self) -> str:
        import html
        return html.escape(self.character)

    # def __repr__(self):
    #     return self.character

    # web
    # ASCII Characters (Printable)
    SPACE: str = '&#32;'
    EXCLAMATION_MARK: str = '&#33;'  #: !
    QUOTATION_MARK: str = '&#34;'  #: "
    NUMBER_SIGN: str = '&#35;'  #: #
    DOLLAR_SIGN: str = '&#36;'  #: $
    PERCENT_SIGN: str = '&#37;'  #: %
    AMPERSAND: str = '&amp;'  #: &
    APOSTROPHE: str = '&#39;'  #: '
    OPENING_PARENTHESIS: str = '&#40;'  #: (
    LEFT_PARENTHESIS: str = '&#40;'  #: (
    CLOSING_PARENTHESIS: str = '&#41;'  #: )
    RIGHT_PARENTHESIS: str = '&#41;'  #: )
    ASTERISK: str = '&#42;'  #: *
    PLUS_SIGN: str = '&#43;'  #: +
    COMMA: str = '&#44;'  #: ,
    HYPHEN: str = '&#45;'  #: -
    PERIOD: str = '&#46;'  #: .
    SLASH: str = '&#47;'  #: /
    ZERO: str = '&#48;'  #: 0
    ONE: str = '&#49;'  #: 1
    TWO: str = '&#50;'  #: 2
    THREE: str = '&#51;'  #: 3
    FOUR: str = '&#52;'  #: 4
    FIVE: str = '&#53;'  #: 5
    SIX: str = '&#54;'  #: 6
    SEVEN: str = '&#55;'  #: 7
    EIGHT: str = '&#56;'  #: 8
    NINE: str = '&#57;'  #: 9

    COLON: str = '&#58;'  #: :
    SEMICOLON: str = '&#59;'  #: ;
    LESS_THAN: str = '&lt;'  #: <
    EQUALS_SIGN: str = '&#61;'  # :: str =
    GREATER_THAN: str = '&gt;'  #: >
    QUESTION_MARK: str = '&#63;'  #: ?
    AT_SIGN: str = '&#64;'  #: @

    UPPERCASE_A: str = '&#65;'  #: A
    UPPERCASE_B: str = '&#66;'  #: B
    UPPERCASE_C: str = '&#67;'  #: C
    UPPERCASE_D: str = '&#68;'  #: D
    UPPERCASE_E: str = '&#69;'  #: E
    UPPERCASE_F: str = '&#70;'  #: F
    UPPERCASE_G: str = '&#71;'  #: G
    UPPERCASE_H: str = '&#72;'  #: H
    UPPERCASE_I: str = '&#73;'  #: I
    UPPERCASE_J: str = '&#74;'  #: J
    UPPERCASE_K: str = '&#75;'  #: K
    UPPERCASE_L: str = '&#76;'  #: L
    UPPERCASE_M: str = '&#77;'  #: M
    UPPERCASE_N: str = '&#78;'  #: N
    UPPERCASE_O: str = '&#79;'  #: O
    UPPERCASE_P: str = '&#80;'  #: P
    UPPERCASE_Q: str = '&#81;'  #: Q
    UPPERCASE_R: str = '&#82;'  #: R
    UPPERCASE_S: str = '&#83;'  #: S
    UPPERCASE_T: str = '&#84;'  #: T
    UPPERCASE_U: str = '&#85;'  #: U
    UPPERCASE_V: str = '&#86;'  #: V
    UPPERCASE_W: str = '&#87;'  #: W
    UPPERCASE_X: str = '&#88;'  #: X
    UPPERCASE_Y: str = '&#89;'  #: Y
    UPPERCASE_Z: str = '&#90;'  #: Z

    OPENING_SQUARE_BRACKET: str = '&#91;'  #: [
    BACKSLASH: str = '&#92;'  #: \
    CLOSING_SQUARE_BRACKET: str = '&#93;'  #: ]
    CARET: str = '&#94;'  #: ^
    UNDERSCORE: str = '&#95;'  #: _
    GRAVE_ACCENT: str = '&#96;'  #:
    LOWERCASE_A: str = '&#97;'  #: a
    LOWERCASE_B: str = '&#98;'  #: b
    LOWERCASE_C: str = '&#99;'  #: c
    LOWERCASE_D: str = '&#100;'  #: d
    LOWERCASE_E: str = '&#101;'  #: e
    LOWERCASE_F: str = '&#102;'  #: f
    LOWERCASE_G: str = '&#103;'  #: g
    LOWERCASE_H: str = '&#104;'  #: h
    LOWERCASE_I: str = '&#105;'  #: i
    LOWERCASE_J: str = '&#106;'  #: j
    LOWERCASE_K: str = '&#107;'  #: k
    LOWERCASE_L: str = '&#108;'  #: l
    LOWERCASE_M: str = '&#109;'  #: m
    LOWERCASE_N: str = '&#110;'  #: n
    LOWERCASE_O: str = '&#111;'  #: o
    LOWERCASE_P: str = '&#112;'  #: p
    LOWERCASE_Q: str = '&#113;'  #: q
    LOWERCASE_R: str = '&#114;'  #: r
    LOWERCASE_S: str = '&#115;'  #: s
    LOWERCASE_T: str = '&#116;'  #: t
    LOWERCASE_U: str = '&#117;'  #: u
    LOWERCASE_V: str = '&#118;'  #: v
    LOWERCASE_W: str = '&#119;'  #: w
    LOWERCASE_X: str = '&#120;'  #: x
    LOWERCASE_Y: str = '&#121;'  #: y
    LOWERCASE_Z: str = '&#122;'  #: z

    OPENING_CURLY_BRACE: str = '&#123;'  #: {
    LEFT_CURLY_BRACE: str = '&#123;'  #: {
    VERTICAL_BAR: str = '&#124;'  #: |
    CLOSING_CURLY_BRACE: str = '&#125;'  #: }
    RIGHT_CURLY_BRACE: str = '&#125;'  #: }
    TILDE: str = '&#126;'  #: ~

    # ISO-8859-1 Characters
    AGRAVE: str = '&Agrave;'  #: À
    AACUTE: str = '&Aacute;'  #: Á
    ACIRC: str = '&Acirc;'  #: Â
    ATILDE: str = '&Atilde;'  #: Ã
    AUML: str = '&Auml;'  #: Ä
    ARING: str = '&Aring;'  #: Å
    AELIG: str = '&AElig;'  #: Æ
    CCEDIL: str = '&Ccedil;'  #: Ç
    EGRAVE: str = '&Egrave;'  #: È
    EACUTE: str = '&Eacute;'  #: É
    ECIRC: str = '&Ecirc;'  #: Ê
    EUML: str = '&Euml;'  #: Ë
    IGRAVE: str = '&Igrave;'  #: Ì
    IACUTE: str = '&Iacute;'  #: Í
    ICIRC: str = '&Icirc;'  #: Î
    IUML: str = '&Iuml;'  #: Ï
    ETH: str = '&ETH;'  #: Ð
    NTILDE: str = '&Ntilde;'  #: Ñ
    OGRAVE: str = '&Ograve;'  #: Ò
    OACUTE: str = '&Oacute;'  #: Ó
    OCIRC: str = '&Ocirc;'  #: Ô
    OTILDE: str = '&Otilde;'  #: Õ
    OUML: str = '&Ouml;'  #: Ö
    OSLASH: str = '&Oslash;'  #: Ø
    UGRAVE: str = '&Ugrave;'  #: Ù
    UACUTE: str = '&Uacute;'  #: Ú
    UCIRC: str = '&Ucirc;'  #: Û
    UUML: str = '&Uuml;'  #: Ü
    YACUTE: str = '&Yacute;'  #: Ý
    THORN: str = '&THORN;'  #: Þ
    SZLIG: str = '&szlig;'  #: ß
    AGRAVE: str = '&agrave;'  #: à
    AACUTE: str = '&aacute;'  #: á
    ACIRC: str = '&acirc;'  #: â
    ATILDE: str = '&atilde;'  #: ã
    AUML: str = '&auml;'  #: ä
    ARING: str = '&aring;'  #: å
    AELIG: str = '&aelig;'  #: æ
    CCEDIL: str = '&ccedil;'  #: ç
    EGRAVE: str = '&egrave;'  #: è
    EACUTE: str = '&eacute;'  #: é
    ECIRC: str = '&ecirc;'  #: ê
    EUML: str = '&euml;'  #: ë
    IGRAVE: str = '&igrave;'  #: ì
    IACUTE: str = '&iacute;'  #: í
    ICIRC: str = '&icirc;'  #: î
    IUML: str = '&iuml;'  #: ï
    ETH: str = '&eth;'  #: ð
    NTILDE: str = '&ntilde;'  #: ñ
    OGRAVE: str = '&ograve;'  #: ò
    OACUTE: str = '&oacute;'  #: ó
    OCIRC: str = '&ocirc;'  #: ô
    OTILDE: str = '&otilde;'  #: õ
    OUML: str = '&ouml;'  #: ö
    OSLASH: str = '&oslash;'  #: ø
    UGRAVE: str = '&ugrave;'  #: ù
    UACUTE: str = '&uacute;'  #: ú
    UCIRC: str = '&ucirc;'  #: û
    UUML: str = '&uuml;'  #: ü
    YACUTE: str = '&yacute;'  #: ý
    THORN: str = '&thorn;'  #: þ
    YUML: str = '&yuml;'  #: ÿ

    # ISO-8859-1 Symbols
    NBSP: str = '&nbsp;'  #:
    IEXCL: str = '&iexcl;'  #: ¡
    CENT: str = '&cent;'  #: ¢
    POUND: str = '&pound;'  #: £
    CURREN: str = '&curren;'  #: ¤
    YEN: str = '&yen;'  #: ¥
    BRVBAR: str = '&brvbar;'  #: ¦
    SECT: str = '&sect;'  #: §
    UML: str = '&uml;'  #: ¨
    COPY: str = '&copy;'  #: ©
    COPYRIGHT: str = '&copy;'  #: ©
    ORDF: str = '&ordf;'  #: ª
    LAQUO: str = '&laquo;'  #: «
    NOT: str = '&not;'  #: ¬
    # ­   &shy;   &#173;  Soft hyphen
    REG: str = '&reg;'  #: ®
    MACR: str = '&macr;'  #: ¯
    DEG: str = '&deg;'  #: °
    PLUSMN: str = '&plusmn;'  #: ±
    SUP2: str = '&sup2;'  #: ²
    SUP3: str = '&sup3;'  #: ³
    ACUTE: str = '&acute;'  #: ´
    MICRO: str = '&micro;'  #: µ
    PARA: str = '&para;'  #: ¶
    CEDIL: str = '&cedil;'  #: ¸
    SUP1: str = '&sup1;'  #: ¹
    ORDM: str = '&ordm;'  #: º
    RAQUO: str = '&raquo;'  #: »
    FRAC14: str = '&frac14;'  #: ¼
    FRAC12: str = '&frac12;'  #: ½
    FRAC34: str = '&frac34;'  #: ¾
    IQUEST: str = '&iquest;'  #: ¿
    TIMES: str = '&times;'  #: ×
    DIVIDE: str = '&divide;'  #: ÷

    # Math Symbols
    FORALL: str = '&forall;'  #: ∀
    PART: str = '&part;'  #: ∂
    EXIST: str = '&exist;'  #: ∃
    EMPTY: str = '&empty;'  #: ∅
    NABLA: str = '&nabla;'  #: ∇
    ISIN: str = '&isin;'  #: ∈
    NOTIN: str = '&notin;'  #: ∉
    NI: str = '&ni;'  #: ∋
    PROD: str = '&prod;'  #: ∏
    SUM: str = '&sum;'  #: ∑
    MINUS: str = '&minus;'  #: −
    LOWAST: str = '&lowast;'  #: ∗
    RADIC: str = '&radic;'  #: √
    PROP: str = '&prop;'  #: ∝
    INFIN: str = '&infin;'  #: ∞
    ANG: str = '&ang;'  #: ∠
    AND: str = '&and;'  #: ∧
    OR: str = '&or;'  #: ∨
    CAP: str = '&cap;'  #: ∩
    CUP: str = '&cup;'  #: ∪
    INT: str = '&int;'  #: ∫
    THERE4: str = '&there4;'  #: ∴
    SIM: str = '&sim;'  #: ∼
    CONG: str = '&cong;'  #: ≅
    ASYMP: str = '&asymp;'  #: ≈
    NE: str = '&ne;'  #: ≠
    EQUIV: str = '&equiv;'  #: ≡
    LE: str = '&le;'  #: ≤
    GE: str = '&ge;'  #: ≥
    SUB: str = '&sub;'  #: ⊂
    SUP: str = '&sup;'  #: ⊃
    NSUB: str = '&nsub;'  #: ⊄
    SUBE: str = '&sube;'  #: ⊆
    SUPE: str = '&supe;'  #: ⊇
    OPLUS: str = '&oplus;'  #: ⊕
    OTIMES: str = '&otimes;'  #: ⊗
    PERP: str = '&perp;'  #: ⊥
    SDOT: str = '&sdot;'  #: ⋅

    # Greek Letters
    ALPHA: str = '&Alpha;'  #: Α
    BETA: str = '&Beta;'  #: Β
    GAMMA: str = '&Gamma;'  #: Γ
    DELTA: str = '&Delta;'  #: Δ
    EPSILON: str = '&Epsilon;'  #: Ε
    ZETA: str = '&Zeta;'  #: Ζ
    ETA: str = '&Eta;'  #: Η
    THETA: str = '&Theta;'  #: Θ
    IOTA: str = '&Iota;'  #: Ι
    KAPPA: str = '&Kappa;'  #: Κ
    LAMBDA: str = '&Lambda;'  #: Λ
    MU: str = '&Mu;'  #: Μ
    NU: str = '&Nu;'  #: Ν
    XI: str = '&Xi;'  #: Ξ
    OMICRON: str = '&Omicron;'  #: Ο
    PI: str = '&Pi;'  #: Π
    RHO: str = '&Rho;'  #: Ρ
    SIGMA: str = '&Sigma;'  #: Σ
    TAU: str = '&Tau;'  #: Τ
    UPSILON: str = '&Upsilon;'  #: Υ
    PHI: str = '&Phi;'  #: Φ
    CHI: str = '&Chi;'  #: Χ
    PSI: str = '&Psi;'  #: Ψ
    OMEGA: str = '&Omega;'  #: Ω
    ALPHA: str = '&alpha;'  #: α
    BETA: str = '&beta;'  #: β
    GAMMA: str = '&gamma;'  #: γ
    DELTA: str = '&delta;'  #: δ
    EPSILON: str = '&epsilon;'  #: ε
    ZETA: str = '&zeta;'  #: ζ
    ETA: str = '&eta;'  #: η
    THETA: str = '&theta;'  #: θ
    IOTA: str = '&iota;'  #: ι
    KAPPA: str = '&kappa;'  #: κ
    LAMBDA: str = '&lambda;'  #: λ
    MU: str = '&mu;'  #: μ
    NU: str = '&nu;'  #: ν
    XI: str = '&xi;'  #: ξ
    OMICRON: str = '&omicron;'  #: ο
    PI: str = '&pi;'  #: π
    RHO: str = '&rho;'  #: ρ
    SIGMAF: str = '&sigmaf;'  #: ς
    SIGMA: str = '&sigma;'  #: σ
    TAU: str = '&tau;'  #: τ
    UPSILON: str = '&upsilon;'  #: υ
    PHI: str = '&phi;'  #: φ
    CHI: str = '&chi;'  #: χ
    PSI: str = '&psi;'  #: ψ
    OMEGA: str = '&omega;'  #: ω
    THETASYM: str = '&thetasym;'  #: ϑ
    UPSIH: str = '&upsih;'  #: ϒ
    PIV: str = '&piv;'  #: ϖ

    OELIG: str = '&OElig;'  #: Œ
    oeLIG: str = '&oelig;'  #: œ
    SCARON: str = '&Scaron;'  #: Š
    Scaron: str = '&Scaron;'  #: Š
    scaron: str = '&scaron;'  #: š
    YUML: str = '&Yuml;'  #: Ÿ
    FNOF: str = '&fnof;'  #: ƒ
    CIRC: str = '&circ;'  #: ˆ
    TILDE: str = '&tilde;'  #: ˜

    #     &ensp;  &#8194; En space
    #     &emsp;  &#8195; Em space
    #     &thinsp;    &#8201; Thin space
    # ‌   &zwnj;  &#8204; Zero width non-joiner
    # ‍   &zwj;   &#8205; Zero width joiner
    # ‎   &lrm;   &#8206; Left-to-right mark
    # ‏   &rlm;   &#8207; Right-to-left mark

    NDASH: str = '&ndash;'  #: –
    MDASH: str = '&mdash;'  #: —
    LSQUO: str = '&lsquo;'  #: ‘
    RSQUO: str = '&rsquo;'  #: ’
    SBQUO: str = '&sbquo;'  #: ‚
    LDQUO: str = '&ldquo;'  #: “
    RDQUO: str = '&rdquo;'  #: ”
    BDQUO: str = '&bdquo;'  #: „
    DAGGER: str = '&dagger;'  #: †
    DAGGER: str = '&Dagger;'  #: ‡
    BULL: str = '&bull;'  #: •
    HELLIP: str = '&hellip;'  #: …
    PERMIL: str = '&permil;'  #: ‰
    PRIME: str = '&prime;'  #: ′
    PRIME: str = '&Prime;'  #: ″
    LSAQUO: str = '&lsaquo;'  #: ‹
    RSAQUO: str = '&rsaquo;'  #: ›
    OLINE: str = '&oline;'  #: ‾
    EURO: str = '&euro;'  #: €
    TRADE: str = '&trade;'  #: ™
    TRADEMARK: str = '&trade;'  #: ™

    # ARROWS
    LARR: str = '&larr;'  #: ←
    LEFT: str = '&larr;'  #: ←
    UARR: str = '&uarr;'  #: ↑
    UP: str = '&uarr;'  #: ↑
    RARR: str = '&rarr;'  #: →
    RIGHT: str = '&rarr;'  #: →
    DARR: str = '&darr;'  #: ↓
    DOWN: str = '&darr;'  #: ↓

    HARR: str = '&harr;'  #: ↔
    CRARR: str = '&crarr;'  #: ↵
    LCEIL: str = '&lceil;'  #: ⌈
    RCEIL: str = '&rceil;'  #: ⌉
    LFLOOR: str = '&lfloor;'  #: ⌊
    RFLOOR: str = '&rfloor;'  #: ⌋
    LOZ: str = '&loz;'  #: ◊

    SPADES: str = '&spades;'  #: ♠
    CLUBS: str = '&clubs;'  #: ♣
    HEARTS: str = '&hearts;'  #: ♥
    DIAMS: str = '&diams;'  #: ♦
    DIAMONDS: str = '&diams;'  #: ♦

    SUNG: str = '&sung;'  #: ♪
    FLAT: str = '&flat;'  #: ♭
    NATUR: str = '&natur;'  #: ♮
    NATURAL: str = '&natural;'  #: ♮
    SHARP: str = '&sharp;'  #: ♯

    CHECK: str = "&check;"  #: ✓
    CHECKMARK: str = "&checkmark;"  #: ✓
    TICK: str = "&check;"  #: ✓
    CROSS: str = "&cross;"  #: ✗

    OHM: str = '&ohm;'  #: Ω
    MHO: str = '&mho;'  #: ℧

    FRAC13: str = '&frac13;'  #: ⅓
    FRAC23: str = '&frac23;'  #: ⅔
    FRAC15: str = '&frac15;'  #: ⅕
    FRAC25: str = '&frac25;'  #: ⅖
    FRAC35: str = '&frac35;'  #: ⅗
    FRAC45: str = '&frac45;'  #: ⅘
    FRAC16: str = '&frac16;'  #: ⅙
    FRAC56: str = '&frac56;'  #: ⅚
    FRAC18: str = '&frac18;'  #: ⅛
    FRAC38: str = '&frac38;'  #: ⅜
    FRAC58: str = '&frac58;'  #: ⅝
    FRAC78: str = '&frac78;'  #: ⅞

    STAR: str = "&star;"  #: ☆
    STARF: str = "&starf;"  #: ★
    BIGSTAR: str = "&bigstar;"
    PHONE: str = "&phone;"  #: ☎
    FEMALE: str = "&female;"  #: ♀
    MALE: str = "&male;"  #: ♂
