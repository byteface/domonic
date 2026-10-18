"""
test_domonic
~~~~~~~~~~~~
unit tests for css
"""

import unittest

from domonic.dom import *
from domonic.html import *
from domonic.style import *
from domonic.style import _supports_condition


class TestCase(unittest.TestCase):
    def test_domonic_css(self):

        empty = div()
        self.assertIsInstance(empty.style, CSSStyleDeclaration)
        self.assertEqual(empty.style.getPropertyValue("display"), "")

        test = div("huh?", _style="alignContent: center;")
        assert test.style.alignContent == "center"
        assert test.style.getPropertyValue("align-content") == "center"
        test.style.alignContent = "flex-start"
        assert test.style.alignContent == "flex-start"
        assert str(test) == '<div style="align-content: flex-start;">huh?</div>'

        atag = a(
            "linky", _href="https://eventual.technology", _style="alignContent: center;"
        )
        assert atag.style.alignContent is not None

        sometag = div("asdfasdf", _id="test")
        sometag.style.alignContent = None
        assert sometag.style.alignContent == "none"
        assert div().style.getPropertyValue("display") == ""

        sometag.style.backgroundColor = "black"
        sometag.style.fontSize = "12px"

        # huh = document.createAttribute("test")
        # huh.value = "wtf"
        # sometag.setAttributeNode(huh)
        assert sometag.style.fontSize == "12px"
        sometag.style.display = "none"
        assert sometag.style.getPropertyValue("display") == "none"
        assert "font-size: 12px;" in str(sometag)
        sometag.style.cssFloat = "right"
        assert sometag.style.getPropertyValue("float") == "right"
        assert sometag.style.float == "right"

        sometag.style = "color: red; font-size: 16px;"
        self.assertIsInstance(sometag.style, CSSStyleDeclaration)
        self.assertEqual(sometag.style.color, "red")
        self.assertEqual(sometag.style.fontSize, "16px")
        self.assertIn('style="color: red; font-size: 16px;"', str(sometag))

        declaration = CSSStyleDeclaration()
        declaration.setProperty("background-color", "green")
        sometag.style = declaration
        self.assertIs(sometag.style, declaration)
        self.assertEqual(sometag.style.backgroundColor, "green")
        self.assertIn("background-color: green;", str(sometag))

        # print(sometag.style)
        # print(sometag.tagName)
        # s = Style()
        # print(sometag)

    def test_document_stylesheets_lazy_initializes(self):
        doc = Document(head(link(_rel="stylesheet", _href="/main.css")))

        self.assertIsInstance(doc.stylesheets, StyleSheetList)
        self.assertEqual(len(doc.stylesheets), 1)

    # create some failing tests

    # def test_css_style_declaration(self):
    # styleObj = document.styleSheets[0].cssRules[0].style
    # print(styleObj.cssText)

    # def test_css_style_rules(self):
    # myRules = document.styleSheets[0].cssRules # Returns a CSSRuleList
    # print(myRules)

    # myRules = document.styleSheets[0].cssRules
    # print(myRules[0]); # a CSSStyleRule representing the h1.

    # def test_css_styledpropertymap(self):
    # pass

    def test_paser(self):

        somecss = """
            :host {
                display: block;
            }

            div {
                color: red;
            }

            .class1 {
                color: blue;
            }

            .class1.class2 span {
                color: green;
            }

            .class1[attr1=\"value1\"] {
                color: yellow;
            }

            [attr1=\"value1\"] {
                color: yellow;
            }
        """

        from domonic.style import CSSParser

        ss = CSSStyleSheet()
        p = CSSParser.parseFromString(ss, somecss)

        for r in p:
            assert r.selectorText is not None
            assert r.style.cssText is not None
            # print(r.style)
            # print(r.parentRule)

        cssStyleSheet: CSSStyleSheet = CSSStyleSheet()
        cssStyleSheet.insertRule("div { background-color: green }")
        cssStyleSheet.insertRule("span { background-color: green }")
        cssStyleSheet.insertRule("div { background-color: green }")

        # print(cssStyleSheet.cssRules)
        # print(cssStyleSheet.cssRules.length)
        # print(cssStyleSheet.cssRules[0].selectorText)
        # print(cssStyleSheet.cssRules[0].style.cssText)
        assert cssStyleSheet.cssRules.length == 3
        assert cssStyleSheet.cssRules[0].selectorText == "div"
        assert cssStyleSheet.cssRules[0].style.cssText == "background-color: green;"

        # cssStyleSheet.insertRule('background-color: green');
        # DOMException('Invalid CSS rule.', DOMExceptionNameEnum.hierarchyRequestError)
        somecss = """
            :host {
                display: flex;
                overflow: hidden;
                width: 100%;
            }
            .container {
                flex-grow: 1;
                display: flex;
                flex-direction: column;
                overflow: hidden;
            }
            @media screen and (max-width: 36rem) {
                .container {
                    height: 0.5rem;
                    animation: keyframes2 2s linear infinite;
                }
            }
            @keyframes keyframes1 {
                from {
                    transform: rotate(0deg);
                }
                to {
                    transform: rotate(360deg);
                }
            }
            @keyframes keyframes2 {
                0% {
                    transform: rotate(0deg);
                }
                100% {
                    transform: rotate(360deg);
                }
            }
        """

        cssStyleSheet = CSSStyleSheet()
        cssRules = CSSParser.parseFromString(cssStyleSheet, somecss)

        assert len(cssRules) == 5

        # CSSStyleRule
        assert cssRules[0].parentRule == None
        assert cssRules[0].parentStyleSheet == cssStyleSheet
        assert cssRules[0].selectorText == ":host"
        # assert cssRules[0].cssText == ':host { display: flex; overflow: hidden; width: 100%; }'
        assert cssRules[0].style.parentRule == cssRules[0]
        # assert cssRules[0].style.length == 3
        # assert cssRules[0].style[0] == 'display'
        # assert cssRules[0].style[1] == 'overflow'
        # assert cssRules[0].style[2] == 'width'
        # assert cssRules[0].style['display'] == 'flex'
        # assert cssRules[0].style['overflow'] == 'hidden'
        # assert cssRules[0].style['width'] == '100%'
        assert (
            cssRules[0].style.cssText == "display: flex; overflow: hidden; width: 100%;"
        )

        # CSSStyleRule
        assert cssRules[1].parentRule == None
        assert cssRules[1].parentStyleSheet == cssStyleSheet
        assert cssRules[1].selectorText == ".container"
        # assert cssRules[1].cssText == '.container { flex-grow: 1; display: flex; flex-direction: column; overflow: hidden; }'
        # assert cssRules[1].style.length == 4
        assert cssRules[1].style.parentRule == cssRules[1]
        # assert cssRules[1].style[0] == 'flex-grow'
        # assert cssRules[1].style[1] == 'display'
        # assert cssRules[1].style[2] == 'flex-direction'
        # assert cssRules[1].style[3] == 'overflow'
        # assert cssRules[1].style['flexGrow'] == '1'
        # assert cssRules[1].style['display'] == 'flex'
        # assert cssRules[1].style['flexDirection'] == 'column'
        # assert cssRules[1].style['overflow'] == 'hidden'
        assert (
            cssRules[1].style.cssText
            == "flex-grow: 1; display: flex; flex-direction: column; overflow: hidden;"
        )

        # CSSMediaRule
        assert cssRules[2].parentRule == None
        assert cssRules[2].parentStyleSheet == cssStyleSheet
        assert cssRules[2].media.length == 1
        assert cssRules[2].media[0] == "screen and (max-width: 36rem)"
        assert cssRules[2].media.mediaText == "screen and (max-width: 36rem)"
        # assert cssRules[2].cssText == '@media screen and (max-width: 36rem) { .container { height: 0.5rem; animation: keyframes2 2s linear infinite; } }'
        # assert cssRules[2].cssRules.length == 1
        children1 = cssRules[2].cssRules
        assert children1[0].parentRule == cssRules[2]
        assert children1[0].parentStyleSheet == cssStyleSheet
        assert children1[0].selectorText == ".container"
        # assert children1[0].style.length == 2
        assert children1[0].style.parentRule == children1[0]
        # assert children1[0].style[0] == 'height'
        # assert children1[0].style[1] == 'animation'
        # assert children1[0].style['height'] == '0.5rem'
        # assert children1[0].style['animation'] == 'keyframes2 2s linear infinite'
        # assert children1[0].cssText == '.container { height: 0.5rem; animation: keyframes2 2s linear infinite; }'

        # CSSKeyframesRule
        assert cssRules[3].parentRule == None
        assert cssRules[3].parentStyleSheet == cssStyleSheet
        assert cssRules[3].name == "keyframes1"
        # assert cssRules[3].cssText == '@keyframes keyframes1 { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }'
        # assert cssRules[3].cssRules.length == 2
        children2 = cssRules[3].cssRules
        assert children2[0].parentRule == cssRules[3]
        assert children2[0].parentStyleSheet == cssStyleSheet
        assert children2[0].keyText == "from"
        # assert children2[0].style.length == 1
        assert children2[0].style.parentRule == children2[0]
        # assert children2[0].style[0] == 'transform'
        # assert children2[0].style['transform'] == 'rotate(0deg)'
        # assert children2[0].cssText == 'from { transform: rotate(0deg); }'
        assert children2[1].parentRule == cssRules[3]
        assert children2[1].parentStyleSheet == cssStyleSheet
        assert children2[1].keyText == "to"
        # assert children2[1].style.length == 1
        # assert children2[1].style[0] == 'transform'
        # assert children2[1].style['transform'] == 'rotate(360deg)'
        # assert children2[1].cssText == 'to { transform: rotate(360deg); }'

        # CSSKeyframesRule
        assert cssRules[4].parentRule == None
        assert cssRules[4].parentStyleSheet == cssStyleSheet
        assert cssRules[4].name == "keyframes2"
        # assert cssRules[4].cssText == '@keyframes keyframes2 { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }'
        # assert cssRules[4].cssRules.length == 2
        children3 = cssRules[4].cssRules
        assert children3[0].parentRule == cssRules[4]
        assert children3[0].parentStyleSheet == cssStyleSheet
        assert children3[0].keyText == "0%"
        # assert children3[0].style.length == 1
        assert children3[0].style.parentRule == children3[0]
        # assert children3[0].style[0] == 'transform'
        # assert children3[0].style['transform'] == 'rotate(0deg)'
        # assert children3[0].cssText == '0% { transform: rotate(0deg); }'
        assert children3[1].parentRule == cssRules[4]
        assert children3[1].parentStyleSheet == cssStyleSheet
        assert children3[1].keyText == "100%"
        # assert children3[1].style.length == 1
        # assert children3[1].style[0] == 'transform'
        # assert children3[1].style['transform'] == 'rotate(360deg)'
        # assert children3[1].cssText == '100% { transform: rotate(360deg); }'

    def test_new_props(self):

        s = Style()
        s.all = "border: 1px solid black;"
        assert s.all == "border: 1px solid black;"

        s.alignmentBaseline = "baseline"
        s.appearance = "none"
        s.backdropFilter = "blur(2px)"
        s.backgroundBlendMode = "normal"
        s.backgroundPositionX = "0"
        s.backgroundPositionY = "0"
        s.backgroundRepeatX = 0
        s.backgroundRepeatY = 0
        s.baselineShift = "0"
        s.blockSize = "0"
        s.borderBlockEnd = "0"
        # s.borderBlockEndColor = None
        # s.borderBlockEndStyle = None
        # s.borderBlockEndWidth = None
        # s.borderBlockStart = None
        # s.borderBlockStartColor = None
        # s.borderBlockStartStyle = None
        # s.borderBlockStartWidth = None
        # s.borderInlineEnd = None
        # s.borderInlineEndColor = None
        # s.borderInlineEndStyle = None
        # s.borderInlineEndWidth = None
        # s.borderInlineStart = None
        # s.borderInlineStartColor = None
        # s.borderInlineStartStyle = None
        # s.borderInlineStartWidth = None
        # s.breakAfter = 'auto'
        # s.breakBefore = 'auto'
        # s.breakInside = 'auto'
        # s.bufferedRendering = 'auto'
        # s.caretColor = None
        # s.clipPath = None
        # s.clipRule = None
        # s.colorInterpolation = None
        # s.colorInterpolationFilters = None
        # s.colorRendering = None
        # s.colorScheme = None
        # s.contain = None
        # s.containIntrinsicSize = None
        # s.contentVisibility = None
        # s.counterSet = None
        # s.cx = None
        # s.cy = None
        # s.dominantBaseline = None
        # s.d = None
        # s.fill = None
        # s.fillOpacity = None
        # s.fillRule = None
        # s.fontDisplay = None
        # s.floodColor = None
        # s.floodOpacity = None
        # s.fontFeatureSettings = None
        # s.fontKerning = None
        # s.fontOpticalSizing = None
        # s.fontVariantCaps = None
        # s.fontVariantEastAsian = None
        # s.fontVariantLigatures = None
        # s.fontVariantNumeric = None
        # s.fontVariationSettings = None
        # s.gap = None
        # s.grid = None
        # s.gridArea = None
        # s.gridAutoColumns = None
        # s.gridAutoFlow = None
        # s.gridAutoRows = None
        # s.gridColumn = None
        # s.gridColumnEnd = None
        # s.gridColumnGap = None
        # s.gridColumnStart = None
        # s.gridGap = None
        # s.gridRow = None
        # s.gridRowEnd = None
        # s.gridRowGap = None
        # s.gridRowStart = None
        # s.gridTemplate = None
        # s.gridTemplateAreas = None
        # s.gridTemplateColumns = None
        # s.gridTemplateRows = None
        # s.imageRendering = None
        # s.inherits = None
        # s.initialValue = None
        # s.inlineSize = None
        # s.justifyItems = None
        # s.justifySelf = None
        # s.lightingColor = None
        # s.lineBreak = None
        # s.marginBlockEnd = None
        # s.marginBlockStart = None
        # s.marginInlineEnd = None
        # s.marginInlineStart = None
        # s.marker = None
        # s.markerEnd = None
        # s.markerMid = None
        # s.markerStart = None
        # s.mask = None
        # s.maskType = None
        # s.maxBlockSize = None
        # s.maxInlineSize = None
        # s.maxZoom = None
        # s.minBlockSize = None
        # s.minInlineSize = None
        # s.minZoom = None
        # s.mixBlendMode = None
        # s.objectFit = None
        # s.objectPosition = None
        # s.offset = None
        # s.offsetDistance = None
        # s.offsetPath = None
        # s.offsetRotate = None
        # s.orientation = None
        # s.overflow = None
        # s.overflowAnchor = None
        # s.overflowWrap = None
        # s.overscrollBehavior = None
        # s.overscrollBehaviorBlock = None
        # s.overscrollBehaviorInline = None
        # s.overscrollBehaviorX = None
        # s.overscrollBehaviorY = None
        # s.paddingBlockEnd = None
        # s.paddingBlockStart = None
        # s.paddingInlineEnd = None
        # s.paddingInlineStart = None
        # s.page = None
        # s.pageOrientation = None
        # s.paintOrder = None
        # s.perspective = None
        # s.perspectiveOrigin = None
        # s.placeContent = None
        # s.placeItems = None
        # s.placeSelf = None
        # s.pointerEvents = None
        # s.r = None
        # s.rowGap = None
        # s.rubyPosition = None
        # s.rx = None
        # s.ry = None
        # s.scrollBehavior = None
        # s.scrollMargin = None
        # s.scrollMarginBlock = None
        # s.scrollMarginBlockEnd = None
        # s.scrollMarginBlockStart = None
        # s.scrollMarginBottom = None
        # s.scrollMarginInline = None
        # s.scrollMarginInlineEnd = None
        # s.scrollMarginInlineStart = None
        # s.scrollMarginLeft = None
        # s.scrollMarginRight = None
        # s.scrollMarginTop = None
        # s.scrollPadding = None
        # s.scrollPaddingBlock = None
        # s.scrollPaddingBlockEnd = None
        # s.scrollPaddingBlockStart = None
        # s.scrollPaddingBottom = None
        # s.scrollPaddingInline = None
        # s.scrollPaddingInlineEnd = None
        # s.scrollPaddingInlineStart = None
        # s.scrollPaddingLeft = None
        # s.scrollPaddingRight = None
        # s.scrollPaddingTop = None
        # s.scrollSnapAlign = None
        # s.scrollSnapStop = None
        # s.scrollSnapType = None
        # s.shapeImageThreshold = None
        # s.shapeMargin = None
        # s.shapeOutside = None
        # s.shapeRendering = None
        # s.size = None
        # s.speak = None
        # s.src = None
        # s.stopColor = None
        # s.stopOpacity = None
        # s.stroke = None
        # s.strokeDasharray = None
        # s.strokeDashoffset = None
        # s.strokeLinecap = None
        # s.strokeLinejoin = None
        # s.strokeMiterlimit = None
        # s.strokeOpacity = None
        # s.strokeWidth = None
        # s.syntax = None
        # s.textAnchor = None
        # s.textCombineUpright = None
        # s.textDecorationSkipInk = None
        # s.textOrientation = None
        # s.textRendering = None
        # s.textSizeAdjust = None
        # s.textUnderlinePosition = None
        # s.touchAction = None
        # s.transformBox = None
        # s.unicodeRange = None
        # s.userZoom = None
        # s.vectorEffect = None
        # s.willChange = None
        # s.writingMode = None
        # s.x = None
        # s.y = None

    def test_css_style_declaration_property_helpers(self):
        style = CSSStyleDeclaration()
        style.setProperty("width", "10px")
        self.assertEqual(style.getPropertyValue("width"), "10px")
        self.assertEqual(style.getPropertyCSSValue("width"), "10px")
        self.assertEqual(style.removeProperty("width"), "10px")
        self.assertEqual(style.getPropertyValue("width"), "")
        self.assertIsNone(style.getPropertyCSSValue("width"))

    def test_css_style_declaration_index_and_priority_helpers(self):
        style = CSSStyleDeclaration()
        style.setProperty("background-color", "red")
        style.setProperty("font-size", "12px", "important")
        style.setProperty("--brand-color", "oklch(62% 0.18 240)")

        self.assertEqual(style.length, 3)
        self.assertEqual(style.item(0), "background-color")
        self.assertEqual(style.item(1), "font-size")
        self.assertEqual(style.item(2), "--brand-color")
        self.assertEqual(style.item(3), "")
        self.assertEqual(style.getPropertyPriority("font-size"), "important")
        self.assertEqual(style.getPropertyValue("font-size"), "12px")
        self.assertEqual(style.getPropertyValue("--brand-color"), "oklch(62% 0.18 240)")
        self.assertIn("font-size: 12px !important;", style.cssText)

        style.setProperty("font-size", "14px")
        self.assertEqual(style.length, 3)
        self.assertEqual(style.getPropertyPriority("font-size"), "")
        self.assertEqual(style.getPropertyValue("font-size"), "14px")

    def test_css_style_declaration_replaces_css_text_cleanly(self):
        style = CSSStyleDeclaration()
        style.cssText = "color: red; background-image: url('/important.png'); width: 10px !important;"

        self.assertEqual(style.getPropertyValue("color"), "red")
        self.assertEqual(
            style.getPropertyValue("background-image"), "url('/important.png')"
        )
        self.assertEqual(style.getPropertyPriority("background-image"), "")
        self.assertEqual(style.getPropertyPriority("width"), "important")
        self.assertEqual(list(style), ["color", "background-image", "width"])
        self.assertIn("color", style)

        style.cssText = "margin: 0;"
        self.assertEqual(style.getPropertyValue("color"), "")
        self.assertEqual(style.getPropertyValue("width"), "")
        # the CSSOM normalises a unit-optional zero to "0px"
        self.assertEqual(style.getPropertyValue("margin"), "0px")
        self.assertNotIn("color", style)

        style["padding"] = "1rem"
        self.assertEqual(style.getPropertyValue("padding"), "1rem")

    def test_inline_style_replaces_existing_properties(self):
        node = div(_style="color:red;")
        node.style.color = "blue"
        node.style.color = "green"
        node.style.accentColor = "hotpink"
        node.style.containerType = "inline-size"

        self.assertEqual(
            node.getAttribute("style"),
            "color: green; accent-color: hotpink; container-type: inline-size;",
        )
        self.assertEqual(node.style.getPropertyValue("color"), "green")
        self.assertEqual(node.style.getPropertyValue("accent-color"), "hotpink")
        self.assertEqual(node.style.getPropertyValue("container-type"), "inline-size")

    def test_css_stylesheet_rule_mutation_helpers(self):
        sheet = CSSStyleSheet()
        first_index = sheet.insertRule("div { color: red; }")
        second_index = sheet.addRule(".card", "padding: 1rem;", 1)

        self.assertEqual(first_index, 0)
        self.assertEqual(second_index, 1)
        self.assertEqual(len(sheet.cssRules), 2)
        self.assertEqual(sheet.cssRules[0].selectorText, "div")
        self.assertEqual(sheet.cssRules[1].selectorText, ".card")

        sheet.deleteRule(0)
        self.assertEqual(len(sheet.cssRules), 1)
        self.assertEqual(sheet.cssRules[0].selectorText, ".card")

        sheet.removeRule(0)
        self.assertEqual(len(sheet.cssRules), 0)

        with self.assertRaises(DOMException):
            sheet.insertRule("main { display: block; }", -1)
        with self.assertRaises(DOMException):
            sheet.deleteRule(0)

    def test_cssom_list_helpers(self):
        media = MediaList(["screen"])
        media.appendMedium("print")
        media.deleteMedium("screen")
        media.deleteMedium("missing")

        self.assertEqual(media.length, 1)
        self.assertEqual(media.mediaText, "print")
        self.assertEqual(media.item(0), "print")
        self.assertIsNone(media.item(1))

        sheet = CSSStyleSheet()
        sheet.insertRule("main { display: block; }")
        rules = sheet.cssRules

        self.assertIs(rules.item(0), rules[0])
        self.assertIsNone(rules.item(1))

    def test_stylesheet_list_populates_from_document(self):
        page = html(
            head(
                link(_rel="stylesheet", _href="/assets/site.css"),
                style("div { color: red; }"),
            )
        )
        sheets = StyleSheetList()
        sheets._populate_stylesheets_from_document(page)

        self.assertEqual(sheets.length, 2)
        self.assertEqual(sheets.item(0).href, "/assets/site.css")
        self.assertEqual(sheets.item(1).cssRules[0].selectorText, "div")
        self.assertIsNone(sheets.item(2))

    def test_stylesheet_list_strips_cdata_wrapper(self):
        # a <style> element's content wrapped in a CDATA section is valid,
        # common XHTML practice (needed for strict XML well-formedness); the
        # markers survive as literal text in textContent since domonic's
        # HTML parser has no CDATA-section mode, so replaceSync must strip
        # them itself rather than handing them to the CSS parser as-is.
        page = html(head(style("<![CDATA[\ndiv { color: red; }\n]]>")))
        sheets = StyleSheetList()
        sheets._populate_stylesheets_from_document(page)

        self.assertEqual(sheets.item(0).cssRules[0].selectorText, "div")
        self.assertEqual(sheets.item(0).cssRules[0].style.getPropertyValue("color"), "red")

    def test_css_parser_strips_comments(self):
        sheet = CSSStyleSheet()
        rules = CSSParser.parseFromString(
            sheet, "/* heading */ div { color: red; } /* tail */"
        )
        self.assertEqual(len(rules), 1)
        self.assertEqual(rules[0].selectorText, "div")
        self.assertEqual(rules[0].style.getPropertyValue("color"), "red")

    def test_css_parser_modern_rules(self):
        css = """
            @layer reset, theme;
            @layer theme {
                @supports (display: grid) {
                    .card {
                        display: grid;
                    }
                }
            }
            @container sidebar (width > 40rem) {
                .item {
                    container-type: inline-size;
                }
            }
            @container style(--dense: true), main scroll-state(stuck: top) {
                .toolbar {
                    position: sticky;
                }
            }
            @scope (.article) to (.comments) {
                p {
                    color: blue;
                }
            }
            @import url("theme.css") layer(theme.components) supports(display: grid) screen and (min-width: 40rem);
            @supports-condition --fancy-layout {
                .fancy {
                    display: grid;
                }
            }
            @when supports(display: flex) {
                .when-rule {
                    display: flex;
                }
            }
            @else {
                .fallback {
                    display: block;
                }
            }
            @font-face {
                font-family: Test;
                src: url("fonts/a;b.woff2");
            }
            @property --brand-hue {
                syntax: "<number>";
                inherits: true;
                initial-value: 210;
            }
        """
        sheet = CSSStyleSheet()
        sheet.replaceSync(css)

        self.assertIsInstance(sheet.cssRules[0], CSSLayerStatementRule)
        self.assertEqual(sheet.cssRules[0].nameList, ["reset", "theme"])

        layer = sheet.cssRules[1]
        self.assertIsInstance(layer, CSSLayerBlockRule)
        self.assertEqual(layer.name, "theme")
        self.assertIsInstance(layer.cssRules[0], CSSSupportsRule)
        self.assertEqual(layer.cssRules[0].conditionText, "(display: grid)")
        self.assertEqual(
            layer.cssRules[0].cssRules[0].style.getPropertyValue("display"), "grid"
        )

        container = sheet.cssRules[2]
        self.assertIsInstance(container, CSSContainerRule)
        self.assertEqual(container.containerName, "sidebar")
        self.assertEqual(container.containerQuery, "(width > 40rem)")
        self.assertEqual(
            container.cssRules[0].style.getPropertyValue("container-type"),
            "inline-size",
        )

        multi_container = sheet.cssRules[3]
        self.assertIsInstance(multi_container, CSSContainerRule)
        self.assertEqual(multi_container.containerName, "")
        self.assertEqual(multi_container.containerQuery, "")
        self.assertEqual(
            multi_container.conditions,
            [
                {"name": "", "query": "style(--dense: true)"},
                {"name": "main", "query": "scroll-state(stuck: top)"},
            ],
        )
        self.assertEqual(
            multi_container.conditionText,
            "style(--dense: true), main scroll-state(stuck: top)",
        )

        scope = sheet.cssRules[4]
        self.assertIsInstance(scope, CSSScopeRule)
        self.assertEqual(scope.start, ".article")
        self.assertEqual(scope.end, ".comments")

        import_rule = sheet.cssRules[5]
        self.assertIsInstance(import_rule, CSSImportRule)
        self.assertEqual(import_rule.href, "theme.css")
        self.assertEqual(import_rule.layerName, "theme.components")
        self.assertEqual(import_rule.supportsText, "display: grid")
        self.assertEqual(import_rule.media.mediaText, "screen and (min-width: 40rem)")

        supports_condition = sheet.cssRules[6]
        self.assertIsInstance(supports_condition, CSSSupportsConditionRule)
        self.assertEqual(supports_condition.name, "--fancy-layout")
        self.assertEqual(supports_condition.cssRules[0].selectorText, ".fancy")

        when_rule = sheet.cssRules[7]
        self.assertIsInstance(when_rule, CSSWhenRule)
        self.assertEqual(when_rule.conditionText, "supports(display: flex)")
        self.assertEqual(
            when_rule.cssRules[0].style.getPropertyValue("display"), "flex"
        )

        else_rule = sheet.cssRules[8]
        self.assertIsInstance(else_rule, CSSElseRule)
        self.assertEqual(else_rule.conditionText, "")
        self.assertEqual(else_rule.cssRules[0].selectorText, ".fallback")

        font_face = sheet.cssRules[9]
        self.assertIsInstance(font_face, CSSFontFaceRule)
        self.assertEqual(
            font_face.style.getPropertyValue("src"), 'url("fonts/a;b.woff2")'
        )

        prop = sheet.cssRules[10]
        self.assertIsInstance(prop, CSSPropertyRule)
        self.assertEqual(prop.name, "--brand-hue")
        self.assertEqual(prop.style.getPropertyValue("initial-value"), "210")

    def test_css_parser_nested_style_rules(self):
        sheet = CSSStyleSheet()
        sheet.replaceSync("""
            .card {
                color: red;
                &:hover {
                    color: blue;
                }
                @media (width > 40rem) {
                    & {
                        display: grid;
                    }
                }
                background: white;
            }
            """)

        rule = sheet.cssRules[0]
        self.assertEqual(rule.selectorText, ".card")
        self.assertEqual(rule.style.getPropertyValue("color"), "red")
        self.assertEqual(rule.cssRules[0].selectorText, "&:hover")
        self.assertEqual(rule.cssRules[0].style.getPropertyValue("color"), "blue")
        self.assertIsInstance(rule.cssRules[1], CSSMediaRule)
        self.assertEqual(rule.cssRules[1].cssRules[0].selectorText, "&")
        self.assertEqual(
            rule.cssRules[1].cssRules[0].style.getPropertyValue("display"), "grid"
        )
        self.assertIsInstance(rule.cssRules[2], CSSNestedDeclarations)
        self.assertEqual(rule.cssRules[2].style.getPropertyValue("background"), "white")

    def test_css_stylesheet_replace_returns_promise(self):
        sheet = CSSStyleSheet()
        promise = sheet.replace("article { margin: 0; }")

        self.assertEqual(promise.state, "fulfilled")
        self.assertIs(promise.data, sheet)
        self.assertEqual(sheet.cssRules[0].selectorText, "article")

    def test_shorthand_expands_to_longhands(self):
        s = CSSStyleDeclaration()
        s.setProperty("border", "1px solid red")
        self.assertEqual(s.getPropertyValue("border-width"), "1px")
        self.assertEqual(s.getPropertyValue("border-style"), "solid")
        self.assertEqual(s.getPropertyValue("border-color"), "red")
        self.assertEqual(s.getPropertyValue("border-top-width"), "1px")
        self.assertEqual(s.cssText, "border: 1px solid red;")

        s2 = CSSStyleDeclaration()
        s2.setProperty("margin", "10px")
        self.assertEqual(s2.getPropertyValue("margin-top"), "10px")
        self.assertEqual(s2.getPropertyValue("margin-left"), "10px")
        self.assertEqual(s2.cssText, "margin: 10px;")

        s3 = CSSStyleDeclaration()
        s3.setProperty("font", "italic bold 16px/1.5 Arial, sans-serif")
        self.assertEqual(s3.getPropertyValue("font-size"), "16px")
        self.assertEqual(s3.getPropertyValue("font-weight"), "bold")
        self.assertEqual(s3.getPropertyValue("font-style"), "italic")
        self.assertEqual(s3.getPropertyValue("line-height"), "1.5")
        self.assertEqual(s3.getPropertyValue("font-family"), "Arial, sans-serif")

    def test_longhands_reconstruct_shorthand(self):
        s = CSSStyleDeclaration()
        for prop in ("padding-top", "padding-right", "padding-bottom", "padding-left"):
            s.setProperty(prop, "1rem")
        self.assertEqual(s.getPropertyValue("padding"), "1rem")
        self.assertEqual(s.cssText, "padding: 1rem;")

        # setting a longhand over a set shorthand collapses to the short form
        s2 = CSSStyleDeclaration()
        s2.setProperty("margin", "10px")
        s2.setProperty("margin-left", "5px")
        self.assertEqual(s2.getPropertyValue("margin"), "10px 10px 10px 5px")
        self.assertEqual(s2.cssText, "margin: 10px 10px 10px 5px;")

    def test_shorthand_via_css_text_and_inline_attr(self):
        node = div(_style="border: 2px dotted blue")
        self.assertEqual(node.style.getPropertyValue("border-style"), "dotted")
        self.assertEqual(node.style.getPropertyValue("border-top-width"), "2px")
        self.assertEqual(node.style.getPropertyValue("border-color"), "blue")

    def test_cssom_writes_serialise_consistently(self):
        # both the camelCase-attribute path and setProperty produce the same
        # normalised "prop: value; " form (like a browser)
        a = div()
        a.style.setProperty("color", "red")
        a.style.setProperty("font-size", "12px")

        b = div()
        b.style.color = "red"
        b.style.fontSize = "12px"

        self.assertEqual(a.style.cssText, "color: red; font-size: 12px;")
        self.assertEqual(b.style.cssText, a.style.cssText)
        self.assertEqual(b.getAttribute("style"), a.getAttribute("style"))

        # a directly-authored attribute stays verbatim until a CSSOM write
        n = div(_style="color:red;font-size:12px")
        self.assertEqual(n.getAttribute("style"), "color:red;font-size:12px")
        n.style.color = "blue"
        self.assertEqual(n.getAttribute("style"), "color: blue; font-size: 12px;")

    def test_shorthand_via_idl_expands_to_longhands(self):
        s = div().style
        s.margin = "1px 2px 3px 4px"
        self.assertEqual(s.marginTop, "1px")
        self.assertEqual(s.marginRight, "2px")
        self.assertEqual(s.marginBottom, "3px")
        self.assertEqual(s.marginLeft, "4px")
        self.assertEqual(s.getPropertyValue("margin-left"), "4px")

        s2 = div().style
        s2.border = "1px solid red"
        self.assertEqual(s2.getPropertyValue("border-top-width"), "1px")
        self.assertEqual(s2.getPropertyValue("border-style"), "solid")

    def test_shorthand_idl_getter_reconstructs_from_longhands(self):
        s = div().style
        s.marginTop = s.marginRight = s.marginBottom = s.marginLeft = "1px"
        self.assertEqual(s.margin, "1px")  # four equal longhands collapse

        b = div().style
        b.borderTopWidth = "1px"
        b.borderTopStyle = "solid"
        b.borderTopColor = "red"
        self.assertEqual(b.borderTop, "1px solid red")

    def test_unit_optional_zero_normalises_to_0px(self):
        s = div().style
        s.padding = "0"
        self.assertEqual(s.paddingTop, "0px")
        self.assertEqual(s.cssText, "padding: 0px;")
        s2 = div().style
        s2.marginTop = "0"
        self.assertEqual(s2.marginTop, "0px")
        s3 = div().style
        s3.cssText = "padding: 0"
        self.assertEqual(s3.getPropertyValue("padding-top"), "0px")
        # a percentage / unitless-number property is untouched
        s4 = div().style
        s4.lineHeight = "0"
        self.assertEqual(s4.getPropertyValue("line-height"), "0")

    def test_shorthand_counts_as_its_longhands(self):
        # a browser enumerates a set shorthand as its longhand sub-properties
        s = div().style
        s.setProperty("margin", "1px 2px 3px 4px")
        self.assertEqual(s.length, 4)
        self.assertEqual(
            [s.item(i) for i in range(s.length)],
            ["margin-top", "margin-right", "margin-bottom", "margin-left"],
        )
        self.assertEqual(list(s), list(s)[: s.length])
        # ...but serialisation still collapses back to the shorthand
        self.assertEqual(s.cssText, "margin: 1px 2px 3px 4px;")

        s.setProperty("color", "red")
        self.assertEqual(s.length, 5)

        b = div().style
        b.setProperty("border", "1px solid red")
        self.assertEqual(b.length, 12)
        self.assertEqual(b.item(0), "border-top-width")
        self.assertEqual(b.cssText, "border: 1px solid red;")

        # important flag propagates to the longhand view
        p = div().style
        p.setProperty("padding", "5px", "important")
        self.assertEqual(p.length, 4)
        self.assertEqual(p.getPropertyPriority("padding-top"), "important")

    def test_complete_longhand_set_collapses_on_serialisation(self):
        # a browser re-forms the shorthand when every longhand is present
        def css(pairs):
            s = div().style
            for name, value in pairs:
                s.setProperty(name, value)
            return s.cssText

        self.assertEqual(
            css([("border-top-width", "1px"), ("border-top-style", "solid"),
                 ("border-top-color", "red")]),
            "border-top: 1px solid red;",
        )
        self.assertEqual(
            css([("overflow-x", "hidden"), ("overflow-y", "hidden")]),
            "overflow: hidden;",
        )
        self.assertEqual(
            css([("overflow-x", "hidden"), ("overflow-y", "scroll")]),
            "overflow: hidden scroll;",
        )
        self.assertEqual(
            css([("flex-grow", "1"), ("flex-shrink", "1"), ("flex-basis", "0%")]),
            "flex: 1 1 0%;",
        )
        self.assertEqual(
            css([("row-gap", "1px"), ("column-gap", "2px")]),
            "gap: 1px 2px;",
        )
        # all four sides equal -> the one-word border shorthand
        self.assertEqual(
            css([(f"border-{s}-{c}", v) for c, v in
                 (("width", "1px"), ("style", "solid"), ("color", "red"))
                 for s in ("top", "right", "bottom", "left")]),
            "border: 1px solid red;",
        )
        # a mixed !important set must not collapse
        s = div().style
        s.setProperty("margin-top", "1px", "important")
        s.setProperty("margin-right", "2px")
        s.setProperty("margin-bottom", "3px")
        s.setProperty("margin-left", "4px")
        self.assertIn("margin-top: 1px !important;", s.cssText)
        self.assertNotIn("margin:", s.cssText)

    def test_flex_flow_single_keyword_expands_by_keyword_type(self):
        from domonic._cssom import expand_shorthand

        self.assertEqual(
            expand_shorthand("flex-flow", "row-reverse"),
            [("flex-direction", "row-reverse"), ("flex-wrap", "nowrap")],
        )
        self.assertEqual(
            expand_shorthand("flex-flow", "WRAP"),
            [("flex-direction", "row"), ("flex-wrap", "WRAP")],
        )
        self.assertEqual(
            expand_shorthand("flex-flow", "column wrap-reverse"),
            [("flex-direction", "column"), ("flex-wrap", "wrap-reverse")],
        )

        style = div().style
        style.setProperty("flex-flow", "row")
        self.assertEqual(style.getPropertyValue("flex-direction"), "row")
        self.assertEqual(style.getPropertyValue("flex-wrap"), "nowrap")

        # Uniform-value shorthands retain their existing broadcast behavior.
        self.assertEqual(
            expand_shorthand("gap", "10px"),
            [("row-gap", "10px"), ("column-gap", "10px")],
        )

    def test_remove_longhand_of_a_set_shorthand(self):
        s = div().style
        s.setProperty("margin", "1px 2px 3px 4px")
        s.removeProperty("margin-right")
        self.assertEqual(s.getPropertyValue("margin-right"), "")
        self.assertEqual(s.getPropertyValue("margin-top"), "1px")
        self.assertEqual(s.length, 3)
        self.assertNotIn("margin:", s.cssText)

    def test_background_shorthand_expands_to_longhands(self):
        s = div().style
        s.setProperty("background", "#fff url(x.svg) no-repeat")
        self.assertEqual(s.getPropertyValue("background-color"), "#fff")
        self.assertEqual(s.getPropertyValue("background-image"), "url(x.svg)")
        self.assertEqual(s.getPropertyValue("background-repeat"), "no-repeat")
        self.assertEqual(s.length, 8)
        # a comma-separated multi-layer value is kept verbatim (not split)
        s2 = div().style
        s2.setProperty("background", "red, url(a.png)")
        self.assertEqual(s2.getPropertyValue("background"), "red, url(a.png)")

    def test_csstext_setter_always_returns_serialised_form(self):
        s = div().style
        s.cssText = "color: red; margin-top: 5px"  # no trailing ;
        self.assertEqual(s.cssText, "color: red; margin-top: 5px;")

    def test_style_idl_is_backed_by_the_content_attribute(self):
        e = div()
        e.style.color = "red"
        e.setAttribute("style", "")  # clearing the attribute clears the block
        self.assertEqual(e.style.color, "")

        e.style.color = "red"
        e.removeAttribute("style")
        self.assertEqual(e.style.color, "")

        e.setAttribute("style", "color: green; padding: 1px")
        self.assertEqual(e.style.color, "green")
        self.assertEqual(e.style.padding, "1px")

    def test_get_attribute_names_and_case_insensitivity(self):
        e = div()
        e.setAttribute("Title", "T")
        e.setAttribute("data-X", "1")
        self.assertEqual(sorted(e.getAttributeNames()), ["data-x", "title"])
        self.assertEqual(e.getAttribute("title"), "T")   # lower-cased on HTML
        self.assertEqual(e.getAttribute("DATA-x"), "1")
        self.assertTrue(e.hasAttribute("TITLE"))

    def test_setting_a_property_to_empty_string_removes_the_declaration(self):
        node = div()
        node.style.color = "red"
        node.style.background = "blue"

        node.style.color = ""  # camelCase attribute path
        self.assertNotIn("color:", str(node))
        self.assertEqual(str(node), '<div style="background: blue;"></div>')

        node.style["background"] = ""  # subscript / setProperty path
        self.assertEqual(str(node), '<div style=""></div>')
        self.assertEqual(node.style.getPropertyValue("background"), "")

    def test_get_computed_style_cascade(self):
        page = document.createElement("html")
        page.innerHTML = (
            "<head><style>"
            ".box { color: red; padding: 8px; font-size: 13px }"
            "div.box { color: green }"
            "#hero { font-weight: bold }"
            "</style></head>"
            "<body><div id='hero' class='box' style='color: blue; margin: 4px'>"
            "<span>child</span></div></body>"
        )
        from domonic.window import window

        hero = page.querySelector("#hero")
        computed = window.getComputedStyle(hero)
        self.assertEqual(computed.getPropertyValue("color"), "rgb(0, 0, 255)")  # inline wins
        self.assertEqual(computed.getPropertyValue("padding"), "8px")  # .box
        self.assertEqual(computed.getPropertyValue("padding-top"), "8px")
        self.assertEqual(computed.getPropertyValue("font-weight"), "700")  # #hero
        self.assertEqual(computed.getPropertyValue("font-size"), "13px")  # .box
        self.assertEqual(computed.getPropertyValue("margin"), "4px")  # inline
        self.assertEqual(computed.getPropertyValue("display"), "inline")  # initial

        span = page.querySelector("span")
        span_computed = window.getComputedStyle(span)
        self.assertEqual(span_computed.getPropertyValue("color"), "rgb(0, 0, 255)")  # inherited
        self.assertEqual(span_computed.getPropertyValue("font-size"), "13px")  # inherited
        self.assertEqual(span_computed.getPropertyValue("margin"), "0px")  # not inherited

        with self.assertRaises(Exception):
            span_computed.setProperty("color", "orange")

        # the camelCase dot-access surface (``computed.color``) must return
        # the same as ``getPropertyValue`` -- ``ComputedStyleDeclaration``
        # skips ``Style.__init__``'s hundreds of ``self.__<prop>`` assignments
        # (it serves reads through the cascade instead), so those inherited
        # per-property getters used to raise ``AttributeError`` on the
        # never-set private attribute for *every* property, from any source.
        self.assertEqual(computed.color, "rgb(0, 0, 255)")
        self.assertEqual(computed.fontWeight, "700")
        self.assertEqual(computed.paddingTop, "8px")
        self.assertEqual(span_computed.color, "rgb(0, 0, 255)")

    def test_style_initial_values_resolve_lazily(self):
        # Style.__init__ no longer pre-assigns all ~380 property defaults
        # (it was ~430 us per construction); the camelCase getters fall back
        # to _STYLE_INITIAL_VALUES for an unset property. Behaviour must be
        # identical to the old eager assignment.
        from domonic.dom import document

        el = document.createElement("div")
        # a None-defaulted property renders as "none"
        self.assertEqual(el.style.color, "none")
        self.assertEqual(el.style.display, "none")
        # non-None initial values are preserved exactly
        self.assertEqual(el.style.fontSize, "medium")
        self.assertEqual(el.style.fontWeight, "normal")
        self.assertEqual(el.style.visibility, "visible")
        self.assertEqual(el.style.marginTop, "0px")
        self.assertEqual(el.style.borderRadius, "0px")
        self.assertEqual(el.style.animationIterationCount, 1)
        self.assertEqual(el.style.zIndex, "auto")
        # a set value still wins, and unrelated unset props still resolve
        el.style.color = "red"
        self.assertEqual(el.style.color, "red")
        self.assertEqual(el.style.fontSize, "medium")
        # a bare Style() (no CSSOM read surface) resolves initial values too
        from domonic.style import Style

        self.assertEqual(Style().fontSize, "medium")
        self.assertEqual(Style().opacity, "none")

    def test_selector_specificity_functional_pseudo_classes(self):
        from domonic.style import _selector_specificity as spec

        self.assertEqual(spec(":where(#a#b#c)"), (0, 0, 0))
        self.assertEqual(spec(":is(#a, .b)"), (1, 0, 0))
        self.assertEqual(spec("a:not(.b, #c)"), (1, 0, 1))
        self.assertEqual(spec("div:has(> img)"), (0, 0, 2))
        self.assertEqual(spec("li:nth-child(2n+1)"), (0, 1, 1))
        self.assertEqual(spec("ul li:nth-child(2n of .foo)"), (0, 2, 2))

    def test_where_pseudo_class_loses_the_cascade(self):
        from domonic.window import window

        page = document.createElement("html")
        page.innerHTML = (
            "<head><style>"
            ":where(#a#a#a) { color: blue }"
            ".card { color: green }"
            "</style></head>"
            "<body><div id='a' class='card'></div></body>"
        )
        div = page.querySelector("#a")
        self.assertEqual(
            window.getComputedStyle(div).getPropertyValue("color"), "rgb(0, 128, 0)"
        )

    def test_css_register_property_and_at_property_rule(self):
        from domonic.style import CSS, CSSStyleSheet
        from domonic import _cssom

        _cssom.REGISTERED_PROPERTIES.pop("--demo-gap", None)
        _cssom.REGISTERED_PROPERTIES.pop("--demo-ink", None)

        CSS.registerProperty(
            {
                "name": "--demo-ink",
                "syntax": "<color>",
                "inherits": True,
                "initialValue": "rebeccapurple",
            }
        )
        self.assertTrue(_cssom.inherits("--demo-ink"))
        self.assertEqual(_cssom.initial_value("--demo-ink"), "rebeccapurple")
        with self.assertRaises(Exception):
            CSS.registerProperty({"name": "--demo-ink", "inherits": False})
        with self.assertRaises(SyntaxError):
            CSS.registerProperty({"name": "nodashes", "inherits": True})

        sheet = CSSStyleSheet()
        sheet.replaceSync(
            "@property --demo-gap { syntax: '<length>'; inherits: false; "
            "initial-value: 8px; }"
        )
        self.assertFalse(_cssom.inherits("--demo-gap"))
        self.assertEqual(_cssom.initial_value("--demo-gap"), "8px")
        rule = sheet.cssRules[0]
        self.assertEqual(rule.name, "--demo-gap")
        self.assertFalse(rule.inherits)
        self.assertEqual(rule.initialValue, "8px")

    def test_constructable_stylesheet_options_and_metadata(self):
        from domonic.style import CSSStyleSheet

        sheet = CSSStyleSheet({"media": "print", "disabled": True})
        self.assertEqual(sheet.media.mediaText, "print")
        self.assertTrue(sheet.disabled)
        self.assertEqual(sheet.type, "text/css")

        plain = CSSStyleSheet()
        self.assertFalse(plain.disabled)  # spec default is enabled
        plain.media.mediaText = "screen, print"
        self.assertEqual(list(plain.media), ["screen", "print"])

    def test_computed_display_blockification(self):
        def display_of(style):
            e = document.createElement("span")
            e.setAttribute("style", style)
            document.createElement("div").appendChild(e)
            return ComputedStyleDeclaration(e).getPropertyValue("display")

        self.assertEqual(display_of("display: inline"), "inline")
        # out-of-flow (float / abs-pos) blockifies the display type
        self.assertEqual(display_of("display: inline; float: left"), "block")
        self.assertEqual(
            display_of("display: inline-block; position: absolute"), "block"
        )
        self.assertEqual(display_of("display: inline-flex; float: right"), "flex")
        self.assertEqual(display_of("display: none; float: left"), "none")
        # two-value display syntax -> the legacy single keyword
        self.assertEqual(display_of("display: block flow"), "block")
        self.assertEqual(display_of("display: inline flow-root"), "inline-block")

    def test_ua_stylesheet_defaults_non_content_tags_to_display_none(self):
        # a real browser's UA stylesheet gives these tags display:none
        # outright -- nothing about them is content -- so an element with no
        # author/inline `display` declared at all must report "none" here,
        # not the same "inline" any unrecognised tag falls back to.
        for tag in ("head", "title", "script", "style", "meta", "link", "noscript", "template"):
            with self.subTest(tag=tag):
                el = document.createElement(tag)
                self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("display"), "none")
        # an ordinary tag is unaffected
        self.assertEqual(
            ComputedStyleDeclaration(document.createElement("div")).getPropertyValue("display"), "inline"
        )

    def test_ua_display_none_default_loses_to_any_explicit_display(self):
        # the UA stylesheet is the weakest-priority origin -- an inline
        # style or an author rule must still win, exactly like overriding
        # any other UA default.
        el = document.createElement("script")
        el.setAttribute("style", "display: block")
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("display"), "block")

        el2 = document.createElement("script")
        sheet = CSSStyleSheet()
        sheet.replaceSync("script { display: block; }")
        # (the shared module-level document: put it back for the other tests)
        self.addCleanup(setattr, document, "adoptedStyleSheets", list(document.adoptedStyleSheets))
        document.adoptedStyleSheets = [sheet]
        document.appendChild(el2)
        self.addCleanup(el2.remove)
        self.assertEqual(ComputedStyleDeclaration(el2).getPropertyValue("display"), "block")

    def test_computed_percentage_lengths(self):
        outer = document.createElement("div")
        outer.setAttribute("style", "width: 400px")
        inner = document.createElement("div")
        inner.setAttribute(
            "style",
            "font-size: 20px; width: 50%; padding-left: 10%; "
            "margin-top: 25%; line-height: 150%",
        )
        outer.appendChild(inner)
        document.createElement("div").appendChild(outer)

        c = ComputedStyleDeclaration(inner)
        self.assertEqual(c.getPropertyValue("width"), "200px")
        self.assertEqual(c.getPropertyValue("padding-left"), "40px")
        # vertical margin % is still resolved against the containing block width
        self.assertEqual(c.getPropertyValue("margin-top"), "100px")
        self.assertEqual(c.getPropertyValue("line-height"), "30px")

        # no ancestor with an explicit size -> % is kept
        lone = document.createElement("div")
        lone.setAttribute("style", "width: 50%")
        document.createElement("div").appendChild(lone)
        self.assertEqual(
            ComputedStyleDeclaration(lone).getPropertyValue("width"), "50%"
        )

    def test_computed_transform_composes_to_matrix(self):
        def transform_of(value):
            e = document.createElement("div")
            e.setAttribute("style", f"font-size: 16px; transform: {value}")
            document.createElement("div").appendChild(e)
            return ComputedStyleDeclaration(e).getPropertyValue("transform")

        self.assertEqual(transform_of("none"), "none")
        self.assertEqual(
            transform_of("translate(10px, 20px)"), "matrix(1, 0, 0, 1, 10, 20)"
        )
        self.assertEqual(transform_of("scale(2)"), "matrix(2, 0, 0, 2, 0, 0)")
        self.assertEqual(transform_of("rotate(90deg)"), "matrix(0, 1, -1, 0, 0, 0)")
        # CSS list order: rotate is applied first, then the translate
        self.assertEqual(
            transform_of("translateX(10px) rotate(90deg)"),
            "matrix(0, 1, -1, 0, 10, 0)",
        )
        self.assertEqual(transform_of("translate(2em, 1rem)"), "matrix(1, 0, 0, 1, 32, 16)")
        # a percentage translate needs layout -- keep it verbatim
        self.assertEqual(transform_of("translate(50%, 0)"), "translate(50%, 0)")

    def test_computed_calc_length_evaluation(self):
        e = document.createElement("div")
        e.setAttribute(
            "style",
            "font-size: 16px; width: calc(100px + 2em); "
            "margin-top: calc(10px * 3); height: calc((4 + 1) * 8px); "
            "padding-left: calc(50% + 10px)",
        )
        document.createElement("div").appendChild(e)
        c = ComputedStyleDeclaration(e)
        self.assertEqual(c.getPropertyValue("width"), "132px")
        self.assertEqual(c.getPropertyValue("margin-top"), "30px")
        self.assertEqual(c.getPropertyValue("height"), "40px")
        # a percentage term needs layout -- calc() is kept verbatim
        self.assertEqual(c.getPropertyValue("padding-left"), "calc(50% + 10px)")

    def test_computed_css_wide_keywords(self):
        parent = document.createElement("div")
        parent.setAttribute("style", "color: rgb(1, 2, 3); font-size: 24px")
        child = document.createElement("span")
        child.setAttribute(
            "style", "color: inherit; font-size: initial; letter-spacing: unset"
        )
        parent.appendChild(child)
        document.createElement("div").appendChild(parent)

        c = ComputedStyleDeclaration(child)
        self.assertEqual(c.getPropertyValue("color"), "rgb(1, 2, 3)")   # inherit
        self.assertEqual(c.getPropertyValue("font-size"), "16px")        # initial
        # letter-spacing inherits, so unset == inherit == parent's "normal"
        self.assertEqual(c.getPropertyValue("letter-spacing"), "normal")

    def test_computed_colors_are_normalised_to_rgb(self):
        e = document.createElement("div")
        e.setAttribute(
            "style",
            "color: red; background-color: #0a0; "
            "outline-color: hsl(120, 100%, 50%); "
            "border-top-color: rgba(0, 0, 0, 0.25)",
        )
        document.createElement("div").appendChild(e)
        c = ComputedStyleDeclaration(e)
        self.assertEqual(c.getPropertyValue("color"), "rgb(255, 0, 0)")
        self.assertEqual(c.getPropertyValue("background-color"), "rgb(0, 170, 0)")
        self.assertEqual(c.getPropertyValue("outline-color"), "rgb(0, 255, 0)")
        self.assertEqual(c.getPropertyValue("border-top-color"), "rgba(0, 0, 0, 0.25)")
        # a regular declaration is NOT normalised
        self.assertEqual(e.style.getPropertyValue("color"), "red")

    def test_computed_currentcolor_resolves_to_color(self):
        e = document.createElement("div")
        e.setAttribute(
            "style",
            "color: rgb(10, 20, 30); border-top-color: currentColor; "
            "border-top-style: solid; border-top-width: 1px",
        )
        document.createElement("div").appendChild(e)
        c = ComputedStyleDeclaration(e)
        self.assertEqual(c.getPropertyValue("border-top-color"), "rgb(10, 20, 30)")
        self.assertEqual(c.getPropertyValue("border-top"), "1px solid rgb(10, 20, 30)")

    def test_currentcolor_substitution_treats_backslashes_literally(self):
        e = document.createElement("div")
        e.setAttribute(
            "style",
            r"color: g\re\45n; border-top-color: currentColor; "
            "border-top-style: solid; border-top-width: 1px",
        )
        document.createElement("div").appendChild(e)
        computed = ComputedStyleDeclaration(e)

        # CSS escape decoding is separate from this regression: whatever raw
        # color text reaches currentColor replacement must not be interpreted
        # as a Python regular-expression replacement template.
        self.assertEqual(computed.getPropertyValue("color"), r"g\re\45n")
        self.assertEqual(computed.getPropertyValue("border-top-color"), r"g\re\45n")

    def test_grid_column_row_shorthand_splits_on_slash_not_whitespace(self):
        # grid-column/grid-row is "<start> / <end>" -- unlike gap/overflow,
        # each <grid-line> can itself contain a space ("span 3"), so the
        # separator has to be the slash, not whitespace.
        e = document.createElement("div")
        e.setAttribute("style", "grid-column: 2 / span 3; grid-row: auto / 4")
        c = ComputedStyleDeclaration(e)
        self.assertEqual(c.getPropertyValue("grid-column-start"), "2")
        self.assertEqual(c.getPropertyValue("grid-column-end"), "span 3")
        self.assertEqual(c.getPropertyValue("grid-row-start"), "auto")
        self.assertEqual(c.getPropertyValue("grid-row-end"), "4")
        self.assertEqual(c.getPropertyValue("grid-column"), "2 / span 3")

    def test_grid_column_single_value_leaves_end_auto(self):
        e = document.createElement("div")
        e.setAttribute("style", "grid-column: 3")
        c = ComputedStyleDeclaration(e)
        self.assertEqual(c.getPropertyValue("grid-column-start"), "3")
        self.assertEqual(c.getPropertyValue("grid-column-end"), "auto")
        self.assertEqual(c.getPropertyValue("grid-column"), "3")

    def test_get_computed_style_for_pseudo_element(self):
        from domonic.dom import Document
        from domonic.style import CSSStyleSheet, ComputedStyleDeclaration

        doc = Document()
        sheet = CSSStyleSheet()
        sheet.replaceSync('p { color: black; } p::before { content: "* "; color: red; }')
        doc.adoptedStyleSheets = [sheet]

        p = doc.createElement("p")
        doc.createElement("div").appendChild(p)
        p._ownerDocument = doc

        self.assertEqual(ComputedStyleDeclaration(p).getPropertyValue("color"), "rgb(0, 0, 0)")
        before = ComputedStyleDeclaration(p, "::before")
        self.assertEqual(before.getPropertyValue("color"), "rgb(255, 0, 0)")
        self.assertEqual(before.getPropertyValue("content"), '"* "')
        # the element's own style is unaffected by ::before rules (normal is
        # the initial value, as a browser reports it)
        self.assertEqual(ComputedStyleDeclaration(p).getPropertyValue("content"), "normal")

    def test_pseudo_element_inherits_from_its_own_element_not_the_dom_parent(self):
        # per CSS Pseudo-Elements, a generated box's parent is the element
        # its pseudo is attached to -- an inherited property the element's
        # own rules set (e.g. Font Awesome's `.fas { font-family: ... }`)
        # must reach its ::before/::after, not be skipped in favour of
        # whatever the element's *DOM parent* happens to inherit.
        from domonic.dom import Document
        from domonic.style import CSSStyleSheet, ComputedStyleDeclaration

        doc = Document()
        sheet = CSSStyleSheet()
        sheet.replaceSync(
            'body { font-family: Arial; } '
            '.icon { font-family: "Icon Font"; } '
            '.icon::before { content: "x"; }'
        )
        doc.adoptedStyleSheets = [sheet]

        body = doc.createElement("body")
        icon = doc.createElement("i")
        icon.setAttribute("class", "icon")
        body.appendChild(icon)
        icon._ownerDocument = doc

        before = ComputedStyleDeclaration(icon, "::before")
        self.assertEqual(before.getPropertyValue("font-family"), '"Icon Font"')

    def test_adopted_stylesheets_feed_the_cascade(self):
        from domonic.dom import Document
        from domonic.style import CSSStyleSheet, ComputedStyleDeclaration

        doc = Document()
        sheet = CSSStyleSheet()
        sheet.replaceSync(".hl { color: rebeccapurple; }")
        doc.adoptedStyleSheets = [sheet]

        el = doc.createElement("span")
        el.setAttribute("class", "hl")
        doc.createElement("div").appendChild(el)
        el._ownerDocument = doc

        computed = ComputedStyleDeclaration(el)
        self.assertEqual(computed.getPropertyValue("color"), "rgb(102, 51, 153)")

    def test_cascade_layers_ordering(self):
        from domonic.window import window

        def color_of(css):
            page = document.createElement("html")
            page.innerHTML = f"<head><style>{css}</style></head><body><div id='x'></div></body>"
            return window.getComputedStyle(page.querySelector("#x")).getPropertyValue("color")

        # unlayered beats any layer
        self.assertEqual(
            color_of("@layer a { #x { color: red } } #x { color: blue }"),
            "rgb(0, 0, 255)",
        )
        # later layer wins for normal declarations
        self.assertEqual(
            color_of("@layer a { div { color: red } } @layer b { div { color: green } }"),
            "rgb(0, 128, 0)",
        )
        # a `@layer a, b;` statement pre-declares the order
        self.assertEqual(
            color_of(
                "@layer base, theme;"
                "@layer theme { div { color: green } }"
                "@layer base { div { color: red } }"
            ),
            "rgb(0, 128, 0)",
        )
        # for !important the earliest layer wins
        self.assertEqual(
            color_of(
                "@layer a { div { color: red !important } }"
                "@layer b { div { color: green !important } }"
            ),
            "rgb(255, 0, 0)",
        )

    def test_important_author_rule_beats_inline_style(self):
        from domonic.window import window

        page = document.createElement("html")
        page.innerHTML = (
            "<head><style>"
            "#a { color: red !important; padding-left: 1px }"
            "</style></head>"
            "<body>"
            "<div id='a' style='color: blue; padding-left: 9px'></div>"
            "</body>"
        )
        a = window.getComputedStyle(page.querySelector("#a"))
        # important author beats normal inline...
        self.assertEqual(a.getPropertyValue("color"), "rgb(255, 0, 0)")
        # ...but normal author loses to normal inline
        self.assertEqual(a.getPropertyValue("padding-left"), "9px")

        b = document.createElement("html")
        b.innerHTML = (
            "<head><style>#c { color: red !important }</style></head>"
            "<body><div id='c' style='color: blue !important'></div></body>"
        )
        # important inline still wins over important author
        self.assertEqual(
            window.getComputedStyle(b.querySelector("#c")).getPropertyValue("color"),
            "rgb(0, 0, 255)",
        )

    def test_get_computed_style_substitutes_var_references(self):
        from domonic.window import window

        page = document.createElement("html")
        page.innerHTML = (
            "<head><style>"
            "div { --brand: #0a0; --pad: 6px; color: var(--brand); "
            "padding: var(--missing, 4px); margin: var(--pad); "
            "border-color: var(--x, var(--brand)); }"
            "</style></head>"
            "<body><div id='a'><span id='b'></span></div></body>"
        )
        div = page.querySelector("#a")
        computed = window.getComputedStyle(div)
        self.assertEqual(computed.getPropertyValue("color"), "rgb(0, 170, 0)")
        self.assertEqual(computed.getPropertyValue("padding"), "4px")
        self.assertEqual(computed.getPropertyValue("margin"), "6px")
        self.assertEqual(computed.getPropertyValue("border-color"), "rgb(0, 170, 0)")
        # custom property itself is returned raw
        self.assertEqual(computed.getPropertyValue("--brand"), "#0a0")
        # inherited through the parent's already-substituted computed value
        child = window.getComputedStyle(page.querySelector("#b"))
        self.assertEqual(child.getPropertyValue("color"), "rgb(0, 170, 0)")

    def test_root_custom_properties_reach_descendants(self):
        from domonic.window import window

        page = document.createElement("html")
        page.innerHTML = (
            "<head><style>"
            ":root { --gap: 10px; --brand: #0a0; }"
            "#child { margin: var(--gap); color: var(--brand); }"
            "</style></head>"
            "<body><div id='child'></div></body>"
        )
        child = window.getComputedStyle(page.querySelector("#child"))
        self.assertEqual(child.getPropertyValue("--gap"), "10px")
        self.assertEqual(child.getPropertyValue("margin"), "10px")
        self.assertEqual(child.getPropertyValue("color"), "rgb(0, 170, 0)")

    def test_computed_style_resolves_font_relative_and_absolute_lengths(self):
        outer = document.createElement("div")
        outer.setAttribute("style", "font-size: 20px")
        inner = document.createElement("p")
        inner.setAttribute(
            "style",
            "font-size: 1.5em; margin: 1em; padding: 2rem 10px; "
            "line-height: 2; border-top-style: solid; border-top-width: 0.25rem; width: 50%",
        )
        outer.appendChild(inner)
        document.createElement("div").appendChild(outer)

        c = ComputedStyleDeclaration(inner)
        self.assertEqual(c.getPropertyValue("font-size"), "30px")   # 1.5 * 20
        self.assertEqual(c.getPropertyValue("margin"), "30px")      # 1em of own 30
        self.assertEqual(c.getPropertyValue("padding"), "32px 10px")  # 2rem == 32
        self.assertEqual(c.getPropertyValue("line-height"), "60px")   # 2 * 30
        self.assertEqual(c.getPropertyValue("border-top-width"), "4px")
        # % needs layout -- left untouched
        self.assertEqual(c.getPropertyValue("width"), "50%")

    def test_computed_style_resolves_ch_and_ex_using_spec_fallback(self):
        # domonic has no real glyph metrics, so ch/ex fall back to the value
        # the CSS spec itself mandates for that case: 0.5em for both units.
        el = document.createElement("div")
        el.setAttribute("style", "font-size: 20px; text-indent: 5ch")
        document.createElement("div").appendChild(el)

        c = ComputedStyleDeclaration(el)
        self.assertEqual(c.getPropertyValue("text-indent"), "50px")   # 5 * 0.5 * 20

        el.setAttribute("style", "font-size: 20px; text-indent: 3ex")
        self.assertEqual(
            ComputedStyleDeclaration(el).getPropertyValue("text-indent"), "30px"
        )  # 3 * 0.5 * 20

        el.setAttribute("style", "font-size: 20px; width: calc(2ch + 10px)")
        self.assertEqual(
            ComputedStyleDeclaration(el).getPropertyValue("width"), "30px"
        )  # 2 * 0.5 * 20 + 10

    def test_inherited_properties_reach_descendants_from_the_html_root(self):
        # domonic's <html> tag doubles as the Document (the last html()
        # created becomes the active document), so it reports
        # nodeType == DOCUMENT_NODE like any other Document -- but it is
        # still the real <html> element in the tree. Anything set directly
        # on it (an attribute selector, a class, or a bare tag rule) must
        # still inherit down to <body> and beyond, the same as it would for
        # any other ancestor.
        from domonic import domonic
        from domonic.window import window

        attr_page = domonic.parseString(
            '<html dir="rtl"><head><style>[dir=rtl]{direction:rtl}</style></head>'
            "<body><span>x</span></body></html>"
        )
        span = attr_page.querySelector("span")
        self.assertEqual(
            window.getComputedStyle(span).getPropertyValue("direction"), "rtl"
        )

        class_page = domonic.parseString(
            '<html class="rtl"><head><style>.rtl{direction:rtl}</style></head>'
            "<body><span>x</span></body></html>"
        )
        span = class_page.querySelector("span")
        self.assertEqual(
            window.getComputedStyle(span).getPropertyValue("direction"), "rtl"
        )

        tag_page = domonic.parseString(
            "<html><head><style>html{direction:rtl}</style></head>"
            "<body><span>x</span></body></html>"
        )
        span = tag_page.querySelector("span")
        self.assertEqual(
            window.getComputedStyle(span).getPropertyValue("direction"), "rtl"
        )

        font_page = domonic.parseString(
            '<html style="font-size: 40px"><body><span style="font-size: 2em">x</span></body></html>'
        )
        span = font_page.querySelector("span")
        self.assertEqual(
            window.getComputedStyle(span).getPropertyValue("font-size"), "80px"
        )

    def test_custom_properties_inherit_from_any_ancestor(self):
        from domonic.window import window

        page = document.createElement("html")
        page.innerHTML = (
            "<head><style>#leaf { color: var(--c); padding: var(--p); }</style>"
            "</head><body><div style='--c: teal'>"
            "<section style='--p: 3px'><b id='leaf'>x</b></section></div></body>"
        )
        leaf = window.getComputedStyle(page.querySelector("#leaf"))
        self.assertEqual(leaf.getPropertyValue("color"), "rgb(0, 128, 128)")
        self.assertEqual(leaf.getPropertyValue("padding"), "3px")

    def test_structural_pseudo_class_selectors(self):
        page = document.createElement("div")
        page.innerHTML = "<p>a</p><p></p><span>c</span>"
        self.assertEqual(page.querySelector("p:first-child").textContent, "a")
        self.assertEqual(len(page.querySelectorAll("p")), 2)
        self.assertIs(
            page.querySelector("p:empty"), page.querySelectorAll("p")[1]
        )
        self.assertTrue(page.querySelector("span").matches(":last-child"))
        self.assertTrue(page.querySelector("span").matches("span:only-of-type"))
        self.assertFalse(page.querySelector("p").matches(":only-child"))

    def test_link_and_visited_pseudo_class_selectors(self):
        page = document.createElement("div")
        page.innerHTML = (
            "<a id='link' href='/story'>story</a>"
            "<a id='empty' href=''>empty</a>"
            "<a id='missing'>missing</a>"
            "<area id='area' href='/map'>"
            "<link id='stylesheet' href='/site.css'>"
        )

        # https://html.spec.whatwg.org/#selector-link: every a, area and link
        # element with an href attribute, whatever its value (even empty)
        self.assertEqual(
            [element.getAttribute("id") for element in page.querySelectorAll(":link")],
            ["link", "empty", "area", "stylesheet"],
        )
        self.assertTrue(page.querySelector("#link").matches("a:link"))
        self.assertTrue(page.querySelector("#empty").matches(":link"))
        self.assertFalse(page.querySelector("#missing").matches(":link"))
        self.assertTrue(page.querySelector("#stylesheet").matches(":link"))
        self.assertEqual(list(page.querySelectorAll(":visited")), [])

    def test_link_pseudo_class_participates_in_author_cascade(self):
        doc = Document()
        hyperlink = doc.createElement("a")
        hyperlink.setAttribute("href", "/story")
        plain_anchor = doc.createElement("a")
        doc.appendChild(hyperlink)
        doc.appendChild(plain_anchor)

        sheet = CSSStyleSheet()
        sheet.replaceSync("a { color: blue } a:link { color: black } a:visited { color: red }")
        doc.adoptedStyleSheets = [sheet]

        self.assertEqual(
            ComputedStyleDeclaration(hyperlink).getPropertyValue("color"),
            "rgb(0, 0, 0)",
        )
        self.assertEqual(
            ComputedStyleDeclaration(plain_anchor).getPropertyValue("color"),
            "rgb(0, 0, 255)",
        )

    def test_dir_pseudo_class_participates_in_author_cascade(self):
        page = document.createElement("html")
        page.innerHTML = (
            "<head><style>"
            ":dir(ltr) { color: blue }"
            ":dir(rtl) { color: lime }"
            ":dir(foopy) { color: red }"
            "section:dir(rtl) > span:dir(rtl) { background-color: black }"
            "</style></head>"
            "<body><div id='ltr'></div>"
            "<section dir='rtl'><span id='rtl' dir='auto'></span></section>"
            "</body>"
        )
        from domonic.window import window

        ltr = window.getComputedStyle(page.querySelector("#ltr"))
        rtl = window.getComputedStyle(page.querySelector("#rtl"))
        self.assertEqual(ltr.getPropertyValue("color"), "rgb(0, 0, 255)")
        self.assertEqual(rtl.getPropertyValue("color"), "rgb(0, 255, 0)")
        self.assertEqual(rtl.getPropertyValue("background-color"), "rgb(0, 0, 0)")

    def test_element_matches_combinators(self):
        page = document.createElement("div")
        page.innerHTML = (
            "<div class='a'><section><p id='x'>hi</p></section>"
            "<p class='b'>y</p></div>"
        )
        x = page.querySelector("#x")
        y = page.querySelector(".b")
        self.assertTrue(x.matches("div.a p"))
        self.assertTrue(x.matches("section > p"))
        self.assertFalse(x.matches("div.a > p"))
        self.assertTrue(x.matches("div.a > section > p"))
        self.assertTrue(y.matches("section + p"))
        self.assertFalse(y.matches("p + p"))

    def test_css_typed_om_values_and_style_maps(self):
        from domonic.style import CSS, CSSUnitValue, CSSKeywordValue, CSSStyleValue

        self.assertEqual(str(CSS.px(10)), "10px")
        self.assertEqual(CSS.px(10).unit, "px")
        self.assertEqual(CSS.number(3).unit, "number")
        self.assertEqual(CSS.percent(50).unit, "percent")
        self.assertEqual(CSS.px(10) + CSS.px(5), CSSUnitValue(15, "px"))
        self.assertEqual(str(CSS.px(96).to("in")), "1in")
        self.assertEqual(str(CSS.deg(360).to("turn")), "1turn")
        with self.assertRaises(TypeError):
            CSS.px(1) + CSS.em(1)

        self.assertIsInstance(CSSStyleValue.parse("width", "10px"), CSSUnitValue)
        self.assertIsInstance(
            CSSStyleValue.parse("display", "grid"), CSSKeywordValue
        )

        el = document.createElement("div")
        el.setAttribute("style", "width: 10px; color: red")
        attr_map = el.attributeStyleMap
        self.assertEqual(attr_map.get("width"), CSSUnitValue(10, "px"))
        self.assertEqual(str(attr_map.get("color")), "red")
        attr_map.set("height", CSS.px(20))
        self.assertEqual(el.style.getPropertyValue("height"), "20px")

        computed_map = el.computedStyleMap()
        self.assertEqual(computed_map.get("width"), CSSUnitValue(10, "px"))
        with self.assertRaises(Exception):
            computed_map.set("width", CSS.px(1))

    def test_css_namespace_utilities(self):
        self.assertEqual(CSS.escape("123 item"), "\\31 23\\ item")
        self.assertEqual(CSS.escape("-"), "\\-")
        self.assertTrue(CSS.supports("display", "grid"))
        self.assertTrue(CSS.supports("container-type", "inline-size"))
        self.assertTrue(
            CSS.supports("(display: grid) and (container-type: inline-size)")
        )
        self.assertTrue(CSS.supports("at-rule(@container)"))
        self.assertFalse(CSS.supports(" display", "grid"))
        self.assertFalse(CSS.supports("display", "grid !important"))

    # -- computed-style cache invalidation ---------------------------------
    #
    # ComputedStyleDeclaration caches its resolved cascade on the element
    # (see domonic-css-performance notes) instead of redoing it on every
    # getComputedStyle() call. Each of these mutates one specific input and
    # checks the *next* read reflects it -- a narrower invalidation gap would
    # make one of these silently see a stale value.

    def test_repeated_computed_style_reads_agree(self):
        document = Document()
        from domonic.window import window

        el = document.createElement("div")
        el.setAttribute("style", "color: red")
        document.appendChild(el)
        first = window.getComputedStyle(el).getPropertyValue("color")
        second = window.getComputedStyle(el).getPropertyValue("color")
        self.assertEqual(first, "rgb(255, 0, 0)")
        self.assertEqual(second, first)

    def test_css_property_name_normalization_is_cached(self):
        from domonic.style import _css_property_name
        from domonic.utils import Utils

        _css_property_name.cache_clear()
        Utils.case_kebab.cache_clear()
        for _ in range(5):
            self.assertEqual(_css_property_name("backgroundColor"), "background-color")
        property_info = _css_property_name.cache_info()
        kebab_info = Utils.case_kebab.cache_info()
        self.assertEqual(property_info.misses, 1)
        self.assertGreaterEqual(property_info.hits, 4)
        self.assertEqual(kebab_info.misses, 1)

    def test_author_rule_selector_parsing_is_cached_across_elements(self):
        from domonic.bs4 import _parse_selector_chain, _split_simple_selector_chain

        _split_simple_selector_chain.cache_clear()
        _parse_selector_chain.cache_clear()
        Element._parse_simple_selector.cache_clear()

        document = Document()
        sheet = CSSStyleSheet()
        sheet.replaceSync(".item > span.label { color: green }")
        document.adoptedStyleSheets = [sheet]

        for _ in range(5):
            parent = document.createElement("div")
            parent.setAttribute("class", "item")
            child = document.createElement("span")
            child.setAttribute("class", "label")
            parent.appendChild(child)
            document.appendChild(parent)
            self.assertEqual(ComputedStyleDeclaration(child).getPropertyValue("color"), "rgb(0, 128, 0)")

        # the chain matcher parses through _parse_selector_chain's cache, so
        # the split under it runs once
        chain_info = _parse_selector_chain.cache_info()
        split_info = _split_simple_selector_chain.cache_info()
        simple_info = Element._parse_simple_selector.cache_info()
        self.assertLessEqual(chain_info.misses, 2)
        self.assertGreaterEqual(chain_info.hits, 4)
        self.assertLessEqual(split_info.misses, 2)
        self.assertLessEqual(simple_info.misses, 4)
        self.assertGreaterEqual(simple_info.hits, 4)

    def test_inline_style_change_invalidates_cached_style(self):
        document = Document()
        from domonic.window import window

        el = document.createElement("div")
        el.setAttribute("style", "color: red")
        document.appendChild(el)
        window.getComputedStyle(el).getPropertyValue("color")
        el.setAttribute("style", "color: blue")
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("color"), "rgb(0, 0, 255)")

    def test_class_change_invalidates_cached_style(self):
        document = Document()
        from domonic.window import window

        el = document.createElement("div")
        document.appendChild(el)
        sheet = CSSStyleSheet()
        sheet.replaceSync(".hot { color: green }")
        document.adoptedStyleSheets = [sheet]
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("color"), "rgb(0, 0, 0)")
        el.setAttribute("class", "hot")
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("color"), "rgb(0, 128, 0)")

    def test_stylesheet_rule_mutation_invalidates_cached_style(self):
        document = Document()
        from domonic.window import window

        el = document.createElement("div")
        el.setAttribute("class", "hot")
        document.appendChild(el)
        sheet = CSSStyleSheet()
        sheet.replaceSync(".hot { color: green }")
        document.adoptedStyleSheets = [sheet]
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("color"), "rgb(0, 128, 0)")
        sheet.insertRule(".hot { color: purple }", 1)
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("color"), "rgb(128, 0, 128)")
        sheet.deleteRule(1)
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("color"), "rgb(0, 128, 0)")

    def test_reassigning_adopted_stylesheets_invalidates_cached_style(self):
        document = Document()
        from domonic.window import window

        el = document.createElement("div")
        el.setAttribute("class", "hot")
        document.appendChild(el)
        sheet_a = CSSStyleSheet()
        sheet_a.replaceSync(".hot { color: green }")
        document.adoptedStyleSheets = [sheet_a]
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("color"), "rgb(0, 128, 0)")
        sheet_b = CSSStyleSheet()
        sheet_b.replaceSync(".hot { color: orange }")
        document.adoptedStyleSheets = [sheet_b]
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("color"), "rgb(255, 165, 0)")

    def test_reparenting_invalidates_cached_inherited_value(self):
        document = Document()
        from domonic.window import window

        parent_a = document.createElement("div")
        parent_a.setAttribute("style", "color: red")
        parent_b = document.createElement("div")
        parent_b.setAttribute("style", "color: teal")
        child = document.createElement("span")
        parent_a.appendChild(child)
        document.appendChild(parent_a)
        document.appendChild(parent_b)
        self.assertEqual(window.getComputedStyle(child).getPropertyValue("color"), "rgb(255, 0, 0)")
        parent_a.removeChild(child)
        parent_b.appendChild(child)
        self.assertEqual(window.getComputedStyle(child).getPropertyValue("color"), "rgb(0, 128, 128)")

    def test_clone_node_after_computing_style_is_unaffected(self):
        document = Document()
        from domonic.window import window

        root = document.createElement("div")
        root.setAttribute("style", "color: red")
        document.appendChild(root)
        window.getComputedStyle(root).getPropertyValue("color")  # populate the cache
        clone = root.cloneNode(True)
        self.assertEqual(window.getComputedStyle(clone).getPropertyValue("color"), "rgb(255, 0, 0)")
        self.assertIsNot(clone.__dict__.get("_computed_style_cache"), root.__dict__.get("_computed_style_cache"))

    def test_viewport_resize_changes_the_computed_style_cache_key(self):
        from domonic.style import _computed_style_cache_key
        from domonic.window import Window

        document = Document()
        el = document.createElement("div")
        document.appendChild(el)
        win = Window(doc=document)
        win.resizeTo(1000, 800)
        wide_key = _computed_style_cache_key(el)
        win.resizeTo(400, 800)
        narrow_key = _computed_style_cache_key(el)
        self.assertNotEqual(wide_key, narrow_key)

    def test_media_query_rules_only_apply_at_the_matching_viewport(self):
        # a @media condition must be evaluated for real against the actual
        # viewport, not treated as always matching regardless of width.
        from domonic.window import Window

        page = html(
            head(
                style(
                    "@media (max-width: 600px) { .box { color: red; } }"
                    "@media (min-width: 601px) { .box { color: blue; } }"
                )
            ),
            body(div(_class="box")),
        )
        document = Document()
        document.appendChild(page)
        win = Window(doc=document)
        el = document.getElementsByClassName("box")[0]

        win.resizeTo(500, 800)
        self.assertEqual(win.getComputedStyle(el).getPropertyValue("color"), "rgb(255, 0, 0)")

        win.resizeTo(1000, 800)
        self.assertEqual(win.getComputedStyle(el).getPropertyValue("color"), "rgb(0, 0, 255)")

    def test_supports_condition_is_evaluated_for_real(self):
        # an @supports condition must be evaluated through CSS.supports(),
        # not treated as always matching regardless of what it says.
        page = html(
            head(
                style(
                    "@supports (display: grid) { .a { color: red; } }"
                    "@supports not (display: grid) { .b { color: red; } }"
                    "@supports (display: grid) and (gap: 1px) { .c { color: red; } }"
                )
            ),
            body(div(_class="a"), div(_class="b"), div(_class="c")),
        )
        document = Document()
        document.appendChild(page)

        a = document.getElementsByClassName("a")[0]
        b = document.getElementsByClassName("b")[0]
        c = document.getElementsByClassName("c")[0]
        self.assertEqual(ComputedStyleDeclaration(a).getPropertyValue("color"), "rgb(255, 0, 0)")
        self.assertEqual(ComputedStyleDeclaration(b).getPropertyValue("color"), "rgb(0, 0, 0)")
        self.assertEqual(ComputedStyleDeclaration(c).getPropertyValue("color"), "rgb(255, 0, 0)")

    # -- border-width / min-size / layout-box-driven used values -----------

    def test_border_width_is_zero_when_style_is_none_or_hidden(self):
        document = Document()
        for style in ("none", "hidden"):
            with self.subTest(border_style=style):
                el = document.createElement("div")
                el.setAttribute("style", f"border-style: {style}; border-width: 5px")
                document.appendChild(el)
                computed = ComputedStyleDeclaration(el)
                self.assertEqual(computed.getPropertyValue("border-top-width"), "0px")
                self.assertEqual(computed.getPropertyValue("border-right-width"), "0px")

    def test_border_width_unset_defaults_to_zero(self):
        # border-style's initial value is "none", so with nothing declared at
        # all the computed border-top-width is 0px, not the raw "medium" (or
        # whatever length) sitting in border-width.
        document = Document()
        el = document.createElement("div")
        document.appendChild(el)
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("border-top-width"), "0px")

    def test_border_width_kept_when_style_is_set(self):
        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "border-style: solid; border-width: 5px")
        document.appendChild(el)
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("border-top-width"), "5px")

    def test_logical_padding_and_margin_properties_expand_to_physical(self):
        # padding-inline/-block (and their single-side -start/-end longhands)
        # are Tailwind v4's generated CSS for essentially every spacing
        # value -- domonic's cascade only ever competes on physical longhand
        # names, so these must be expanded before the declaration reaches it.
        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "padding-inline: 10px; padding-block: 8px; margin-inline-start: 5px")
        document.appendChild(el)
        computed = ComputedStyleDeclaration(el)
        self.assertEqual(computed.getPropertyValue("padding-top"), "8px")
        self.assertEqual(computed.getPropertyValue("padding-right"), "10px")
        self.assertEqual(computed.getPropertyValue("padding-bottom"), "8px")
        self.assertEqual(computed.getPropertyValue("padding-left"), "10px")
        self.assertEqual(computed.getPropertyValue("margin-left"), "5px")

    def test_logical_property_wins_the_cascade_by_source_order(self):
        # a logical declaration must compete on the *same* physical longhand
        # name as an unrelated reset rule, at its own position in the
        # cascade -- not lose just because the reset's physical longhand
        # already has a value by the time anyone looks.
        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "padding: 0; padding-inline: 20px")
        document.appendChild(el)
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("padding-left"), "20px")

    def test_later_shorthand_overrides_an_earlier_one_for_a_shared_longhand(self):
        # `border: solid 1em blue; border-top: none;` in the same rule -- the
        # later `border-top` must win border-top-style/-width/-color back to
        # none/medium/currentcolor for the top side only, not lose to
        # `border`'s own expansion just because it's processed first.
        document = Document()
        sheet = CSSStyleSheet()
        sheet.replaceSync(".t { border: solid 1em blue; border-top: none; }")
        document.adoptedStyleSheets = [sheet]
        el = document.createElement("div")
        el.setAttribute("class", "t")
        document.appendChild(el)
        computed = ComputedStyleDeclaration(el)
        self.assertEqual(computed.getPropertyValue("border-top-style"), "none")
        self.assertEqual(computed.getPropertyValue("border-top-width"), "0px")
        self.assertEqual(computed.getPropertyValue("border-right-style"), "solid")

    def test_repeated_longhand_in_one_rule_keeps_the_later_value(self):
        # a stylesheet rule's declarations all share one cascade "order" (see
        # _build_rule_index), so two same-name entries don't naturally
        # compete by position -- the later one must still win.
        document = Document()
        sheet = CSSStyleSheet()
        sheet.replaceSync(".t { padding-left: 10px; padding-left: 5px; }")
        document.adoptedStyleSheets = [sheet]
        el = document.createElement("div")
        el.setAttribute("class", "t")
        document.appendChild(el)
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("padding-left"), "5px")

    def test_later_shorthand_in_a_separate_stylesheet_beats_an_earlier_longhand(self):
        # two same-specificity, same-origin/layer <style> blocks -- the
        # *later* one wins outright regardless of which form (shorthand or
        # longhand) either is written in. A common reset pattern
        # (`* { margin: 0; padding: 0; }`) relies on exactly this to clear a
        # longhand set anywhere earlier in the document.
        document = Document()
        early = CSSStyleSheet()
        early.replaceSync("ul { padding-left: 40px; }")
        later = CSSStyleSheet()
        later.replaceSync("ul { padding: 0; }")
        document.adoptedStyleSheets = [early, later]
        el = document.createElement("ul")
        document.appendChild(el)
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("padding-left"), "0px")

    def test_negative_padding_declaration_is_dropped_not_applied(self):
        # CSS 2.1 8.4: negative padding is invalid -- an invalid declaration
        # is dropped entirely, as if never written, not applied literally.
        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "padding-left: -1px")
        document.appendChild(el)
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("padding-left"), "0px")

    def test_invalid_second_declaration_leaves_the_earlier_valid_one(self):
        # the same property declared twice, the second one invalid: the
        # invalid one must not simply clamp to the initial value (0) -- the
        # earlier, still-valid 8px must survive, exactly as a real cascade
        # (the invalid declaration never entering it at all) would leave it.
        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "padding: 8px; padding: -8px")
        document.appendChild(el)
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("padding-left"), "8px")

    def test_border_width_keyword_resolves_to_px(self):
        # thin/medium/thick (CSS 2.1 8.5.3) are lengths, not passthrough
        # keywords -- every browser resolves them to 1px/3px/5px once a
        # border-style actually draws that side.
        document = Document()
        for keyword, px in (("thin", "1px"), ("medium", "3px"), ("thick", "5px")):
            with self.subTest(border_width=keyword):
                el = document.createElement("div")
                el.setAttribute("style", f"border-style: solid; border-width: {keyword}")
                document.appendChild(el)
                self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("border-top-width"), px)

    def test_border_shorthand_reflects_the_zeroed_width(self):
        document = Document()
        el = document.createElement("div")
        document.appendChild(el)
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("border-top"), "0px none rgb(0, 0, 0)")

    def test_min_width_and_min_height_normalise_auto_to_zero(self):
        # Matches Chrome: min-width/min-height's initial "auto" is reported
        # as 0px, not the literal keyword.
        document = Document()
        el = document.createElement("div")
        document.appendChild(el)
        computed = ComputedStyleDeclaration(el)
        self.assertEqual(computed.getPropertyValue("min-width"), "0px")
        self.assertEqual(computed.getPropertyValue("min-height"), "0px")

    def test_max_width_and_max_height_are_unaffected(self):
        # max-width/max-height's initial value is "none", not "auto" -- the
        # min-size normalisation must not touch them.
        document = Document()
        el = document.createElement("div")
        document.appendChild(el)
        computed = ComputedStyleDeclaration(el)
        self.assertEqual(computed.getPropertyValue("max-width"), "none")
        self.assertEqual(computed.getPropertyValue("max-height"), "none")

    def test_explicit_min_width_percent_is_untouched_without_a_layout_box(self):
        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "min-width: 50%")
        document.appendChild(el)
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("min-width"), "50%")

    def test_layout_box_resolves_auto_width_height_and_margin(self):
        from domonic.layout import LayoutBox, set_layout_box

        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "width: auto; height: auto; margin: auto")
        document.appendChild(el)
        set_layout_box(
            el,
            LayoutBox(content_width=200.0, content_height=80.0, margin_left=12.0, margin_right=12.0),
        )
        computed = ComputedStyleDeclaration(el)
        self.assertEqual(computed.getPropertyValue("width"), "200px")
        self.assertEqual(computed.getPropertyValue("height"), "80px")
        self.assertEqual(computed.getPropertyValue("margin-left"), "12px")
        self.assertEqual(computed.getPropertyValue("margin-right"), "12px")

    def test_layout_box_reports_box_size_when_content_size_unset(self):
        # A layout engine naturally computes a concrete box. When it does not
        # provide content_width/content_height separately, getComputedStyle
        # reports that real used geometry instead of falling back to auto/0px.
        from domonic.layout import LayoutBox, set_layout_box

        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "width: auto; height: auto; padding: 10px; border-style: solid; border-width: 5px")
        document.appendChild(el)
        set_layout_box(el, LayoutBox(width=220.0, height=120.0))
        computed = ComputedStyleDeclaration(el)
        self.assertEqual(computed.getPropertyValue("width"), "220px")
        self.assertEqual(computed.getPropertyValue("height"), "120px")

    def test_layout_box_regression_reports_real_width_from_external_layout(self):
        from domonic.dom import DOMParser
        from domonic.layout import LayoutBox

        doc = DOMParser().parseFromString(
            '<html><body><div id="x" style="padding:20px;"></div></body></html>',
            "text/html",
        )
        el = doc.getElementById("x")
        el.set_layout_box(
            LayoutBox(
                x=0,
                y=0,
                width=752,
                height=265,
                client_width=712,
                client_height=225,
                border_top=0,
                border_left=0,
            )
        )
        computed = ComputedStyleDeclaration(el)
        self.assertEqual(computed.getPropertyValue("width"), "752px")
        self.assertEqual(computed.getPropertyValue("height"), "265px")

    def test_layout_box_explicit_content_size_wins_over_derivation(self):
        from domonic.layout import LayoutBox, set_layout_box

        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "width: auto; padding: 10px")
        document.appendChild(el)
        set_layout_box(el, LayoutBox(width=220.0, content_width=150.0))
        self.assertEqual(ComputedStyleDeclaration(el).getPropertyValue("width"), "150px")

    def test_layout_box_percent_resolves_against_parents_derived_content_box(self):
        from domonic.layout import LayoutBox, set_layout_box

        document = Document()
        parent = document.createElement("div")
        parent.setAttribute("style", "padding: 20px")
        document.appendChild(parent)
        child = document.createElement("div")
        child.setAttribute("style", "width: 50%")
        parent.appendChild(child)
        set_layout_box(parent, LayoutBox(width=400.0))
        self.assertEqual(ComputedStyleDeclaration(child).getPropertyValue("width"), "200px")

    def test_min_width_and_min_height_auto_stay_zero_even_with_a_layout_box(self):
        # Matches a real browser: min-width/min-height:auto normalises to
        # 0px unconditionally (see test_min_width_and_min_height_normalise_
        # auto_to_zero) -- attaching a layout box does not change that, since
        # there is no general "automatic minimum size" a plain border box
        # implies. An explicit, non-auto min-width still resolves normally
        # (percentages against the parent's box, as tested elsewhere).
        from domonic.layout import LayoutBox, set_layout_box

        document = Document()
        el = document.createElement("div")
        document.appendChild(el)
        set_layout_box(el, LayoutBox(width=220.0, height=120.0))
        computed = ComputedStyleDeclaration(el)
        self.assertEqual(computed.getPropertyValue("min-width"), "0px")
        self.assertEqual(computed.getPropertyValue("min-height"), "0px")

    def test_layout_box_resolves_percent_width_against_the_parent_box(self):
        from domonic.layout import LayoutBox, clear_layout_box, set_layout_box

        document = Document()
        parent = document.createElement("div")
        document.appendChild(parent)
        child = document.createElement("div")
        child.setAttribute("style", "width: 50%")
        parent.appendChild(child)

        set_layout_box(parent, LayoutBox(content_width=400.0))
        self.assertEqual(ComputedStyleDeclaration(child).getPropertyValue("width"), "200px")

        clear_layout_box(parent)
        self.assertEqual(ComputedStyleDeclaration(child).getPropertyValue("width"), "50%")

    def test_layout_box_change_invalidates_the_cached_used_value(self):
        from domonic.window import window
        from domonic.layout import LayoutBox, clear_layout_box, set_layout_box

        document = Document()
        el = document.createElement("div")
        el.setAttribute("style", "margin-left: auto")
        document.appendChild(el)
        set_layout_box(el, LayoutBox(margin_left=10.0))
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("margin-left"), "10px")
        set_layout_box(el, LayoutBox(margin_left=25.0))
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("margin-left"), "25px")
        clear_layout_box(el)
        self.assertEqual(window.getComputedStyle(el).getPropertyValue("margin-left"), "auto")



