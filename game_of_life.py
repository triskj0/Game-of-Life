"""
John Conway's game of life

rules:
1) SOLITUDE - a cell with one or no neighbors dies
2) OVERPOPULATION - a cell with four or more neighbors dies
3) HARMONY - a cell with two or three neighbors survives
4) NEW LIFE - cell with three neighbors becomes populated

"""

import pygame

# creating a pygame widow
WIDTH = 720
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Game of Life")

WHITE = (255, 255, 255)
GREEN = (25, 252, 93)
GREY = (128, 128, 128)

pygame.init()
clock = pygame.time.Clock()
FPS = 8


class Cell:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.width = width
		self.color = WHITE
		self.alive_neighbors = []
		self.total_rows = total_rows

	def make_alive(self):
		self.color = GREEN

	def make_dead(self):
		self.color = WHITE

	def is_alive(self):
		return self.color == GREEN

	def is_dead(self):
		return self.color == WHITE

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.alive_neighbors = []

		# down
		if self.row < self.total_rows - 1 and grid[self.row + 1][self.col].is_alive():
			self.alive_neighbors.append(grid[self.row + 1][self.col])

		# up
		if self.row > 0 and grid[self.row - 1][self.col].is_alive():
			self.alive_neighbors.append(grid[self.row - 1][self.col])
	
		# left
		if self.col < self.total_rows - 1 and grid[self.row][self.col + 1].is_alive():
			self.alive_neighbors.append(grid[self.row][self.col + 1])

		# right
		if self.col > 0 and grid[self.row][self.col - 1].is_alive():
			self.alive_neighbors.append(grid[self.row][self.col - 1])

		# upper left corner
		if self.row > 0 and self.col > 0 and grid[self.row-1][self.col-1].is_alive():
			self.alive_neighbors.append(grid[self.row-1][self.col-1])

		# upper right corner
		if self.row > 0 and self.col < self.total_rows-1 and grid[self.row-1][self.col+1].is_alive():
			self.alive_neighbors.append(grid[self.row-1][self.col+1])

		# lower left corner
		if self.row < self.total_rows-1 and self.col > 0 and grid[self.row+1][self.col-1].is_alive():
			self.alive_neighbors.append(grid[self.row+1][self.col-1])

		# lower right corner
		if self.row < self.total_rows-1 and self.col < self.total_rows-1 and grid[self.row+1][self.col+1].is_alive():
			self.alive_neighbors.append(grid[self.row+1][self.col+1])


def make_grid(total_rows, width):
	grid = []
	gap = width // total_rows

	for i in range(total_rows):
		grid.append([])
		for j in range(total_rows):
			cell = Cell(i, j, gap, total_rows)
			grid[i].append(cell)

	return grid


def draw_grid_lines(win, rows, width):
	gap = width // rows

	# drawing horizontal lines
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))

	# drawing vertical lines
	for j in range(rows):
		pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	# draw cells
	for row in grid:
		for cell in row:
			cell.draw(win)

	# draw grid lines
	draw_grid_lines(win, rows, width)
	pygame.display.update() # update the pygame window


def get_clicked_position(pos, rows, width):
	gap = width // rows # the width of each cell
	y, x = pos # mouse position

	row = y // gap
	col = x // gap

	return row, col # returning the row and column that was clicked


def update_cells(grid, total_rows, fps):
	cells_to_kill = []
	living_cells = []

	for row in range(total_rows):
		for col in range(total_rows):
			cell = grid[row][col]
			cell.update_neighbors(grid)

			# NEW LIFE - cell with three neighbors comes alive
			if len(cell.alive_neighbors) == 3 and cell.is_dead:
				living_cells.append(cell)
			# OVERPOPULATION - a cell with four or more neighbors dies
			if len(cell.alive_neighbors) > 3:
				cells_to_kill.append(cell)
			# SOLITUDE - a cell with one or no neighbors dies
			if len(cell.alive_neighbors) < 2:
				cells_to_kill.append(cell)
			# HARMONY - a cell with two or three neighbors survives

	for cell in cells_to_kill:
		cell.make_dead()
	for cell in living_cells:
		cell.make_alive()

	clock.tick(fps)


def main(win, width, fps):
	space_count = 0
	ROWS = 60
	grid = make_grid(ROWS, width)

	run = True
	while run:
		draw(win, grid, ROWS, width)
		if space_count % 2 != 0:
			update_cells(grid, ROWS, fps)

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # if we left click:
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, ROWS, width)
				cell = grid[row][col]
				cell.make_alive()

			elif pygame.mouse.get_pressed()[2]: # if we right click
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_position(pos, ROWS, width)
				cell = grid[row][col]
				cell.make_dead()

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_SPACE:
					space_count += 1

				if event.key == pygame.K_c:
					grid = make_grid(ROWS, width)
					for row in range(ROWS):
						for col in range(ROWS):
							cell = grid[row][col]
							cell.make_dead()


if __name__ == '__main__':
	main(WIN, WIDTH, FPS)
