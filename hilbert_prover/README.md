This is a naive proof searcher and checker for Hilbert style logics.

It's a toy project that brute forces and should not replace a real prover like Otter or McCune.

Internally, propositions are stored as trees, and determining when an axiom scheme can be applied to another is done by matching the left side of the root node (the antecedent of the implication), and making appropriate substitutions in the right side of the root node (the consequent of the implication). That's all handled in engine.py.

File test.py runs some ad hoc unit tests on engine.py.

File search.py uses engine.py to brute force generate other axioms.

Files proof_* "prove" statements by showing that a sequence of modus ponens applications (enforced by engine.py) lay a path between initial axioms and the desired result. A different file exists for different Hilbert systems.