def _computed(markup, selector, prop, pseudo=None):
    """``getComputedStyle(<selector>, pseudo).getPropertyValue(prop)`` on a parsed page."""
    import domonic
    from domonic.window import window

    page = domonic.parseString(markup)
    return window.getComputedStyle(page.querySelector(selector), pseudo).getPropertyValue(prop)


class CascadeSelectorTest(unittest.TestCase):
    """Selector shapes the cascade's rule index used to file or match wrongly."""

    def page(self, css, body):
        return f"<html><head><style>{css}</style></head><body>{body}</body></html>"

    def test_selector_list_splits_at_top_level_commas(self):
        markup = self.page("div:is(p, .x) { color: red } :is(p, table) span { color: green }", "<p><span>s</span></p>")
        self.assertEqual(_computed(markup, "span", "color"), "rgb(0, 128, 0)")
        # the rule is not a bare 'table' / '.x)' selector
        self.assertNotEqual(_computed(markup, "p", "color"), "rgb(255, 0, 0)")

    def test_pseudo_only_last_compound_is_an_implicit_universal(self):
        markup = self.page("div :first-child { color: green } section :after { content: \"x\" }",
                           "<div id=d><b id=b>b</b></div><section><i>i</i></section>")
        self.assertEqual(_computed(markup, "#b", "color"), "rgb(0, 128, 0)")
        self.assertNotEqual(_computed(markup, "#d", "color"), "rgb(0, 128, 0)")
        self.assertIn(_computed(markup, "section", "content", "::after"), ("", "normal", "none"))
        self.assertEqual(_computed(markup, "i", "content", "::after"), '"x"')

    def test_compound_with_several_pseudo_classes(self):
        markup = self.page(".btn:not(:disabled):not(.off) { color: green } .skip:not(:focus) { color: blue }",
                           "<button class=btn id=on>a</button><button class='btn off'>b</button><a class=skip>s</a>")
        self.assertEqual(_computed(markup, "#on", "color"), "rgb(0, 128, 0)")
        self.assertEqual(_computed(markup, ".skip", "color"), "rgb(0, 0, 255)")

    def test_not_takes_a_selector_list(self):
        markup = self.page("p:not(.a, .b) { color: green }", "<p class=a>a</p><p id=c>c</p>")
        self.assertEqual(_computed(markup, "#c", "color"), "rgb(0, 128, 0)")
        self.assertNotEqual(_computed(markup, ".a", "color"), "rgb(0, 128, 0)")

    def test_pseudo_element_names_are_case_insensitive(self):
        markup = self.page('p::BEFORE { content: "b" } p:After { content: "a" }', "<p>x</p>")
        self.assertEqual(_computed(markup, "p", "content", "::before"), '"b"')
        self.assertEqual(_computed(markup, "p", "content", "::after"), '"a"')

    def test_style_element_media_attribute_gates_the_sheet(self):
        markup = (
            "<html><head><style>p { color: green }</style><style media=print>p { color: red }</style>"
            "<style media='(prefers-color-scheme: dark)'>p { color: blue }</style></head><body><p>x</p></body></html>"
        )
        self.assertEqual(_computed(markup, "p", "color"), "rgb(0, 128, 0)")

    def test_an_imported_sheet_cascades_gated_by_its_media_and_layer(self):
        import domonic
        from domonic.window import window

        page = domonic.parseString(
            "<html><head><style>@import url(base.css); @import 'print.css' print;"
            "@import url(theme.css) layer(theme); p { margin-left: 1px }</style></head><body><p>x</p></body></html>"
        )
        sheet = page.styleSheets[0]
        imports = [rule for rule in sheet.cssRules if isinstance(rule, CSSImportRule)]
        self.assertEqual([rule.href for rule in imports], ["base.css", "print.css", "theme.css"])
        for rule, css in zip(imports, ["p { color: green }", "p { color: red }", "p { margin-left: 9px; padding-top: 2px }"]):
            rule.styleSheet = CSSStyleSheet()
            rule.styleSheet.replaceSync(css)
        computed = window.getComputedStyle(page.querySelector("p"))
        self.assertEqual(computed.getPropertyValue("color"), "rgb(0, 128, 0)")  # print.css doesn't apply
        self.assertEqual(computed.getPropertyValue("margin-left"), "1px")  # unlayered beats layer(theme)
        self.assertEqual(computed.getPropertyValue("padding-top"), "2px")

    def test_stylesheet_list_is_live_in_tree_order_with_element_sheets(self):
        import domonic
        from domonic.window import window

        page = domonic.parseString(
            "<html><head><link rel='stylesheet' href='a.css'><style>p { color: red }</style>"
            "<link rel=stylesheet><link rel='preload stylesheet' href='b.css'>"
            "<link rel='alternate stylesheet' href='c.css' title=C></head><body><p>x</p></body></html>"
        )
        sheets = page.styleSheets
        # tree order; the href-less link has no sheet; rel is a token list
        self.assertEqual([s.ownerNode.tagName for s in sheets], ["LINK", "STYLE", "LINK", "LINK"])
        self.assertEqual([sheets[0].href, sheets[2].href, sheets[3].href], ["a.css", "b.css", "c.css"])
        self.assertTrue(sheets[3].disabled)  # an alternate sheet
        style_el = page.querySelector("style")
        self.assertIs(style_el.sheet, sheets[1])
        style_el.sheet.insertRule("p { margin-left: 3px }", 0)
        added = page.createElement("style")
        self.assertIsNone(added.sheet)  # not in a document yet
        added.textContent = "p { color: green }"
        page.head.appendChild(added)
        self.assertEqual(len(page.styleSheets), 5)
        self.assertIs(page.styleSheets[1], style_el.sheet)
        computed = window.getComputedStyle(page.querySelector("p"))
        self.assertEqual(computed.getPropertyValue("color"), "rgb(0, 128, 0)")
        self.assertEqual(computed.getPropertyValue("margin-left"), "3px")
        page.head.removeChild(added)
        self.assertEqual(len(page.styleSheets), 4)

    def test_link_sheet_after_a_style_wins_by_source_order(self):
        import domonic
        from domonic.window import window

        page = domonic.parseString(
            "<html><head><style>p { color: red }</style><link rel=stylesheet href=x.css></head>"
            "<body><p>x</p></body></html>"
        )
        page.styleSheets[1].replaceSync("p { color: blue }")
        self.assertEqual(window.getComputedStyle(page.querySelector("p")).getPropertyValue("color"), "rgb(0, 0, 255)")

    def test_pseudo_element_inherits_from_its_element_not_its_parent(self):
        markup = self.page('body { font-size: 10px } div { font-size: 20px } div::before { content: "x"; font-size: 2em }',
                           "<div>x</div>")
        self.assertEqual(_computed(markup, "div", "font-size", "::before"), "40px")

    def test_inline_style_is_not_applied_to_pseudo_elements(self):
        markup = self.page('div::before { content: "x" }', '<div style="counter-reset: c 48; width: 10px">x</div>')
        self.assertEqual(_computed(markup, "div", "width"), "10px")
        self.assertEqual(_computed(markup, "div", "width", "::before"), "auto")
        self.assertNotIn("48", _computed(markup, "div", "counter-reset", "::before"))

    def test_unitless_line_height_is_inherited_as_the_number(self):
        markup = self.page(
            "body { font: 14px/1.5 serif } h1 { font-size: 2em } h2 { font-size: 20px; line-height: calc(1.25 / .5) }"
            " h2 b { font-size: 10px } p { line-height: 20px } p b { font-size: 40px }",
            "<h1>x</h1><h2><b>b</b></h2><p><b>b</b></p>",
        )
        self.assertEqual(_computed(markup, "h1", "line-height"), "42px")
        self.assertEqual(_computed(markup, "h2 b", "line-height"), "25px")
        self.assertEqual(_computed(markup, "p b", "line-height"), "20px")  # a length is inherited as the length

    def test_a_unitless_calc_line_height_multiplies_the_font_size(self):
        markup = self.page("p { font-size: 14px; line-height: calc(1.25 / .875) } i { line-height: calc(10px + 2px) }",
                           "<p>x</p><i>i</i>")
        self.assertEqual(_computed(markup, "p", "line-height"), "20px")
        self.assertEqual(_computed(markup, "i", "line-height"), "12px")

    def test_a_percentage_inset_without_layout_stays_a_percentage(self):
        markup = self.page("div { position: relative; width: 600px } p { position: relative; left: 50%; top: 10% }",
                           "<div><p>x</p></div>")
        self.assertEqual(_computed(markup, "p", "left"), "50%")
        self.assertEqual(_computed(markup, "p", "top"), "10%")

    def test_font_size_keywords_match_browsers_and_relative_keywords_scale(self):
        sizes = {"xx-small": "9px", "x-small": "10px", "small": "13px", "medium": "16px", "large": "18px",
                 "x-large": "24px", "xx-large": "32px", "xxx-large": "48px"}
        for keyword, expected in sizes.items():
            self.assertEqual(_computed(self.page(f"p {{ font-size: {keyword} }}", "<p>x</p>"), "p", "font-size"), expected)
        markup = self.page("div { font-size: 24px } sub { font-size: smaller } sup { font-size: larger }",
                           "<div><sub>a</sub><sup>b</sup></div>")
        self.assertEqual(_computed(markup, "sub", "font-size"), "20px")
        self.assertEqual(_computed(markup, "sup", "font-size"), "28.8px")

    def test_math_functions_and_viewport_units_resolve(self):
        import domonic
        from domonic.style import _eval_math
        from domonic.window import Window

        page = domonic.parseString(
            "<html><head><style>p { font-size: clamp(1rem, 2vw, 2rem) } i { width: 5vw; margin-left: min(10px, 2em) }"
            " b { font-size: calc(1rem + 1vw); padding-left: max(1rem, 30px) }</style></head>"
            "<body><p><i>i</i><b>b</b></p></body></html>"
        )
        window = Window()
        window.attach(page)
        style = window.getComputedStyle
        self.assertEqual(style(page.querySelector("p")).getPropertyValue("font-size"), "20.48px")
        self.assertEqual(style(page.querySelector("i")).getPropertyValue("width"), "51.2px")
        self.assertEqual(style(page.querySelector("i")).getPropertyValue("margin-left"), "10px")
        self.assertEqual(style(page.querySelector("b")).getPropertyValue("font-size"), "26.24px")
        self.assertEqual(style(page.querySelector("b")).getPropertyValue("padding-left"), "30px")
        # nesting, types and what needs a base
        self.assertEqual(_eval_math("calc((10px + 5px) / 3)", em_px=16, rem_px=16), (5.0, True))
        self.assertEqual(_eval_math("calc(1.25 / .875)", em_px=16, rem_px=16)[1], False)
        self.assertIsNone(_eval_math("calc(10px * 2px)", em_px=16, rem_px=16))
        self.assertIsNone(_eval_math("calc(1px + 2)", em_px=16, rem_px=16))
        self.assertIsNone(_eval_math("calc(50% - 10px)", em_px=16, rem_px=16))
        self.assertEqual(_eval_math("calc(50% - 10px)", em_px=16, rem_px=16, percent_px=200), (90.0, True))
        self.assertIsNone(_eval_math("clamp(1px, 2px)", em_px=16, rem_px=16))

    def test_a_custom_property_cycle_takes_the_fallback(self):
        markup = self.page(":root { --x: var(--x, 1rem); --a: var(--b, red); --b: var(--a) }"
                           " p { margin-left: var(--x, 2px); color: var(--a, green) }", "<p>x</p>")
        self.assertEqual(_computed(markup, "p", "margin-left"), "2px")
        self.assertEqual(_computed(markup, "p", "color"), "rgb(0, 128, 0)")

    def test_a_shorthand_with_var_is_expanded_after_substitution(self):
        markup = self.page(
            ":root { --m: 0 auto; --f: 2 3 10px; --b: 3px solid red }"
            " .a { margin: var(--m) } .b { flex: var(--f) } .c { border: var(--b) }"
            " .d { border: var(--missing, 1px dashed blue) } .e { border: var(--unset) solid black }"
            " .f { margin: var(--m); margin-left: 7px } .g { font: italic var(--fs, 20px)/2 serif }",
            "".join(f"<p class={c}>{c}</p>" for c in "abcdefg"),
        )
        self.assertEqual([_computed(markup, ".a", f"margin-{side}") for side in ("top", "right", "left")],
                         ["0px", "auto", "auto"])
        self.assertEqual([_computed(markup, ".b", p) for p in ("flex-grow", "flex-shrink", "flex-basis")],
                         ["2", "3", "10px"])
        self.assertEqual(_computed(markup, ".c", "border-left-color"), "rgb(255, 0, 0)")
        self.assertEqual(_computed(markup, ".c", "border-top-width"), "3px")
        self.assertEqual(_computed(markup, ".d", "border-top-style"), "dashed")
        # an unset var() with no fallback makes the shorthand invalid at computed-value time
        self.assertEqual(_computed(markup, ".e", "border-top-style"), "none")
        self.assertEqual(_computed(markup, ".f", "margin-left"), "7px")
        self.assertEqual(_computed(markup, ".g", "font-size"), "20px")
        self.assertEqual(_computed(markup, ".g", "line-height"), "40px")

    def test_shorthands_with_spaces_inside_functions_expand(self):
        markup = self.page(
            ".a { border-top: 12px solid rgba(0, 0, 0, .5) } .b { background: linear-gradient(to right, red, blue) no-repeat }"
            " .c { margin: 0 calc(1px + 2px) } .d { flex: 0 0 calc(50% - 10px) } .e { border: calc(1px + 1px) solid red }"
            " .f { text-decoration: underline rgba(0, 0, 0, 0.5) }",
            "".join(f"<p class={c}>{c}</p>" for c in "abcdef"),
        )
        self.assertEqual(_computed(markup, ".a", "border-top-width"), "12px")
        self.assertEqual(_computed(markup, ".a", "border-top-color"), "rgba(0, 0, 0, 0.5)")
        self.assertEqual(_computed(markup, ".b", "background-image"), "linear-gradient(to right, red, blue)")
        self.assertEqual(_computed(markup, ".b", "background-repeat"), "no-repeat")
        self.assertEqual(_computed(markup, ".c", "margin-right"), "3px")
        self.assertEqual(_computed(markup, ".d", "flex-basis"), "calc(50% - 10px)")
        self.assertEqual(_computed(markup, ".e", "border-top-width"), "2px")
        self.assertEqual(_computed(markup, ".f", "text-decoration-color"), "rgba(0, 0, 0, 0.5)")

    def test_a_registered_length_computes_a_unitless_zero_to_0px(self):
        markup = self.page(
            '@property --ring-offset { syntax: "<length>"; inherits: false; initial-value: 0 }'
            " p { --plain: 0; margin-left: calc(1px + var(--ring-offset)) }",
            "<p>x</p>",
        )
        self.assertEqual(_computed(markup, "p", "--ring-offset"), "0px")
        self.assertEqual(_computed(markup, "p", "--plain"), "0")  # unregistered: as written
        self.assertEqual(_computed(markup, "p", "margin-left"), "1px")

    def test_computed_font_family_is_serialised_like_a_browser(self):
        markup = self.page(
            "p { font-family: 'DejaVu Sans', Arial, Sans-Serif } i { font: 16px Times New Roman }"
            " b { font-family: 'monospace' } code { font-family: monospace }",
            "<p>p</p><i>i</i><b>b</b><code>c</code>",
        )
        self.assertEqual(_computed(markup, "p", "font-family"), '"DejaVu Sans", Arial, sans-serif')
        self.assertEqual(_computed(markup, "i", "font-family"), '"Times New Roman"')
        self.assertEqual(_computed(markup, "b", "font-family"), '"monospace"')
        # a family named "monospace" isn't the generic: no 13px quirk for it
        self.assertEqual(_computed(markup, "b", "font-size"), "16px")
        self.assertEqual(_computed(markup, "code", "font-size"), "13px")

    def test_monospace_quirk_respects_an_inherited_absolute_size(self):
        markup = self.page(
            "body { font-size: 12px } .k { font-size: medium } pre { font-family: monospace }"
            " .e { font-size: 2em; font-family: monospace }",
            "<pre>a</pre><div class=k><pre id=b>b</pre><p class=e>e</p></div>",
        )
        self.assertEqual(_computed(markup, "pre", "font-size"), "12px")  # absolute size inherited from body
        self.assertEqual(_computed(markup, "#b", "font-size"), "13px")  # a keyword clears it
        self.assertEqual(_computed(markup, ".e", "font-size"), "26px")

    def test_flex_and_grid_items_are_blockified(self):
        markup = self.page('.f { display: flex } .g { display: inline-grid } .ib { display: inline-block }'
                           ' .f::before { content: "x" }',
                           "<div class=f><span>a</span><i class=ib>i</i></div><div class=g><b>b</b></div>"
                           "<p><span id=n>n</span></p>")
        self.assertEqual(_computed(markup, ".f span", "display"), "block")
        self.assertEqual(_computed(markup, ".ib", "display"), "block")
        self.assertEqual(_computed(markup, ".g b", "display"), "block")
        self.assertEqual(_computed(markup, ".f", "display", "::before"), "block")
        self.assertEqual(_computed(markup, "#n", "display"), "inline")

    def test_hwb_light_dark_and_system_colours_compute_to_rgb(self):
        markup = self.page(
            ".a { color: hwb(120 0% 50%) } .b { background-color: hwb(0 50% 50%); color: hwb(240 20% 20% / 50%) }"
            " .c { color: light-dark(rgb(1, 2, 3), white) }"
            " .d { color-scheme: dark; color: light-dark(red, rgb(0, 0, 255)); background-color: Canvas }"
            " .e { color: LinkText; border-top-color: ButtonFace }",
            "".join(f"<p class={c}>{c}</p>" for c in "abcde"),
        )
        expected = {(".a", "color"): "rgb(0, 128, 0)", (".b", "background-color"): "rgb(128, 128, 128)",
                    (".b", "color"): "rgba(51, 51, 204, 0.5)", (".c", "color"): "rgb(1, 2, 3)",
                    (".d", "color"): "rgb(0, 0, 255)", (".d", "background-color"): "rgb(18, 18, 18)",
                    (".e", "color"): "rgb(0, 0, 238)", (".e", "border-top-color"): "rgb(239, 239, 239)"}
        for (selector, prop), value in expected.items():
            self.assertEqual(_computed(markup, selector, prop), value, f"{selector} {prop}")

    def test_computed_urls_are_absolute_against_their_stylesheet(self):
        import domonic
        from domonic.window import Window

        page = domonic.parseString(
            "<html><head><link rel=stylesheet href='/css/main.css'><style>p { background-image: url(img/a.png),"
            " url(data:image/png;base64,AAA) } i { list-style-image: url('/b.svg'); fill: url(#grad) }</style></head>"
            "<body><p style='cursor: url(c.cur), auto'>x</p><i>i</i><b>b</b></body></html>"
        )
        page.URL = "https://example.com/docs/page.html"
        linked = page.styleSheets[0]
        linked.href = "https://cdn.example.org/css/main.css"
        linked.replaceSync("b { background: url(../img/b.png) no-repeat }")
        window = Window()
        window.attach(page)

        def style(selector, prop):
            return window.getComputedStyle(page.querySelector(selector)).getPropertyValue(prop)

        self.assertEqual(style("p", "background-image"),
                         'url("https://example.com/docs/img/a.png"), url("data:image/png;base64,AAA")')
        self.assertEqual(style("i", "list-style-image"), 'url("https://example.com/b.svg")')
        self.assertEqual(style("i", "fill"), "url(#grad)")  # a fragment reference stays local
        self.assertEqual(style("p", "cursor"), 'url("https://example.com/docs/c.cur"), auto')
        self.assertEqual(style("b", "background-image"), 'url("https://cdn.example.org/img/b.png")')

    def test_currentcolor_is_inherited_as_the_keyword(self):
        markup = self.page(".c { background-color: currentcolor; color: red } .c i { color: blue; background-color: inherit }",
                           "<div class=c><i>i</i></div>")
        self.assertEqual(_computed(markup, "i", "background-color"), "rgb(0, 0, 255)")

    def test_inherit_copies_a_percentage_not_the_parents_pixels(self):
        from domonic.layout import LayoutBox, set_layout_box

        document = Document()
        outer = document.createElement("div")
        document.appendChild(outer)
        middle = document.createElement("div")
        middle.setAttribute("style", "width: 100%")
        outer.appendChild(middle)
        inner = document.createElement("span")
        inner.setAttribute("style", "width: inherit")
        middle.appendChild(inner)
        set_layout_box(outer, LayoutBox(content_width=800.0))
        set_layout_box(middle, LayoutBox(content_width=400.0))
        self.assertEqual(ComputedStyleDeclaration(middle).getPropertyValue("width"), "800px")
        self.assertEqual(ComputedStyleDeclaration(inner).getPropertyValue("width"), "400px")

    def test_nested_rules_cascade(self):
        import domonic
        from domonic.window import Window

        page = domonic.parseString(
            "<html><head><style>"
            ".a { color: red; .b { color: blue } & + p { margin-left: 1px } > .c { padding-top: 2px }"
            " @media (min-width: 1px) { border-top-style: solid; .d { margin-top: 3px } } padding-left: 4px }"
            ' .x, .y { &.z { color: green } .w & { margin-left: 9px } } p[data-a="a&b"] { color: rgb(1, 2, 3) }'
            "</style></head><body><div class=a><span class=b>b</span><i class=c>c</i><em class=d>d</em></div>"
            "<p>p</p><div class='y z'>z</div><section class=w><div class=x>x</div></section>"
            '<p data-a="a&b">q</p></body></html>'
        )
        window = Window()
        window.attach(page)

        def style(selector, prop):
            return window.getComputedStyle(page.querySelector(selector)).getPropertyValue(prop)

        self.assertEqual(style(".a", "color"), "rgb(255, 0, 0)")
        self.assertEqual(style(".a", "padding-left"), "4px")  # declarations after nested rules
        self.assertEqual(style(".a", "border-top-style"), "solid")  # a nested @media's declarations
        self.assertEqual(style(".b", "color"), "rgb(0, 0, 255)")  # relative: .a .b
        self.assertEqual(style(".a + p", "margin-left"), "1px")
        self.assertEqual(style(".c", "padding-top"), "2px")
        self.assertEqual(style(".d", "margin-top"), "3px")
        self.assertEqual(style(".y", "color"), "rgb(0, 128, 0)")  # &.z for each parent of a list
        self.assertEqual(style(".w .x", "margin-left"), "9px")
        self.assertEqual(style("p[data-a]", "color"), "rgb(1, 2, 3)")  # an & in a string isn't nesting

    def test_revert_layer_and_revert_roll_the_cascade_back(self):
        markup = self.page(
            "@layer base, theme; @layer base { p { color: green; margin-left: 2px } }"
            " @layer theme { p { color: revert-layer; margin-left: revert-layer } .r { color: revert } }"
            " p.u { margin-left: revert-layer } .n { color: red } .n { color: revert-layer }"
            " script.s { display: block } script.s { display: revert }",
            "<p>a</p><p class=r>r</p><p class=u>u</p><p class=n>n</p>"
            "<div style='color: blue'><p class=r>r2</p></div><script class=s></script>",
        )
        self.assertEqual(_computed(markup, "p", "color"), "rgb(0, 128, 0)")
        self.assertEqual(_computed(markup, "p", "margin-left"), "2px")
        self.assertEqual(_computed(markup, ".r", "color"), "rgb(0, 0, 0)")  # revert: out of the author origin
        self.assertEqual(_computed(markup, ".u", "margin-left"), "2px")  # rolls back twice
        self.assertEqual(_computed(markup, ".n", "color"), "rgb(0, 128, 0)")
        self.assertEqual(_computed(markup, "div .r", "color"), "rgb(0, 0, 255)")  # ...to inheritance
        self.assertEqual(_computed(markup, "script.s", "display"), "none")  # ...to the UA default

    def test_the_dir_attribute_sets_direction_like_the_ua_sheet(self):
        markup = (
            "<html dir=rtl><head><style>.x { direction: ltr }</style></head><body><p>a</p><div dir=ltr><i>i</i></div>"
            "<b dir=RTL>b</b><em dir=foo>e</em><span dir=rtl class=x>x</span><u dir=rtl style='direction: ltr'>u</u>"
            "</body></html>"
        )
        expected = {"p": "rtl", "i": "ltr", "b": "rtl", "em": "rtl", ".x": "ltr", "u": "ltr"}
        for selector, direction in expected.items():
            self.assertEqual(_computed(markup, selector, "direction"), direction, selector)

    def test_state_pseudo_classes_in_the_cascade(self):
        markup = self.page(
            "input:placeholder-shown { color: green } input:required { margin-left: 3px } a:hover { color: red }",
            "<input placeholder=x required><a href=#>l</a>",
        )
        self.assertEqual(_computed(markup, "input", "color"), "rgb(0, 128, 0)")
        self.assertEqual(_computed(markup, "input", "margin-left"), "3px")
        self.assertNotEqual(_computed(markup, "a", "color"), "rgb(255, 0, 0)")


