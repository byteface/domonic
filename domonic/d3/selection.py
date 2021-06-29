"""
    domonic.d3.selection
    ====================================

	https://github.com/d3/d3-selection/tree/main/src/selection

"""


# same as dquery?!
class Selection:


	@classmethod
	def _selection(self, *args. **kwargs):
		"""
			creates an instance of a selection
		"""
	    return Selection( *args, **kwargs)


	def append(self, *args):
		self.this.appendChild(args)
	    return self  #.this


	# def attr(self, *args):


	def call(self, *args):
		callback = args[0]
		args[0] = self.this
		# callback(None,args)
		callback(args)
		return self  #.this


d3.select = Selection._selection()