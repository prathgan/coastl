"""
later add functionality which translates string of logic such as "!G[0,10](F[1,3](!(x>=1)&&(y<=0))" intro tree structure
"""

class Node(object):
	
	"""Constructs node to be used in tree representing expression of signal temporal logical.

        Parameters
        ----------
        parent: pointer to the object of 
        child1: pointer to the object of
        child2: pointer to the object of 
        ttype: part of logic which this node represents; logic (0) or predicate (1) (ttype not type because type is Python keyword)
        logic: logic operator which which this node represents, null if predicate node
        vvars: variables which this node pertains to (vvars not vars because vars is Python keyword)
        range_start: start of range for complex operator nodes
        range_end: end of range for complex operator nodes

        Raises
        ------
        
        """
	def __init__(self, parent, child1, child2, ttype, logic, vvars, range_start, range_end):
		self.__parent = parent
		self.__child1 = child1
		self.__child2 = child2
		self.__type = ttype
		self.__logic = logic
		self.__vars = variables
		self.__range_start = range_start
		self.__range_end = range_end

	@property
	def parent(self):
		return self.__parent
		
	@property
	def child1(self):
		return self.__child1
	
	@property
	def child2(self):
		return self.__child2

	@property
	def type(self):
		return self.__type

	@property
	def logic(self):
		return self.__logic
	
	@property
	def vars(self):
		return self.__vars
	
	@property
	def range_start(self):
		return self.__range_start

	@property
	def range_end(self):
		return self.__range_end

		