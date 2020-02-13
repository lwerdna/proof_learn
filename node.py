# represent a lambda term by a tree structure
#
# every node in the tree is a TermNode, of which three classes derive:
# AbstractionNode, ApplicationNode, and VariableNode

import copy

class TermNode:
	def __init__(self):
		self.children = []
		pass

	# VariableNode overrides this one, substituting itself
	def var_subst(self, name, term):
		for i in range(len(self.children)):
			self.children[i] = self.children[i].var_subst(name, term)
		return self

	# Perform the application on node <target>
	# currently inefficiently visits the whole tree
	def apply(self, target):
		# if one of our children is the target, perform the application
		if len(self.children) > 0 and self.children[0] == target:
			self.children[0] = self.children[0].apply(target)
			return self

		if len(self.children) > 1 and self.children[1] == target:
			self.children[1] = self.children[1].apply(target)
			return self

		# else search deeper
		if len(self.children) > 0:
			self.children[0].apply(target)
		if len(self.children) > 1:
			self.children[1].apply(target)

		# done
		return self

class VariableNode(TermNode):
	def __init__(self, name):
		super().__init__()
		self.name = name

	def var_subst(self, name, term):
		if self.name == name:
			return copy.deepcopy(term)
		return self

	def str_line(self):
		return self.name

	def str_tree(self, node_hl=None, depth=0):
		indent = '  ' * depth
		mark = ' <--' if self==node_hl else ''
		return '%sVariable "%s"%s' % (indent, self.name, mark)

class AbstractionNode(TermNode):
	def __init__(self, var_name, term):
		self.var_name = var_name
		self.children = [term]

	def str_line(self):
		return '\\%s[%s]' % (self.var_name, self.children[0].str_line())

	def str_tree(self, node_hl=None, depth=0):
		indent = '  ' * depth
		mark = ' <--' if self==node_hl else ''
		result = '%sAbstraction %s%s\n' % (indent, self.var_name, mark)
		result += self.children[0].str_tree(node_hl, depth+1)
		return result

class ApplicationNode(TermNode):
	def __init__(self, left, right):
		self.children = [left, right]

	def apply(self, target):
		if self != target:
			return super().apply(target)

		# I'm the ApplicationNode they want executed! do it!
		abstraction = self.children[0]
		argument = self.children[1]

		varname = abstraction.var_name
		body = abstraction.children[0]

		return body.var_subst(varname, argument)

	def str_line(self):
		return '(%s %s)' % (self.children[0].str_line(), self.children[1].str_line())

	def str_tree(self, node_hl=None, depth=0):
		indent = '  ' * depth
		mark = ' <--' if self==node_hl else ''
		result = '%sApplication%s\n' % (indent, mark)
		result += self.children[0].str_tree(node_hl, depth+1)
		result += '\n'
		result += self.children[1].str_tree(node_hl, depth+1)
		return result
