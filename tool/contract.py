from stl import Node
from stl import process
from utilities import join_stringlists, remove_dups_stringlist

class Contract(object):
	"""docstring for Contract"""
	def __init__(self, variables, assumptions, guarantees):
		self.process_assumptions(assumptions)
		self.process_guarantees(guarantees)
		self.process_variables(variables)
		self.__isSat = 0

	def process_assumptions(self, assumptions):
		assum_arr = []
		var_str = ""
		for assumption in assumptions:
			temp_root = process(assumption)
			assum_arr.append(temp_root)
			var_str += temp_root.vars
		self.__assumptions = Node(None, assum_arr, 0, "&&", remove_dups_stringlist(var_str), None, None, "&&")

	def process_guarantees(self, guarantees):
		guar_arr = []
		var_str = ""
		for guarantee in guarantees:
			temp_root = process(guarantee)
			guar_arr.append(temp_root)
			var_str += temp_root.vars
		self.__guarantees = Node(None, guar_arr, 0, "&&", remove_dups_stringlist(var_str), None, None, "&&")

	def process_variables(self, variables):
		for var in variables:
			self.__assumptions.propogate_var_down(var, None, 1)
			self.__guarantees.propogate_var_down(var, None, 1)
		self.__variables = variables

	@property
	def variables(self):
		return self.__variables

	@property
	def assumptions(self):
		return self.__assumptions

	@property
	def guarantees(self):
		return self.__guarantees

	def saturate(self):
		notA = Node(None, self.__assumptions, 0, "!", self.__assumptions.vars, None, None, "!")
		self.__guarantees = Node(None, [notA,self.guarantees], 0, "||", join_stringlists(notA.vars,self.__guarantees.vars), None, None, "||")
		notA.parent = self.__guarantees
		self.__isSat = 1

	def __repr__(self):
		return "Variables:\n"+self.__variables+"\nAssumptions:"+self.__assumptions+"\nGuarantees:"+self.__guarantees