class ShorthandExpansionTest(unittest.TestCase):
    """``_cssom.expand_shorthand`` against what browsers set each longhand to."""

    def expand(self, name, value):
        from domonic._cssom import expand_shorthand

        pairs = expand_shorthand(name, value)
        return dict(pairs) if pairs is not None else None

    def test_list_style_none_sets_whichever_of_type_and_image_is_unset(self):
        self.assertEqual(self.expand("list-style", "none")["list-style-type"], "none")
        self.assertEqual(self.expand("list-style", "none")["list-style-image"], "none")
        expanded = self.expand("list-style", "none url(a.png)")
        self.assertEqual((expanded["list-style-type"], expanded["list-style-image"]), ("none", "url(a.png)"))
        expanded = self.expand("list-style", "square none")
        self.assertEqual((expanded["list-style-type"], expanded["list-style-image"]), ("square", "none"))
        self.assertEqual(self.expand("list-style", "inside")["list-style-type"], "disc")

    def test_columns_takes_width_and_count_in_either_order(self):
        self.assertEqual(self.expand("columns", "6 100px"), {"column-width": "100px", "column-count": "6"})
        self.assertEqual(self.expand("columns", "100px 6"), {"column-width": "100px", "column-count": "6"})
        self.assertEqual(self.expand("columns", "6"), {"column-width": "auto", "column-count": "6"})
        self.assertEqual(self.expand("columns", "auto 12em"), {"column-width": "12em", "column-count": "auto"})
        self.assertIsNone(self.expand("columns", "1 2"))

    def test_font_slash_spacing_numeric_weights_and_system_fonts(self):
        spaced = self.expand("font", "1rem / 1.5 sans-serif")
        self.assertEqual((spaced["font-size"], spaced["line-height"], spaced["font-family"]), ("1rem", "1.5", "sans-serif"))
        weighted = self.expand("font", "650 16px serif")
        self.assertEqual((weighted["font-weight"], weighted["font-size"], weighted["font-family"]), ("650", "16px", "serif"))
        fluid = self.expand("font", "clamp(1rem, 2vw, 2rem)/1.2 serif")
        self.assertEqual((fluid["font-size"], fluid["line-height"]), ("clamp(1rem, 2vw, 2rem)", "1.2"))
        menu = self.expand("font", "menu")
        self.assertEqual((menu["font-size"], menu["font-family"]), ("13px", "Arial"))

    def test_flex_basis_of_a_unitless_zero_is_0px_and_a_third_number_is_invalid(self):
        self.assertEqual(self.expand("flex", "1 1 0")["flex-basis"], "0px")
        self.assertEqual(self.expand("flex", "1")["flex-basis"], "0%")
        self.assertEqual(self.expand("flex", "10px 2"), {"flex-grow": "2", "flex-shrink": "1", "flex-basis": "10px"})
        self.assertEqual(self.expand("flex", "1 calc(50% - 10px)")["flex-basis"], "calc(50% - 10px)")
        self.assertIsNone(self.expand("flex", "0 0 4"))

    def test_grid_shorthands_expand(self):
        self.assertEqual(self.expand("grid-row", "foo"), {"grid-row-start": "foo", "grid-row-end": "foo"})
        self.assertEqual(self.expand("grid-row", "span 2")["grid-row-end"], "auto")
        self.assertEqual(
            self.expand("grid-area", "a / b"),
            {"grid-row-start": "a", "grid-column-start": "b", "grid-row-end": "a", "grid-column-end": "b"},
        )
        self.assertEqual(self.expand("grid-area", "1 / 1")["grid-row-end"], "auto")
        template = self.expand("grid-template", "auto 1fr / 12.25rem minmax(0,1fr)")
        self.assertEqual(template["grid-template-columns"], "12.25rem minmax(0,1fr)")
        areas = self.expand("grid-template", '[a] "h h" 50px [b] "s m" 1fr / 100px 1fr')
        self.assertEqual(areas["grid-template-rows"], "[a] 50px [b] 1fr")
        self.assertEqual(areas["grid-template-areas"], '"h h" "s m"')
        grid = self.expand("grid", "auto-flow dense 40px / 1fr 1fr")
        self.assertEqual((grid["grid-auto-flow"], grid["grid-auto-rows"]), ("row dense", "40px"))
        self.assertEqual(self.expand("grid", "100px 1fr / auto-flow 3em")["grid-auto-columns"], "3em")

    def test_grid_area_places_an_item_in_the_cascade(self):
        markup = (
            "<html><head><style>.i { grid-area: 2 / 1 / 3 / 4 } .w { grid-template: auto 1fr / 1fr 2fr }</style></head>"
            "<body><div class=w><p class=i>x</p></div></body></html>"
        )
        self.assertEqual(_computed(markup, ".i", "grid-row-start"), "2")
        self.assertEqual(_computed(markup, ".i", "grid-column-end"), "4")
        self.assertEqual(_computed(markup, ".w", "grid-template-columns"), "1fr 2fr")

    def test_elliptical_border_radius(self):
        self.assertEqual(
            self.expand("border-radius", "10px 20px / 5px"),
            {"border-top-left-radius": "10px 5px", "border-top-right-radius": "20px 5px",
             "border-bottom-right-radius": "10px 5px", "border-bottom-left-radius": "20px 5px"},
        )
        style = CSSStyleDeclaration()
        style.cssText = "border-radius: 1px 2px 3px 4px / 5px 6px"
        self.assertEqual(style.getPropertyValue("border-bottom-left-radius"), "4px 6px")
        self.assertEqual(style.cssText, "border-radius: 1px 2px 3px 4px / 5px 6px;")
        self.assertIsNone(self.expand("margin", "1px 2px 3px 4px 5px"))

    def test_background_layers_and_position_size(self):
        single = self.expand("background", "url(a.png) 0 0/2ch 2ch no-repeat")
        self.assertEqual((single["background-position"], single["background-size"]), ("0 0", "2ch 2ch"))
        cover = self.expand("background", "#fff url(x.png) center / cover no-repeat fixed")
        self.assertEqual((cover["background-size"], cover["background-color"]), ("cover", "#fff"))
        layered = self.expand("background", "url(a.svg), linear-gradient(red, blue) no-repeat")
        self.assertEqual(layered["background-image"], "url(a.svg), linear-gradient(red, blue)")
        self.assertEqual(layered["background-repeat"], "repeat, no-repeat")
        self.assertEqual(layered["background-color"], "transparent")
        self.assertIsNone(self.expand("background", "url(a) red, blue"))  # colour only in the final layer

    def test_all_resets_every_longhand_but_direction(self):
        self.assertEqual(self.expand("all", "unset")["color"], "unset")
        self.assertNotIn("direction", self.expand("all", "initial"))
        self.assertNotIn("unicode-bidi", self.expand("all", "initial"))
        markup = (
            "<html><head><style>button { color: red; padding: 5px; direction: rtl } button.x { all: unset }"
            " p { color: green } p b { all: inherit }</style></head>"
            "<body><button class=x>a</button><p style='margin-left: 4px'><b>b</b></p></body></html>"
        )
        self.assertEqual(_computed(markup, ".x", "color"), "rgb(0, 0, 0)")
        self.assertEqual(_computed(markup, ".x", "padding-left"), "0px")
        self.assertEqual(_computed(markup, ".x", "direction"), "rtl")
        self.assertEqual(_computed(markup, "p b", "margin-left"), "4px")


    def test_place_shorthands_take_multi_word_alignment_values(self):
        self.assertEqual(self.expand("place-content", "unsafe center safe flex-start"),
                         {"align-content": "unsafe center", "justify-content": "safe flex-start"})
        self.assertEqual(self.expand("place-content", "baseline")["justify-content"], "start")
        self.assertEqual(self.expand("place-items", "first baseline")["justify-items"], "first baseline")
        self.assertEqual(self.expand("place-items", "center legacy left")["justify-items"], "legacy left")
        # a rule setting both longhands serialises them as place-content and
        # must read back
        markup = ("<html><head><style>.a { justify-content: safe flex-start; align-content: unsafe center }</style>"
                  "</head><body><p class=a>a</p></body></html>")
        self.assertEqual(_computed(markup, ".a", "justify-content"), "safe flex-start")
        self.assertEqual(_computed(markup, ".a", "align-content"), "unsafe center")


