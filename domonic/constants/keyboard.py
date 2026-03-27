class KeyCode:
    """Class representing keyboard key codes."""

    # Alphabet keys
    A: str = "65"
    B: str = "66"
    C: str = "67"
    D: str = "68"
    E: str = "69"
    F: str = "70"
    G: str = "71"
    H: str = "72"
    I: str = "73"
    J: str = "74"
    K: str = "75"
    L: str = "76"
    M: str = "77"
    N: str = "78"
    O: str = "79"
    P: str = "80"
    Q: str = "81"
    R: str = "82"
    S: str = "83"
    T: str = "84"
    U: str = "85"
    V: str = "86"
    W: str = "87"
    X: str = "88"
    Y: str = "89"
    Z: str = "90"

    # Numeric keys
    NUMBER_0: str = "48"
    NUMBER_1: str = "49"
    NUMBER_2: str = "50"
    NUMBER_3: str = "51"
    NUMBER_4: str = "52"
    NUMBER_5: str = "53"
    NUMBER_6: str = "54"
    NUMBER_7: str = "55"
    NUMBER_8: str = "56"
    NUMBER_9: str = "57"

    # Numpad keys
    NUMPAD: str = "21"
    NUMPAD_0: str = "96"
    NUMPAD_1: str = "97"
    NUMPAD_2: str = "98"
    NUMPAD_3: str = "99"
    NUMPAD_4: str = "100"
    NUMPAD_5: str = "101"
    NUMPAD_6: str = "102"
    NUMPAD_7: str = "103"
    NUMPAD_8: str = "104"
    NUMPAD_9: str = "105"
    NUMPAD_ADD: str = "107"
    NUMPAD_DECIMAL: str = "110"
    NUMPAD_DIVIDE: str = "111"
    NUMPAD_ENTER: str = "108"
    NUMPAD_MULTIPLY: str = "106"
    NUMPAD_SUBTRACT: str = "109"

    # Special characters
    EXCLAMATION: str = "49"  # Shift + 1
    AT: str = "50"  # Shift + 2
    HASH: str = "51"  # Shift + 3
    DOLLAR: str = "52"  # Shift + 4
    PERCENT: str = "53"  # Shift + 5
    CARET: str = "54"  # Shift + 6
    AMPERSAND: str = "55"  # Shift + 7
    STAR: str = "56"  # Shift + 8
    LEFT_PARENTHESIS: str = "57"  # Shift + 9
    RIGHT_PARENTHESIS: str = "48"  # Shift + 0
    UNDERSCORE: str = "189"  # Shift + -
    PLUS: str = "187"  # Shift + =
    LEFT_CURLY_BRACKET: str = "219"  # Shift + [
    RIGHT_CURLY_BRACKET: str = "221"  # Shift + ]
    PIPE: str = "220"  # Shift + \
    COLON: str = "186"  # Shift + ;
    DOUBLE_QUOTE: str = "222"  # Shift + '
    LESS_THAN: str = "188"  # Shift + ,
    GREATER_THAN: str = "190"  # Shift + .
    QUESTION_MARK: str = "191"  # Shift + /

    # Function keys
    F1: str = "112"
    F2: str = "113"
    F3: str = "114"
    F4: str = "115"
    F5: str = "116"
    F6: str = "117"
    F7: str = "118"
    F8: str = "119"
    F9: str = "120"
    F10: str = "121"
    F11: str = "122"
    F12: str = "123"
    F13: str = "124"
    F14: str = "125"
    F15: str = "126"

    # Control keys
    BACKSPACE: str = "8"
    CAPS_LOCK: str = "20"
    COMMA: str = "188"
    COMMAND: str = "15"
    CONTROL: str = "17"
    DELETE: str = "46"
    DOWN: str = "40"
    END: str = "35"
    ENTER: str = "13"
    RETURN: str = "13"
    EQUAL: str = "187"
    ESCAPE: str = "27"
    HOME: str = "36"
    INSERT: str = "45"
    LEFT: str = "37"
    LEFTBRACKET: str = "219"
    MINUS: str = "189"
    PAGE_DOWN: str = "34"
    PAGE_UP: str = "33"
    PERIOD: str = "190"
    QUOTE: str = "222"
    RIGHT: str = "39"
    RIGHTBRACKET: str = "221"
    SEMICOLON: str = "186"
    SHIFT: str = "16"  #: ?? left or right or both?
    SLASH: str = "191"
    SPACE: str = "32"
    TAB: str = "9"
    UP: str = "38"

    # Modifier keys
    LEFT_SHIFT: str = "16L"
    RIGHT_SHIFT: str = "16R"
    LEFT_CONTROL: str = "17L"
    RIGHT_CONTROL: str = "17R"
    LEFT_ALT: str = "18L"
    RIGHT_ALT: str = "18R"
    LEFT_COMMAND: str = "91L"  # Left Apple/Command key
    RIGHT_COMMAND: str = "93R"  # Right Apple/Command key
    FN: str = "255"  # Fn key

    # Media Control Keys
    VOLUME_UP: str = "175"
    VOLUME_DOWN: str = "174"
    MUTE: str = "173"
    PLAY_PAUSE: str = "179"
    NEXT_TRACK: str = "176"
    PREVIOUS_TRACK: str = "177"

    # Special Keys
    WINDOWS: str = "91"  # Windows key
    MENU: str = "93"  # Menu key
    PRINT_SCREEN: str = "44"
    SCROLL_LOCK: str = "145"
    PAUSE_BREAK: str = "19"

    def __init__(self) -> None:
        """Constructor for the KeyCode class."""
        pass
