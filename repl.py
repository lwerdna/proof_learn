#!/usr/bin/env python

import re
import os
import sys
import copy
from enum import Enum, auto

import readline

RED = '\x1B[31m'
GREEN = '\x1B[32m'
NORMAL = '\x1B[0m'

def info(msg):
	print(GREEN + msg + NORMAL)

###############################################################################
# TOKENIZING STUFF
###############################################################################
class TID(Enum):
	LAMBDA = auto()
	VARIABLE = auto()
	DOT = auto()
	LPAREN = auto()
	RPAREN = auto()
	LBRACK = auto()
	RBRACK = auto()

# a token is a tuple (TID, <val>) if value applies

class TokenManager:
	def __init__(self, tokenList):
		self.tokenList = tokenList
		self.i = 0

	def reset(self):
		self.i = 0

	def peek(self, nAhead=0):
		if (self.i + nAhead) >= len(self.tokenList):
			return None
		return self.tokenList[self.i + nAhead]

	def shift(self, tid_expected=None):
		if self.is_end():
			raise Exception("token list is empty")

		(tok_id, tok_val) = self.tokenList[self.i]
		self.i += 1

		if tid_expected != None and tid_expected != tok_id:
			raise Exception("expected token %s but got instead %s" % (tid_expected.name, tok_val))

		return (tok_id, tok_val)

	def is_end(self):
		return self.peek() == None

	def __str__(self):
		result = []
		for k in range(self.i, len(self.tokenList)):
			(tok_type, tok_val) = self.tokenList[k]
			result.append("%d: %s '%s'" % (k, tok_type.name, tok_val))
		return "\n".join(result)

	def str_line(self):
		return ' '.join([x[1] for x in self.tokenList[self.i:]])

def tokenize(line):
	tokens = []
	line = line.rstrip()
	chars = list(line)

	i = 0
	while i < len(chars):
		c = chars[i]
		if c == '\\':
			tokens.append((TID.LAMBDA,'\\'))
			i += 1
		elif c.isspace():
			while i<len(chars) and chars[i].isspace():
				i += 1
		elif c == '.':
			tokens.append((TID.DOT, '.'))
			i += 1
		elif c.islower():
			value = ''
			while i<len(chars) and chars[i].isalpha():
				value += chars[i]
				i += 1
			tokens.append((TID.VARIABLE, value))
		elif c == '(':
			tokens.append((TID.LPAREN, '('))
			i += 1
		elif c == ')':
			tokens.append((TID.RPAREN, ')'))
			i += 1
		elif c == '[':
			tokens.append((TID.LBRACK, '['))
			i += 1
		elif c == ']':
			tokens.append((TID.RBRACK, ']'))
			i += 1
		else:
			raise Exception("tokenizing on \"%s...\"" % chars[i:i+8])

	return TokenManager(tokens)

###############################################################################
# PARSING
###############################################################################

class Term:
	def __init__(self):
		self.children = []
		pass

	# VariableNode overrides this one, substituting itself
	def var_subst(self, name, term):
		for i in range(len(self.children)):
			self.children[i] = self.children[i].var_subst(name, term)
		return self

	# Application overrides this one, drawing attention to itself
	def get_deepest_application_candidate(self, depth=0):
		(record_depth, record_node) = (None, None)

		if len(self.children) > 0:
			(foo, bar) = self.children[0].get_deepest_application_candidate(depth+1)
			if bar:
				(record_depth, record_node) = (foo, bar)

		if len(self.children) > 1:
			(foo, bar) = self.children[1].get_deepest_application_candidate(depth+1)
			if bar and foo > record_depth:
				(record_depth, record_node) = (foo, bar)

		return (record_depth, record_node)

	# Application overrides this one, carrying out the application operation
	def apply(self):
		pass

	#
	def reduce_one(self, one):
		if len(self.children) > 0 and self.children[0] == one:
			self.children[0] = self.children[0].apply()
			return True

		if len(self.children) > 1 and self.children[1] == one:
			self.children[1] = self.children[1].apply()
			return True

		if len(self.children) > 0:
			tmp = self.children[0].reduce_one(one)
			if tmp: return True

		if len(self.children) > 1:
			tmp = self.children[1].reduce_one(one)
			if tmp: return True

		return False

class VariableNode(Term):
	def __init__(self, name):
		super().__init__()
		self.name = name

	def var_subst(self, name, term):
		if self.name == name:
			return copy.deepcopy(term)
		return self

	def str_line(self):
		return self.name

	def str_tree(self, node_hl=None, depth=0):
		indent = '  ' * depth
		mark = ' <--' if self==node_hl else ''
		return '%sVariable "%s"%s' % (indent, self.name, mark)

class AbstractionNode(Term):
	def __init__(self, var_name, term):
		self.var_name = var_name
		self.children = [term]

	def str_line(self):
		return '\\%s[%s]' % (self.var_name, self.children[0].str_line())

	def str_tree(self, node_hl=None, depth=0):
		indent = '  ' * depth
		mark = ' <--' if self==node_hl else ''
		result = '%sAbstraction %s%s\n' % (indent, self.var_name, mark)
		result += self.children[0].str_tree(node_hl, depth+1)
		return result

