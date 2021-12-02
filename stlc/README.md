This is a proof checker implementing [simply typed lambda calculus](https://en.wikipedia.org/wiki/Simply_typed_lambda_calculus) to process statements in [minimal logic](https://en.wikipedia.org/wiki/Minimal_logic) restricted to implication.

See `./test.py` for 

## Syntax

The syntax for terms is a very verbose lisp-like syntax to ease the burden of parsing. I was losing too much time trying to get a grammar to work the way I wanted.

| stlc term   | syntax                     |
| ----------- | -------------------------- |
| variable    | (VAR $varname)             |
| abstraction | (ABS $varname $type $body) |
| application | (APP $term $term)          |

The symbol `λ` can be used instead of `ABS`.

For the type field in an abstraction, there are two syntax forms:

| kind                    | syntax              |
| ----------------------- | ------------------- |
| base types              | (BASE $typename)    |
| function or arrow types | (ARROW $type $type) |

### Example

The stlc term `λx:α.x` is expressed with `(λ x (BASE α) (VAR x))`.

### Example

The stlc term `λx:α.λy:β.x` is expressed with `(λ x (BASE α) (λ y (BASE β) (VAR x)))`.

### Example

The stlc term `λx:α→(β→γ).λy:α→β.λz:α.((x z) (y z))` is expressed with `(λ x (→ (→ (BASE A) (BASE Q)) (BASE Q)) (λ y (→ (BASE B) (BASE Q)) (λ z (→ (BASE A) (BASE B)) (APP (VAR x) (λ v (BASE A) (APP (VAR y) (APP (VAR z) (VAR v))))))))`.

## Proofs

### Example

https://math.stackexchange.com/questions/1985352/how-to-prove-a-a%E2%86%92b%E2%8A%A2b-without-double-negation-elimination

claim: `((A -> Q) -> Q) -> (B -> Q) -> (A -> B) -> Q`

proof:

```
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
        (VAR v)
       )))))))
```

### Examples

http://logic.stanford.edu/intrologic/exercises/exercise_04_05.html

claim: `((P → (Q → R)) → ((P → Q) → (P → R)))`
proof:

```
(λ x (→ (BASE P) (→ (BASE Q) (BASE R)))
 (λ y (→ (BASE P) (BASE Q))
  (λ z (BASE P)
   (APP
    (APP (VAR x) (VAR z))
    (APP (VAR y) (VAR z))
   ))))
```

