Write proofs in python by making implementing a domain-specific language (DSL) / fluid interface. Proofs look like this:

### Example 1:

```python
# Given p => q and q <=> r, prove p => r
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
assert tree.check_deduction('(P => R)')
```

### Example 2:

```python
# Given p => (q => r), prove (p => q) => (p => r).
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
```

