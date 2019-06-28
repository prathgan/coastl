from stl import *

class Contract(object):
	"""docstring for Contract"""
	def __init__(self, variables, assumptions, guarantees):
		self.process_variables(variables)
		self.process_assumptions(assumptions)
		self.process_guarantees(guarantees)
		self.__isSat = 0

	def process_variables(self, variables):
		self.__variables = variables

	def process_assumptions(self, assumptions):
		arr = []
		for assumption in assumptions:
			arr.append(process(assumption))
		self.__assumptions = arr

	def process_guarantees(self, guarantees):
		self.__guarantees = guarantees

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
		# A becomes A, and G becomes G or not A
		pass

	def __repr__(self):
		print("Variables:")
		print(self.__variables)
		print("Assumptions:")
		print(self.__assumptions)
		print("Guarantees:")
		print(self.__guarantees)
