# Stanford's Fitch System Learning Tool

I really like [this tool](http://intrologic.stanford.edu/glossary/fitch_system.html) from [Stanford's Introduction to Logic Course](http://intrologic.stanford.edu/homepage/index.html). It's straightforward html and javascript with no frameworks or fluff. This goal of this repository is to preserve the tool and add additional exercises.

There is no absurdity ⊥ in this system, unlike https://proofs.openlogicproject.org/ which adds some difficulty.

Use the [quick reference](./quickref.html) for a review of all the permitted rules in the Fitch system. The "Be-Fitched! Strategy Guide" ([local](./strategy.html)) ([Stanford](http://logic.stanford.edu/intrologic/extras/fitch.html)) has very good advice on when to work forward from premises or backward from goals.

## Propositional Logic
| links | task | notes |
| ----- | ---- | ----- |
|([local](./exercise_04_01.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_01.html))|p, q, p ∧ q ⇒ r ⊢ r||
|([local](./exercise_04_02.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_02.html))|p ∧ q ⊢ q ∨ r|conjunction introduction|
|([local](./exercise_04_03.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_03.html))|p ⇒ q, q ⇔ r ⊢ p ⇒ r|hypothetical syllogism, chain deduction|
|([local](./exercise_04_04.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_04.html))|p ⇒ q, m ⇒ p ∨ q ⊢ m ⇒ q|practice or elimination|
|([local](./exercise_04_05.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_05.html))|p ⇒ (q ⇒ r) ⊢ (p ⇒ q) ⇒ (p ⇒ r)|distributivity property of implication|
|([local](./exercise_04_06.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_06.html))|⊢ p ⇒ (q ⇒ p)|raw implication introduction|
|([local](./exercise_04_07.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_07.html))|⊢ (p ⇒ (q ⇒ r)) ⇒ ((p ⇒ q) ⇒ (p ⇒ r))||
|([local](./exercise_04_08.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_08.html))|⊢ (¬p ⇒ q) ⇒ ((¬p ⇒ ¬q) ⇒ p)||
|([local](./exercise_04_09.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_09.html))|⊢ ¬¬p||
|([local](./exercise_04_10.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_10.html))|p ⇒ q ⊢ ¬q ⇒ ¬p||
|([local](./exercise_04_11.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_11.html))|p ⇒ q ⊢ ¬p ∨ q|material implication|
|([local](./exercise_04_12.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_12.html))|⊢ ((p ⇒ q) ⇒ p) ⇒ p|Pierce's law|
|([local](./exercise_04_13.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_13.html))|¬(p ∨ q) ⊢ (¬p ∧ ¬q)|De Morgan, negation of disjunction|
|([local](./exercise_04_14.html)) ([Stanford](http://intrologic.stanford.edu/exercises/exercise_04_14.html))|⊢ p v ¬p|law excluded middle|
|([local](./exercise_g2.html))|p ⇒ ¬q, q ⊢ ¬p|modus tollens variation, Be-Fitched technique G2|
|([local](./exercise_disjunction_elimination.html))|p ∨ q, ¬p ⊢ ¬q|disjunctive syllogism|
|([local](./exercise_material_implication.html))|¬p ∨ q ⊢ p ⇒ q|material implication, reversed|
|([local](./exercise_double_negation.html))|⊢ ¬¬p ⇒ p|double negation|
|([local](./exercise_contrapositive.html))|p ⇒ q ⊢ ¬q ⇒ ¬p |contrapositive|
|([local](./exercise_impl_conv_bicond.html))|p ⇒ q, ¬p ⇒ ¬q ⊢ p ⇔ q|implication and converse leads to biconditional|
