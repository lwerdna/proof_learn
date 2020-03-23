#!/usr/bin/env python

from engine import *

# these axioms are from:
# - Incredible Proof Machine's Hilbert System
# - Lukasiewicz third system from the section admitting implication and negation
# -- https://en.wikipedia.org/wiki/List_of_Hilbert_systems#Implicational_propositional_calculus)
# -- On axiom systems of propositional calculi, I, Proceedings of the Japan Academy. Volume 41, Number 6 (1965), 436–439.

# (a->(b->a))
ax0 = impl(var('a'),impl(var('b'),var('a')))
# ((a->(b->c))->((a->b)->(a->c)))
ax1 = impl(impl(var('a'),impl(var('b'),var('c'))),impl(impl(var('a'),var('b')),impl(var('a'),var('c'))))
# (/a->/b)->(b->a)
# ax2 = TODO

# prove (a->a)
ax2 = mp(ax1, ax0) # ((a->b)->(a->a))
ax3 = mp(ax2, ax0) # (a->a)
assert str(ax3) == '(a->a)'

# prove ((a->b)->((c->a)->(c->b))) (hypothetical syllogism)
ax2 = mp(ax0, ax0) # (a->(b->(c->b)))
ax3 = mp(ax0, ax1) # (a->((b->(c->d))->((b->c)->(b->d))))
ax4 = mp(ax1, ax0) # ((a->b)->(a->a))
ax5 = mp(ax1, ax2) # ((a->b)->(a->(c->b)))
ax6 = mp(ax1, ax3) # ((a->(b->(c->d)))->(a->((b->c)->(b->d))))
ax7 = mp(ax4, ax4) # ((a->b)->(a->b))
ax8 = mp(ax5, ax7) # ((a->b)->(c->(a->b)))
ax9 = mp(ax6, ax8) # ((a->b)->((c->a)->(c->b)))
assert str(ax9) == '((a->b)->((c->a)->(c->b)))'

