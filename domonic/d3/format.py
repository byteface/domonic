"""
    domonic.d3.format
    ==================================

"""

from domonic.javascript import Math, Array, Number, String, Global, RegExp


def formatDecimal(x, ignore=None):
    x = Math.round(x)
    if Math.abs(x) >= 1e21:
        return x.toLocaleString("en").replace(r'/,/g', "")
    else:
        return Number(x).toString(10)


def formatDecimalParts(x, p = None):
    """[ Computes the decimal coefficient and exponent of the specified number x with
        significant digits p, where x is positive and p is in [1, 21] or undefined.
        For example, formatDecimalParts(1.23) returns ["123", 0].]

    Args:
        x ([type]): [description]
        p ([type]): [description]

    Returns:
        [type]: [description]
    """
    x = Number(x).toExponential() if p is None else Number(x).toExponential(p - 1)
    x2 = String(x).indexOf("e")
    i = x2
    if i < 0:
        return None  # NaN, ±Infinity

    coefficient = String(x).slice(0, i)

    # The string returned by toExponential either has the form \d\.\d+e[-+]\d+
    # (e.g., 1.2e+3) or the form \de[-+]\d+ (e.g., 1e+3).
    return [
        coefficient[0] + String(coefficient).slice(2) if len(coefficient) > 1 else coefficient,
        String(x).slice(i + 1)  # .lstrip('+')
    ]


prefixExponent = None


def formatPrefixAuto(x, p):

    print("formatPrefixAuto1",x,p)

    d = formatDecimalParts(x, p)
    if not d:
        return str(x)

    print("formatPrefixAuto22",x,p)

    coefficient = d[0]
    if d[1] == '' : d[1] = 0

    exponent = int(d[1])

    global prefixExponent
    prefixExponent = (Math.max(-8, Math.min(8, Math.floor(exponent / 3))) * 3)

    i = exponent - prefixExponent + 1
    n = len(coefficient)

    if i == n:
        return coefficient
    else:
        if i > n:
            return coefficient + "0".join(Array(i - n + 1))
        else:
            if i > 0:
                return String(coefficient).slice(0, i) + "." + String(coefficient).slice(i)
            else:
                return "0." + str("0".join(Array(1 - i))) + formatDecimalParts(x, Math.max(0, p + i - 1))[0]


def formatRounded(x, p):
    d = formatDecimalParts(x, p)
    if not d:
        return str(x)
    coefficient = d[0]

    if d[1] == '': d[1] = 0

    exponent = int(d[1])

    if exponent < 0:
        return "0." + Array(-exponent).join("0") + coefficient
    else:
        if len(coefficient) > (exponent + 1):
            return String(coefficient).slice(0, exponent + 1) + "." + String(coefficient).slice(exponent + 1)
        else:
            return coefficient + "0".join(Array(exponent - len(coefficient) + 2))

formatTypes = {
            "%": lambda x, p: Number(x * 100).toFixed(p),
            "b": lambda x, ignore = None: Number(Math.round(x)).toString(2),
            "c": lambda x, ignore = None: str(x),
            "d": formatDecimal,
            "e": lambda x, p: Number(x).toExponential(p),
            "f": lambda x, p: Number(x).toFixed(p),
            "g": lambda x, p: Number(x).toPrecision(p),
            "o": lambda x, ignore: Number(Math.round(x)).toString(8),
            "p": lambda x, p: formatRounded(x * 100, p),
            "r": formatRounded,
            "s": formatPrefixAuto,
            "X": lambda x, ignore = None: Number(Math.round(x)).toString(16).toUpperCase(),
            "x": lambda x, ignore = None: Number(Math.round(x)).toString(16)
        }


def exponent(x):
    x = formatDecimalParts(Math.abs(x))
    return x[1] if x else None


def formatGroup(grouping, thousands):
    def func(value, width):

        i = len(str(value))
        t = []
        j = 0
        g = grouping[0]
        length = 0

        while i > 0 and g > 0:
            if (length + g + 1) > width:
                g = Math.max(1, width - length)

            a = i-g
            i -= g
            t.append(String(value).substring(a, i + g))

            length += (g+1)
            if length > width:
                break

            j = (j + 1) % len(grouping)
            g = grouping[j]

        return thousands.join(Array(t).reverse())

    return func


