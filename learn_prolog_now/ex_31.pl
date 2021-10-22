% swipl -s ./31.pl

child(john,jim).
child(jim,james).
child(james,jerry).

descend(X,Y) :- child(X,Y).
descend(X,Y) :- descend(X,Z), descend(Z,Y).

% yes, descend will keep expanding, with no "escape"
