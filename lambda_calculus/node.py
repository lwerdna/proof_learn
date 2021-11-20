# represent a lambda term by a tree structure
#
# every node in the tree is a TermNode, of which three classes derive:
# AbstractionNode, ApplicationNode, and VariableNode

import copy

class TermNode:
    def __init__(self):
        self.children = []
        self.parent = None
        self.id = 0

        # these get decorated later, after parsing
        self.depth = -1    # depth of this node (recalculated after reductions)

    def update_children(self, old, new):
        if self.degree > 0 and self.children[0] is old:
            self.children[0] = new
        if self.degree > 1 and self.children[1] is old:
            self.children[1] = new

    def descendents(self):
        result = []
        for child in self.children:
            result.append(child)
            result += child.descendents()
        return result

    # '│  │  │'         current indent string
    #
    # if this is not the last child:
    # '│  │  ├'         this indent string
    # '│  │  │  │'      next indent string
    #
    # if this is the last child
    # '│  │  └'         this indent string
    # '│  │     │'      next indent string
    def compute_indent_strings(self, indent:str, last_child:bool):
        if not indent:
            return ('', ' │')

        indent = indent[0:-1]
        if last_child:
            return (indent+'└─', indent+'  │')
        else:
            return (indent+'├─', indent+'│ │')

    def str_tree(self, node_hl=None, indent='', last_child=True):
        pass

    def __ne__(self, other):
        return not (self == other)

    def __hash__(self):
        return id(self)

class VariableNode(TermNode):
    def __init__(self, name):
        super().__init__()
        self.degree = 0
        self.name = name

        # decorated after parsing
        self.binding = None # abstraction node

    def __str__(self):
        return self.name

    def str_tree(self, node_hl=None, indent='', last_child=True):
        mark = ' <--' if self is node_hl else ''

        (indent_here, _) = self.compute_indent_strings(indent, last_child)
        #return '%sVAR "%s"%s%s' % (indent_here, self.name, ' bound=%d'%self.binding.id if self.binding else '', mark)
        return '%s"%s"%s' % (indent_here, self.name, mark)
        #return '%sVariable "%s"%s .parent=%s' % (indent, self.name, mark, self.parent)

class AbstractionNode(TermNode):
    def __init__(self, var_name, term):
        super().__init__()
        self.degree = 1
        self.var_name = var_name
        self.children = [term]

    def __str__(self):
        return 'λ%s[%s]' % (self.var_name, str(self.children[0]))

    def str_lone(self):
        return 'λ%d.%s[...]' % (self.id, self.var_name)

    def str_tree(self, node_hl=None, indent='', last_child=True):
        mark = ' <--' if self is node_hl else ''
        (indent_here, indent_next) = self.compute_indent_strings(indent, last_child)
        #result = '%s%d.λ %s%s\n' % (indent_here, self.id, self.var_name, mark)
        result = '%sλ%s%s\n' % (indent_here, self.var_name, mark)
        #result = '%sAbstraction %s%s .parent=%s\n' % (indent, self.var_name, mark, self.parent)
        result += self.children[0].str_tree(node_hl, indent_next)
        return result

class ApplicationNode(TermNode):
    def __init__(self, left, right):
        super().__init__()
        self.degree = 2
        self.children = [left, right]

    def __str__(self):
        return '(%s %s)' % (str(self.children[0]), str(self.children[1]))

    def str_tree(self, node_hl=None, indent='', last_child=True):
        mark = ' <--' if self is node_hl else ''
        #result = '%s%d.Application%s\n' % (indent, self.id, mark)
        #result = '%sApplication%s .parent=%s\n' % (indent, mark, self.parent)

        (indent_here, indent_next) = self.compute_indent_strings(indent, last_child)

        #result = '%s%s.APP%s\n' % (indent_here, self.id, mark)
        result = '%sapply%s\n' % (indent_here, mark)

        result += self.children[0].str_tree(node_hl, indent_next, False)
        result += '\n'
        result += self.children[1].str_tree(node_hl, indent_next)
        return result

