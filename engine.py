#!/usr/bin/env python
#
# interact with the lambda term to do reductions, etc.

import os
import copy
from node import ApplicationNode, AbstractionNode, VariableNode
from parser import parse_expr

macros = {}

DEBUG = False

def debug_set():
	global DEBUG
	DEBUG = True

def debug_clear():
	global DEBUG
	DEBUG = False

def get_all_nodes(tree):
	result = []
	queue = [tree]
	while queue:
		result += queue
		tmp = []
		for node in queue:
			tmp += node.children
		queue = tmp

	return result

# should be called MULTIPLE times: after parsing, and after B-reduction,
# since depths will change
def decorate(ast):
	curid = 0
	depth = 0
	queue = [ast]
	while queue:
		for node in queue:
			node.depth = depth
			node.id = curid
			curid += 1

		tmp = []
		for node in queue:
			tmp += node.children

		queue = tmp
		depth += 1

# have each AbstractionNode point to all its bound VariableNodes
# assumes the given ast has had its depths decorated
#
# should be called ONCE after parsing, depth decorating
# (the bindings shouldn't change even during B-reduction)
def decorate_bindings(ast):
	for anode in filter(lambda x: isinstance(x, AbstractionNode), get_all_nodes(ast)):
		for vnode in filter(lambda x: isinstance(x, VariableNode) and x.name==anode.var_name, anode.descendents()):
			vnode.binding = anode

def substitute_macros(ast):
	global macros
	result = ast
	for var in [x for x in get_all_nodes(ast) if isinstance(x, VariableNode)]:
		if var.name in macros:
			new = copy.deepcopy(macros[var.name])
			if not var.parent:
				result = new
			else:
				var.parent.update_children(var, new)
				new.parent = var.parent
	return result

def to_tree(expr:str):
	ast = parse_expr(expr)
	#print(ast.str_tree())
	decorate(ast)
	decorate_bindings(ast)
	ast = substitute_macros(ast)
	decorate(ast)
	return ast

# note: macros are NOT lexical, they're tree replacements that happen after parsing and binding
def assign_macro(name:str, expr:str):
	global macros
	macros[name] = to_tree(expr)
	#print('assigned %s to:' % name)
	#print(macros[name].str_tree())

# if reducible -> return the ApplicationNode that will be the target of the next reduce step
#         else -> return None
def reducible(term):
	assert not term is None
	nodes = get_all_nodes(term)
	nodes = [x for x in nodes if isinstance(x, ApplicationNode) and isinstance(x.children[0], AbstractionNode)]
	if not nodes: return None
	nodes = sorted(nodes, key=lambda x: x.depth, reverse=True)
	return nodes[0]

# reduce a term, single-step style
def reduce_step(term, target=None):
	if not target:
		target = reducible(term)
	if not target:
		return term

	# substitute all variables bound by abst in body with val:
	#
	#    appl
	#    /  \
	#  abst  val
	#   |
	#  body
	#
	appl = target
	val = appl.children[1] 
	abst = appl.children[0]
	body = abst.children[0]

	#assert not (abst is val)
	#print('appl: %s' % appl)
	#print('val: %s' % val)
	#print('abst: %s' % abst)
	#print('body: %s' % body)
	#assert not (body is val)

	assert isinstance(appl, ApplicationNode)
	assert isinstance(abst, AbstractionNode)

	# replace all bound variables
	#print('changing bindings: ', abst.bindings)
	#print('changing bindings: ', list(map(str, abst.bindings)))
	for var in filter(lambda x: isinstance(x, VariableNode) and x.binding is abst, abst.descendents()):
		var.parent.update_children(var, copy.deepcopy(val))

	body = abst.children[0] # important! body could have been a replaced variable

	# replace link to appl with links to body
	if not appl.parent:
		result = body
		body.parent = None
	else:
		appl.parent.update_children(appl, body)
		body.parent = appl.parent
		result = term

	# depths have changed, update
	decorate(result)
	return result

def reduce_(term:str, target=None):
	term = to_tree(term)

	if not target:
		target = reducible(term)

	while target:
		if DEBUG: print(term.str_tree(target))
		term = reduce_step(term, target)
		if DEBUG: print('----')
		target = reducible(term)

	if DEBUG:
		print(term.str_tree())

	return term

def equals(a, b):
	if type(a) == str:
		a = to_tree(a)
	if type(b) == str:
		b = to_tree(b)
	return a == b

def draw_graphviz(term:str, fname=None):
	term = to_tree(term)

	dot = 'digraph g {\n'
	
	def node2mark(node):
		if isinstance(node, VariableNode): return node.name
		elif isinstance(node, AbstractionNode): return '&lambda;.%s' % node.var_name
		else: return '@'

	nodes = get_all_nodes(term)

	# labels
	for node in nodes:
		dot += '\t"obj_%d" [ label = "%s" ];\n' % (id(node), node2mark(node))

	# parent-child edges
	for node in nodes:
		src = 'obj_%d' % id(node)
		for child in node.children:
			dst = 'obj_%d' % id(child)
			dot += '\t"%s" -> "%s";\n' % (src, dst)

	# variable -> abstraction bindings
	for node in filter(lambda x: isinstance(x, VariableNode) and x.binding, nodes):
		src = 'obj_%d' % id(node)
		dst = 'obj_%d' % id(node.binding)
		dot += '%s -> %s [style=dashed, color=grey]' % (src, dst)

	dot += '}\n'

	with open('/tmp/tmp.dot', 'w') as fp:
		fp.write(dot)

	if not fname:
		fname = '/tmp/tmp.png'
	os.system('dot /tmp/tmp.dot -Tpng -o' + fname)
	os.system('open /tmp/tmp.png')

	
