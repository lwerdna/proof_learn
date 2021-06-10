#!/usr/bin/env python

import os
import re
import readline

import engine
from engine import load_stdlib, reduce_step, to_tree, assign_macro, reducible
from engine import VariableNode, AbstractionNode, ApplicationNode
from parser import ParserException

single_step = True # evaluate and print one reduction step at a time
single_step_max = 32 # None or 0 means no limit, else stop after
auto_reduce = True # automatically attempt reduction on entered expressions
draw_enabled = True

RED = '\x1B[31m'
GREEN = '\x1B[32m'
NORMAL = '\x1B[0m'

def info(msg):
	print(GREEN + msg + NORMAL)

def error(msg):
	print(RED + msg + NORMAL)

def draw_graphviz(term, hlnode=None, fname=None):
	if type(term) == str:
		term = to_tree(term)

	#print('gonna draw: ')
	#print(term.str_tree())

	dot = 'digraph g {\n'
	dot += '\tgraph [ordering="out"];'

	def node2mark(node):
		if isinstance(node, VariableNode): return '%s' % (node.name)
		elif isinstance(node, AbstractionNode): return '&lambda;.%s' % node.var_name
		else: return '@'

	nodes = engine.get_all_nodes(term)

	# labels
	for node in nodes:
		color = ' fillcolor="red" style="filled"' if node is hlnode else ''
		shape = ' shape="box"' if isinstance(node, VariableNode) else ''
		dot += '\t"obj_%d" [ label = "%s"%s%s];\n' % (id(node), node2mark(node), shape, color)

	# parent -> child edges
	for node in nodes:
		src = 'obj_%d' % id(node)
		for child in node.children:
			dst = 'obj_%d' % id(child)
			dot += '\t"%s" -> "%s";\n' % (src, dst)

	# child -> parent edges
	#for node in nodes:
	#	if not node.parent: continue
	#	src = 'obj_%d' % id(node)
	#	dst = 'obj_%d' % id(node.parent)
	#	dot += '\t"%s" -> "%s" [color="red"];\n' % (src, dst)

	# variable -> abstraction bindings
	for node in filter(lambda x: isinstance(x, VariableNode) and x.binding, nodes):
		src = 'obj_%d' % id(node)
		dst = 'obj_%d' % id(node.binding)
		dot += '\t"%s" -> "%s" [style=dashed, color="grey"]' % (src, dst)

	dot += '}\n'

	with open('/tmp/tmp.dot', 'w') as fp:
		fp.write(dot)

	if not fname:
		fname = '/tmp/tmp.png'
	print('writing %s' % fname)
	os.system('dot /tmp/tmp.dot -Tpng -o' + fname)
	os.system('convert ' + fname + ' -resize 50% ' + fname)

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
			if line == '.ss':
				single_step = not single_step
				info('changed single step to: %s' % single_step)
				continue
			if line.startswith('.ssmax '):
				single_step_max = int(line[7:])
				info('changed single step max to: %d' % single_step_max)
				continue
			if line == '.draw':
				draw_enabled = not draw_enabled
				info('changed draw_enabled to: %s' % draw_enabled)
				continue
			if line == '.macros':
				for (name, val) in engine.macros.items():
					print('%s: %s' % (name, str(val)))
				continue
			if line == '.settings':
				info('automatic reduction: %s' % auto_reduce)
				info(' reduction strategy: %s (change with .normal, .applicative)' % engine.reduction_strategy)
				info('    single step max: %s (change with .ssmax <num>)' % single_step_max)
				info('        single step: %s (change with .ss)' % single_step)
				info('       draw enabled: %s (change with .draw)' % draw_enabled)
				continue

			# evaluate
			term = to_tree(line)
			if auto_reduce:
				if single_step:
					print('0: %s' % str(term))
					if draw_enabled: draw_graphviz(term, reducible(term), '/tmp/step_0000.png')
					step = 1
					while 1:
						term = reduce_step(term)
						if draw_enabled: draw_graphviz(term, reducible(term), '/tmp/step_%04d.png' % step)
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

