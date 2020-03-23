#!/usr/bin/env python

# Incredible Proof Machine's Hilbert System
# Lukasiewicz third system from the section admitting implication and negation:
# https://en.wikipedia.org/wiki/List_of_Hilbert_systems#Implicational_propositional_calculus

import sys

class node():
	pass

class impl(node):
	def __init__(self, l, r, n=False):
		self.lchild = l
		self.rchild = r
	def directions(self):
		result = 'L'+self.lchild.directions()+'U'
		result += 'R'+self.rchild.directions()+'U'
		return result
	def vars(self):
		return self.lchild.vars() + self.rchild.vars()
	def rename(self, mapping):
		self.lchild.rename(mapping)
		self.rchild.rename(mapping)
	def clone(self):
		return impl(self.lchild.clone(), self.rchild.clone())
	def __eq__(self, other):
		return type(other)==impl and self.lchild==other.lchild and self.rchild==other.rchild
	def __str__(self):
		return '(%s->%s)' % (self.lchild, self.rchild)

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

class neg(node):
	def __init__(self, child):
		self.child = child
	def directions(self):
		return 'D'
	def vars(self):
		return self.child.vars()
	def rename(self, mapping):
		self.child.rename(mapping)
	def clone(self):
		return neg(self.child.clone())
	def __eq__(self, other):
		return type(other)==neg and self.child==other.child
	def __str__(self):
		return '/%s' % self.child

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
	#print('left directions: ', implication.lchild.directions())
	try:
		for d in implication.lchild.directions():
			if d == 'L':
				stack.append(cur)
				cur = cur.lchild
			elif d == 'R':
				stack.append(cur)
				cur = cur.rchild
			elif d == 'D':
				stack.append(cur)
				cur = cur.child
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
	#print('right directions: ', implication.rchild.directions())
	for d in implication.rchild.directions():
		if d == 'L':
			stack.append(impl(None,None))
		elif d == 'R':
			pass
		elif d == 'U':
			tmp = stack.pop()
			if stack[-1].lchild == None: stack[-1].lchild = tmp
			elif stack[-1].rchild == None: stack[-1].rchild = tmp
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
