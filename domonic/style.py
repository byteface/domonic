"""
    domonic.style
    ====================================

    # TODO - should this be moved to the webapi in a future revision?

"""

from re import M, findall, finditer
from .utils import Utils


class StyleSheet:
    """An object implementing the StyleSheet interface represents a single style sheet.
    CSS style sheets will further implement the more specialized CSSStyleSheet interface.
    """

    def __init__(self):
        self.disabled = True  # a boolean value representing whether the current stylesheet has been applied or not
        self.href = None
        self.parentStyleSheet = None
        self.ownerNode = None
        self.media = None

    # @property
    # def href(self):
    #     """Returns a DOMString representing the location of the stylesheet."""
    #     return self.href

    # @property
    # def media(self):
    #     """Returns a MediaList representing the intended destination medium for style information."""
    #     raise NotImplementedError

    # @property
    # def ownerNode(self):
    #     """Returns a Node associating this style sheet with the current document."""
    #     raise NotImplementedError

    # @property
    # def parentStyleSheet(self):
    #     """Returns a StyleSheet including this one, if any; returns null if there aren't any."""
    #     raise NotImplementedError

    # @property
    # def title(self):
    #     """Returns a DOMString representing the advisory title of the current style sheet."""
    #     raise NotImplementedError

    # @property
    # def type(self):
    #     """Returns a DOMString representing the style sheet language for this style sheet."""
    #     raise NotImplementedError


class StyleSheetList(list):
    """An instance of this object can be returned by Document.styleSheets.
    it can be iterated over in a standard for loop over its indices, or converted to an Array.
    """

    def _populate_stylesheets_from_document(self, doc):
        """ parse the document to find all the stylesheets and add them to the list.
        """
        # print('this runs')
        # get loaded styles
        # from domonic.dom import document
        # newme = []

        sheets = doc.querySelectorAll('link[rel="stylesheet"]')
        for sheet in sheets:
            # get the content of the style sheet
            # TODO - sheet.href # make absolute
            # TODO - download and parse
            # self.styleSheets.append(StyleSheet(sheet))
            print('external:', sheet)
            ss = StyleSheet()
            # print('whats going on?')
            ss.href = sheet.href
            # ss.disabled = False
            # ss.ownerNode = doc
            # ss.parentStyleSheet = None
            self.append(ss)

        # get inline styles
        styles = doc.querySelectorAll('style')
        for style in styles:
            # self.styleSheets.append(StyleSheet(style))
            print('inline:', style)
            ss = StyleSheet()
            ss.href = doc.URL
            # ss.disabled = False
            # ss.ownerNode = doc
            # ss.parentStyleSheet = None
            self.append(ss)

        # self = newme

    @property
    def length(self):
        """Returns the number of CSSStyleSheet objects in the collection."""
        return len(self)

    def item(self, index):
        """Returns the CSSStyleSheet object at the index passed in, or null if no item exists for that index."""
        return self[index]


class CSSRule:
    """The CSSRule interface represents a single CSS rule.
    There are several types of rules which inherit properties from CSSRule.

    CSSFontFeatureValuesRule
    CSSViewportRule
    """

    UNKNOWN_RULE: int = 0
    STYLE_RULE: int = 1
    CHARSET_RULE: int = 2
    IMPORT_RULE: int = 3
    MEDIA_RULE: int = 4
    FONT_FACE_RULE: int = 5
    PAGE_RULE: int = 6
    NAMESPACE_RULE: int = 7
    KEYFRAMES_RULE: int = 8
    KEYFRAME_RULE: int = 9
    COUNTER_STYLE_RULE: int = 10
    SUPPORTS_RULE: int = 11
    FONT_FEATURE_VALUES_RULE: int = 12
    VIEWPORT_RULE: int = 13
    SUPPORTS_CONDITION_RULE: int = 14
    DOCUMENT_RULE: int = 15

    # GROUPING_RULES = [FONT_FACE_RULE, MEDIA_RULE, NAMESPACE_RULE, KEYFRAMES_RULE, COUNTER_STYLE_RULE, SUPPORTS_RULE, SUPPORTS_CONDITION_RULE]

    def __init__(self):
        self.parentStyleSheet = None
        # self._type = None
        self.parentRule: 'CSSRule' = None
        self.parentStyleSheet: 'CSSStyleSheet' = None
        self.type: int = None
        self.__cssText: str = None

    @property
    def cssText(self):
        """Represents the textual representation of the rule, e.g. "h1,h2 { font-size: 16pt }" or "@import 'url'".
        To access or modify parts of the rule (e.g. the value of "font-size" in the example)
        use the properties on the specialized interface for the rule's type.
        """
        return self.__cssText

    # @property
    # def parentRule(self):
    #     """Returns the containing rule, otherwise null. E.g. if this rule is a style rule inside an @media block,
    #     the parent rule would be that CSSMediaRule."""
    #     raise NotImplementedError

    # def parentStyleSheet(self):
    #     """Returns the CSSStyleSheet object for the style sheet that contains this rule"""
    #     raise NotImplementedError

    # def type(self):
    #     """Returns one of the Type constants to determine which type of rule is represented."""
    #     raise NotImplementedError


class CSSImportRule(CSSRule):
    """The CSSImportRule interface represents an @import rule in a CSS style sheet."""

    def __init__(self):
        super().__init__()
        self.href: str = None
        self.media: 'MediaList' = None
        self.styleSheet: 'CSSStyleSheet' = None
        self.type = CSSRule.IMPORT_RULE

    # @property
    # def href(self):
    #     """Returns a DOMString representing the URL of the imported style sheet."""
    #     raise NotImplementedError

    # @property
    # def media(self):
    #     """Returns a MediaList representing the intended destination medium for style information."""
    #     raise NotImplementedError

    # @property
    # def styleSheet(self):
    #     """Returns the CSSStyleSheet object representing the style sheet referenced by this rule."""
    #     raise NotImplementedError


class CSSStyleRule(CSSRule):
    """The CSSStyleRule interface represents a single style rule in a CSS style sheet."""

    def __init__(self):
        super().__init__()
        self.selectorText: str = None
        self.style: 'CSSStyleDeclaration' = None
        self.type = CSSRule.STYLE_RULE

    # @property
    # def selectorText(self):
    #     """Returns the textual representation of the rule selector."""
    #     raise NotImplementedError

    # @property
    # def style(self):
    #     """Returns the CSSStyleDeclaration object representing the declaration block of this rule."""
    #     raise NotImplementedError

    @property
    def cssText(self):
        """Returns the textual representation of the rule."""
        return self.selectorText + '{' + self.style.cssText + '}'

    # @cssText.setter
    # def cssText(self, value):
    #     """Sets the textual representation of the rule."""
    #     raise NotImplementedError


class CSSFontFaceRule(CSSRule):
    """The CSSFontFaceRule interface represents a @font-face rule in a CSS style sheet."""

    def __init__(self):
        super().__init__()
        self.style: 'CSSStyleDeclaration' = None
        self.type = CSSRule.FONT_FACE_RULE

    # @property
    # def style(self):
    #     """Returns the CSSStyleDeclaration object representing the declaration block of this rule."""
    #     raise NotImplementedError


class CSSPageRule(CSSRule):
    """The CSSPageRule interface represents a @page rule in a CSS style sheet."""

    def __init__(self):
        super().__init__()
        self.selectorText: str = None
        self.style: 'CSSStyleDeclaration' = None
        self.type = CSSRule.PAGE_RULE

    # @property
    # def selectorText(self):
    #     """Returns the textual representation of the page selector for the rule."""
    #     raise NotImplementedError

    # @property
    # def style(self):
    #     """Returns the CSSStyleDeclaration object representing the declaration block of this rule."""
    #     raise NotImplementedError


class CSSNamespaceRule(CSSRule):
    """The CSSNamespaceRule interface represents an @namespace rule in a CSS style sheet."""

    def __init__(self):
        super().__init__()
        self.namespaceURI: str = None
        self.prefix: str = None
        self.type = CSSRule.NAMESPACE_RULE

    # @property
    # def namespaceURI(self):
    #     """Returns the namespace URI for this rule."""
    #     raise NotImplementedError

    # @property
    # def prefix(self):
    #     """Returns the namespace prefix for this rule."""
    #     raise NotImplementedError


class CSSKeyframesRule(CSSRule):
    """The CSSKeyframesRule interface represents a @keyframes at-rule."""

    def __init__(self):
        super().__init__()
        self.cssRules: 'CSSRuleList' = CSSRuleList()
        self.name: str = None
        self.type = CSSRule.KEYFRAMES_RULE

    # @property
    # def cssRules(self):
    #     """Returns the CSSRuleList object representing the CSS rules in the media rule."""
    #     raise NotImplementedError

    # @property
    # def name(self):
    #     """Returns the name of the keyframes. This is a DOMString containing the unescaped keyframes name."""
    #     raise NotImplementedError


class CSSKeyframeRule(CSSRule):
    """The CSSKeyframeRule interface represents a single @keyframes at-rule."""

    def __init__(self):
        super().__init__()
        self.cssRules: 'CSSRuleList' = CSSRuleList()
        self.keyText: str = None
        self.style: 'CSSStyleDeclaration' = None
        self.type = CSSRule.KEYFRAME_RULE

    # @property
    # def cssRules(self):
    #     """Returns the CSSRuleList object representing the CSS rules in the media rule."""
    #     raise NotImplementedError

    # @property
    # def keyText(self):
    #     """Returns the text of the keyframe rule."""
    #     raise NotImplementedError

    # @property
    # def style(self):
    #     """Returns the CSSStyleDeclaration object representing the declaration block of this rule."""
    #     raise NotImplementedError


class CSSCounterStyleRule(CSSRule):
    """The CSSCounterStyleRule interface represents a @counter-style rule."""

    def __init__(self):
        super().__init__()
        self.name: str = None
        self.system: str = None
        self.type = CSSRule.COUNTER_STYLE_RULE

    # @property
    # def name(self):
    #     """Returns the name of the counter style."""
    #     raise NotImplementedError

    # @property
    # def system(self):
    #     """Returns the system of the counter style."""
    #     raise NotImplementedError


class CSSDocumentRule(CSSRule):
    """The CSSDocumentRule interface represents an @document rule."""

    def __init__(self):
        super().__init__()
        self.cssRules: 'CSSRuleList' = None
        self.type = CSSRule.DOCUMENT_RULE

    # @property
    # def cssRules(self):
    #     """Returns the CSSRuleList object representing the CSS rules in the media rule."""
    #     raise NotImplementedError


# class CSSValue(DOMObject): # deprecated
# class CSSValueList(list):

# class CSSRuleList(DOMObject):
# class CSSRuleList(list):

class CSSColorProfileRule(CSSRule):
    """The CSSColorProfileRule interface represents an @color-profile rule."""

    def __init__(self):
        super().__init__()
        self.colorProfile: str = None
        self.type = CSSRule.COLOR_PROFILE_RULE

    # @property
    # def colorProfile(self):
    #     """Returns the textual representation of the rule selector."""
    #     raise NotImplementedError


class CSSFontFeatureValuesRule(CSSRule):
    """The CSSFontFeatureValuesRule interface represents a @font-feature-values rule."""

    def __init__(self):
        super().__init__()
        self.cssRules: 'CSSRuleList' = None
        self.type = CSSRule.FONT_FEATURE_VALUES_RULE

    # @property
    # def cssRules(self):
    #     """Returns the CSSRuleList object representing the CSS rules in the media rule."""
    #     raise NotImplementedError


