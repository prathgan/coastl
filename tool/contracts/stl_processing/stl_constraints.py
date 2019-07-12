from gurobipy import *
from .stl_constraints_helpers import *
from .utilities.simple_utilities import remove_gurobi_log, parentheses_match

def create_constraints(node, m=None, remove_log=False, M=10**4, E=10**(-4)):
    if m is None:
        m = Model("solver")
    m = topmost_constr(node, m)
    m.update()
    node_switch_L = SwitchDict([("~",not_constr),
                              ("&&", and_constr),
                              ("||", or_constr),
                              ("G",g_constr),
                              ("F",f_constr)])
    node_switch_AP = SwitchDict([("<=",leq_constr),
                                (">=",geq_constr)])
    if node_switch_L[node.logic] is not None:
        m = node_switch_L[node.logic](node, m)
    else:
        m = node_switch_AP[node.logic](node, m, M, E)
    m.update()
    if node.child1 is not None:
        m = create_constraints(node.child1, m)
        m.update()
    if node.child2 is not None:
        m = create_constraints(node.child2, m)
        m.update()
    if remove_log:
        remove_gurobi_log()
    return m

def topmost_constr(node, m):
    if node.parent is None:
        bin_name = get_bin_name(node)
        exec(bin_name+"= m.addVar(vtype=GRB.BINARY, name='"+bin_name+"')")
        exec("node.add_gurobi_var("+bin_name+")")
        exec("m.addConstr("+bin_name+" == 1, 'c_"+bin_name+"')")
    m.update()
    return m

def not_constr(node, m):
    self_bin_name = get_bin_name(node)
    child1_bin_name = get_bin_name(node.child1)
    times = list(range(handle_no_range(node).range_start, handle_no_range(node).range_end+1))
    create_new_vars = False
    gurobi_vars_ind = 0
    for t in times:
        self_temp_bin_name = self_bin_name+"_"+str(t)
        child1_temp_bin_name = child1_bin_name+"_"+str(t)
        # add variables for ~ and expression
        if (not node.gurobi_vars) or create_new_vars:
            exec(self_temp_bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+self_temp_bin_name+"')")
            exec("node.add_gurobi_var("+self_temp_bin_name+")")
            create_new_vars = True
        else:
            exec(self_temp_bin_name+"=node.gurobi_vars["+str(gurobi_vars_ind)+"]")
            gurobi_vars_ind+=1
        exec(child1_temp_bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+child1_temp_bin_name+"')")
        exec("node.child1.add_gurobi_var("+child1_temp_bin_name+")")
        # add constraints to relate ~ and the expression at each timestep
        exec("m.addConstr("+ child1_temp_bin_name + " == 1 - " + self_temp_bin_name + ", 'c_" + self_temp_bin_name + "_1')")
        m.update()
    m.update()
    return m

def and_constr(node, m):
    self_bin_name = get_bin_name(node)
    child1_bin_name = get_bin_name(node.child1)
    child2_bin_name = get_bin_name(node.child2)
    times = list(range(handle_no_range(node).range_start, handle_no_range(node).range_end+1))
    create_new_vars = False
    gurobi_vars_ind = 0
    for t in times:
        self_temp_bin_name = self_bin_name+"_"+str(t)
        child1_temp_bin_name = child1_bin_name+"_"+str(t)
        child2_temp_bin_name = child2_bin_name+"_"+str(t)
        # add variables for &&, expression1, and expression2 at each timestep
        if (not node.gurobi_vars) or create_new_vars:
            exec(self_temp_bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+self_temp_bin_name+"')")
            exec("node.add_gurobi_var("+self_temp_bin_name+")")
            create_new_vars = True
        else:
            exec(self_temp_bin_name+"=node.gurobi_vars["+str(gurobi_vars_ind)+"]")
            gurobi_vars_ind+=1
        exec(child1_temp_bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+child1_temp_bin_name+"')")
        exec("node.child1.add_gurobi_var("+child1_temp_bin_name+")")
        exec(child2_temp_bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+child2_temp_bin_name+"')")
        exec("node.child2.add_gurobi_var("+child2_temp_bin_name+")")
        # add constraints to relate && and the expressions at each timestep
        exec("m.addConstr(2 * "+ self_temp_bin_name + " <= " + child1_temp_bin_name + "+" + child2_temp_bin_name + ", 'c_" + self_temp_bin_name + "_1')")
        exec("m.addConstr("+ child1_temp_bin_name + "+" + child2_temp_bin_name + " <= 1 + " + self_temp_bin_name + ", 'c_" + self_temp_bin_name + "_2')")
        m.update()
    m.update()
    return m