class MediaQueryTest(unittest.TestCase):
    def matches(self, query, width=1024, height=768, **kwargs):
        from domonic.window import MediaQueryList

        return MediaQueryList._evaluate(query, width=width, height=height, **kwargs)

    def test_calc_values_and_value_first_ranges(self):
        mdn = "(width >= calc(1rem * 2 + (15rem + 2rem) * 2 + 31rem))"  # MDN's two-sidebar layout
        self.assertTrue(self.matches(mdn, width=1200))
        self.assertFalse(self.matches(mdn, width=900))
        self.assertTrue(self.matches("(1000px < width)"))
        self.assertFalse(self.matches("(1000px < width)", width=900))
        self.assertTrue(self.matches("(400px <= width <= 1100px)"))
        self.assertTrue(self.matches("screen and (min-width: 40em)"))

    def test_ratios_resolution_and_logic(self):
        self.assertTrue(self.matches("(aspect-ratio: 4/3)"))
        self.assertFalse(self.matches("(min-aspect-ratio: 16/9)"))
        self.assertTrue(self.matches("(resolution >= 1dppx)"))
        self.assertFalse(self.matches("(min-resolution: 2dppx)"))
        self.assertTrue(self.matches("(pointer: coarse) or (min-width: 1000px)"))
        self.assertTrue(self.matches("(width > 600px) and (not (height < 100px))"))
        self.assertTrue(self.matches("not screen and (max-width: 100px)"))
        self.assertFalse(self.matches("only screen and (min-width: 768px) and (max-width: 1023px)"))
        self.assertFalse(self.matches("not (unknown-feature)"))  # unknown, not false
        self.assertTrue(self.matches("screen, print"))


