"""
    domonic.webapi.geolocation
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Geolocation_API
"""

from domonic.events import Event
from domonic.javascript import Error


class Geolocation:

    @staticmethod
    def getCurrentPosition(successCallback, errorCallback, options):
        pass

    @staticmethod
    def watchPosition(successCallback, errorCallback, options):
        pass

    @staticmethod
    def clearWatch(watchId):
        pass


class GeolocationPosition():
    coords = None
    timestamp = None


class GeolocationCoordinates():
    latitude = None
    longitude = None
    altitude = None
    accuracy = None
    altitudeAccuracy = None
    heading = None
    speed = None


class GeolocationError(Error):

    PERMISSION_DENIED = 1
    POSITION_UNAVAILABLE = 2
    TIMEOUT = 3

    # def __init__(self, code, message,):
    #     self.code = code
        # self.message = message
        # super().__init__(message)
