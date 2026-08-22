from __future__ import annotations

from typing import ClassVar, Final


class KeyLocation:
    """KeyboardEvent.location constants from the modern UI Events model."""

    STANDARD: ClassVar[int] = 0
    LEFT: ClassVar[int] = 1
    RIGHT: ClassVar[int] = 2
    NUMPAD: ClassVar[int] = 3


class Key:
    """Common KeyboardEvent.key values."""

    ENTER: ClassVar[str] = "Enter"
    TAB: ClassVar[str] = "Tab"
    SPACE: ClassVar[str] = " "
    ESCAPE: ClassVar[str] = "Escape"
    BACKSPACE: ClassVar[str] = "Backspace"
    DELETE: ClassVar[str] = "Delete"
    INSERT: ClassVar[str] = "Insert"
    HOME: ClassVar[str] = "Home"
    END: ClassVar[str] = "End"
    PAGE_UP: ClassVar[str] = "PageUp"
    PAGE_DOWN: ClassVar[str] = "PageDown"
    ARROW_LEFT: ClassVar[str] = "ArrowLeft"
    ARROW_RIGHT: ClassVar[str] = "ArrowRight"
    ARROW_UP: ClassVar[str] = "ArrowUp"
    ARROW_DOWN: ClassVar[str] = "ArrowDown"
    SHIFT: ClassVar[str] = "Shift"
    CONTROL: ClassVar[str] = "Control"
    ALT: ClassVar[str] = "Alt"
    META: ClassVar[str] = "Meta"
    CAPS_LOCK: ClassVar[str] = "CapsLock"
    NUM_LOCK: ClassVar[str] = "NumLock"
    SCROLL_LOCK: ClassVar[str] = "ScrollLock"
    CONTEXT_MENU: ClassVar[str] = "ContextMenu"

    F1: ClassVar[str] = "F1"
    F2: ClassVar[str] = "F2"
    F3: ClassVar[str] = "F3"
    F4: ClassVar[str] = "F4"
    F5: ClassVar[str] = "F5"
    F6: ClassVar[str] = "F6"
    F7: ClassVar[str] = "F7"
    F8: ClassVar[str] = "F8"
    F9: ClassVar[str] = "F9"
    F10: ClassVar[str] = "F10"
    F11: ClassVar[str] = "F11"
    F12: ClassVar[str] = "F12"

    A: ClassVar[str] = "a"
    B: ClassVar[str] = "b"
    C: ClassVar[str] = "c"
    D: ClassVar[str] = "d"
    E: ClassVar[str] = "e"
    F: ClassVar[str] = "f"
    G: ClassVar[str] = "g"
    H: ClassVar[str] = "h"
    I: ClassVar[str] = "i"
    J: ClassVar[str] = "j"
    K: ClassVar[str] = "k"
    L: ClassVar[str] = "l"
    M: ClassVar[str] = "m"
    N: ClassVar[str] = "n"
    O: ClassVar[str] = "o"
    P: ClassVar[str] = "p"
    Q: ClassVar[str] = "q"
    R: ClassVar[str] = "r"
    S: ClassVar[str] = "s"
    T: ClassVar[str] = "t"
    U: ClassVar[str] = "u"
    V: ClassVar[str] = "v"
    W: ClassVar[str] = "w"
    X: ClassVar[str] = "x"
    Y: ClassVar[str] = "y"
    Z: ClassVar[str] = "z"

    DIGIT_0: ClassVar[str] = "0"
    DIGIT_1: ClassVar[str] = "1"
    DIGIT_2: ClassVar[str] = "2"
    DIGIT_3: ClassVar[str] = "3"
    DIGIT_4: ClassVar[str] = "4"
    DIGIT_5: ClassVar[str] = "5"
    DIGIT_6: ClassVar[str] = "6"
    DIGIT_7: ClassVar[str] = "7"
    DIGIT_8: ClassVar[str] = "8"
    DIGIT_9: ClassVar[str] = "9"


