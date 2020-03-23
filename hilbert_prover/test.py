#!/usr/bin/env python

from engine import *

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

