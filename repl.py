#!/usr/bin/env python

import re
import readline

from engine import reducible, reduce_step, to_tree, assign_macro

RED = '\x1B[31m'
GREEN = '\x1B[32m'
NORMAL = '\x1B[0m'

variables = {}

def info(msg):
	print(GREEN + msg + NORMAL)

def load_vars(term):
	global variables
	for (vname, subterm) in variables.items():
		term = term.var_subst(vname, subterm)
	return term

if __name__ == '__main__':
	assign_macro('TRUE', '\\x[\\y[x]]')
	assign_macro('FALSE', '\\x[\\y[y]]')
	assign_macro('ITE', '\\cond[\\a[\\b[((cond a) b)]]]')

	while 1:
		try:
			line = input('lshell> ')
			line = line.rstrip()
		except EOFError:
			break

		if line == 'q': break
		if line == '': continue
		if line.startswith('!comment'): continue

		# assignment
		m = re.match(r'^(\w+) ?= ?(.*)', line)
		if m:
			(lhs, rhs) = m.group(1, 2)
			assign_macro(lhs, rhs)
			continue

		# evaluate
		term = to_tree(line)
		print(term.str_tree())
#		while 1:
#			#print('target is: %s' % target.str_line())
#
#			print(term.str_tree(target)) 
#			print('----')
#
#			term = reduce_step(term, target)
#
#		print(term.str_tree())

