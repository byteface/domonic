from __future__ import annotations

import math
import re
from dataclasses import dataclass
from typing import Any

from domonic.events import Event, EventTarget
from domonic.lerpy import lerp
from domonic.lerpy.easing import Linear, Quad


def _coerce_timing_options(options: EffectTiming | dict[str, Any] | None) -> dict[str, Any]:
    if options is None:
        return {}
    if isinstance(options, EffectTiming):
        return options.to_dict()
    if isinstance(options, dict):
        return dict(options)
    if isinstance(options, (int, float)):
        return {"duration": float(options)}
    raise TypeError("Unsupported timing options")


def _normalize_iteration_count(value: Any) -> float:
    if value in (None, "", "Infinity", "infinity"):
        return math.inf if value in ("Infinity", "infinity") else 1.0
    return float(value)


def _parse_interpolable(value: Any) -> tuple[float, str] | None:
    if isinstance(value, (int, float)):
        return float(value), ""
    if isinstance(value, str):
        match = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?)([a-zA-Z%]*)\s*", value)
        if match:
            return float(match.group(1)), match.group(2)
    return None


def _format_interpolated(value: float, unit: str) -> str | float:
    if unit:
        formatted = int(value) if float(value).is_integer() else round(value, 6)
        return f"{formatted}{unit}"
    return int(value) if float(value).is_integer() else value


def _resolve_easing(name: str):
    easing = (name or "linear").strip().lower()
    mapping = {
        "linear": Linear.easeIn,
        "ease": Quad.easeInOut,
        "ease-in": Quad.easeIn,
        "ease-out": Quad.easeOut,
        "ease-in-out": Quad.easeInOut,
    }
    return mapping.get(easing, Linear.easeIn)


@dataclass
class EffectTiming:
    delay: float = 0.0
    direction: str = "normal"
    duration: float = 0.0
    easing: str = "linear"
    endDelay: float = 0.0
    fill: str = "none"
    iterationStart: float = 0.0
    iterations: float = 1.0

    def __init__(
        self,
        delay: float = 0.0,
        direction: str = "normal",
        duration: float = 0.0,
        easing: str = "linear",
        endDelay: float = 0.0,
        fill: str = "none",
        iterationStart: float = 0.0,
        iterations: float = 1.0,
    ) -> None:
        self.delay = float(delay)
        self.direction = direction
        self.duration = float(duration)
        self.easing = easing
        self.endDelay = float(endDelay)
        self.fill = fill
        self.iterationStart = float(iterationStart)
        self.iterations = _normalize_iteration_count(iterations)

    def to_dict(self) -> dict[str, Any]:
        return {
            "delay": self.delay,
            "direction": self.direction,
            "duration": self.duration,
            "easing": self.easing,
            "endDelay": self.endDelay,
            "fill": self.fill,
            "iterationStart": self.iterationStart,
            "iterations": self.iterations,
        }


class ComputedEffectTiming(EffectTiming):
    def __init__(
        self,
        timing: EffectTiming | None = None,
        *,
        activeDuration: float = 0.0,
        currentIteration: int | None = None,
        endTime: float = 0.0,
        progress: float | None = None,
    ) -> None:
        timing = timing or EffectTiming()
        super().__init__(**timing.to_dict())
        self.activeDuration = activeDuration
        self.currentIteration = currentIteration
        self.endTime = endTime
        self.progress = progress


class AnimationPlaybackEvent(Event):
    def __init__(self, _type: str, options: dict[str, Any] | None = None, *args, **kwargs) -> None:
        options = options or kwargs
        self.currentTime = options.get("currentTime")
        self.timelineTime = options.get("timelineTime")
        super().__init__(_type, options, *args, **kwargs)


