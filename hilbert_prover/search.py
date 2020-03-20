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

def test():
	# basic tree properties
	l = impl(impl(var('a'),impl(var('a'),var('a'))),impl(impl(var('a'),var('a')),impl(var('a'),var('a'))))
	r = impl(impl(var('a'),impl(var('a'),var('a'))),impl(impl(var('a'),var('a')),impl(var('a'),var('a'))))
	assert l == r
	r = impl(impl(var('a'),impl(var('a'),var('b'))),impl(impl(var('a'),var('a')),impl(var('a'),var('a'))))
	assert l != r
	r = impl(impl(var('a'),impl(var('a'),var('b'))),impl(var('a'),var('a')),impl(var('a'),var('a')))
	assert l != r

	# normalizing
	l = impl(var('c'), impl(var('a'), var('a')))
	assert str(l) == '(c->(a->a))'
	normalize(l)
	assert str(l) == '(a->(b->b))'

	# capture tests
	l = impl(impl(var('a'), var('b')), var('z'))
	r = impl(var('x'), var('y'))
	# (a->b)->z matches (x,y) with {a:x, b:y} then gets mapped to z then normalizes to a
	assert mp(l, r) == var('a')	

	# (a->a)->z NO MATCH (x,y)
	l = impl(impl(var('a'), var('a')), var('z'))
	assert mp(l, r) == None

	# axioms
	# (a->(b->a))
	ax0 = impl(var('a'),impl(var('b'),var('a')))
	# ((a->(b->c))->((a->b)->(a->c)))
	ax1 = impl(impl(var('a'),impl(var('b'),var('c'))),impl(impl(var('a'),var('b')),impl(var('a'),var('c'))))

	assert str(ax0) == '(a->(b->a))'
	assert ax0.directions() == 'LaURLbURaUU'
	assert ax0.left.directions() == 'a'

	assert str(ax1) == '((a->(b->c))->((a->b)->(a->c)))'
	assert ax1.directions() == 'LLaURLbURcUUURLLaURbUURLaURcUUU'
	assert ax1.left.directions() == 'LaURLbURcUU'
	ax1.rename({'a':'z', 'b':'y', 'c':'x'})
	assert str(ax1) == '((z->(y->x))->((z->y)->(z->x)))'
	normalize(ax1)
	assert str(ax1) == '((a->(b->c))->((a->b)->(a->c)))'

	# test variable introduction
	assert str(mp(ax0, ax0)) == '(a->(b->(c->b)))'
	assert str(mp(ax0,mp(ax0, ax0))) == '(a->(b->(c->(d->c))))'
	assert str(mp(ax0, mp(ax0, mp(ax0, ax0)))) == '(a->(b->(c->(d->(e->d)))))'

	# ((a->(a->a))->((a->a)->(a->a)))
	l = impl(impl(var('a'),impl(var('a'),var('a'))),impl(impl(var('a'),var('a')),impl(var('a'),var('a'))))
	# ((a->(b->c))->((a->b)->(a->c)))
	r = impl(impl(var('a'),impl(var('b'),var('c'))),impl(impl(var('a'),var('b')),impl(var('a'),var('c'))))
	#mp(l, r)

	# prove (a->a)
	ax2 = mp(ax1, ax0)					# ((a->b)->(a->a))
	ax3 = mp(ax2, ax0)					# (a->a)
	assert str(ax3) == '(a->a)'

test()
#sys.exit(-1)

# search

# set initial axioms
ax0 = impl(var('a'),impl(var('b'),var('a')))
ax1 = impl(impl(var('a'),impl(var('b'),var('c'))),impl(impl(var('a'),var('b')),impl(var('a'),var('c'))))
gamma = [ax0, ax1]

seen = set(map(str, gamma))
for (i,axiom) in enumerate(gamma):
	seen.add(str(axiom))
	print('%d: %s' % (i, axiom))
print('----')

frontier = 0
while len(gamma) < 100:
	batch = []

	for i in range(len(gamma)):
		for j in range(frontier, len(gamma)):
			pairs = ((i,j),) if i==j else ((i,j),(j,i))

			for (l,r) in pairs:
				#print('attempting mp() on:')
				#print('   impl: %s' % gamma[l])
				#print('   ante: %s' % gamma[r])
				c = mp(gamma[l], gamma[r])

				if c == None:
					#print('mp(%d,%d) failed' % (l,r))
					continue

				s = str(c)
				if s in seen:
					#print('mp(%d,%d) we have seen before' % (l,r))
					continue

				print('%d: %s mp(%d,%d)' % (len(gamma)+len(batch), s, l, r))
				seen.add(s)
				batch.append(c)

	print('----')
	frontier = len(gamma)
	gamma.extend(batch)

