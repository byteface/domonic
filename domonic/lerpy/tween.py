from domonic.javascript import window
from domonic.events import EventDispatcher
from domonic.events import TweenEvent
from domonic.lerpy import get_timer
from domonic.lerpy.easing import *


class TweenEquation(object):
    def __init__(self, ease, extra=None):
        self.ease = ease
        self.extra = extra


class TweenData(object):
    def __init__(self, prop, target, equation=None):
        self.prop = prop
        self.target = target
        self.equation = equation
        self.start = 0
        self.change = 0


class Tween(EventDispatcher):
    """

    Tween is a complex lerp but you don't have do the math cos robert penner did already.
    Just pass an easing equation from the easing package

    i.e

    twn = Tween(someObj, { 'x':10, 'y':5, 'z':3}, 6, Linear.easeIn )

    will tween the objects properties over the given time using Linear.easeIn

    """

    FPS = 60

    _tweening = False
    _paused = False
    _target = None
    _values = None
    _equations = None
    _duration = 0
    _delay = 0
    _position = 0
    _loop = False
    _timeStart = 0
    _timePaused = 0
    _timePrevious = 0

    def __init__(self, target=None, values=None, duration=0, equations=None, delay=0, loop=False):
        self.target = target
        self.values = values
        self.duration = duration
        self.equations = equations
        self.delay = delay
        self.loop = loop
        self._intID = None
        super().__init__()

    @property
    def tweening(self):
        return self._foo

    @property
    def paused(self):
        return self._paused

    @property
    def position(self):
        if self._position < 0:
            return 0
        elif self._position > 100:
            return 100
        else:
            return self._position

    @property
    def target(self):
        return self._target

    @target.setter
    def target(self, target):
        self._target = target

    @property
    def values(self):
        v = {}
        for value in self._values:
            v[value.prop] = value.target
        return v

    @values.setter
    def values(self, values):
        if values != None:
            self._values = []
            for s in values:
                self._values.append(TweenData(s, values[s]))
            self.equations = self._equations

    @property
    def duration(self):
        return self._duration  # /1000

    @duration.setter
    def duration(self, duration):
        self._duration = duration  # * 1000

    @property
    def equations(self):
        return self._equations

    @equations.setter
    def equations(self, equations):
        if equations != None:
            self._equations = equations
            e = equations if type(equations) == list else [equations]
            i = 0
            for v in self._values:
                i = len(e) - 1 if i > len(e) - 1 else i
                if callable(e[i]):
                    p = TweenEquation(e[i])
                else:
                    p = TweenEquation(e[i].fn, {'a': e[i].a, 'b': e[i].b})
                v.equation = p
                i += 1

    @property
    def delay(self):
        return self._delay  # / 1000

    @delay.setter
    def delay(self, delay):
        self._delay = delay  # * 1000

    @property
    def loop(self):
        return self._loop

    @loop.setter
    def loop(self, loop):
        """ Set to True if you want it to loop """
        self._loop = loop

    def start(self):
        self._timeStart = get_timer()   # TODO!! ---
        self._timePaused = 0
        self._timePrevious = self._timeStart
        self._position = 0

        for v in self._values:
            v.start = self._target[v.prop]
            v.change = v.target - v.start

        self._tweening = True
        self._paused = False
        self._intID = window.setInterval(self._update, 1000 / Tween.FPS, TweenEvent(TweenEvent.TIMER))
        self.dispatchEvent(TweenEvent(TweenEvent.START, self))

    def stop(self):
        self._tweening = False
        self.dispatchEvent(TweenEvent(TweenEvent.STOP, self))

        # NOTE
        # window.clearInterval(self._intID )
        # clearInt fails. because join won't allow as a 'return' happens just after the stop
        self._intID.stopped.set()  # call stopped on the thread so program exits

    def pause(self):
        """ Pauses the tween from changing the values  """
        # TODO - pause should modify timer so it DOESNT jump frames. at mo does the opposite.
        # seems to not increment. then suddenly jumps to catch up with where it should be
        self._paused = True
        self.dispatchEvent(TweenEvent(TweenEvent.PAUSE if self._paused else TweenEvent.UNPAUSE, self))

    def unpause(self):
        """ unpauses the tween """
        self._paused = False
        self.dispatchEvent(TweenEvent(TweenEvent.UNPAUSE, self))

    def reset(self):

        for v in self._values:
            self._target[v.prop] = v.start
        self._update(get_timer())
        self.dispatchEvent(TweenEvent(TweenEvent.RESET, self))

    def _update(self, event):
        timeCurrent = get_timer()
        if self._tweening:
            if not self._paused:
                self.dispatchEvent(TweenEvent(TweenEvent.UPDATE_START, self))
                time = timeCurrent - self._timePaused - self._timeStart
                self._position = 100 / (self._duration + self._delay) * time

                if time < self._delay:
                    return
                time -= self._delay

                if time > self._duration:
                    for v in self._values:
                        self._target[v.prop] = v.target

                    if self._loop:
                        self._timeStart = timeCurrent
                        self._timePaused = 0
                        self._timePrevious = self._timeStart
                        self._position = 0
                        self.reset()
                    else:
                        self.dispatchEvent(TweenEvent(TweenEvent.UPDATE_END, self))
                        self.stop()
                        self.dispatchEvent(TweenEvent(TweenEvent.COMPLETE, self))

                    return

                for v in self._values:
                    e = v.equation
                    x = e.extra
                    a = x.a if x != None else 0
                    b = x.b if x != None else 0
                    self._target[v.prop] = e.ease(time, v.start, v.change, self._duration, a, b)

                self.dispatchEvent(TweenEvent(TweenEvent.UPDATE_END, self))

            else:
                self._timePaused += (timeCurrent - self._timePrevious)

            self._timePrevious = timeCurrent

    # def _dispatchEvent(self, event):
    #     if event.type == TweenEvent.UPDATE_START:
    #         self._timeStart = get_timer()
    #         self._timePaused = 0
    #         self._timePrevious = self._timeStart
    #         self._position = 0
    #         self.dispatchEvent(event)
    #     elif event.type == TweenEvent.UPDATE_END:
    #         self.dispatchEvent(event)
    #     elif event.type == TweenEvent.START:
    #         self.dispatchEvent(event)
    #     elif event.type == TweenEvent.STOP:
    #         self.dispatchEvent(event)
    #     elif event.type == TweenEvent.PAUSE:
    #         self.dispatchEvent(event)
    #     elif event.type == TweenEvent.UNPAUSE:
    #         self.dispatchEvent(event)
    #     elif event.type == TweenEvent.RESET:
    #         self.dispatchEvent(event)
    #     elif event.type == TweenEvent.COMPLETE:
    #         self.dispatchEvent(event)
    #     elif event.type == TweenEvent.UPDATE:
    #         self.dispatchEvent(event)
    #     else:
    #         super(Tween, self)._dispatchEvent(event)