def formatNumerals(numerals):
    def func(value):
        return value.replace(r'[0-9]g', lambda i: numerals[i])
    return func


re = r'^(?:(.)?([<>=^]))?([+\-( ])?([$#])?(0)?(\d+)?(,)?(\.\d+)?(~)?([a-z%])?$'


def formatSpecifier(specifier):
    match = RegExp(re).exec(str(specifier))
    if not match:
        raise Exception("invalid format: " + specifier)

    return FormatSpecifier({
                'fill': match[0], 'align': match[1],
                'sign': match[2], 'symbol': match[3],
                'zero': match[4], 'width': match[5],
                'comma': match[6], 'precision': match[7] and String(match[7]).slice(1),
                'trim': match[8], 'type': match[9]
                })


class FormatSpecifier():

    def __init__(self, specifier):
        self.fill = " " if specifier.get('fill', None) == None else str(specifier.get('fill'))
        self.align = ">" if specifier.get('align', None) == None else str(specifier.get('align'))
        self.sign = "-" if specifier.get('sign', None) == None else str(specifier.get('sign'))
        self.symbol = "" if specifier.get('symbol', None) == None else str(specifier.get('symbol'))
        self.zero = bool(specifier.get('zero', False))
        self.width = None if specifier.get('width', None) == None else specifier.get('width')
        self.comma = bool(specifier.get('comma', None))
        self.precision = None if specifier.get('precision', None) == None else specifier.get('precision')
        self.trim = bool(specifier.get('trim', None))
        self.type = "" if specifier.get('type', None) == None else str(specifier.get('type'))

    def toString(self):
        z = ("0" if self.zero else "")
        w = "" if self.width == None else Math.max(1, int(self.width) | 0)
        c = "," if self.comma else ""
        p = "" if self.precision == None else "." + str(Math.max(0, int(self.precision) | 0))
        t = "~" if self.trim else ""
        return self.fill + self.align + self.sign + self.symbol + str(z) + str(w) + str(c) + str(p) + str(t) + self.type

    def __str__(self):
        return self.toString()



# import formatTrim from "./formatTrim.js";

# // Trims insignificant zeros, e.g., replaces 1.2000k with 1.2k.
def formatTrim(s):
    #   out:
    #   for (var n = s.length, i = 1, i0 = -1, i1; i < n; ++i) {
    s = str(s)

    n = len(s)
    i = 1
    i0 = -1
    i1 = None

#   for (var n = s.length, i = 1, i0 = -1, i1; i < n; ++i) {
    for i in range(1, n):
        if s[i] == ".":
            i0 = i1 = i
        elif s[i] == "0":
            if i0 == 0:
                i0 = i
                i1 = i
        # else:
        if not s[i]:
            break  # out
        if (i0 > 0):
            i0 = 0

    return String(s).slice(0, i0) + String(s).slice(i1 + 1) if i0 > 0 else s


def identity(x):
    return x

map = Array.map
prefixes = ["y", "z", "a", "f", "p", "n", "µ", "m", "", "k", "M", "G", "T", "P", "E", "Z", "Y"]


class NewFormatProxy():
    def __init__(self, nf, specifier):
        self.func = nf
        self.specifier = specifier
    def __call__(self, *args, **kwargs):
        return self.func(*args, **kwargs)
    def __str__(self, *args, **kwargs):
        return str(self.specifier)


