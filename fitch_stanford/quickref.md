Fitch system for propositional logic: http://intrologic.stanford.edu/glossary/fitch_system.html

Has 9 rules of inference:

| rule                                        | source/dest                                 | description          |
| ------------------------------------------- | ------------------------------------------- | -------------------- |
| and introduction                            | conjunction from conjuncts                  | a, b ⊢ a&b           |
| and elimination                             | conjuncts from conjunction                  | a&b ⊢ a              |
| or introduction                             | disjunction from **at least one** disjunct  | a ⊢ a\|b             |
| or elimination                              | conclusion from (disjunction, implications) | a\|b, a->c, b->c ⊢ c |
| negation introduction                       | negation from path to contradiction         | a -> b, a -> /b ⊢ /a |
| negation elimination                        |                                             | //a ⊢ a              |
| implication introduction                    | implication from a subproof                 | (a ⊢ b) ⊢ a -> b     |
| implication elimination<br />(modus ponens) | consequent from implication, antecedent     | a -> b, a ⊢ b        |
| biconditional introduction                  | biconditional from implication, inverse     | a->b, b->a ⊢ a<->b   |
| biconditional elimination                   | implication, inverse from biconditional     | a<->b ⊢ a->b, b->a   |
