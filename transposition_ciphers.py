from string import ascii_lowercase, digits

import string_matrix
import cipher_grid
import string_processing

'''
	Transposition ciphers

	ciphers provided:
		- ADFGX
		- ADFGVX
'''

class ADFGVXGrid(cipher_grid.CipherGrid):
	alphabet = ascii_lowercase + digits
	dimensions = (6, 6)
	labels = list('adfgvx')
	padding = 'x'
	transposition_key = None

	def __init__(self, transposition_key, grid_key = None, **kwargs):
		self.transposition_key = string_processing.unique(transposition_key)
		super().__init__(
			self.alphabet, self.dimensions, grid_key = grid_key, **kwargs
		) 
		
	def encode(self, s, **kwargs): 
		l = len(self.transposition_key)
		s = super().encode(s, **kwargs)
		cipher_grid = self.ADFGVXCipher(
			'encode', s, (-1, l), self.transposition_key
		)
		cipher_grid.transpose_columns()
		cipher_grid.transpose()
		return cipher_grid.s

	def decode(self, s, **kwargs):
		l = len(self.transposition_key)
		cipher_grid = self.ADFGVXCipher(
			'decode', s, (-1, len(s) // l), self.transposition_key
		)
		cipher_grid.transpose()
		cipher_grid.transpose_columns(**kwargs)
		s = cipher_grid.s
		return super().decode(s).strip(self.decoded_padding())

	def plaintext_to_parts(self, s):
		return string_processing.group_alpha(s, 1)

	def ciphertext_to_parts(self, s):
		return string_processing.group_alpha(s, 2)

	def coords_to_part(self, coords, **kwargs):
		return ''.join(tuple(map(self.labels.__getitem__, coords)))

	def part_to_coords(self, p, **kwargs):
		return tuple(map(self.labels.index, p))

	def decoded_padding(self):
		padding = self.padding
		return self.locate(self.part_to_coords(padding + padding))

	class ADFGVXCipher(string_matrix.StringMatrix):
		mode = None
		transposition_key = None
		padding = 'x'

		def __init__(self, mode, s, dimensions, transposition_key):
			self.mode = mode
			self.transposition_key = transposition_key
			super().__init__(s, dimensions, padding = self.padding)

		def transpose_columns(self):
			o = self.permutation_order()
			super().transpose_columns(o)
	
		def permutation_order(self):
			l = len(self.transposition_key)
			res = sorted(range(l), key = lambda i: self.transposition_key[i])
			if self.mode == 'decode':
				res = [res.index(i) for i in range(l)]
			return res

class ADFGXGrid(ADFGVXGrid):
	alphabet = ascii_lowercase
	dimensions = (5, 5)
	labels = list('adfgx')

	def __init__(self, transposition_key, grid_key = None, **kwargs):
		kwargs['replacements'] = cipher_grid.CipherGrid.replacements_dict(
			kwargs.pop('remove', '').lower(), 
			kwargs.pop('translate', '').lower()
		) or {'i': 'j'}
		super().__init__(transposition_key, grid_key = grid_key, **kwargs) 