class InitialValuesTest(unittest.TestCase):
    def test_common_longhands_report_their_initial_values(self):
        document = Document()
        element = document.createElement("div")
        document.appendChild(element)
        computed = ComputedStyleDeclaration(element)
        for name, initial in {"quotes": "auto", "content": "normal", "box-shadow": "none", "filter": "none",
                              "counter-reset": "none", "will-change": "auto", "aspect-ratio": "auto",
                              "transform-style": "flat", "text-overflow": "clip", "color-scheme": "normal"}.items():
            self.assertEqual(computed.getPropertyValue(name), initial, name)

    def test_camelcase_accessors_on_a_computed_style(self):
        markup = ("<html><head><style>p { justify-self: end; row-gap: 3px; place-items: center; aspect-ratio: 2 / 1 }"
                  "</style></head><body><p>a</p></body></html>")
        import domonic
        from domonic.window import window

        computed = window.getComputedStyle(domonic.parseString(markup).querySelector("p"))
        self.assertEqual(computed.justifySelf, "end")
        self.assertEqual(computed.justifyItems, "center")
        self.assertEqual(computed.rowGap, "3px")
        self.assertEqual(computed.placeItems, "center")
        self.assertEqual(computed.aspectRatio, "2 / 1")
        self.assertEqual(computed.containerType, "normal")
        with self.assertRaises(AttributeError):
            computed.notACssProperty

    def test_color_scheme_and_caret_color_inherit(self):
        markup = "<html><head><style>div { color-scheme: dark }</style></head><body><div><p>x</p></div></body></html>"
        self.assertEqual(_computed(markup, "p", "color-scheme"), "dark")