class formatLocale():

    def __init__(self, locale):

        self.group = locale.get('grouping', None) == None or identity if locale.get('thousands', None) == None else formatGroup([Global.Number(g) for g in locale['grouping']], str(locale.get('thousands')))
        self.currencyPrefix = "" if locale.get('currency', None) == None else str(locale.get('currency')[0])
        self.currencySuffix = "" if locale.get('currency') == None else str(locale.get('currency')[1])
        self.decimal = "." if locale.get('decimal', None) == None else str(locale.get('decimal'))
        self.numerals = identity if locale.get('numerals', None) == None else formatNumerals([str(n) for n in locale['numerals']])
        self.percent = "%" if locale.get('percent', None) == None else str(locale['percent'])
        self.minus = "−" if locale.get('minus', None) == None else str(locale['minus'])
        self.nan = "NaN" if locale.get('nan', None) == None else str(locale['nan'])

    def newFormat(self, specifier):
        specifier = formatSpecifier(specifier)

        fill = specifier.fill
        align = specifier.align
        sign = specifier.sign
        symbol = specifier.symbol
        zero = specifier.zero
        width = specifier.width
        comma = specifier.comma
        precision = specifier.precision
        trim = specifier.trim
        type = specifier.type

        if type == "n":
            comma = True
            type = "g"

        # The "" type, and any invalid type, is an alias for ".12~g".
        elif formatTypes.get(type, "") == "":
            if precision == None:
                precision = 12
                trim = True
                type = "g"

        # If zero fill is specified, padding goes after sign and before digits.
        if (zero or (fill == "0" and align == "=")):
            zero = True
            fill = "0"
            align = "="

        # Compute the prefix and suffix.
        # For SI-prefix, the suffix is lazily computed.
        prefix = ""
        if symbol == "$":
            prefix = self.currencyPrefix
        else:
            if (symbol == "#" and RegExp(r'[boxX]').test(type)):
                prefix = "0" + String(type).toLowerCase()
            else:
                prefix = ""

        suffix = ""
        if symbol == "$":
            suffix = self.currencySuffix
        else:
            suffix = self.percent if RegExp(r'[%p]').test(type) else ""

        # What format function should we use?
        # Is this an integer type?
        # Can this type generate exponential notation?
        formatType = formatTypes[type]
        maybeSuffix = RegExp(r'[defgprs%]').test(type)

        # Set the default precision if not specified,
        # or clamp the specified precision to the supported range.
        # For significant precision, it must be in [1, 21].
        # For fixed precision, it must be in [0, 20].
        if precision == None:
            precision = 6
            # precision = 0
        else:
            precision = Math.max(1, Math.min(21, precision)) if RegExp(r'[gprs]').test(type) else Math.max(0, Math.min(20, precision))


        def format(value):
            valuePrefix = prefix
            valueSuffix = suffix
            i = None
            n = None
            c = None

            if (type == "c"):
                valueSuffix = formatType(value) + valueSuffix
                value = ""
            else:
                value = value

                # Determine the sign. -0 is not less than 0, but 1 / -0 is!
                try:
                    valueNegative = value < 0
                except ZeroDivisionError:
                    valueNegative = 1 / value < 0
                except TypeError:
                    valueNegative = False

                # Perform the initial formatting.
                value = self.nan if Global.isNaN(value) else formatType(Math.abs(value), precision)

                # Trim insignificant zeros.
                if trim:
                    value = formatTrim(value)

                # If a negative value rounds to zero after formatting, and no explicit positive sign is requested, hide the sign.
                if (valueNegative and value == 0 and sign != "+"):
                    valueNegative = False
                
                # Compute the prefix and suffix.
                valuePrefix = ((sign if sign == "(" else self.minus) if valueNegative else "" if (sign == "-" or sign == "(") else sign) + valuePrefix

                global prefixExponent
                p1 = prefixes[int(8 + prefixExponent / 3)] if type == "s" else ""
                p2 = ")" if valueNegative and sign == "(" else ""
                valueSuffix = p1 + valueSuffix + p2

                # Break the formatted value into the integer “value” part that can be
                # grouped, and fractional or exponential “suffix” part that is not.
                if maybeSuffix:
                    i = -1
                    n = len(str(value))

                    while i < n:
                        c = String(value).charCodeAt(i)
                        if 48 > c or c > 57:
                            suff = self.decimal + String(value).slice(i + 1) if c == 46 else String(value).slice(i)
                            valueSuffix = suff + valueSuffix
                            value = String(value).slice(0, i)
                            break
                        i += 1

            # If the fill character is not "0", grouping is applied before padding.
            if comma and not zero:
                value = self.group(value, Global.Infinity)

            # Compute the padding.
            length = len(valuePrefix) + len(str(value)) + len(valueSuffix)

            nonlocal width
            if width == "" or width == None:
                width = 0
            width = int(width)
            padding = fill.join(Array(width - length + 1)) if length < int(width) else ""

            # If the fill character is "0", grouping is applied after padding.
            if comma and zero:
                value = self.group(padding + str(value), width - len(valueSuffix) if len(padding) else Global.Infinity)
                padding = ""

            # Reconstruct the final output based on the desired alignment.
            if align == "<":
                value = valuePrefix + value + valueSuffix + padding
            elif align == "=":
                value = valuePrefix + padding + str(value) + valueSuffix
            elif align == "^":
                length = len(padding) >> 1
                value = String(padding).slice(0, length) + valuePrefix + value + valueSuffix + String(padding).slice(length)
            else:
                value = padding + valuePrefix + str(value) + valueSuffix

            return self.numerals(value)

        return NewFormatProxy(format, specifier)  # = newFormat

    def formatPrefix(self, specifier, value):
        specifier = formatSpecifier(specifier)
        specifier.type = "f"
        f = self.newFormat(specifier)
        e = Math.max(-8, Math.min(8, Math.floor(int(exponent(value)) / 3))) * 3
        k = Math.pow(10, -e)
        prefix = prefixes[int(8 + e / 3)]
        return lambda value: f(k * value) + prefix

    format = newFormat
    formatPrefix = formatPrefix


