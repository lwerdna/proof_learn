#!/usr/bin/env python

import sys
import copy
from node import ApplicationNode, AbstractionNode, VariableNode
from parser import parse_expr as ps
from engine import reduce_, equals, assign_macro, debug_set, draw_graphviz, to_tree, clone_tree

#debug_set()
#reduce_('\\x[(\\y[y] x)]')
#sys.exit(0)

# alpha equivalence
assign_macro('TRUE', '\\x[\\y[x]]')
assign_macro('FALSE', '\\x[\\y[y]]')

assert equals('TRUE', '\\foo[\\bar[foo]]')
assert equals('FALSE', '\\foo[\\bar[bar]]')

# do true/false work
assert equals(reduce_('((TRUE a) b)'), 'a')
assert equals(reduce_('((FALSE a) b)'), 'b')
#assert equals(reduce_('((TRUE FALSE) FALSE)'), 'FALSE')

assign_macro('ITE', '\\cond[\\a[\\b[((cond a) b)]]]')
assert equals(reduce_('(ITE FALSE)'), 'FALSE')
assert equals(reduce_('(ITE TRUE)'), 'TRUE')

# K combinator from SKI returns a function that always returns the given argument
assign_macro('K', '\\x[\\y[x]]')
assign_macro('RET_TRUE', '(K TRUE)')
assign_macro('RET_FALSE', '(K FALSE)')
assert equals(reduce_('(RET_TRUE FALSE)'), 'TRUE')
assert equals(reduce_('(RET_TRUE foo)'), 'TRUE')
assert equals(reduce_('(RET_TRUE bar)'), 'TRUE')
assert equals(reduce_('(RET_FALSE FALSE)'), 'FALSE')
assert equals(reduce_('(RET_FALSE foo)'), 'FALSE')
assert equals(reduce_('(RET_FALSE bar)'), 'FALSE')

# since the "action" of if is in the booleans, if is just applying the
# boolean to the next argument
assign_macro('IF', '\\x[x]')

assign_macro('IDENT', '\\x[x]')
assert equals(reduce_('(IDENT foo)'), 'foo')
assert equals(reduce_('(IDENT TRUE)'), 'TRUE')
assert equals(reduce_('(IDENT FALSE)'), 'FALSE')

#assign_macro('OR', '\\x[((x RET_TRUE) IDENT)]')
assign_macro('OR', '\\x[\\y[(((IF x) TRUE) y)]]')
assert equals(reduce_('((OR TRUE) TRUE)'), 'TRUE')
assert equals(reduce_('((OR TRUE) FALSE)'), 'TRUE')
assert equals(reduce_('((OR FALSE) TRUE)'), 'TRUE')
assert equals(reduce_('((OR FALSE) FALSE)'), 'FALSE')

#assign_macro('AND', '\\x[((x IDENT) RET_FALSE)]')
assign_macro('AND', '\\x[\\y[(((IF x) y) FALSE)]]')
assert equals(reduce_('((AND TRUE) TRUE)'), 'TRUE')
assert equals(reduce_('((AND TRUE) FALSE)'), 'FALSE')
assert equals(reduce_('((AND FALSE) TRUE)'), 'FALSE')
assert equals(reduce_('((AND FALSE) FALSE)'), 'FALSE')

assign_macro('NOT', '\\x[(((IF x) FALSE) TRUE)]')
assert equals(reduce_('(NOT TRUE)'), 'FALSE')
assert equals(reduce_('(NOT FALSE)'), 'TRUE')