class InlineStyleTest(unittest.TestCase):
    def test_css_wide_keywords_are_not_folded_into_a_shorthand(self):
        style = CSSStyleDeclaration()
        style.cssText = "border-width: 50px; border-style: solid; border-color: inherit"
        self.assertEqual(style.cssText, "border-width: 50px; border-style: solid; border-color: inherit;")
        style.cssText = "margin-top: inherit; margin-right: 1px; margin-bottom: 1px; margin-left: 1px"
        self.assertNotIn("margin:", style.cssText)
        style.cssText = "margin-top: unset; margin-right: unset; margin-bottom: unset; margin-left: unset"
        self.assertEqual(style.cssText, "margin: unset;")

    def test_reading_style_does_not_rewrite_the_attribute(self):
        import domonic
        from domonic import _cssom

        page = domonic.parseString('<html><body><p style="color:red;MARGIN : 1px">x</p></body></html>')
        p = page.querySelector("p")
        epoch = _cssom.dom_style_epoch()
        self.assertEqual(p.style.color, "red")
        self.assertEqual(p.style.marginTop, "1px")
        self.assertEqual(p.getAttribute("style"), "color:red;MARGIN : 1px")
        self.assertEqual(_cssom.dom_style_epoch(), epoch)
        # a CSSOM write still serialises the whole block back
        p.style.color = "blue"
        self.assertEqual(p.getAttribute("style"), "color: blue; margin: 1px;")


