"""
test_domonic
~~~~~~~~~~~~
unit tests for css
"""

import unittest

from domonic.dom import *
from domonic.html import *
from domonic.style import *


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
        assert str(test) == '<div style="align-content:flex-start;">huh?</div>'

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
        assert "font-size:12px;" in str(sometag)
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
        assert cssStyleSheet.cssRules[0].style.cssText == "background-color: green"

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
        self.assertEqual(style.getPropertyValue("margin"), "0")
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
            "color:green;accent-color:hotpink;container-type:inline-size;",
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
        self.assertEqual(import_rule.href, 'url("theme.css")')
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
        self.assertEqual(computed.getPropertyValue("color"), "blue")  # inline wins
        self.assertEqual(computed.getPropertyValue("padding"), "8px")  # .box
        self.assertEqual(computed.getPropertyValue("padding-top"), "8px")
        self.assertEqual(computed.getPropertyValue("font-weight"), "bold")  # #hero
        self.assertEqual(computed.getPropertyValue("font-size"), "13px")  # .box
        self.assertEqual(computed.getPropertyValue("margin"), "4px")  # inline
        self.assertEqual(computed.getPropertyValue("display"), "inline")  # initial

        span = page.querySelector("span")
        span_computed = window.getComputedStyle(span)
        self.assertEqual(span_computed.getPropertyValue("color"), "blue")  # inherited
        self.assertEqual(span_computed.getPropertyValue("font-size"), "13px")  # inherited
        self.assertEqual(span_computed.getPropertyValue("margin"), "0px")  # not inherited

        with self.assertRaises(Exception):
            span_computed.setProperty("color", "orange")

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


if __name__ == "__main__":
    unittest.main()
