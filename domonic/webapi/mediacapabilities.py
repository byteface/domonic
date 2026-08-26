"""
domonic.webapi.mediacapabilities
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Media_Capabilities_API
"""

from __future__ import annotations


def _configuration_supported(configuration):
    audio = configuration.get("audio") or {}
    video = configuration.get("video") or {}
    has_media = bool(audio or video)
    has_type = bool(audio.get("contentType") or video.get("contentType"))
    return has_media and has_type


class MediaCapabilities:
    def encodingInfo(self, mediaEncodingConfiguration):
        supported = _configuration_supported(mediaEncodingConfiguration or {})
        return {
            "supported": supported,
            "smooth": supported,
            "powerEfficient": supported,
            "keySystemAccess": None,
        }

    def decodingInfo(self, mediaDecodingConfiguration):
        supported = _configuration_supported(mediaDecodingConfiguration or {})
        return {
            "supported": supported,
            "smooth": supported,
            "powerEfficient": supported,
            "keySystemAccess": None,
        }


# MediaDecodingConfiguration
# MediaEncodingConfiguration
# VideoConfiguration
# AudioConfiguration