class StylesheetParsingTest(unittest.TestCase):
    """CSS Syntax 3 details the stylesheet and declaration parsers missed."""

    def rules(self, css):
        sheet = CSSStyleSheet()
        sheet.replaceSync(css)
        return [rule.cssText for rule in sheet.cssRules]

    def test_comments_separate_tokens_and_skip_strings(self):
        self.assertEqual(self.rules("p { color: rgb(10/**/175/**/10) }"), ["p {color: rgb(10 175 10);}"])
        self.assertEqual(self.rules('a::after { content: "/*x*/" }'), ['a::after {content: "/*x*/";}'])
        self.assertEqual(self.rules("/* a { b } */ i { color: red }"), ["i {color: red;}"])

    def test_escapes_outside_strings_do_not_open_strings_or_blocks(self):
        # Tailwind's escaped class names (react.dev): the escaped quote used to
        # open a string that ran to the end of the sheet
        rules = self.rules(r".after\:content-\[\'\'\]:after { content: '' } p { color: red } .a\{b { color: blue }")
        self.assertEqual(len(rules), 3)
        self.assertEqual(rules[1], "p {color: red;}")
        self.assertEqual(rules[2], r".a\{b {color: blue;}")

    def test_a_block_open_at_the_end_of_the_sheet_is_closed(self):
        self.assertEqual(
            self.rules("p { color: red } .test { width: 10px; white-space: pre"),
            ["p {color: red;}", ".test {width: 10px; white-space: pre;}"],
        )
        self.assertEqual(
            self.rules("@media screen { p { color: red } .x { color: blue"),
            ["@media screen {p {color: red;} .x {color: blue;}}"],
        )

    def test_cdo_and_cdc_at_the_top_level_are_ignored(self):
        self.assertEqual(
            self.rules("<!-- p { color: red } --> .b { border: 1px } <!-- --> .c { color: blue }"),
            ["p {color: red;}", ".b {border: 1px;}", ".c {color: blue;}"],
        )

    def test_supports_evaluates_a_parenthesised_group_as_a_condition(self):
        self.assertFalse(CSS.supports("not ((-webkit-mask-image: none) or (mask-image: none))"))
        self.assertTrue(CSS.supports("((display: grid) and (color: red))"))
        self.assertFalse(CSS.supports("(not (display: grid))"))
        self.assertTrue(CSS.supports("((color: red))"))
        sheet = CSSStyleSheet()
        sheet.replaceSync("@supports not ((mask-image: none) or (-webkit-mask-image: none)) { p { color: red } }")
        rule = sheet.cssRules[0]
        self.assertFalse(_supports_condition(rule.conditionText))

    def test_property_names_keep_prefixes_and_map_legacy_aliases(self):
        from domonic.style import _css_property_name

        self.assertEqual(_css_property_name("-webkit-mask-image"), "-webkit-mask-image")
        self.assertEqual(_css_property_name("MozBoxSizing"), "-moz-box-sizing")
        self.assertEqual(_css_property_name("marginTop"), "margin-top")
        self.assertEqual(_css_property_name("MARGIN-TOP"), "margin-top")
        self.assertEqual(_css_property_name("-font-family"), "-font-family")  # not a vendor prefix: unknown
        self.assertEqual(_css_property_name("grid-gap"), "gap")
        self.assertEqual(_css_property_name("wordWrap"), "overflow-wrap")
        self.assertEqual(_css_property_name("-webkit-flex-direction"), "flex-direction")
        markup = (
            "<html><head><style>.g { display: grid; grid-gap: 1.25rem } p { word-wrap: break-word; -font-family: x }"
            "</style></head><body><div class=g><p>x</p></div></body></html>"
        )
        self.assertEqual(_computed(markup, ".g", "row-gap"), "20px")
        self.assertEqual(_computed(markup, "p", "overflow-wrap"), "break-word")
        self.assertNotEqual(_computed(markup, "p", "font-family"), "x")

    def test_logical_properties_keep_their_names_in_a_declaration_block(self):
        style = CSSStyleDeclaration()
        style.cssText = "padding-inline: calc(var(--p) - 1px); inline-size: 100px; border-block: 2px dashed"
        self.assertEqual(style.getPropertyValue("padding-inline-end"), "calc(var(--p) - 1px)")
        self.assertEqual(style.getPropertyValue("inline-size"), "100px")
        self.assertEqual(style.getPropertyValue("border-block-end"), "2px dashed")
        self.assertEqual(style.getPropertyValue("padding-right"), "")  # (a separate property, as in a browser)

    def test_logical_properties_map_by_writing_mode_and_direction(self):
        markup = (
            "<html><head><style>ul { padding-inline-start: 40px } .v { writing-mode: vertical-rl; margin-block: 1em 2px }"
            " .both { margin-left: 5px; margin-inline-start: 7px } .phys { margin-inline-start: 7px; margin-left: 5px }"
            " .b { border-inline-start: 2px solid red; border-start-end-radius: 3px; inline-size: 50px }"
            " :root { --bb: 4px dashed blue } .vb { border-inline-end: var(--bb) }</style></head><body>"
            "<ul id=ltr><li>a</li></ul><div dir=rtl><ul id=rtl><li>b</li></ul><p class=b>b</p><p class=vb>vb</p></div>"
            "<p class=v>v</p><p class=both>x</p><p class=phys>y</p><p class=b id=lb>z</p>"
            "<p style='direction: rtl; padding-inline-end: 3px; border-inline-start: 1px solid' id=inl>i</p>"
            "</body></html>"
        )
        expected = {
            ("#ltr", "padding-left"): "40px", ("#rtl", "padding-right"): "40px", ("#rtl", "padding-left"): "0px",
            (".v", "margin-right"): "16px", (".v", "margin-left"): "2px",  # vertical-rl: block start is the right
            (".both", "margin-left"): "7px", (".phys", "margin-left"): "5px",  # the later declaration wins
            ("div .b", "border-right-style"): "solid", ("div .b", "border-top-left-radius"): "3px",
            ("div .b", "width"): "50px", ("#lb", "border-left-style"): "solid", ("#lb", "border-top-right-radius"): "3px",
            (".vb", "border-left-style"): "dashed", (".vb", "border-left-width"): "4px",  # var() substituted, then mapped
            ("#inl", "padding-left"): "3px", ("#inl", "border-right-style"): "solid",
        }
        for (selector, prop), value in expected.items():
            self.assertEqual(_computed(markup, selector, prop), value, f"{selector} {prop}")

    def test_supports_checks_the_value_where_a_grammar_is_known(self):
        self.assertFalse(CSS.supports("(display: bogus-value-xyz)"))
        self.assertFalse(CSS.supports("display", "nope"))
        self.assertFalse(CSS.supports("(padding: -1px)"))
        self.assertTrue(CSS.supports("(display: inline flow-root)"))
        self.assertTrue(CSS.supports("(aspect-ratio: 1)"))
        self.assertTrue(CSS.supports("(color: red)"))

    def test_font_feature_values_keeps_its_family_list(self):
        sheet = CSSStyleSheet()
        sheet.replaceSync('@font-feature-values Font One, "Font Two" { @styleset { nice-style: 12; } }')
        rule = sheet.cssRules[0]
        self.assertEqual(rule.fontFamily, '"Font One", "Font Two"')
        self.assertTrue(rule.cssText.startswith('@font-feature-values "Font One", "Font Two" {'))

    def test_comments_in_a_declaration_block(self):
        style = CSSStyleDeclaration()
        style.cssText = "/* lead */ color: red; /* between */ margin: 1px"
        self.assertEqual(style.getPropertyValue("color"), "red")
        self.assertEqual(style.getPropertyValue("margin"), "1px")
        self.assertEqual(style.cssText, "color: red; margin: 1px;")


if __name__ == "__main__":
    unittest.main()
