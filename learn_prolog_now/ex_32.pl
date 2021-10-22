% swipl -s ./32.pl

directlyin(irini,natasha). % "irina is directly in natasha"
directlyin(natasha,olga). % "natasha is directly in olga"
directlyin(olga,katarina). % "olga is directly in katarina"

in(X,Y) :- directlyin(X,Y).
in(X,Y) :- directlyin(X,T), in(T,Y).