class CSSGroupingRule(CSSRule):
    """The CSSGroupingRule interface represents a @grouping rule."""

    def __init__(self):
        super().__init__()
        self.cssRules: 'CSSRuleList' = None
        # self.type = CSSRule.GROUPING_RULE

    # @property
    # def cssRules(self):
    #     """Returns the CSSRuleList object representing the CSS rules in the media rule."""
    #     raise NotImplementedError


class CSSConditionRule(CSSGroupingRule):
    """The CSSConditionRule interface represents a condition rule."""

    def __init__(self):
        super().__init__()
        self.conditionText: str = None
        self.cssRules: 'CSSRuleList' = None
        # self.type = CSSRule.CONDITIONAL_RULE

    # @property
    # def conditionText(self):
    #     """Returns the textual representation of the condition sub-rule."""
    #     raise NotImplementedError

    # @property
    # def cssRules(self):
    #     """Returns the CSSRuleList object representing the CSS rules in the media rule."""
    #     raise NotImplementedError


class CSSSupportsRule(CSSConditionRule):
    """The CSSSupportsRule interface represents a @supports at-rule."""

    def __init__(self):
        super().__init__()
        self.conditionText: str = None
        self.cssRules: 'CSSRuleList' = None
        self.type = CSSRule.SUPPORTS_RULE


class CSSMediaRule(CSSConditionRule):
    """The CSSMediaRule interface represents a @media rule in a CSS style sheet."""

    def __init__(self):
        super().__init__()
        self.media: 'MediaList' = MediaList()
        self.cssRules: 'CSSRuleList' = CSSRuleList()
        self.type = CSSRule.MEDIA_RULE

    # @property
    # def cssRules(self):
    #     """Returns a CSSRuleList containing the CSS rules in the media rule."""
    #     raise NotImplementedError

    # @property
    # def media(self):
    #     """Returns a MediaList representing the intended destination medium for style information."""
    #     raise NotImplementedError


class MediaList(list):
    """The MediaList interface represents a list of media. It is used in the @media at-rule."""

    @property
    def length(self) -> int:
        """Returns the number of media in the list."""
        return len(self)

    @property
    def mediaText(self) -> str:
        """Returns a string containing the text of the media query."""
        return ','.join(self)

    def item(self, index: int) -> str:
        """Returns the media at the given index in the MediaList."""
        return self[index]

    def appendMedium(self, newMedium: str) -> None:
        """Appends a new medium to the end of the list."""
        self.append(newMedium)

    def deleteMedium(self, oldMedium: str) -> None:
        """Removes medium in the media list. If the medium is not found nothing happens."""
        self.remove(oldMedium)


class CSSRuleList(list):
    """A CSSRuleList represents an ordered collection of read-only CSSRule objects.
    While the CSSRuleList object is read-only, and cannot be directly modified,
    it is considered a live object, as the content can change over time.
    """

    @property
    def length(self) -> int:
        """Returns an integer representing the number of CSSRule objects in the collection."""
        return len(self)

    def item(self, index: int) -> 'CSSRule':
        """Gets a single CSSRule."""
        return self[index]


class CSSStyleSheet(StyleSheet):
    """Creates a new CSSStyleSheet object."""

    def __init__(self):
        super().__init__()
        self.rules: list = []
        self.cssRules: CSSRuleList = CSSRuleList()
        self.ownerRule: CSSRule = None

    # @property
    # def cssRules():  # -> 'CSSStyleRuleList':
    #     """Returns a live CSSRuleList which maintains an up-to-date list of the CSSRule objects
    #     that comprise the stylesheet."""
    #     # return CSSStyleRuleList()
    #     raise NotImplementedError

    # @property
    # def ownerRule(self):
    #     """If this stylesheet is imported into the document using an @import rule,
    #     the ownerRule property returns the corresponding CSSImportRule; otherwise, this property's value is null."""
    #     raise NotImplementedError

    def deleteRule(self, index: int):
        """Deletes the rule at the specified index into the stylesheet's rule list."""
        raise NotImplementedError

    def insertRule(self, rule: str, index: int = None):
        """Inserts a new rule at the specified position in the stylesheet,
        given the textual representation of the rule."""
        from domonic.dom import DOMException
        rules = CSSParser.parseFromString(self, rule)
        if len(rules) == 0:
            raise DOMException(
                DOMException.HIERARCHY_REQUEST_ERR,
                'Invalid CSS rule.'
            )
        if len(rules) > 1:
            raise DOMException(
                DOMException.HIERARCHY_REQUEST_ERR,
                'Only one rule is allowed.'
            )
        if index is not None:
            if index > len(self.cssRules):
                raise DOMException(
                    DOMException.INDEX_SIZE_ERR,
                    'Index is out of range.'
                )
            self.cssRules.insert(index, rules[0])
            return index
        new_index = len(self.cssRules)
        self.cssRules.append(rules[0])
        return new_index

    def replace(self, text: str):
        """Asynchronously replaces the content of the stylesheet and returns
        a Promise that resolves with the updated CSSStyleSheet."""
        self.replaceSync(text)

    def replaceSync(self, text: str):
        """Synchronously replaces the content of the stylesheet."""
        self.cssRules = CSSParser.parseFromString(self, text)

    # @property
    # def rules(self):
    #     """The rules property is functionally identical to the standard cssRules property
    #     it returns a live CSSRuleList which maintains an up-to-date list of all of the rules in the style sheet.
    #     """
    #     raise NotImplementedError

    # Legacy methods
    def addRule(self, selectorText: str, style: str, index: int):
        """Adds a new rule to the stylesheet given the selector to which the style applies and the style block to apply
        to the matching elements.
        This differs from insertRule(), which takes the textual representation of the entire rule as a single string.
        """
        raise NotImplementedError

    def removeRule(self, index: int):
        """Functionally identical to deleteRule();
        removes the rule at the specified index from the stylesheet's rule list."""
        raise NotImplementedError

    def __str__(self):
        # converts the rules to css code
        return ''.join([str(rule) for rule in self.rules])


