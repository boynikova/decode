import string_matrix
import string_processing

'''
	Transposition ciphers

	ciphers provided:
		- Scytale
'''

class TranspositionCipher(string_matrix.StringMatrix):
	padding = 'x'
	mode = None
	transposition_key = None

	def __init__(self, mode, s, dimensions, 
			transposition_key = None, **kwargs):
		if transposition_key:
			self.transposition_key = string_processing.unique(
				transposition_key
			)
		super().__init__(s, dimensions, padding = self.padding)
		self.mode = mode
		self.__transform(mode)

	def __transform(self, mode, **kwargs):
		if self.mode == 'encode':
			self.encode(**kwargs)
		elif self.mode == 'decode':
			self.decode(**kwargs) 

	def encode(self, **kwargs):
		self.transpose_columns()
		self.transpose()

	def decode(self, **kwargs):
		self.transpose()
		self.transpose_columns()

	def transpose_columns(self):
		o = self.permutation_order()
		super().transpose_columns(o)

	def permutation_order(self):
		l = len(self.transposition_key)
		res = sorted(range(l), key = lambda i: self.transposition_key[i])
		if self.mode == 'decode':
			res = [res.index(i) for i in range(l)]
		return res

	def get_s(self):
		return self.s

class ScytaleCipher(TranspositionCipher):

	def __init__(self, mode, s, turns):
		dimensions = None
		if mode == 'encode':
			dimensions = (-1, turns)
		elif mode == 'decode':
			dimensions = (-1, len(s) // turns)
		super().__init__(mode, s, dimensions)

	def encode(self, **kwargs):
		self.transpose()

	def decode(self, **kwargs):
		self.transpose()

	def get_s(self):
		res = None
		if self.mode == 'decode':
			res = self.s.strip(self.padding)
		else:
			res = self.s
		return res

