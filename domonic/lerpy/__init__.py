import time
_start = time.time()
def get_timer():
	end = time.time()
	return end-_start 


def lerp(a, b, d):
    return a * (1 - d) + b * d
# print lerp([3, 5], 0.75)