class Code:
    """Common KeyboardEvent.code values."""

    ENTER: ClassVar[str] = "Enter"
    TAB: ClassVar[str] = "Tab"
    SPACE: ClassVar[str] = "Space"
    ESCAPE: ClassVar[str] = "Escape"
    BACKSPACE: ClassVar[str] = "Backspace"
    DELETE: ClassVar[str] = "Delete"
    INSERT: ClassVar[str] = "Insert"
    HOME: ClassVar[str] = "Home"
    END: ClassVar[str] = "End"
    PAGE_UP: ClassVar[str] = "PageUp"
    PAGE_DOWN: ClassVar[str] = "PageDown"
    ARROW_LEFT: ClassVar[str] = "ArrowLeft"
    ARROW_RIGHT: ClassVar[str] = "ArrowRight"
    ARROW_UP: ClassVar[str] = "ArrowUp"
    ARROW_DOWN: ClassVar[str] = "ArrowDown"
    SHIFT_LEFT: ClassVar[str] = "ShiftLeft"
    SHIFT_RIGHT: ClassVar[str] = "ShiftRight"
    CONTROL_LEFT: ClassVar[str] = "ControlLeft"
    CONTROL_RIGHT: ClassVar[str] = "ControlRight"
    ALT_LEFT: ClassVar[str] = "AltLeft"
    ALT_RIGHT: ClassVar[str] = "AltRight"
    META_LEFT: ClassVar[str] = "MetaLeft"
    META_RIGHT: ClassVar[str] = "MetaRight"
    CAPS_LOCK: ClassVar[str] = "CapsLock"
    NUM_LOCK: ClassVar[str] = "NumLock"
    SCROLL_LOCK: ClassVar[str] = "ScrollLock"
    CONTEXT_MENU: ClassVar[str] = "ContextMenu"

    F1: ClassVar[str] = "F1"
    F2: ClassVar[str] = "F2"
    F3: ClassVar[str] = "F3"
    F4: ClassVar[str] = "F4"
    F5: ClassVar[str] = "F5"
    F6: ClassVar[str] = "F6"
    F7: ClassVar[str] = "F7"
    F8: ClassVar[str] = "F8"
    F9: ClassVar[str] = "F9"
    F10: ClassVar[str] = "F10"
    F11: ClassVar[str] = "F11"
    F12: ClassVar[str] = "F12"

    KEY_A: ClassVar[str] = "KeyA"
    KEY_B: ClassVar[str] = "KeyB"
    KEY_C: ClassVar[str] = "KeyC"
    KEY_D: ClassVar[str] = "KeyD"
    KEY_E: ClassVar[str] = "KeyE"
    KEY_F: ClassVar[str] = "KeyF"
    KEY_G: ClassVar[str] = "KeyG"
    KEY_H: ClassVar[str] = "KeyH"
    KEY_I: ClassVar[str] = "KeyI"
    KEY_J: ClassVar[str] = "KeyJ"
    KEY_K: ClassVar[str] = "KeyK"
    KEY_L: ClassVar[str] = "KeyL"
    KEY_M: ClassVar[str] = "KeyM"
    KEY_N: ClassVar[str] = "KeyN"
    KEY_O: ClassVar[str] = "KeyO"
    KEY_P: ClassVar[str] = "KeyP"
    KEY_Q: ClassVar[str] = "KeyQ"
    KEY_R: ClassVar[str] = "KeyR"
    KEY_S: ClassVar[str] = "KeyS"
    KEY_T: ClassVar[str] = "KeyT"
    KEY_U: ClassVar[str] = "KeyU"
    KEY_V: ClassVar[str] = "KeyV"
    KEY_W: ClassVar[str] = "KeyW"
    KEY_X: ClassVar[str] = "KeyX"
    KEY_Y: ClassVar[str] = "KeyY"
    KEY_Z: ClassVar[str] = "KeyZ"

    DIGIT_0: ClassVar[str] = "Digit0"
    DIGIT_1: ClassVar[str] = "Digit1"
    DIGIT_2: ClassVar[str] = "Digit2"
    DIGIT_3: ClassVar[str] = "Digit3"
    DIGIT_4: ClassVar[str] = "Digit4"
    DIGIT_5: ClassVar[str] = "Digit5"
    DIGIT_6: ClassVar[str] = "Digit6"
    DIGIT_7: ClassVar[str] = "Digit7"
    DIGIT_8: ClassVar[str] = "Digit8"
    DIGIT_9: ClassVar[str] = "Digit9"

    NUMPAD_0: ClassVar[str] = "Numpad0"
    NUMPAD_1: ClassVar[str] = "Numpad1"
    NUMPAD_2: ClassVar[str] = "Numpad2"
    NUMPAD_3: ClassVar[str] = "Numpad3"
    NUMPAD_4: ClassVar[str] = "Numpad4"
    NUMPAD_5: ClassVar[str] = "Numpad5"
    NUMPAD_6: ClassVar[str] = "Numpad6"
    NUMPAD_7: ClassVar[str] = "Numpad7"
    NUMPAD_8: ClassVar[str] = "Numpad8"
    NUMPAD_9: ClassVar[str] = "Numpad9"
    NUMPAD_ADD: ClassVar[str] = "NumpadAdd"
    NUMPAD_DECIMAL: ClassVar[str] = "NumpadDecimal"
    NUMPAD_DIVIDE: ClassVar[str] = "NumpadDivide"
    NUMPAD_ENTER: ClassVar[str] = "NumpadEnter"
    NUMPAD_MULTIPLY: ClassVar[str] = "NumpadMultiply"
    NUMPAD_SUBTRACT: ClassVar[str] = "NumpadSubtract"


