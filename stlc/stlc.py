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

    # x:σ ∈ Γ
    # -------
    # Γ ⊢ x:σ
    #
    # if x has type σ in the environment, we know x has type σ
    #
    # this corresponds to a variable representing a proposition
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

    #    Γ, x:σ ⊢ e:τ
    # ------------------
    # Γ ⊢ (λx:σ.e):(σ→τ)
    #
    # if, with an environment temporarily extended with x:σ, the body of an abstraction has type e:τ
    # then the type of the abstraction is (σ→τ)
    #
    # this corresponds to the natural deduction move "assume x..."
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

    #    Γ ⊢ a:σ→τ Τ ⊢ b:σ
    # ----------------------
    #       Γ ⊢ (a b):τ
    #
    # if a has type σ→τ and b has type σ then (a b) has type τ
    #
    # this corresponds to modus ponens
    def type_assignment(self, environment):
        ltype = self.lhs.type_assignment(environment)
        rtype = self.rhs.type_assignment(environment)
        if isinstance(ltype, FunctionType):
            if ltype.lhs == rtype:
                return ltype.rhs
        breakpoint()

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
        #return '(→ %s %s)' % (self.lhs, self.rhs)
        return '(%s → %s)' % (self.lhs, self.rhs)

    def __eq__(self, other):
        return isinstance(other, FunctionType) and self.lhs == other.lhs \
          and self.rhs == other.rhs

#------------------------------------------------------------------------------
# lispy like parser
#------------------------------------------------------------------------------

def lists_to_nodes(lists):
    # lambda calculus core elements
    if lists[0] in ['ABS', 'λ']:
        assert len(lists) == 4
        var_name = lists[1]
        var_type = lists_to_nodes(lists[2])
        body = lists_to_nodes(lists[3])
        return Abstraction(var_name, var_type, body)
    elif lists[0] == 'APP':
        assert len(lists) == 3
        lhs = lists_to_nodes(lists[1])
        rhs = lists_to_nodes(lists[2])
        return Application(lhs, rhs)
    elif lists[0] == 'VAR':
        assert len(lists) == 2
        return Variable(lists[1])
    # STLC types
    if lists[0] == 'BASE':
        assert len(lists) == 2 
        var_name = lists[1]
        return BaseType(var_name)
    elif lists[0] in ['ARROW', '→']:
        assert len(lists) == 3
        lhs = lists_to_nodes(lists[1])
        rhs = lists_to_nodes(lists[2])
        return FunctionType(lhs, rhs)        
    else:
        raise SyntaxError('stlc unrecognized: ' + str(lists[0]))

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