class Style(object):
    """[ js syntax styles ]
    # TODO - just add normal float?
    # TODO - consider camel case for hyphen params?
    # TODO - not json serialisable due to the decorators.
    """

    def __init__(self, parent_node=None):
        # print("*** MADE A STYLE11 ***")

        self._members_checked = False

        self._parent_node = parent_node  # so I can update a tags returned style attributes if a style gets set

        self.alignContent = "normal"
        """Sets or returns the alignment between the lines inside a flexible container
        when the items do not use all available space"""

        self.alignItems = "normal"
        """Sets or returns the alignment for items inside a flexible container"""

        self.alignSelf = "auto"
        """Sets or returns the alignment for selected items inside a flexible container"""

        self.animation = "normal"
        """ shorthand property for all the animation properties below, except the animationPlayState property"""

        self.animationDelay = 0
        """Sets or returns when the animation will start"""

        self.animationDirection = "normal"
        """Sets or returns whether or not the animation should play in reverse on alternate cycles"""

        self.animationDuration = 0
        """Sets or returns how many seconds or milliseconds an animation takes to complete one cycle"""

        self.animationFillMode = None
        """Sets or returns what values are applied by the animation outside the time it is executing"""

        self.animationIterationCount = 1
        """Sets or returns the number of times an animation should be played"""

        self.animationName = None
        """Sets or returns a name for the @keyframes animation"""

        self.animationTimingFunction = "ease"
        """Sets or returns the speed curve of the animation"""

        self.animationPlayState = "running"
        """Sets or returns whether the animation is running or paused """

        self.background = None
        """Sets or returns all the background properties in one declaration"""

        self.backgroundAttachment = "scroll"
        """Sets or returns whether a background-image is fixed or scrolls with the page"""

        self.backgroundColor = None
        """Sets or returns the background-color of an element """

        self.backgroundImage = None
        """Sets or returns the background-image for an element"""

        self.backgroundPosition = None
        """Sets or returns the starting position of a background-image"""

        self.backgroundRepeat = None
        """Sets or returns how to repeat (tile) a background-image"""

        self.backgroundClip = None
        """Sets or returns the painting area of the background"""

        self.backgroundOrigin = None
        """Sets or returns the positioning area of the background images"""

        self.backgroundSize = None
        """Sets or returns the size of the background image"""

        self.backfaceVisibility = None
        """Sets or returns whether or not an element should be visible when not facing the screen """

        self.border = "medium none black"
        """Sets or returns borderWidth, borderStyle, and borderColor in one declaration"""

        self.borderBottom = "medium none black"
        """Sets or returns all the borderBottom properties in one declaration """

        self.borderBottomColor = None
        """Sets or returns the color of the bottom border  1 """

        self.borderBottomLeftRadius = 0
        """Sets or returns the shape of the border of the bottom-left corner"""

        self.borderBottomRightRadius = 0
        """Sets or returns the shape of the border of the bottom-right corner """

        self.borderBottomStyle = None
        """Sets or returns the style of the bottom border """

        self.borderBottomWidth = None
        """Sets or returns the width of the bottom border """

        self.borderCollapse = None
        """Sets or returns whether the table border should be collapsed into a single border, or not"""

        self.borderColor = None
        """Sets or returns the color of an element's border (can have up to four values)"""

        self.borderImage = None
        """horthand property for setting or returning all the borderImage properties"""

        self.borderImageOutset = None
        """Sets or returns the amount by which the border image area extends beyond the border box"""

        self.borderImageRepeat = None
        """Sets or returns whether the image-border should be repeated, rounded or stretched"""

        self.borderImageSlice = None
        """Sets or returns the inward offsets of the image-border """

        self.borderImageSource = None
        """Sets or returns the image to be used as a border"""

        self.borderImageWidth = None
        """Sets or returns the widths of the image-border """

        self.borderLeft = None
        """Sets or returns all the borderLeft properties in one declaration"""

        self.borderLeftColor = None
        """Sets or returns the color of the left border"""

        self.borderLeftStyle = None
        """Sets or returns the style of the left border"""

        self.borderLeftWidth = None
        """Sets or returns the width of the left border"""

        self.borderRadius = 0
        """A shorthand property for setting or returning all the four borderRadius properties """

        self.borderRight = None
        """Sets or returns all the borderRight properties in one declaration"""

        self.borderRightColor = None
        """Sets or returns the color of the right border"""

        self.borderRightStyle = None
        """Sets or returns the style of the right border"""

        self.borderRightWidth = None
        """Sets or returns the width of the right border"""

        self.borderSpacing = None
        """Sets or returns the space between cells in a table """

        self.borderStyle = None
        """Sets or returns the style of an element's border (can have up to four values)"""

        self.borderTop = None
        """Sets or returns all the borderTop properties in one declaration"""

        self.borderTopColor = None
        """Sets or returns the color of the top border"""

        self.borderTopLeftRadius = 0
        """Sets or returns the shape of the border of the top-left corner """

        self.borderTopRightRadius = 0
        """Sets or returns the shape of the border of the top-right corner"""

        self.borderTopStyle = None
        """Sets or returns the style of the top border"""

        self.borderTopWidth = None
        """Sets or returns the width of the top border"""

        self.borderWidth = None
        """Sets or returns the width of an element's border (can have up to four values)"""

        self.bottom = None
        """Sets or returns the bottom position of a positioned element"""

        self.boxDecorationBreak = None
        """Sets or returns the behaviour of the background and border of an element at page-break, or,
        for in-line elements, at line-break."""

        self.boxShadow = None
        """ttaches one or more drop-shadows to the box"""

        self.boxSizing = None
        """llows you to define certain elements to fit an area in a certain way"""

        self.captionSide = None
        """Sets or returns the position of the table caption"""

        self.clear = None
        """Sets or returns the position of the element relative to floating objects"""

        self.clip = None
        """Sets or returns which part of a positioned element is visible"""

        self.color = None
        """Sets or returns the color of the text"""

        self.columnCount = None
        """Sets or returns the number of columns an element should be divided into"""

        self.columnFill = None
        """Sets or returns how to fill columns"""

        self.columnGap = "normal"
        """Sets or returns the gap between the columns"""

        self.columnRule = None
        """shorthand property for setting or returning all the columnRule properties"""

        self.columnRuleColor = None
        """Sets or returns the color of the rule between columns"""

        self.columnRuleStyle = None
        """Sets or returns the style of the rule between columns"""

        self.columnRuleWidth = None
        """Sets or returns the width of the rule between columns"""

        self.columns = None
        """horthand property for setting or returning columnWidth and columnCount"""

        self.columnSpan = None
        """Sets or returns how many columns an element should span across """

        self.columnWidth = None
        """Sets or returns the width of the columns"""

        self.content = None
        """d with the :before and :after pseudo-elements, to insert generated content"""

        self.counterIncrement = None
        """Increments one or more counters"""

        self.counterReset = None
        """Creates or resets one or more counters """

        self.cursor = None
        """Sets or returns the type of cursor to display for the mouse pointer"""

        self.direction = None
        """Sets or returns the text direction """

        self.display = None
        """Sets or returns an element's display type"""

        self.emptyCells = None
        """Sets or returns whether to show the border and background of empty cells, or not """

        self.filter = None
        """Sets or returns image filters (visual effects, like blur and saturation)"""

        self.flex = None
        """Sets or returns the length of the item, relative to the rest"""

        self.flexBasis = None
        """Sets or returns the initial length of a flexible item"""

        self.flexDirection = None
        """Sets or returns the direction of the flexible items"""

        self.flexFlow = None
        """A shorthand property for the flexDirection and the flexWrap properties """

        self.flexGrow = None
        """Sets or returns how much the item will grow relative to the rest"""

        self.flexShrink = None
        """Sets or returns how the item will shrink relative to the rest"""

        self.flexWrap = None
        """Sets or returns whether the flexible items should wrap or not"""

        self.float = None  # ADDED BY ME

        self.cssFloat = None
        """Sets or returns the horizontal alignment of an element """

        self.font = None
        """Sets or returns fontStyle, fontVariant, fontWeight, fontSize, lineHeight, and fontFamily
        in one declaration"""

        self.fontFamily = None
        """Sets or returns the font family for text"""

        self.fontSize = "medium"
        """Sets or returns the font size of the text"""

        self.fontStyle = "normal"
        """Sets or returns whether the style of the font is normal, italic or oblique """

        self.fontVariant = None
        """Sets or returns whether the font should be displayed in small capital letters"""

        self.fontWeight = "normal"
        """Sets or returns the boldness of the font"""

        self.fontSizeAdjust = None
        """eserves the readability of text when font fallback occurs"""

        self.fontStretch = None
        """ects a normal, condensed, or expanded face from a font family"""

        self.hangingPunctuation = None
        """ecifies whether a punctuation character may be placed outside the line box"""

        self.height = "auto"
        """Sets or returns the height of an element"""

        self.hyphens = None
        """Sets how to split words to improve the layout of paragraphs"""

        self.icon = None
        """Provides the author the ability to style an element with an iconic equivalent"""

        self.imageOrientation = None
        """Specifies a rotation in the right or clockwise direction that a user agent applies to an image """

        self.isolation = None
        """efines whether an element must create a new stacking content"""

        self.justifyContent = "normal"
        """Sets or returns the alignment between the items inside a flexible container when the items
        do not use all available space. """

        self.left = "auto"
        """Sets or returns the left position of a positioned element"""

        self.letterSpacing = None
        """Sets or returns the space between characters in a text """

        self.lineHeight = None
        """Sets or returns the distance between lines in a text"""

        self.listStyle = None
        """Sets or returns listStyleImage, listStylePosition, and listStyleType in one declaration"""

        self.listStyleImage = None
        """Sets or returns an image as the list-item marker"""

        self.listStylePosition = None
        """Sets or returns the position of the list-item marker"""

        self.listStyleType = None
        """Sets or returns the list-item marker type"""

        self.margin = 0
        """Sets or returns the margins of an element (can have up to four values) """

        self.marginBottom = 0
        """Sets or returns the bottom margin of an element"""

        self.marginLeft = 0
        """Sets or returns the left margin of an element"""

        self.marginRight = 0
        """Sets or returns the right margin of an element """

        self.marginTop = 0
        """Sets or returns the top margin of an element"""

        self.maxHeight = None
        """Sets or returns the maximum height of an element """

        self.maxWidth = None
        """Sets or returns the maximum width of an element"""

        self.minHeight = None
        """Sets or returns the minimum height of an element """

        self.minWidth = None
        """Sets or returns the minimum width of an element"""

        self.navDown = None
        """Sets or returns where to navigate when using the arrow-down navigation key """

        self.navIndex = None
        """Sets or returns the tabbing order for an element"""

        self.navLeft = None
        """Sets or returns where to navigate when using the arrow-left navigation key """

        self.navRight = None
        """Sets or returns where to navigate when using the arrow-right navigation key"""

        self.navUp = None
        """Sets or returns where to navigate when using the arrow-up navigation key"""

        self.objectFit = None
        """pecifies how the contents of a replaced element should be fitted to the box
        established by its used height and width"""

        self.objectPosition = None
        """ecifies the alignment of the replaced element inside its box """

        self.opacity = None
        """Sets or returns the opacity level for an element"""

        self.order = None
        """Sets or returns the order of the flexible item, relative to the rest"""

        self.orphans = None
        """Sets or returns the minimum number of lines for an element that must be left at the bottom
        of a page when a page break occurs inside an element"""

        self.outline = None
        """Sets or returns all the outline properties in one declaration"""

        self.outlineColor = None
        """Sets or returns the color of the outline around a element"""

        self.outlineOffset = None
        """ffsets an outline, and draws it beyond the border edge"""

        self.outlineStyle = None
        """Sets or returns the style of the outline around an element """

        self.outlineWidth = None
        """Sets or returns the width of the outline around an element """

        self.overflow = "visible"
        """Sets or returns what to do with content that renders outside the element box """

        self.overflowX = None
        """pecifies what to do with the left/right edges of the content, if it overflows the element's content area"""

        self.overflowY = None
        """pecifies what to do with the top/bottom edges of the content, if it overflows the element's content area"""

        self.padding = 0
        """Sets or returns the padding of an element (can have up to four values) """

        self.paddingBottom = 0
        """Sets or returns the bottom padding of an element"""

        self.paddingLeft = 0
        """Sets or returns the left padding of an element """

        self.paddingRight = 0
        """Sets or returns the right padding of an element"""

        self.paddingTop = 0
        """Sets or returns the top padding of an element"""

        self.pageBreakAfter = "auto"
        """Sets or returns the page-break behavior after an element """

        self.pageBreakBefore = "auto"
        """Sets or returns the page-break behavior before an element"""

        self.pageBreakInside = "auto"
        """Sets or returns the page-break behavior inside an element"""

        self.perspective = None
        """Sets or returns the perspective on how 3D elements are viewed"""

        self.perspectiveOrigin = None
        """Sets or returns the bottom position of 3D elements """

        self.position = None
        """Sets or returns the type of positioning method used for an element (static, relative, absolute or fixed) """

        self.quotes = None
        """Sets or returns the type of quotation marks for embedded quotations"""

        self.resize = None
        """Sets or returns whether or not an element is resizable by the user """

        self.right = "auto"
        """Sets or returns the right position of a positioned element """

        self.tableLayout = "auto"
        """Sets or returns the way to lay out table cells, rows, and columns"""

        self.tabSize = None
        """Sets or returns the length of the tab-character"""

        self.textAlign = "left"
        """Sets or returns the horizontal alignment of text"""

        self.textAlignLast = "auto"
        """Sets or returns how the last line of a block or a line right before a forced line break
        is aligned when text-align is justify"""

        self.textDecoration = None
        """Sets or returns the decoration of a text"""

        self.textDecorationColor = None
        """Sets or returns the color of the text-decoration"""

        self.textDecorationLine = None
        """Sets or returns the type of line in a text-decoration"""

        self.textDecorationStyle = None
        """Sets or returns the style of the line in a text decoration """

        self.textIndent = None
        """Sets or returns the indentation of the first line of text"""

        self.textJustify = None
        """Sets or returns the justification method used when text-align is justify"""

        self.textOverflow = "clip"
        """Sets or returns what should happen when text overflows the containing element"""

        self.textShadow = None
        """Sets or returns the shadow effect of a text"""

        self.textTransform = None
        """Sets or returns the capitalization of a text"""

        self.top = None
        """Sets or returns the top position of a positioned element """

        self.transform = None
        """pplies a 2D or 3D transformation to an element"""

        self.transformOrigin = None
        """Sets or returns the position of transformed elements"""

        self.transformStyle = None
        """Sets or returns how nested elements are rendered in 3D space"""

        self.transition = None
        """shorthand property for setting or returning the four transition properties"""

        self.transitionProperty = None
        """Sets or returns the CSS property that the transition effect is for """

        self.transitionDuration = 0
        """Sets or returns how many seconds or milliseconds a transition effect takes to complete """

        self.transitionTimingFunction = None
        """Sets or returns the speed curve of the transition effect"""

        self.transitionDelay = 0
        """Sets or returns when the transition effect will start"""

        self.unicodeBidi = None
        """Sets or returns whether the text should be overridden to support multiple languages in the same document """

        self.userSelect = None
        """Sets or returns whether the text of an element can be selected or not"""

        self.verticalAlign = None
        """Sets or returns the vertical alignment of the content in an element"""

        self.visibility = "visible"
        """Sets or returns whether an element should be visible"""

        self.whiteSpace = "normal"
        """ Sets or returns how to handle tabs, line breaks and whitespace in a text 1 """

        self.width = "auto"
        """Sets or returns the width of an element"""

        self.wordBreak = "normal"
        """Sets or returns line breaking rules for non-CJK scripts"""

        self.wordSpacing = None
        """Sets or returns the spacing between words in a text"""

        self.wordWrap = "normal"
        """Allows long, unbreakable words to be broken and wrap to the next line"""

        self.widows = None
        """Sets or returns the minimum number of lines for an element that must be visible at the top of a page """

        self.zIndex = "auto"
        """Sets or returns the stack order of a positioned element"""

        # adds a bunch of more recent CSS3 properties
        self.all = None
        self.alignmentBaseline = None
        self.appearance = None
        self.backdropFilter = None
        self.backgroundBlendMode = None
        self.backgroundPositionX = None
        self.backgroundPositionY = None
        self.backgroundRepeatX = None
        self.backgroundRepeatY = None
        self.baselineShift = None
        self.blockSize = None
        self.borderBlockEnd = None
        self.borderBlockEndColor = None
        self.borderBlockEndStyle = None
        self.borderBlockEndWidth = None
        self.borderBlockStart = None
        self.borderBlockStartColor = None
        self.borderBlockStartStyle = None
        self.borderBlockStartWidth = None
        self.borderInlineEnd = None
        self.borderInlineEndColor = None
        self.borderInlineEndStyle = None
        self.borderInlineEndWidth = None
        self.borderInlineStart = None
        self.borderInlineStartColor = None
        self.borderInlineStartStyle = None
        self.borderInlineStartWidth = None
        self.breakAfter = None
        self.breakBefore = None
        self.breakInside = None
        self.bufferedRendering = None
        self.caretColor = None
        self.clipPath = None
        self.clipRule = None
        self.colorInterpolation = None
        self.colorInterpolationFilters = None
        self.colorRendering = None
        self.colorScheme = None
        self.contain = None
        self.containIntrinsicSize = None
        self.contentVisibility = None
        self.counterSet = None
        self.cx = None
        self.cy = None
        self.dominantBaseline = None
        self.d = None
        self.fill = None
        self.fillOpacity = None
        self.fillRule = None
        self.fontDisplay = None
        self.floodColor = None
        self.floodOpacity = None
        self.fontFeatureSettings = None
        self.fontKerning = None
        self.fontOpticalSizing = None
        self.fontVariantCaps = None
        self.fontVariantEastAsian = None
        self.fontVariantLigatures = None
        self.fontVariantNumeric = None
        self.fontVariationSettings = None
        self.gap = None
        self.grid = None
        self.gridArea = None
        self.gridAutoColumns = None
        self.gridAutoFlow = None
        self.gridAutoRows = None
        self.gridColumn = None
        self.gridColumnEnd = None
        self.gridColumnGap = None
        self.gridColumnStart = None
        self.gridGap = None
        self.gridRow = None
        self.gridRowEnd = None
        self.gridRowGap = None
        self.gridRowStart = None
        self.gridTemplate = None
        self.gridTemplateAreas = None
        self.gridTemplateColumns = None
        self.gridTemplateRows = None
        self.imageRendering = None
        self.inherits = None
        self.initialValue = None
        self.inlineSize = None
        self.justifyItems = None
        self.justifySelf = None
        self.lightingColor = None
        self.lineBreak = None
        self.marginBlockEnd = None
        self.marginBlockStart = None
        self.marginInlineEnd = None
        self.marginInlineStart = None
        self.marker = None
        self.markerEnd = None
        self.markerMid = None
        self.markerStart = None
        self.mask = None
        self.maskType = None
        self.maxBlockSize = None
        self.maxInlineSize = None
        self.maxZoom = None
        self.minBlockSize = None
        self.minInlineSize = None
        self.minZoom = None
        self.mixBlendMode = None
        self.objectFit = None
        self.objectPosition = None
        self.offset = None
        self.offsetDistance = None
        self.offsetPath = None
        self.offsetRotate = None
        self.orientation = None
        self.overflowAnchor = None
        self.overflowWrap = None
        self.overscrollBehavior = None
        self.overscrollBehaviorBlock = None
        self.overscrollBehaviorInline = None
        self.overscrollBehaviorX = None
        self.overscrollBehaviorY = None
        self.paddingBlockEnd = None
        self.paddingBlockStart = None
        self.paddingInlineEnd = None
        self.paddingInlineStart = None
        self.page = None
        self.pageOrientation = None
        self.paintOrder = None
        self.placeContent = None
        self.placeItems = None
        self.placeSelf = None
        self.pointerEvents = None
        self.r = None
        self.rowGap = None
        self.rubyPosition = None
        self.rx = None
        self.ry = None
        self.scrollBehavior = None
        self.scrollMargin = None
        self.scrollMarginBlock = None
        self.scrollMarginBlockEnd = None
        self.scrollMarginBlockStart = None
        self.scrollMarginBottom = None
        self.scrollMarginInline = None
        self.scrollMarginInlineEnd = None
        self.scrollMarginInlineStart = None
        self.scrollMarginLeft = None
        self.scrollMarginRight = None
        self.scrollMarginTop = None
        self.scrollPadding = None
        self.scrollPaddingBlock = None
        self.scrollPaddingBlockEnd = None
        self.scrollPaddingBlockStart = None
        self.scrollPaddingBottom = None
        self.scrollPaddingInline = None
        self.scrollPaddingInlineEnd = None
        self.scrollPaddingInlineStart = None
        self.scrollPaddingLeft = None
        self.scrollPaddingRight = None
        self.scrollPaddingTop = None
        self.scrollSnapAlign = None
        self.scrollSnapStop = None
        self.scrollSnapType = None
        self.shapeImageThreshold = None
        self.shapeMargin = None
        self.shapeOutside = None
        self.shapeRendering = None
        self.size = None
        self.speak = None
        self.src = None
        self.stopColor = None
        self.stopOpacity = None
        self.stroke = None
        self.strokeDasharray = None
        self.strokeDashoffset = None
        self.strokeLinecap = None
        self.strokeLinejoin = None
        self.strokeMiterlimit = None
        self.strokeOpacity = None
        self.strokeWidth = None
        self.syntax = None
        self.textAnchor = None
        self.textCombineUpright = None
        self.textDecorationSkipInk = None
        self.textOrientation = None
        self.textRendering = None
        self.textSizeAdjust = None
        self.textUnderlinePosition = None
        self.touchAction = None
        self.transformBox = None
        self.unicodeRange = None
        self.userZoom = None
        self.vectorEffect = None
        self.willChange = None
        self.writingMode = None
        self.x = None
        self.y = None

        self._members_checked = True  # NOTE - this ALWAYS needs to be last or all props will render


    def style_set_decorator(func):
        from functools import wraps

        @wraps(func)
        def style_wrapper(self, *args, **kwargs):
            value = args[0]
            if value is None:
                value = "none"
            func(self, value, *args, **kwargs)

            # to only render to the Node what gets set. allows init to run first
            # note - this was a counter prior to 0.8.3 and is now a bool as counter stops custom props on extended classes
            if not self._members_checked:
                return

            if self._parent_node is not None:
                key = func.__name__
                s = f"{Utils.case_kebab(key)}:{value};"
                styles = self._parent_node.getAttribute("style")
                if styles is not None:
                    # TODO - replace if exists. should be able to do this now with the parser?
                    # if key not in styles:
                    styles = styles + s
                    # else:
                        # styles = styles.replace(f"{key}:{self.__dict__[key]}", s)
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
                value = "none"
            return value

        return style_wrapper

    @property
    @style_get_decorator  # TODO - pass array of valid words as params. so can raise value errors
    def alignContent(self):
        return self.__alignContent

    @alignContent.setter
    @style_set_decorator
    def alignContent(self, value="stretch", *args, **kwargs):
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
    
    # new adds all newer css3 properties

    @property
    def all(self):
        return self.__all

    @all.setter
    @style_set_decorator
    def all(self, value=None, *args, **kwargs):
        self.__all = value

    @property    
    def alignmentBaseline(self):
        return self.__alignmentBaseline

    @alignmentBaseline.setter
    @style_set_decorator
    def alignmentBaseline(self, value=None, *args, **kwargs):
        self.__alignmentBaseline = value

    @property    
    def appearance(self):
        return self.__appearance

    @appearance.setter
    @style_set_decorator
    def appearance(self, value=None, *args, **kwargs):
        self.__appearance = value

    @property    
    def backdropFilter(self):
        return self.__backdropFilter

    @backdropFilter.setter
    @style_set_decorator
    def backdropFilter(self, value=None, *args, **kwargs):
        self.__backdropFilter = value

    @property    
    def backgroundBlendMode(self):
        return self.__backgroundBlendMode

    @backgroundBlendMode.setter
    @style_set_decorator
    def backgroundBlendMode(self, value=None, *args, **kwargs):
        self.__backgroundBlendMode = value

    @property    
    def backgroundPositionX(self):
        return self.__backgroundPositionX

    @backgroundPositionX.setter
    @style_set_decorator
    def backgroundPositionX(self, value=None, *args, **kwargs):
        self.__backgroundPositionX = value

    @property    
    def backgroundPositionY(self):
        return self.__backgroundPositionY

    @backgroundPositionY.setter
    @style_set_decorator
    def backgroundPositionY(self, value=None, *args, **kwargs):
        self.__backgroundPositionY = value

    @property    
    def backgroundRepeatX(self):
        return self.__backgroundRepeatX

    @backgroundRepeatX.setter
    @style_set_decorator
    def backgroundRepeatX(self, value=None, *args, **kwargs):
        self.__backgroundRepeatX = value

    @property    
    def backgroundRepeatY(self):
        return self.__backgroundRepeatY

    @backgroundRepeatY.setter
    @style_set_decorator
    def backgroundRepeatY(self, value=None, *args, **kwargs):
        self.__backgroundRepeatY = value

    @property    
    def baselineShift(self):
        return self.__baselineShift

    @baselineShift.setter
    @style_set_decorator
    def baselineShift(self, value=None, *args, **kwargs):
        self.__baselineShift = value

    @property    
    def blockSize(self):
        return self.__blockSize

    @blockSize.setter
    @style_set_decorator
    def blockSize(self, value=None, *args, **kwargs):
        self.__blockSize = value

    @property    
    def borderBlockEnd(self):
        return self.__borderBlockEnd

    @borderBlockEnd.setter
    @style_set_decorator
    def borderBlockEnd(self, value=None, *args, **kwargs):
        self.__borderBlockEnd = value

    @property    
    def borderBlockEndColor(self):
        return self.__borderBlockEndColor

    @borderBlockEndColor.setter
    @style_set_decorator
    def borderBlockEndColor(self, value=None, *args, **kwargs):
        self.__borderBlockEndColor = value

    @property    
    def borderBlockEndStyle(self):
        return self.__borderBlockEndStyle

    @borderBlockEndStyle.setter
    @style_set_decorator
    def borderBlockEndStyle(self, value=None, *args, **kwargs):
        self.__borderBlockEndStyle = value

    @property    
    def borderBlockEndWidth(self):
        return self.__borderBlockEndWidth

    @borderBlockEndWidth.setter
    @style_set_decorator
    def borderBlockEndWidth(self, value=None, *args, **kwargs):
        self.__borderBlockEndWidth = value

    @property    
    def borderBlockStart(self):
        return self.__borderBlockStart

    @borderBlockStart.setter
    @style_set_decorator
    def borderBlockStart(self, value=None, *args, **kwargs):
        self.__borderBlockStart = value

    @property    
    def borderBlockStartColor(self):
        return self.__borderBlockStartColor

    @borderBlockStartColor.setter
    @style_set_decorator
    def borderBlockStartColor(self, value=None, *args, **kwargs):
        self.__borderBlockStartColor = value

    @property    
    def borderBlockStartStyle(self):
        return self.__borderBlockStartStyle

    @borderBlockStartStyle.setter
    @style_set_decorator
    def borderBlockStartStyle(self, value=None, *args, **kwargs):
        self.__borderBlockStartStyle = value

    @property    
    def borderBlockStartWidth(self):
        return self.__borderBlockStartWidth

    @borderBlockStartWidth.setter
    @style_set_decorator
    def borderBlockStartWidth(self, value=None, *args, **kwargs):
        self.__borderBlockStartWidth = value

    @property    
    def borderInlineEnd(self):
        return self.__borderInlineEnd

    @borderInlineEnd.setter
    @style_set_decorator
    def borderInlineEnd(self, value=None, *args, **kwargs):
        self.__borderInlineEnd = value

    @property    
    def borderInlineEndColor(self):
        return self.__borderInlineEndColor

    @borderInlineEndColor.setter
    @style_set_decorator
    def borderInlineEndColor(self, value=None, *args, **kwargs):
        self.__borderInlineEndColor = value

    @property    
    def borderInlineEndStyle(self):
        return self.__borderInlineEndStyle

    @borderInlineEndStyle.setter
    @style_set_decorator
    def borderInlineEndStyle(self, value=None, *args, **kwargs):
        self.__borderInlineEndStyle = value

    @property    
    def borderInlineEndWidth(self):
        return self.__borderInlineEndWidth

    @borderInlineEndWidth.setter
    @style_set_decorator
    def borderInlineEndWidth(self, value=None, *args, **kwargs):
        self.__borderInlineEndWidth = value

    @property    
    def borderInlineStart(self):
        return self.__borderInlineStart

    @borderInlineStart.setter
    @style_set_decorator
    def borderInlineStart(self, value=None, *args, **kwargs):
        self.__borderInlineStart = value

    @property    
    def borderInlineStartColor(self):
        return self.__borderInlineStartColor

    @borderInlineStartColor.setter
    @style_set_decorator
    def borderInlineStartColor(self, value=None, *args, **kwargs):
        self.__borderInlineStartColor = value

    @property    
    def borderInlineStartStyle(self):
        return self.__borderInlineStartStyle

    @borderInlineStartStyle.setter
    @style_set_decorator
    def borderInlineStartStyle(self, value=None, *args, **kwargs):
        self.__borderInlineStartStyle = value

    @property    
    def borderInlineStartWidth(self):
        return self.__borderInlineStartWidth

    @borderInlineStartWidth.setter
    @style_set_decorator
    def borderInlineStartWidth(self, value=None, *args, **kwargs):
        self.__borderInlineStartWidth = value

    @property    
    def breakAfter(self):
        return self.__breakAfter

    @breakAfter.setter
    @style_set_decorator
    def breakAfter(self, value=None, *args, **kwargs):
        self.__breakAfter = value

    @property    
    def breakBefore(self):
        return self.__breakBefore

    @breakBefore.setter
    @style_set_decorator
    def breakBefore(self, value=None, *args, **kwargs):
        self.__breakBefore = value

    @property    
    def breakInside(self):
        return self.__breakInside

    @breakInside.setter
    @style_set_decorator
    def breakInside(self, value=None, *args, **kwargs):
        self.__breakInside = value

    @property    
    def bufferedRendering(self):
        return self.__bufferedRendering

    @bufferedRendering.setter
    @style_set_decorator
    def bufferedRendering(self, value=None, *args, **kwargs):
        self.__bufferedRendering = value

    @property    
    def caretColor(self):
        return self.__caretColor

    @caretColor.setter
    @style_set_decorator
    def caretColor(self, value=None, *args, **kwargs):
        self.__caretColor = value

    @property    
    def clipPath(self):
        return self.__clipPath

    @clipPath.setter
    @style_set_decorator
    def clipPath(self, value=None, *args, **kwargs):
        self.__clipPath = value

    @property    
    def clipRule(self):
        return self.__clipRule

    @clipRule.setter
    @style_set_decorator
    def clipRule(self, value=None, *args, **kwargs):
        self.__clipRule = value

    @property    
    def colorInterpolation(self):
        return self.__colorInterpolation

    @colorInterpolation.setter
    @style_set_decorator
    def colorInterpolation(self, value=None, *args, **kwargs):
        self.__colorInterpolation = value

    @property    
    def colorInterpolationFilters(self):
        return self.__colorInterpolationFilters

    @colorInterpolationFilters.setter
    @style_set_decorator
    def colorInterpolationFilters(self, value=None, *args, **kwargs):
        self.__colorInterpolationFilters = value

    @property    
    def colorRendering(self):
        return self.__colorRendering

    @colorRendering.setter
    @style_set_decorator
    def colorRendering(self, value=None, *args, **kwargs):
        self.__colorRendering = value

    @property    
    def colorScheme(self):
        return self.__colorScheme

    @colorScheme.setter
    @style_set_decorator
    def colorScheme(self, value=None, *args, **kwargs):
        self.__colorScheme = value

    @property    
    def contain(self):
        return self.__contain

    @contain.setter
    @style_set_decorator
    def contain(self, value=None, *args, **kwargs):
        self.__contain = value

    @property    
    def containIntrinsicSize(self):
        return self.__containIntrinsicSize

    @containIntrinsicSize.setter
    @style_set_decorator
    def containIntrinsicSize(self, value=None, *args, **kwargs):
        self.__containIntrinsicSize = value

    @property    
    def contentVisibility(self):
        return self.__contentVisibility

    @contentVisibility.setter
    @style_set_decorator
    def contentVisibility(self, value=None, *args, **kwargs):
        self.__contentVisibility = value

    @property    
    def counterSet(self):
        return self.__counterSet

    @counterSet.setter
    @style_set_decorator
    def counterSet(self, value=None, *args, **kwargs):
        self.__counterSet = value

    @property    
    def cx(self):
        return self.__cx

    @cx.setter
    @style_set_decorator
    def cx(self, value=None, *args, **kwargs):
        self.__cx = value

    @property    
    def cy(self):
        return self.__cy

    @cy.setter
    @style_set_decorator
    def cy(self, value=None, *args, **kwargs):
        self.__cy = value

    @property    
    def dominantBaseline(self):
        return self.__dominantBaseline

    @dominantBaseline.setter
    @style_set_decorator
    def dominantBaseline(self, value=None, *args, **kwargs):
        self.__dominantBaseline = value

    @property    
    def d(self):
        return self.__d

    @d.setter
    @style_set_decorator
    def d(self, value=None, *args, **kwargs):
        self.__d = value

    @property    
    def fill(self):
        return self.__fill

    @fill.setter
    @style_set_decorator
    def fill(self, value=None, *args, **kwargs):
        self.__fill = value

    @property    
    def fillOpacity(self):
        return self.__fillOpacity

    @fillOpacity.setter
    @style_set_decorator
    def fillOpacity(self, value=None, *args, **kwargs):
        self.__fillOpacity = value

    @property    
    def fillRule(self):
        return self.__fillRule

    @fillRule.setter
    @style_set_decorator
    def fillRule(self, value=None, *args, **kwargs):
        self.__fillRule = value

    @property    
    def fontDisplay(self):
        return self.__fontDisplay

    @fontDisplay.setter
    @style_set_decorator
    def fontDisplay(self, value=None, *args, **kwargs):
        self.__fontDisplay = value

    @property    
    def floodColor(self):
        return self.__floodColor

    @floodColor.setter
    @style_set_decorator
    def floodColor(self, value=None, *args, **kwargs):
        self.__floodColor = value

    @property    
    def floodOpacity(self):
        return self.__floodOpacity

    @floodOpacity.setter
    @style_set_decorator
    def floodOpacity(self, value=None, *args, **kwargs):
        self.__floodOpacity = value

    @property    
    def fontFeatureSettings(self):
        return self.__fontFeatureSettings

    @fontFeatureSettings.setter
    @style_set_decorator
    def fontFeatureSettings(self, value=None, *args, **kwargs):
        self.__fontFeatureSettings = value

    @property    
    def fontKerning(self):
        return self.__fontKerning

    @fontKerning.setter
    @style_set_decorator
    def fontKerning(self, value=None, *args, **kwargs):
        self.__fontKerning = value

    @property    
    def fontOpticalSizing(self):
        return self.__fontOpticalSizing

    @fontOpticalSizing.setter
    @style_set_decorator
    def fontOpticalSizing(self, value=None, *args, **kwargs):
        self.__fontOpticalSizing = value

    @property    
    def fontVariantCaps(self):
        return self.__fontVariantCaps

    @fontVariantCaps.setter
    @style_set_decorator
    def fontVariantCaps(self, value=None, *args, **kwargs):
        self.__fontVariantCaps = value

    @property    
    def fontVariantEastAsian(self):
        return self.__fontVariantEastAsian

    @fontVariantEastAsian.setter
    @style_set_decorator
    def fontVariantEastAsian(self, value=None, *args, **kwargs):
        self.__fontVariantEastAsian = value

    @property    
    def fontVariantLigatures(self):
        return self.__fontVariantLigatures

    @fontVariantLigatures.setter
    @style_set_decorator
    def fontVariantLigatures(self, value=None, *args, **kwargs):
        self.__fontVariantLigatures = value

    @property    
    def fontVariantNumeric(self):
        return self.__fontVariantNumeric

    @fontVariantNumeric.setter
    @style_set_decorator
    def fontVariantNumeric(self, value=None, *args, **kwargs):
        self.__fontVariantNumeric = value

    @property    
    def fontVariationSettings(self):
        return self.__fontVariationSettings

    @fontVariationSettings.setter
    @style_set_decorator
    def fontVariationSettings(self, value=None, *args, **kwargs):
        self.__fontVariationSettings = value

    @property    
    def gap(self):
        return self.__gap

    @gap.setter
    @style_set_decorator
    def gap(self, value=None, *args, **kwargs):
        self.__gap = value

    @property    
    def grid(self):
        return self.__grid

    @grid.setter
    @style_set_decorator
    def grid(self, value=None, *args, **kwargs):
        self.__grid = value

    @property    
    def gridArea(self):
        return self.__gridArea

    @gridArea.setter
    @style_set_decorator
    def gridArea(self, value=None, *args, **kwargs):
        self.__gridArea = value

    @property    
    def gridAutoColumns(self):
        return self.__gridAutoColumns

    @gridAutoColumns.setter
    @style_set_decorator
    def gridAutoColumns(self, value=None, *args, **kwargs):
        self.__gridAutoColumns = value

    @property    
    def gridAutoFlow(self):
        return self.__gridAutoFlow

    @gridAutoFlow.setter
    @style_set_decorator
    def gridAutoFlow(self, value=None, *args, **kwargs):
        self.__gridAutoFlow = value

    @property    
    def gridAutoRows(self):
        return self.__gridAutoRows

    @gridAutoRows.setter
    @style_set_decorator
    def gridAutoRows(self, value=None, *args, **kwargs):
        self.__gridAutoRows = value

    @property    
    def gridColumn(self):
        return self.__gridColumn

    @gridColumn.setter
    @style_set_decorator
    def gridColumn(self, value=None, *args, **kwargs):
        self.__gridColumn = value

    @property    
    def gridColumnEnd(self):
        return self.__gridColumnEnd

    @gridColumnEnd.setter
    @style_set_decorator
    def gridColumnEnd(self, value=None, *args, **kwargs):
        self.__gridColumnEnd = value

    @property    
    def gridColumnGap(self):
        return self.__gridColumnGap

    @gridColumnGap.setter
    @style_set_decorator
    def gridColumnGap(self, value=None, *args, **kwargs):
        self.__gridColumnGap = value

    @property    
    def gridColumnStart(self):
        return self.__gridColumnStart

    @gridColumnStart.setter
    @style_set_decorator
    def gridColumnStart(self, value=None, *args, **kwargs):
        self.__gridColumnStart = value

    @property    
    def gridGap(self):
        return self.__gridGap

    @gridGap.setter
    @style_set_decorator
    def gridGap(self, value=None, *args, **kwargs):
        self.__gridGap = value

    @property    
    def gridRow(self):
        return self.__gridRow

    @gridRow.setter
    @style_set_decorator
    def gridRow(self, value=None, *args, **kwargs):
        self.__gridRow = value

    @property    
    def gridRowEnd(self):
        return self.__gridRowEnd

    @gridRowEnd.setter
    @style_set_decorator
    def gridRowEnd(self, value=None, *args, **kwargs):
        self.__gridRowEnd = value

    @property    
    def gridRowGap(self):
        return self.__gridRowGap

    @gridRowGap.setter
    @style_set_decorator
    def gridRowGap(self, value=None, *args, **kwargs):
        self.__gridRowGap = value

    @property    
    def gridRowStart(self):
        return self.__gridRowStart

    @gridRowStart.setter
    @style_set_decorator
    def gridRowStart(self, value=None, *args, **kwargs):
        self.__gridRowStart = value

    @property    
    def gridTemplate(self):
        return self.__gridTemplate

    @gridTemplate.setter
    @style_set_decorator
    def gridTemplate(self, value=None, *args, **kwargs):
        self.__gridTemplate = value

    @property    
    def gridTemplateAreas(self):
        return self.__gridTemplateAreas

    @gridTemplateAreas.setter
    @style_set_decorator
    def gridTemplateAreas(self, value=None, *args, **kwargs):
        self.__gridTemplateAreas = value

    @property    
    def gridTemplateColumns(self):
        return self.__gridTemplateColumns

    @gridTemplateColumns.setter
    @style_set_decorator
    def gridTemplateColumns(self, value=None, *args, **kwargs):
        self.__gridTemplateColumns = value

    @property    
    def gridTemplateRows(self):
        return self.__gridTemplateRows

    @gridTemplateRows.setter
    @style_set_decorator
    def gridTemplateRows(self, value=None, *args, **kwargs):
        self.__gridTemplateRows = value

    @property    
    def imageRendering(self):
        return self.__imageRendering

    @imageRendering.setter
    @style_set_decorator
    def imageRendering(self, value=None, *args, **kwargs):
        self.__imageRendering = value

    @property    
    def inherits(self):
        return self.__inherits

    @inherits.setter
    @style_set_decorator
    def inherits(self, value=None, *args, **kwargs):
        self.__inherits = value

    @property    
    def initialValue(self):
        return self.__initialValue

    @initialValue.setter
    @style_set_decorator
    def initialValue(self, value=None, *args, **kwargs):
        self.__initialValue = value

    @property    
    def inlineSize(self):
        return self.__inlineSize

    @inlineSize.setter
    @style_set_decorator
    def inlineSize(self, value=None, *args, **kwargs):
        self.__inlineSize = value

    @property    
    def justifyItems(self):
        return self.__justifyItems

    @justifyItems.setter
    @style_set_decorator
    def justifyItems(self, value=None, *args, **kwargs):
        self.__justifyItems = value

    @property    
    def justifySelf(self):
        return self.__justifySelf

    @justifySelf.setter
    @style_set_decorator
    def justifySelf(self, value=None, *args, **kwargs):
        self.__justifySelf = value

    @property    
    def lightingColor(self):
        return self.__lightingColor

    @lightingColor.setter
    @style_set_decorator
    def lightingColor(self, value=None, *args, **kwargs):
        self.__lightingColor = value

    @property    
    def lineBreak(self):
        return self.__lineBreak

    @lineBreak.setter
    @style_set_decorator
    def lineBreak(self, value=None, *args, **kwargs):
        self.__lineBreak = value

    @property    
    def marginBlockEnd(self):
        return self.__marginBlockEnd

    @marginBlockEnd.setter
    @style_set_decorator
    def marginBlockEnd(self, value=None, *args, **kwargs):
        self.__marginBlockEnd = value

    @property    
    def marginBlockStart(self):
        return self.__marginBlockStart

    @marginBlockStart.setter
    @style_set_decorator
    def marginBlockStart(self, value=None, *args, **kwargs):
        self.__marginBlockStart = value

    @property    
    def marginInlineEnd(self):
        return self.__marginInlineEnd

    @marginInlineEnd.setter
    @style_set_decorator
    def marginInlineEnd(self, value=None, *args, **kwargs):
        self.__marginInlineEnd = value

    @property    
    def marginInlineStart(self):
        return self.__marginInlineStart

    @marginInlineStart.setter
    @style_set_decorator
    def marginInlineStart(self, value=None, *args, **kwargs):
        self.__marginInlineStart = value

    @property    
    def marker(self):
        return self.__marker

    @marker.setter
    @style_set_decorator
    def marker(self, value=None, *args, **kwargs):
        self.__marker = value

    @property    
    def markerEnd(self):
        return self.__markerEnd

    @markerEnd.setter
    @style_set_decorator
    def markerEnd(self, value=None, *args, **kwargs):
        self.__markerEnd = value

    @property    
    def markerMid(self):
        return self.__markerMid

    @markerMid.setter
    @style_set_decorator
    def markerMid(self, value=None, *args, **kwargs):
        self.__markerMid = value

    @property    
    def markerStart(self):
        return self.__markerStart

    @markerStart.setter
    @style_set_decorator
    def markerStart(self, value=None, *args, **kwargs):
        self.__markerStart = value

    @property    
    def mask(self):
        return self.__mask

    @mask.setter
    @style_set_decorator
    def mask(self, value=None, *args, **kwargs):
        self.__mask = value

    @property    
    def maskType(self):
        return self.__maskType

    @maskType.setter
    @style_set_decorator
    def maskType(self, value=None, *args, **kwargs):
        self.__maskType = value

    @property    
    def maxBlockSize(self):
        return self.__maxBlockSize

    @maxBlockSize.setter
    @style_set_decorator
    def maxBlockSize(self, value=None, *args, **kwargs):
        self.__maxBlockSize = value

    @property    
    def maxInlineSize(self):
        return self.__maxInlineSize

    @maxInlineSize.setter
    @style_set_decorator
    def maxInlineSize(self, value=None, *args, **kwargs):
        self.__maxInlineSize = value

    @property    
    def maxZoom(self):
        return self.__maxZoom

    @maxZoom.setter
    @style_set_decorator
    def maxZoom(self, value=None, *args, **kwargs):
        self.__maxZoom = value

    @property    
    def minBlockSize(self):
        return self.__minBlockSize

    @minBlockSize.setter
    @style_set_decorator
    def minBlockSize(self, value=None, *args, **kwargs):
        self.__minBlockSize = value

    @property    
    def minInlineSize(self):
        return self.__minInlineSize

    @minInlineSize.setter
    @style_set_decorator
    def minInlineSize(self, value=None, *args, **kwargs):
        self.__minInlineSize = value

    @property    
    def minZoom(self):
        return self.__minZoom

    @minZoom.setter
    @style_set_decorator
    def minZoom(self, value=None, *args, **kwargs):
        self.__minZoom = value

    @property    
    def mixBlendMode(self):
        return self.__mixBlendMode

    @mixBlendMode.setter
    @style_set_decorator
    def mixBlendMode(self, value=None, *args, **kwargs):
        self.__mixBlendMode = value

    @property    
    def objectFit(self):
        return self.__objectFit

    @objectFit.setter
    @style_set_decorator
    def objectFit(self, value=None, *args, **kwargs):
        self.__objectFit = value

    @property    
    def objectPosition(self):
        return self.__objectPosition

    @objectPosition.setter
    @style_set_decorator
    def objectPosition(self, value=None, *args, **kwargs):
        self.__objectPosition = value

    @property    
    def offset(self):
        return self.__offset

    @offset.setter
    @style_set_decorator
    def offset(self, value=None, *args, **kwargs):
        self.__offset = value

    @property    
    def offsetDistance(self):
        return self.__offsetDistance

    @offsetDistance.setter
    @style_set_decorator
    def offsetDistance(self, value=None, *args, **kwargs):
        self.__offsetDistance = value

    @property    
    def offsetPath(self):
        return self.__offsetPath

    @offsetPath.setter
    @style_set_decorator
    def offsetPath(self, value=None, *args, **kwargs):
        self.__offsetPath = value

    @property    
    def offsetRotate(self):
        return self.__offsetRotate

    @offsetRotate.setter
    @style_set_decorator
    def offsetRotate(self, value=None, *args, **kwargs):
        self.__offsetRotate = value

    @property    
    def orientation(self):
        return self.__orientation

    @orientation.setter
    @style_set_decorator
    def orientation(self, value=None, *args, **kwargs):
        self.__orientation = value

    @property    
    def overflowAnchor(self):
        return self.__overflowAnchor

    @overflowAnchor.setter
    @style_set_decorator
    def overflowAnchor(self, value=None, *args, **kwargs):
        self.__overflowAnchor = value

    @property    
    def overflowWrap(self):
        return self.__overflowWrap

    @overflowWrap.setter
    @style_set_decorator
    def overflowWrap(self, value=None, *args, **kwargs):
        self.__overflowWrap = value

    @property    
    def overscrollBehavior(self):
        return self.__overscrollBehavior

    @overscrollBehavior.setter
    @style_set_decorator
    def overscrollBehavior(self, value=None, *args, **kwargs):
        self.__overscrollBehavior = value

    @property    
    def overscrollBehaviorBlock(self):
        return self.__overscrollBehaviorBlock

    @overscrollBehaviorBlock.setter
    @style_set_decorator
    def overscrollBehaviorBlock(self, value=None, *args, **kwargs):
        self.__overscrollBehaviorBlock = value

    @property    
    def overscrollBehaviorInline(self):
        return self.__overscrollBehaviorInline

    @overscrollBehaviorInline.setter
    @style_set_decorator
    def overscrollBehaviorInline(self, value=None, *args, **kwargs):
        self.__overscrollBehaviorInline = value

    @property    
    def overscrollBehaviorX(self):
        return self.__overscrollBehaviorX

    @overscrollBehaviorX.setter
    @style_set_decorator
    def overscrollBehaviorX(self, value=None, *args, **kwargs):
        self.__overscrollBehaviorX = value

    @property    
    def overscrollBehaviorY(self):
        return self.__overscrollBehaviorY

    @overscrollBehaviorY.setter
    @style_set_decorator
    def overscrollBehaviorY(self, value=None, *args, **kwargs):
        self.__overscrollBehaviorY = value

    @property    
    def paddingBlockEnd(self):
        return self.__paddingBlockEnd

    @paddingBlockEnd.setter
    @style_set_decorator
    def paddingBlockEnd(self, value=None, *args, **kwargs):
        self.__paddingBlockEnd = value

    @property    
    def paddingBlockStart(self):
        return self.__paddingBlockStart

    @paddingBlockStart.setter
    @style_set_decorator
    def paddingBlockStart(self, value=None, *args, **kwargs):
        self.__paddingBlockStart = value

    @property    
    def paddingInlineEnd(self):
        return self.__paddingInlineEnd

    @paddingInlineEnd.setter
    @style_set_decorator
    def paddingInlineEnd(self, value=None, *args, **kwargs):
        self.__paddingInlineEnd = value

    @property    
    def paddingInlineStart(self):
        return self.__paddingInlineStart

    @paddingInlineStart.setter
    @style_set_decorator
    def paddingInlineStart(self, value=None, *args, **kwargs):
        self.__paddingInlineStart = value

    @property    
    def page(self):
        return self.__page

    @page.setter
    @style_set_decorator
    def page(self, value=None, *args, **kwargs):
        self.__page = value

    @property    
    def pageOrientation(self):
        return self.__pageOrientation

    @pageOrientation.setter
    @style_set_decorator
    def pageOrientation(self, value=None, *args, **kwargs):
        self.__pageOrientation = value

    @property    
    def paintOrder(self):
        return self.__paintOrder

    @paintOrder.setter
    @style_set_decorator
    def paintOrder(self, value=None, *args, **kwargs):
        self.__paintOrder = value

    @property    
    def placeContent(self):
        return self.__placeContent

    @placeContent.setter
    @style_set_decorator
    def placeContent(self, value=None, *args, **kwargs):
        self.__placeContent = value

    @property    
    def placeItems(self):
        return self.__placeItems

    @placeItems.setter
    @style_set_decorator
    def placeItems(self, value=None, *args, **kwargs):
        self.__placeItems = value

    @property    
    def placeSelf(self):
        return self.__placeSelf

    @placeSelf.setter
    @style_set_decorator
    def placeSelf(self, value=None, *args, **kwargs):
        self.__placeSelf = value

    @property    
    def pointerEvents(self):
        return self.__pointerEvents

    @pointerEvents.setter
    @style_set_decorator
    def pointerEvents(self, value=None, *args, **kwargs):
        self.__pointerEvents = value

    @property    
    def r(self):
        return self.__r

    @r.setter
    @style_set_decorator
    def r(self, value=None, *args, **kwargs):
        self.__r = value

    @property    
    def rowGap(self):
        return self.__rowGap

    @rowGap.setter
    @style_set_decorator
    def rowGap(self, value=None, *args, **kwargs):
        self.__rowGap = value

    @property    
    def rubyPosition(self):
        return self.__rubyPosition

    @rubyPosition.setter
    @style_set_decorator
    def rubyPosition(self, value=None, *args, **kwargs):
        self.__rubyPosition = value

    @property    
    def rx(self):
        return self.__rx

    @rx.setter
    @style_set_decorator
    def rx(self, value=None, *args, **kwargs):
        self.__rx = value

    @property    
    def ry(self):
        return self.__ry

    @ry.setter
    @style_set_decorator
    def ry(self, value=None, *args, **kwargs):
        self.__ry = value

    @property    
    def scrollBehavior(self):
        return self.__scrollBehavior

    @scrollBehavior.setter
    @style_set_decorator
    def scrollBehavior(self, value=None, *args, **kwargs):
        self.__scrollBehavior = value

    @property    
    def scrollMargin(self):
        return self.__scrollMargin

    @scrollMargin.setter
    @style_set_decorator
    def scrollMargin(self, value=None, *args, **kwargs):
        self.__scrollMargin = value

    @property    
    def scrollMarginBlock(self):
        return self.__scrollMarginBlock

    @scrollMarginBlock.setter
    @style_set_decorator
    def scrollMarginBlock(self, value=None, *args, **kwargs):
        self.__scrollMarginBlock = value

    @property    
    def scrollMarginBlockEnd(self):
        return self.__scrollMarginBlockEnd

    @scrollMarginBlockEnd.setter
    @style_set_decorator
    def scrollMarginBlockEnd(self, value=None, *args, **kwargs):
        self.__scrollMarginBlockEnd = value

    @property    
    def scrollMarginBlockStart(self):
        return self.__scrollMarginBlockStart

    @scrollMarginBlockStart.setter
    @style_set_decorator
    def scrollMarginBlockStart(self, value=None, *args, **kwargs):
        self.__scrollMarginBlockStart = value

    @property    
    def scrollMarginBottom(self):
        return self.__scrollMarginBottom

    @scrollMarginBottom.setter
    @style_set_decorator
    def scrollMarginBottom(self, value=None, *args, **kwargs):
        self.__scrollMarginBottom = value

    @property    
    def scrollMarginInline(self):
        return self.__scrollMarginInline

    @scrollMarginInline.setter
    @style_set_decorator
    def scrollMarginInline(self, value=None, *args, **kwargs):
        self.__scrollMarginInline = value

    @property    
    def scrollMarginInlineEnd(self):
        return self.__scrollMarginInlineEnd

    @scrollMarginInlineEnd.setter
    @style_set_decorator
    def scrollMarginInlineEnd(self, value=None, *args, **kwargs):
        self.__scrollMarginInlineEnd = value

    @property    
    def scrollMarginInlineStart(self):
        return self.__scrollMarginInlineStart

    @scrollMarginInlineStart.setter
    @style_set_decorator
    def scrollMarginInlineStart(self, value=None, *args, **kwargs):
        self.__scrollMarginInlineStart = value

    @property    
    def scrollMarginLeft(self):
        return self.__scrollMarginLeft

    @scrollMarginLeft.setter
    @style_set_decorator
    def scrollMarginLeft(self, value=None, *args, **kwargs):
        self.__scrollMarginLeft = value

    @property    
    def scrollMarginRight(self):
        return self.__scrollMarginRight

    @scrollMarginRight.setter
    @style_set_decorator
    def scrollMarginRight(self, value=None, *args, **kwargs):
        self.__scrollMarginRight = value

    @property    
    def scrollMarginTop(self):
        return self.__scrollMarginTop

    @scrollMarginTop.setter
    @style_set_decorator
    def scrollMarginTop(self, value=None, *args, **kwargs):
        self.__scrollMarginTop = value

    @property    
    def scrollPadding(self):
        return self.__scrollPadding

    @scrollPadding.setter
    @style_set_decorator
    def scrollPadding(self, value=None, *args, **kwargs):
        self.__scrollPadding = value

    @property    
    def scrollPaddingBlock(self):
        return self.__scrollPaddingBlock

    @scrollPaddingBlock.setter
    @style_set_decorator
    def scrollPaddingBlock(self, value=None, *args, **kwargs):
        self.__scrollPaddingBlock = value

    @property    
    def scrollPaddingBlockEnd(self):
        return self.__scrollPaddingBlockEnd

    @scrollPaddingBlockEnd.setter
    @style_set_decorator
    def scrollPaddingBlockEnd(self, value=None, *args, **kwargs):
        self.__scrollPaddingBlockEnd = value

    @property    
    def scrollPaddingBlockStart(self):
        return self.__scrollPaddingBlockStart

    @scrollPaddingBlockStart.setter
    @style_set_decorator
    def scrollPaddingBlockStart(self, value=None, *args, **kwargs):
        self.__scrollPaddingBlockStart = value

    @property    
    def scrollPaddingBottom(self):
        return self.__scrollPaddingBottom

    @scrollPaddingBottom.setter
    @style_set_decorator
    def scrollPaddingBottom(self, value=None, *args, **kwargs):
        self.__scrollPaddingBottom = value

    @property    
    def scrollPaddingInline(self):
        return self.__scrollPaddingInline

    @scrollPaddingInline.setter
    @style_set_decorator
    def scrollPaddingInline(self, value=None, *args, **kwargs):
        self.__scrollPaddingInline = value

    @property    
    def scrollPaddingInlineEnd(self):
        return self.__scrollPaddingInlineEnd

    @scrollPaddingInlineEnd.setter
    @style_set_decorator
    def scrollPaddingInlineEnd(self, value=None, *args, **kwargs):
        self.__scrollPaddingInlineEnd = value

    @property    
    def scrollPaddingInlineStart(self):
        return self.__scrollPaddingInlineStart

    @scrollPaddingInlineStart.setter
    @style_set_decorator
    def scrollPaddingInlineStart(self, value=None, *args, **kwargs):
        self.__scrollPaddingInlineStart = value

    @property    
    def scrollPaddingLeft(self):
        return self.__scrollPaddingLeft

    @scrollPaddingLeft.setter
    @style_set_decorator
    def scrollPaddingLeft(self, value=None, *args, **kwargs):
        self.__scrollPaddingLeft = value

    @property    
    def scrollPaddingRight(self):
        return self.__scrollPaddingRight

    @scrollPaddingRight.setter
    @style_set_decorator
    def scrollPaddingRight(self, value=None, *args, **kwargs):
        self.__scrollPaddingRight = value

    @property    
    def scrollPaddingTop(self):
        return self.__scrollPaddingTop

    @scrollPaddingTop.setter
    @style_set_decorator
    def scrollPaddingTop(self, value=None, *args, **kwargs):
        self.__scrollPaddingTop = value

    @property    
    def scrollSnapAlign(self):
        return self.__scrollSnapAlign

    @scrollSnapAlign.setter
    @style_set_decorator
    def scrollSnapAlign(self, value=None, *args, **kwargs):
        self.__scrollSnapAlign = value

    @property    
    def scrollSnapStop(self):
        return self.__scrollSnapStop

    @scrollSnapStop.setter
    @style_set_decorator
    def scrollSnapStop(self, value=None, *args, **kwargs):
        self.__scrollSnapStop = value

    @property    
    def scrollSnapType(self):
        return self.__scrollSnapType

    @scrollSnapType.setter
    @style_set_decorator
    def scrollSnapType(self, value=None, *args, **kwargs):
        self.__scrollSnapType = value

    @property    
    def shapeImageThreshold(self):
        return self.__shapeImageThreshold

    @shapeImageThreshold.setter
    @style_set_decorator
    def shapeImageThreshold(self, value=None, *args, **kwargs):
        self.__shapeImageThreshold = value

    @property    
    def shapeMargin(self):
        return self.__shapeMargin

    @shapeMargin.setter
    @style_set_decorator
    def shapeMargin(self, value=None, *args, **kwargs):
        self.__shapeMargin = value

    @property    
    def shapeOutside(self):
        return self.__shapeOutside

    @shapeOutside.setter
    @style_set_decorator
    def shapeOutside(self, value=None, *args, **kwargs):
        self.__shapeOutside = value

    @property    
    def shapeRendering(self):
        return self.__shapeRendering

    @shapeRendering.setter
    @style_set_decorator
    def shapeRendering(self, value=None, *args, **kwargs):
        self.__shapeRendering = value

    @property    
    def size(self):
        return self.__size

    @size.setter
    @style_set_decorator
    def size(self, value=None, *args, **kwargs):
        self.__size = value

    @property    
    def speak(self):
        return self.__speak

    @speak.setter
    @style_set_decorator
    def speak(self, value=None, *args, **kwargs):
        self.__speak = value

    @property    
    def src(self):
        return self.__src

    @src.setter
    @style_set_decorator
    def src(self, value=None, *args, **kwargs):
        self.__src = value

    @property    
    def stopColor(self):
        return self.__stopColor

    @stopColor.setter
    @style_set_decorator
    def stopColor(self, value=None, *args, **kwargs):
        self.__stopColor = value

    @property    
    def stopOpacity(self):
        return self.__stopOpacity

    @stopOpacity.setter
    @style_set_decorator
    def stopOpacity(self, value=None, *args, **kwargs):
        self.__stopOpacity = value

    @property    
    def stroke(self):
        return self.__stroke

    @stroke.setter
    @style_set_decorator
    def stroke(self, value=None, *args, **kwargs):
        self.__stroke = value

    @property    
    def strokeDasharray(self):
        return self.__strokeDasharray

    @strokeDasharray.setter
    @style_set_decorator
    def strokeDasharray(self, value=None, *args, **kwargs):
        self.__strokeDasharray = value

    @property    
    def strokeDashoffset(self):
        return self.__strokeDashoffset

    @strokeDashoffset.setter
    @style_set_decorator
    def strokeDashoffset(self, value=None, *args, **kwargs):
        self.__strokeDashoffset = value

    @property    
    def strokeLinecap(self):
        return self.__strokeLinecap

    @strokeLinecap.setter
    @style_set_decorator
    def strokeLinecap(self, value=None, *args, **kwargs):
        self.__strokeLinecap = value

    @property    
    def strokeLinejoin(self):
        return self.__strokeLinejoin

    @strokeLinejoin.setter
    @style_set_decorator
    def strokeLinejoin(self, value=None, *args, **kwargs):
        self.__strokeLinejoin = value

    @property    
    def strokeMiterlimit(self):
        return self.__strokeMiterlimit

    @strokeMiterlimit.setter
    @style_set_decorator
    def strokeMiterlimit(self, value=None, *args, **kwargs):
        self.__strokeMiterlimit = value

    @property    
    def strokeOpacity(self):
        return self.__strokeOpacity

    @strokeOpacity.setter
    @style_set_decorator
    def strokeOpacity(self, value=None, *args, **kwargs):
        self.__strokeOpacity = value

    @property    
    def strokeWidth(self):
        return self.__strokeWidth

    @strokeWidth.setter
    @style_set_decorator
    def strokeWidth(self, value=None, *args, **kwargs):
        self.__strokeWidth = value

    @property    
    def syntax(self):
        return self.__syntax

    @syntax.setter
    @style_set_decorator
    def syntax(self, value=None, *args, **kwargs):
        self.__syntax = value

    @property    
    def textAnchor(self):
        return self.__textAnchor

    @textAnchor.setter
    @style_set_decorator
    def textAnchor(self, value=None, *args, **kwargs):
        self.__textAnchor = value

    @property    
    def textCombineUpright(self):
        return self.__textCombineUpright

    @textCombineUpright.setter
    @style_set_decorator
    def textCombineUpright(self, value=None, *args, **kwargs):
        self.__textCombineUpright = value

    @property    
    def textDecorationSkipInk(self):
        return self.__textDecorationSkipInk

    @textDecorationSkipInk.setter
    @style_set_decorator
    def textDecorationSkipInk(self, value=None, *args, **kwargs):
        self.__textDecorationSkipInk = value

    @property    
    def textOrientation(self):
        return self.__textOrientation

    @textOrientation.setter
    @style_set_decorator
    def textOrientation(self, value=None, *args, **kwargs):
        self.__textOrientation = value

    @property    
    def textRendering(self):
        return self.__textRendering

    @textRendering.setter
    @style_set_decorator
    def textRendering(self, value=None, *args, **kwargs):
        self.__textRendering = value

    @property    
    def textSizeAdjust(self):
        return self.__textSizeAdjust

    @textSizeAdjust.setter
    @style_set_decorator
    def textSizeAdjust(self, value=None, *args, **kwargs):
        self.__textSizeAdjust = value

    @property    
    def textUnderlinePosition(self):
        return self.__textUnderlinePosition

    @textUnderlinePosition.setter
    @style_set_decorator
    def textUnderlinePosition(self, value=None, *args, **kwargs):
        self.__textUnderlinePosition = value

    @property    
    def touchAction(self):
        return self.__touchAction

    @touchAction.setter
    @style_set_decorator
    def touchAction(self, value=None, *args, **kwargs):
        self.__touchAction = value

    @property    
    def transformBox(self):
        return self.__transformBox

    @transformBox.setter
    @style_set_decorator
    def transformBox(self, value=None, *args, **kwargs):
        self.__transformBox = value

    @property    
    def unicodeRange(self):
        return self.__unicodeRange

    @unicodeRange.setter
    @style_set_decorator
    def unicodeRange(self, value=None, *args, **kwargs):
        self.__unicodeRange = value

    @property    
    def userZoom(self):
        return self.__userZoom

    @userZoom.setter
    @style_set_decorator
    def userZoom(self, value=None, *args, **kwargs):
        self.__userZoom = value

    @property    
    def vectorEffect(self):
        return self.__vectorEffect

    @vectorEffect.setter
    @style_set_decorator
    def vectorEffect(self, value=None, *args, **kwargs):
        self.__vectorEffect = value

    @property    
    def willChange(self):
        return self.__willChange

    @willChange.setter
    @style_set_decorator
    def willChange(self, value=None, *args, **kwargs):
        self.__willChange = value

    @property    
    def writingMode(self):
        return self.__writingMode

    @writingMode.setter
    @style_set_decorator
    def writingMode(self, value=None, *args, **kwargs):
        self.__writingMode = value

    @property    
    def x(self):
        return self.__x

    @x.setter
    @style_set_decorator
    def x(self, value=None, *args, **kwargs):
        self.__x = value

    @property    
    def y(self):
        return self.__y

    @y.setter
    @style_set_decorator
    def y(self, value=None, *args, **kwargs):
        self.__y = value

    @property
    @style_get_decorator
    def zoom(self):
        return self.__zoom

    @zoom.setter
    @style_set_decorator
    def zoom(self, value=None, *args, **kwargs):
        self.__zoom = value

    # @property
    # @style_get_decorator
    # def zoomAndPan(self):
    #     return self.__zoomAndPan

    # @zoomAndPan.setter
    # @style_set_decorator
    # def zoomAndPan(self, value=None, *args, **kwargs):
    #     self.__zoomAndPan = value

    # @property
    # @style_get_decorator
    # def zoomAndResize(self):
    #     return self.__zoomAndResize

    # @zoomAndResize.setter
    # @style_set_decorator
    # def zoomAndResize(self, value=None, *args, **kwargs):
    #     self.__zoomAndResize = value

    # @property
    # @style_get_decorator
    # def zoomType(self):
    #     return self.__zoomType

    # @zoomType.setter
    # @style_set_decorator
    # def zoomType(self, value=None, *args, **kwargs):
    #     self.__zoomType = value

    # Modifies an existing CSS property or creates a new CSS property in the declaration block. """
    # def setProperty(self, property, value):
    # self[property] = value



