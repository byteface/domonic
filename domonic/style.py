# -*- coding: utf-8 -*-
"""
    domonic.style
    ~~~~~~~~~~~
"""


class Style(object):
    """[ js syntax styles ]
        # TODO - just add normal float?
        # TODO - consider camel case for hyphen params?
    """

    def __init__(self):

        self.alignContent = 'stretch'
        '''Sets or returns the alignment between the lines inside a flexible container when the items do not use all available space   3'''

        self.alignItems = None
        '''Sets or returns the alignment for items \
            inside a flexible container 3'''

        self.alignSelf = None
        '''Sets or returns the alignment for selected items inside a flexible container    3'''

        self.animation = None
        ''' shorthand property for all the animation properties below, except the animationPlayState property 3'''

        self.animationDelay = None
        '''Sets or returns when the animation will start   3'''

        self.animationDirection = None
        '''Sets or returns whether or not the animation should play in reverse on alternate cycles 3'''

        self.animationDuration = None
        '''Sets or returns how many seconds or milliseconds an animation takes to complete one cycle   3'''

        self.animationFillMode = None
        '''Sets or returns what values are applied by the animation outside the time it is executing   3'''

        self.animationIterationCount = None
        '''Sets or returns the number of times an animation should be played   3'''

        self.animationName = None
        '''Sets or returns a name for the @keyframes animation 3'''

        self.animationTimingFunction = None
        '''Sets or returns the speed curve of the animation    3'''

        self.animationPlayState = None
        '''Sets or returns whether the animation is running or paused  3'''

        self.background = None
        '''Sets or returns all the background properties in one declaration    1'''

        self.backgroundAttachment = None
        '''Sets or returns whether a background-image is fixed or scrolls with the page    1'''

        self.backgroundColor = None
        '''Sets or returns the background-color of an element  1'''

        self.backgroundImage = None
        '''Sets or returns the background-image for an element 1'''

        self.backgroundPosition = None
        '''Sets or returns the starting position of a background-image 1'''

        self.backgroundRepeat = None
        '''Sets or returns how to repeat (tile) a background-image 1'''

        self.backgroundClip = None
        '''Sets or returns the painting area of the background 3'''

        self.backgroundOrigin = None
        '''Sets or returns the positioning area of the background images   3'''

        self.backgroundSize = None
        '''Sets or returns the size of the background image    3'''

        self.backfaceVisibility = None
        '''Sets or returns whether or not an element should be visible when not facing the screen  3'''

        self.border = None
        '''Sets or returns borderWidth, borderStyle, and borderColor in one declaration    1'''

        self.borderBottom = None
        '''Sets or returns all the borderBottom properties in one declaration  1'''

        self.borderBottomColor = None
        '''Sets or returns the color of the bottom border  1 '''

        self.borderBottomLeftRadius = None
        '''Sets or returns the shape of the border of the bottom-left corner   3'''

        self.borderBottomRightRadius = None
        '''Sets or returns the shape of the border of the bottom-right corner  3'''

        self.borderBottomStyle = None
        '''Sets or returns the style of the bottom border  1'''

        self.borderBottomWidth = None
        '''Sets or returns the width of the bottom border  1'''

        self.borderCollapse = None
        '''Sets or returns whether the table border should be collapsed into a single border, or not   2'''

        self.borderColor = None
        '''Sets or returns the color of an element's border (can have up to four values)   1'''

        self.borderImage = None
        '''horthand property for setting or returning all the borderImage properties    3'''

        self.borderImageOutset = None
        '''Sets or returns the amount by which the border image area extends beyond the border box 3'''

        self.borderImageRepeat = None
        '''Sets or returns whether the image-border should be repeated, rounded or stretched   3'''

        self.borderImageSlice = None
        '''Sets or returns the inward offsets of the image-border  3'''

        self.borderImageSource = None
        '''Sets or returns the image to be used as a border    3'''

        self.borderImageWidth = None
        '''Sets or returns the widths of the image-border  3'''

        self.borderLeft = None
        '''Sets or returns all the borderLeft properties in one declaration    1'''

        self.borderLeftColor = None
        '''Sets or returns the color of the left border    1'''

        self.borderLeftStyle = None
        '''Sets or returns the style of the left border    1'''

        self.borderLeftWidth = None
        '''Sets or returns the width of the left border    1'''

        self.borderRadius = None
        '''A shorthand property for setting or returning all the four borderRadius properties  3'''

        self.borderRight = None
        '''Sets or returns all the borderRight properties in one declaration   1'''

        self.borderRightColor = None
        '''Sets or returns the color of the right border   1'''

        self.borderRightStyle = None
        '''Sets or returns the style of the right border   1'''

        self.borderRightWidth = None
        '''Sets or returns the width of the right border   1'''

        self.borderSpacing = None
        '''Sets or returns the space between cells in a table  2'''

        self.borderStyle = None
        '''Sets or returns the style of an element's border (can have up to four values)   1'''

        self.borderTop = None
        '''Sets or returns all the borderTop properties in one declaration 1'''

        self.borderTopColor = None
        '''Sets or returns the color of the top border 1'''

        self.borderTopLeftRadius = None
        '''Sets or returns the shape of the border of the top-left corner  3'''

        self.borderTopRightRadius = None
        '''Sets or returns the shape of the border of the top-right corner 3'''

        self.borderTopStyle = None
        '''Sets or returns the style of the top border 1'''

        self.borderTopWidth = None
        '''Sets or returns the width of the top border 1'''

        self.borderWidth = None
        '''Sets or returns the width of an element's border (can have up to four values)   1'''

        self.bottom = None
        '''Sets or returns the bottom position of a positioned element 2'''

        self.boxDecorationBreak = None
        '''Sets or returns the behaviour of the background and border of an element at page-break, or, for in-line elements, at line-break.    3'''

        self.boxShadow = None
        '''ttaches one or more drop-shadows to the box    3'''

        self.boxSizing = None
        '''llows you to define certain elements to fit an area in a certain way   3'''

        self.captionSide = None
        '''Sets or returns the position of the table caption   2'''

        self.clear = None
        '''Sets or returns the position of the element relative to floating objects    1'''

        self.clip = None
        '''Sets or returns which part of a positioned element is visible   2'''

        self.color = None
        '''Sets or returns the color of the text   1'''

        self.columnCount = None
        '''Sets or returns the number of columns an element should be divided into 3'''

        self.columnFill = None
        '''Sets or returns how to fill columns 3'''

        self.columnGap = None
        '''Sets or returns the gap between the columns 3'''

        self.columnRule = None
        '''shorthand property for setting or returning all the columnRule properties 3'''

        self.columnRuleColor = None
        '''Sets or returns the color of the rule between columns   3'''

        self.columnRuleStyle = None
        '''Sets or returns the style of the rule between columns   3'''

        self.columnRuleWidth = None
        '''Sets or returns the width of the rule between columns   3'''

        self.columns = None
        '''horthand property for setting or returning columnWidth and columnCount   3'''

        self.columnSpan = None
        '''Sets or returns how many columns an element should span across  3'''

        self.columnWidth = None
        '''Sets or returns the width of the columns    3'''

        self.content = None
        '''d with the :before and :after pseudo-elements, to insert generated content   2'''

        self.counterIncrement = None
        '''Increments one or more counters 2'''

        self.counterReset = None
        '''Creates or resets one or more counters  2'''

        self.cursor = None
        '''Sets or returns the type of cursor to display for the mouse pointer 2'''

        self.direction = None
        '''Sets or returns the text direction  2'''

        self.display = None
        '''Sets or returns an element's display type   1'''

        self.emptyCells = None
        '''Sets or returns whether to show the border and background of empty cells, or not    2'''

        self.filter = None
        '''Sets or returns image filters (visual effects, like blur and saturation)    3'''

        self.flex = None
        '''Sets or returns the length of the item, relative to the rest    3'''

        self.flexBasis = None
        '''Sets or returns the initial length of a flexible item   3'''

        self.flexDirection = None
        '''Sets or returns the direction of the flexible items 3'''

        self.flexFlow = None
        '''A shorthand property for the flexDirection and the flexWrap properties  3'''

        self.flexGrow = None
        '''Sets or returns how much the item will grow relative to the rest    3'''

        self.flexShrink = None
        '''Sets or returns how the item will shrink relative to the rest   3'''

        self.flexWrap = None
        '''Sets or returns whether the flexible items should wrap or not   3'''

        self.cssFloat = None
        '''Sets or returns the horizontal alignment of an element  1'''

        self.font = None
        '''Sets or returns fontStyle, fontVariant, fontWeight, fontSize, lineHeight, and fontFamily in one declaration 1'''

        self.fontFamily = None
        '''Sets or returns the font family for text    1'''

        self.fontSize = None
        '''Sets or returns the font size of the text   1'''

        self.fontStyle = None
        '''Sets or returns whether the style of the font is normal, italic or oblique  1'''

        self.fontVariant = None
        '''Sets or returns whether the font should be displayed in small capital letters   1'''

        self.fontWeight = None
        '''Sets or returns the boldness of the font    1'''

        self.fontSizeAdjust = None
        '''eserves the readability of text when font fallback occurs 3'''

        self.fontStretch = None
        '''ects a normal, condensed, or expanded face from a font family    3'''

        self.hangingPunctuation = None
        '''ecifies whether a punctuation character may be placed outside the line box    3'''

        self.height = None
        '''Sets or returns the height of an element    1'''

        self.hyphens = None
        '''Sets how to split words to improve the layout of paragraphs 3'''

        self.icon = None
        '''Provides the author the ability to style an element with an iconic equivalent   3'''

        self.imageOrientation = None
        '''Specifies a rotation in the right or clockwise direction that a user agent applies to an image  3'''

        self.isolation = None
        '''efines whether an element must create a new stacking content   3'''

        self.justifyContent = None
        '''Sets or returns the alignment between the items inside a flexible container when the items do not use all available space.  3'''

        self.left = None
        '''Sets or returns the left position of a positioned element   2'''

        self.letterSpacing = None
        '''Sets or returns the space between characters in a text  1'''

        self.lineHeight = None
        '''Sets or returns the distance between lines in a text    1'''

        self.listStyle = None
        '''Sets or returns listStyleImage, listStylePosition, and listStyleType in one declaration 1'''

        self.listStyleImage = None
        '''Sets or returns an image as the list-item marker    1'''

        self.listStylePosition = None
        '''Sets or returns the position of the list-item marker    1'''

        self.listStyleType = None
        '''Sets or returns the list-item marker type   1'''

        self.margin = None
        '''Sets or returns the margins of an element (can have up to four values)  1'''

        self.marginBottom = None
        '''Sets or returns the bottom margin of an element 1'''

        self.marginLeft = None
        '''Sets or returns the left margin of an element   1'''

        self.marginRight = None
        '''Sets or returns the right margin of an element  1'''

        self.marginTop = None
        '''Sets or returns the top margin of an element    1'''

        self.maxHeight = None
        '''Sets or returns the maximum height of an element    2'''

        self.maxWidth = None
        '''Sets or returns the maximum width of an element 2'''

        self.minHeight = None
        '''Sets or returns the minimum height of an element    2'''

        self.minWidth = None
        '''Sets or returns the minimum width of an element 2'''

        self.navDown = None
        '''Sets or returns where to navigate when using the arrow-down navigation key  3'''

        self.navIndex = None
        '''Sets or returns the tabbing order for an element    3'''

        self.navLeft = None
        '''Sets or returns where to navigate when using the arrow-left navigation key  3'''

        self.navRight = None
        '''Sets or returns where to navigate when using the arrow-right navigation key 3'''

        self.navUp = None
        '''Sets or returns where to navigate when using the arrow-up navigation key    3'''

        self.objectFit = None
        '''pecifies how the contents of a replaced element should be fitted to the box established by its used height and width   3'''

        self.objectPosition = None
        '''ecifies the alignment of the replaced element inside its box  3'''

        self.opacity = None
        '''Sets or returns the opacity level for an element    3'''

        self.order = None
        '''Sets or returns the order of the flexible item, relative to the rest    3'''

        self.orphans = None
        '''Sets or returns the minimum number of lines for an element that must be left at the bottom of a page when a page break occurs inside an element 2'''

        self.outline = None
        '''Sets or returns all the outline properties in one declaration   2'''

        self.outlineColor = None
        '''Sets or returns the color of the outline around a element   2'''

        self.outlineOffset = None
        '''ffsets an outline, and draws it beyond the border edge 3'''

        self.outlineStyle = None
        '''Sets or returns the style of the outline around an element  2'''

        self.outlineWidth = None
        '''Sets or returns the width of the outline around an element  2'''

        self.overflow = None
        '''Sets or returns what to do with content that renders outside the element box    2'''

        self.overflowX = None
        '''pecifies what to do with the left/right edges of the content, if it overflows the element's content area   3'''

        self.overflowY = None
        '''pecifies what to do with the top/bottom edges of the content, if it overflows the element's content area   3'''

        self.padding = None
        '''Sets or returns the padding of an element (can have up to four values)  1'''

        self.paddingBottom = None
        '''Sets or returns the bottom padding of an element    1'''

        self.paddingLeft = None
        '''Sets or returns the left padding of an element  1'''

        self.paddingRight = None
        '''Sets or returns the right padding of an element 1'''

        self.paddingTop = None
        '''Sets or returns the top padding of an element   1'''

        self.pageBreakAfter = None
        '''Sets or returns the page-break behavior after an element    2'''

        self.pageBreakBefore = None
        '''Sets or returns the page-break behavior before an element   2'''

        self.pageBreakInside = None
        '''Sets or returns the page-break behavior inside an element   2'''

        self.perspective = None
        '''Sets or returns the perspective on how 3D elements are viewed   3'''

        self.perspectiveOrigin = None
        '''Sets or returns the bottom position of 3D elements  3'''

        self.position = None
        '''Sets or returns the type of positioning method used for an element (static, relative, absolute or fixed)    2'''

        self.quotes = None
        '''Sets or returns the type of quotation marks for embedded quotations 2'''

        self.resize = None
        '''Sets or returns whether or not an element is resizable by the user  3'''

        self.right = None
        '''Sets or returns the right position of a positioned element  2'''

        self.tableLayout = None
        '''Sets or returns the way to lay out table cells, rows, and columns   2'''

        self.tabSize = None
        '''Sets or returns the length of the tab-character 3'''

        self.textAlign = None
        '''Sets or returns the horizontal alignment of text    1'''

        self.textAlignLast = None
        '''Sets or returns how the last line of a block or a line right before a forced line break is aligned when text-align is "justify" 3'''

        self.textDecoration = None
        '''Sets or returns the decoration of a text    1'''

        self.textDecorationColor = None
        '''Sets or returns the color of the text-decoration    3'''

        self.textDecorationLine = None
        '''Sets or returns the type of line in a text-decoration   3'''

        self.textDecorationStyle = None
        '''Sets or returns the style of the line in a text decoration  3'''

        self.textIndent = None
        '''Sets or returns the indentation of the first line of text   1'''

        self.textJustify = None
        '''Sets or returns the justification method used when text-align is "justify"  3'''

        self.textOverflow = None
        '''Sets or returns what should happen when text overflows the containing element   3'''

        self.textShadow = None
        '''Sets or returns the shadow effect of a text 3'''

        self.textTransform = None
        '''Sets or returns the capitalization of a text    1'''

        self.top = None
        '''Sets or returns the top position of a positioned element    2'''

        self.transform = None
        '''pplies a 2D or 3D transformation to an element 3'''

        self.transformOrigin = None
        '''Sets or returns the position of transformed elements    3'''

        self.transformStyle = None
        '''Sets or returns how nested elements are rendered in 3D space    3'''

        self.transition = None
        '''shorthand property for setting or returning the four transition properties    3'''

        self.transitionProperty = None
        '''Sets or returns the CSS property that the transition effect is for  3'''

        self.transitionDuration = None
        '''Sets or returns how many seconds or milliseconds a transition effect takes to complete  3'''

        self.transitionTimingFunction = None
        '''Sets or returns the speed curve of the transition effect    3'''

        self.transitionDelay = None
        '''Sets or returns when the transition effect will start   3'''

        self.unicodeBidi = None
        '''Sets or returns whether the text should be overridden to support multiple languages in the same document    2'''

        self.userSelect = None
        '''Sets or returns whether the text of an element can be selected or not   2'''

        self.verticalAlign = None
        '''Sets or returns the vertical alignment of the content in an element 1'''

        self.visibility = None
        '''Sets or returns whether an element should be visible 2'''

        self.whiteSpace = None
        """[Sets or returns how to handle tabs, line breaks and whitespace in a text 1]
        """

        self.width = None
        '''Sets or returns the width of an element 1'''

        self.wordBreak = None
        '''Sets or returns line breaking rules for non-CJK scripts 3'''

        self.wordSpacing = None
        '''Sets or returns the spacing between words in a text 1'''

        self.wordWrap = None
        '''Allows long, unbreakable words to be broken and wrap to the next line   3'''

        self.widows = None
        '''Sets or returns the minimum number of lines for an element that must be visible at the top of a page    2'''

        self.zIndex = None
        '''Sets or returns the stack order of a positioned element 2'''

    # def render_style(): # thinking if a style gets set. it could call this and force render the style tag with that prop?

    def style_set_decorator(func):
        def style_wrapper(value=None, *args, **kwargs):
            if value is None:
                value = 'none'
            func(value, *args, **kwargs)
        return style_wrapper

    def style_get_decorator(func):
        def style_wrapper(value=None, *args, **kwargs):
            value = func(value, *args, **kwargs)
            if value is None:
                value = 'none'
            return value
        return style_wrapper

    @property
    # TODO - pass array of valid words as params. so can raise value errors
    @style_get_decorator
    def alignContent(self):
        return self.__alignContent

    @alignContent.setter
    @style_get_decorator
    def alignContent(self, value='stretch'):
        self.__alignContent = value
