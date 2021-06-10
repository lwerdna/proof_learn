# Lambda Lab

These are some tools for learning and experimenting with lambda calculus.

I always get confused implementing grammars and parsers, so I sacrificed some brevity and imposed:

* parentheses around application (like https://en.wikipedia.org/wiki/Lambda_calculus)
* not dots, but brackets around the bodies of abstractions (like https://plato.stanford.edu/entries/lambda-calculus/)

Backslashes are used instead of the lambda symbol to ease typing. The grammar is:

```
term -> var
     -> \var[term]
     -> (var var)
```

## Why? Aren't there enough lambda calculus implementations?

There are, and this one likely won't do anything special, but it's a learning effort.

> What I cannot create, I do not understand. -Feynman