class CSSStyleDeclaration(Style):
    """The CSSStyleDeclaration interface represents an object that is a CSS declaration block,
    and exposes style information and various style-related methods and properties.

    A CSSStyleDeclaration object can be exposed using three different APIs:

    Via HTMLElement.style, which deals with the inline styles of a single element (e.g., <div style="...">).
    Via the CSSStyleSheet API. For example, document.styleSheets[0].cssRules[0].style
    returns a CSSStyleDeclaration object on the first CSS rule in the document's first stylesheet.
    Via Window.getComputedStyle(), which exposes the CSSStyleDeclaration object as a read-only interface.
    """

    def __init__(self, parentNode=None, *args, **kwargs):
        # print("*** MADE A STYLE ***")
        # super(Style).__init__(*args, **kwargs)
        super().__init__(parentNode, *args, **kwargs)
        # self.__parentNode = parentNode
        # self.__cssText = None
        self.parentRule = None
        self.cssText = None

    # @property
    # def cssText(self):
    #     """Textual representation of the declaration block, if and only if it is exposed via HTMLElement.style.
    #     Setting this attribute changes the inline style.
    #     If you want a text representation of a computed declaration block,
    #     you can get it with JSON.stringify()."""
    #     raise NotImplementedError

    @property
    def length(self):
        """The number of properties. See the item() method below."""
        raise NotImplementedError

    # @property
    # def parentRule(self):
    #     """The containing CSSRule."""
    #     return self.__parentRule

    # @parentRule.setter
    # def parentRule(self, value=None, *args, **kwargs):
    #     self.__parentRule = value

    # @property
    # def cssFloat(self):
    #     """ Special alias for the float CSS property. """
    #     raise NotImplementedError

    def getPropertyPriority(self):
        """Returns the optional priority, "important"."""
        raise NotImplementedError

    def getPropertyValue(self, propertyName: str) -> str:  # TODO - test
        """Returns the value of the property with the specified name."""
        raise NotImplementedError

    def item(self, index: int) -> str:
        """Returns a CSS property name by its index, or the empty string if the index is out-of-bounds.
        An alternative to accessing nodeList[i] (which instead returns undefined when i is out-of-bounds).
        This is mostly useful for non-JavaScript DOM implementations.
        """
        raise NotImplementedError

    def removeProperty(self):
        """Removes a property from the CSS declaration block."""
        raise NotImplementedError

    # Modifies an existing CSS property or creates a new CSS property in the declaration block. """
    def setProperty(self, property, value, priority=None):
        # print("is this magic!")
        # self[property] = value
        setattr(self, property, value)

    def getPropertyCSSValue(self):
        """ Only supported via getComputedStyle in Firefox. Returns the property value as a
        CSSPrimitiveValue or null for shorthand properties."""
        raise NotImplementedError