locale = None
format = None
formatPrefix = None


def defaultLocale(definition):
    global locale
    global format
    global formatPrefix
    locale = formatLocale(definition)
    format = locale.format
    formatPrefix = locale.formatPrefix  # ['formatPrefix']
    return locale


defaultLocale({'thousands': ",", "grouping": [3], "currency": ["$", ""]})


# https://github.com/d3/d3-format/tree/main/locale - TODO - finish all 
def set_locale(code):
    """[sets the locale of the formatting engine]

    Args:
        code ([str]): [A language/country code i.e. en-GB, en-IN, en-US]

    Returns:
        [type]: [a new format obj]
    """
    loc = {
        "en-GB": {"decimal": ".", "thousands": ",", "grouping": [3], "currency": ["£", ""]},
        "en-IN": {"decimal": ".", "thousands": ",", "grouping": [3, 2, 2, 2, 2, 2, 2, 2, 2, 2], "currency": ["₹", ""]},
        "en-US": {"decimal": ".", "thousands": ",", "grouping": [3], "currency": ["$", ""]},
        "uk-UA": {"decimal": ",", "thousands": "\u00a0", "grouping": [3], "currency": ["", "\u00a0₴."]},
        "zh-CN": {"decimal": ".", "thousands": ",","grouping": [3], "currency": ["¥", ""]},
        "sv-SE": {"decimal": ",", "thousands": "\u00a0","grouping": [3], "currency": ["", " kr"]},
        "sl-SI": {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["", "\u00a0€"]},
        "ru-RU": {"decimal": ",", "thousands": "\u00a0", "grouping": [3], "currency": ["", "\u00a0руб."]},
        "pt-PT": {"decimal": ",","thousands": "\u00a0","grouping": [3],"currency": ["", "\u00a0€"]},
        "pt-BR": {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["R$", ""]},
        "pl-PL": {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["", "zł"]},
        "nl-NL": {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["€\u00a0", ""]},
        "mk-MK.": {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["", "\u00a0ден."]},
        "ko-KR": {"decimal": ".", "thousands": ",", "grouping": [3], "currency": ["₩", ""]},
        "ja-JP": {"decimal": ".", "thousands": ",", "grouping": [3], "currency": ["", "円"]},
        "it-IT": {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["€", ""]},
        "hu-HU.": {"decimal": ",", "thousands": "\u00a0", "grouping": [3], "currency": ["", "\u00a0Ft"]},
        "he-IL": {"decimal": ".", "thousands": ",", "grouping": [3], "currency": ["₪", ""]},
        "fr-FR": {"decimal": ",", "thousands": "\u00a0", "grouping": [3], "currency": ["", "\u00a0€"], "percent": "\u202f%"},
        "es-ES": {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["", "\u00a0€"]},
        "de-DE": {"decimal": ",", "thousands": ".", "grouping": [3], "currency": ["", "\u00a0€"]},
        "ar-YE": {"decimal": "\u066b", "thousands": "\u066c", "grouping": [3], "currency": ["", " \u0631\u002e\u0649\u002e"], "numerals" : ["\u0660", "\u0661", "\u0662", "\u0663", "\u0664", "\u0665", "\u0666", "\u0667", "\u0668", "\u0669"]}

    }[code]
    return formatLocale(loc)

# formatDefaultLocale, 
# format, 
# precisionFixed
# precisionPrefix
# precisionRound