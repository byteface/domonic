"""
    test_domonic
    ~~~~~~~~~~~~
    unit tests for css
"""

import unittest
# import requests
# from mock import patch

from domonic.html import *
from domonic.style import *
from domonic.dom import *


class TestCase(unittest.TestCase):

    def test_domonic_css(self):

        test = div("huh?", _style="alignContent: center;")  # TODO - should be parsing these styles
        print(test.style.alignContent)
        test.style.alignContent = 'flex-start'
        print(test.style.alignContent)
        print(str(test))
        assert test.style.alignContent == 'flex-start'
        # assert str(test) == '<div style="align-content: flex-start;">huh?</div>'

        atag = a("linky", _href="https://eventual.technology", _style="alignContent: center;")
        print(atag.style.alignContent)

        sometag = div("asdfasdf", _id="test")
        print(sometag.style)
        sometag.style.alignContent = None
        print(sometag.style.alignContent)

        sometag.style.backgroundColor = "black"
        sometag.style.fontSize = "12px"

        # huh = document.createAttribute("test")
        # huh.value = "wtf"
        # sometag.setAttributeNode(huh)
        print(sometag.style.fontSize)
        print(sometag)

        # dom.select('#test' ).dostuff() # TODO -
        # print(sometag.style)
        # print(sometag.tagName)
        # s = Style()
        # print(sometag)

    # create some failing tests

    # def test_css_style_declaration(self):
        # styleObj = document.styleSheets[0].cssRules[0].style
        # print(styleObj.cssText)

    # def test_css_style_rules(self):
        # myRules = document.styleSheets[0].cssRules # Returns a CSSRuleList
        # print(myRules)

        # myRules = document.styleSheets[0].cssRules
        # print(myRules[0]); # a CSSStyleRule representing the h1.

    #def test_css_styledpropertymap(self):
        # pass

    def test_paser(self):

        somecss = '''
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
        '''

        from domonic.style import CSSParser

        ss = CSSStyleSheet()
        p = CSSParser.parseFromString(ss, somecss)

        print("SHEET:", ss.rules)
        print("PARSER:", p)

        for r in p:
            print("bo:", r.selectorText)
            print(r.style.cssText)
            # print(r.style)
            # print(r.parentRule)

        cssStyleSheet: CSSStyleSheet = CSSStyleSheet()
        cssStyleSheet.insertRule('div { background-color: green }')
        cssStyleSheet.insertRule('span { background-color: green }')
        cssStyleSheet.insertRule('div { background-color: green }')

        # print(cssStyleSheet.cssRules)
        # print(cssStyleSheet.cssRules.length)
        # print(cssStyleSheet.cssRules[0].selectorText)
        # print(cssStyleSheet.cssRules[0].style.cssText)
        assert cssStyleSheet.cssRules.length == 3
        assert cssStyleSheet.cssRules[0].selectorText == 'div'
        assert cssStyleSheet.cssRules[0].style.cssText == 'background-color: green'

        # cssStyleSheet.insertRule('background-color: green');
        # DOMException('Invalid CSS rule.', DOMExceptionNameEnum.hierarchyRequestError)
        somecss = '''
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
        '''

        cssStyleSheet = CSSStyleSheet()
        cssRules = CSSParser.parseFromString(cssStyleSheet, somecss)

        assert len(cssRules) == 5

        # CSSStyleRule
        assert cssRules[0].parentRule == None
        assert cssRules[0].parentStyleSheet == cssStyleSheet
        assert cssRules[0].selectorText == ':host'
        print('>>>>>>>>>>>>>>>>>>>>>', cssRules[0].cssText)
        # assert cssRules[0].cssText == ':host { display: flex; overflow: hidden; width: 100%; }'
        assert cssRules[0].style.parentRule == cssRules[0]
        # assert cssRules[0].style.length == 3
        # assert cssRules[0].style[0] == 'display'
        # assert cssRules[0].style[1] == 'overflow'
        # assert cssRules[0].style[2] == 'width'
        # assert cssRules[0].style['display'] == 'flex'
        # assert cssRules[0].style['overflow'] == 'hidden'
        # assert cssRules[0].style['width'] == '100%'
        assert cssRules[0].style.cssText == 'display: flex; overflow: hidden; width: 100%;'

        # CSSStyleRule
        assert cssRules[1].parentRule == None
        assert cssRules[1].parentStyleSheet == cssStyleSheet
        assert cssRules[1].selectorText == '.container'
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
        assert cssRules[1].style.cssText == 'flex-grow: 1; display: flex; flex-direction: column; overflow: hidden;'

        # CSSMediaRule
        assert cssRules[2].parentRule == None
        assert cssRules[2].parentStyleSheet == cssStyleSheet
        assert cssRules[2].media.length == 1
        assert cssRules[2].media[0] == 'screen and (max-width: 36rem)'
        assert cssRules[2].media.mediaText == 'screen and (max-width: 36rem)'
        # assert cssRules[2].cssText == '@media screen and (max-width: 36rem) { .container { height: 0.5rem; animation: keyframes2 2s linear infinite; } }'
        # assert cssRules[2].cssRules.length == 1
        children1 = cssRules[2].cssRules
        assert children1[0].parentRule == cssRules[2]
        assert children1[0].parentStyleSheet == cssStyleSheet
        assert children1[0].selectorText == '.container'
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
        assert cssRules[3].name == 'keyframes1'
        print(cssRules[3].cssText)
        # assert cssRules[3].cssText == '@keyframes keyframes1 { from { transform: rotate(0deg); } to { transform: rotate(360deg); } }'
        # assert cssRules[3].cssRules.length == 2
        children2 = cssRules[3].cssRules
        assert children2[0].parentRule == cssRules[3]
        assert children2[0].parentStyleSheet == cssStyleSheet
        assert children2[0].keyText == 'from'
        # assert children2[0].style.length == 1
        assert children2[0].style.parentRule == children2[0]
        # assert children2[0].style[0] == 'transform'
        # assert children2[0].style['transform'] == 'rotate(0deg)'
        print(children2[0].cssText)
        # assert children2[0].cssText == 'from { transform: rotate(0deg); }'
        assert children2[1].parentRule == cssRules[3]
        assert children2[1].parentStyleSheet == cssStyleSheet
        assert children2[1].keyText == 'to'
        # assert children2[1].style.length == 1
        # assert children2[1].style[0] == 'transform'
        # assert children2[1].style['transform'] == 'rotate(360deg)'
        # assert children2[1].cssText == 'to { transform: rotate(360deg); }'

        # CSSKeyframesRule
        assert cssRules[4].parentRule == None
        assert cssRules[4].parentStyleSheet == cssStyleSheet
        assert cssRules[4].name == 'keyframes2'
        # assert cssRules[4].cssText == '@keyframes keyframes2 { 0% { transform: rotate(0deg); } 100% { transform: rotate(360deg); } }'
        # assert cssRules[4].cssRules.length == 2
        children3 = cssRules[4].cssRules
        assert children3[0].parentRule == cssRules[4]
        assert children3[0].parentStyleSheet == cssStyleSheet
        assert children3[0].keyText == '0%'
        # assert children3[0].style.length == 1
        assert children3[0].style.parentRule == children3[0]
        # assert children3[0].style[0] == 'transform'
        # assert children3[0].style['transform'] == 'rotate(0deg)'
        print(children3[0].cssText)
        # assert children3[0].cssText == '0% { transform: rotate(0deg); }'
        assert children3[1].parentRule == cssRules[4]
        assert children3[1].parentStyleSheet == cssStyleSheet
        assert children3[1].keyText == '100%'
        # assert children3[1].style.length == 1
        # assert children3[1].style[0] == 'transform'
        # assert children3[1].style['transform'] == 'rotate(360deg)'
        # assert children3[1].cssText == '100% { transform: rotate(360deg); }'


    def test_new_props(self):

        s = Style()
        s.all = 'border: 1px solid black;'
        assert s.all == 'border: 1px solid black;'

        s.alignmentBaseline = 'baseline'
        s.appearance = 'none'
        s.backdropFilter = 'blur(2px)'
        s.backgroundBlendMode = 'normal'
        s.backgroundPositionX = '0'
        s.backgroundPositionY = '0'
        s.backgroundRepeatX = 0
        s.backgroundRepeatY = 0
        s.baselineShift = '0'
        s.blockSize = '0'
        s.borderBlockEnd = '0'
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









if __name__ == '__main__':
    unittest.main()
