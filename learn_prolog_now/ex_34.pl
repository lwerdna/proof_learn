greater_than(succ(X), 0).
greater_than(succ(X), succ(Y)) :- greater_than(X, Y).

% why won't greater_than(succ(succ(succ(0))), X) return all the numbers 3 is greater than?
