"""
domonic.webapi.gamepad
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Gamepad_API
"""

from __future__ import annotations

import time
from typing import Any

from domonic.events import EventTarget, GamePadEvent


def _create_promise():
    from domonic.javascript import Promise

    return Promise()


class GamepadButton:
    """State for a single gamepad button."""

    def __init__(
        self, value: float = 0.0, pressed: bool = False, touched: bool = False
    ) -> None:
        self.value = float(value)
        self.pressed = bool(pressed)
        self.touched = bool(touched)

    def update(
        self,
        value: float | None = None,
        pressed: bool | None = None,
        touched: bool | None = None,
    ) -> "GamepadButton":
        if value is not None:
            self.value = float(value)
        if pressed is not None:
            self.pressed = bool(pressed)
        if touched is not None:
            self.touched = bool(touched)
        return self

    def toJSON(self) -> dict[str, Any]:
        return {"value": self.value, "pressed": self.pressed, "touched": self.touched}


class GamepadHapticActuator:
    """Minimal haptics recorder."""

    def __init__(self) -> None:
        self.effects: list[dict[str, float]] = []

    def pulse(self, value: float, duration: float):
        effect = {"value": float(value), "duration": float(duration)}
        self.effects.append(effect)
        return _create_promise().resolve(True)

    def reset(self):
        self.effects.clear()
        return _create_promise().resolve(True)


class Gamepad:
    """Gamepad state object returned by ``navigator.getGamepads()``."""

    def __init__(
        self,
        id: str,
        *,
        index: int = 0,
        axes: list[float] | tuple[float, ...] | None = None,
        buttons: (
            list[GamepadButton | dict[str, Any] | float] | tuple[Any, ...] | None
        ) = None,
        mapping: str = "",
        connected: bool = False,
    ) -> None:
        self.id = str(id)
        self.index = int(index)
        self.mapping = str(mapping)
        self.connected = bool(connected)
        self.axes = [float(axis) for axis in (axes or [])]
        self.buttons = [self._coerce_button(button) for button in (buttons or [])]
        self.timestamp = time.perf_counter() * 1000
        self.vibrationActuator = GamepadHapticActuator()

    @staticmethod
    def _coerce_button(button: GamepadButton | dict[str, Any] | float) -> GamepadButton:
        if isinstance(button, GamepadButton):
            return button
        if isinstance(button, dict):
            return GamepadButton(
                button.get("value", 0.0),
                button.get("pressed", False),
                button.get("touched", False),
            )
        return GamepadButton(float(button), bool(button), bool(button))

    def update(
        self,
        *,
        axes: list[float] | tuple[float, ...] | None = None,
        buttons: (
            list[GamepadButton | dict[str, Any] | float] | tuple[Any, ...] | None
        ) = None,
    ) -> "Gamepad":
        if axes is not None:
            self.axes = [float(axis) for axis in axes]
        if buttons is not None:
            self.buttons = [self._coerce_button(button) for button in buttons]
        self.timestamp = time.perf_counter() * 1000
        return self

    def toJSON(self) -> dict[str, Any]:
        return {
            "id": self.id,
            "index": self.index,
            "connected": self.connected,
            "mapping": self.mapping,
            "axes": list(self.axes),
            "buttons": [button.toJSON() for button in self.buttons],
            "timestamp": self.timestamp,
        }


class GamepadManager(EventTarget):
    """In-process registry behind ``navigator.getGamepads()``."""

    def __init__(self, eventTarget: EventTarget | None = None) -> None:
        super().__init__()
        self.eventTarget = eventTarget
        self._gamepads: dict[int, Gamepad] = {}

    def getGamepads(self) -> list[Gamepad | None]:
        if not self._gamepads:
            return []
        highest_index = max(self._gamepads)
        return [self._gamepads.get(index) for index in range(highest_index + 1)]

    def connect(self, gamepad: Gamepad, index: int | None = None) -> Gamepad:
        if not isinstance(gamepad, Gamepad):
            raise TypeError("connect() expects a Gamepad")
        if index is not None:
            gamepad.index = int(index)
        gamepad.connected = True
        gamepad.timestamp = time.perf_counter() * 1000
        self._gamepads[gamepad.index] = gamepad
        self._dispatch(GamePadEvent.START, gamepad)
        return gamepad

    def disconnect(self, gamepad: Gamepad | int) -> Gamepad | None:
        index = gamepad.index if isinstance(gamepad, Gamepad) else int(gamepad)
        stored = self._gamepads.pop(index, None)
        if stored is None:
            return None
        stored.connected = False
        stored.timestamp = time.perf_counter() * 1000
        self._dispatch(GamePadEvent.STOP, stored)
        return stored

    def _dispatch(self, event_type: str, gamepad: Gamepad) -> None:
        event = GamePadEvent(event_type, {"gamepad": gamepad})
        target = self.eventTarget or self
        target.dispatchEvent(event)
        if target is not self and self.hasEventListener(event_type):
            self.dispatchEvent(GamePadEvent(event_type, {"gamepad": gamepad}))


__all__ = ["Gamepad", "GamepadButton", "GamepadHapticActuator", "GamepadManager"]
