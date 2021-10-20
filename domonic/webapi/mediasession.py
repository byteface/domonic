"""
    domonic.webapi.mediasession
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/MediaStream_Image_Capture_API
"""

class MediaSession:

    def __init__(self):
        self.metadata = {}
        self.playbackState = {}

    def setActionHandler(self, action, handler):
        # self.actionHandler = handler
        pass

    def setPositionState(self, positionState):
        pass


# class MediaImage:
#     src = ""
#     sizes = ""
#     type = ""
