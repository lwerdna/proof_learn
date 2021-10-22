% swipl -s ./21.pl

%  Exercise  2.1 Which of the following pairs of terms unify? Where relevant, give the variable instantiations that lead to successful unification. 

bread = bread. % yes, atom to atom
'Bread' = bread. % no, mismatch on first char, atom to atom
'bread' = bread. % yes, atom to atom
Bread = bread. % no, mismatch on first char
bread = sausage. % no, different atoms
food(bread) = bread. % no, complex term vs atom
food(bread) = X. % yes, X can be the complex term
food(X) = food(bread). % yes, with {X==bread}
food(bread,X) = food(Y,sausage). % yes, with {Y==bread, X==sausage}
food(bread,X,beer) = food(Y,sausage,X). % no, X can't be both sausage and beer
food(bread,X,beer) = food(Y,kahuna_burger). % no, different arities
food(X) = X. % SWI-PROLOG says X = food(X) ???
meal(food(bread),drink(beer)) = meal(X,Y). % yes, with X set to complex term food(bread), etc.
meal(food(bread),X) = meal(X,drink(beer)). % no, X can't be both food(bread) and drink(beer)
