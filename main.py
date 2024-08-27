from random import seed, choice, sample


class Cell:
	def __init__(self, row, column):
		self.coord = (row, column)
		self.visited = False
	
	@property
	def topGap(self):
		r, c = self.coord
		return (r*2, c*2+1)

	@property
	def rightGap(self):
		r, c = self.coord
		return (r*2+1, c*2+2)

	@property
	def bottomGap(self):
		r, c = self.coord
		return (r*2+2, c*2+1)
	
	@property
	def leftGap(self):
		r, c = self.coord
		return (r*2+1, c*2)
	
	@property
	def neighbors(self):
		r, c = self.coord
		return [(r-1, c), (r, c+1), (r+1, c), (r, c-1)]
	
	def gapTo(self, n):
		r, c = self.coord
		rn, cn = n
		if r-rn != 0:
			if r-rn < 0:
				return self.bottomGap
			else:
				return self.topGap
		else:
			if c-cn < 0:
				return self.rightGap
			else:
				return self.leftGap
	
	def __str__(self):
		return str(self.coord)


class Maze:
	def __init__(self, rows, columns, customSeed=None):
		self._cells = {}
		self._gaps = []
		self._solution = []
		self.nRows, self.nColumns = rows, columns
		if customSeed:
			seed(customSeed)
		for r in range(rows):
			for c in range(columns):
				self._cells[(r, c)] = Cell(r, c)
		self.generate()
		self._resetVisited()
	
	def _resetVisited(self):
		for c in self._cells.values():
			c.visited = False

	def getCell(self, row, col):
		return self._cells[(row, col)]
	
	def generate(self, cell=None):
		if cell is None:
			cell = choice(list(self._cells.values()))
		cell.visited = True
		for n in sample(cell.neighbors, 4):
			if n in self._cells and not self._cells[n].visited:
				self._gaps.append(cell.gapTo(n))
				self.generate(self._cells[n])

	def solve(self, fromCell=None, toCell=None):
		if fromCell is None:
			fromCell = self.getCell(0, 0)
		if toCell is None:
			toCell = self.getCell(self.nRows-1, self.nColumns-1)
		fromCell.visited = True
		if fromCell is toCell:
			self._solution = [fromCell.coord]
			self._resetVisited()
			return True
		else:
			for n in fromCell.neighbors:
				if n in self._cells and fromCell.gapTo(n) in self._gaps and not self._cells[n].visited:
					if self.solve(self._cells[n], toCell):
						self._solution.insert(0, fromCell.coord)
						return True
			return False

	
	def __str__(self):
		maze_field = ""
		for r in range(self.nRows*2 + 1):
			for c in range(self.nColumns*2 + 1):
				if r%2:
					if c%2:
						maze_field += " . " if (r//2, c//2) in self._solution else "   "
					else:
						maze_field += " " if (r, c) in self._gaps else "|"
				else:
					if c%2:
						maze_field += "   " if (r, c) in self._gaps else "---"
					else:
						maze_field += "+"
			maze_field += "\n"
		return maze_field


def main():
	m = Maze(8, 8);
	m.solve()
	print(m)


if __name__ == "__main__":
    main()
