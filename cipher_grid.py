from abc import ABC, abstractmethod
from copy import deepcopy

import string_matrix
import string_processing

'''
	CipherGrid class

	functions:
		update() : update alphabet stored in the grid, 
			optionally update grid_key and translation_table
		locate() : locate a character in the grid 
			at the given coordinates
		coordinates() : coordinates of a character in the grid 
			with translation
		encode() : encode a string using the grid
		decode() : decode a string using the grid
		__str__() : format the class variable grid for printing
'''

class CipherGrid(string_matrix.StringMatrix, ABC):
	alphabet = ''
	grid_key = ''
	translation_table = {}
	grid = []

	def __init__(self, alphabet, dimensions, 
				grid_key = None, replace_table = None, base_index = 0):
		super().__init__('', dimensions, base_index = base_index)
		self.update(alphabet, grid_key, replace_table)

	def update(self, alphabet, grid_key = None, replace_table = None):
		self.__set_grid_key(grid_key)
		self. __set_translation_table(replace_table)
		self.__set_alphabet(alphabet)
		super().update(self.alphabet)
		self.grid = deepcopy(self.matrix)

	def __set_grid_key(self, grid_key):
		res = self.grid_key
		if grid_key is not None:
			res = grid_key
		self.grid_key = res

	def __set_translation_table(self, replace_table):
		res = self.translation_table
		if replace_table is not None:
			res = {
				k: v for k, v in replace_table.items() if v
			}
		self.translation_table = res

	def __set_alphabet(self, alphabet):
		res = self.alphabet
		if alphabet:
			s = alphabet
			s = self.grid_key + s
			remove = list(self.translation_table.keys())
			s = string_processing.remove(s, remove)
			s = string_processing.unique(s)
			res = s
		self.alphabet = res

	def locate(self, p):
		res = super().locate(p)
		return res

	def coordinates(self, c):
		res = None
		if c in self.translation_table:
			c = self.translation_table[c]
		coords_list = super().coordinates(c)
		if coords_list:
			res = coords_list[0]
		return res

	def encode(self, s, **kwargs):
		kwargs.update(
			{
				'mode': 'encode',
				'to_parts': self.plaintext_to_parts,
				'transform_part': self.encode_part,
				'parts_to_string': self.encoded_parts_to_string
			}
		)
		return self.__transform(s, **kwargs)

	def decode(self, s, **kwargs):
		kwargs.update(
			{
				'mode': 'decode',
				'to_parts': self.ciphertext_to_parts,
				'transform_part': self.decode_part,
				'parts_to_string': self.decoded_parts_to_string				
			}
		)
		return self.__transform(s, **kwargs)

	def __transform(self, s, **kwargs):
		res = []
		to_parts = kwargs.pop('to_parts')
		transform_part = kwargs.pop('transform_part')
		parts_to_string = kwargs.pop('parts_to_string')
		parts = to_parts(s)
		i = 0
		for p in parts:
			kwargs.update({'index': i})
			p = transform_part(p, **kwargs)
			res.append(p)
			i += 1
		kwargs.pop('index')
		return parts_to_string(res)

	@abstractmethod
	def plaintext_to_parts(self, s):
		pass

	@abstractmethod
	def ciphertext_to_parts(self, s):
		pass

	@abstractmethod
	def encode_part(self, p, **kwargs):
		pass

	@abstractmethod
	def decode_part(self, p, **kwargs):
		pass

	@abstractmethod
	def coords_to_part(self, coords, **kwargs):
		pass

	@abstractmethod
	def part_to_coords(self, p, **kwargs):
		pass

	@abstractmethod
	def encoded_parts_to_string(self, parts):
		pass

	@abstractmethod
	def decoded_parts_to_string(self, parts):
		pass

	def __str__(self):
		if self.grid:
			return '\n'.join(str(row) for row in self.grid)
		elif self.grid == []:
			return str([])
		else:
			return str(None)		