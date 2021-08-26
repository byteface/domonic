"""
    domonic.d3.timer
    ====================================

    # TODO - completely untested

"""

from domonic.javascript import *

frame = 0  # is an animation frame pending?
timeout = None # 0  # is a timeout pending?
interval = 0  # are any timers active?
pokeDelay = 1000  # how frequently we check for clock skew
taskHead = None
taskTail = None
clockLast = 0
clockNow = 0
clockSkew = 0
clock = performance  # if isinstance(performance, object) and performance.now else Date
# setFrame = window.requestAnimationFrame.bind(window)  # if isinstance( window, object) and window.requestAnimationFrame ?  : function(f) { setTimeout(f, 17); }

def fr(f):
    """ framerate """
    setTimeout(f, 17)
setFrame = fr


def now():
    global clockNow
    global clockSkew
    clockNow = clock.now() + clockSkew
    return clockNow or (setFrame(clearNow), clockNow)

def clearNow():
    global clockNow
    clockNow = 0

class Timer():

    def __init__(self):
        self._call = None
        self._time = None
        self._next = None

    def restart(self, callback, delay, time):

        global taskTail
        global taskHead

        if not callable(callback):
            raise Error("callback is not a function")

        b = 0 if delay == None else delay
        time = now() if time == None else time + b

        if not self._next and taskTail != self:
            if taskTail:
                taskTail._next = self
        else:
            taskHead = self

        taskTail = self

        self._call = callback
        self._time = time
        sleep()

    def stop(self):
        if (self._call):
            self._call = None
            self._time = Infinity
        sleep()


def timer(callback, delay, time):
    t = Timer()
    t.restart(callback, delay, time)
    return t


def timerFlush():
    global frame
    now()  # Get the current time, if not already set.
    frame += 1  # Pretend we’ve set an alarm, if we haven’t already.
    t = taskHead
    #   e
    while t:
        e = clockNow - t._time
        if e >= 0:
            t._call.call(None, e)
        t = t._next
    frame -= 1


def wake():
    global timeout
    global clockLast
    global clockNow
    global frame
    clockLast = clock.now()
    clockNow = (clockLast) + clockSkew
    frame = timeout = 0
    try:
        timerFlush()
    finally:
        frame = 0
        nap()
        clockNow = 0


def poke():
    global clockLast
    global clockSkew
    now = clock.now()
    delay = now - clockLast
    if delay > pokeDelay:
        clockSkew -= delay
        clockLast = now


def nap():
    global taskHead
    global taskTail
    # t0
    t1 = taskHead
    # t2
    time = Infinity
    while t1:
        if (t1._call):
            if time > t1._time:
                time = t1._time
                t0 = t1
                t1 = t1._next
            else:
                t2 = t1._next
                t1._next = None
                t0._next = t2
                taskHead = t2
                t1 = t0._next if t0 else taskHead
        taskTail = t0
        sleep(time)


def sleep(time=0):
    global frame
    global clockNow
    global clockLast
    global timeout
    global interval
    if frame:
        return  # Soonest alarm already set, or will be.
    print(timeout)
    if timeout is not None:
        timeout = Global.clearTimeout(timeout)
    delay = time - clockNow  # Strictly less than if we recomputed clockNow.
    if delay > 24:
        if time < Infinity:
            timeout = Global.setTimeout(wake, time - clock.now() - clockSkew)
        if interval:
            interval = Global.clearInterval(interval)
        else:
            if not interval:
                clockLast = clock.now()
                interval = Global.setInterval(poke, pokeDelay)
        frame = 1
        setFrame(wake)

def timeout(callback, delay, time):
    t = Timer()
    delay = 0 if delay == None else delay

    def elapsed():
        t.stop()
        callback(elapsed + delay)
    t.restart(elapsed, delay, time)
    return t


def interval(callback, delay=None, time=None):

    t = Timer()
    total = delay
    if delay == None:
        t.restart(callback, delay, time)
        return t
    t._restart = t.restart

    def r(callback, delay, time):
        delay = delay
        time = now() if time == None else time

        def tick(elapsed):
            nonlocal total
            elapsed += total
            total += delay
            t._restart(tick, total, time)
            callback(elapsed)
        t._restart(tick, delay, time)

    t.restart = r
    t.restart(callback, delay, time)
    return t
