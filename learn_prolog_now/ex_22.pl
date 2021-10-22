% swipl -s ./22.pl

house_elf(dobby).
witch(hermione).
witch('McGonagall').
witch(rita_skeeter).
magic(X) :- house_elf(X).
magic(X) :- wizard(X).
magic(X) :- witch(X).

%?-  magic(house_elf).     false, house_elf isn't an atom
%?-  wizard(harry).        false, where is wizard(harry). asserted?
%?-  magic(wizard).        false, wizard isn't an atom
%?-  magic('McGonagall').  true, but wizard({X=McGonagall}) will be tried first and wizard() procedure is not defined
%?-  magic(Hermione).      tricky! Hermione is a variable name, and will match for
%                          Hermione = dobby
%                          Hermione = McGonagall
%                          Hermione = rita_skeeter
