from domonic.javascript import Math

"""
t : current time
b : start value
c : change
d : total time

http://robertpenner.com/easing/

"""


class Back():

    @staticmethod
    def easeIn(t, b, c, d, aa, bb, s=1.70158):
        t /= d
        return c * t * t * ((s + 1) * t - s) + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb, s=1.70158):
        t = t / d - 1
        return c * (t * t * ((s + 1) * t + s) + 1) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb, s=1.70158):
        t /= d / 2
        s *= 1.525
        if t < 1:
            return c / 2 * (t * t * ((s + 1) * t - s)) + b

        t -= 2
        return c/2 * (t * t * ((s + 1) * t + s) + 2) + b


class Bounce():

    @staticmethod
    def easeIn(t, b, c, d, aa=0, bb=0):
        return c - Bounce.easeOut(d-t, 0, c, d) + b

    @staticmethod
    def easeOut(t, b, c, d, aa=0, bb=0):
        t /= d
        if t < (1/2.75):
            return c*(7.5625*t*t) + b

        elif t < (2/2.75):
            t -= (1.5/2.75)
            return c*(7.5625*t*t + 0.75) + b

        elif t < (2.5/2.75):
            t -= (2.25/2.75)
            return c*(7.5625*t*t + 0.9375) + b

        else:
            t -= (2.625/2.75)
            return c*(7.5625*t*t + 0.984375) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa=0, bb=0):
        if t < d/2:
            return Bounce.easeIn(t*2, 0, c, d) * .5 + b
        return Bounce.easeOut(t*2-d, 0, c, d) * .5 + c*.5 + b


class Circ():

    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        t /= d
        return -c * (Math.sqrt(1 - t*t) - 1) + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        t /= d
        t -= 1
        return c * Math.sqrt(1 - t*t) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        t /= d/2
        if t < 1:
            return -c/2 * (Math.sqrt(1 - t*t) - 1) + b
        t -= 2
        return c/2 * (Math.sqrt(1 - t*t) + 1) + b


class Cubic():

    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        t /= d
        return c*t*t*t + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        t /= d
        t -= 1
        return c * (t*t*t + 1) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        t /= d/2
        if t < 1:
            return c/2*t*t*t + b
        t -= 2
        return c/2*(t*t*t + 2) + b


class Elastic():

    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        s = 1.70158
        p = 0
        a = c
        if t == 0:
            return b

        t /= d
        if t == 1:
            return b + c

        if not p:
            p = d * .3

        if a < abs(c):
            a = c
            s = p/4
        else:
            s = p/(2*Math.PI) * Math.asin(c/a)

        t -= 1
        return -(a*Math.pow(2, 10 * t) * Math.sin((t*d-s)*(2*Math.PI)/p)) + b


    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        s = 1.70158
        p = 0
        a = c
        if t == 0:
            return b

        t /= d
        if t == 1:
            return b + c

        if not p:
            p = d * .3

        if a < abs(c):
            a = c
            s = p/4
        else:
            s = p/(2*Math.PI) * Math.asin(c/a)

        return a * Math.pow(2, -10*t) * Math.sin((t*d-s)*(2*Math.PI) / p) + c + b


    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        s = 1.70158
        p = 0
        a = c
        if t == 0:
            return b

        t /= d/2
        if t == 2:
            return b + c

        if not p:
            p = d * (.3 * 1.5)

        if a < abs(c):
            a = c
            s = p/4
        else:
            s = p/(2*Math.PI) * Math.asin(c/a)


        if t < 1:
            t -= 1
            return -a/2 *Math.pow(2, 10*t) * Math.sin((t*d - s)*(2*Math.PI) / p) + b

        t -= 1
        return a * Math.pow(2, -10*t) * Math.sin((t*d - s)*(2*Math.PI) / p) * .5 + c + b


class Expo():

    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        return c * Math.pow(2, 10 * (t/d - 1)) + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        return c * (-Math.pow(2, -10 * t/d) + 1) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        t /= d/2
        if t < 1:
            return c/2 * Math.pow(2, 10 * (t - 1)) + b
        t -= 1
        return c/2 * (-Math.pow(2, -10 * t) + 2) + b


class Linear():

    # lambda t, b, c, d : c*t/d + b

    @staticmethod
    def easeNone(t, b, c, d, aa, bb):
        return c*t/d + b

    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        return c*t/d + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        return c*t/d + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        return c*t/d + b


class Quad():

    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        t /= d
        return c*t*t + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        t /= d
        return -c * t*(t-2) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        t /= d/2
        if t < 1:
            return c/2*t*t + b
        t-=1
        return -c/2 * (t*(t-2) - 1) + b


class Quart():

    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        t /= d
        return c*t*t*t*t + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        t /= d
        t -= 1
        return -c * (t*t*t*t - 1) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        t /= d/2
        if t < 1:
            return c/2*t*t*t*t + b
        t -= 2
        return -c/2 * (t*t*t*t - 2) + b


class Quint():
    
    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        t /= d
        return c*t*t*t*t*t + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        t /= d
        t -= 1
        return c*(t*t*t*t*t + 1) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        t /= d/2
        if t < 1:
            return c/2*t*t*t*t*t + b
        t -= 2
        return c/2*(t*t*t*t*t + 2) + b


class Sine():

    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        return -c * Math.cos(t/d * (Math.PI/2)) + c + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        return c * Math.sin(t/d * (Math.PI/2)) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        return -c/2 * (Math.cos(Math.PI*t/d) - 1) + b


# class Angle():
    
#     @staticmethod
#     def easeIn(t, b, c, d, aa, bb):
#         return -c * (t/d - 1) + b

#     @staticmethod
#     def easeOut(t, b, c, d, aa, bb):
#         return c * (t/d) + b

#     @staticmethod
#     def easeInOut(t, b, c, d, aa, bb):
#         if t==0:
#             return b
#         elif t==d:
#             return b+c
#         else:
#             return -c/2 * (t/d - 2) + b

# class Zoom():
#     @staticmethod
#     def easeIn(t, b, c, d, aa, bb):
#         return c * t/d + b

#     @staticmethod
#     def easeOut(t, b, c, d, aa, bb):
#         return c * (t - d/2)/d + b

#     @staticmethod
#     def easeInOut(t, b, c, d, aa, bb):
#         if t<d/2:
#             return c/2 * t/d + b
#         t-=d/2
#         return c/2 * (t/d - 1) + b

'''
class Exponential():
    
    @staticmethod
    def easeIn(t, b, c, d, aa, bb):
        if t == 0:
            return b
        else:
            return c * Math.pow(2, 10 * (t/d - 1)) + b

    @staticmethod
    def easeOut(t, b, c, d, aa, bb):
        if t == d:
            return b + c
        else:
            return c * (-Math.pow(2, -10 * t/d) + 1) + b

    @staticmethod
    def easeInOut(t, b, c, d, aa, bb):
        if t==0:
            return b
        elif t==d:
            return b+c

        t = t / (d * 0.5)

        if t < 1:
            return c/2 * Math.pow(2, 10 * (t - 1)) + b
        t -= 1
        return c/2 * (-Math.pow(2, -10 * t) + 2) + b
'''

# class PressIn():
    
#     @staticmethod
#     def easeIn(t, b, c, d, aa, bb):
#         return c - b*t/d

#     @staticmethod
#     def easeOut(t, b, c, d, aa, bb):
#         return b*t/d + c

#     @staticmethod
#     def easeInOut(t, b, c, d, aa, bb):
#         if t==0:
#             return b
#         t *= 2
#         if t < 1:
#             return c - b*t/d
#         return b*t/d + c