class AnimationEffect:
    def __init__(self, timing: EffectTiming | dict[str, Any] | None = None) -> None:
        self._timing = EffectTiming(**_coerce_timing_options(timing))

    def getTiming(self) -> EffectTiming:
        return EffectTiming(**self._timing.to_dict())

    def updateTiming(self, options: EffectTiming | dict[str, Any] | None = None) -> None:
        if options is None:
            return
        updated = self._timing.to_dict()
        updated.update(_coerce_timing_options(options))
        self._timing = EffectTiming(**updated)

    def getComputedTiming(self, local_time: float | None = None) -> ComputedEffectTiming:
        timing = self.getTiming()
        iterations = timing.iterations
        active_duration = math.inf if math.isinf(iterations) else timing.duration * iterations
        end_time = timing.delay + active_duration + timing.endDelay
        progress = None
        current_iteration = None

        if local_time is not None:
            active_time = local_time - timing.delay
            if active_time < 0:
                if timing.fill in {"backwards", "both"}:
                    progress = 0.0
                    current_iteration = 0
            elif math.isinf(active_duration) or active_time < active_duration:
                duration = timing.duration if timing.duration > 0 else 1.0
                current_iteration = int(active_time // duration) if timing.duration > 0 else 0
                simple_progress = 1.0 if timing.duration == 0 else (active_time % duration) / duration
                progress = self._directed_progress(simple_progress, current_iteration)
            elif active_duration == 0 or active_time == active_duration:
                progress = self._directed_progress(1.0, max(0, int(iterations) - 1 if not math.isinf(iterations) else 0))
                current_iteration = None if math.isinf(iterations) else max(0, int(iterations) - 1)
            elif timing.fill in {"forwards", "both"}:
                progress = self._directed_progress(1.0, max(0, int(iterations) - 1 if not math.isinf(iterations) else 0))
                current_iteration = None if math.isinf(iterations) else max(0, int(iterations) - 1)

        return ComputedEffectTiming(
            timing,
            activeDuration=active_duration,
            currentIteration=current_iteration,
            endTime=end_time,
            progress=progress,
        )

    def _directed_progress(self, progress: float, iteration: int) -> float:
        direction = self._timing.direction
        if direction == "reverse":
            return 1.0 - progress
        if direction == "alternate" and iteration % 2 == 1:
            return 1.0 - progress
        if direction == "alternate-reverse":
            return progress if iteration % 2 == 1 else 1.0 - progress
        return progress

    def apply(self, local_time: float | None = None) -> None:
        raise NotImplementedError


class KeyframeEffect(AnimationEffect):
    def __init__(
        self,
        target: Any,
        keyframes: list[dict[str, Any]] | dict[str, Any],
        options: EffectTiming | dict[str, Any] | None = None,
    ) -> None:
        self.target = target
        self._keyframes = self._normalize_keyframes(keyframes)
        super().__init__(options)

    @staticmethod
    def _normalize_keyframes(keyframes: list[dict[str, Any]] | dict[str, Any]) -> list[dict[str, Any]]:
        frames = [dict(frame) for frame in (keyframes if isinstance(keyframes, list) else [keyframes])]
        if not frames:
            return [{"offset": 0.0}, {"offset": 1.0}]

        for index, frame in enumerate(frames):
            if "offset" in frame and frame["offset"] is not None:
                frame["offset"] = float(frame["offset"])
            else:
                frame["offset"] = index / (len(frames) - 1) if len(frames) > 1 else 1.0
        frames.sort(key=lambda frame: frame["offset"])
        return frames

    def getKeyframes(self) -> list[dict[str, Any]]:
        return [dict(frame) for frame in self._keyframes]

    def _interpolate_value(self, prop: str, start: Any, end: Any, progress: float) -> Any:
        easing_fn = _resolve_easing(self._timing.easing)
        eased = easing_fn(progress, 0, 1, 1, 0, 0)
        start_value = _parse_interpolable(start)
        end_value = _parse_interpolable(end)
        if start_value is not None and end_value is not None and start_value[1] == end_value[1]:
            return _format_interpolated(lerp(start_value[0], end_value[0], eased), start_value[1])
        return end if eased >= 0.5 else start

    def _apply_property(self, prop: str, value: Any) -> None:
        if hasattr(self.target, "style") and hasattr(self.target.style, "__dict__"):
            setattr(self.target.style, prop, value)
            return
        if hasattr(self.target, prop):
            setattr(self.target, prop, value)
            return
        if hasattr(self.target, "setAttribute"):
            self.target.setAttribute(prop, value)

    def apply(self, local_time: float | None = None) -> None:
        computed = self.getComputedTiming(local_time)
        if computed.progress is None:
            return

        progress = computed.progress
        before = self._keyframes[0]
        after = self._keyframes[-1]
        for index in range(len(self._keyframes) - 1):
            start = self._keyframes[index]
            end = self._keyframes[index + 1]
            if start["offset"] <= progress <= end["offset"]:
                before = start
                after = end
                break

        span = after["offset"] - before["offset"]
        local_progress = 1.0 if span == 0 else (progress - before["offset"]) / span
        properties = set(before.keys()) | set(after.keys())
        properties.discard("offset")
        properties.discard("easing")
        properties.discard("composite")

        for prop in properties:
            start_value = before.get(prop, after.get(prop))
            end_value = after.get(prop, before.get(prop))
            value = self._interpolate_value(prop, start_value, end_value, local_progress)
            self._apply_property(prop, value)


class Animation(EventTarget):
    def __init__(
        self,
        effect: AnimationEffect | None = None,
        timeline: Any = None,
        *,
        id: str = "",
    ) -> None:
        super().__init__()
        self.effect = effect
        self.timeline = timeline
        self.id = id
        self.playbackRate: float = 1.0
        self.startTime: float | None = None
        self._currentTime: float | None = None
        self.playState: str = "idle"

    @property
    def currentTime(self) -> float | None:
        if self.playState == "running" and self.startTime is not None and self.timeline is not None:
            self._currentTime = (self.timeline.currentTime - self.startTime) * self.playbackRate
        return self._currentTime

    @currentTime.setter
    def currentTime(self, value: float | None) -> None:
        self._currentTime = None if value is None else float(value)
        if self.effect is not None and self._currentTime is not None:
            self.effect.apply(self._currentTime)

    def play(self) -> None:
        if self.timeline is not None:
            self.startTime = self.timeline.currentTime - (self._currentTime or 0.0)
        self.playState = "running"
        if self._currentTime is None:
            self.currentTime = 0.0

    def pause(self) -> None:
        self.currentTime = self.currentTime
        self.playState = "paused"

    def cancel(self) -> None:
        self.playState = "idle"
        self.startTime = None
        self._currentTime = None
        self.dispatchEvent(
            AnimationPlaybackEvent(
                "cancel",
                {"currentTime": None, "timelineTime": getattr(self.timeline, "currentTime", None)},
            )
        )

    def finish(self) -> None:
        effect_time = 0.0
        if self.effect is not None:
            effect_time = self.effect.getComputedTiming().activeDuration
        self.currentTime = effect_time
        self.playState = "finished"
        self.dispatchEvent(
            AnimationPlaybackEvent(
                "finish",
                {"currentTime": self.currentTime, "timelineTime": getattr(self.timeline, "currentTime", None)},
            )
        )

    def reverse(self) -> None:
        self.playbackRate = -self.playbackRate
        self.play()

    def updatePlaybackRate(self, playback_rate: float) -> None:
        self.currentTime = self.currentTime
        self.playbackRate = float(playback_rate)
