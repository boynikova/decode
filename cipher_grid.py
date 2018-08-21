from abc import ABC, abstractmethod

import string_matrix
import string_processing

'''
	CipherGrid class

	functions:
		locate() : locate a character in the grid 
			at the given coordinates
		coordinates() : coordinates of a character in the grid 
			with translation
		encode() : encode a string using the grid
		decode() : decode a string using the grid
'''

class CipherGrid(string_matrix.StringMatrix, ABC):
	alphabet = ''
	grid_key = ''
	translation_table = {}

	def __init__(self, alphabet, dimensions, 
				grid_key = None, replace_table = None, base_index = 0):
		s = alphabet
		self.grid_key = grid_key
		if grid_key is not None:
			s = grid_key + s
		if replace_table is not None:
			translation_table = {
				k: v for k, v in replace_table.items() if v
			}
			self.translation_table = translation_table
			remove = list(translation_table.keys())
			s = string_processing.remove(s, remove)
		s = string_processing.unique(s)
		super().__init__(s, dimensions, base_index = base_index)
		if self.s is not None:
			self.alphabet = self.s

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

	def encode_part(self, p, **kwargs):
		res = ''
		coords = self.coordinates(p)
		if coords:
			res = self.coords_to_part(coords, **kwargs)
		return res

	def decode_part(self, p, **kwargs):
		res = ''
		coords = self.part_to_coords(p, **kwargs)
		if coords:
			res = self.locate(coords)
		return res

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