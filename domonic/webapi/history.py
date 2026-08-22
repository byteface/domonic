"""
domonic.webapi.history
====================================
https://developer.mozilla.org/en-US/docs/Web/API/History
"""

from domonic.events import PopStateEvent


class History:  # (EventTarget):
    def __init__(self, window=None):
        self.window = window
        self.states = []
        self.index = 0
        self.skip_update = False
        try:
            if self.window is not None:
                self.states.append(self.window.location.href)
                self.index = 1
        except Exception as e:
            print("History is empty:", e)

    def _update(self, url: str):
        """Updates the current history state"""
        if self.skip_update:
            self.skip_update = False
            return
        self.states.append(url)
        self.index = len(self.states) - 1
        # self.dispatchEvent(Event('popstate'))

    def back(self):
        """Loads the previous URL in the history list"""
        self.go(-1)
        self.skip_update = True
        if self.window:
            self.window.location = self.states[self.index]
            self.window.dispatchEvent(PopStateEvent("popstate", {"state": self.state}))
        # self.dispatchEvent(Event('popstate'))

    def forward(self):
        """Loads the next URL in the history list"""
        self.go(1)
        self.skip_update = True
        if self.window:
            self.window.location = self.state  # s[self.index]
            self.window.dispatchEvent(PopStateEvent("popstate", {"state": self.state}))

    def go(self, n: int):
        """Loads a specific URL from the history list"""
        self.index += n
        if self.index < 1:
            self.index = 1
        if self.index > self.length:
            self.index = self.length
        return self.index

    @property
    def length(self):
        """Returns the number of URLs in the history list"""
        return len(self.states)

    # def pushState(self, data, title, url):
    #     return self.replaceState(data, title, url)

    # def replaceState(self, data, title, url):
    #     self.states[self.index] = url

    @property
    def state(self):
        if not self.states:
            return None
        if self.index >= len(self.states):
            return self.states[-1]
        return self.states[self.index]

    def __repr__(self) -> str:
        # show the full history
        from pprint import pformat

        return pformat(self.states)
