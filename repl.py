#!/usr/bin/env python

import os
import re
import readline

import engine
from engine import load_stdlib, reduce_step, to_tree, assign_macro, draw_graphviz, reducible
from parser import ParserException

single_step = True # evaluate and print one reduction step at a time
single_step_max = 999 # None or 0 means no limit, else stop after
auto_reduce = True # automatically attempt reduction on entered expressions
output_type = 'line' # or 'tree' or 'graphviz'
sstep_limit = 100

RED = '\x1B[31m'
GREEN = '\x1B[32m'
NORMAL = '\x1B[0m'

def info(msg):
	print(GREEN + msg + NORMAL)

def error(msg):
	print(RED + msg + NORMAL)

if __name__ == '__main__':
	load_stdlib()

	while 1:
		try:
			line = input('lshell> ')
			line = line.rstrip()

			if line == 'q': break
			if line == '': continue
			if line.startswith('!comment'): continue

			# assignment
			m = re.match(r'^(\w+) ?= ?(.*)', line)
			if m:
				(lhs, rhs) = m.group(1, 2)
				assign_macro(lhs, rhs)
				info('assigned macro %s' % lhs)
				continue

			# draw
			if line[0:5] in ['draw ', 'DRAW ']:
				term = to_tree(line[5:])
				print(term.str_tree())
				target = reducible(term)
				draw_graphviz(term, target)
				os.system('open /tmp/tmp.png')
				continue

			if line[0:8] == 'reduce1 ':
				term = to_tree(line[8:])
				term = reduce_step(term)
				print(term.str_tree())
				print(str(term))
				continue

			# internal settings
			if line == '.normal':
				engine.reduction_strategy = 'normal'
				info('changed evaluation strategy to normal (left-most, outer-most redex first)')
				continue
			if line == '.applicative':
				engine.reduction_strategy = 'applicative'
				info('changed evaluation strategy to applicative (deepest, most-nested redex first)')
				continue
			if line.startswith('.ssmax '):
				single_step_max = int(line[7:])
				info('changed single step max to: %d' % single_step_max)
				continue
			if line == '.settings':
				info('automatic reduction: %s' % auto_reduce)
				info(' reduction strategy: %s (change with .normal, .applicative)' % engine.reduction_strategy)
				info('    single step max: %s (change with .ssmax <num>)' % single_step_max)
				info('        single step: %s' % single_step)
				continue

			# evaluate
			term = to_tree(line)
			if auto_reduce:
				if single_step:
					step = 1
					while 1:
						term = reduce_step(term)
						print('%d: %s' % (step, str(term)))
						step += 1
						if step > single_step_max: break
						if not reducible(term): break
				else:
					term = reduce_(term)

#		while 1:
#			#print('target is: %s' % target.str_line())
#
#			print(term.str_tree(target))
#			print('----')
#
#			term = reduce_step(term, target)
#
#		print(term.str_tree())

		except EOFError:
			break
		except ParserException as e:
			error(str(e))

