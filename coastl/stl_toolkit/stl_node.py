class Node(object):
	def __init__(self, parent, child1, child2, type, logic, vars, range_start, range_end, string_rep):
		"""
		Constructs node to be used in tree representing expression of signal temporal logical.

	    Parameters
	    ----------
	    parent: 		pointer to the object of parent of this node
	    child1: 		pointer to the object of child1; points to anterior requirement of 'until' logic
		child2: 		pointer to the object of child2; points to posterior condition of 'until' logic
	    type: 			part of logic which this node represents; logic (0) or predicate (1)
	    logic: 			logic operator which which this node represents, null if predicate node
	    vars: 			variables which this node pertains to
	    range_start: 	start of range for complex operator nodes, min range
	    range_end: 		end of range for complex operator nodes, max range
		string_rep: 	string representation of node
	    """
		self.__parent = parent
		self.__child1 = child1
		if child1 is not None:
			self.__child1.parent = self
		self.__child2 = child2
		if child2 is not None:
			self.__child2.parent = self
		self.__type = type
		self.__logic = logic
		self.__vars = vars
		self.__range_start = range_start
		self.__range_end = range_end
		self.__value = ""
		self.__string_rep = string_rep
		self.__gurobi_vars = []

	@property
	def parent(self):
		"""Return parent"""
		return self.__parent

	@property
	def child1(self):
		"""Return child1"""
		return self.__child1

	@property
	def child2(self):
		"""Return child2"""
		return self.__child2

	@property
	def type(self):
		"""Return type"""
		return self.__type

	@property
	def logic(self):
		"""Return logic"""
		return self.__logic

	@property
	def vars(self):
		"""Return vars"""
		return self.__vars

	@property
	def range_start(self):
		"""Return range_start"""
		return self.__range_start

	@property
	def range_end(self):
		"""Return range_end"""
		return self.__range_end

	@property
	def gurobi_vars(self):
		"""Return gurobi_vars"""
		return self.__gurobi_vars

	@parent.setter
	def parent(self, parent):
		"""Set parent"""
		self.__parent = parent

	def set_parent_alt(self,parent):
		"""Set parent while setting open child of parent to self"""
		self.__parent = parent
		if parent.child1 == None:
			parent.child1 = self
		elif parent.child2 == None:
			parent.child2 = self

	@child1.setter
	def child1(self, children):
		"""Set children"""
		self.__child1 = child1

	@child2.setter
	def child2(self, children):
		"""Set children"""
		self.__child2 = child2

	@range_start.setter
	def range_start(self, range_start):
		"""Set range_start"""
		self.__range_start = range_start

	@range_end.setter
	def range_end(self, range_end):
		"""Set range_end"""
		self.__range_end = range_end

	def add_gurobi_var(self, var):
		self.__gurobi_vars.append(var)

	def propogate_var_up(self, var):
		"""Remove all variables except for var until junction node"""
		if (self.__child1!=None and self.__child2!=None) or self.__parent==None:
			return
		self.__vars = var
		self.__parent.propogate_var_up(var)

	def propogate_var_down(self, var, parent, top):
		"""Propogate value of var down children and set parents"""
		if top == 0:
			self.__parent = parent
		if self.__child1==None and self.__child2 == None:
			self.propogate_var_up(self.vars)
		if self.__child1 != None:
			self.__vars += "," + var
			self.__child1.propogate_var_down(var, self, 0)
		if self.__child2 != None:
			self.__vars += "," + var
			self.__child2.propogate_var_down(var, self, 0)

	def get_highest_ancestor(self):
		"""Return highest ancestor"""
		if __parent == None:
			return self
		else:
			return __parent.get_highest_ancestor

	@property
	def value_alt(self):
		"""Complicated return string representation of this node"""
		if self.__type==0:
			if self.__logic=="G" or self.__logic=="F" or self.__logic=="U":
				self.__value = self.__logic+"["+str(self.__range_start)+","+\
				str(self.__range_end)+"]"
			if self.__logic=="~" or self.__logic=="|" or self.__logic=="&":
				self.__value = self.__logic
		elif self.__type==1:
			self.__value = str(self.__vars)+self.__logic+\
			str(self.__range_start if self.__range_start==self.__range_end else\
			self.__range_start if self.__range_end==None else self.__range_end)
		return self.__value

	@property
	def string_rep(self):
		"""Return string_rep"""
		return self.__string_rep

	@property
	def value(self):
		"""Return string representation of this node"""
		return self.__string_rep

	def __repr__(self, level=0):
		"""Return string representation of this node"""
		ret = "\t"*level+repr(self.value)
		children = []
		if self.__child1 != None:
			children.append(self.__child1)
		if self.__child2 != None:
			children.append(self.__child2)
		for child in children:
			ret += "\n" + child.__repr__(level+1)
		return ret
