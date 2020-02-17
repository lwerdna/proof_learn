# represent a lambda term by a tree structure
#
# every node in the tree is a TermNode, of which three classes derive:
# AbstractionNode, ApplicationNode, and VariableNode

import re
import copy

class TermNode:
	def __init__(self):
		self.children = []
		self.parent = None
		self.id = 0

		# these get decorated later, after parsing
		self.depth = -1	# depth of this node (recalculated after reductions)

	# VariableNode overrides this one, substituting itself
	def var_subst(self, name, term):
		for i in range(len(self.children)):
			self.children[i] = self.children[i].var_subst(name, term)
		return self

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

	def __eq__(self, other):
		assert not (other is None) # else None -> 'None' -> 'x'
		#print('__eq__(\"%s\", \"%s\")' % (self, other))
		a = str(self)
		b = str(other)
		a = re.sub(r'\w+', 'x', a)
		b = re.sub(r'\w+', 'x', b)
		#print('left as un-variabled string: %s' % a)
		#print('right as un-variabled string: %s' % b)
		return a == b

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

	def var_subst(self, name, term):
		if self.name == name:
			return copy.deepcopy(term)
		return self

	def __str__(self):
		return self.name

	def str_tree(self, node_hl=None, depth=0):
		indent = '  ' * depth
		mark = ' <--' if self is node_hl else ''
		return '%s%d.Variable "%s"%s%s' % (indent, self.id, self.name, ' bound=%d'%self.binding.id if self.binding else '', mark)
		#return '%sVariable "%s"%s .parent=%s' % (indent, self.name, mark, self.parent)

class AbstractionNode(TermNode):
	def __init__(self, var_name, term):
		super().__init__()
		self.degree = 1
		self.var_name = var_name
		self.children = [term]

	def __str__(self):
		return '\\%s[%s]' % (self.var_name, str(self.children[0]))

	def str_lone(self):
		return '\\%d.%s[...]' % (self.id, self.var_name)

	def str_tree(self, node_hl=None, depth=0):
		indent = '  ' * depth
		mark = ' <--' if self is node_hl else ''
		result = '%s%d.Abstraction %s%s\n' % (indent, self.id, self.var_name, mark)
		#result = '%sAbstraction %s%s .parent=%s\n' % (indent, self.var_name, mark, self.parent)
		result += self.children[0].str_tree(node_hl, depth+1)
		return result

class ApplicationNode(TermNode):
	def __init__(self, left, right):
		super().__init__()
		self.degree = 2
		self.children = [left, right]

	def __str__(self):
		return '(%s %s)' % (str(self.children[0]), str(self.children[1]))

	def str_tree(self, node_hl=None, depth=0):
		indent = '  ' * depth
		mark = ' <--' if self is node_hl else ''
		result = '%s%d.Application%s\n' % (indent, self.id, mark)
		#result = '%sApplication%s .parent=%s\n' % (indent, mark, self.parent)
		result += self.children[0].str_tree(node_hl, depth+1)
		result += '\n'
		result += self.children[1].str_tree(node_hl, depth+1)
		return result

