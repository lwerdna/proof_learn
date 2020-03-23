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
# (/a->/b)->(b->a)
ax2 = impl(impl(neg(var('a')), neg(var('b'))), impl(var('b'), var('a')))

assert str(ax0) == '(a->(b->a))'
assert ax0.directions() == 'LaURLbURaUU'
assert ax0.lchild.directions() == 'a'

assert str(ax1) == '((a->(b->c))->((a->b)->(a->c)))'
assert ax1.directions() == 'LLaURLbURcUUURLLaURbUURLaURcUUU'
assert ax1.lchild.directions() == 'LaURLbURcUU'
assert ax1.rchild.directions() == 'LLaURbUURLaURcUU'
ax1.rename({'a':'z', 'b':'y', 'c':'x'})
assert str(ax1) == '((z->(y->x))->((z->y)->(z->x)))'
normalize(ax1)
assert str(ax1) == '((a->(b->c))->((a->b)->(a->c)))'

assert str(ax2) == '((/a->/b)->(b->a))'
assert str(mp(ax0, ax2)) == '(a->((/b->/c)->(c->b)))'
assert str(mp(ax1, ax2)) == '(((/a->/b)->b)->((/a->/b)->a))'

# test variable introduction
assert str(mp(ax0, ax0)) == '(a->(b->(c->b)))'
assert str(mp(ax0,mp(ax0, ax0))) == '(a->(b->(c->(d->c))))'
assert str(mp(ax0, mp(ax0, mp(ax0, ax0)))) == '(a->(b->(c->(d->(e->d)))))'

# ((a->(a->a))->((a->a)->(a->a)))
l = impl(impl(var('a'),impl(var('a'),var('a'))),impl(impl(var('a'),var('a')),impl(var('a'),var('a'))))
# ((a->(b->c))->((a->b)->(a->c)))
r = impl(impl(var('a'),impl(var('b'),var('c'))),impl(impl(var('a'),var('b')),impl(var('a'),var('c'))))
#mp(l, r)


