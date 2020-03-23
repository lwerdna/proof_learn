#!/usr/bin/env python

# Incredible Proof Machine's Hilbert System
# Lukasiewicz third system from the section admitting implication and negation:
# https://en.wikipedia.org/wiki/List_of_Hilbert_systems#Implicational_propositional_calculus

import sys

class node():
	pass

class impl(node):
	def __init__(self, l, r, n=False):
		self.left = l
		self.right = r
	def directions(self):
		result = ''
		result += 'L'+self.left.directions()+'U'
		result += 'R'+self.right.directions()+'U'
		return result
	def vars(self):
		return self.left.vars() + self.right.vars()
	def rename(self, mapping):
		self.left.rename(mapping)
		self.right.rename(mapping)
	def clone(self):
		return impl(self.left.clone(), self.right.clone())
	def __eq__(self, other):
		return type(other)==impl and self.left==other.left and self.right==other.right
	def __str__(self):
		return '(%s->%s)' % (self.left, self.right)

class var(node):
	def __init__(self, var_name):
		self.name = var_name
	def directions(self):
		return self.name
	def vars(self):
		return [self.name]
	def rename(self, mapping):
		self.name = mapping[self.name]
	def clone(self):
		return var(self.name)
	def __eq__(self, other):
		return type(other)==var and self.name == other.name
	def __str__(self):
		return self.name

def normalize(term):
	fount = iter('abcdefjhijklmnopqrstuvwxyz')
	mapping = {}
	for v in term.vars():
		if v in mapping: continue
		mapping[v] = next(fount)
	
	#print('mapping: %s' % mapping)
	term.rename(mapping)

def mp(implication, antecedent):
	stack = []

	# collect left side
	lookup = {}
	cur = antecedent
	#print('left directions: ', implication.left.directions())
	try:
		for d in implication.left.directions():
			if d == 'L':
				stack.append(cur)
				cur = cur.left
			elif d == 'R':
				stack.append(cur)
				cur = cur.right
			elif d == 'U':
				cur = stack.pop()
			else:
				if d in lookup:
					assert lookup[d] == cur
				else:
					lookup[d] = cur
	except Exception:
		return None

	#for (k,v) in lookup.items():
	#	print('%s: %s' % (k,v))

	# create right side
	i = 0
	stack.clear()
	#print('right directions: ', implication.right.directions())
	for d in implication.right.directions():
		if d == 'L':
			stack.append(impl(None,None))
		elif d == 'R':
			pass
		elif d == 'U':
			tmp = stack.pop()
			if stack[-1].left == None: stack[-1].left = tmp
			elif stack[-1].right == None: stack[-1].right = tmp
			else: assert False
		else:
			if d in lookup:
				stack.append(lookup[d].clone())
			else: # introduce a var
				varlist = antecedent.vars()
				varname = chr(max(map(ord, varlist))+1)
				stack.append(var(varname))

	assert len(stack) == 1
	result = stack[0]
	normalize(result)
	return result
