#!/usr/bin/env python

import stlc

def check(claim:str, proof:str):
    term = stlc.parse(proof)
    assert str(term.type_assignment({})) == claim

if __name__ == '__main__':
    # https://en.wikipedia.org/wiki/Simply_typed_lambda_calculus

    # I = λx:α.x
    claim = '(α → α)'
    proof = '(λ x (BASE α) (VAR x))'
    check(claim, proof)

    # K = λx:α.λy:β.x
    claim = '(α → (β → α))'
    proof = '(λ x (BASE α) (λ y (BASE β) (VAR x)))'
    check(claim, proof)

    # S = λx:α→(β→γ).λy:α→β.λz:α.((x z) (y z))
    claim = '((α → (β → γ)) → ((α → β) → (α → γ)))'
    proof = '''
        (λ x (→ (BASE α) (→ (BASE β) (BASE γ)))
         (λ y (→ (BASE α) (BASE β))
          (λ z (BASE α)
           (APP
            (APP (VAR x) (VAR z))
            (APP (VAR y) (VAR z))))))'''
    check(claim, proof)

    # https://math.stackexchange.com/questions/1985352/how-to-prove-a-a%E2%86%92b%E2%8A%A2b-without-double-negation-elimination
    claim = '(((A → Q) → Q) → ((B → Q) → ((A → B) → Q)))'
    proof = '''
        (λ x (→ (→ (BASE A) (BASE Q)) (BASE Q))
         (λ y (→ (BASE B) (BASE Q))
          (λ z (→ (BASE A) (BASE B))
           (APP
            (VAR x)
            (λ v (BASE A)
             (APP
              (VAR y)
              (APP
               (VAR z)
               (VAR v))))))))'''
    check(claim, proof)

    # http://logic.stanford.edu/intrologic/exercises/exercise_04_05.html
    claim = '((P → (Q → R)) → ((P → Q) → (P → R)))'
    proof = '''
        (λ x (→ (BASE P) (→ (BASE Q) (BASE R)))
         (λ y (→ (BASE P) (BASE Q))
          (λ z (BASE P)
           (APP
            (APP (VAR x) (VAR z))
            (APP (VAR y) (VAR z))
           ))))'''
    check(claim, proof)

    print('PASS')

