"""
domonic.webapi.mediasession
====================================
https://developer.mozilla.org/en-US/docs/Web/API/Media_Session_API
"""


class MediaSession:
    def __init__(self):
        self.metadata = None
        self.playbackState = "none"
        self._action_handlers = {}
        self._position_state = None

    def setActionHandler(self, action, handler):
        if handler is not None and not callable(handler):
            raise TypeError("MediaSession action handler must be callable or None")
        if handler is None:
            self._action_handlers.pop(action, None)
        else:
            self._action_handlers[action] = handler
        return None

    def setPositionState(self, positionState):
        self._position_state = dict(positionState or {})
        return None

    def dispatchAction(self, action, details=None):
        handler = self._action_handlers.get(action)
        if handler is None:
            return None
        return handler(details or {})

    @property
    def positionState(self):
        return self._position_state


# class MediaImage:
#     src = ""
#     sizes = ""
#     type = ""