_LEGACY_KEYCODE_TO_KEY: Final[dict[str, str]] = {
    "8": Key.BACKSPACE,
    "9": Key.TAB,
    "13": Key.ENTER,
    "16": Key.SHIFT,
    "17": Key.CONTROL,
    "18": Key.ALT,
    "20": Key.CAPS_LOCK,
    "27": Key.ESCAPE,
    "32": Key.SPACE,
    "33": Key.PAGE_UP,
    "34": Key.PAGE_DOWN,
    "35": Key.END,
    "36": Key.HOME,
    "37": Key.ARROW_LEFT,
    "38": Key.ARROW_UP,
    "39": Key.ARROW_RIGHT,
    "40": Key.ARROW_DOWN,
    "45": Key.INSERT,
    "46": Key.DELETE,
    "91": Key.META,
    "93": Key.CONTEXT_MENU,
    "144": Key.NUM_LOCK,
    "145": Key.SCROLL_LOCK,
}
_LEGACY_KEYCODE_TO_KEY.update({str(48 + i): str(i) for i in range(10)})
_LEGACY_KEYCODE_TO_KEY.update({str(65 + i): chr(97 + i) for i in range(26)})
_LEGACY_KEYCODE_TO_KEY.update({str(111 + i): f"F{i}" for i in range(1, 13)})

