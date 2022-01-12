"""
    domonic.constants.color
    ====================================
"""

# from typing import Union, Tuple, List, Dict, Any, Optional, Callable, cast, TypeVar, Generic, Iterable, Sequence

from typing import Tuple, Optional

from domonic.geom import vec3, vec4

# function rgb
# function rgba
# function hsl
# function hsla
# function hex
# function hexa
# function hsv


class Color():
    """ Color Functions """

    # BLACK = Color(0, 0, 0)
    # WHITE = Color(255, 255, 255)

    @staticmethod
    def random_hex() -> str:
        """[returns a random hex color i.e. #000000]

        Returns:
            [str]: [random hex color i.e. #000000]
        """
        import random

        def r():
            return random.randint(0, 255)
        # r = lambda: random.randint(0, 255)
        return '#%02X%02X%02X' % (r(), r(), r())
        # import secrets
        # rgba = '#'+secrets.token_hex(4)

    @staticmethod
    def hex2rgb(h: str) -> Tuple[int, int, int]:
        """[takes a hex color in the form of #RRGGBB and returns the rgb values as a tuple i.e (r, g, b)]

        Args:
            h ([str]): [hex string i.e #ffffff]

        Returns:
            [tuple]: [rgb tuple i.e. (255, 255, 255)]
        """
        if h[0] == '#':
            h = h.lstrip('#')
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

    # rgb = hex2rgb  # TODO - as static. but can also check if instance has value? so can get/set.

    # @staticmethod
    # def hsl2rgb(h, s, l):
    #     """ convert hsl to rgb """
    #     if s == 0:
    #         return l, l, l
    #     if l < 0.5:
    #         if s == 1:
    #             return l * (1 + l), l * 2, l * 2
    #         if s == 2:
    #             return l * 2, l * (1 + l), l * 2
    #         if s == 3:
    #             return l * 2, l * 2, l * (1 + l)
    #     else:
    #         if s == 1:
    #             return l * (1 - l), l * 2, l * 2
    #         if s == 2:
    #             return l * (1 - l), l * 2, l * (1 + l)
    #         if s == 3:
    #             return l * (1 - l), l * (1 + l), l * 2

    # @staticmethod
    # def rgb2hsl(r, g, b):
    #     """ convert rgb to hsl """
    #     maxv = max(r, g, b)
    #     minv = min(r, g, b)
    #     l = (maxv + minv) / 2
    #     if maxv == minv:
    #         return 0.0, 0.0, l
    #     s = (maxv - minv) / (maxv + minv)
    #     if r == maxv:
    #         h = (g - b) / (maxv - minv)
    #     elif g == maxv:
    #         h = 2 + (b - r) / (maxv - minv)
    #     else:
    #         h = 4 + (r - g) / (maxv - minv)
    #     h *= 60
    #     if h < 0:
    #         h += 360
    #     return h, s, l

    @staticmethod
    def rgb2hex(r: int, g: int, b: int) -> str:
        """[ takes 3 rgb values and returns a hex string i.e. #000000]

        Args:
            r ([int]): [a value between 0 and 255]
            g ([int]): [a value between 0 and 255]
            b ([int]): [a value between 0 and 255]

        Returns:
            [str]: [retuns a hex string i.e #ffffff]
        """
        #  TODO - pass tuples or
        # if isinstance(a, (int, float)):
        # elif isinstance(a, (tuple, list)):
        return '#%02x%02x%02x' % (r, g, b)

    # deprecated
    @staticmethod
    def fromRGBA(r: int, g: int, b: int, a: int = 255) -> 'Color':
        """[creates a Color from rgba values]

        Args:
            r ([int]): [a value between 0 and 255]
            g ([int]): [a value between 0 and 255]
            b ([int]): [a value between 0 and 255]
            a ([int]): [a value between 0 and 255]

        Returns:
            [type]: [a Color object]
        """
        return Color(r, g, b, a)

    # @staticmethod
    # def fromHsl(h, s, l):
    #     return Color(h, s, l)

    # deprecated
    @staticmethod
    def fromHex(hex: str) -> 'Color':
        """ create a Color from a hex string i.e. #ffffff """
        return Color(hex)

    def __init__(self, *args, **kwargs) -> None:
        """
        accepts a color in a variety of formats:
        """
        if isinstance(args[0], vec4):
            self.r = args[0][0]
            self.g = args[0][1]
            self.b = args[0][2]
            self.a = args[0][3]
        if isinstance(args[0], vec3):
            self.r = args[0][0]
            self.g = args[0][1]
            self.b = args[0][2]
        if isinstance(args[0], str):
            if args[0].startswith('#'):
                self.r, self.g, self.b = Color.hex2rgb(args[0])
        if isinstance(args[0], (int, float)):
            if len(args) == 3:
                self.r, self.g, self.b = args
            if len(args) == 4:
                self.r, self.g, self.b, self.a = args

        # self.alpha = kwargs.get('a', 1.0)
        # self.red = kwargs.get('r', self.r)
        # self.green = kwargs.get('g', self.g)
        # self.blue = kwargs.get('b', self.b)

        self.alpha = kwargs.get('alpha', 1.0)  # TODO - props instead?
        self.red = kwargs.get('red', self.r)
        self.green = kwargs.get('green', self.g)
        self.blue = kwargs.get('blue', self.b)
        # self.gray = kwargs.get('gray', self.r)
        self.hue = kwargs.get('hue', 0.0)
        self.saturation = kwargs.get('saturation', 1.0)
        self.brightness = kwargs.get('brightness', 1.0)
        self.lightness = kwargs.get('lightness', 1.0)

        # print(self.r, self.g, self.b)

    @property
    def alpha(self) -> float:
        return self.a

    @alpha.setter
    def alpha(self, value: float) -> None:
        self.a = value

    @property
    def red(self) -> float:
        return self.r

    @red.setter
    def red(self, value: float) -> None:
        self.r = value

    @property
    def green(self) -> float:
        return self.g

    @green.setter
    def green(self, value: float) -> None:
        self.g = value

    @property
    def blue(self) -> float:
        return self.b

    @blue.setter
    def blue(self, value: float) -> None:
        self.b = value

    def toRGB(self):  # : -> vec3:
        """[returns the color as RGB]

        Returns:
            [tuple]: [ (r, g, b) ]
        """
        return (self.r, self.g, self.b)

    def toHsl(self):
        """ returns the hsl for the color """
        return (self.hue, self.saturation, self.brightness)

    # def toString(self):
        # return str(self)

    def __str__(self) -> str:
        return Color.rgb2hex(self.r, self.g, self.b)

    # def __repr__(self):
    #     return str(self)

    def toHsv(self):
        """ get the hsv for the color """
        return (self.hue, self.saturation, self.brightness)

    def toCSS(self) -> str:
        """ return the color as a CSS string """
        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    def toHex(self) -> str:
        return str(self)

    def toRGBA(self):
        return (self.r, self.g, self.b, self.a)

    def toSVG(self, shape="circle", size=10):
        """ returns the color as an svg string
        Args:
            shape ([str]): [can be circle or square]
            size ([int]): [size in pixels]
        """
        if shape == "circle":
            return '<circle cx="0" cy="0" r="%d" fill="%s" />' % (size, self.toHex())
        if shape == "square":
            return '<rect x="0" y="0" width="%d" height="%d" fill="%s" />' % (size, size, self.toHex())

    # def toIMG(self, size=10):
    #     """ returns the color as an svg string
    #     Args:
    #         shape ([str]): [can be circle or square]
    #         size ([int]): [size in pixels]
    #     """
    #     import PIL.Image as Image
    #     img = Image.new('RGB', (size, size), self.toHex())
    #     return img

    def convert(self, to: str):
        """ convert the color to a different color space

        Args:
            to ([str]): [can be one of the following: 'rgb', 'hsl', 'hsv', 'hex']
        """
        if to == 'rgb':
            return self.toRGB()
        if to == 'hsl':
            return self.toHsl()
        if to == 'hsv':
            return self.toHsv()
        if to == 'hex':
            return self.toHex()
        if to == 'css':
            return self.toCSS()

    # set(*args)

    def hasAlpha(self) -> bool:
        """[does the color have an alpha channel]

        Returns:
            [bool]: [True if alpha channel exists else False]
        """
        return self.a > 0

    def equals(self, color) -> bool:
        return self.r == color.r and self.g == color.g and self.b == color.b

    def __eq__(self, other):
        """ check if two colors are equal """
        return self.r == other.r and self.g == other.g and self.b == other.b

    def __add__(self, other):
        """ add two colors together """
        return Color(self.r + other.r, self.g + other.g, self.b + other.b)

    def __sub__(self, color):
        """ subtract a color from this color """
        return Color(self.r - color.r, self.g - color.g, self.b - color.b)

    def __mul__(self, color):
        """ multiply a color with this color """
        return Color(self.r * color.r, self.g * color.g, self.b * color.b)

    def __div__(self, color):
        """ divide a color with this color """
        return Color(self.r / color.r, self.g / color.g, self.b / color.b)

    # web
    Black: str = '#000000'  #:
    Navy: str = "#000080"  #:
    DarkBlue: str = "#00008B"  #:
    MediumBlue: str = "#0000CD"  #:
    Blue: str = "#0000FF"  #:
    DarkGreen: str = "#006400"  #:
    Green: str = "#008000"  #:
    Teal: str = "#008080"  #:
    DarkCyan: str = "#008B8B"  #:
    DeepSkyBlue: str = "#00BFFF"  #:
    DarkTurquoise: str = "#00CED1"  #:
    MediumSpringGreen: str = "#00FA9A"  #:
    Lime: str = "#00FF00"  #:
    SpringGreen: str = "#00FF7F"  #:
    Aqua: str = "#00FFFF"  #:
    Cyan: str = "#00FFFF"  #:
    MidnightBlue: str = "#191970"  #:
    DodgerBlue: str = "#1E90FF"  #:
    LightSeaGreen: str = "#20B2AA"  #:
    ForestGreen: str = "#228B22"  #:
    SeaGreen: str = "#2E8B57"  #:
    DarkSlateGray: str = "#2F4F4F"  #:
    DarkSlateGrey: str = "#2F4F4F"  #:
    LimeGreen: str = "#32CD32"  #:
    MediumSeaGreen: str = "#3CB371"  #:
    Turquoise: str = "#40E0D0"  #:
    RoyalBlue: str = "#4169E1"  #:
    SteelBlue: str = "#4682B4"  #:
    DarkSlateBlue: str = "#483D8B"  #:
    MediumTurquoise: str = "#48D1CC"  #:
    Indigo: str = "#4B0082"  #:
    DarkOliveGreen: str = "#556B2F"  #:
    CadetBlue: str = "#5F9EA0"  #:
    CornflowerBlue: str = "#6495ED"  #:
    RebeccaPurple: str = "#663399"  #:
    MediumAquaMarine: str = "#66CDAA"  #:
    DimGray: str = "#696969"  #:
    DimGrey: str = "#696969"  #:
    SlateBlue: str = "#6A5ACD"  #:
    OliveDrab: str = "#6B8E23"  #:
    SlateGray: str = "#708090"  #:
    SlateGrey: str = "#708090"  #:
    LightSlateGray: str = "#778899"  #:
    LightSlateGrey: str = "#778899"  #:
    MediumSlateBlue: str = "#7B68EE"  #:
    LawnGreen: str = "#7CFC00"  #:
    Chartreuse: str = "#7FFF00"  #:
    Aquamarine: str = "#7FFFD4"  #:
    Maroon: str = "#800000"  #:
    Purple: str = "#800080"  #:
    Olive: str = "#808000"  #:
    Gray: str = "#808080"  #:
    Grey: str = "#808080"  #:
    SkyBlue: str = "#87CEEB"  #:
    LightSkyBlue: str = "#87CEFA"  #:
    BlueViolet: str = "#8A2BE2"  #:
    DarkRed: str = "#8B0000"  #:
    DarkMagenta: str = "#8B008B"  #:
    SaddleBrown: str = "#8B4513"  #:
    DarkSeaGreen: str = "#8FBC8F"  #:
    LightGreen: str = "#90EE90"  #:
    MediumPurple: str = "#9370DB"  #:
    DarkViolet: str = "#9400D3"  #:
    PaleGreen: str = "#98FB98"  #:
    DarkOrchid: str = "#9932CC"  #:
    YellowGreen: str = "#9ACD32"  #:
    Sienna: str = "#A0522D"  #:
    Brown: str = "#A52A2A"  #:
    DarkGray: str = "#A9A9A9"  #:
    DarkGrey: str = "#A9A9A9"  #:
    LightBlue: str = "#ADD8E6"  #:
    GreenYellow: str = "#ADFF2F"  #:
    PaleTurquoise: str = "#AFEEEE"  #:
    LightSteelBlue: str = "#B0C4DE"  #:
    PowderBlue: str = "#B0E0E6"  #:
    FireBrick: str = "#B22222"  #:
    DarkGoldenRod: str = "#B8860B"  #:
    MediumOrchid: str = "#BA55D3"  #:
    RosyBrown: str = "#BC8F8F"  #:
    DarkKhaki: str = "#BDB76B"  #:
    Silver: str = "#C0C0C0"  #:
    MediumVioletRed: str = "#C71585"  #:
    IndianRed: str = "#CD5C5C"  #:
    Peru: str = "#CD853F"  #:
    Chocolate: str = "#D2691E"  #:
    Tan: str = "#D2B48C"  #:
    LightGray: str = "#D3D3D3"  #:
    LightGrey: str = "#D3D3D3"  #:
    Thistle: str = "#D8BFD8"  #:
    Orchid: str = "#DA70D6"  #:
    GoldenRod: str = "#DAA520"  #:
    PaleVioletRed: str = "#DB7093"  #:
    Crimson: str = "#DC143C"  #:
    Gainsboro: str = "#DCDCDC"  #:
    Plum: str = "#DDA0DD"  #:
    BurlyWood: str = "#DEB887"  #:
    LightCyan: str = "#E0FFFF"  #:
    Lavender: str = "#E6E6FA"  #:
    DarkSalmon: str = "#E9967A"  #:
    Violet: str = "#EE82EE"  #:
    PaleGoldenRod: str = "#EEE8AA"  #:
    LightCoral: str = "#F08080"  #:
    Khaki: str = "#F0E68C"  #:
    AliceBlue: str = "#F0F8FF"  #:
    HoneyDew: str = "#F0FFF0"  #:
    Azure: str = "#F0FFFF"  #:
    SandyBrown: str = "#F4A460"  #:
    Wheat: str = "#F5DEB3"  #:
    Beige: str = "#F5F5DC"  #:
    WhiteSmoke: str = "#F5F5F5"  #:
    MintCream: str = "#F5FFFA"  #:
    GhostWhite: str = "#F8F8FF"  #:
    Salmon: str = "#FA8072"  #:
    AntiqueWhite: str = "#FAEBD7"  #:
    Linen: str = "#FAF0E6"  #:
    LightGoldenRodYellow: str = "#FAFAD2"  #:
    OldLace: str = "#FDF5E6"  #:
    Red: str = "#FF0000"  #:
    Fuchsia: str = "#FF00FF"  #:
    Magenta: str = "#FF00FF"  #:
    DeepPink: str = "#FF1493"  #:
    OrangeRed: str = "#FF4500"  #:
    Tomato: str = "#FF6347"  #:
    HotPink: str = "#FF69B4"  #:
    Coral: str = "#FF7F50"  #:
    DarkOrange: str = "#FF8C00"  #:
    LightSalmon: str = "#FFA07A"  #:
    Orange: str = "#FFA500"  #:
    LightPink: str = "#FFB6C1"  #:
    Pink: str = "#FFC0CB"  #:
    Gold: str = "#FFD700"  #:
    PeachPuff: str = "#FFDAB9"  #:
    NavajoWhite: str = "#FFDEAD"  #:
    Moccasin: str = "#FFE4B5"  #:
    Bisque: str = "#FFE4C4"  #:
    MistyRose: str = "#FFE4E1"  #:
    BlanchedAlmond: str = "#FFEBCD"  #:
    PapayaWhip: str = "#FFEFD5"  #:
    LavenderBlush: str = "#FFF0F5"  #:
    SeaShell: str = "#FFF5EE"  #:
    Cornsilk: str = "#FFF8DC"  #:
    LemonChiffon: str = "#FFFACD"  #:
    FloralWhite: str = "#FFFAF0"  #:
    Snow: str = "#FFFAFA"  #:
    Yellow: str = "#FFFF00"  #:
    LightYellow: str = "#FFFFE0"  #:
    Ivory: str = "#FFFFF0"  #:
    White: str = "#FFFFFF"  #:

    # XKCD
    acidgreen: str = "#8ffe09"  #:
    adobe: str = "#bd6c48"  #:
    algae: str = "#54ac68"  #:
    algaegreen: str = "#21c36f"  #:
    almostblack: str = "#070d0d"  #:
    amber: str = "#feb308"  #:
    amethyst: str = "#9b5fc0"  #:
    apple: str = "#6ecb3c"  #:
    applegreen: str = "#76cd26"  #:
    apricot: str = "#ffb16d"  #:
    aqua: str = "#13eac9"  #:
    aquablue: str = "#02d8e9"  #:
    aquagreen: str = "#12e193"  #:
    aquamarine: str = "#2ee8bb"  #:
    armygreen: str = "#4b5d16"  #:
    asparagus: str = "#77ab56"  #:
    aubergine: str = "#3d0734"  #:
    auburn: str = "#9a3001"  #:
    avocado: str = "#90b134"  #:
    avocadogreen: str = "#87a922"  #:
    azul: str = "#1d5dec"  #:
    azure: str = "#069af3"  #:
    babyblue: str = "#a2cffe"  #:
    babygreen: str = "#8cff9e"  #:
    babypink: str = "#ffb7ce"  #:
    babypoo: str = "#ab9004"  #:
    babypoop: str = "#937c00"  #:
    babypoopgreen: str = "#8f9805"  #:
    babypukegreen: str = "#b6c406"  #:
    babypurple: str = "#ca9bf7"  #:
    babyshitbrown: str = "#ad900d"  #:
    babyshitgreen: str = "#889717"  #:
    banana: str = "#ffff7e"  #:
    bananayellow: str = "#fafe4b"  #:
    barbiepink: str = "#fe46a5"  #:
    barfgreen: str = "#94ac02"  #:
    barney: str = "#ac1db8"  #:
    barneypurple: str = "#a00498"  #:
    battleshipgrey: str = "#6b7c85"  #:
    beige: str = "#e6daa6"  #:
    berry: str = "#990f4b"  #:
    bile: str = "#b5c306"  #:
    black: str = "#000000"  #:
    bland: str = "#afa88b"  #:
    blood: str = "#770001"  #:
    bloodorange: str = "#fe4b03"  #:
    bloodred: str = "#980002"  #:
    blue: str = "#0343df"  #:
    blueberry: str = "#464196"  #:
    blueblue: str = "#2242c7"  #:
    bluegreen: str = "#0f9b8e"  #:
    bluegrey: str = "#85a3b2"  #:
    bluepurple: str = "#5a06ef"  #:
    blueviolet: str = "#5d06e9"  #:
    bluewithahintofpurple: str = "#533cc6"  #:
    blueygreen: str = "#2bb179"  #:
    blueygrey: str = "#89a0b0"  #:
    blueypurple: str = "#6241c7"  #:
    bluish: str = "#2976bb"  #:
    bluishgreen: str = "#10a674"  #:
    bluishgrey: str = "#748b97"  #:
    bluishpurple: str = "#703be7"  #:
    blurple: str = "#5539cc"  #:
    blush: str = "#f29e8e"  #:
    blushpink: str = "#fe828c"  #:
    booger: str = "#9bb53c"  #:
    boogergreen: str = "#96b403"  #:
    bordeaux: str = "#7b002c"  #:
    boringgreen: str = "#63b365"  #:
    bottlegreen: str = "#044a05"  #:
    brick: str = "#a03623"  #:
    brickorange: str = "#c14a09"  #:
    brickred: str = "#8f1402"  #:
    brightaqua: str = "#0bf9ea"  #:
    brightblue: str = "#0165fc"  #:
    brightcyan: str = "#41fdfe"  #:
    brightgreen: str = "#01ff07"  #:
    brightlavender: str = "#c760ff"  #:
    brightlightblue: str = "#26f7fd"  #:
    brightlightgreen: str = "#2dfe54"  #:
    brightlilac: str = "#c95efb"  #:
    brightlime: str = "#87fd05"  #:
    brightlimegreen: str = "#65fe08"  #:
    brightmagenta: str = "#ff08e8"  #:
    brightolive: str = "#9cbb04"  #:
    brightorange: str = "#ff5b00"  #:
    brightpink: str = "#fe01b1"  #:
    brightpurple: str = "#be03fd"  #:
    brightred: str = "#ff000d"  #:
    brightseagreen: str = "#05ffa6"  #:
    brightskyblue: str = "#02ccfe"  #:
    brightteal: str = "#01f9c6"  #:
    brightturquoise: str = "#0ffef9"  #:
    brightviolet: str = "#ad0afd"  #:
    brightyellow: str = "#fffd01"  #:
    brightyellowgreen: str = "#9dff00"  #:
    britishracinggreen: str = "#05480d"  #:
    bronze: str = "#a87900"  #:
    brown: str = "#653700"  #:
    browngreen: str = "#706c11"  #:
    browngrey: str = "#8d8468"  #:
    brownish: str = "#9c6d57"  #:
    brownishgreen: str = "#6a6e09"  #:
    brownishgrey: str = "#86775f"  #:
    brownishorange: str = "#cb7723"  #:
    brownishpink: str = "#c27e79"  #:
    brownishpurple: str = "#76424e"  #:
    brownishred: str = "#9e3623"  #:
    brownishyellow: str = "#c9b003"  #:
    brownorange: str = "#b96902"  #:
    brownred: str = "#922b05"  #:
    brownyellow: str = "#b29705"  #:
    brownygreen: str = "#6f6c0a"  #:
    brownyorange: str = "#ca6b02"  #:
    bruise: str = "#7e4071"  #:
    bubblegum: str = "#ff6cb5"  #:
    bubblegumpink: str = "#ff69af"  #:
    buff: str = "#fef69e"  #:
    burgundy: str = "#610023"  #:
    burntorange: str = "#c04e01"  #:
    burntred: str = "#9f2305"  #:
    burntsiena: str = "#b75203"  #:
    burntsienna: str = "#b04e0f"  #:
    burntumber: str = "#a0450e"  #:
    burntyellow: str = "#d5ab09"  #:
    burple: str = "#6832e3"  #:
    butter: str = "#ffff81"  #:
    butterscotch: str = "#fdb147"  #:
    butteryellow: str = "#fffd74"  #:
    cadetblue: str = "#4e7496"  #:
    camel: str = "#c69f59"  #:
    camo: str = "#7f8f4e"  #:
    camogreen: str = "#526525"  #:
    camouflagegreen: str = "#4b6113"  #:
    canary: str = "#fdff63"  #:
    canaryyellow: str = "#fffe40"  #:
    candypink: str = "#ff63e9"  #:
    caramel: str = "#af6f09"  #:
    carmine: str = "#9d0216"  #:
    carnation: str = "#fd798f"  #:
    carnationpink: str = "#ff7fa7"  #:
    carolinablue: str = "#8ab8fe"  #:
    celadon: str = "#befdb7"  #:
    celery: str = "#c1fd95"  #:
    cement: str = "#a5a391"  #:
    cerise: str = "#de0c62"  #:
    cerulean: str = "#0485d1"  #:
    ceruleanblue: str = "#056eee"  #:
    charcoal: str = "#343837"  #:
    charcoalgrey: str = "#3c4142"  #:
    chartreuse: str = "#c1f80a"  #:
    cherry: str = "#cf0234"  #:
    cherryred: str = "#f7022a"  #:
    chestnut: str = "#742802"  #:
    chocolate: str = "#3d1c02"  #:
    chocolatebrown: str = "#411900"  #:
    cinnamon: str = "#ac4f06"  #:
    claret: str = "#680018"  #:
    clay: str = "#b66a50"  #:
    claybrown: str = "#b2713d"  #:
    clearblue: str = "#247afd"  #:
    cobalt: str = "#1e488f"  #:
    cobaltblue: str = "#030aa7"  #:
    cocoa: str = "#875f42"  #:
    coffee: str = "#a6814c"  #:
    coolblue: str = "#4984b8"  #:
    coolgreen: str = "#33b864"  #:
    coolgrey: str = "#95a3a6"  #:
    copper: str = "#b66325"  #:
    coral: str = "#fc5a50"  #:
    coralpink: str = "#ff6163"  #:
    cornflower: str = "#6a79f7"  #:
    cornflowerblue: str = "#5170d7"  #:
    cranberry: str = "#9e003a"  #:
    cream: str = "#ffffc2"  #:
    creme: str = "#ffffb6"  #:
    crimson: str = "#8c000f"  #:
    custard: str = "#fffd78"  #:
    cyan: str = "#00ffff"  #:
    dandelion: str = "#fedf08"  #:
    dark: str = "#1b2431"  #:
    darkaqua: str = "#05696b"  #:
    darkaquamarine: str = "#017371"  #:
    darkbeige: str = "#ac9362"  #:
    darkblue: str = "#030764"  #:
    darkbluegreen: str = "#005249"  #:
    darkbluegrey: str = "#1f3b4d"  #:
    darkbrown: str = "#341c02"  #:
    darkcoral: str = "#cf524e"  #:
    darkcream: str = "#fff39a"  #:
    darkcyan: str = "#0a888a"  #:
    darkforestgreen: str = "#002d04"  #:
    darkfuchsia: str = "#9d0759"  #:
    darkgold: str = "#b59410"  #:
    darkgrassgreen: str = "#388004"  #:
    darkgreen: str = "#054907"  #:
    darkgreenblue: str = "#1f6357"  #:
    darkgrey: str = "#363737"  #:
    darkgreyblue: str = "#29465b"  #:
    darkhotpink: str = "#d90166"  #:
    darkindigo: str = "#1f0954"  #:
    darkishblue: str = "#014182"  #:
    darkishgreen: str = "#287c37"  #:
    darkishpink: str = "#da467d"  #:
    darkishpurple: str = "#751973"  #:
    darkishred: str = "#a90308"  #:
    darkkhaki: str = "#9b8f55"  #:
    darklavender: str = "#856798"  #:
    darklilac: str = "#9c6da5"  #:
    darklime: str = "#84b701"  #:
    darklimegreen: str = "#7ebd01"  #:
    darkmagenta: str = "#960056"  #:
    darkmaroon: str = "#3c0008"  #:
    darkmauve: str = "#874c62"  #:
    darkmint: str = "#48c072"  #:
    darkmintgreen: str = "#20c073"  #:
    darkmustard: str = "#a88905"  #:
    darknavy: str = "#000435"  #:
    darknavyblue: str = "#00022e"  #:
    darkolive: str = "#373e02"  #:
    darkolivegreen: str = "#3c4d03"  #:
    darkorange: str = "#c65102"  #:
    darkpastelgreen: str = "#56ae57"  #:
    darkpeach: str = "#de7e5d"  #:
    darkperiwinkle: str = "#665fd1"  #:
    darkpink: str = "#cb416b"  #:
    darkplum: str = "#3f012c"  #:
    darkpurple: str = "#35063e"  #:
    darkred: str = "#840000"  #:
    darkrose: str = "#b5485d"  #:
    darkroyalblue: str = "#02066f"  #:
    darksage: str = "#598556"  #:
    darksalmon: str = "#c85a53"  #:
    darksand: str = "#a88f59"  #:
    darkseafoam: str = "#1fb57a"  #:
    darkseafoamgreen: str = "#3eaf76"  #:
    darkseagreen: str = "#11875d"  #:
    darkskyblue: str = "#448ee4"  #:
    darkslateblue: str = "#214761"  #:
    darktan: str = "#af884a"  #:
    darktaupe: str = "#7f684e"  #:
    darkteal: str = "#014d4e"  #:
    darkturquoise: str = "#045c5a"  #:
    darkviolet: str = "#34013f"  #:
    darkyellow: str = "#d5b60a"  #:
    darkyellowgreen: str = "#728f02"  #:
    deepaqua: str = "#08787f"  #:
    deepblue: str = "#040273"  #:
    deepbrown: str = "#410200"  #:
    deepgreen: str = "#02590f"  #:
    deeplavender: str = "#8d5eb7"  #:
    deeplilac: str = "#966ebd"  #:
    deepmagenta: str = "#a0025c"  #:
    deeporange: str = "#dc4d01"  #:
    deeppink: str = "#cb0162"  #:
    deeppurple: str = "#36013f"  #:
    deepred: str = "#9a0200"  #:
    deeprose: str = "#c74767"  #:
    deepseablue: str = "#015482"  #:
    deepskyblue: str = "#0d75f8"  #:
    deepteal: str = "#00555a"  #:
    deepturquoise: str = "#017374"  #:
    deepviolet: str = "#490648"  #:
    denim: str = "#3b638c"  #:
    denimblue: str = "#3b5b92"  #:
    desert: str = "#ccad60"  #:
    diarrhea: str = "#9f8303"  #:
    dirt: str = "#8a6e45"  #:
    dirtbrown: str = "#836539"  #:
    dirtyblue: str = "#3f829d"  #:
    dirtygreen: str = "#667e2c"  #:
    dirtyorange: str = "#c87606"  #:
    dirtypink: str = "#ca7b80"  #:
    dirtypurple: str = "#734a65"  #:
    dirtyyellow: str = "#cdc50a"  #:
    dodgerblue: str = "#3e82fc"  #:
    drab: str = "#828344"  #:
    drabgreen: str = "#749551"  #:
    driedblood: str = "#4b0101"  #:
    duckeggblue: str = "#c3fbf4"  #:
    dullblue: str = "#49759c"  #:
    dullbrown: str = "#876e4b"  #:
    dullgreen: str = "#74a662"  #:
    dullorange: str = "#d8863b"  #:
    dullpink: str = "#d5869d"  #:
    dullpurple: str = "#84597e"  #:
    dullred: str = "#bb3f3f"  #:
    dullteal: str = "#5f9e8f"  #:
    dullyellow: str = "#eedc5b"  #:
    dusk: str = "#4e5481"  #:
    duskblue: str = "#26538d"  #:
    duskyblue: str = "#475f94"  #:
    duskypink: str = "#cc7a8b"  #:
    duskypurple: str = "#895b7b"  #:
    duskyrose: str = "#ba6873"  #:
    dust: str = "#b2996e"  #:
    dustyblue: str = "#5a86ad"  #:
    dustygreen: str = "#76a973"  #:
    dustylavender: str = "#ac86a8"  #:
    dustyorange: str = "#f0833a"  #:
    dustypink: str = "#d58a94"  #:
    dustypurple: str = "#825f87"  #:
    dustyred: str = "#b9484e"  #:
    dustyrose: str = "#c0737a"  #:
    dustyteal: str = "#4c9085"  #:
    earth: str = "#a2653e"  #:
    eastergreen: str = "#8cfd7e"  #:
    easterpurple: str = "#c071fe"  #:
    ecru: str = "#feffca"  #:
    eggplant: str = "#380835"  #:
    eggplantpurple: str = "#430541"  #:
    eggshell: str = "#fffcc4"  #:
    eggshellblue: str = "#c4fff7"  #:
    electricblue: str = "#0652ff"  #:
    electricgreen: str = "#21fc0d"  #:
    electriclime: str = "#a8ff04"  #:
    electricpink: str = "#ff0490"  #:
    electricpurple: str = "#aa23ff"  #:
    emerald: str = "#01a049"  #:
    emeraldgreen: str = "#028f1e"  #:
    evergreen: str = "#05472a"  #:
    fadedblue: str = "#658cbb"  #:
    fadedgreen: str = "#7bb274"  #:
    fadedorange: str = "#f0944d"  #:
    fadedpink: str = "#de9dac"  #:
    fadedpurple: str = "#916e99"  #:
    fadedred: str = "#d3494e"  #:
    fadedyellow: str = "#feff7f"  #:
    fawn: str = "#cfaf7b"  #:
    fern: str = "#63a950"  #:
    ferngreen: str = "#548d44"  #:
    fireenginered: str = "#fe0002"  #:
    flatblue: str = "#3c73a8"  #:
    flatgreen: str = "#699d4c"  #:
    fluorescentgreen: str = "#08ff08"  #:
    flurogreen: str = "#0aff02"  #:
    foamgreen: str = "#90fda9"  #:
    forest: str = "#0b5509"  #:
    forestgreen: str = "#06470c"  #:
    forrestgreen: str = "#154406"  #:
    frenchblue: str = "#436bad"  #:
    freshgreen: str = "#69d84f"  #:
    froggreen: str = "#58bc08"  #:
    fuchsia: str = "#ed0dd9"  #:
    gold: str = "#dbb40c"  #:
    golden: str = "#f5bf03"  #:
    goldenbrown: str = "#b27a01"  #:
    goldenrod: str = "#f9bc08"  #:
    goldenyellow: str = "#fec615"  #:
    grape: str = "#6c3461"  #:
    grapefruit: str = "#fd5956"  #:
    grapepurple: str = "#5d1451"  #:
    grass: str = "#5cac2d"  #:
    grassgreen: str = "#3f9b0b"  #:
    grassygreen: str = "#419c03"  #:
    green: str = "#15b01a"  #:
    greenapple: str = "#5edc1f"  #:
    greenblue: str = "#01c08d"  #:
    greenbrown: str = "#544e03"  #:
    greengrey: str = "#77926f"  #:
    greenish: str = "#40a368"  #:
    greenishbeige: str = "#c9d179"  #:
    greenishblue: str = "#0b8b87"  #:
    greenishbrown: str = "#696112"  #:
    greenishcyan: str = "#2afeb7"  #:
    greenishgrey: str = "#96ae8d"  #:
    greenishtan: str = "#bccb7a"  #:
    greenishteal: str = "#32bf84"  #:
    greenishturquoise: str = "#00fbb0"  #:
    greenishyellow: str = "#cdfd02"  #:
    greenteal: str = "#0cb577"  #:
    greenyblue: str = "#42b395"  #:
    greenybrown: str = "#696006"  #:
    greenyellow: str = "#b5ce08"  #:
    greenygrey: str = "#7ea07a"  #:
    greenyyellow: str = "#c6f808"  #:
    grey: str = "#929591"  #:
    greyblue: str = "#647d8e"  #:
    greybrown: str = "#7f7053"  #:
    greygreen: str = "#86a17d"  #:
    greyish: str = "#a8a495"  #:
    greyishblue: str = "#5e819d"  #:
    greyishbrown: str = "#7a6a4f"  #:
    greyishgreen: str = "#82a67d"  #:
    greyishpink: str = "#c88d94"  #:
    greyishpurple: str = "#887191"  #:
    greyishteal: str = "#719f91"  #:
    greypink: str = "#c3909b"  #:
    greypurple: str = "#826d8c"  #:
    greyteal: str = "#5e9b8a"  #:
    grossgreen: str = "#a0bf16"  #:
    gunmetal: str = "#536267"  #:
    hazel: str = "#8e7618"  #:
    heather: str = "#a484ac"  #:
    heliotrope: str = "#d94ff5"  #:
    highlightergreen: str = "#1bfc06"  #:
    hospitalgreen: str = "#9be5aa"  #:
    hotgreen: str = "#25ff29"  #:
    hotmagenta: str = "#f504c9"  #:
    hotpink: str = "#ff028d"  #:
    hotpurple: str = "#cb00f5"  #:
    huntergreen: str = "#0b4008"  #:
    ice: str = "#d6fffa"  #:
    iceblue: str = "#d7fffe"  #:
    ickygreen: str = "#8fae22"  #:
    indianred: str = "#850e04"  #:
    indigo: str = "#380282"  #:
    indigoblue: str = "#3a18b1"  #:
    iris: str = "#6258c4"  #:
    irishgreen: str = "#019529"  #:
    ivory: str = "#ffffcb"  #:
    jade: str = "#1fa774"  #:
    jadegreen: str = "#2baf6a"  #:
    junglegreen: str = "#048243"  #:
    kelleygreen: str = "#009337"  #:
    kellygreen: str = "#02ab2e"  #:
    kermitgreen: str = "#5cb200"  #:
    keylime: str = "#aeff6e"  #:
    khaki: str = "#aaa662"  #:
    khakigreen: str = "#728639"  #:
    kiwi: str = "#9cef43"  #:
    kiwigreen: str = "#8ee53f"  #:
    lavender: str = "#c79fef"  #:
    lavenderblue: str = "#8b88f8"  #:
    lavenderpink: str = "#dd85d7"  #:
    lawngreen: str = "#4da409"  #:
    leaf: str = "#71aa34"  #:
    leafgreen: str = "#5ca904"  #:
    leafygreen: str = "#51b73b"  #:
    leather: str = "#ac7434"  #:
    lemon: str = "#fdff52"  #:
    lemongreen: str = "#adf802"  #:
    lemonlime: str = "#bffe28"  #:
    lemonyellow: str = "#fdff38"  #:
    lichen: str = "#8fb67b"  #:
    lightaqua: str = "#8cffdb"  #:
    lightaquamarine: str = "#7bfdc7"  #:
    lightbeige: str = "#fffeb6"  #:
    lightblue: str = "#7bc8f6"  #:
    lightbluegreen: str = "#7efbb3"  #:
    lightbluegrey: str = "#b7c9e2"  #:
    lightbluishgreen: str = "#76fda8"  #:
    lightbrightgreen: str = "#53fe5c"  #:
    lightbrown: str = "#ad8150"  #:
    lightburgundy: str = "#a8415b"  #:
    lightcyan: str = "#acfffc"  #:
    lighteggplant: str = "#894585"  #:
    lightergreen: str = "#75fd63"  #:
    lighterpurple: str = "#a55af4"  #:
    lightforestgreen: str = "#4f9153"  #:
    lightgold: str = "#fddc5c"  #:
    lightgrassgreen: str = "#9af764"  #:
    lightgreen: str = "#76ff7b"  #:
    lightgreenblue: str = "#56fca2"  #:
    lightgreenishblue: str = "#63f7b4"  #:
    lightgrey: str = "#d8dcd6"  #:
    lightgreyblue: str = "#9dbcd4"  #:
    lightgreygreen: str = "#b7e1a1"  #:
    lightindigo: str = "#6d5acf"  #:
    lightishblue: str = "#3d7afd"  #:
    lightishgreen: str = "#61e160"  #:
    lightishpurple: str = "#a552e6"  #:
    lightishred: str = "#fe2f4a"  #:
    lightkhaki: str = "#e6f2a2"  #:
    lightlavendar: str = "#efc0fe"  #:
    lightlavender: str = "#dfc5fe"  #:
    lightlightblue: str = "#cafffb"  #:
    lightlightgreen: str = "#c8ffb0"  #:
    lightlilac: str = "#edc8ff"  #:
    lightlime: str = "#aefd6c"  #:
    lightlimegreen: str = "#b9ff66"  #:
    lightmagenta: str = "#fa5ff7"  #:
    lightmaroon: str = "#a24857"  #:
    lightmauve: str = "#c292a1"  #:
    lightmint: str = "#b6ffbb"  #:
    lightmintgreen: str = "#a6fbb2"  #:
    lightmossgreen: str = "#a6c875"  #:
    lightmustard: str = "#f7d560"  #:
    lightnavy: str = "#155084"  #:
    lightnavyblue: str = "#2e5a88"  #:
    lightneongreen: str = "#4efd54"  #:
    lightolive: str = "#acbf69"  #:
    lightolivegreen: str = "#a4be5c"  #:
    lightorange: str = "#fdaa48"  #:
    lightpastelgreen: str = "#b2fba5"  #:
    lightpeach: str = "#ffd8b1"  #:
    lightpeagreen: str = "#c4fe82"  #:
    lightperiwinkle: str = "#c1c6fc"  #:
    lightpink: str = "#ffd1df"  #:
    lightplum: str = "#9d5783"  #:
    lightpurple: str = "#bf77f6"  #:
    lightred: str = "#ff474c"  #:
    lightrose: str = "#ffc5cb"  #:
    lightroyalblue: str = "#3a2efe"  #:
    lightsage: str = "#bcecac"  #:
    lightsalmon: str = "#fea993"  #:
    lightseafoam: str = "#a0febf"  #:
    lightseafoamgreen: str = "#a7ffb5"  #:
    lightseagreen: str = "#98f6b0"  #:
    lightskyblue: str = "#c6fcff"  #:
    lighttan: str = "#fbeeac"  #:
    lightteal: str = "#90e4c1"  #:
    lightturquoise: str = "#7ef4cc"  #:
    lighturple: str = "#b36ff6"  #:
    lightviolet: str = "#d6b4fc"  #:
    lightyellow: str = "#fffe7a"  #:
    lightyellowgreen: str = "#ccfd7f"  #:
    lightyellowishgreen: str = "#c2ff89"  #:
    lilac: str = "#cea2fd"  #:
    liliac: str = "#c48efd"  #:
    lime: str = "#aaff32"  #:
    limegreen: str = "#89fe05"  #:
    limeyellow: str = "#d0fe1d"  #:
    lipstick: str = "#d5174e"  #:
    lipstickred: str = "#c0022f"  #:
    macaroniandcheese: str = "#efb435"  #:
    magenta: str = "#c20078"  #:
    mahogany: str = "#4a0100"  #:
    maize: str = "#f4d054"  #:
    mango: str = "#ffa62b"  #:
    manilla: str = "#fffa86"  #:
    marigold: str = "#fcc006"  #:
    marine: str = "#042e60"  #:
    marineblue: str = "#01386a"  #:
    maroon: str = "#650021"  #:
    mauve: str = "#ae7181"  #:
    mediumblue: str = "#2c6fbb"  #:
    mediumbrown: str = "#7f5112"  #:
    mediumgreen: str = "#39ad48"  #:
    mediumgrey: str = "#7d7f7c"  #:
    mediumpink: str = "#f36196"  #:
    mediumpurple: str = "#9e43a2"  #:
    melon: str = "#ff7855"  #:
    merlot: str = "#730039"  #:
    metallicblue: str = "#4f738e"  #:
    midblue: str = "#276ab3"  #:
    midgreen: str = "#50a747"  #:
    midnight: str = "#03012d"  #:
    midnightblue: str = "#020035"  #:
    midnightpurple: str = "#280137"  #:
    militarygreen: str = "#667c3e"  #:
    milkchocolate: str = "#7f4e1e"  #:
    mint: str = "#9ffeb0"  #:
    mintgreen: str = "#8fff9f"  #:
    mintygreen: str = "#0bf77d"  #:
    mocha: str = "#9d7651"  #:
    moss: str = "#769958"  #:
    mossgreen: str = "#658b38"  #:
    mossygreen: str = "#638b27"  #:
    mud: str = "#735c12"  #:
    mudbrown: str = "#60460f"  #:
    muddybrown: str = "#886806"  #:
    muddygreen: str = "#657432"  #:
    muddyyellow: str = "#bfac05"  #:
    mudgreen: str = "#606602"  #:
    mulberry: str = "#920a4e"  #:
    murkygreen: str = "#6c7a0e"  #:
    mushroom: str = "#ba9e88"  #:
    mustard: str = "#ceb301"  #:
    mustardbrown: str = "#ac7e04"  #:
    mustardgreen: str = "#a8b504"  #:
    mustardyellow: str = "#d2bd0a"  #:
    mutedblue: str = "#3b719f"  #:
    mutedgreen: str = "#5fa052"  #:
    mutedpink: str = "#d1768f"  #:
    mutedpurple: str = "#805b87"  #:
    nastygreen: str = "#70b23f"  #:
    navy: str = "#01153e"  #:
    navyblue: str = "#001146"  #:
    navygreen: str = "#35530a"  #:
    neonblue: str = "#04d9ff"  #:
    neongreen: str = "#0cff0c"  #:
    neonpink: str = "#fe019a"  #:
    neonpurple: str = "#bc13fe"  #:
    neonred: str = "#ff073a"  #:
    neonyellow: str = "#cfff04"  #:
    niceblue: str = "#107ab0"  #:
    nightblue: str = "#040348"  #:
    ocean: str = "#017b92"  #:
    oceanblue: str = "#03719c"  #:
    oceangreen: str = "#3d9973"  #:
    ocher: str = "#bf9b0c"  #:
    ochre: str = "#bf9005"  #:
    ocre: str = "#c69c04"  #:
    offblue: str = "#5684ae"  #:
    offgreen: str = "#6ba353"  #:
    offwhite: str = "#ffffe4"  #:
    offyellow: str = "#f1f33f"  #:
    oldpink: str = "#c77986"  #:
    oldrose: str = "#c87f89"  #:
    olive: str = "#6e750e"  #:
    olivebrown: str = "#645403"  #:
    olivedrab: str = "#6f7632"  #:
    olivegreen: str = "#677a04"  #:
    oliveyellow: str = "#c2b709"  #:
    orange: str = "#f97306"  #:
    orangebrown: str = "#be6400"  #:
    orangeish: str = "#fd8d49"  #:
    orangepink: str = "#ff6f52"  #:
    orangered: str = "#fe420f"  #:
    orangeybrown: str = "#b16002"  #:
    orangeyellow: str = "#ffad01"  #:
    orangeyred: str = "#fa4224"  #:
    orangeyyellow: str = "#fdb915"  #:
    orangish: str = "#fc824a"  #:
    orangishbrown: str = "#b25f03"  #:
    orangishred: str = "#f43605"  #:
    orchid: str = "#c875c4"  #:
    pale: str = "#fff9d0"  #:
    paleaqua: str = "#b8ffeb"  #:
    paleblue: str = "#d0fefe"  #:
    palebrown: str = "#b1916e"  #:
    palecyan: str = "#b7fffa"  #:
    palegold: str = "#fdde6c"  #:
    palegreen: str = "#c7fdb5"  #:
    palegrey: str = "#fdfdfe"  #:
    palelavender: str = "#eecffe"  #:
    palelightgreen: str = "#b1fc99"  #:
    palelilac: str = "#e4cbff"  #:
    palelime: str = "#befd73"  #:
    palelimegreen: str = "#b1ff65"  #:
    palemagenta: str = "#d767ad"  #:
    palemauve: str = "#fed0fc"  #:
    paleolive: str = "#b9cc81"  #:
    paleolivegreen: str = "#b1d27b"  #:
    paleorange: str = "#ffa756"  #:
    palepeach: str = "#ffe5ad"  #:
    palepink: str = "#ffcfdc"  #:
    palepurple: str = "#b790d4"  #:
    palered: str = "#d9544d"  #:
    palerose: str = "#fdc1c5"  #:
    palesalmon: str = "#ffb19a"  #:
    paleskyblue: str = "#bdf6fe"  #:
    paleteal: str = "#82cbb2"  #:
    paleturquoise: str = "#a5fbd5"  #:
    paleviolet: str = "#ceaefa"  #:
    paleyellow: str = "#ffff84"  #:
    parchment: str = "#fefcaf"  #:
    pastelblue: str = "#a2bffe"  #:
    pastelgreen: str = "#b0ff9d"  #:
    pastelorange: str = "#ff964f"  #:
    pastelpink: str = "#ffbacd"  #:
    pastelpurple: str = "#caa0ff"  #:
    pastelred: str = "#db5856"  #:
    pastelyellow: str = "#fffe71"  #:
    pea: str = "#a4bf20"  #:
    peach: str = "#ffb07c"  #:
    peachypink: str = "#ff9a8a"  #:
    peacockblue: str = "#016795"  #:
    peagreen: str = "#8eab12"  #:
    pear: str = "#cbf85f"  #:
    peasoup: str = "#929901"  #:
    peasoupgreen: str = "#94a617"  #:
    periwinkle: str = "#8e82fe"  #:
    periwinkleblue: str = "#8f99fb"  #:
    perrywinkle: str = "#8f8ce7"  #:
    petrol: str = "#005f6a"  #:
    pigpink: str = "#e78ea5"  #:
    pine: str = "#2b5d34"  #:
    pinegreen: str = "#0a481e"  #:
    pink: str = "#ff81c0"  #:
    pinkish: str = "#d46a7e"  #:
    pinkishbrown: str = "#b17261"  #:
    pinkishgrey: str = "#c8aca9"  #:
    pinkishorange: str = "#ff724c"  #:
    pinkishpurple: str = "#d648d7"  #:
    pinkishred: str = "#f10c45"  #:
    pinkishtan: str = "#d99b82"  #:
    pinkpurple: str = "#ef1de7"  #:
    pinkred: str = "#f5054f"  #:
    pinky: str = "#fc86aa"  #:
    pinkypurple: str = "#c94cbe"  #:
    pinkyred: str = "#fc2647"  #:
    pissyellow: str = "#ddd618"  #:
    pistachio: str = "#c0fa8b"  #:
    plum: str = "#580f41"  #:
    plumpurple: str = "#4e0550"  #:
    poisongreen: str = "#40fd14"  #:
    poo: str = "#8f7303"  #:
    poobrown: str = "#885f01"  #:
    poop: str = "#7f5e00"  #:
    poopbrown: str = "#7a5901"  #:
    poopgreen: str = "#6f7c00"  #:
    powderblue: str = "#b1d1fc"  #:
    powderpink: str = "#ffb2d0"  #:
    primaryblue: str = "#0804f9"  #:
    prussianblue: str = "#004577"  #:
    puce: str = "#a57e52"  #:
    puke: str = "#a5a502"  #:
    pukebrown: str = "#947706"  #:
    pukegreen: str = "#9aae07"  #:
    pukeyellow: str = "#c2be0e"  #:
    pumpkin: str = "#e17701"  #:
    pumpkinorange: str = "#fb7d07"  #:
    pureblue: str = "#0203e2"  #:
    purple: str = "#7e1e9c"  #:
    purpleblue: str = "#5d21d0"  #:
    purplebrown: str = "#673a3f"  #:
    purplegrey: str = "#866f85"  #:
    purpleish: str = "#98568d"  #:
    purpleishblue: str = "#6140ef"  #:
    purpleishpink: str = "#df4ec8"  #:
    purplepink: str = "#d725de"  #:
    purplered: str = "#990147"  #:
    purpley: str = "#8756e4"  #:
    purpleyblue: str = "#5f34e7"  #:
    purpleygrey: str = "#947e94"  #:
    purpleypink: str = "#c83cb9"  #:
    purplish: str = "#94568c"  #:
    purplishblue: str = "#601ef9"  #:
    purplishbrown: str = "#6b4247"  #:
    purplishgrey: str = "#7a687f"  #:
    purplishpink: str = "#ce5dae"  #:
    purplishred: str = "#b0054b"  #:
    purply: str = "#983fb2"  #:
    purplyblue: str = "#661aee"  #:
    purplypink: str = "#f075e6"  #:
    putty: str = "#beae8a"  #:
    racinggreen: str = "#014600"  #:
    radioactivegreen: str = "#2cfa1f"  #:
    raspberry: str = "#b00149"  #:
    rawsienna: str = "#9a6200"  #:
    rawumber: str = "#a75e09"  #:
    reallylightblue: str = "#d4ffff"  #:
    red: str = "#e50000"  #:
    redbrown: str = "#8b2e16"  #:
    reddish: str = "#c44240"  #:
    reddishbrown: str = "#7f2b0a"  #:
    reddishgrey: str = "#997570"  #:
    reddishorange: str = "#f8481c"  #:
    reddishpink: str = "#fe2c54"  #:
    reddishpurple: str = "#910951"  #:
    reddybrown: str = "#6e1005"  #:
    redorange: str = "#fd3c06"  #:
    redpink: str = "#fa2a55"  #:
    redpurple: str = "#820747"  #:
    redviolet: str = "#9e0168"  #:
    redwine: str = "#8c0034"  #:
    richblue: str = "#021bf9"  #:
    richpurple: str = "#720058"  #:
    robineggblue: str = "#8af1fe"  #:
    robinsegg: str = "#6dedfd"  #:
    robinseggblue: str = "#98eff9"  #:
    rosa: str = "#fe86a4"  #:
    rose: str = "#cf6275"  #:
    rosepink: str = "#f7879a"  #:
    rosered: str = "#be013c"  #:
    rosypink: str = "#f6688e"  #:
    rouge: str = "#ab1239"  #:
    royal: str = "#0c1793"  #:
    royalblue: str = "#0504aa"  #:
    royalpurple: str = "#4b006e"  #:
    ruby: str = "#ca0147"  #:
    russet: str = "#a13905"  #:
    rust: str = "#a83c09"  #:
    rustbrown: str = "#8b3103"  #:
    rustorange: str = "#c45508"  #:
    rustred: str = "#aa2704"  #:
    rustyorange: str = "#cd5909"  #:
    rustyred: str = "#af2f0d"  #:
    saffron: str = "#feb209"  #:
    sage: str = "#87ae73"  #:
    sagegreen: str = "#88b378"  #:
    salmon: str = "#ff796c"  #:
    salmonpink: str = "#fe7b7c"  #:
    sand: str = "#e2ca76"  #:
    sandbrown: str = "#cba560"  #:
    sandstone: str = "#c9ae74"  #:
    sandy: str = "#f1da7a"  #:
    sandybrown: str = "#c4a661"  #:
    sandyellow: str = "#fce166"  #:
    sandyyellow: str = "#fdee73"  #:
    sapgreen: str = "#5c8b15"  #:
    sapphire: str = "#2138ab"  #:
    scarlet: str = "#be0119"  #:
    sea: str = "#3c9992"  #:
    seablue: str = "#047495"  #:
    seafoam: str = "#80f9ad"  #:
    seafoamblue: str = "#78d1b6"  #:
    seafoamgreen: str = "#7af9ab"  #:
    seagreen: str = "#53fca1"  #:
    seaweed: str = "#18d17b"  #:
    seaweedgreen: str = "#35ad6b"  #:
    sepia: str = "#985e2b"  #:
    shamrock: str = "#01b44c"  #:
    shamrockgreen: str = "#02c14d"  #:
    shit: str = "#7f5f00"  #:
    shitbrown: str = "#7b5804"  #:
    shitgreen: str = "#758000"  #:
    shockingpink: str = "#fe02a2"  #:
    sickgreen: str = "#9db92c"  #:
    sicklygreen: str = "#94b21c"  #:
    sicklyyellow: str = "#d0e429"  #:
    sienna: str = "#a9561e"  #:
    silver: str = "#c5c9c7"  #:
    sky: str = "#82cafc"  #:
    skyblue: str = "#75bbfd"  #:
    slate: str = "#516572"  #:
    slateblue: str = "#5b7c99"  #:
    slategreen: str = "#658d6d"  #:
    slategrey: str = "#59656d"  #:
    slimegreen: str = "#99cc04"  #:
    snot: str = "#acbb0d"  #:
    snotgreen: str = "#9dc100"  #:
    softblue: str = "#6488ea"  #:
    softgreen: str = "#6fc276"  #:
    softpink: str = "#fdb0c0"  #:
    softpurple: str = "#a66fb5"  #:
    spearmint: str = "#1ef876"  #:
    springgreen: str = "#a9f971"  #:
    spruce: str = "#0a5f38"  #:
    squash: str = "#f2ab15"  #:
    steel: str = "#738595"  #:
    steelblue: str = "#5a7d9a"  #:
    steelgrey: str = "#6f828a"  #:
    stone: str = "#ada587"  #:
    stormyblue: str = "#507b9c"  #:
    straw: str = "#fcf679"  #:
    strawberry: str = "#fb2943"  #:
    strongblue: str = "#0c06f7"  #:
    strongpink: str = "#ff0789"  #:
    sunflower: str = "#ffc512"  #:
    sunfloweryellow: str = "#ffda03"  #:
    sunnyyellow: str = "#fff917"  #:
    sunshineyellow: str = "#fffd37"  #:
    sunyellow: str = "#ffdf22"  #:
    swamp: str = "#698339"  #:
    swampgreen: str = "#748500"  #:
    tan: str = "#d1b26f"  #:
    tanbrown: str = "#ab7e4c"  #:
    tangerine: str = "#ff9408"  #:
    tangreen: str = "#a9be70"  #:
    taupe: str = "#b9a281"  #:
    tea: str = "#65ab7c"  #:
    teagreen: str = "#bdf8a3"  #:
    teal: str = "#029386"  #:
    tealblue: str = "#01889f"  #:
    tealgreen: str = "#25a36f"  #:
    tealish: str = "#24bca8"  #:
    tealishgreen: str = "#0cdc73"  #:
    terracota: str = "#cb6843"  #:
    terracotta: str = "#c9643b"  #:
    tiffanyblue: str = "#7bf2da"  #:
    tomato: str = "#ef4026"  #:
    tomatored: str = "#ec2d01"  #:
    topaz: str = "#13bbaf"  #:
    toupe: str = "#c7ac7d"  #:
    toxicgreen: str = "#61de2a"  #:
    treegreen: str = "#2a7e19"  #:
    trueblue: str = "#010fcc"  #:
    truegreen: str = "#089404"  #:
    turquoise: str = "#06c2ac"  #:
    turquoiseblue: str = "#06b1c4"  #:
    turquoisegreen: str = "#04f489"  #:
    turtlegreen: str = "#75b84f"  #:
    twilight: str = "#4e518b"  #:
    twilightblue: str = "#0a437a"  #:
    uglyblue: str = "#31668a"  #:
    uglybrown: str = "#7d7103"  #:
    uglygreen: str = "#7a9703"  #:
    uglypink: str = "#cd7584"  #:
    uglypurple: str = "#a442a0"  #:
    uglyyellow: str = "#d0c101"  #:
    ultramarine: str = "#2000b1"  #:
    ultramarineblue: str = "#1805db"  #:
    umber: str = "#b26400"  #:
    velvet: str = "#750851"  #:
    vermillion: str = "#f4320c"  #:
    verydarkblue: str = "#000133"  #:
    verydarkbrown: str = "#1d0200"  #:
    verydarkgreen: str = "#062e03"  #:
    verydarkpurple: str = "#2a0134"  #:
    verylightblue: str = "#d5ffff"  #:
    verylightbrown: str = "#d3b683"  #:
    verylightgreen: str = "#d1ffbd"  #:
    verylightpink: str = "#fff4f2"  #:
    verylightpurple: str = "#f6cefc"  #:
    verypaleblue: str = "#d6fffe"  #:
    verypalegreen: str = "#cffdbc"  #:
    vibrantblue: str = "#0339f8"  #:
    vibrantgreen: str = "#0add08"  #:
    vibrantpurple: str = "#ad03de"  #:
    violet: str = "#9a0eea"  #:
    violetblue: str = "#510ac9"  #:
    violetpink: str = "#fb5ffc"  #:
    violetred: str = "#a50055"  #:
    viridian: str = "#1e9167"  #:
    vividblue: str = "#152eff"  #:
    vividgreen: str = "#2fef10"  #:
    vividpurple: str = "#9900fa"  #:
    vomit: str = "#a2a415"  #:
    vomitgreen: str = "#89a203"  #:
    vomityellow: str = "#c7c10c"  #:
    warmblue: str = "#4b57db"  #:
    warmbrown: str = "#964e02"  #:
    warmgrey: str = "#978a84"  #:
    warmpink: str = "#fb5581"  #:
    warmpurple: str = "#952e8f"  #:
    washedoutgreen: str = "#bcf5a6"  #:
    waterblue: str = "#0e87cc"  #:
    watermelon: str = "#fd4659"  #:
    weirdgreen: str = "#3ae57f"  #:
    wheat: str = "#fbdd7e"  #:
    white: str = "#ffffff"  #:
    windowsblue: str = "#3778bf"  #:
    wine: str = "#80013f"  #:
    winered: str = "#7b0323"  #:
    wintergreen: str = "#20f986"  #:
    wisteria: str = "#a87dc2"  #:
    yellow: str = "#ffff14"  #:
    yellowbrown: str = "#b79400"  #:
    yellowgreen: str = "#bbf90f"  #:
    yellowish: str = "#faee66"  #:
    yellowishbrown: str = "#9b7a01"  #:
    yellowishgreen: str = "#b0dd16"  #:
    yellowishorange: str = "#ffab0f"  #:
    yellowishtan: str = "#fcfc81"  #:
    yellowochre: str = "#cb9d06"  #:
    yelloworange: str = "#fcb001"  #:
    yellowtan: str = "#ffe36e"  #:
    yellowybrown: str = "#ae8b0c"  #:
    yellowygreen: str = "#bff128"  #:
