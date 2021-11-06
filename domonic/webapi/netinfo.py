"""
    domonic.webapi.netinfo
    ====================================
    https://developer.mozilla.org/en-US/docs/Web/API/Network_Information_API
"""

from domonic.dom import EventTarget

class NetworkInformation(EventTarget):

    def __init__(self):
        self.type = None
        self.downlinkMax = None
        self.effectiveType = None
        self.rtt = None
        self.saveData = None
        self.downlink = None
        self.effectiveType = None
        self.rtt = None

    def __str__(self):
        return 'type: {}, downlinkMax: {}, effectiveType: {}, rtt: {}, saveData: {}, downlink: {}, effectiveType: {}, rtt: {}'.format(
            self.type, self.downlinkMax, self.effectiveType, self.rtt, self.saveData, self.downlink, self.effectiveType, self.rtt
        )
