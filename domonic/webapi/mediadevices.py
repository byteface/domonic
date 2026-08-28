"""
domonic.webapi.mediadevices
====================================
https://developer.mozilla.org/en-US/docs/Web/API/MediaDevices
"""

from __future__ import annotations

import uuid
from typing import Any

from domonic.events import Event, EventTarget, TrackEvent


def _create_promise():
    from domonic.javascript import Promise

    return Promise()


class MediaDeviceInfo:
    """Information about an available media input or output device."""

    def __init__(
        self,
        deviceId: str = "",
        kind: str = "videoinput",
        label: str = "",
        groupId: str = "",
    ) -> None:
        self.deviceId = deviceId or str(uuid.uuid4())
        self.kind = kind
        self.label = label
        self.groupId = groupId

    def toJSON(self) -> dict[str, str]:
        return {
            "deviceId": self.deviceId,
            "kind": self.kind,
            "label": self.label,
            "groupId": self.groupId,
        }


class InputDeviceInfo(MediaDeviceInfo):
    """Media input device with basic capability reporting."""

    def __init__(self, *args, capabilities: dict[str, Any] | None = None, **kwargs):
        super().__init__(*args, **kwargs)
        self._capabilities = dict(capabilities or {})

    def getCapabilities(self) -> dict[str, Any]:
        return dict(self._capabilities)


class MediaStreamTrack(EventTarget):
    """Single audio, video, or display media track."""

    def __init__(
        self,
        kind: str = "video",
        label: str = "",
        *,
        id: str | None = None,
        capabilities: dict[str, Any] | None = None,
        constraints: dict[str, Any] | None = None,
        settings: dict[str, Any] | None = None,
    ) -> None:
        super().__init__()
        self.kind = kind
        self.id = id or str(uuid.uuid4())
        self.label = label or kind
        self.enabled = True
        self.muted = False
        self.readyState = "live"
        self.onended = None
        self.onmute = None
        self.onunmute = None
        self._capabilities = dict(capabilities or {})
        self._constraints = dict(constraints or {})
        self._settings = dict(settings or {})

    def stop(self) -> None:
        if self.readyState == "ended":
            return None
        self.readyState = "ended"
        self.dispatchEvent(Event("ended"))
        return None

    def clone(self) -> "MediaStreamTrack":
        return MediaStreamTrack(
            self.kind,
            self.label,
            capabilities=self._capabilities,
            constraints=self._constraints,
            settings=self._settings,
        )

    def getCapabilities(self) -> dict[str, Any]:
        return dict(self._capabilities)

    def getConstraints(self) -> dict[str, Any]:
        return dict(self._constraints)

    def getSettings(self) -> dict[str, Any]:
        return dict(self._settings)

    def applyConstraints(self, constraints: dict[str, Any] | None = None):
        self._constraints.update(constraints or {})
        self._settings.update(constraints or {})
        return _create_promise().resolve(None)


class MediaStream(EventTarget):
    """Collection of media tracks."""

    def __init__(
        self, tracks: list[MediaStreamTrack] | None = None, id: str | None = None
    ):
        super().__init__()
        self.id = id or str(uuid.uuid4())
        self.onaddtrack = None
        self.onremovetrack = None
        self._tracks: list[MediaStreamTrack] = []
        for track in tracks or []:
            self.addTrack(track)

    @property
    def active(self) -> bool:
        return any(track.readyState == "live" for track in self._tracks)

    def addTrack(self, track: MediaStreamTrack) -> None:
        if track not in self._tracks:
            self._tracks.append(track)
            self.dispatchEvent(TrackEvent("addtrack", {"track": track}))
        return None

    def removeTrack(self, track: MediaStreamTrack) -> None:
        if track in self._tracks:
            self._tracks.remove(track)
            self.dispatchEvent(TrackEvent("removetrack", {"track": track}))
        return None

    def getTrackById(self, id: str) -> MediaStreamTrack | None:
        for track in self._tracks:
            if track.id == id:
                return track
        return None

    def getTracks(self) -> list[MediaStreamTrack]:
        return list(self._tracks)

    def getAudioTracks(self) -> list[MediaStreamTrack]:
        return [track for track in self._tracks if track.kind == "audio"]

    def getVideoTracks(self) -> list[MediaStreamTrack]:
        return [track for track in self._tracks if track.kind == "video"]

    def clone(self) -> "MediaStream":
        return MediaStream([track.clone() for track in self._tracks])


class MediaDevices(EventTarget):
    """Media device registry with browser-like stream factory helpers."""

    def __init__(self, devices: list[MediaDeviceInfo] | None = None) -> None:
        super().__init__()
        self.ondevicechange = None
        self._devices = (
            list(devices) if devices is not None else self._default_devices()
        )

    @staticmethod
    def _default_devices() -> list[MediaDeviceInfo]:
        return [
            InputDeviceInfo("default-audio", "audioinput", "Default microphone"),
            InputDeviceInfo("default-video", "videoinput", "Default camera"),
            MediaDeviceInfo("default-speaker", "audiooutput", "Default speaker"),
        ]

    def enumerateDevices(self):
        return _create_promise().resolve(list(self._devices))

    def getSupportedConstraints(self) -> dict[str, bool]:
        return {
            "aspectRatio": True,
            "deviceId": True,
            "echoCancellation": True,
            "facingMode": True,
            "frameRate": True,
            "height": True,
            "sampleRate": True,
            "width": True,
        }

    def getUserMedia(self, constraints: dict[str, Any] | None = None):
        constraints = constraints or {"audio": True, "video": True}
        tracks = []
        if constraints.get("audio"):
            tracks.append(
                self._track_from_constraint("audio", constraints.get("audio"))
            )
        if constraints.get("video"):
            tracks.append(
                self._track_from_constraint("video", constraints.get("video"))
            )
        if not tracks:
            return _create_promise().reject(ValueError("No media requested"))
        return _create_promise().resolve(MediaStream(tracks))

    def getDisplayMedia(self, constraints: dict[str, Any] | None = None):
        constraints = constraints or {"video": True}
        track = MediaStreamTrack(
            "video",
            "Display capture",
            constraints={"displaySurface": "monitor", **dict(constraints or {})},
            settings={"displaySurface": "monitor"},
        )
        return _create_promise().resolve(MediaStream([track]))

    def addDevice(self, device: MediaDeviceInfo) -> MediaDeviceInfo:
        self._devices.append(device)
        self.dispatchEvent(Event("devicechange"))
        return device

    def removeDevice(self, deviceId: str) -> MediaDeviceInfo | None:
        for device in list(self._devices):
            if device.deviceId == deviceId:
                self._devices.remove(device)
                self.dispatchEvent(Event("devicechange"))
                return device
        return None

    def _track_from_constraint(self, kind: str, constraint: Any) -> MediaStreamTrack:
        constraint_dict = constraint if isinstance(constraint, dict) else {}
        device_kind = "audioinput" if kind == "audio" else "videoinput"
        label = next(
            (device.label for device in self._devices if device.kind == device_kind),
            kind,
        )
        return MediaStreamTrack(kind, label, constraints=constraint_dict)


__all__ = [
    "InputDeviceInfo",
    "MediaDeviceInfo",
    "MediaDevices",
    "MediaStream",
    "MediaStreamTrack",
]
