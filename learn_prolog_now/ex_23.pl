% swipl -s ./23.pl

%  Exercise  2.3 Here is a tiny lexicon (that is, information about individual words) and a mini grammar consisting of one syntactic rule (which defines a sentence to be an entity consisting of five words in the following order: a determiner, a noun, a verb, a determiner, a noun). 

word(determiner,a).
word(determiner,every).
word(noun,criminal).
word(noun,'big kahuna burger').
word(verb,eats).
word(verb,likes).

sentence(Word1,Word2,Word3,Word4,Word5):-
      word(determiner,Word1),
      word(noun,Word2),
      word(verb,Word3),
      word(determiner,Word4),
      word(noun,Word5). 

% ?- sentence(A,B,C,D,E).