_KEY_TO_CODE: Final[dict[str, str]] = {
    Key.ENTER: Code.ENTER,
    Key.TAB: Code.TAB,
    Key.SPACE: Code.SPACE,
    Key.ESCAPE: Code.ESCAPE,
    Key.BACKSPACE: Code.BACKSPACE,
    Key.DELETE: Code.DELETE,
    Key.INSERT: Code.INSERT,
    Key.HOME: Code.HOME,
    Key.END: Code.END,
    Key.PAGE_UP: Code.PAGE_UP,
    Key.PAGE_DOWN: Code.PAGE_DOWN,
    Key.ARROW_LEFT: Code.ARROW_LEFT,
    Key.ARROW_RIGHT: Code.ARROW_RIGHT,
    Key.ARROW_UP: Code.ARROW_UP,
    Key.ARROW_DOWN: Code.ARROW_DOWN,
    Key.SHIFT: Code.SHIFT_LEFT,
    Key.CONTROL: Code.CONTROL_LEFT,
    Key.ALT: Code.ALT_LEFT,
    Key.META: Code.META_LEFT,
    Key.CAPS_LOCK: Code.CAPS_LOCK,
    Key.NUM_LOCK: Code.NUM_LOCK,
    Key.SCROLL_LOCK: Code.SCROLL_LOCK,
    Key.CONTEXT_MENU: Code.CONTEXT_MENU,
}
_KEY_TO_CODE.update({chr(97 + i): f"Key{chr(65 + i)}" for i in range(26)})
_KEY_TO_CODE.update({str(i): f"Digit{i}" for i in range(10)})
_KEY_TO_CODE.update({f"F{i}": f"F{i}" for i in range(1, 13)})

_KEY_TO_LEGACY_KEYCODE: Final[dict[str, int]] = {
    key: int(code) for code, key in _LEGACY_KEYCODE_TO_KEY.items()
}