def or_constr(node, m):
    self_bin_name = get_bin_name(node)
    child1_bin_name = get_bin_name(node.child1)
    child2_bin_name = get_bin_name(node.child2)
    times = list(range(handle_no_range(node).range_start, handle_no_range(node).range_end+1))
    create_new_vars = False
    gurobi_vars_ind = 0
    for t in times:
        self_temp_bin_name = self_bin_name+"_"+str(t)
        child1_temp_bin_name = child1_bin_name+"_"+str(t)
        child2_temp_bin_name = child2_bin_name+"_"+str(t)
        # add variables for ||, expression1, and expression2 at each timestep
        if (not node.gurobi_vars) or create_new_vars:
            exec(self_temp_bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+self_temp_bin_name+"')")
            exec("node.add_gurobi_var("+self_temp_bin_name+")")
            create_new_vars = True
        else:
            exec(self_temp_bin_name+"=node.gurobi_vars["+str(gurobi_vars_ind)+"]")
            gurobi_vars_ind+=1
        exec(child1_temp_bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+child1_temp_bin_name+"')")
        exec("node.child1.add_gurobi_var("+child1_temp_bin_name+")")
        exec(child2_temp_bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+child2_temp_bin_name+"')")
        exec("node.child2.add_gurobi_var("+child2_temp_bin_name+")")
        # add constraints to relate || and the expressions at each timestep
        exec("m.addConstr(2 * "+ self_temp_bin_name + " <= " + child1_temp_bin_name + "+" + child2_temp_bin_name + ", 'c_" + self_temp_bin_name + "_1')")
        exec("m.addConstr("+ child1_temp_bin_name + "+" + child2_temp_bin_name + " <= 2 * " + self_temp_bin_name + ", 'c_" + self_temp_bin_name + "_2')")
        m.update()
    m.update()
    return m

def g_constr(node, m):
    bin_name = get_bin_name(node)
    create_new_vars = False
    if (not node.gurobi_vars) or create_new_vars:
        exec(bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+bin_name+"')")
        exec("node.add_gurobi_var("+bin_name+")")
        create_new_vars = True
    else:
        exec(bin_name+"=node.gurobi_vars[0]")
    child_bin_name = get_bin_name(node.child1)
    times = list(range(handle_no_range(node).range_start, handle_no_range(node).range_end+1))
    sum_bin_allTs = ""
    n = 0
    for t in times:
        temp_child_bin = child_bin_name+"_"+str(t)
        exec(temp_child_bin+"=m.addVar(vtype=GRB.BINARY, name='"+temp_child_bin+"')")
        exec("node.child1.add_gurobi_var("+temp_child_bin+")")
        sum_bin_allTs += temp_child_bin + "+"
        m.update()
        n += 1
    sum_bin_allTs = sum_bin_allTs[:-1]
    exec("m.addConstr("+ str(n) + "*" + bin_name + " <= " + sum_bin_allTs + ", 'c_" + bin_name + "_1')")
    exec("m.addConstr("+ sum_bin_allTs + " <= " + str(n-1) + " + " + bin_name + ", 'c_"+bin_name+"_2')")
    m.update()
    return m

def f_constr(node, m):
    bin_name = get_bin_name(node)
    create_new_vars = False
    if (not node.gurobi_vars) or create_new_vars:
        exec(bin_name+"=m.addVar(vtype=GRB.BINARY, name='"+bin_name+"')")
        exec("node.add_gurobi_var("+bin_name+")")
        create_new_vars = True
    else:
        exec(bin_name+"=node.gurobi_vars[0]")
    child_bin_name = get_bin_name(node.child1)
    times = list(range(handle_no_range(node).range_start, handle_no_range(node).range_end+1))
    sum_bin_allTs = ""
    n = 0
    for t in times:
        temp_child_bin = child_bin_name+"_"+str(t)
        exec(temp_child_bin+"=m.addVar(vtype=GRB.BINARY, name='"+temp_child_bin+"')")
        exec("node.child1.add_gurobi_var("+temp_child_bin+")")
        sum_bin_allTs += temp_child_bin + "+"
        m.update()
        n += 1
    sum_bin_allTs = sum_bin_allTs[:-1]
    exec("m.addConstr(" + bin_name + " <= " + sum_bin_allTs + ", 'c_" + bin_name + "_1')")
    exec("m.addConstr("+ sum_bin_allTs + " <= " + str(n) + " + " + bin_name + ", 'c_"+bin_name+"_2')")
    m.update()
    return m

def leq_constr(node, m):
    self_bin_name = get_bin_name(node)
    times = list(range(handle_no_range(node).range_start, handle_no_range(node).range_end+1))
    return m

def geq_constr(node, m):
    return m