COMMENT_REGEXP = r'/\/\*[^*]*\*\//gm'

class CSSParser:

    @staticmethod
    def parseFromString(parentStyleSheet: CSSStyleSheet, cssText: str): 
        css = cssText.replace(COMMENT_REGEXP, '')
        cssRules = []
        stack = []
        parentRule: CSSRule = None
        lastIndex = 0
        match = None

        def matches(s: str):
            regExp = r'{|}'
            class Match:
                def __init__(self, index: int, match: str):
                    self.index = index
                    self.match = match
                def __str__(self):
                    return f'{self.match}'
                def __repr__(self):
                    return f'{self.match}'
                def __getitem__(self, index):
                    return self.match[index]

            import re
            matches = re.finditer(regExp, s, flags=re.MULTILINE)
            return [Match(m.start(), m.group(0)) for m in matches]

        for count, match in enumerate(matches(css)):
            if (match[0] == '{'):
                selectorText = css[lastIndex:match.index].strip()
                if selectorText.startswith('@keyframes'):
                    newRule = CSSKeyframesRule()
                    newRule.name = selectorText.replace('@keyframes ', '')
                    newRule.parentStyleSheet = parentStyleSheet
                    cssRules.append(newRule)
                    parentRule = newRule
                elif selectorText.startswith('@media'):
                    mediums = selectorText.replace('@media', '').split(',')
                    newRule = CSSMediaRule()
                    for medium in mediums:
                        newRule.media.appendMedium(medium.strip())
                    newRule.parentStyleSheet = parentStyleSheet
                    cssRules.append(newRule)
                    parentRule = newRule
                elif parentRule is not None and parentRule.type == CSSRule.KEYFRAMES_RULE:
                    newRule = CSSKeyframeRule()
                    newRule.keyText = selectorText.strip()
                    newRule.parentStyleSheet = parentStyleSheet
                    newRule.parentRule = parentRule
                    parentRule.cssRules.append(newRule)
                    parentRule = newRule
                elif parentRule is not None and parentRule.type == CSSRule.MEDIA_RULE:
                    newRule = CSSStyleRule()
                    newRule.selectorText = selectorText
                    newRule.parentStyleSheet = parentStyleSheet
                    newRule.parentRule = parentRule
                    parentRule.cssRules.append(newRule)
                    parentRule = newRule
                else:
                    newRule = CSSStyleRule()
                    newRule.selectorText = selectorText
                    newRule.parentStyleSheet = parentStyleSheet
                    newRule.parentRule = parentRule
                    if not parentRule:
                        cssRules.append(newRule)
                    parentRule = newRule
                stack.append(parentRule)
            else:
                if parentRule is not None:
                    cssText = css[lastIndex:match.index].strip()
                    import re
                    cssText = re.sub(' +', ' ', cssText)
                    cssText = re.sub('\n', '', cssText)
                    if parentRule.type == CSSRule.FONT_FACE_RULE or parentRule.type == CSSRule.KEYFRAME_RULE or parentRule.type == CSSRule.STYLE_RULE:
                            style = CSSStyleDeclaration()
                            style.cssText = cssText
                            style.parentRule = parentRule
                            parentRule.style = style
                            # print('break')

                stack.pop()
                parentRule = stack[-1] if stack else None
            lastIndex = match.index + 1
        return cssRules
