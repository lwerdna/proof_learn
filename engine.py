#!/usr/bin/env python
#
# interact with the lambda term to do reductions, etc.

from node import ApplicationNode, AbstractionNode, VariableNode

def get_all_nodes(term):
	result = []

	depth = 0
	queue = [term]
	while queue:
		for node in queue:
			result.append((node, depth))

		tmp = []
		for node in queue:
			tmp = node.children

		queue = tmp
		depth += 1

	return result

# return the ApplicationNode that will be the target of the next reduce step
def reducible(term):
	nodes_and_depths = get_all_nodes(term)
	nodes_and_depths = filter(lambda x: isinstance(x[0], ApplicationNode), nodes_and_depths)
	nodes_and_depths = sorted(nodes_and_depths, key=lambda x: x[1], reverse=True)
	if not nodes_and_depths:
		return None
	return nodes_and_depths[0][0]

# reduce a term, single-step style
def reduce_step(term, target=None):
	if not target:
		target = term.reducible()
	if not target:
		return term

	# if the target is the tree itself, return what he leaves behind
	if target == term:
		return term.apply(target)

	# else return 
	term.apply(target)
	return term
