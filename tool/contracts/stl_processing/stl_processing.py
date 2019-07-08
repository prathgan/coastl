import re
from gurobipy import *
from .stl_parsing import parse_logic
from .utilities.simple_utilities import remove_gurobi_log, parentheses_match

def process(logic, remove_log=False):
	"""
	Return result of passing logic expression into process_logic()
	"""
	if not parentheses_match(logic):
		raise ValueError("Opening and closing brackets do not match, check '(' and ')'")
	stl_tree = parse_logic(logic, None, None)
	m = Model("optimization_model")
	# add constraints
	# solve problem
	if remove_log:
		remove_gurobi_log()
	return stl_tree
