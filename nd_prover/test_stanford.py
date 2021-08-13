#!/usr/bin/env python

from stanford_fitch import *

# http://logic.stanford.edu/intrologic/exercises/exercise_04_01.html
# given p, q, (p^q => r) prove r
tree = \
    ImplicationElimination(
        Assumption('(P&Q)=>R'),
        AndIntroduction(
            Assumption('P'),
            Assumption('Q')
        ),
    )
print(tree.str_tree())
assert tree.check_deduction('R')

print('--------')

# http://logic.stanford.edu/intrologic/exercises/exercise_04_02.html
# given (p ^ q) prove (q v r)
tree = \
    OrIntroduction( # Q v R
        AndElimination( # Q
            Assumption('(P&Q)'),
            'right'
        ),
        'R'
    )
print(tree.str_tree())
assert tree.check_deduction('(Q | R)')

print('--------')

# http://logic.stanford.edu/intrologic/exercises/exercise_04_03.html
# Given p => q and q <=> r, use the Fitch system to prove p => r
tree = \
    ImplicationIntroduction(
        ImplicationElimination( # R
            BiImplicationElimination( # Q => R
                Assumption('Q <=> R', label='premise2'),
            ),
            ImplicationElimination( # Q
                Assumption('P => Q', label='premise1'),
                Assumption('P', label="assumption1")
            )
        ),
        discharge='assumption1'
    )
print(tree.str_tree())
assert tree.check_deduction('(P => R)')

print('--------')

# http://logic.stanford.edu/intrologic/exercises/exercise_04_04.html
# Given p => q and m => p ∨ q, use the Fitch System to prove m => q
tree = \
    ImplicationIntroduction( # M
        OrElimination( # Q
            ImplicationElimination( # P v Q
                Assumption('M => (P | Q)', label='premise2'),
                Assumption('M', label='assumption1')
            ),

            Assumption('P => Q', label='premise1'),

            ImplicationIntroduction( # Q => Q
                Assumption('Q', label='assumption2'),
                discharge='assumption2'
            )
        ),
        discharge='assumption1'
    )
print(tree.str_tree())
assert tree.check_deduction('(M => Q)')

print('--------')

# http://logic.stanford.edu/intrologic/exercises/exercise_04_05.html
# Given p => (q => r), use the Fitch System to prove (p => q) => (p => r).
tree = \
        ImplicationIntroduction(
            ImplicationIntroduction( # P => R
                ImplicationElimination( # R
                    ImplicationElimination( # Q => R
                    	Assumption('P => (Q => R)'),
                    	Assumption('P', label='1')
                    ),
                    ImplicationElimination( # Q
                        Assumption('P => Q', label='2'),
                        Assumption('P', label='1')
                    )
                ),
                discharge='1'
            ),
            discharge='2'
        )
print(tree.str_tree())
assert tree.check_deduction('(P => Q) => (P => R)')
