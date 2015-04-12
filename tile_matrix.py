import easygui
#Makes the text file parsing the level
#helper functions
def fill_row(size):
	row = []
	for i in range(size):
		row.append("X")
	return row

def fill_section(matrix, row, col, x, y, element):
	for i in range(x):
		matrix[row-i][col] = "!"
		matrix[row+i][col] = "!"
		for p in range(y):
			matrix[row][col+p] = "!"
			matrix[row][col-p] = "!"
			matrix[row+i][col+p] = "!"
			matrix[row-i][col+p] = "!"
			matrix[row+i][col-p] = "!"
			matrix[row-i][col-p] = "!"
	matrix[row][col] = element
	return matrix

class Tile_Matrix:
	def __init__(self, rows, cols):
		self.rows = rows
		self.cols = cols
		self.matrix = []
		for i in range(cols):
			self.matrix.append(fill_row(rows))

	def change_matrix(self, row, col, element):
		self.matrix[row][col] = element


	def save(self):
		file_name = easygui.filesavebox('.txt','Save File as', '.txt')
		if file_name == None:
			return None
		file = open(file_name, 'w')
		for rows in self.matrix:
			line = ''
			for char in rows:
				for i in char:
					line += i
			line += '\n'
			file.write(line)
		file.close()

	def open_matrix(self, path):
		if path == ".":
			pass
		else:
			new_matrix = []
			file_matrix = [line.rstrip() for line in open(path, 'r')]
			for row in file_matrix:
				new_matrix.append(list(row))
		self.matrix = new_matrix

	def clear_matrix(self):
		self.matrix = []
		for i in range(self.cols):
			self.matrix.append(fill_row(self.rows))