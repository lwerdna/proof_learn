#!/usr/bin/env python

import re
import readline

from parser import parse_str
from engine import reducible, reduce_step

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

	variables['true'] = parse_str('\\x[\\y[x]]')
	variables['false'] = parse_str('\\x[\\y[y]]')
	variables['ite'] = parse_str('\\cond[\\a[\\b[((cond a) b)]]]')

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
			term = parse_str(rhs)
			info('assigning %s to %s' % (rhs, lhs))
			variables[lhs] = term
			continue

		# evaluate
		term = parse_str(line)
		term = load_vars(term)
		#print(term.str_tree())

		while 1:
			target = reducible(term)
			if not target: break
			#print('target is: %s' % target.str_line())

			print(term.str_tree(target)) 
			print('----')

			term = reduce_step(term, target)

		print(term.str_tree())

