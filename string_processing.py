import re

'''
	string processing
'''
def unique(s):
	"""
		unique characters in a string
		preserves original order
	"""
	x = set()
	res = [c for c in s if c not in x and (x.add(c) or True)]
	return ''.join(res)

def rotate(s, n):
	"""
		rotation of a string or list

		arguments:
			s : string or list
			n : the number of characters to rotate by
				to the right if n is positive
				to the left if n is negative
	"""
	return s[-n:] + s[:-n]

def replace(s, mapping, default = None, join = None):
	""" 
		arguments
			s : string or list of strings
			mapping : dict  
			default : None or string
			join : None or string
				if not None, replacements will be joined 
				on this string in the output
		return 
			string
	"""
	s2 = []
	for c in s:
		if c in mapping:
			s2.append(mapping[c])
		else:
			if not default:
				s2.append(c)
			else:
				s2.append(default)
	if join:
		res = join.join(s2)
	else:
		res = ''.join(s2)   
	return res

def replace_and_remove(s, mapping):
	"""
		arguments
			s : string or list of strings
			mapping : dict {k : v}
		return
			string

		replace all k in the string with v for (k, v) and remove v
	"""
	replace_compliment = {v : '' for v in mapping.values() if v}
	mapping.update(replace_compliment)
	return replace(s, mapping)

def remove(s, chars):
	"""
		arguments
			s : string or list
			chars : string or list
		return 
			string
	"""
	res = s
	if chars:
		pattern = re.compile(r'[' + ''.join(chars) + r']')
		res = pattern.sub('', s)
	return res

'''
	searching
'''
def find_char(s, c):
	"""
		get indices of a character in a string

		arguments
			s : string
			c : string
		return
			list
			empty list 
				if s is empty
			None
				if c is empty
	"""
	res = None
	if c:
		if len(c) == 1:
			c = re.escape(c)
			pattern = re.compile(r'[' + c + r']')
			fi = pattern.finditer(s)
			res = [f.start() for f in fi]
	return res

'''
	splitting and repeating
'''
def split_n(s, n):
	"""
		split a string into a list of strings 
		of the given length, preserving the remainder if any

		arguments
			s : string
			n : int
		return
			list of strings
				of length n 
				with the possible exception of the last item 
				which might have less than n characters
			empty list
				if n is 0
				if the string is empty
			None
				if n is a negative number
	"""
	res = None
	if n == 0:
		res = []
	elif n > 0:
		l = len(s)
		res = [s[i : i + n] for i in range(0, l, n)]
	return res

def split_n_padding(s, n, padding = ' '):
	"""
		split a string into a list of strings 
		of the given length

		arguments
			s : string
			n : int
			padding : string
		return
			list of strings 
				of length n
			empty list 
				if the length of the string is less than n, 
				and no padding is specified  					
				if n is 0
			None
				if n is a negative number
	"""
	res = split_n(s, n)
	if res:
		li = res[-1]
		l = len(li)
		if l != n:
			if padding:
				li = pad_to_length(li, n, padding = padding)
				if li:
					res[-1] = li
			else:
				res = res[:-1]
	return res

def pad_to_length(s, n, padding = ' '):
	"""
		pad a string to a given length

		arguments
			s : string
			n : int
			padding : string
		return
			string
				of length n
				trimmed if the string is longer than n
			empty string
				if n is 0
				if the string is shorter than n 
					and no padding is specified	
			None
				if n is a negative number
	"""
	res = None
	if n == 0:
		res = ''
	elif n > 0:
		l = len(s)
		if l < n:
			d = n - l
			if padding:
				s = s + padding * d
			else:
				s = ''	
		res = s[:n]	
	return res

def repeat_to_length(s, n):
	"""
		repeat a string to a given length

		arguments
			s : string
			n : int
			padding : string
		return
			string
				of length n
				trimmed if the string is longer than n
			empty string
				if n is 0
				if the string is shorter than n 
					and no padding is specified	
			None
				if n is a negative number
	"""
	return pad_to_length(s, n, padding = s)

'''
	filtering
'''
def alnum(s):
	"""
		only alphanumeric characters in a string

		arguments
			s : string
		return
			string
	"""
	pattern = re.compile(r'[a-zA-Z0-9]+')
	return ''.join(pattern.findall(s))

def alpha(s):
	"""
		only alphabetic characters in a string

		arguments
			s : string
		return
			string
	"""
	pattern = re.compile(r'[a-zA-Z]')
	return ''.join(pattern.findall(s))

def digits(s):
	"""
		only digits in a string

		arguments
			s : string
		return
			string
	"""
	pattern = re.compile(r'\d')
	return ''.join(pattern.findall(s))

'''
	grouping
'''

def group_n(s, n): 
	"""
		get all nonoverlapping groups of exactly n 
		contiguous characters of any type but newline 

		arguments
			s : string
			n : int
		return
			list
	"""
	pattern = re.compile(r'.{' + str(n) + r'}')
	return pattern.findall(s)

def group_printable(s, n):
	"""
		get all nonoverlapping groups of n contiguous 
		printable characters in a string

		arguments
			s : string
			n : 
		return 
			list
	"""
	pattern = re.compile(r'[ -~]{' + str(n) + r'}')
	return pattern.findall(s)

def group_alpha(s, n):
	"""
		get all nonoverlapping groups of n contiguous 
		alphabet characters in a string

		arguments
			s : string
			n : 
		return 
			lists
	"""
	pattern = re.compile(r'[a-zA-Z]{' + str(n) + r'}')
	return pattern.findall(s)

def group_digits(s, n):
	"""
		get all nonoverlapping groups of n contiguous 
		digits in a string

		arguments
			s : string
			n : int
		return 
			list
	"""
	pattern = re.compile(r'[\d]{' + str(n) + r'}')
	return pattern.findall(s)

def group_alnum(s, n):
	"""
		get all nonoverlapping groups of n contiguous 
		alphanumeric characters in a string

		arguments
			s : string
			n : 
		return 
			list 
	"""
	pattern = re.compile(r'[a-zA-Z0-9]{' + str(n) + '}')
	return pattern.findall(s)

def double_letters_i(s):
	"""
		get the indices of each pair of repeated letters 
		in a string, including pairs separated by any number 
		of non-alphabetic characters
		
		arguments
			s : string
		return
			list of tuples
				index of each letter in the pair
	"""
	pattern = re.compile(r'([a-zA-Z])[^a-zA-Z]*\1')
	return [(m.start(), m.end() - 1) for m in re.finditer(pattern, s)]

def every_nth(s, n, o = 0):
	"""
		every nth character in a string

		arguments
			s : string
			n : int
				stride 
			o : int
				offset
			return
				string
	"""
	l = len(s)
	return ''.join(s[o : l : n])

def every_nth_digit(s, n, o = 0):
	"""
		get the first digit in a string at the given offset
		and every nth digit after that
		
		arguments
			s : string
			n : int
			o : int
				offset
		return
			list
	"""
	return digits(s[o:])[::n]