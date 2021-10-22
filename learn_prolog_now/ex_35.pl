
leaf(X).

tree(X) :- leaf(X).
% tree(tree(Left),tree(Right)).
tree(Left,Right) :- tree(Left), tree(Right).

%?- leaf(1).
%true.
%
%?- leaf(2).
%true.
%
%?- tree(leaf(1), leaf(2)).
%true.
%
%?- tree(tree(leaf(1),  leaf(2)),leaf(4)).
%true.
%

swap(leaf(Atom), leaf(Atom)).
swap(tree(L1,R1),tree(L2,R2)) :- swap(L1,R2), swap(R1,L2).

% ?- swap(tree(tree(leaf(1),  leaf(2)),  leaf(4)),T).
% T = tree(leaf(4), tree(leaf(2), leaf(1))).
