"""
domonic.webapi.geolocation
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API
"""

from __future__ import annotations

import time
from typing import Any

from domonic.javascript import Error


class Geolocation:
    def __init__(self, coords: "GeolocationCoordinates | None" = None):
        self._coords = coords or GeolocationCoordinates()
        self._watchers: dict[int, tuple[Any, Any, Any]] = {}
        self._next_watch_id = 1

    def getCurrentPosition(self, successCallback, errorCallback=None, options=None):
        if not callable(successCallback):
            raise TypeError("getCurrentPosition successCallback must be callable")
        successCallback(GeolocationPosition(self._coords))
        return None

    def watchPosition(self, successCallback, errorCallback=None, options=None):
        if not callable(successCallback):
            raise TypeError("watchPosition successCallback must be callable")
        watch_id = self._next_watch_id
        self._next_watch_id += 1
        self._watchers[watch_id] = (successCallback, errorCallback, options or {})
        successCallback(GeolocationPosition(self._coords))
        return watch_id

    def clearWatch(self, watchId):
        self._watchers.pop(watchId, None)
        return None

    def setPosition(self, coords: "GeolocationCoordinates | dict[str, Any]"):
        if isinstance(coords, dict):
            coords = GeolocationCoordinates(**coords)
        self._coords = coords
        position = GeolocationPosition(self._coords)
        for successCallback, _errorCallback, _options in list(self._watchers.values()):
            successCallback(position)
        return position


class GeolocationPosition:
    def __init__(self, coords=None, timestamp=None):
        self.coords = coords or GeolocationCoordinates()
        self.timestamp = timestamp if timestamp is not None else time.time() * 1000


class GeolocationCoordinates:
    def __init__(
        self,
        latitude=0,
        longitude=0,
        altitude=None,
        accuracy=0,
        altitudeAccuracy=None,
        heading=None,
        speed=None,
    ):
        self.latitude = latitude
        self.longitude = longitude
        self.altitude = altitude
        self.accuracy = accuracy
        self.altitudeAccuracy = altitudeAccuracy
        self.heading = heading
        self.speed = speed


class GeolocationError(Error):

    PERMISSION_DENIED = 1
    POSITION_UNAVAILABLE = 2
    TIMEOUT = 3

    # def __init__(self, code, message,):
    #     self.code = code
    # self.message = message
    # super().__init__(message)
