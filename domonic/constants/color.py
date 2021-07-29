"""
    domonic.constants.color
    ====================================
"""

from domonic.geom import vec3, vec4


class Color():
    """
        a class for all possible colors
    """

    @staticmethod
    def random_hex():
        """[random_hex]

        Returns:
            [str]: [random hex color]
        """
        import random
        r = lambda: random.randint(0, 255)
        return '#%02X%02X%02X' % (r(), r(), r())
        # import secrets
        # rgba = '#'+secrets.token_hex(4)

    @staticmethod
    def hex2rgb(h):
        """[hex2rgb]

        Args:
            h ([str]): [hex string]

        Returns:
            [tuple]: [rgb tuple]
        """
        if h[0] == '#':
            h = h.lstrip('#')
        return tuple(int(h[i:i + 2], 16) for i in (0, 2, 4))

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
    def rgb2hex(a, b, c):
        """[rgb2hex]

        Args:
            a ([type]): [r]
            b ([type]): [g]
            c ([type]): [b]

        Returns:
            [str]: [retuns a hex string]
        """
        #  TODO - pass tuples or
        # if isinstance(a, (int, float)):
        # elif isinstance(a, (tuple, list)):
        return '#%02x%02x%02x' % (a, b, c)

    @staticmethod
    def fromRGBA(r, g, b, a):
        return Color(r, g, b, a)

    # @staticmethod
    # def fromHsl(h, s, l):
    #     return Color(h, s, l)

    @staticmethod
    def fromHex(hex):
        """ create a color from a hex string """
        return Color(hex)

    def __init__(self, *args, **kwargs):
        # TODO - if type is vec4 / if hash / if word
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

        self.alpha = kwargs.get('alpha', 1.0)
        self.red = kwargs.get('red', self.r)
        self.green = kwargs.get('green', self.g)
        self.blue = kwargs.get('blue', self.b)
        # self.gray = kwargs.get('gray', self.r)
        self.hue = kwargs.get('hue', 0.0)
        self.saturation = kwargs.get('saturation', 1.0)
        self.brightness = kwargs.get('brightness', 1.0)
        self.lightness = kwargs.get('lightness', 1.0)

        # print(self.r, self.g, self.b)

    def toRGB(self):
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

    def __str__(self):
        return Color.rgb2hex(self.r, self.g, self.b)

    def toHsv(self):
        """ get the hsv for the color """
        return (self.hue, self.saturation, self.brightness)

    def toCSS(self):
        """ return the color as a CSS string """
        return '#%02x%02x%02x' % (self.r, self.g, self.b)

    def toHex(self):
        return str(self)

    def toRGBA(self):
        return (self.r, self.g, self.b, self.a)

    def convert(self, to):
        """ convert the color to another color """
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

    def hasAlpha(self):
        """[does the color have an alpha channel]

        Returns:
            [bool]: [True if alpha channel exists else False]
        """
        return self.a > 0

    def equals(self, color):
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
    Black = "#000000"  #:
    Navy = "#000080"  #:
    DarkBlue = "#00008B"  #:
    MediumBlue = "#0000CD"  #:
    Blue = "#0000FF"  #:
    DarkGreen = "#006400"  #:
    Green = "#008000"  #:
    Teal = "#008080"  #:
    DarkCyan = "#008B8B"  #:
    DeepSkyBlue = "#00BFFF"  #:
    DarkTurquoise = "#00CED1"  #:
    MediumSpringGreen = "#00FA9A"  #:
    Lime = "#00FF00"  #:
    SpringGreen = "#00FF7F"  #:
    Aqua = "#00FFFF"  #:
    Cyan = "#00FFFF"  #:
    MidnightBlue = "#191970"  #:
    DodgerBlue = "#1E90FF"  #:
    LightSeaGreen = "#20B2AA"  #:
    ForestGreen = "#228B22"  #:
    SeaGreen = "#2E8B57"  #:
    DarkSlateGray = "#2F4F4F"  #:
    DarkSlateGrey = "#2F4F4F"  #:
    LimeGreen = "#32CD32"  #:
    MediumSeaGreen = "#3CB371"  #:
    Turquoise = "#40E0D0"  #:
    RoyalBlue = "#4169E1"  #:
    SteelBlue = "#4682B4"  #:
    DarkSlateBlue = "#483D8B"  #:
    MediumTurquoise = "#48D1CC"  #:
    Indigo = "#4B0082"  #:
    DarkOliveGreen = "#556B2F"  #:
    CadetBlue = "#5F9EA0"  #:
    CornflowerBlue = "#6495ED"  #:
    RebeccaPurple = "#663399"  #:
    MediumAquaMarine = "#66CDAA"  #:
    DimGray = "#696969"  #:
    DimGrey = "#696969"  #:
    SlateBlue = "#6A5ACD"  #:
    OliveDrab = "#6B8E23"  #:
    SlateGray = "#708090"  #:
    SlateGrey = "#708090"  #:
    LightSlateGray = "#778899"  #:
    LightSlateGrey = "#778899"  #:
    MediumSlateBlue = "#7B68EE"  #:
    LawnGreen = "#7CFC00"  #:
    Chartreuse = "#7FFF00"  #:
    Aquamarine = "#7FFFD4"  #:
    Maroon = "#800000"  #:
    Purple = "#800080"  #:
    Olive = "#808000"  #:
    Gray = "#808080"  #:
    Grey = "#808080"  #:
    SkyBlue = "#87CEEB"  #:
    LightSkyBlue = "#87CEFA"  #:
    BlueViolet = "#8A2BE2"  #:
    DarkRed = "#8B0000"  #:
    DarkMagenta = "#8B008B"  #:
    SaddleBrown = "#8B4513"  #:
    DarkSeaGreen = "#8FBC8F"  #:
    LightGreen = "#90EE90"  #:
    MediumPurple = "#9370DB"  #:
    DarkViolet = "#9400D3"  #:
    PaleGreen = "#98FB98"  #:
    DarkOrchid = "#9932CC"  #:
    YellowGreen = "#9ACD32"  #:
    Sienna = "#A0522D"  #:
    Brown = "#A52A2A"  #:
    DarkGray = "#A9A9A9"  #:
    DarkGrey = "#A9A9A9"  #:
    LightBlue = "#ADD8E6"  #:
    GreenYellow = "#ADFF2F"  #:
    PaleTurquoise = "#AFEEEE"  #:
    LightSteelBlue = "#B0C4DE"  #:
    PowderBlue = "#B0E0E6"  #:
    FireBrick = "#B22222"  #:
    DarkGoldenRod = "#B8860B"  #:
    MediumOrchid = "#BA55D3"  #:
    RosyBrown = "#BC8F8F"  #:
    DarkKhaki = "#BDB76B"  #:
    Silver = "#C0C0C0"  #:
    MediumVioletRed = "#C71585"  #:
    IndianRed = "#CD5C5C"  #:
    Peru = "#CD853F"  #:
    Chocolate = "#D2691E"  #:
    Tan = "#D2B48C"  #:
    LightGray = "#D3D3D3"  #:
    LightGrey = "#D3D3D3"  #:
    Thistle = "#D8BFD8"  #:
    Orchid = "#DA70D6"  #:
    GoldenRod = "#DAA520"  #:
    PaleVioletRed = "#DB7093"  #:
    Crimson = "#DC143C"  #:
    Gainsboro = "#DCDCDC"  #:
    Plum = "#DDA0DD"  #:
    BurlyWood = "#DEB887"  #:
    LightCyan = "#E0FFFF"  #:
    Lavender = "#E6E6FA"  #:
    DarkSalmon = "#E9967A"  #:
    Violet = "#EE82EE"  #:
    PaleGoldenRod = "#EEE8AA"  #:
    LightCoral = "#F08080"  #:
    Khaki = "#F0E68C"  #:
    AliceBlue = "#F0F8FF"  #:
    HoneyDew = "#F0FFF0"  #:
    Azure = "#F0FFFF"  #:
    SandyBrown = "#F4A460"  #:
    Wheat = "#F5DEB3"  #:
    Beige = "#F5F5DC"  #:
    WhiteSmoke = "#F5F5F5"  #:
    MintCream = "#F5FFFA"  #:
    GhostWhite = "#F8F8FF"  #:
    Salmon = "#FA8072"  #:
    AntiqueWhite = "#FAEBD7"  #:
    Linen = "#FAF0E6"  #:
    LightGoldenRodYellow = "#FAFAD2"  #:
    OldLace = "#FDF5E6"  #:
    Red = "#FF0000"  #:
    Fuchsia = "#FF00FF"  #:
    Magenta = "#FF00FF"  #:
    DeepPink = "#FF1493"  #:
    OrangeRed = "#FF4500"  #:
    Tomato = "#FF6347"  #:
    HotPink = "#FF69B4"  #:
    Coral = "#FF7F50"  #:
    DarkOrange = "#FF8C00"  #:
    LightSalmon = "#FFA07A"  #:
    Orange = "#FFA500"  #:
    LightPink = "#FFB6C1"  #:
    Pink = "#FFC0CB"  #:
    Gold = "#FFD700"  #:
    PeachPuff = "#FFDAB9"  #:
    NavajoWhite = "#FFDEAD"  #:
    Moccasin = "#FFE4B5"  #:
    Bisque = "#FFE4C4"  #:
    MistyRose = "#FFE4E1"  #:
    BlanchedAlmond = "#FFEBCD"  #:
    PapayaWhip = "#FFEFD5"  #:
    LavenderBlush = "#FFF0F5"  #:
    SeaShell = "#FFF5EE"  #:
    Cornsilk = "#FFF8DC"  #:
    LemonChiffon = "#FFFACD"  #:
    FloralWhite = "#FFFAF0"  #:
    Snow = "#FFFAFA"  #:
    Yellow = "#FFFF00"  #:
    LightYellow = "#FFFFE0"  #:
    Ivory = "#FFFFF0"  #:
    White = "#FFFFFF"  #:

    # XKCD
    acidgreen = "#8ffe09"  #:
    adobe = "#bd6c48"  #:
    algae = "#54ac68"  #:
    algaegreen = "#21c36f"  #:
    almostblack = "#070d0d"  #:
    amber = "#feb308"  #:
    amethyst = "#9b5fc0"  #:
    apple = "#6ecb3c"  #:
    applegreen = "#76cd26"  #:
    apricot = "#ffb16d"  #:
    aqua = "#13eac9"  #:
    aquablue = "#02d8e9"  #:
    aquagreen = "#12e193"  #:
    aquamarine = "#2ee8bb"  #:
    armygreen = "#4b5d16"  #:
    asparagus = "#77ab56"  #:
    aubergine = "#3d0734"  #:
    auburn = "#9a3001"  #:
    avocado = "#90b134"  #:
    avocadogreen = "#87a922"  #:
    azul = "#1d5dec"  #:
    azure = "#069af3"  #:
    babyblue = "#a2cffe"  #:
    babygreen = "#8cff9e"  #:
    babypink = "#ffb7ce"  #:
    babypoo = "#ab9004"  #:
    babypoop = "#937c00"  #:
    babypoopgreen = "#8f9805"  #:
    babypukegreen = "#b6c406"  #:
    babypurple = "#ca9bf7"  #:
    babyshitbrown = "#ad900d"  #:
    babyshitgreen = "#889717"  #:
    banana = "#ffff7e"  #:
    bananayellow = "#fafe4b"  #:
    barbiepink = "#fe46a5"  #:
    barfgreen = "#94ac02"  #:
    barney = "#ac1db8"  #:
    barneypurple = "#a00498"  #:
    battleshipgrey = "#6b7c85"  #:
    beige = "#e6daa6"  #:
    berry = "#990f4b"  #:
    bile = "#b5c306"  #:
    black = "#000000"  #:
    bland = "#afa88b"  #:
    blood = "#770001"  #:
    bloodorange = "#fe4b03"  #:
    bloodred = "#980002"  #:
    blue = "#0343df"  #:
    blueberry = "#464196"  #:
    blueblue = "#2242c7"  #:
    bluegreen = "#0f9b8e"  #:
    bluegrey = "#85a3b2"  #:
    bluepurple = "#5a06ef"  #:
    blueviolet = "#5d06e9"  #:
    bluewithahintofpurple = "#533cc6"  #:
    blueygreen = "#2bb179"  #:
    blueygrey = "#89a0b0"  #:
    blueypurple = "#6241c7"  #:
    bluish = "#2976bb"  #:
    bluishgreen = "#10a674"  #:
    bluishgrey = "#748b97"  #:
    bluishpurple = "#703be7"  #:
    blurple = "#5539cc"  #:
    blush = "#f29e8e"  #:
    blushpink = "#fe828c"  #:
    booger = "#9bb53c"  #:
    boogergreen = "#96b403"  #:
    bordeaux = "#7b002c"  #:
    boringgreen = "#63b365"  #:
    bottlegreen = "#044a05"  #:
    brick = "#a03623"  #:
    brickorange = "#c14a09"  #:
    brickred = "#8f1402"  #:
    brightaqua = "#0bf9ea"  #:
    brightblue = "#0165fc"  #:
    brightcyan = "#41fdfe"  #:
    brightgreen = "#01ff07"  #:
    brightlavender = "#c760ff"  #:
    brightlightblue = "#26f7fd"  #:
    brightlightgreen = "#2dfe54"  #:
    brightlilac = "#c95efb"  #:
    brightlime = "#87fd05"  #:
    brightlimegreen = "#65fe08"  #:
    brightmagenta = "#ff08e8"  #:
    brightolive = "#9cbb04"  #:
    brightorange = "#ff5b00"  #:
    brightpink = "#fe01b1"  #:
    brightpurple = "#be03fd"  #:
    brightred = "#ff000d"  #:
    brightseagreen = "#05ffa6"  #:
    brightskyblue = "#02ccfe"  #:
    brightteal = "#01f9c6"  #:
    brightturquoise = "#0ffef9"  #:
    brightviolet = "#ad0afd"  #:
    brightyellow = "#fffd01"  #:
    brightyellowgreen = "#9dff00"  #:
    britishracinggreen = "#05480d"  #:
    bronze = "#a87900"  #:
    brown = "#653700"  #:
    browngreen = "#706c11"  #:
    browngrey = "#8d8468"  #:
    brownish = "#9c6d57"  #:
    brownishgreen = "#6a6e09"  #:
    brownishgrey = "#86775f"  #:
    brownishorange = "#cb7723"  #:
    brownishpink = "#c27e79"  #:
    brownishpurple = "#76424e"  #:
    brownishred = "#9e3623"  #:
    brownishyellow = "#c9b003"  #:
    brownorange = "#b96902"  #:
    brownred = "#922b05"  #:
    brownyellow = "#b29705"  #:
    brownygreen = "#6f6c0a"  #:
    brownyorange = "#ca6b02"  #:
    bruise = "#7e4071"  #:
    bubblegum = "#ff6cb5"  #:
    bubblegumpink = "#ff69af"  #:
    buff = "#fef69e"  #:
    burgundy = "#610023"  #:
    burntorange = "#c04e01"  #:
    burntred = "#9f2305"  #:
    burntsiena = "#b75203"  #:
    burntsienna = "#b04e0f"  #:
    burntumber = "#a0450e"  #:
    burntyellow = "#d5ab09"  #:
    burple = "#6832e3"  #:
    butter = "#ffff81"  #:
    butterscotch = "#fdb147"  #:
    butteryellow = "#fffd74"  #:
    cadetblue = "#4e7496"  #:
    camel = "#c69f59"  #:
    camo = "#7f8f4e"  #:
    camogreen = "#526525"  #:
    camouflagegreen = "#4b6113"  #:
    canary = "#fdff63"  #:
    canaryyellow = "#fffe40"  #:
    candypink = "#ff63e9"  #:
    caramel = "#af6f09"  #:
    carmine = "#9d0216"  #:
    carnation = "#fd798f"  #:
    carnationpink = "#ff7fa7"  #:
    carolinablue = "#8ab8fe"  #:
    celadon = "#befdb7"  #:
    celery = "#c1fd95"  #:
    cement = "#a5a391"  #:
    cerise = "#de0c62"  #:
    cerulean = "#0485d1"  #:
    ceruleanblue = "#056eee"  #:
    charcoal = "#343837"  #:
    charcoalgrey = "#3c4142"  #:
    chartreuse = "#c1f80a"  #:
    cherry = "#cf0234"  #:
    cherryred = "#f7022a"  #:
    chestnut = "#742802"  #:
    chocolate = "#3d1c02"  #:
    chocolatebrown = "#411900"  #:
    cinnamon = "#ac4f06"  #:
    claret = "#680018"  #:
    clay = "#b66a50"  #:
    claybrown = "#b2713d"  #:
    clearblue = "#247afd"  #:
    cobalt = "#1e488f"  #:
    cobaltblue = "#030aa7"  #:
    cocoa = "#875f42"  #:
    coffee = "#a6814c"  #:
    coolblue = "#4984b8"  #:
    coolgreen = "#33b864"  #:
    coolgrey = "#95a3a6"  #:
    copper = "#b66325"  #:
    coral = "#fc5a50"  #:
    coralpink = "#ff6163"  #:
    cornflower = "#6a79f7"  #:
    cornflowerblue = "#5170d7"  #:
    cranberry = "#9e003a"  #:
    cream = "#ffffc2"  #:
    creme = "#ffffb6"  #:
    crimson = "#8c000f"  #:
    custard = "#fffd78"  #:
    cyan = "#00ffff"  #:
    dandelion = "#fedf08"  #:
    dark = "#1b2431"  #:
    darkaqua = "#05696b"  #:
    darkaquamarine = "#017371"  #:
    darkbeige = "#ac9362"  #:
    darkblue = "#030764"  #:
    darkbluegreen = "#005249"  #:
    darkbluegrey = "#1f3b4d"  #:
    darkbrown = "#341c02"  #:
    darkcoral = "#cf524e"  #:
    darkcream = "#fff39a"  #:
    darkcyan = "#0a888a"  #:
    darkforestgreen = "#002d04"  #:
    darkfuchsia = "#9d0759"  #:
    darkgold = "#b59410"  #:
    darkgrassgreen = "#388004"  #:
    darkgreen = "#054907"  #:
    darkgreenblue = "#1f6357"  #:
    darkgrey = "#363737"  #:
    darkgreyblue = "#29465b"  #:
    darkhotpink = "#d90166"  #:
    darkindigo = "#1f0954"  #:
    darkishblue = "#014182"  #:
    darkishgreen = "#287c37"  #:
    darkishpink = "#da467d"  #:
    darkishpurple = "#751973"  #:
    darkishred = "#a90308"  #:
    darkkhaki = "#9b8f55"  #:
    darklavender = "#856798"  #:
    darklilac = "#9c6da5"  #:
    darklime = "#84b701"  #:
    darklimegreen = "#7ebd01"  #:
    darkmagenta = "#960056"  #:
    darkmaroon = "#3c0008"  #:
    darkmauve = "#874c62"  #:
    darkmint = "#48c072"  #:
    darkmintgreen = "#20c073"  #:
    darkmustard = "#a88905"  #:
    darknavy = "#000435"  #:
    darknavyblue = "#00022e"  #:
    darkolive = "#373e02"  #:
    darkolivegreen = "#3c4d03"  #:
    darkorange = "#c65102"  #:
    darkpastelgreen = "#56ae57"  #:
    darkpeach = "#de7e5d"  #:
    darkperiwinkle = "#665fd1"  #:
    darkpink = "#cb416b"  #:
    darkplum = "#3f012c"  #:
    darkpurple = "#35063e"  #:
    darkred = "#840000"  #:
    darkrose = "#b5485d"  #:
    darkroyalblue = "#02066f"  #:
    darksage = "#598556"  #:
    darksalmon = "#c85a53"  #:
    darksand = "#a88f59"  #:
    darkseafoam = "#1fb57a"  #:
    darkseafoamgreen = "#3eaf76"  #:
    darkseagreen = "#11875d"  #:
    darkskyblue = "#448ee4"  #:
    darkslateblue = "#214761"  #:
    darktan = "#af884a"  #:
    darktaupe = "#7f684e"  #:
    darkteal = "#014d4e"  #:
    darkturquoise = "#045c5a"  #:
    darkviolet = "#34013f"  #:
    darkyellow = "#d5b60a"  #:
    darkyellowgreen = "#728f02"  #:
    deepaqua = "#08787f"  #:
    deepblue = "#040273"  #:
    deepbrown = "#410200"  #:
    deepgreen = "#02590f"  #:
    deeplavender = "#8d5eb7"  #:
    deeplilac = "#966ebd"  #:
    deepmagenta = "#a0025c"  #:
    deeporange = "#dc4d01"  #:
    deeppink = "#cb0162"  #:
    deeppurple = "#36013f"  #:
    deepred = "#9a0200"  #:
    deeprose = "#c74767"  #:
    deepseablue = "#015482"  #:
    deepskyblue = "#0d75f8"  #:
    deepteal = "#00555a"  #:
    deepturquoise = "#017374"  #:
    deepviolet = "#490648"  #:
    denim = "#3b638c"  #:
    denimblue = "#3b5b92"  #:
    desert = "#ccad60"  #:
    diarrhea = "#9f8303"  #:
    dirt = "#8a6e45"  #:
    dirtbrown = "#836539"  #:
    dirtyblue = "#3f829d"  #:
    dirtygreen = "#667e2c"  #:
    dirtyorange = "#c87606"  #:
    dirtypink = "#ca7b80"  #:
    dirtypurple = "#734a65"  #:
    dirtyyellow = "#cdc50a"  #:
    dodgerblue = "#3e82fc"  #:
    drab = "#828344"  #:
    drabgreen = "#749551"  #:
    driedblood = "#4b0101"  #:
    duckeggblue = "#c3fbf4"  #:
    dullblue = "#49759c"  #:
    dullbrown = "#876e4b"  #:
    dullgreen = "#74a662"  #:
    dullorange = "#d8863b"  #:
    dullpink = "#d5869d"  #:
    dullpurple = "#84597e"  #:
    dullred = "#bb3f3f"  #:
    dullteal = "#5f9e8f"  #:
    dullyellow = "#eedc5b"  #:
    dusk = "#4e5481"  #:
    duskblue = "#26538d"  #:
    duskyblue = "#475f94"  #:
    duskypink = "#cc7a8b"  #:
    duskypurple = "#895b7b"  #:
    duskyrose = "#ba6873"  #:
    dust = "#b2996e"  #:
    dustyblue = "#5a86ad"  #:
    dustygreen = "#76a973"  #:
    dustylavender = "#ac86a8"  #:
    dustyorange = "#f0833a"  #:
    dustypink = "#d58a94"  #:
    dustypurple = "#825f87"  #:
    dustyred = "#b9484e"  #:
    dustyrose = "#c0737a"  #:
    dustyteal = "#4c9085"  #:
    earth = "#a2653e"  #:
    eastergreen = "#8cfd7e"  #:
    easterpurple = "#c071fe"  #:
    ecru = "#feffca"  #:
    eggplant = "#380835"  #:
    eggplantpurple = "#430541"  #:
    eggshell = "#fffcc4"  #:
    eggshellblue = "#c4fff7"  #:
    electricblue = "#0652ff"  #:
    electricgreen = "#21fc0d"  #:
    electriclime = "#a8ff04"  #:
    electricpink = "#ff0490"  #:
    electricpurple = "#aa23ff"  #:
    emerald = "#01a049"  #:
    emeraldgreen = "#028f1e"  #:
    evergreen = "#05472a"  #:
    fadedblue = "#658cbb"  #:
    fadedgreen = "#7bb274"  #:
    fadedorange = "#f0944d"  #:
    fadedpink = "#de9dac"  #:
    fadedpurple = "#916e99"  #:
    fadedred = "#d3494e"  #:
    fadedyellow = "#feff7f"  #:
    fawn = "#cfaf7b"  #:
    fern = "#63a950"  #:
    ferngreen = "#548d44"  #:
    fireenginered = "#fe0002"  #:
    flatblue = "#3c73a8"  #:
    flatgreen = "#699d4c"  #:
    fluorescentgreen = "#08ff08"  #:
    flurogreen = "#0aff02"  #:
    foamgreen = "#90fda9"  #:
    forest = "#0b5509"  #:
    forestgreen = "#06470c"  #:
    forrestgreen = "#154406"  #:
    frenchblue = "#436bad"  #:
    freshgreen = "#69d84f"  #:
    froggreen = "#58bc08"  #:
    fuchsia = "#ed0dd9"  #:
    gold = "#dbb40c"  #:
    golden = "#f5bf03"  #:
    goldenbrown = "#b27a01"  #:
    goldenrod = "#f9bc08"  #:
    goldenyellow = "#fec615"  #:
    grape = "#6c3461"  #:
    grapefruit = "#fd5956"  #:
    grapepurple = "#5d1451"  #:
    grass = "#5cac2d"  #:
    grassgreen = "#3f9b0b"  #:
    grassygreen = "#419c03"  #:
    green = "#15b01a"  #:
    greenapple = "#5edc1f"  #:
    greenblue = "#01c08d"  #:
    greenbrown = "#544e03"  #:
    greengrey = "#77926f"  #:
    greenish = "#40a368"  #:
    greenishbeige = "#c9d179"  #:
    greenishblue = "#0b8b87"  #:
    greenishbrown = "#696112"  #:
    greenishcyan = "#2afeb7"  #:
    greenishgrey = "#96ae8d"  #:
    greenishtan = "#bccb7a"  #:
    greenishteal = "#32bf84"  #:
    greenishturquoise = "#00fbb0"  #:
    greenishyellow = "#cdfd02"  #:
    greenteal = "#0cb577"  #:
    greenyblue = "#42b395"  #:
    greenybrown = "#696006"  #:
    greenyellow = "#b5ce08"  #:
    greenygrey = "#7ea07a"  #:
    greenyyellow = "#c6f808"  #:
    grey = "#929591"  #:
    greyblue = "#647d8e"  #:
    greybrown = "#7f7053"  #:
    greygreen = "#86a17d"  #:
    greyish = "#a8a495"  #:
    greyishblue = "#5e819d"  #:
    greyishbrown = "#7a6a4f"  #:
    greyishgreen = "#82a67d"  #:
    greyishpink = "#c88d94"  #:
    greyishpurple = "#887191"  #:
    greyishteal = "#719f91"  #:
    greypink = "#c3909b"  #:
    greypurple = "#826d8c"  #:
    greyteal = "#5e9b8a"  #:
    grossgreen = "#a0bf16"  #:
    gunmetal = "#536267"  #:
    hazel = "#8e7618"  #:
    heather = "#a484ac"  #:
    heliotrope = "#d94ff5"  #:
    highlightergreen = "#1bfc06"  #:
    hospitalgreen = "#9be5aa"  #:
    hotgreen = "#25ff29"  #:
    hotmagenta = "#f504c9"  #:
    hotpink = "#ff028d"  #:
    hotpurple = "#cb00f5"  #:
    huntergreen = "#0b4008"  #:
    ice = "#d6fffa"  #:
    iceblue = "#d7fffe"  #:
    ickygreen = "#8fae22"  #:
    indianred = "#850e04"  #:
    indigo = "#380282"  #:
    indigoblue = "#3a18b1"  #:
    iris = "#6258c4"  #:
    irishgreen = "#019529"  #:
    ivory = "#ffffcb"  #:
    jade = "#1fa774"  #:
    jadegreen = "#2baf6a"  #:
    junglegreen = "#048243"  #:
    kelleygreen = "#009337"  #:
    kellygreen = "#02ab2e"  #:
    kermitgreen = "#5cb200"  #:
    keylime = "#aeff6e"  #:
    khaki = "#aaa662"  #:
    khakigreen = "#728639"  #:
    kiwi = "#9cef43"  #:
    kiwigreen = "#8ee53f"  #:
    lavender = "#c79fef"  #:
    lavenderblue = "#8b88f8"  #:
    lavenderpink = "#dd85d7"  #:
    lawngreen = "#4da409"  #:
    leaf = "#71aa34"  #:
    leafgreen = "#5ca904"  #:
    leafygreen = "#51b73b"  #:
    leather = "#ac7434"  #:
    lemon = "#fdff52"  #:
    lemongreen = "#adf802"  #:
    lemonlime = "#bffe28"  #:
    lemonyellow = "#fdff38"  #:
    lichen = "#8fb67b"  #:
    lightaqua = "#8cffdb"  #:
    lightaquamarine = "#7bfdc7"  #:
    lightbeige = "#fffeb6"  #:
    lightblue = "#7bc8f6"  #:
    lightbluegreen = "#7efbb3"  #:
    lightbluegrey = "#b7c9e2"  #:
    lightbluishgreen = "#76fda8"  #:
    lightbrightgreen = "#53fe5c"  #:
    lightbrown = "#ad8150"  #:
    lightburgundy = "#a8415b"  #:
    lightcyan = "#acfffc"  #:
    lighteggplant = "#894585"  #:
    lightergreen = "#75fd63"  #:
    lighterpurple = "#a55af4"  #:
    lightforestgreen = "#4f9153"  #:
    lightgold = "#fddc5c"  #:
    lightgrassgreen = "#9af764"  #:
    lightgreen = "#76ff7b"  #:
    lightgreenblue = "#56fca2"  #:
    lightgreenishblue = "#63f7b4"  #:
    lightgrey = "#d8dcd6"  #:
    lightgreyblue = "#9dbcd4"  #:
    lightgreygreen = "#b7e1a1"  #:
    lightindigo = "#6d5acf"  #:
    lightishblue = "#3d7afd"  #:
    lightishgreen = "#61e160"  #:
    lightishpurple = "#a552e6"  #:
    lightishred = "#fe2f4a"  #:
    lightkhaki = "#e6f2a2"  #:
    lightlavendar = "#efc0fe"  #:
    lightlavender = "#dfc5fe"  #:
    lightlightblue = "#cafffb"  #:
    lightlightgreen = "#c8ffb0"  #:
    lightlilac = "#edc8ff"  #:
    lightlime = "#aefd6c"  #:
    lightlimegreen = "#b9ff66"  #:
    lightmagenta = "#fa5ff7"  #:
    lightmaroon = "#a24857"  #:
    lightmauve = "#c292a1"  #:
    lightmint = "#b6ffbb"  #:
    lightmintgreen = "#a6fbb2"  #:
    lightmossgreen = "#a6c875"  #:
    lightmustard = "#f7d560"  #:
    lightnavy = "#155084"  #:
    lightnavyblue = "#2e5a88"  #:
    lightneongreen = "#4efd54"  #:
    lightolive = "#acbf69"  #:
    lightolivegreen = "#a4be5c"  #:
    lightorange = "#fdaa48"  #:
    lightpastelgreen = "#b2fba5"  #:
    lightpeach = "#ffd8b1"  #:
    lightpeagreen = "#c4fe82"  #:
    lightperiwinkle = "#c1c6fc"  #:
    lightpink = "#ffd1df"  #:
    lightplum = "#9d5783"  #:
    lightpurple = "#bf77f6"  #:
    lightred = "#ff474c"  #:
    lightrose = "#ffc5cb"  #:
    lightroyalblue = "#3a2efe"  #:
    lightsage = "#bcecac"  #:
    lightsalmon = "#fea993"  #:
    lightseafoam = "#a0febf"  #:
    lightseafoamgreen = "#a7ffb5"  #:
    lightseagreen = "#98f6b0"  #:
    lightskyblue = "#c6fcff"  #:
    lighttan = "#fbeeac"  #:
    lightteal = "#90e4c1"  #:
    lightturquoise = "#7ef4cc"  #:
    lighturple = "#b36ff6"  #:
    lightviolet = "#d6b4fc"  #:
    lightyellow = "#fffe7a"  #:
    lightyellowgreen = "#ccfd7f"  #:
    lightyellowishgreen = "#c2ff89"  #:
    lilac = "#cea2fd"  #:
    liliac = "#c48efd"  #:
    lime = "#aaff32"  #:
    limegreen = "#89fe05"  #:
    limeyellow = "#d0fe1d"  #:
    lipstick = "#d5174e"  #:
    lipstickred = "#c0022f"  #:
    macaroniandcheese = "#efb435"  #:
    magenta = "#c20078"  #:
    mahogany = "#4a0100"  #:
    maize = "#f4d054"  #:
    mango = "#ffa62b"  #:
    manilla = "#fffa86"  #:
    marigold = "#fcc006"  #:
    marine = "#042e60"  #:
    marineblue = "#01386a"  #:
    maroon = "#650021"  #:
    mauve = "#ae7181"  #:
    mediumblue = "#2c6fbb"  #:
    mediumbrown = "#7f5112"  #:
    mediumgreen = "#39ad48"  #:
    mediumgrey = "#7d7f7c"  #:
    mediumpink = "#f36196"  #:
    mediumpurple = "#9e43a2"  #:
    melon = "#ff7855"  #:
    merlot = "#730039"  #:
    metallicblue = "#4f738e"  #:
    midblue = "#276ab3"  #:
    midgreen = "#50a747"  #:
    midnight = "#03012d"  #:
    midnightblue = "#020035"  #:
    midnightpurple = "#280137"  #:
    militarygreen = "#667c3e"  #:
    milkchocolate = "#7f4e1e"  #:
    mint = "#9ffeb0"  #:
    mintgreen = "#8fff9f"  #:
    mintygreen = "#0bf77d"  #:
    mocha = "#9d7651"  #:
    moss = "#769958"  #:
    mossgreen = "#658b38"  #:
    mossygreen = "#638b27"  #:
    mud = "#735c12"  #:
    mudbrown = "#60460f"  #:
    muddybrown = "#886806"  #:
    muddygreen = "#657432"  #:
    muddyyellow = "#bfac05"  #:
    mudgreen = "#606602"  #:
    mulberry = "#920a4e"  #:
    murkygreen = "#6c7a0e"  #:
    mushroom = "#ba9e88"  #:
    mustard = "#ceb301"  #:
    mustardbrown = "#ac7e04"  #:
    mustardgreen = "#a8b504"  #:
    mustardyellow = "#d2bd0a"  #:
    mutedblue = "#3b719f"  #:
    mutedgreen = "#5fa052"  #:
    mutedpink = "#d1768f"  #:
    mutedpurple = "#805b87"  #:
    nastygreen = "#70b23f"  #:
    navy = "#01153e"  #:
    navyblue = "#001146"  #:
    navygreen = "#35530a"  #:
    neonblue = "#04d9ff"  #:
    neongreen = "#0cff0c"  #:
    neonpink = "#fe019a"  #:
    neonpurple = "#bc13fe"  #:
    neonred = "#ff073a"  #:
    neonyellow = "#cfff04"  #:
    niceblue = "#107ab0"  #:
    nightblue = "#040348"  #:
    ocean = "#017b92"  #:
    oceanblue = "#03719c"  #:
    oceangreen = "#3d9973"  #:
    ocher = "#bf9b0c"  #:
    ochre = "#bf9005"  #:
    ocre = "#c69c04"  #:
    offblue = "#5684ae"  #:
    offgreen = "#6ba353"  #:
    offwhite = "#ffffe4"  #:
    offyellow = "#f1f33f"  #:
    oldpink = "#c77986"  #:
    oldrose = "#c87f89"  #:
    olive = "#6e750e"  #:
    olivebrown = "#645403"  #:
    olivedrab = "#6f7632"  #:
    olivegreen = "#677a04"  #:
    oliveyellow = "#c2b709"  #:
    orange = "#f97306"  #:
    orangebrown = "#be6400"  #:
    orangeish = "#fd8d49"  #:
    orangepink = "#ff6f52"  #:
    orangered = "#fe420f"  #:
    orangeybrown = "#b16002"  #:
    orangeyellow = "#ffad01"  #:
    orangeyred = "#fa4224"  #:
    orangeyyellow = "#fdb915"  #:
    orangish = "#fc824a"  #:
    orangishbrown = "#b25f03"  #:
    orangishred = "#f43605"  #:
    orchid = "#c875c4"  #:
    pale = "#fff9d0"  #:
    paleaqua = "#b8ffeb"  #:
    paleblue = "#d0fefe"  #:
    palebrown = "#b1916e"  #:
    palecyan = "#b7fffa"  #:
    palegold = "#fdde6c"  #:
    palegreen = "#c7fdb5"  #:
    palegrey = "#fdfdfe"  #:
    palelavender = "#eecffe"  #:
    palelightgreen = "#b1fc99"  #:
    palelilac = "#e4cbff"  #:
    palelime = "#befd73"  #:
    palelimegreen = "#b1ff65"  #:
    palemagenta = "#d767ad"  #:
    palemauve = "#fed0fc"  #:
    paleolive = "#b9cc81"  #:
    paleolivegreen = "#b1d27b"  #:
    paleorange = "#ffa756"  #:
    palepeach = "#ffe5ad"  #:
    palepink = "#ffcfdc"  #:
    palepurple = "#b790d4"  #:
    palered = "#d9544d"  #:
    palerose = "#fdc1c5"  #:
    palesalmon = "#ffb19a"  #:
    paleskyblue = "#bdf6fe"  #:
    paleteal = "#82cbb2"  #:
    paleturquoise = "#a5fbd5"  #:
    paleviolet = "#ceaefa"  #:
    paleyellow = "#ffff84"  #:
    parchment = "#fefcaf"  #:
    pastelblue = "#a2bffe"  #:
    pastelgreen = "#b0ff9d"  #:
    pastelorange = "#ff964f"  #:
    pastelpink = "#ffbacd"  #:
    pastelpurple = "#caa0ff"  #:
    pastelred = "#db5856"  #:
    pastelyellow = "#fffe71"  #:
    pea = "#a4bf20"  #:
    peach = "#ffb07c"  #:
    peachypink = "#ff9a8a"  #:
    peacockblue = "#016795"  #:
    peagreen = "#8eab12"  #:
    pear = "#cbf85f"  #:
    peasoup = "#929901"  #:
    peasoupgreen = "#94a617"  #:
    periwinkle = "#8e82fe"  #:
    periwinkleblue = "#8f99fb"  #:
    perrywinkle = "#8f8ce7"  #:
    petrol = "#005f6a"  #:
    pigpink = "#e78ea5"  #:
    pine = "#2b5d34"  #:
    pinegreen = "#0a481e"  #:
    pink = "#ff81c0"  #:
    pinkish = "#d46a7e"  #:
    pinkishbrown = "#b17261"  #:
    pinkishgrey = "#c8aca9"  #:
    pinkishorange = "#ff724c"  #:
    pinkishpurple = "#d648d7"  #:
    pinkishred = "#f10c45"  #:
    pinkishtan = "#d99b82"  #:
    pinkpurple = "#ef1de7"  #:
    pinkred = "#f5054f"  #:
    pinky = "#fc86aa"  #:
    pinkypurple = "#c94cbe"  #:
    pinkyred = "#fc2647"  #:
    pissyellow = "#ddd618"  #:
    pistachio = "#c0fa8b"  #:
    plum = "#580f41"  #:
    plumpurple = "#4e0550"  #:
    poisongreen = "#40fd14"  #:
    poo = "#8f7303"  #:
    poobrown = "#885f01"  #:
    poop = "#7f5e00"  #:
    poopbrown = "#7a5901"  #:
    poopgreen = "#6f7c00"  #:
    powderblue = "#b1d1fc"  #:
    powderpink = "#ffb2d0"  #:
    primaryblue = "#0804f9"  #:
    prussianblue = "#004577"  #:
    puce = "#a57e52"  #:
    puke = "#a5a502"  #:
    pukebrown = "#947706"  #:
    pukegreen = "#9aae07"  #:
    pukeyellow = "#c2be0e"  #:
    pumpkin = "#e17701"  #:
    pumpkinorange = "#fb7d07"  #:
    pureblue = "#0203e2"  #:
    purple = "#7e1e9c"  #:
    purpleblue = "#5d21d0"  #:
    purplebrown = "#673a3f"  #:
    purplegrey = "#866f85"  #:
    purpleish = "#98568d"  #:
    purpleishblue = "#6140ef"  #:
    purpleishpink = "#df4ec8"  #:
    purplepink = "#d725de"  #:
    purplered = "#990147"  #:
    purpley = "#8756e4"  #:
    purpleyblue = "#5f34e7"  #:
    purpleygrey = "#947e94"  #:
    purpleypink = "#c83cb9"  #:
    purplish = "#94568c"  #:
    purplishblue = "#601ef9"  #:
    purplishbrown = "#6b4247"  #:
    purplishgrey = "#7a687f"  #:
    purplishpink = "#ce5dae"  #:
    purplishred = "#b0054b"  #:
    purply = "#983fb2"  #:
    purplyblue = "#661aee"  #:
    purplypink = "#f075e6"  #:
    putty = "#beae8a"  #:
    racinggreen = "#014600"  #:
    radioactivegreen = "#2cfa1f"  #:
    raspberry = "#b00149"  #:
    rawsienna = "#9a6200"  #:
    rawumber = "#a75e09"  #:
    reallylightblue = "#d4ffff"  #:
    red = "#e50000"  #:
    redbrown = "#8b2e16"  #:
    reddish = "#c44240"  #:
    reddishbrown = "#7f2b0a"  #:
    reddishgrey = "#997570"  #:
    reddishorange = "#f8481c"  #:
    reddishpink = "#fe2c54"  #:
    reddishpurple = "#910951"  #:
    reddybrown = "#6e1005"  #:
    redorange = "#fd3c06"  #:
    redpink = "#fa2a55"  #:
    redpurple = "#820747"  #:
    redviolet = "#9e0168"  #:
    redwine = "#8c0034"  #:
    richblue = "#021bf9"  #:
    richpurple = "#720058"  #:
    robineggblue = "#8af1fe"  #:
    robinsegg = "#6dedfd"  #:
    robinseggblue = "#98eff9"  #:
    rosa = "#fe86a4"  #:
    rose = "#cf6275"  #:
    rosepink = "#f7879a"  #:
    rosered = "#be013c"  #:
    rosypink = "#f6688e"  #:
    rouge = "#ab1239"  #:
    royal = "#0c1793"  #:
    royalblue = "#0504aa"  #:
    royalpurple = "#4b006e"  #:
    ruby = "#ca0147"  #:
    russet = "#a13905"  #:
    rust = "#a83c09"  #:
    rustbrown = "#8b3103"  #:
    rustorange = "#c45508"  #:
    rustred = "#aa2704"  #:
    rustyorange = "#cd5909"  #:
    rustyred = "#af2f0d"  #:
    saffron = "#feb209"  #:
    sage = "#87ae73"  #:
    sagegreen = "#88b378"  #:
    salmon = "#ff796c"  #:
    salmonpink = "#fe7b7c"  #:
    sand = "#e2ca76"  #:
    sandbrown = "#cba560"  #:
    sandstone = "#c9ae74"  #:
    sandy = "#f1da7a"  #:
    sandybrown = "#c4a661"  #:
    sandyellow = "#fce166"  #:
    sandyyellow = "#fdee73"  #:
    sapgreen = "#5c8b15"  #:
    sapphire = "#2138ab"  #:
    scarlet = "#be0119"  #:
    sea = "#3c9992"  #:
    seablue = "#047495"  #:
    seafoam = "#80f9ad"  #:
    seafoamblue = "#78d1b6"  #:
    seafoamgreen = "#7af9ab"  #:
    seagreen = "#53fca1"  #:
    seaweed = "#18d17b"  #:
    seaweedgreen = "#35ad6b"  #:
    sepia = "#985e2b"  #:
    shamrock = "#01b44c"  #:
    shamrockgreen = "#02c14d"  #:
    shit = "#7f5f00"  #:
    shitbrown = "#7b5804"  #:
    shitgreen = "#758000"  #:
    shockingpink = "#fe02a2"  #:
    sickgreen = "#9db92c"  #:
    sicklygreen = "#94b21c"  #:
    sicklyyellow = "#d0e429"  #:
    sienna = "#a9561e"  #:
    silver = "#c5c9c7"  #:
    sky = "#82cafc"  #:
    skyblue = "#75bbfd"  #:
    slate = "#516572"  #:
    slateblue = "#5b7c99"  #:
    slategreen = "#658d6d"  #:
    slategrey = "#59656d"  #:
    slimegreen = "#99cc04"  #:
    snot = "#acbb0d"  #:
    snotgreen = "#9dc100"  #:
    softblue = "#6488ea"  #:
    softgreen = "#6fc276"  #:
    softpink = "#fdb0c0"  #:
    softpurple = "#a66fb5"  #:
    spearmint = "#1ef876"  #:
    springgreen = "#a9f971"  #:
    spruce = "#0a5f38"  #:
    squash = "#f2ab15"  #:
    steel = "#738595"  #:
    steelblue = "#5a7d9a"  #:
    steelgrey = "#6f828a"  #:
    stone = "#ada587"  #:
    stormyblue = "#507b9c"  #:
    straw = "#fcf679"  #:
    strawberry = "#fb2943"  #:
    strongblue = "#0c06f7"  #:
    strongpink = "#ff0789"  #:
    sunflower = "#ffc512"  #:
    sunfloweryellow = "#ffda03"  #:
    sunnyyellow = "#fff917"  #:
    sunshineyellow = "#fffd37"  #:
    sunyellow = "#ffdf22"  #:
    swamp = "#698339"  #:
    swampgreen = "#748500"  #:
    tan = "#d1b26f"  #:
    tanbrown = "#ab7e4c"  #:
    tangerine = "#ff9408"  #:
    tangreen = "#a9be70"  #:
    taupe = "#b9a281"  #:
    tea = "#65ab7c"  #:
    teagreen = "#bdf8a3"  #:
    teal = "#029386"  #:
    tealblue = "#01889f"  #:
    tealgreen = "#25a36f"  #:
    tealish = "#24bca8"  #:
    tealishgreen = "#0cdc73"  #:
    terracota = "#cb6843"  #:
    terracotta = "#c9643b"  #:
    tiffanyblue = "#7bf2da"  #:
    tomato = "#ef4026"  #:
    tomatored = "#ec2d01"  #:
    topaz = "#13bbaf"  #:
    toupe = "#c7ac7d"  #:
    toxicgreen = "#61de2a"  #:
    treegreen = "#2a7e19"  #:
    trueblue = "#010fcc"  #:
    truegreen = "#089404"  #:
    turquoise = "#06c2ac"  #:
    turquoiseblue = "#06b1c4"  #:
    turquoisegreen = "#04f489"  #:
    turtlegreen = "#75b84f"  #:
    twilight = "#4e518b"  #:
    twilightblue = "#0a437a"  #:
    uglyblue = "#31668a"  #:
    uglybrown = "#7d7103"  #:
    uglygreen = "#7a9703"  #:
    uglypink = "#cd7584"  #:
    uglypurple = "#a442a0"  #:
    uglyyellow = "#d0c101"  #:
    ultramarine = "#2000b1"  #:
    ultramarineblue = "#1805db"  #:
    umber = "#b26400"  #:
    velvet = "#750851"  #:
    vermillion = "#f4320c"  #:
    verydarkblue = "#000133"  #:
    verydarkbrown = "#1d0200"  #:
    verydarkgreen = "#062e03"  #:
    verydarkpurple = "#2a0134"  #:
    verylightblue = "#d5ffff"  #:
    verylightbrown = "#d3b683"  #:
    verylightgreen = "#d1ffbd"  #:
    verylightpink = "#fff4f2"  #:
    verylightpurple = "#f6cefc"  #:
    verypaleblue = "#d6fffe"  #:
    verypalegreen = "#cffdbc"  #:
    vibrantblue = "#0339f8"  #:
    vibrantgreen = "#0add08"  #:
    vibrantpurple = "#ad03de"  #:
    violet = "#9a0eea"  #:
    violetblue = "#510ac9"  #:
    violetpink = "#fb5ffc"  #:
    violetred = "#a50055"  #:
    viridian = "#1e9167"  #:
    vividblue = "#152eff"  #:
    vividgreen = "#2fef10"  #:
    vividpurple = "#9900fa"  #:
    vomit = "#a2a415"  #:
    vomitgreen = "#89a203"  #:
    vomityellow = "#c7c10c"  #:
    warmblue = "#4b57db"  #:
    warmbrown = "#964e02"  #:
    warmgrey = "#978a84"  #:
    warmpink = "#fb5581"  #:
    warmpurple = "#952e8f"  #:
    washedoutgreen = "#bcf5a6"  #:
    waterblue = "#0e87cc"  #:
    watermelon = "#fd4659"  #:
    weirdgreen = "#3ae57f"  #:
    wheat = "#fbdd7e"  #:
    white = "#ffffff"  #:
    windowsblue = "#3778bf"  #:
    wine = "#80013f"  #:
    winered = "#7b0323"  #:
    wintergreen = "#20f986"  #:
    wisteria = "#a87dc2"  #:
    yellow = "#ffff14"  #:
    yellowbrown = "#b79400"  #:
    yellowgreen = "#bbf90f"  #:
    yellowish = "#faee66"  #:
    yellowishbrown = "#9b7a01"  #:
    yellowishgreen = "#b0dd16"  #:
    yellowishorange = "#ffab0f"  #:
    yellowishtan = "#fcfc81"  #:
    yellowochre = "#cb9d06"  #:
    yelloworange = "#fcb001"  #:
    yellowtan = "#ffe36e"  #:
    yellowybrown = "#ae8b0c"  #:
    yellowygreen = "#bff128"  #:
