"""
    domonic.constants.keyboard
    ===================================

"""


class KeyCode():

    A: str = '65'  #:
    ALTERNATE: str = '18'  #:
    B: str = '66'  #:
    BACKQUOTE: str = '192'  #:
    BACKSLASH: str = '220'  #:
    BACKSPACE: str = '8'  #:
    C: str = '67'  #:
    CAPS_LOCK: str = '20'  #:
    COMMA: str = '188'  #:
    COMMAND: str = '15'  #:
    CONTROL: str = '17'  #:
    D: str = '68'  #:
    DELETE: str = '46'  #:
    DOWN: str = '40'  #:
    E: str = '69'  #:
    END: str = '35'  #:

    ENTER: str = '13'  #:
    RETURN: str = '13'  #:

    EQUAL: str = '187'  #:
    ESCAPE: str = '27'  #:
    F: str = '70'  #:
    F1: str = '112'  #:
    F10: str = '121'  #:
    F11: str = '122'  #:
    F12: str = '123'  #:
    F13: str = '124'  #:
    F14: str = '125'  #:
    F15: str = '126'  #:
    F2: str = '113'  #:
    F3: str = '114'  #:
    F4: str = '115'  #:
    F5: str = '116'  #:
    F6: str = '117'  #:
    F7: str = '118'  #:
    F8: str = '119'  #:
    F9: str = '120'  #:
    G: str = '71'  #:
    H: str = '72'  #:
    HOME: str = '36'  #:
    I: str = '73'  #:
    INSERT: str = '45'  #:
    J: str = '74'  #:
    K: str = '75'  #:
    L: str = '76'  #:
    LEFT: str = '37'  #:
    LEFTBRACKET: str = '219'  #:
    M: str = '77'  #:
    MINUS: str = '189'  #:
    N: str = '78'  #:
    NUMBER_0: str = '48'  #:
    NUMBER_1: str = '49'  #:
    NUMBER_2: str = '50'  #:
    NUMBER_3: str = '51'  #:
    NUMBER_4: str = '52'  #:
    NUMBER_5: str = '53'  #:
    NUMBER_6: str = '54'  #:
    NUMBER_7: str = '55'  #:
    NUMBER_8: str = '56'  #:
    NUMBER_9: str = '57'  #:
    NUMPAD: str = '21'  #:
    NUMPAD_0: str = '96'  #:
    NUMPAD_1: str = '97'  #:
    NUMPAD_2: str = '98'  #:
    NUMPAD_3: str = '99'  #:
    NUMPAD_4: str = '100'  #:
    NUMPAD_5: str = '101'  #:
    NUMPAD_6: str = '102'  #:
    NUMPAD_7: str = '103'  #:
    NUMPAD_8: str = '104'  #:
    NUMPAD_9: str = '105'  #:
    NUMPAD_ADD: str = '107'  #:
    NUMPAD_DECIMAL: str = '110'  #:
    NUMPAD_DIVIDE: str = '111'  #:
    NUMPAD_ENTER: str = '108'  #:
    NUMPAD_MULTIPLY: str = '106'  #:
    NUMPAD_SUBTRACT: str = '109'  #:
    O: str = '79'  #:
    P: str = '80'  #:
    PAGE_DOWN: str = '34'  #:
    PAGE_UP: str = '33'  #:
    PERIOD: str = '190'  #:
    Q: str = '81'  #:
    QUOTE: str = '222'  #:
    R: str = '82'  #:
    RIGHT: str = '39'  #:
    RIGHTBRACKET: str = '221'  #:
    S: str = '83'  #:
    SEMICOLON: str = '186'  #:
    SHIFT: str = '16'  #: ?? left or right or both?
    SLASH: str = '191'  #:
    SPACE: str = '32'  #:
    T: str = '84'  #:
    TAB: str = '9'  #:
    U: str = '85'  #:
    UP: str = '38'  #:
    V: str = '86'  #:
    W: str = '87'  #:
    X: str = '88'  #:
    Y: str = '89'  #:
    Z: str = '9'  #:

    # TODO - do the modifiers

    # find attribute by value
    # def get_letter(self, attr):
    #     for key, value in self.__dict__.iteritems():
    #         if value: str == attr:
    #             return key
    #     return None

    def __init__(self) -> None:
        """ constructor for the KeyCode class """
        pass