# number n is a 2-param func that applies the first param n times to the 2nd
assign_macro('0', '\\f[\\x[x]]')
assign_macro('1', '\\f[\\x[(f x)]]')
assign_macro('2', '\\f[\\x[(f (f x))]]')
assign_macro('3', '\\f[\\x[(f (f (f x)))]]')
assign_macro('4', '\\f[\\x[(f (f (f (f x))))]]')
assign_macro('5', '\\f[\\x[(f (f (f (f (f x)))))]]')
assign_macro('6', '\\f[\\x[(f (f (f (f (f (f x))))))]]')
assign_macro('7', '\\f[\\x[(f (f (f (f (f (f (f x)))))))]]')
assign_macro('8', '\\f[\\x[(f (f (f (f (f (f (f (f x))))))))]]')
assign_macro('9', '\\f[\\x[(f (f (f (f (f (f (f (f (f x)))))))))]]')
assign_macro('10', '\\f[\\x[(f (f (f (f (f (f (f (f (f (f x))))))))))]]')

assign_macro('SUCC', '\\n[\\f[\\x[(f ((n f) x))]]]')

assert equals(reduce_('(SUCC 0)'), '1')
assert equals(reduce_('(SUCC 2)'), '3')
assert equals(reduce_('(SUCC 4)'), '5')
assert equals(reduce_('(SUCC 8)'), '9')
assert equals(reduce_('(SUCC (SUCC (SUCC (SUCC (SUCC 0)))))'), '5')

#assign_macro('Y', '\\f[( \\x[(f (x x))] \\x[(f (x x))] )]')


print('tests passed')

# from https://github.com/andrejbauer/plzoo
#
#pair := ^ a b . ^p . p a b ;
#first := ^ p . p (^x y . x) ;
#second := ^ p . p (^x y. y) ;
#

#
#-- Recursive definitions
#
#fix := ^f . (^x . f (x x)) (^x . f (x x)) ;
#
#-- Lists
#
#:constant error
#
#nil := ^x f . x ;
#
#cons := ^g r . ^x f . f g r ;
#
#head := ^l . l error (^a b . a) ;
#
#tail := ^l . l error (^a b . b) ;
#
#match := ^l x f. l x f ;
#
#map := fix (^map f l . match l nil (^x xs. cons (f x) (map f xs))) ;
#
#fold := fix (^fold x f l. match l x (^y ys . f y (fold x f ys))) ;
#
#-- Numbers
#
#0  := ^f x . x ;
#1  := ^f x . f x ;
#2  := ^f x . f (f x) ;
#3  := ^f x . f (f (f x)) ;
#4  := ^f x . f (f (f (f x))) ;
#5  := ^f x . f (f (f (f (f x)))) ;
#6  := ^f x . f (f (f (f (f (f x))))) ;
#7  := ^f x . f (f (f (f (f (f (f x)))))) ;
#8  := ^f x . f (f (f (f (f (f (f (f x))))))) ;
#9  := ^f x . f (f (f (f (f (f (f (f (f x)))))))) ;
#10 := ^f x . f (f (f (f (f (f (f (f (f (f x))))))))) ;
#
#succ := ^n f x . f (n f x) ;
#
#+ := ^n m f x . (n f) ((m f) x) ;
#
#* := ^n m f x . (n (m f)) x ;
#
#** := ^n m . m n ;
#
#iszero := ^n . (n (K false)) true ;
#
#pred := ^n . second (n (^p. pair (succ (first p)) (first p)) (pair 0 0)) ;
#
#== := fix (^== n m . if (iszero n) (iszero m) (== (pred n) (pred m))) ;
#
#fact := fix (^fact n . if (iszero n) 1 (* n (fact (pred n)))) ;
#
#<= := ^m n . iszero (n pred m) ;
#
#>= := ^m n . iszero (m pred n) ;
#
#< := ^m n . <= (succ m) n ;
#
#> := ^m n . >= m (succ n) ;
#
#mu := fix (^mu n f . if (f n) n (mu (succ n) f)) 0 ;
#
#/ := ^m n . mu (^k . > (* (succ k) n) m) ;
#
#| := ^m n . == (* m (/ n m)) n ;
#
#all := ^m n f . fix (^all k . if (> k n) true (if (f k) (all (succ k)) false)) m ;
#
#prime := ^n . all 2 (/ n 2) (^k . not (| k n)) ;
