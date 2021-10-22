% swipl -s ./24.pl

% Exercise  2.4 Here are six Italian words:
% astante , astoria , baratto , cobalto , pistola , statale .
% They are to be arranged, crossword puzzle fashion, in the following grid: 

word(astante,  a,s,t,a,n,t,e).
word(astoria,  a,s,t,o,r,i,a).
word(baratto,  b,a,r,a,t,t,o).
word(cobalto,  c,o,b,a,l,t,o).
word(pistola,  p,i,s,t,o,l,a).
word(statale,  s,t,a,t,a,l,e). 

crossword(V1,V2,V3,H1,H2,H3) :- word(V1,A,M1,B,M2,C,M3,D),
								word(V2,E,M4,F,M5,G,M6,H),
								word(V3,I,M7,J,M8,K,M9,L),
								word(H1,M,M1,N,M4,O,M6,P),
								word(H2,Q,M2,R,M5,S,M8,T),
								word(H3,U,M3,V,M6,W,M9,X).

% ?- crossword(V1,V2,V3,H1,H2,H3), dif(V1,H1), dif(V3,H3).
% V1 = astoria,
% V2 = baratto,
% V3 = statale,
% H1 = astante,
% H2 = cobalto,
% H3 = pistola
