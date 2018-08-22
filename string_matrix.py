import string_processing

'''
	StringMatrix class

	characters stored in a two-dimensional list

	functions:
		locate() : find character in the matrix given coordinates
		coordinates() : get matrix coordinates for the given character
		transpose_columns() : switch columns of the matrix
		transpose() : matrix transposition
		__str()__() : format the class variable matrix for printing
'''

class StringMatrix():
	"""
		properties
			s : string
				the string stored in the matrix
			dimensions : tuple of int
				dimensions of the matrix
			base_index : int
				base index of coordinates in the matrix
			matrix : list of lists
				two-dimensional list of characters
	"""
	s = None
	dimensions = None
	base_index = None
	matrix = None

	def __init__(self, s, dimensions, 
				base_index = 0, padding = None):
		"""
			arguments
				s : string
				dimensions : tuple of int 
					(r, c) for an r-by-c matrix 
				base_index : int
				padding : string
		"""
		self.base_index = base_index
		matrix = string_matrix(s, dimensions, padding = padding)
		if matrix:
			self.dimensions = dimensions
			self.matrix = matrix
		if matrix is None:
			self.s = None
		else:
			self.s = matrix_to_string(self.matrix)

	def locate(self, p):
		"""
			value of the character at the specified position

			arguments
				p : tuple of int
			return
				string
				None
					if the matrix coordinates represented by p 
						are out of range
		"""
		res = None
		b = self.base_index
		rows, columns = self.dimensions
		r, c = p
		r -= b 
		c -= b
		if 0 <= r < rows and 0 <= c < columns:
			res = self.s[r * columns + c]
		return res

	def coordinates(self, c):
		"""
			location(s) of a character in the matrix

			arguments
				c : string 
			return
				list of tuple of int
				empty list
					if the character is not in the matrix
					if c is an empty string	
					if c has more than one character		
		"""
		res = []
		n_columns = self.dimensions[1]
		if c and len(c) == 1:
			index_list = string_processing.find_char(self.s, c)
			if index_list:
				for i in index_list:
					base_index = self.base_index
					row_index, col_index = divmod(i, n_columns)
					res.append(
						(row_index + base_index, col_index + base_index)
					)
		return res

	def transpose_columns(self, o):
		"""
			transpose columns of the matrix 
				to the order specified 
	
			arguments
				o : list
					where o[i] is the index of the column 
					that should be at the ith position 
					in the result
					all i should be unique and within 
						the number of columns of m
			return
				True
					if the matrix is set to a new value
				False
					otherwise
		"""
		res = False
		m = transpose_columns(self.matrix, o)
		if m:
			self.matrix = m
			self.s = matrix_to_string(m)
			res = True
		return res

	def transpose(self):
		"""
			transpose of the matrix

			return
				True
					if the matrix is set to a new value
				False
					otherwise
		"""
		res = False
		m = transpose(self.matrix)
		if m:
			self.matrix = m
			self.s = matrix_to_string(m)
			res = True
		return res

	def __str__(self):
		"""
			string representation of the matrix

			return
				string
		"""
		if self.matrix:
			return '\n'.join(str(row) for row in self.matrix)
		elif self.matrix == []:
			return str([])
		else:
			return str(None)

'''
	module level functions
'''

def string_matrix(s, dimensions, padding = None):
	"""
		create a two-dimensional list of characters from a string
		filled by row 
		
		if only one of the dimensions (r, c) are positive, 
		the resulting matrix will have r rows or c columns 

		if necessary, s will be trimmed to fit the given dimensions 
		or padded to length, if padding string is provided 

		arguments
			s : string
			dimensions : tuple of int 
				(r, c) for an r-by-c matrix 
			padding : string
		return
			list of lists of string
			empty list
				if both dimensions are zero
				if s is empty
			None
				if neither dimension is a positive number
				if dimensions multiply to a value greater 
					than the length of the string 
					and no padding is specified
	"""
	res = None
	try:
		r, c = dimensions
	except:
		pass
	else:
		if r == 0:
			if c == 0:
				res = []
		if s:
			l = len(s)
			if c > 0:
				if r > 0:
					s = string_processing.pad_to_length(
						s, r * c, padding = padding
					)
			elif r > 0:			
				d, m = divmod(l, r)
				if m != 0:
					d += 1
					m = 0
				s = string_processing.pad_to_length(
					s, r * d, padding = padding
				)
				c = len(s) // r
			spl = string_processing.split_n_padding(
					s, c, padding = padding
				)
			if spl:
				res = list(map(list, spl))
		else:
			res = []
	return res

def matrix_to_string(m):
	"""
		list of items 
		flattened to string

		arguments
			m : list of lists of string
		return
			string
			empty string
				if the list is empty
	"""
	res = []
	list(map(res.extend, m))
	return ''.join([str(s) for s in res])

def transpose_columns(m, order):
	"""
		transpose columns of a matrix represented 
		by a two-dimensional list 

		arguments
			m : list of lists
			order : list
				where o[i] is the index of the column 
				that should be at the ith position 
				in the result
				all i should be unique and within 
					the number of columns of m
		return
			list of lists
			empty list
				if the list is empty
			None
				if any column index is out of range
				if an column is not listed in o
	"""
	res = None
	t = transpose(m)
	if t:
		t_n_columns = len(t)
		unique_columns = set(order)
		if len(unique_columns) == len(order) == t_n_columns:
			if all(i < t_n_columns for i in unique_columns):
				res = []
				for i in order:
					res.append(t[i])
				res = transpose(res)
	elif t == []:
		res = []
	return res

def transpose(m):
	"""
		transpose of a matrix represented 
		by a two-dimensional list

		arguments
			m : list of lists
		return
			list of lists
			empty list 
				if the list is empty
			None 
				if the sublists 
					are not the same length
	"""
	res = None
	if m == []:
		res = []
	else:
		n_columns = len(m[0])
		if all(len(row) == n_columns for row in m):
			res = list(map(list, zip(*m)))
	return res