#!/usr/bin/env python

from engine import *

# set initial axioms
ax0 = impl(var('a'),impl(var('b'),var('a')))
ax1 = impl(impl(var('a'),impl(var('b'),var('c'))),impl(impl(var('a'),var('b')),impl(var('a'),var('c'))))
ax2 = impl(impl(neg(var('a')), neg(var('b'))), impl(var('b'), var('a')))
gamma = [ax0, ax1, ax2]

seen = set(map(str, gamma))
for (i,axiom) in enumerate(gamma):
	seen.add(str(axiom))
	print('%d: %s' % (i, axiom))
print('----')

depth = 0
frontier = 0
while depth < 5:
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

				print('%d = mp(%d,%d) # %s' % (len(gamma)+len(batch), l, r, s))
				seen.add(s)
				batch.append(c)

	print('----')
	frontier = len(gamma)
	gamma.extend(batch)
	depth += 1

