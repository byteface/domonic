"""
    domonic.style
    ====================================
"""

from .utils import Utils


class Style(object):
    """[ js syntax styles ]
        # TODO - just add normal float?
        # TODO - consider camel case for hyphen params?
        # TODO - not json serialisable due to the decorators.
    """

    def __init__(self, parent_node=None):

        self._members_checked = 0

        self._parent_node = parent_node  # so I can update a tags returned style attributes if a style gets set

        self.alignContent = 'normal'
        '''Sets or returns the alignment between the lines inside a flexible container when the items do not use all available space   3'''

        self.alignItems = 'normal'
        '''Sets or returns the alignment for items inside a flexible container 3'''

        self.alignSelf = 'auto'
        '''Sets or returns the alignment for selected items inside a flexible container    3'''

        self.animation = 'normal'
        ''' shorthand property for all the animation properties below, except the animationPlayState property 3'''

        self.animationDelay = 0
        '''Sets or returns when the animation will start   3'''

        self.animationDirection = 'normal'
        '''Sets or returns whether or not the animation should play in reverse on alternate cycles 3'''

        self.animationDuration = 0
        '''Sets or returns how many seconds or milliseconds an animation takes to complete one cycle   3'''

        self.animationFillMode = None
        '''Sets or returns what values are applied by the animation outside the time it is executing   3'''

        self.animationIterationCount = 1
        '''Sets or returns the number of times an animation should be played   3'''

        self.animationName = None
        '''Sets or returns a name for the @keyframes animation 3'''

        self.animationTimingFunction = 'ease'
        '''Sets or returns the speed curve of the animation    3'''

        self.animationPlayState = 'running'
        '''Sets or returns whether the animation is running or paused  3'''

        self.background = None
        '''Sets or returns all the background properties in one declaration    1'''

        self.backgroundAttachment = 'scroll'
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

        self.border = 'medium none black'
        '''Sets or returns borderWidth, borderStyle, and borderColor in one declaration    1'''

        self.borderBottom = 'medium none black'
        '''Sets or returns all the borderBottom properties in one declaration  1'''

        self.borderBottomColor = None
        '''Sets or returns the color of the bottom border  1 '''

        self.borderBottomLeftRadius = 0
        '''Sets or returns the shape of the border of the bottom-left corner   3'''

        self.borderBottomRightRadius = 0
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

        self.borderRadius = 0
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

        self.borderTopLeftRadius = 0
        '''Sets or returns the shape of the border of the top-left corner  3'''

        self.borderTopRightRadius = 0
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

        self.columnGap = 'normal'
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

        self.float = None  # ADDED BY ME

        self.cssFloat = None
        '''Sets or returns the horizontal alignment of an element  1'''

        self.font = None
        '''Sets or returns fontStyle, fontVariant, fontWeight, fontSize, lineHeight, and fontFamily in one declaration 1'''

        self.fontFamily = None
        '''Sets or returns the font family for text    1'''

        self.fontSize = 'medium'
        '''Sets or returns the font size of the text   1'''

        self.fontStyle = 'normal'
        '''Sets or returns whether the style of the font is normal, italic or oblique  1'''

        self.fontVariant = None
        '''Sets or returns whether the font should be displayed in small capital letters   1'''

        self.fontWeight = 'normal'
        '''Sets or returns the boldness of the font    1'''

        self.fontSizeAdjust = None
        '''eserves the readability of text when font fallback occurs 3'''

        self.fontStretch = None
        '''ects a normal, condensed, or expanded face from a font family    3'''

        self.hangingPunctuation = None
        '''ecifies whether a punctuation character may be placed outside the line box    3'''

        self.height = 'auto'
        '''Sets or returns the height of an element    1'''

        self.hyphens = None
        '''Sets how to split words to improve the layout of paragraphs 3'''

        self.icon = None
        '''Provides the author the ability to style an element with an iconic equivalent   3'''

        self.imageOrientation = None
        '''Specifies a rotation in the right or clockwise direction that a user agent applies to an image  3'''

        self.isolation = None
        '''efines whether an element must create a new stacking content   3'''

        self.justifyContent = 'normal'
        '''Sets or returns the alignment between the items inside a flexible container when the items do not use all available space.  3'''

        self.left = 'auto'
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

        self.margin = 0
        '''Sets or returns the margins of an element (can have up to four values)  1'''

        self.marginBottom = 0
        '''Sets or returns the bottom margin of an element 1'''

        self.marginLeft = 0
        '''Sets or returns the left margin of an element   1'''

        self.marginRight = 0
        '''Sets or returns the right margin of an element  1'''

        self.marginTop = 0
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

        self.overflow = 'visible'
        '''Sets or returns what to do with content that renders outside the element box    2'''

        self.overflowX = None
        '''pecifies what to do with the left/right edges of the content, if it overflows the element's content area   3'''

        self.overflowY = None
        '''pecifies what to do with the top/bottom edges of the content, if it overflows the element's content area   3'''

        self.padding = 0
        '''Sets or returns the padding of an element (can have up to four values)  1'''

        self.paddingBottom = 0
        '''Sets or returns the bottom padding of an element    1'''

        self.paddingLeft = 0
        '''Sets or returns the left padding of an element  1'''

        self.paddingRight = 0
        '''Sets or returns the right padding of an element 1'''

        self.paddingTop = 0
        '''Sets or returns the top padding of an element   1'''

        self.pageBreakAfter = 'auto'
        '''Sets or returns the page-break behavior after an element    2'''

        self.pageBreakBefore = 'auto'
        '''Sets or returns the page-break behavior before an element   2'''

        self.pageBreakInside = 'auto'
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

        self.right = 'auto'
        '''Sets or returns the right position of a positioned element  2'''

        self.tableLayout = 'auto'
        '''Sets or returns the way to lay out table cells, rows, and columns   2'''

        self.tabSize = None
        '''Sets or returns the length of the tab-character 3'''

        self.textAlign = 'left'
        '''Sets or returns the horizontal alignment of text    1'''

        self.textAlignLast = 'auto'
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

        self.textOverflow = 'clip'
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

        self.transitionDuration = 0
        '''Sets or returns how many seconds or milliseconds a transition effect takes to complete  3'''

        self.transitionTimingFunction = None
        '''Sets or returns the speed curve of the transition effect    3'''

        self.transitionDelay = 0
        '''Sets or returns when the transition effect will start   3'''

        self.unicodeBidi = None
        '''Sets or returns whether the text should be overridden to support multiple languages in the same document    2'''

        self.userSelect = None
        '''Sets or returns whether the text of an element can be selected or not   2'''

        self.verticalAlign = None
        '''Sets or returns the vertical alignment of the content in an element 1'''

        self.visibility = 'visible'
        '''Sets or returns whether an element should be visible 2'''

        self.whiteSpace = 'normal'
        """ Sets or returns how to handle tabs, line breaks and whitespace in a text 1 """

        self.width = 'auto'
        '''Sets or returns the width of an element 1'''

        self.wordBreak = 'normal'
        '''Sets or returns line breaking rules for non-CJK scripts 3'''

        self.wordSpacing = None
        '''Sets or returns the spacing between words in a text 1'''

        self.wordWrap = 'normal'
        '''Allows long, unbreakable words to be broken and wrap to the next line   3'''

        self.widows = None
        '''Sets or returns the minimum number of lines for an element that must be visible at the top of a page    2'''

        self.zIndex = 'auto'
        '''Sets or returns the stack order of a positioned element 2'''

    def style_set_decorator(func):
        from functools import wraps
        @wraps(func)
        def style_wrapper(self, *args, **kwargs):
            value = args[0]
            if value is None:
                value = 'none'
            func(self, value, *args, **kwargs)

            self._members_checked += 1
            if self._members_checked < len(vars(self)) - 1:
                return

            if self._parent_node is not None:
                s = f'{Utils.case_kebab(func.__name__)}:{value};'
                styles = self._parent_node.getAttribute('style')
                # print('sup:', styles)

                if styles is not None:
                    # TODO - replace if exists
                    styles = styles + s
                else:
                    styles = s

                # print(styles)
                self._parent_node.setAttribute("style", styles)

        return style_wrapper

    def style_get_decorator(func):
        from functools import wraps
        @wraps(func)
        def style_wrapper(value=None, *args, **kwargs):
            value = func(value, *args, **kwargs)
            if value is None:
                value = 'none'
            return value
        return style_wrapper

    @property
    @style_get_decorator # TODO - pass array of valid words as params. so can raise value errors
    def alignContent(self):
        return self.__alignContent

    @alignContent.setter
    @style_set_decorator
    def alignContent(self, value='stretch', *args, **kwargs):
        self.__alignContent = value

    @property
    @style_get_decorator
    def alignItems(self):
        return self.__alignItems

    @alignItems.setter
    @style_set_decorator
    def alignItems(self, value=None, *args, **kwargs):
        self.__alignItems = value

    @property
    @style_get_decorator
    def alignSelf(self):
        return self.__alignSelf

    @alignSelf.setter
    @style_set_decorator
    def alignSelf(self, value=None, *args, **kwargs):
        self.__alignSelf = value

    @property
    @style_get_decorator
    def animation(self):
        return self.__animation

    @animation.setter
    @style_set_decorator
    def animation(self, value=None, *args, **kwargs):
        self.__animation = value

    @property
    @style_get_decorator
    def animationDelay(self):
        return self.__animationDelay

    @animationDelay.setter
    @style_set_decorator
    def animationDelay(self, value=None, *args, **kwargs):
        self.__animationDelay = value

    @property
    @style_get_decorator
    def animationDirection(self):
        return self.__animationDirection

    @animationDirection.setter
    @style_set_decorator
    def animationDirection(self, value=None, *args, **kwargs):
        self.__animationDirection = value

    @property
    @style_get_decorator
    def animationDuration(self):
        return self.__animationDuration

    @animationDuration.setter
    @style_set_decorator
    def animationDuration(self, value=None, *args, **kwargs):
        self.__animationDuration = value

    @property
    @style_get_decorator
    def animationFillMode(self):
        return self.__animationFillMode

    @animationFillMode.setter
    @style_set_decorator
    def animationFillMode(self, value=None, *args, **kwargs):
        self.__animationFillMode = value

    @property
    @style_get_decorator
    def animationIterationCount(self):
        return self.__animationIterationCount

    @animationIterationCount.setter
    @style_set_decorator
    def animationIterationCount(self, value=None, *args, **kwargs):
        self.__animationIterationCount = value

    @property
    @style_get_decorator
    def animationName(self):
        return self.__animationName

    @animationName.setter
    @style_set_decorator
    def animationName(self, value=None, *args, **kwargs):
        self.__animationName = value

    @property
    @style_get_decorator
    def animationTimingFunction(self):
        return self.__animationTimingFunction

    @animationTimingFunction.setter
    @style_set_decorator
    def animationTimingFunction(self, value=None, *args, **kwargs):
        self.__animationTimingFunction = value

    @property
    @style_get_decorator
    def animationPlayState(self):
        return self.__animationPlayState

    @animationPlayState.setter
    @style_set_decorator
    def animationPlayState(self, value=None, *args, **kwargs):
        self.__animationPlayState = value

    @property
    @style_get_decorator
    def background(self):
        return self.__background

    @background.setter
    @style_set_decorator
    def background(self, value=None, *args, **kwargs):
        self.__background = value

    @property
    @style_get_decorator
    def backgroundAttachment(self):
        return self.__backgroundAttachment

    @backgroundAttachment.setter
    @style_set_decorator
    def backgroundAttachment(self, value=None, *args, **kwargs):
        self.__backgroundAttachment = value

    @property
    @style_get_decorator
    def backgroundColor(self):
        return self.__backgroundColor

    @backgroundColor.setter
    @style_set_decorator
    def backgroundColor(self, value=None, *args, **kwargs):
        self.__backgroundColor = value

    @property
    @style_get_decorator
    def backgroundImage(self):
        return self.__backgroundImage

    @backgroundImage.setter
    @style_set_decorator
    def backgroundImage(self, value=None, *args, **kwargs):
        self.__backgroundImage = value

    @property
    @style_get_decorator
    def backgroundPosition(self):
        return self.__backgroundPosition

    @backgroundPosition.setter
    @style_set_decorator
    def backgroundPosition(self, value=None, *args, **kwargs):
        self.__backgroundPosition = value

    @property
    @style_get_decorator
    def backgroundRepeat(self):
        return self.__backgroundRepeat

    @backgroundRepeat.setter
    @style_set_decorator
    def backgroundRepeat(self, value=None, *args, **kwargs):
        self.__backgroundRepeat = value

    @property
    @style_get_decorator
    def backgroundClip(self):
        return self.__backgroundClip

    @backgroundClip.setter
    @style_set_decorator
    def backgroundClip(self, value=None, *args, **kwargs):
        self.__backgroundClip = value

    @property
    @style_get_decorator
    def backgroundOrigin(self):
        return self.__backgroundOrigin

    @backgroundOrigin.setter
    @style_set_decorator
    def backgroundOrigin(self, value=None, *args, **kwargs):
        self.__backgroundOrigin = value

    @property
    @style_get_decorator
    def backgroundSize(self):
        return self.__backgroundSize

    @backgroundSize.setter
    @style_set_decorator
    def backgroundSize(self, value=None, *args, **kwargs):
        self.__backgroundSize = value

    @property
    @style_get_decorator
    def backfaceVisibility(self):
        return self.__backfaceVisibility

    @backfaceVisibility.setter
    @style_set_decorator
    def backfaceVisibility(self, value=None, *args, **kwargs):
        self.__backfaceVisibility = value

    @property
    @style_get_decorator
    def border(self):
        return self.__border

    @border.setter
    @style_set_decorator
    def border(self, value=None, *args, **kwargs):
        self.__border = value

    @property
    @style_get_decorator
    def borderBottom(self):
        return self.__borderBottom

    @borderBottom.setter
    @style_set_decorator
    def borderBottom(self, value=None, *args, **kwargs):
        self.__borderBottom = value

    @property
    @style_get_decorator
    def borderBottomColor(self):
        return self.__borderBottomColor

    @borderBottomColor.setter
    @style_set_decorator
    def borderBottomColor(self, value=None, *args, **kwargs):
        self.__borderBottomColor = value

    @property
    @style_get_decorator
    def borderBottomLeftRadius(self):
        return self.__borderBottomLeftRadius

    @borderBottomLeftRadius.setter
    @style_set_decorator
    def borderBottomLeftRadius(self, value=None, *args, **kwargs):
        self.__borderBottomLeftRadius = value

    @property
    @style_get_decorator
    def borderBottomRightRadius(self):
        return self.__borderBottomRightRadius

    @borderBottomRightRadius.setter
    @style_set_decorator
    def borderBottomRightRadius(self, value=None, *args, **kwargs):
        self.__borderBottomRightRadius = value

    @property
    @style_get_decorator
    def borderBottomStyle(self):
        return self.__borderBottomStyle

    @borderBottomStyle.setter
    @style_set_decorator
    def borderBottomStyle(self, value=None, *args, **kwargs):
        self.__borderBottomStyle = value

    @property
    @style_get_decorator
    def borderBottomWidth(self):
        return self.__borderBottomWidth

    @borderBottomWidth.setter
    @style_set_decorator
    def borderBottomWidth(self, value=None, *args, **kwargs):
        self.__borderBottomWidth = value

    @property
    @style_get_decorator
    def borderCollapse(self):
        return self.__borderCollapse

    @borderCollapse.setter
    @style_set_decorator
    def borderCollapse(self, value=None, *args, **kwargs):
        self.__borderCollapse = value

    @property
    @style_get_decorator
    def borderColor(self):
        return self.__borderColor

    @borderColor.setter
    @style_set_decorator
    def borderColor(self, value=None, *args, **kwargs):
        self.__borderColor = value

    @property
    @style_get_decorator
    def borderImage(self):
        return self.__borderImage

    @borderImage.setter
    @style_set_decorator
    def borderImage(self, value=None, *args, **kwargs):
        self.__borderImage = value

    @property
    @style_get_decorator
    def borderImageOutset(self):
        return self.__borderImageOutset

    @borderImageOutset.setter
    @style_set_decorator
    def borderImageOutset(self, value=None, *args, **kwargs):
        self.__borderImageOutset = value

    @property
    @style_get_decorator
    def borderImageRepeat(self):
        return self.__borderImageRepeat

    @borderImageRepeat.setter
    @style_set_decorator
    def borderImageRepeat(self, value=None, *args, **kwargs):
        self.__borderImageRepeat = value

    @property
    @style_get_decorator
    def borderImageSlice(self):
        return self.__borderImageSlice

    @borderImageSlice.setter
    @style_set_decorator
    def borderImageSlice(self, value=None, *args, **kwargs):
        self.__borderImageSlice = value

    @property
    @style_get_decorator
    def borderImageSource(self):
        return self.__borderImageSource

    @borderImageSource.setter
    @style_set_decorator
    def borderImageSource(self, value=None, *args, **kwargs):
        self.__borderImageSource = value

    @property
    @style_get_decorator
    def borderImageWidth(self):
        return self.__borderImageWidth

    @borderImageWidth.setter
    @style_set_decorator
    def borderImageWidth(self, value=None, *args, **kwargs):
        self.__borderImageWidth = value

    @property
    @style_get_decorator
    def borderLeft(self):
        return self.__borderLeft

    @borderLeft.setter
    @style_set_decorator
    def borderLeft(self, value=None, *args, **kwargs):
        self.__borderLeft = value

    @property
    @style_get_decorator
    def borderLeftColor(self):
        return self.__borderLeftColor

    @borderLeftColor.setter
    @style_set_decorator
    def borderLeftColor(self, value=None, *args, **kwargs):
        self.__borderLeftColor = value

    @property
    @style_get_decorator
    def borderLeftStyle(self):
        return self.__borderLeftStyle

    @borderLeftStyle.setter
    @style_set_decorator
    def borderLeftStyle(self, value=None, *args, **kwargs):
        self.__borderLeftStyle = value

    @property
    @style_get_decorator
    def borderLeftWidth(self):
        return self.__borderLeftWidth

    @borderLeftWidth.setter
    @style_set_decorator
    def borderLeftWidth(self, value=None, *args, **kwargs):
        self.__borderLeftWidth = value

    @property
    @style_get_decorator
    def borderRadius(self):
        return self.__borderRadius

    @borderRadius.setter
    @style_set_decorator
    def borderRadius(self, value=None, *args, **kwargs):
        self.__borderRadius = value

    @property
    @style_get_decorator
    def borderRight(self):
        return self.__borderRight

    @borderRight.setter
    @style_set_decorator
    def borderRight(self, value=None, *args, **kwargs):
        self.__borderRight = value

    @property
    @style_get_decorator
    def borderRightColor(self):
        return self.__borderRightColor

    @borderRightColor.setter
    @style_set_decorator
    def borderRightColor(self, value=None, *args, **kwargs):
        self.__borderRightColor = value

    @property
    @style_get_decorator
    def borderRightStyle(self):
        return self.__borderRightStyle

    @borderRightStyle.setter
    @style_set_decorator
    def borderRightStyle(self, value=None, *args, **kwargs):
        self.__borderRightStyle = value

    @property
    @style_get_decorator
    def borderRightWidth(self):
        return self.__borderRightWidth

    @borderRightWidth.setter
    @style_set_decorator
    def borderRightWidth(self, value=None, *args, **kwargs):
        self.__borderRightWidth = value

    @property
    @style_get_decorator
    def borderSpacing(self):
        return self.__borderSpacing

    @borderSpacing.setter
    @style_set_decorator
    def borderSpacing(self, value=None, *args, **kwargs):
        self.__borderSpacing = value

    @property
    @style_get_decorator
    def borderStyle(self):
        return self.__borderStyle

    @borderStyle.setter
    @style_set_decorator
    def borderStyle(self, value=None, *args, **kwargs):
        self.__borderStyle = value

    @property
    @style_get_decorator
    def borderTop(self):
        return self.__borderTop

    @borderTop.setter
    @style_set_decorator
    def borderTop(self, value=None, *args, **kwargs):
        self.__borderTop = value

    @property
    @style_get_decorator
    def borderTopColor(self):
        return self.__borderTopColor

    @borderTopColor.setter
    @style_set_decorator
    def borderTopColor(self, value=None, *args, **kwargs):
        self.__borderTopColor = value

    @property
    @style_get_decorator
    def borderTopLeftRadius(self):
        return self.__borderTopLeftRadius

    @borderTopLeftRadius.setter
    @style_set_decorator
    def borderTopLeftRadius(self, value=None, *args, **kwargs):
        self.__borderTopLeftRadius = value

    @property
    @style_get_decorator
    def borderTopRightRadius(self):
        return self.__borderTopRightRadius

    @borderTopRightRadius.setter
    @style_set_decorator
    def borderTopRightRadius(self, value=None, *args, **kwargs):
        self.__borderTopRightRadius = value

    @property
    @style_get_decorator
    def borderTopStyle(self):
        return self.__borderTopStyle

    @borderTopStyle.setter
    @style_set_decorator
    def borderTopStyle(self, value=None, *args, **kwargs):
        self.__borderTopStyle = value

    @property
    @style_get_decorator
    def borderTopWidth(self):
        return self.__borderTopWidth

    @borderTopWidth.setter
    @style_set_decorator
    def borderTopWidth(self, value=None, *args, **kwargs):
        self.__borderTopWidth = value

    @property
    @style_get_decorator
    def borderWidth(self):
        return self.__borderWidth

    @borderWidth.setter
    @style_set_decorator
    def borderWidth(self, value=None, *args, **kwargs):
        self.__borderWidth = value

    @property
    @style_get_decorator
    def bottom(self):
        return self.__bottom

    @bottom.setter
    @style_set_decorator
    def bottom(self, value=None, *args, **kwargs):
        self.__bottom = value

    @property
    @style_get_decorator
    def boxDecorationBreak(self):
        return self.__boxDecorationBreak

    @boxDecorationBreak.setter
    @style_set_decorator
    def boxDecorationBreak(self, value=None, *args, **kwargs):
        self.__boxDecorationBreak = value

    @property
    @style_get_decorator
    def boxShadow(self):
        return self.__boxShadow

    @boxShadow.setter
    @style_set_decorator
    def boxShadow(self, value=None, *args, **kwargs):
        self.__boxShadow = value

    @property
    @style_get_decorator
    def boxSizing(self):
        return self.__boxSizing

    @boxSizing.setter
    @style_set_decorator
    def boxSizing(self, value=None, *args, **kwargs):
        self.__boxSizing = value

    @property
    @style_get_decorator
    def captionSide(self):
        return self.__captionSide

    @captionSide.setter
    @style_set_decorator
    def captionSide(self, value=None, *args, **kwargs):
        self.__captionSide = value

    @property
    @style_get_decorator
    def clear(self):
        return self.__clear

    @clear.setter
    @style_set_decorator
    def clear(self, value=None, *args, **kwargs):
        self.__clear = value

    @property
    @style_get_decorator
    def clip(self):
        return self.__clip

    @clip.setter
    @style_set_decorator
    def clip(self, value=None, *args, **kwargs):
        self.__clip = value

    @property
    @style_get_decorator
    def color(self):
        return self.__color

    @color.setter
    @style_set_decorator
    def color(self, value=None, *args, **kwargs):
        self.__color = value

    @property
    @style_get_decorator
    def columnCount(self):
        return self.__columnCount

    @columnCount.setter
    @style_set_decorator
    def columnCount(self, value=None, *args, **kwargs):
        self.__columnCount = value

    @property
    @style_get_decorator
    def columnFill(self):
        return self.__columnFill

    @columnFill.setter
    @style_set_decorator
    def columnFill(self, value=None, *args, **kwargs):
        self.__columnFill = value

    @property
    @style_get_decorator
    def columnGap(self):
        return self.__columnGap

    @columnGap.setter
    @style_set_decorator
    def columnGap(self, value=None, *args, **kwargs):
        self.__columnGap = value

    @property
    @style_get_decorator
    def columnRule(self):
        return self.__columnRule

    @columnRule.setter
    @style_set_decorator
    def columnRule(self, value=None, *args, **kwargs):
        self.__columnRule = value

    @property
    @style_get_decorator
    def columnRuleColor(self):
        return self.__columnRuleColor

    @columnRuleColor.setter
    @style_set_decorator
    def columnRuleColor(self, value=None, *args, **kwargs):
        self.__columnRuleColor = value

    @property
    @style_get_decorator
    def columnRuleStyle(self):
        return self.__columnRuleStyle

    @columnRuleStyle.setter
    @style_set_decorator
    def columnRuleStyle(self, value=None, *args, **kwargs):
        self.__columnRuleStyle = value

    @property
    @style_get_decorator
    def columnRuleWidth(self):
        return self.__columnRuleWidth

    @columnRuleWidth.setter
    @style_set_decorator
    def columnRuleWidth(self, value=None, *args, **kwargs):
        self.__columnRuleWidth = value

    @property
    @style_get_decorator
    def columns(self):
        return self.__columns

    @columns.setter
    @style_set_decorator
    def columns(self, value=None, *args, **kwargs):
        self.__columns = value

    @property
    @style_get_decorator
    def columnSpan(self):
        return self.__columnSpan

    @columnSpan.setter
    @style_set_decorator
    def columnSpan(self, value=None, *args, **kwargs):
        self.__columnSpan = value

    @property
    @style_get_decorator
    def columnWidth(self):
        return self.__columnWidth

    @columnWidth.setter
    @style_set_decorator
    def columnWidth(self, value=None, *args, **kwargs):
        self.__columnWidth = value

    @property
    @style_get_decorator
    def content(self):
        return self.__content

    @content.setter
    @style_set_decorator
    def content(self, value=None, *args, **kwargs):
        self.__content = value

    @property
    @style_get_decorator
    def counterIncrement(self):
        return self.__counterIncrement

    @counterIncrement.setter
    @style_set_decorator
    def counterIncrement(self, value=None, *args, **kwargs):
        self.__counterIncrement = value

    @property
    @style_get_decorator
    def counterReset(self):
        return self.__counterReset

    @counterReset.setter
    @style_set_decorator
    def counterReset(self, value=None, *args, **kwargs):
        self.__counterReset = value

    @property
    @style_get_decorator
    def cursor(self):
        return self.__cursor

    @cursor.setter
    @style_set_decorator
    def cursor(self, value=None, *args, **kwargs):
        self.__cursor = value

    @property
    @style_get_decorator
    def direction(self):
        return self.__direction

    @direction.setter
    @style_set_decorator
    def direction(self, value=None, *args, **kwargs):
        self.__direction = value

    @property
    @style_get_decorator
    def display(self):
        return self.__display

    @display.setter
    @style_set_decorator
    def display(self, value=None, *args, **kwargs):
        self.__display = value

    @property
    @style_get_decorator
    def emptyCells(self):
        return self.__emptyCells

    @emptyCells.setter
    @style_set_decorator
    def emptyCells(self, value=None, *args, **kwargs):
        self.__emptyCells = value

    @property
    @style_get_decorator
    def filter(self):
        return self.__filter

    @filter.setter
    @style_set_decorator
    def filter(self, value=None, *args, **kwargs):
        self.__filter = value

    @property
    @style_get_decorator
    def flex(self):
        return self.__flex

    @flex.setter
    @style_set_decorator
    def flex(self, value=None, *args, **kwargs):
        self.__flex = value

    @property
    @style_get_decorator
    def flexBasis(self):
        return self.__flexBasis

    @flexBasis.setter
    @style_set_decorator
    def flexBasis(self, value=None, *args, **kwargs):
        self.__flexBasis = value

    @property
    @style_get_decorator
    def flexDirection(self):
        return self.__flexDirection

    @flexDirection.setter
    @style_set_decorator
    def flexDirection(self, value=None, *args, **kwargs):
        self.__flexDirection = value

    @property
    @style_get_decorator
    def flexFlow(self):
        return self.__flexFlow

    @flexFlow.setter
    @style_set_decorator
    def flexFlow(self, value=None, *args, **kwargs):
        self.__flexFlow = value

    @property
    @style_get_decorator
    def flexGrow(self):
        return self.__flexGrow

    @flexGrow.setter
    @style_set_decorator
    def flexGrow(self, value=None, *args, **kwargs):
        self.__flexGrow = value

    @property
    @style_get_decorator
    def flexShrink(self):
        return self.__flexShrink

    @flexShrink.setter
    @style_set_decorator
    def flexShrink(self, value=None, *args, **kwargs):
        self.__flexShrink = value

    @property
    @style_get_decorator
    def flexWrap(self):
        return self.__flexWrap

    @flexWrap.setter
    @style_set_decorator
    def flexWrap(self, value=None, *args, **kwargs):
        self.__flexWrap = value

    @property
    @style_get_decorator
    def float(self):
        return self.__float

    @float.setter
    @style_set_decorator
    def float(self, value=None, *args, **kwargs):
        self.__float = value

    @property
    @style_get_decorator
    def cssFloat(self):
        return self.__cssFloat

    @cssFloat.setter
    @style_set_decorator
    def cssFloat(self, value=None, *args, **kwargs):
        self.__cssFloat = value

    @property
    @style_get_decorator
    def font(self):
        return self.__font

    @font.setter
    @style_set_decorator
    def font(self, value=None, *args, **kwargs):
        self.__font = value

    @property
    @style_get_decorator
    def fontFamily(self):
        return self.__fontFamily

    @fontFamily.setter
    @style_set_decorator
    def fontFamily(self, value=None, *args, **kwargs):
        self.__fontFamily = value

    @property
    @style_get_decorator
    def fontSize(self):
        return self.__fontSize

    @fontSize.setter
    @style_set_decorator
    def fontSize(self, value=None, *args, **kwargs):
        self.__fontSize = value

    @property
    @style_get_decorator
    def fontStyle(self):
        return self.__fontStyle

    @fontStyle.setter
    @style_set_decorator
    def fontStyle(self, value=None, *args, **kwargs):
        self.__fontStyle = value

    @property
    @style_get_decorator
    def fontVariant(self):
        return self.__fontVariant

    @fontVariant.setter
    @style_set_decorator
    def fontVariant(self, value=None, *args, **kwargs):
        self.__fontVariant = value

    @property
    @style_get_decorator
    def fontWeight(self):
        return self.__fontWeight

    @fontWeight.setter
    @style_set_decorator
    def fontWeight(self, value=None, *args, **kwargs):
        self.__fontWeight = value

    @property
    @style_get_decorator
    def fontSizeAdjust(self):
        return self.__fontSizeAdjust

    @fontSizeAdjust.setter
    @style_set_decorator
    def fontSizeAdjust(self, value=None, *args, **kwargs):
        self.__fontSizeAdjust = value

    @property
    @style_get_decorator
    def fontStretch(self):
        return self.__fontStretch

    @fontStretch.setter
    @style_set_decorator
    def fontStretch(self, value=None, *args, **kwargs):
        self.__fontStretch = value

    @property
    @style_get_decorator
    def hangingPunctuation(self):
        return self.__hangingPunctuation

    @hangingPunctuation.setter
    @style_set_decorator
    def hangingPunctuation(self, value=None, *args, **kwargs):
        self.__hangingPunctuation = value

    @property
    @style_get_decorator
    def height(self):
        return self.__height

    @height.setter
    @style_set_decorator
    def height(self, value=None, *args, **kwargs):
        self.__height = value

    @property
    @style_get_decorator
    def hyphens(self):
        return self.__hyphens

    @hyphens.setter
    @style_set_decorator
    def hyphens(self, value=None, *args, **kwargs):
        self.__hyphens = value

    @property
    @style_get_decorator
    def icon(self):
        return self.__icon

    @icon.setter
    @style_set_decorator
    def icon(self, value=None, *args, **kwargs):
        self.__icon = value

    @property
    @style_get_decorator
    def imageOrientation(self):
        return self.__imageOrientation

    @imageOrientation.setter
    @style_set_decorator
    def imageOrientation(self, value=None, *args, **kwargs):
        self.__imageOrientation = value

    @property
    @style_get_decorator
    def isolation(self):
        return self.__isolation

    @isolation.setter
    @style_set_decorator
    def isolation(self, value=None, *args, **kwargs):
        self.__isolation = value

    @property
    @style_get_decorator
    def justifyContent(self):
        return self.__justifyContent

    @justifyContent.setter
    @style_set_decorator
    def justifyContent(self, value=None, *args, **kwargs):
        self.__justifyContent = value

    @property
    @style_get_decorator
    def left(self):
        return self.__left

    @left.setter
    @style_set_decorator
    def left(self, value=None, *args, **kwargs):
        self.__left = value

    @property
    @style_get_decorator
    def letterSpacing(self):
        return self.__letterSpacing

    @letterSpacing.setter
    @style_set_decorator
    def letterSpacing(self, value=None, *args, **kwargs):
        self.__letterSpacing = value

    @property
    @style_get_decorator
    def lineHeight(self):
        return self.__lineHeight

    @lineHeight.setter
    @style_set_decorator
    def lineHeight(self, value=None, *args, **kwargs):
        self.__lineHeight = value

    @property
    @style_get_decorator
    def listStyle(self):
        return self.__listStyle

    @listStyle.setter
    @style_set_decorator
    def listStyle(self, value=None, *args, **kwargs):
        self.__listStyle = value

    @property
    @style_get_decorator
    def listStyleImage(self):
        return self.__listStyleImage

    @listStyleImage.setter
    @style_set_decorator
    def listStyleImage(self, value=None, *args, **kwargs):
        self.__listStyleImage = value

    @property
    @style_get_decorator
    def listStylePosition(self):
        return self.__listStylePosition

    @listStylePosition.setter
    @style_set_decorator
    def listStylePosition(self, value=None, *args, **kwargs):
        self.__listStylePosition = value

    @property
    @style_get_decorator
    def listStyleType(self):
        return self.__listStyleType

    @listStyleType.setter
    @style_set_decorator
    def listStyleType(self, value=None, *args, **kwargs):
        self.__listStyleType = value

    @property
    @style_get_decorator
    def margin(self):
        return self.__margin

    @margin.setter
    @style_set_decorator
    def margin(self, value=None, *args, **kwargs):
        self.__margin = value

    @property
    @style_get_decorator
    def marginBottom(self):
        return self.__marginBottom

    @marginBottom.setter
    @style_set_decorator
    def marginBottom(self, value=None, *args, **kwargs):
        self.__marginBottom = value

    @property
    @style_get_decorator
    def marginLeft(self):
        return self.__marginLeft

    @marginLeft.setter
    @style_set_decorator
    def marginLeft(self, value=None, *args, **kwargs):
        self.__marginLeft = value

    @property
    @style_get_decorator
    def marginRight(self):
        return self.__marginRight

    @marginRight.setter
    @style_set_decorator
    def marginRight(self, value=None, *args, **kwargs):
        self.__marginRight = value

    @property
    @style_get_decorator
    def marginTop(self):
        return self.__marginTop

    @marginTop.setter
    @style_set_decorator
    def marginTop(self, value=None, *args, **kwargs):
        self.__marginTop = value

    @property
    @style_get_decorator
    def maxHeight(self):
        return self.__maxHeight

    @maxHeight.setter
    @style_set_decorator
    def maxHeight(self, value=None, *args, **kwargs):
        self.__maxHeight = value

    @property
    @style_get_decorator
    def maxWidth(self):
        return self.__maxWidth

    @maxWidth.setter
    @style_set_decorator
    def maxWidth(self, value=None, *args, **kwargs):
        self.__maxWidth = value

    @property
    @style_get_decorator
    def minHeight(self):
        return self.__minHeight

    @minHeight.setter
    @style_set_decorator
    def minHeight(self, value=None, *args, **kwargs):
        self.__minHeight = value

    @property
    @style_get_decorator
    def minWidth(self):
        return self.__minWidth

    @minWidth.setter
    @style_set_decorator
    def minWidth(self, value=None, *args, **kwargs):
        self.__minWidth = value

    @property
    @style_get_decorator
    def navDown(self):
        return self.__navDown

    @navDown.setter
    @style_set_decorator
    def navDown(self, value=None, *args, **kwargs):
        self.__navDown = value

    @property
    @style_get_decorator
    def navIndex(self):
        return self.__navIndex

    @navIndex.setter
    @style_set_decorator
    def navIndex(self, value=None, *args, **kwargs):
        self.__navIndex = value

    @property
    @style_get_decorator
    def navLeft(self):
        return self.__navLeft

    @navLeft.setter
    @style_set_decorator
    def navLeft(self, value=None, *args, **kwargs):
        self.__navLeft = value

    @property
    @style_get_decorator
    def navRight(self):
        return self.__navRight

    @navRight.setter
    @style_set_decorator
    def navRight(self, value=None, *args, **kwargs):
        self.__navRight = value

    @property
    @style_get_decorator
    def navUp(self):
        return self.__navUp

    @navUp.setter
    @style_set_decorator
    def navUp(self, value=None, *args, **kwargs):
        self.__navUp = value

    @property
    @style_get_decorator
    def objectFit(self):
        return self.__objectFit

    @objectFit.setter
    @style_set_decorator
    def objectFit(self, value=None, *args, **kwargs):
        self.__objectFit = value

    @property
    @style_get_decorator
    def objectPosition(self):
        return self.__objectPosition

    @objectPosition.setter
    @style_set_decorator
    def objectPosition(self, value=None, *args, **kwargs):
        self.__objectPosition = value

    @property
    @style_get_decorator
    def opacity(self):
        return self.__opacity

    @opacity.setter
    @style_set_decorator
    def opacity(self, value=None, *args, **kwargs):
        self.__opacity = value

    @property
    @style_get_decorator
    def order(self):
        return self.__order

    @order.setter
    @style_set_decorator
    def order(self, value=None, *args, **kwargs):
        self.__order = value

    @property
    @style_get_decorator
    def orphans(self):
        return self.__orphans

    @orphans.setter
    @style_set_decorator
    def orphans(self, value=None, *args, **kwargs):
        self.__orphans = value

    @property
    @style_get_decorator
    def outline(self):
        return self.__outline

    @outline.setter
    @style_set_decorator
    def outline(self, value=None, *args, **kwargs):
        self.__outline = value

    @property
    @style_get_decorator
    def outlineColor(self):
        return self.__outlineColor

    @outlineColor.setter
    @style_set_decorator
    def outlineColor(self, value=None, *args, **kwargs):
        self.__outlineColor = value

    @property
    @style_get_decorator
    def outlineOffset(self):
        return self.__outlineOffset

    @outlineOffset.setter
    @style_set_decorator
    def outlineOffset(self, value=None, *args, **kwargs):
        self.__outlineOffset = value

    @property
    @style_get_decorator
    def outlineStyle(self):
        return self.__outlineStyle

    @outlineStyle.setter
    @style_set_decorator
    def outlineStyle(self, value=None, *args, **kwargs):
        self.__outlineStyle = value

    @property
    @style_get_decorator
    def outlineWidth(self):
        return self.__outlineWidth

    @outlineWidth.setter
    @style_set_decorator
    def outlineWidth(self, value=None, *args, **kwargs):
        self.__outlineWidth = value

    @property
    @style_get_decorator
    def overflow(self):
        return self.__overflow

    @overflow.setter
    @style_set_decorator
    def overflow(self, value=None, *args, **kwargs):
        self.__overflow = value

    @property
    @style_get_decorator
    def overflowX(self):
        return self.__overflowX

    @overflowX.setter
    @style_set_decorator
    def overflowX(self, value=None, *args, **kwargs):
        self.__overflowX = value

    @property
    @style_get_decorator
    def overflowY(self):
        return self.__overflowY

    @overflowY.setter
    @style_set_decorator
    def overflowY(self, value=None, *args, **kwargs):
        self.__overflowY = value

    @property
    @style_get_decorator
    def padding(self):
        return self.__padding

    @padding.setter
    @style_set_decorator
    def padding(self, value=None, *args, **kwargs):
        self.__padding = value

    @property
    @style_get_decorator
    def paddingBottom(self):
        return self.__paddingBottom

    @paddingBottom.setter
    @style_set_decorator
    def paddingBottom(self, value=None, *args, **kwargs):
        self.__paddingBottom = value

    @property
    @style_get_decorator
    def paddingLeft(self):
        return self.__paddingLeft

    @paddingLeft.setter
    @style_set_decorator
    def paddingLeft(self, value=None, *args, **kwargs):
        self.__paddingLeft = value

    @property
    @style_get_decorator
    def paddingRight(self):
        return self.__paddingRight

    @paddingRight.setter
    @style_set_decorator
    def paddingRight(self, value=None, *args, **kwargs):
        self.__paddingRight = value

    @property
    @style_get_decorator
    def paddingTop(self):
        return self.__paddingTop

    @paddingTop.setter
    @style_set_decorator
    def paddingTop(self, value=None, *args, **kwargs):
        self.__paddingTop = value

    @property
    @style_get_decorator
    def pageBreakAfter(self):
        return self.__pageBreakAfter

    @pageBreakAfter.setter
    @style_set_decorator
    def pageBreakAfter(self, value=None, *args, **kwargs):
        self.__pageBreakAfter = value

    @property
    @style_get_decorator
    def pageBreakBefore(self):
        return self.__pageBreakBefore

    @pageBreakBefore.setter
    @style_set_decorator
    def pageBreakBefore(self, value=None, *args, **kwargs):
        self.__pageBreakBefore = value

    @property
    @style_get_decorator
    def pageBreakInside(self):
        return self.__pageBreakInside

    @pageBreakInside.setter
    @style_set_decorator
    def pageBreakInside(self, value=None, *args, **kwargs):
        self.__pageBreakInside = value

    @property
    @style_get_decorator
    def perspective(self):
        return self.__perspective

    @perspective.setter
    @style_set_decorator
    def perspective(self, value=None, *args, **kwargs):
        self.__perspective = value

    @property
    @style_get_decorator
    def perspectiveOrigin(self):
        return self.__perspectiveOrigin

    @perspectiveOrigin.setter
    @style_set_decorator
    def perspectiveOrigin(self, value=None, *args, **kwargs):
        self.__perspectiveOrigin = value

    @property
    @style_get_decorator
    def position(self):
        return self.__position

    @position.setter
    @style_set_decorator
    def position(self, value=None, *args, **kwargs):
        self.__position = value

    @property
    @style_get_decorator
    def quotes(self):
        return self.__quotes

    @quotes.setter
    @style_set_decorator
    def quotes(self, value=None, *args, **kwargs):
        self.__quotes = value

    @property
    @style_get_decorator
    def resize(self):
        return self.__resize

    @resize.setter
    @style_set_decorator
    def resize(self, value=None, *args, **kwargs):
        self.__resize = value

    @property
    @style_get_decorator
    def right(self):
        return self.__right

    @right.setter
    @style_set_decorator
    def right(self, value=None, *args, **kwargs):
        self.__right = value

    @property
    @style_get_decorator
    def tableLayout(self):
        return self.__tableLayout

    @tableLayout.setter
    @style_set_decorator
    def tableLayout(self, value=None, *args, **kwargs):
        self.__tableLayout = value

    @property
    @style_get_decorator
    def tabSize(self):
        return self.__tabSize

    @tabSize.setter
    @style_set_decorator
    def tabSize(self, value=None, *args, **kwargs):
        self.__tabSize = value

    @property
    @style_get_decorator
    def textAlign(self):
        return self.__textAlign

    @textAlign.setter
    @style_set_decorator
    def textAlign(self, value=None, *args, **kwargs):
        self.__textAlign = value

    @property
    @style_get_decorator
    def textAlignLast(self):
        return self.__textAlignLast

    @textAlignLast.setter
    @style_set_decorator
    def textAlignLast(self, value=None, *args, **kwargs):
        self.__textAlignLast = value

    @property
    @style_get_decorator
    def textDecoration(self):
        return self.__textDecoration

    @textDecoration.setter
    @style_set_decorator
    def textDecoration(self, value=None, *args, **kwargs):
        self.__textDecoration = value

    @property
    @style_get_decorator
    def textDecorationColor(self):
        return self.__textDecorationColor

    @textDecorationColor.setter
    @style_set_decorator
    def textDecorationColor(self, value=None, *args, **kwargs):
        self.__textDecorationColor = value

    @property
    @style_get_decorator
    def textDecorationLine(self):
        return self.__textDecorationLine

    @textDecorationLine.setter
    @style_set_decorator
    def textDecorationLine(self, value=None, *args, **kwargs):
        self.__textDecorationLine = value

    @property
    @style_get_decorator
    def textDecorationStyle(self):
        return self.__textDecorationStyle

    @textDecorationStyle.setter
    @style_set_decorator
    def textDecorationStyle(self, value=None, *args, **kwargs):
        self.__textDecorationStyle = value

    @property
    @style_get_decorator
    def textIndent(self):
        return self.__textIndent

    @textIndent.setter
    @style_set_decorator
    def textIndent(self, value=None, *args, **kwargs):
        self.__textIndent = value

    @property
    @style_get_decorator
    def textJustify(self):
        return self.__textJustify

    @textJustify.setter
    @style_set_decorator
    def textJustify(self, value=None, *args, **kwargs):
        self.__textJustify = value

    @property
    @style_get_decorator
    def textOverflow(self):
        return self.__textOverflow

    @textOverflow.setter
    @style_set_decorator
    def textOverflow(self, value=None, *args, **kwargs):
        self.__textOverflow = value

    @property
    @style_get_decorator
    def textShadow(self):
        return self.__textShadow

    @textShadow.setter
    @style_set_decorator
    def textShadow(self, value=None, *args, **kwargs):
        self.__textShadow = value

    @property
    @style_get_decorator
    def textTransform(self):
        return self.__textTransform

    @textTransform.setter
    @style_set_decorator
    def textTransform(self, value=None, *args, **kwargs):
        self.__textTransform = value

    @property
    @style_get_decorator
    def top(self):
        return self.__top

    @top.setter
    @style_set_decorator
    def top(self, value=None, *args, **kwargs):
        self.__top = value

    @property
    @style_get_decorator
    def transform(self):
        return self.__transform

    @transform.setter
    @style_set_decorator
    def transform(self, value=None, *args, **kwargs):
        self.__transform = value

    @property
    @style_get_decorator
    def transformOrigin(self):
        return self.__transformOrigin

    @transformOrigin.setter
    @style_set_decorator
    def transformOrigin(self, value=None, *args, **kwargs):
        self.__transformOrigin = value

    @property
    @style_get_decorator
    def transformStyle(self):
        return self.__transformStyle

    @transformStyle.setter
    @style_set_decorator
    def transformStyle(self, value=None, *args, **kwargs):
        self.__transformStyle = value

    @property
    @style_get_decorator
    def transition(self):
        return self.__transition

    @transition.setter
    @style_set_decorator
    def transition(self, value=None, *args, **kwargs):
        self.__transition = value

    @property
    @style_get_decorator
    def transitionProperty(self):
        return self.__transitionProperty

    @transitionProperty.setter
    @style_set_decorator
    def transitionProperty(self, value=None, *args, **kwargs):
        self.__transitionProperty = value

    @property
    @style_get_decorator
    def transitionDuration(self):
        return self.__transitionDuration

    @transitionDuration.setter
    @style_set_decorator
    def transitionDuration(self, value=None, *args, **kwargs):
        self.__transitionDuration = value

    @property
    @style_get_decorator
    def transitionTimingFunction(self):
        return self.__transitionTimingFunction

    @transitionTimingFunction.setter
    @style_set_decorator
    def transitionTimingFunction(self, value=None, *args, **kwargs):
        self.__transitionTimingFunction = value

    @property
    @style_get_decorator
    def transitionDelay(self):
        return self.__transitionDelay

    @transitionDelay.setter
    @style_set_decorator
    def transitionDelay(self, value=None, *args, **kwargs):
        self.__transitionDelay = value

    @property
    @style_get_decorator
    def unicodeBidi(self):
        return self.__unicodeBidi

    @unicodeBidi.setter
    @style_set_decorator
    def unicodeBidi(self, value=None, *args, **kwargs):
        self.__unicodeBidi = value

    @property
    @style_get_decorator
    def userSelect(self):
        return self.__userSelect

    @userSelect.setter
    @style_set_decorator
    def userSelect(self, value=None, *args, **kwargs):
        self.__userSelect = value

    @property
    @style_get_decorator
    def verticalAlign(self):
        return self.__verticalAlign

    @verticalAlign.setter
    @style_set_decorator
    def verticalAlign(self, value=None, *args, **kwargs):
        self.__verticalAlign = value

    @property
    @style_get_decorator
    def visibility(self):
        return self.__visibility

    @visibility.setter
    @style_set_decorator
    def visibility(self, value=None, *args, **kwargs):
        self.__visibility = value

    @property
    @style_get_decorator
    def whiteSpace(self):
        return self.__whiteSpace

    @whiteSpace.setter
    @style_set_decorator
    def whiteSpace(self, value=None, *args, **kwargs):
        self.__whiteSpace = value

    @property
    @style_get_decorator
    def width(self):
        return self.__width

    @width.setter
    @style_set_decorator
    def width(self, value=None, *args, **kwargs):
        self.__width = value

    @property
    @style_get_decorator
    def wordBreak(self):
        return self.__wordBreak

    @wordBreak.setter
    @style_set_decorator
    def wordBreak(self, value=None, *args, **kwargs):
        self.__wordBreak = value

    @property
    @style_get_decorator
    def wordSpacing(self):
        return self.__wordSpacing

    @wordSpacing.setter
    @style_set_decorator
    def wordSpacing(self, value=None, *args, **kwargs):
        self.__wordSpacing = value

    @property
    @style_get_decorator
    def wordWrap(self):
        return self.__wordWrap

    @wordWrap.setter
    @style_set_decorator
    def wordWrap(self, value=None, *args, **kwargs):
        self.__wordWrap = value

    @property
    @style_get_decorator
    def widows(self):
        return self.__widows

    @widows.setter
    @style_set_decorator
    def widows(self, value=None, *args, **kwargs):
        self.__widows = value

    @property
    @style_get_decorator
    def zIndex(self):
        return self.__zIndex

    @zIndex.setter
    @style_set_decorator
    def zIndex(self, value=None, *args, **kwargs):
        self.__zIndex = value