class ApplicationNode(Term):
	def __init__(self, left, right):
		self.children = [left, right]

	def get_deepest_application_candidate(self, depth=0):
		# any candidates deeper than us automatically win
		(record_depth, record_node) = super().get_deepest_application_candidate(depth)
		if record_node:
			return (record_depth, record_node)

		# we're a candidate if our left child is an abstraction
		if isinstance(self.children[0], AbstractionNode):
			return (depth, self)

		# dead-end
		return (None, None)

	def apply(self):
		abstraction = self.children[0]
		argument = self.children[1]

		varname = abstraction.var_name
		body = abstraction.children[0]

		return body.var_subst(varname, argument)

	def str_line(self):
		return '(%s %s)' % (self.children[0].str_line(), self.children[1].str_line())

	def str_tree(self, node_hl=None, depth=0):
		indent = '  ' * depth
		mark = ' <--' if self==node_hl else ''
		result = '%sApplication%s\n' % (indent, mark)
		result += self.children[0].str_tree(node_hl, depth+1)
		result += '\n'
		result += self.children[1].str_tree(node_hl, depth+1)
		return result

#------------------------------------------------------------------------------

# term --> var
#      --> \var[term]
#      --> (var var)

# I think this is LL(0) since I only need the current symbol to determine which
# production to follow next. Here's a recursive descent parser:

def parse_term(mgr):
	#print('parse_term(...\'%s\')' % mgr.str_line())

	type_cur = mgr.peek()[0]

	if type_cur == TID.LAMBDA:
		return parse_abstraction(mgr)
	elif type_cur == TID.VARIABLE:
		return parse_variable(mgr)
	elif type_cur == TID.LPAREN:
		return parse_application(mgr)
	else:
		raise Exception('error at: %s' % type_cur)

def parse_abstraction(mgr):
	#print('parse_abstraction(...\'%s\')' % mgr.str_line())

	mgr.shift(TID.LAMBDA)
	(tok_type, var_name) = mgr.shift(TID.VARIABLE)
	mgr.shift(TID.LBRACK)
	body = parse_term(mgr)
	mgr.shift(TID.RBRACK)
	return AbstractionNode(var_name, body)

def parse_variable(mgr):
	#print('parse_variable(...\'%s\')' % mgr.str_line())

	(tok_type, var_name) = mgr.shift(TID.VARIABLE)
	return VariableNode(var_name)

def parse_application(mgr):
	#print('parse_application(...\'%s\')' % mgr.str_line())

	mgr.shift(TID.LPAREN)
	left = parse_term(mgr)
	right = parse_term(mgr)
	mgr.shift(TID.RPAREN)
	return ApplicationNode(left, right)

def parse_toks(mgr):
	tree = parse_term(mgr)
	if not mgr.is_end():
		raise Exception("parse is done, but tokens remain %s...", mgr.peek())
	return tree

def parse(expression):
	mgr = tokenize(expression)
	ast = parse_toks(mgr)
	return ast

###############################################################################
# UTILITIES
###############################################################################

def var_subst_var(term, var_name, subterm):
	return term.var_subst(var_name, subterm)

def var_subst_vars(term, var_dict):
	for (var_name, subterm) in var_dict.items():
		print('substituting %s for %s' % (var_name, subterm.str_line()))
		term = term.var_subst(var_name, subterm)

	return term

def evaluate(line, var_dict):
	term = parse(line)
	#print('tree: ', term.str_tree())
	term = var_subst_vars(term, var_dict)
	#print('tree: ', term.str_tree())
	return term

def lambda_reduce(node):
	step = 0
	while 1:
		print('---- reduction step %d ----' % step)
		(depth, target) = node.get_deepest_application_candidate()
		if target == None:
			print('no application candidates')
			break

		print(node.str_tree(target))

		if depth == 0:
			node = node.apply()
		else:
			node.reduce_one(target)

		step += 1

	return node

###############################################################################
# MAIN
###############################################################################
if __name__ == '__main__':
	variables = {}

	variables['true'] = parse('\\x[\\y[x]]')
	variables['false'] = parse('\\x[\\y[y]]')
	variables['ite'] = parse('\\cond[\\a[\\b[((cond a) b)]]]')

	while 1:
		try:
			line = input('lshell> ')
		except EOFError:
			break

		line = line.rstrip()

		if line == '':
			continue

		if line.startswith('!comment'):
			continue

		m = re.match(r'^(\w+) ?= ?(.*)', line)
		if m:
			(lhs, rhs) = m.group(1, 2)
			ast = parse(rhs)
			info('assigning to: %s' % lhs)
			variables[lhs] = ast
			continue

		m = re.match(r'^!tree (.*)', line)
		if m:
			rhs = m.group(1)
			ast = parse(rhs)
			print(ast.str_tree())
			continue

		if line == 'q':
			break

		term = evaluate(line, variables)
		print(term.str_tree())
		term = lambda_reduce(term)
		print(term.str_tree())