class KeyCode:
    """Legacy KeyboardEvent.keyCode constants kept for compatibility."""

    A: ClassVar[str] = "65"
    B: ClassVar[str] = "66"
    C: ClassVar[str] = "67"
    D: ClassVar[str] = "68"
    E: ClassVar[str] = "69"
    F: ClassVar[str] = "70"
    G: ClassVar[str] = "71"
    H: ClassVar[str] = "72"
    I: ClassVar[str] = "73"
    J: ClassVar[str] = "74"
    K: ClassVar[str] = "75"
    L: ClassVar[str] = "76"
    M: ClassVar[str] = "77"
    N: ClassVar[str] = "78"
    O: ClassVar[str] = "79"
    P: ClassVar[str] = "80"
    Q: ClassVar[str] = "81"
    R: ClassVar[str] = "82"
    S: ClassVar[str] = "83"
    T: ClassVar[str] = "84"
    U: ClassVar[str] = "85"
    V: ClassVar[str] = "86"
    W: ClassVar[str] = "87"
    X: ClassVar[str] = "88"
    Y: ClassVar[str] = "89"
    Z: ClassVar[str] = "90"

    NUMBER_0: ClassVar[str] = "48"
    NUMBER_1: ClassVar[str] = "49"
    NUMBER_2: ClassVar[str] = "50"
    NUMBER_3: ClassVar[str] = "51"
    NUMBER_4: ClassVar[str] = "52"
    NUMBER_5: ClassVar[str] = "53"
    NUMBER_6: ClassVar[str] = "54"
    NUMBER_7: ClassVar[str] = "55"
    NUMBER_8: ClassVar[str] = "56"
    NUMBER_9: ClassVar[str] = "57"

    NUMPAD_0: ClassVar[str] = "96"
    NUMPAD_1: ClassVar[str] = "97"
    NUMPAD_2: ClassVar[str] = "98"
    NUMPAD_3: ClassVar[str] = "99"
    NUMPAD_4: ClassVar[str] = "100"
    NUMPAD_5: ClassVar[str] = "101"
    NUMPAD_6: ClassVar[str] = "102"
    NUMPAD_7: ClassVar[str] = "103"
    NUMPAD_8: ClassVar[str] = "104"
    NUMPAD_9: ClassVar[str] = "105"
    NUMPAD_MULTIPLY: ClassVar[str] = "106"
    NUMPAD_ADD: ClassVar[str] = "107"
    NUMPAD_ENTER: ClassVar[str] = "108"
    NUMPAD_SUBTRACT: ClassVar[str] = "109"
    NUMPAD_DECIMAL: ClassVar[str] = "110"
    NUMPAD_DIVIDE: ClassVar[str] = "111"

    F1: ClassVar[str] = "112"
    F2: ClassVar[str] = "113"
    F3: ClassVar[str] = "114"
    F4: ClassVar[str] = "115"
    F5: ClassVar[str] = "116"
    F6: ClassVar[str] = "117"
    F7: ClassVar[str] = "118"
    F8: ClassVar[str] = "119"
    F9: ClassVar[str] = "120"
    F10: ClassVar[str] = "121"
    F11: ClassVar[str] = "122"
    F12: ClassVar[str] = "123"

    BACKSPACE: ClassVar[str] = "8"
    TAB: ClassVar[str] = "9"
    ENTER: ClassVar[str] = "13"
    SHIFT: ClassVar[str] = "16"
    CONTROL: ClassVar[str] = "17"
    ALT: ClassVar[str] = "18"
    CAPS_LOCK: ClassVar[str] = "20"
    ESCAPE: ClassVar[str] = "27"
    SPACE: ClassVar[str] = "32"
    PAGE_UP: ClassVar[str] = "33"
    PAGE_DOWN: ClassVar[str] = "34"
    END: ClassVar[str] = "35"
    HOME: ClassVar[str] = "36"
    LEFT: ClassVar[str] = "37"
    UP: ClassVar[str] = "38"
    RIGHT: ClassVar[str] = "39"
    DOWN: ClassVar[str] = "40"
    INSERT: ClassVar[str] = "45"
    DELETE: ClassVar[str] = "46"
    LEFT_COMMAND: ClassVar[str] = "91"
    RIGHT_COMMAND: ClassVar[str] = "93"
    WINDOWS: ClassVar[str] = "91"
    MENU: ClassVar[str] = "93"
    NUM_LOCK: ClassVar[str] = "144"
    SCROLL_LOCK: ClassVar[str] = "145"

    MODIFIER_KEYS: ClassVar[frozenset[str]] = frozenset(
        {
            SHIFT,
            CONTROL,
            ALT,
            LEFT_COMMAND,
            RIGHT_COMMAND,
            CAPS_LOCK,
            NUM_LOCK,
            SCROLL_LOCK,
        }
    )

    @classmethod
    def is_modifier(cls, key_code: str) -> bool:
        return key_code in cls.MODIFIER_KEYS

    @classmethod
    def to_key(cls, key_code: str | int) -> str | None:
        return _LEGACY_KEYCODE_TO_KEY.get(str(key_code))

    @classmethod
    def to_code(cls, key_code: str | int) -> str | None:
        key = cls.to_key(key_code)
        return _KEY_TO_CODE.get(key) if key is not None else None

    @classmethod
    def from_key(cls, key: str) -> int | None:
        return _KEY_TO_LEGACY_KEYCODE.get(normalize_key(key))


def normalize_key(key: str | None) -> str:
    """Normalize browser-ish key strings to the modern KeyboardEvent.key form."""
    if key in (None, ""):
        return ""
    aliases = {
        "Esc": Key.ESCAPE,
        "Spacebar": Key.SPACE,
        "Left": Key.ARROW_LEFT,
        "Right": Key.ARROW_RIGHT,
        "Up": Key.ARROW_UP,
        "Down": Key.ARROW_DOWN,
        "Del": Key.DELETE,
        "OS": Key.META,
    }
    normalized = aliases.get(key, key)
    if len(normalized) == 1 and normalized.isalpha():
        return normalized.lower()
    return normalized


def normalize_code(code: str | None) -> str:
    """Normalize shorthand physical key names to KeyboardEvent.code values."""
    if code in (None, ""):
        return ""
    if len(code) == 1 and code.isalpha():
        return f"Key{code.upper()}"
    if len(code) == 1 and code.isdigit():
        return f"Digit{code}"
    return code


__all__ = ["Code", "Key", "KeyCode", "KeyLocation", "normalize_code", "normalize_key"]
