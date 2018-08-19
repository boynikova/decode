from string import ascii_lowercase
import numpy as np 
from fractions import gcd

'''
	encode/decode messages using the Hill cipher.

	usage:
	ciphertext, key = hill_cipher_encode('secret message')
	plaintext, key = hill_cipher_decode(ciphertext, key)
'''
def hill_cipher_encode(message, key = None, 
		block_size = 4, alphabet = ascii_lowercase):
	kwargs = {
		'mode' : 'encode',
		'f_transform_block' : encode_block
	}
	return hill_cipher(message, key, block_size, alphabet, **kwargs)

def hill_cipher_decode(ciphertext, key, 
		block_size = 4, alphabet = ascii_lowercase):
	kwargs = {
		'mode' : 'decode',
		'f_transform_block' : decode_block
	}
	return hill_cipher(ciphertext, key, block_size, alphabet, **kwargs)

def hill_cipher(text, key, block_size, alphabet, **kwargs):
	mode = kwargs.get('mode')
	f_transform_block = kwargs.get('f_transform_block')
	charset_list = list(alphabet)
	len_charset = len(charset_list)
	# results
	res = None
	key_matrix = hill_key(block_size, len_charset, key)
	if key_matrix is not None:
		# list of characters encoded to digits
		digits = chars_to_digits(text, charset_list)
		# split message to blocks
		digit_blocks = blocks(digits, block_size)
		# blocks of characters as digits
		transformed_digits = []
		for block in digit_blocks:
			block = f_transform_block(block, key_matrix, len_charset)
			transformed_digits.extend(block)
		# convert digits to string
		res = ''.join(digits_to_chars(transformed_digits, charset_list))
		# convert key to list of lists
		key = key_matrix.tolist()
	# return result string and key
	return res, key

def encode_block(block, key_matrix, len_charset):
	block_vector = np.array(block)
	encoded_digits = key_matrix.dot(block_vector) % len_charset
	return encoded_digits
	
def decode_block(block, key_matrix, len_charset):
	block_vector = np.array(block)
	key_matrix_mod_inv = matrix_mod_inverse(key_matrix, len_charset)
	decoded_digits = key_matrix_mod_inv.dot(block_vector) % len_charset
	return decoded_digits

"""
	formatting
"""
def blocks(s, block_size):
	res = []
	l = len(s)
	if (l > 0):
		m = l % block_size
		if m > 0:
			if hasattr(s, 'extend'):
				s.extend([s[-1]] * (block_size - m))
			else:
				s += s[-1] * (block_size - m) 
		res = [s[i : i + block_size] for i in range(0, l, block_size)]
	return res

def chars_to_digits(chars, charset_list):
	charset = set(charset_list)
	digits = [
		ord(c) - 97 if c.isalpha() else charset_list.index(c)
		for c in chars.lower() if c in charset
	]
	return digits

def digits_to_chars(digits, charset_list):
	len_charset = len(charset_list)
	chars = [charset_list[i % len_charset] for i in digits]
	return chars

"""
	keys
"""
def hill_key(n, len_charset, key = None):
	key_matrix = None
	if key is None:
		# generate a key
		key_matrix = gen_hill_key(n, len_charset)
	else:
		# check if the key is square
		if all(len(row) == len(key) == n for row in key):
			# convert the key to numpy matrix
			key_matrix_tmp = np.array(key)
			if valid_hill_key(key_matrix_tmp, len_charset):
				key_matrix = key_matrix_tmp.astype(int)
	return key_matrix

def gen_hill_key(n, len_charset):
	key_matrix = np.random.randint(len_charset, size = (n, n))
	while not valid_hill_key(key_matrix, len_charset):
		key_matrix = np.random.randint(len_charset, size = (n, n))
	return key_matrix

def valid_hill_key(key_matrix, len_charset):
	res = False
	det = np.linalg.det(key_matrix)
	if det != 0:
		if coprime(det, len_charset):
			if int_mod_inverse(det, len_charset) is not None:
				res = True
	return res

"""
	math
"""
def coprime(a, b):
	return gcd(a, b) == 1

def matrix_mod_inverse(mat, m):
	det = np.linalg.det(mat)
	det_mod_inv = int_mod_inverse(det, m)
	mat_inv = np.linalg.inv(mat)
	cofactors = mat_inv * det
	return np.rint(cofactors * det_mod_inv % m).astype(int)

def int_mod_inverse(a, m):
	g, x, y = egcd(a, m)
	if g != 1:
		return None
	else:
		return x % m

def egcd(a, b):
	if a == 0:
		return (b, 0, 1)
	else:
		g, y, x = egcd(b % a, a)
		return (g, x - (b // a) * y, y)
