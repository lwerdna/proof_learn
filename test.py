#!/usr/bin/env python

from node import ApplicationNode, AbstractionNode, VariableNode
from parser import parse_str as ps
from engine import reduce_

def apply(a, b):
	tmp = ApplicationNode(a, b)
	tmp = reduce_(tmp)
	return tmp

ltrue = ps('\\x[\\y[x]]')
lfalse = ps('\\x[\\y[y]]')
ite = ps('\\cond[\\a[\\b[((cond a) b)]]]')

assert ltrue == ps('\\foo[\\bar[x]]')
assert ite == ps('\\foo[\\bar[\\baz[((lala a) b)]]]')

assert apply(ite, lfalse) == lfalse
assert apply(ite, ltrue) == ltrue

# from https://github.com/andrejbauer/plzoo
#
#pair := ^ a b . ^p . p a b ;
#first := ^ p . p (^x y . x) ;
#second := ^ p . p (^x y. y) ;
#
#-- The constant function
#
#K := ^ x y . x ;
#
#-- Booleans
#
#true  := ^x y . x ;
#false := ^x y . y ;
#if := ^u . u ;
#
#and := ^x y . if x y false ;
#or  := ^x y . if x true y ;
#not := ^x . if x false true ;
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
