from string import ascii_lowercase, digits

import string_matrix
import cipher_grid
import string_processing

'''
	Transposition ciphers

	ciphers provided:
		- Scytale
'''

class TranspositionCipher(string_matrix.StringMatrix):
	mode = None
	padding = None

	def __init__(self, mode, s, dimensions):
		self.mode = mode
		super().__init__(s, dimensions, padding = self.padding) 

class Scytale():

	def __init__():
		pass
