#!/usr/bin/env python

from enum import Enum, auto

class TID(Enum):
	LAMBDA = auto()
	VARIABLE = auto()
	DOT = auto()
	LPAREN = auto()
	RPAREN = auto()
	LBRACK = auto()
	RBRACK = auto()

# a token is a tuple (TID, <val>) if value applies
class TokenManager:
	def __init__(self, tokenList):
		self.tokenList = tokenList
		self.i = 0

	def reset(self):
		self.i = 0

	def peek(self, nAhead=0):
		if (self.i + nAhead) >= len(self.tokenList):
			return None
		return self.tokenList[self.i + nAhead]

	def shift(self, tid_expected=None):
		if self.is_end():
			raise Exception("token list is empty")

		(tok_id, tok_val) = self.tokenList[self.i]
		self.i += 1

		if tid_expected != None and tid_expected != tok_id:
			raise Exception("expected token %s but got instead %s" % (tid_expected.name, tok_val))

		return (tok_id, tok_val)

	def is_end(self):
		return self.peek() == None

	def __str__(self):
		result = []
		for k in range(self.i, len(self.tokenList)):
			(tok_type, tok_val) = self.tokenList[k]
			result.append("%d: %s '%s'" % (k, tok_type.name, tok_val))
		return "\n".join(result)

	def str_line(self):
		return ' '.join([x[1] for x in self.tokenList[self.i:]])

def tokenize(line):
	tokens = []
	line = line.rstrip()
	chars = list(line)

	i = 0
	while i < len(chars):
		c = chars[i]
		if c == '\\':
			tokens.append((TID.LAMBDA,'\\'))
			i += 1
		elif c.isspace():
			while i<len(chars) and chars[i].isspace():
				i += 1
		elif c == '.':
			tokens.append((TID.DOT, '.'))
			i += 1
		elif c.isidentifier():
			value = ''
			while i<len(chars) and chars[i].isidentifier():
				value += chars[i]
				i += 1
			tokens.append((TID.VARIABLE, value))
		elif c == '(':
			tokens.append((TID.LPAREN, '('))
			i += 1
		elif c == ')':
			tokens.append((TID.RPAREN, ')'))
			i += 1
		elif c == '[':
			tokens.append((TID.LBRACK, '['))
			i += 1
		elif c == ']':
			tokens.append((TID.RBRACK, ']'))
			i += 1
		else:
			raise Exception("tokenizing on \"%s...\"" % chars[i:i+8])

	return TokenManager(tokens)
