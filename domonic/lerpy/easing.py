from domonic.javascript import Math

"""
t : current time
b : start value
c : change
d : total time
"""


# class Back():

# 	@staticmethod
# 	def easeIn (t, b, c, d, aa, bb):
# 		if (s == None):
# 			s = 1.70158
# 		return c*(t/=d)*t*((s+1)*t - s) + b

# 	@staticmethod
# 	def easeOut (t, b, c, d, aa, bb):
# 		# var s : Number = aa == 0 ? 1.70158 : aa
# 		if (s == None) : s = 1.70158
# 		return c*((t=t/d-1)*t*((s+1)*t + s) + 1) + b

# 	@staticmethod
# 	def easeInOut (t, b, c, d, aa, bb):
# 		if (s == undefined) : s = 1.70158
# 		if ((t/=d/2) < 1):
# 			return c/2*(t*t*(((s*=(1.525))+1)*t - s)) + b
# 		return c/2*((t-=2)*t*(((s*=(1.525))+1)*t + s) + 2) + b


# class Bounce():
		
# 	@staticmethod
# 	def easeOut(t, b, c, d, aa = 0, bb = 0):
# 		if ((t/=d) < (1/2.75)):
# 			return c*(7.5625*t*t) + b
# 		elif (t < (2/2.75)):
# 			return c*(7.5625*(t-=(1.5/2.75))*t + .75) + b
# 		elif (t < (2.5/2.75)):
# 			return c*(7.5625*(t-=(2.25/2.75))*t + .9375) + b
# 		else:
# 			return c*(7.5625*(t-=(2.625/2.75))*t + .984375) + b

# 	@staticmethod
# 	def easeIn(t, b, c, d, aa = 0, bb = 0):
# 		return c - Bounce.easeOut(d-t, 0, c, d) + b

# 	@staticmethod
# 	def easeInOut(t, b, c, d, aa = 0, bb = 0):
# 		if (t < d/2) :
# 			return Bounce.easeIn (t*2, 0, c, d) * .5 + b
# 		else:
# 			return Bounce.easeOut (t*2-d, 0, c, d) * .5 + c*.5 + b


# class Circ():

# 	@staticmethod
# 	def easeIn(t, b, c, d, aa, bb):
# 		return -c * (Math.sqrt(1 - (t/=d)*t) - 1) + b

# 	@staticmethod
# 	def easeOut(t, b, c, d, aa, bb):
# 		return c * Math.sqrt(1 - (t=t/d-1)*t) + b

# 	@staticmethod
# 	def easeInOut(t, b, c, d, aa, bb):
# 		if ((t/=d/2) < 1) : return -c/2 * (Math.sqrt(1 - t*t) - 1) + b
# 		return c/2 * (Math.sqrt(1 - (t-=2)*t) + 1) + b


class Cubic():

	@staticmethod
	def easeIn(t, b, c, d, aa, bb):
		# return c*(t/=d)*t*t + b
		t /= d
		return c*t*t*t + b

	@staticmethod
	def easeOut(t, b, c, d, aa, bb):
		# return c*((t=t/d-1)*t*t + 1) + b
		t /= d
		t -= 1
		return c * (t*t*t + 1) + b

	@staticmethod
	def easeInOut(t, b, c, d, aa, bb):
		# if ((t/=d/2) < 1) : return c/2*t*t*t + b
		# return c/2*((t-=2)*t*t + 2) + b
		t /= d/2
		if t < 1:
			return c/2*t*t*t + b
		t -= 2
		return c/2*(t*t*t + 2) + b


# class Elastic():

# 	@staticmethod
# 	def easeIn (t, b, c, d, aa, bb):
# 			a = aa
# 			p = bb
# 			if (t==0) : return b
# 			if ((t/=d)==1) : return b+c
# 			if (!p) : p=d*.3
# 			if (!a || a < Math.abs(c)):
# 				a=c
# 				s=p/4
# 			else:
# 				s = p/(2*Math.PI) * Math.asin (c/a)
# 			return -(a*Math.pow(2,10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )) + b

# 	@staticmethod
# 	def easeOut (t, b, c, d, aa, bb):
# 			a = aa
# 			p = bb
# 			if (t==0) : return b
# 			if ((t/=d)==1) : return b+c
# 			if (!p) p=d*.3
# 			if (!a || a < Math.abs(c)):
# 				a=c
# 				s=p/4
# 			else:
# 				s = p/(2*Math.PI) * Math.asin (c/a)
# 			return (a*Math.pow(2,-10*t) * Math.sin( (t*d-s)*(2*Math.PI)/p ) + c + b)

# 	@staticmethod
# 	def easeInOut (t, b, c, d, aa, bb):
# 			a = aa
# 			p = bb
# 			if (t==0) : return b
# 			if ((t/=d/2)==2) : return b+c
# 			if (!p) : p=d*(.3*1.5)
# 			if (!a || a < Math.abs(c)) :
# 				a=c
# 				s=p/4
# 			else:
# 				s = p/(2*Math.PI) * Math.asin (c/a)
# 			if (t < 1) : return -.5*(a*Math.pow(2,10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )) + b
# 			return a*Math.pow(2,-10*(t-=1)) * Math.sin( (t*d-s)*(2*Math.PI)/p )*.5 + c + b


# class Expo():

# 	@staticmethod
# 	def easeIn (t, b, c, d, aa, bb):
# 		return (t==0) ? b : c * Math.pow(2, 10 * (t/d - 1)) + b

# 	@staticmethod
# 	def easeOut (t, b, c, d, aa, bb):
# 		return (t==d) ? b+c : c * (-Math.pow(2, -10 * t/d) + 1) + b

# 	@staticmethod
# 	def easeInOut (t, b, c, d, aa, bb):
# 		if (t==0) : return b
# 		if (t==d) : return b+c
# 		if ((t/=d/2) < 1) : return c/2 * Math.pow(2, 10 * (t - 1)) + b
# 		return c/2 * (-Math.pow(2, -10 * --t) + 2) + b


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


# class Quad():

# 	@staticmethod
# 	def easeIn (t, b, c, d, aa, bb):
# 		return c*(t/=d)*t + b

# 	@staticmethod
# 	def easeOut (t, b, c, d, aa, bb):
# 		return -c *(t/=d)*(t-2) + b

# 	@staticmethod
# 	def easeInOut (t, b, c, d, aa, bb):
# 		if ((t/=d/2) < 1): return c/2*t*t + b
# 		return -c/2 * ((--t)*(t-2) - 1) + b


# class Quart():

# 	@staticmethod
# 	def easeIn (t, b, c, d, aa, bb):
# 		return c*(t/=d)*t*t*t + b

# 	@staticmethod
# 	def easeOut (t, b, c, d, aa, bb):
# 		return -c * ((t=t/d-1)*t*t*t - 1) + b

# 	@staticmethod
# 	def easeInOut (t, b, c, d, aa, bb):
# 		if ((t/=d/2) < 1): return c/2*t*t*t*t + b
# 		return -c/2 * ((t-=2)*t*t*t - 2) + b


# class Quint():
	
# 	@staticmethod
# 	def easeIn (t, b, c, d, aa, bb):
# 		return c*(t/=d)*t*t*t*t + b

# 	@staticmethod
# 	def easeOut (t, b, c, d, aa, bb):
# 		return c*((t=t/d-1)*t*t*t*t + 1) + b

# 	@staticmethod
# 	def easeInOut (t, b, c, d, aa, bb):
# 		if ((t/=d/2) < 1): return c/2*t*t*t*t*t + b
# 		return c/2*((t-=2)*t*t*t*t + 2) + b


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
