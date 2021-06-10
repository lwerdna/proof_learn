#!/usr/bin/env python

import sys
import copy
from node import ApplicationNode, AbstractionNode, VariableNode
from parser import parse_expr as ps
from engine import equals, assign_macro, to_tree, reduce_, reduce_step, load_stdlib

load_stdlib()

# return first or second arg

assert equals('((RETARG0 a) b)', 'a')
assert equals('((RETARG1 a) b)', 'b')

# alpha equivalence (variable names don't matter after bindings resolved)
assert equals('RETARG0', r'\foo[\bar[foo]]')
assert equals('RETARG1', r'\foo[\bar[bar]]')

# boolean stuff
assert equals('(ITE FALSE)', 'FALSE')
assert equals('(ITE TRUE)', 'TRUE')

# K combinator from SKI returns a function that always returns the given argument
assert equals('(RET_TRUE FALSE)', 'TRUE')
assert equals('(RET_TRUE foo)', 'TRUE')
assert equals('(RET_TRUE bar)', 'TRUE')
assert equals('(RET_FALSE FALSE)', 'FALSE')
assert equals('(RET_FALSE foo)', 'FALSE')
assert equals('(RET_FALSE bar)', 'FALSE')

# I combinator from SKI returns given argument, identity
assert equals('(I foo)', 'foo')
assert equals('(I TRUE)', 'TRUE')
assert equals('(I FALSE)', 'FALSE')

# if just applies the condition (true or false) to the next two arguments

#assign_macro('OR', '\\x[((x RET_TRUE) I)]')
assert equals('((OR TRUE) TRUE)', 'TRUE')
assert equals('((OR TRUE) FALSE)', 'TRUE')
assert equals('((OR FALSE) TRUE)', 'TRUE')
assert equals('((OR FALSE) FALSE)', 'FALSE')

#assign_macro('AND', '\\x[((x I) RET_FALSE)]')
assert equals('((AND TRUE) TRUE)', 'TRUE')
assert equals('((AND TRUE) FALSE)', 'FALSE')
assert equals('((AND FALSE) TRUE)', 'FALSE')
assert equals('((AND FALSE) FALSE)', 'FALSE')

assert equals('(NOT TRUE)', 'FALSE')
assert equals('(NOT FALSE)', 'TRUE')

# number n is a 2-param func that applies the first param n times to the 2nd
assert equals('(SUCC 0)', '1')
assert equals('(SUCC 2)', '3')
assert equals('(SUCC 4)', '5')
assert equals('(SUCC 8)', '9')
assert equals('(SUCC (SUCC (SUCC (SUCC (SUCC 0)))))', '5')

assert equals('((PLUS 0) 0)', '0')
assert equals('((PLUS 0) 1)', '1')
assert equals('((PLUS 1) 1)', '2')
assert equals('((PLUS 2) 2)', '4')
assert equals('((PLUS 4) 3)', '7')

assert equals('((MULT 3) 0)', '0')
assert equals('((MULT 3) 2)', '6')
assert equals('((MULT 3) 3)', '9')
assert equals('((MULT 6) 3)', '((PLUS 9) 9)')
assign_macro('27', '((PLUS ((PLUS 9) 9)) 9)')
assign_macro('36', '((PLUS ((PLUS ((PLUS 9) 9)) 9)) 9)')
assert equals('((MULT 6) 6)', '36')

#assert equals('((EXP 2) 0)', '1') # wouldn't this be nice if it worked
assert equals('((EXP 0) 2)', '0')
assert equals('((EXP 2) 2)', '4')
assert equals('((EXP 2) 3)', '8')
assert equals('((EXP 3) 3)', '27')

assert equals('(ISZERO 0)', 'TRUE')
assert equals('(ISZERO 1)', 'FALSE')
assert equals('(ISZERO 2)', 'FALSE')
assert equals('(ISZERO 3)', 'FALSE')

# from https://github.com/andrejbauer/plzoo/blob/master/src/lambda/example.lambda

# given items a,b return ((f a) b)
print('tuples')
assign_macro('3_AND_5', '((PAIR 3) 5)')
assign_macro('5_AND_7', '((PAIR 5) 7)')
assign_macro('8_AND_9', '((PAIR 8) 9)')
assert equals('(FIRST 3_AND_5)', '3')
assert equals('(FIRST 5_AND_7)', '5')
assert equals('(FIRST 8_AND_9)', '8')
assert equals('(SECOND 3_AND_5)', '5')
assert equals('(SECOND 5_AND_7)', '7')
assert equals('(SECOND 8_AND_9)', '9')

print('predecessor')
assert equals('(PRED_F ((PAIR 3) 5))', '((PAIR 5) 6)')
assert equals('(PRED_F ((PAIR 5) 6))', '((PAIR 6) 7)')
assert equals('(PRED 9)', '8')
assert equals('(PRED 5)', '4')
assert equals('(PRED 1)', '0')

print('recursive double()')
assign_macro('DOUBLE_HOF', r'\f[\n[(((IF (ISZERO n)) 0) ((PLUS 2) (f (PRED n))))]]')
assert equals('((DOUBLE_HOF f) 0)', '0') # test base case
assign_macro('DOUBLE', '(Y DOUBLE_HOF)')
assert equals('(DOUBLE 1)', '2')
assert equals('(DOUBLE 2)', '4')
assert equals('(DOUBLE 4)', '8')

print('recursive triangle()')
assign_macro('TRIANGLE_HOF', r'\f[\n[(((IF (ISZERO n)) 0) ((PLUS n) (f (PRED n))))]]')
assert equals('((TRIANGLE_HOF f) 0)', '0') # test base case
assign_macro('TRIANGLE', '(Y TRIANGLE_HOF)')
assert equals('(TRIANGLE 2)', '3')
assert equals('(TRIANGLE 3)', '6')
assert equals('(TRIANGLE 4)', '10')

print('recursive factorial()')
assign_macro('FACT_HOF', r'\f[\n[(((IF (ISZERO n)) 1) ((MULT n) (f (PRED n))))]]')
assert equals('((FACT_HOF f) 0)', '1') # test base case
assign_macro('FACT', '(Y FACT_HOF)')
assert equals('(FACT 2)', '2')
assert equals('(FACT 3)', '6')
#assign_macro('120', reduce_('((((MULT 5) 4) 3) 2)'))
#assert equals('((Y FACT) 5)', '120')

print('tests passed')

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
