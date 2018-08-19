from string import ascii_lowercase

import cipher_grid
import string_processing

'''
	Grid ciphers

	ciphers provided:
		- Polybius
		- Bifid
		- Playfair
		- Nihilist

	notes
		todo:
			all classes:
				- check input types and sizes
				- check empty return values
			Nihilist:
				- support empty key
'''

class PolybiusGrid(cipher_grid.CipherGrid):

	def __init__(self, translate = 'ck', grid_key = None, base_index = 1):
		if translate:
			if not translate.islower():
				translate = translate.lower()
		replace_table = dict(zip(*translate))
		if grid_key:
			grid_key = string_processing.alpha(grid_key).lower()
		super().__init__(
			ascii_lowercase, (5, 5), grid_key = grid_key, 
			replace_table = replace_table, base_index = base_index
		)

	def plaintext_to_parts(self, s):
		return string_processing.group_alpha(s, 1)

	def ciphertext_to_parts(self, s):
		return string_processing.group_digits(s, 2)

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

	def coords_to_part(self, coords, **kwargs):
		return '{}{}'.format(*coords)

	def part_to_coords(self, p, **kwargs):
		return tuple(map(int, p))

	def encoded_parts_to_string(self, parts):
		return ''.join(parts)

	def decoded_parts_to_string(self, parts):
		return ''.join(parts)

class BifidGrid(PolybiusGrid):

	def __init__(self, translate = 'ck', grid_key = None):
		super().__init__(translate, grid_key)

	def encode(self, s, **kwargs):
		s = super().encode(s)
		s = self.bifid_unzip(s)
		return super().decode(s)

	def decode(self, s):
		s = super().encode(s)
		s = self.bifid_zip(s)
		return super().decode(s)

	def bifid_unzip(self, s):
		return s[::2] + s[1::2]

	def bifid_zip(self, s):
		l = len(s)
		z = list(zip(s[:l // 2 + 1], s[l // 2:]))
		return ''.join([''.join(p) for p in z])

class PlayfairGrid(PolybiusGrid):
	padding = 'x'

	def __init__(self, translate = 'ck', grid_key = None):
		super().__init__(translate, grid_key, base_index = 0)

	def coordinates(self, p):
		p1, p2 = p
		return (super().coordinates(p1), super().coordinates(p2))

	def locate(self, coords):
		c1, c2 = coords
		return super().locate(c1) + super().locate(c2)

	def plaintext_to_parts(self, s):
		s = super().plaintext_to_parts(s)
		res = []
		l = len(s)
		i = 0
		while i < l:
			if i == l - 1 or s[i] == s[i + 1]:
				p = s[i] + self.padding
				i += 1
			else:
				p = s[i] + s[i + 1]
				i += 2
			res.append(p)
		return res

	def ciphertext_to_parts(self, s):
		return string_processing.group_alpha(s, 2)

	def coords_to_part(self, coords, **kwargs):
		coords = self.playfair_substitution(coords, shift = 1)
		return self.locate(coords)

	def part_to_coords(self, p, **kwargs):
		coords = self.coordinates(p)
		return self.playfair_substitution(coords, shift = -1)

	def decoded_parts_to_string(self, parts):
		res = super().decoded_parts_to_string(parts)
		return string_processing.remove(res, self.padding)

	def playfair_substitution(self, coords, shift):
		rows, columns = self.dimensions
		a, b = coords
		r1, c1 = a
		r2, c2 = b
		if r1 == r2:
			a = (r1, (c1 + shift) % columns)
			b = (r2, (c2 + shift) % columns)
		elif c1 == c2:
			a = ((r1 + shift) % rows, c1)
			b = ((r2 + shift) % rows, c2)
		else:
			a = (r1, c2) 
			b = (r2, c1)
		return (a, b)

class NihilistGrid(PolybiusGrid):
	keyword = None

	def __init__(self, keyword, translate = 'ck', grid_key = None):
		self.keyword = keyword
		super().__init__(translate, grid_key)

	def coords_to_part(self, coords, **kwargs):
		pi = int(super().coords_to_part(coords, **kwargs))
		pi += self.key_digit(kwargs.get('index'))
		return str(pi)

	def part_to_coords(self, p, **kwargs):
		pi = int(p)
		pi -= self.key_digit(kwargs.get('index'))
		return super().part_to_coords(str(pi), **kwargs)

	def key_digit(self, index):
		i = index % len(self.keyword)
		c = self.coordinates(self.keyword[i])
		return int('{}{}'.format(*c))