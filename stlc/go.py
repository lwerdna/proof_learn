#!/usr/bin/env python

#------------------------------------------------------------------------------
# nodes for STLC elements (variables, abstraction, application)
#------------------------------------------------------------------------------
class STLCNode:
    def type_assignment(self, environment):
        raise NotImplementedError

# variable, eg: a, b, c
class Variable(STLCNode):
    def __init__(self, name):
        self.name = name

    def type_assignment(self, environment):
        return environment.get(self.name, None)

    def __str__(self):
        return '(VAR "%s")' % self.name

# abstraction, eg: λx:α.x
class Abstraction(STLCNode):
    def __init__(self, var_name, var_type, body):
        self.var_name = var_name
        self.var_type = var_type
        self.body = body

    def type_assignment(self, environment):
        environment2 = dict(environment)
        environment2[self.var_name] = self.var_type
        return FunctionType(self.var_type, self.body.type_assignment(environment2))

    def __str__(self):
        return '(ABS "%s" %s %s)' % (self.var_name, self.var_type, self.body)

# application, eg: (x y)
class Application(STLCNode):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def type_assignment(self, environment):
        ltype = self.lhs.type_assignment(environment)
        rtype = self.rhs.type_assignment(environment)
        if isinstance(ltype, FunctionType):
            if ltype.lhs == rtype:
                return ltype.rhs

    def __str__(self):
        return '(APP %s %s)' % (self.lhs, self.rhs)

# base types / atomic types / type constants, eg: α, β, γ
class BaseType(STLCNode):
    def __init__(self, name):
        self.name = name

    def __str__(self):
        return '%s' % self.name

    def __eq__(self, other):
        return isinstance(other, BaseType) and self.name == other.name

# function types, eg: α → β
class FunctionType(STLCNode):
    def __init__(self, lhs, rhs):
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self):
        return '(%s → %s)' % (self.lhs, self.rhs)

    def __eq__(self, other):
        return isinstance(other, FunctionType) and self.lhs == other.lhs \
          and self.rhs == other.rhs

#------------------------------------------------------------------------------
# lispy like parser
#------------------------------------------------------------------------------

def lists_to_nodes(lol):
    # lambda calculus core elements
    if lol[0] in ['ABS', 'λ']:
        assert len(lol) == 4
        var_name = lol[1]
        var_type = lists_to_nodes(lol[2])
        body = lists_to_nodes(lol[3])
        return Abstraction(var_name, var_type, body)
    elif lol[0] == 'APP':
        assert len(lol) == 3
        lhs = lists_to_nodes(lol[1])
        rhs = lists_to_nodes(lol[2])
        return Application(lhs, rhs)
    elif lol[0] == 'VAR':
        assert len(lol) == 2
        return Variable(lol[1])
    # STLC types
    if lol[0] == 'BASE':
        assert len(lol) == 2 
        var_name = lol[1]
        return BaseType(var_name)
    elif lol[0] in ['ARROW', '→']:
        assert len(lol) == 3
        lhs = lists_to_nodes(lol[1])
        rhs = lists_to_nodes(lol[2])
        return FunctionType(lhs, rhs)        
    else:
        raise SyntaxError('stlc unrecognized: ' + str(lol[0]))

def tokens_to_lists(tokens):
    if len(tokens) == 0:
        raise SyntaxError('unexpected EOF while reading')
    token = tokens.pop(0)
    if token == '(':
        L = []
        while tokens[0] != ')':
            L.append(tokens_to_lists(tokens))
        assert tokens.pop(0) # pop off ')'
        return L
    elif ')' == token:
        raise SyntaxError('unexpected )')
    else:
        return token

# convert '(APP (VAR x) (VAR x))' to ['APP', ['VAR', 'x'], ['VAR', 'x']]
def lispy_to_lists(expr:str):
    tokens = expr.replace('(', ' ( ').replace(')', ' ) ').split()
    return tokens_to_lists(tokens)

def lispy_to_tree_string(result:str):
    import re
    toks = re.split(r'\s+', result.replace('(', ' ( ').replace(')', ' ) ').strip())
    depth = -1
    result = ''
    for i in range(len(toks)):
        if toks[i] == '(':
            depth += 1
            result += '\n' + '  '*depth
        elif toks[i] == ')':
            depth -= 1
        else:
            result += toks[i] + ' '
    return result

def parse(expr:str):
    lists = lispy_to_lists(expr)
    tree = lists_to_nodes(lists)
    return tree

#------------------------------------------------------------------------------
# main
#------------------------------------------------------------------------------

def main():
    #parse(r'a')

    # Examples of closed terms, i.e. terms typable in the empty context, are:

    # I = λx:α.x
    result = parse('(λ x (BASE α) (VAR x))')
    assert str(result.type_assignment({})) == '(α → α)'

    # K = λx:α.λy:β.x
    result = parse('(λ x (BASE α) (λ y (BASE β) (VAR x)))')
    assert str(result.type_assignment({})) == '(α → (β → α))'

    # S = λx:α→(β→γ).λy:α→β.λz:α.((x z) (y z))
    result = parse('''
        (λ x (→ (BASE α) (→ (BASE β) (BASE γ)))
         (λ y (→ (BASE α) (BASE β))
          (λ z (BASE α)
           (APP
            (APP (VAR x) (VAR z))
            (APP (VAR y) (VAR z))
           ))))''')
    assert str(result.type_assignment({})) == '((α → (β → γ)) → ((α → β) → (α → γ)))'

    # https://math.stackexchange.com/questions/1985352/how-to-prove-a-a%E2%86%92b%E2%8A%A2b-without-double-negation-elimination
    # prove ((A -> Q) -> Q) -> (B -> Q) -> (A -> B) -> Q
    result = parse('''
        (λ x (→ (→ (BASE A) (BASE Q)) (BASE Q))
         (λ y (→ (BASE B) (BASE Q))
          (λ z (→ (BASE A) (BASE B))
           (APP
            (VAR x)
            (λ v (BASE A)
              (APP
               (VAR y)
               (APP
                (VAR z)
                (VAR v)
               )))))))''')
    assert str(result.type_assignment({})) == '(((A → Q) → Q) → ((B → Q) → ((A → B) → Q)))'

    print('PASS')

if __name__ == '__main__':
    main()
