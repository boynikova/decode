from string import ascii_lowercase, digits

import cipher_grid
import transposition_ciphers
import string_processing

'''
	Grid ciphers

	ciphers provided:
		- Polybius
		- Bifid
		- Playfair
		- Nihilist
		- ADFGX
		- ADFGVX
'''

class PolybiusGrid(cipher_grid.CipherGrid):

	def __init__(self, grid_key = None, base_index = 1, **kwargs):
		kwargs['replacements'] = cipher_grid.CipherGrid.replacements_dict(
			kwargs.pop('remove', '').lower(), 
			kwargs.pop('translate', '').lower()
		) or {'c': 'k'}
		if grid_key:
			grid_key = string_processing.alpha(grid_key).lower()
		super().__init__(
			ascii_lowercase, (5, 5), grid_key, base_index, **kwargs
		)

	def plaintext_to_parts(self, s):
		return string_processing.group_alpha(s, 1)

	def ciphertext_to_parts(self, s):
		return string_processing.group_digits(s, 2)

	def coords_to_part(self, coords, **kwargs):
		return '{}{}'.format(*coords)

	def part_to_coords(self, p, **kwargs):
		return tuple(map(int, p))

class BifidGrid(PolybiusGrid):

	def __init__(self, grid_key = None, **kwargs):
		super().__init__(grid_key, **kwargs)

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

	def __init__(self, grid_key = None, **kwargs):
		super().__init__(grid_key, base_index = 0, **kwargs)

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

	def __init__(self, keyword, grid_key = None, **kwargs):
		self.keyword = keyword
		super().__init__(grid_key, **kwargs)

	def coords_to_part(self, coords, **kwargs):
		pi = int(super().coords_to_part(coords, **kwargs))
		pi += self.key_digit(kwargs.get('index'))
		return str(pi)

	def part_to_coords(self, p, **kwargs):
		pi = int(p)
		pi -= self.key_digit(kwargs.get('index'))
		return super().part_to_coords(str(pi), **kwargs)

	def key_digit(self, index):
		res = 0
		if self.keyword:
			i = index % len(self.keyword)
			c = self.coordinates(self.keyword[i])
			res = int('{}{}'.format(*c))
		return res

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
		cipher = transposition_ciphers.ADFGVXCipher(
			'encode', s, (-1, l), self.transposition_key
		)
		return cipher.get_s()

	def decode(self, s, **kwargs):
		l = len(self.transposition_key)
		cipher = transposition_ciphers.ADFGVXCipher(
			'decode', s, (-1, len(s) // l), self.transposition_key
		)
		s = cipher.get_s()
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