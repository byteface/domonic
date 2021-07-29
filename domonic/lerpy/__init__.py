import time
# import math
# from typing import Tuple

_start = time.time()

def get_timer():
    end = time.time()
    return end - _start

# def get_timer_str(t):
#     m, s = divmod(t, 60)
#     h, m = divmod(m, 60)
#     return "%d:%02d:%02d" % (h, m, s)

# def get_timer_str_ms(t):
#     m, s = divmod(t, 60)
#     h, m = divmod(m, 60)
#     return "%d:%02d:%02d.%03d" % (h, m, s, int(t * 1000) % 1000)



def lerp(a, b, d):
    return a * (1 - d) + b * d
# print lerp([3, 5], 0.75)



# def distance(point1, point2):
#     """ Return direct distance from point1 to point2. """
#     x_dist = abs(point1[0] - point2[0])
#     y_dist = abs(point1[1] - point2[1])
#     dist = math.sqrt(x_dist**2 + y_dist**2)
#     return dist
