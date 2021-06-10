# this is a [recursive descent parser](https://en.wikipedia.org/wiki/Recursive_descent_parser)
# for the following grammar:
#
# term --> var
#      --> \var[term]
#      --> (var var)
#
# I think this is LL(0) since I only need the current symbol to determine which
# production rule to follow next

from lexer import TID, tokenize
from node import AbstractionNode, ApplicationNode, VariableNode

class ParserException(Exception):
	pass

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
		raise ParserException('error at: %s' % type_cur)

def parse_variable(mgr):
	#print('parse_variable(...\'%s\')' % mgr.str_line())

	(tok_type, var_name) = mgr.shift(TID.VARIABLE)
	return VariableNode(var_name)

def parse_abstraction(mgr):
	#print('parse_abstraction(...\'%s\')' % mgr.str_line())

	mgr.shift(TID.LAMBDA)
	(tok_type, var_name) = mgr.shift(TID.VARIABLE)
	mgr.shift(TID.LBRACK)
	body = parse_term(mgr)
	mgr.shift(TID.RBRACK)
	abst = AbstractionNode(var_name, body)
	body.parent = abst
	return abst

def parse_application(mgr):
	#print('parse_application(...\'%s\')' % mgr.str_line())

	mgr.shift(TID.LPAREN)
	left = parse_term(mgr)
	right = parse_term(mgr)
	mgr.shift(TID.RPAREN)
	app = ApplicationNode(left, right)
	left.parent = app
	right.parent = app
	return app

def parse(mgr):
	tree = parse_term(mgr)
	if not mgr.is_end():
		raise ParserException("parse is done, but tokens remain %s...", mgr.peek())
	return tree

def parse_expr(expr:str):
	mgr = tokenize(expr)
	tree = parse(mgr)
	return tree
