import pygame
import math
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
from queue import PriorityQueue

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption("Pathfinding Algorithm")

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREY = (128, 128, 128)
END = (255, 0, 0)
START = (255, 22 ,148)
OPEN = (150, 241, 214)
CLOSED = (11, 46, 89)
PATH = (255, 255, 0)
BONUS = (163, 44, 196)

class Spot:
	def __init__(self, row, col, width, total_rows):
		self.row = row
		self.col = col
		self.x = row * width
		self.y = col * width
		self.color = WHITE
		self.neighbors = []
		self.width = width
		self.total_rows = total_rows

	def get_pos(self):
		return self.row, self.col

	def is_closed(self):
		return self.color == CLOSED

	def is_open(self):
		return self.color == OPEN

	def is_barrier(self):
		return self.color == BLACK

	def is_start(self):
		return self.color == START

	def is_end(self):
		return self.color == END

	def is_bonus(self):
		return self.color == BONUS

	def reset(self):
		self.color = WHITE

	def make_start(self):
		self.color = START

	def make_closed(self):
		self.color = CLOSED

	def make_open(self):
		self.color = OPEN

	def make_barrier(self):
		self.color = BLACK

	def make_end(self):
		self.color = END

	def make_bonus(self):
		self.color = BONUS

	def make_path(self):
		self.color = PATH

	def draw(self, win):
		pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

	def update_neighbors(self, grid):
		self.neighbors = []
		if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): # UP
			self.neighbors.append(grid[self.row - 1][self.col])

		if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): # LEFT
			self.neighbors.append(grid[self.row][self.col - 1])

		if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): # DOWN
			self.neighbors.append(grid[self.row + 1][self.col])

		if self.col < self.total_rows - 1 and not grid[self.row][self.col + 1].is_barrier(): # RIGHT
			self.neighbors.append(grid[self.row][self.col + 1])

	def __lt__(self, other):
		return False


def h(p1, p2):
	x1, y1 = p1
	x2, y2 = p2
	return abs(x1 - x2) + abs(y1 - y2)


def reconstruct_path(came_from, current, draw, start):
	while current in came_from:
		current = came_from[current]
		current.make_path()
		draw()
	start.make_start()


def astar(draw, grid, start, end, bonus_points):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	g_score = {spot: float("inf") for row in grid for spot in row}
	g_score[start] = 0
	f_score = {spot: float("inf") for row in grid for spot in row}
	f_score[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while not open_set.empty():
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw, start)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_g_score = g_score[current] + 1

			if temp_g_score < g_score[neighbor]:
				came_from[neighbor] = current
				g_score[neighbor] = temp_g_score
				f_score[neighbor] = temp_g_score + h(neighbor.get_pos(), end.get_pos())
				if bonus_points:
					if neighbor.get_pos() in bonus_points:
						f_score[neighbor] += bonus_points[neighbor.get_pos()]
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((f_score[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def Greedy(draw, grid, start, end, bonus_points):
	count = 0
	open_set = PriorityQueue()
	open_set.put((0, count, start))
	came_from = {}
	dis = {spot: float("inf") for row in grid for spot in row}
	dis[start] = h(start.get_pos(), end.get_pos())

	open_set_hash = {start}

	while open_set:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = open_set.get()[2]
		open_set_hash.remove(current)

		if current == end:
			reconstruct_path(came_from, end, draw, start)
			end.make_end()
			return True

		for neighbor in current.neighbors:
			temp_dis = dis[current]

			if temp_dis < dis[neighbor]:
				came_from[neighbor] = current
				dis[neighbor] = temp_dis
				if bonus_points:
					if neighbor.get_pos() in bonus_points:
						dis[neighbor] += bonus_points[neighbor.get_pos()]
				if neighbor not in open_set_hash:
					count += 1
					open_set.put((dis[neighbor], count, neighbor))
					open_set_hash.add(neighbor)
					neighbor.make_open()

		draw()

		if current != start:
			current.make_closed()

	return False


def DFS(draw, start, end):
	stack = []
	stack.append(start)
	came_from = {}
	while stack:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = stack.pop(len(stack) - 1)
		for neighbor in current.neighbors:
			if neighbor.is_end():
				current.make_closed()
				came_from[end] = current
				reconstruct_path(came_from, end, draw, start)
				return True

			elif not neighbor.is_closed() and not neighbor.is_start():
				neighbor.make_open()
				stack.append(neighbor)
				came_from[neighbor] = current

		draw()

		if current != start:
			current.make_closed()

	return False


def BFS(draw, start, end):
	queue = []
	queue.append(start)
	came_from = {}
	while queue:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()

		current = queue.pop(0)

		for neighbor in current.neighbors:
			if neighbor.is_end():
				current.make_closed()
				came_from[end] = current
				reconstruct_path(came_from, end, draw, start)
				return True

			elif not neighbor.is_closed() and not neighbor.is_open() and not neighbor.is_start():
				queue.append(neighbor)
				neighbor.make_open()
				came_from[neighbor] = current
		
		draw()

		if current != start:
			current.make_closed()
	
	return False


def make_grid(rows, width):
	grid = []
	gap = width // rows
	for i in range(rows):
		grid.append([])
		for j in range(rows):
			spot = Spot(i, j, gap, rows)
			grid[i].append(spot)

	return grid


def draw_grid(win, rows, width):
	gap = width // rows
	for i in range(rows):
		pygame.draw.line(win, GREY, (0, i * gap), (width, i * gap))
		for j in range(rows):
			pygame.draw.line(win, GREY, (j * gap, 0), (j * gap, width))


def draw(win, grid, rows, width):
	win.fill(WHITE)

	for row in grid:
		for spot in row:
			spot.draw(win)

	draw_grid(win, rows, width)
	pygame.display.update()


def get_clicked_pos(pos, rows, width):
	gap = width // rows
	y, x = pos

	row = y // gap
	col = x // gap

	return row, col

def open_file():
	file_path = filedialog.askopenfilename(initialdir=".\\")

	bonus_points = {}
	matrix = []

	file = open(file_path, 'r')
	n_bonus_points = int(next(file)[:-1])

	for i in range(n_bonus_points):
		x, y, reward = map(int, next(file)[:-1].split(' '))
		bonus_points[(x, y)] = reward

	text = file.read()
	matrix = [list(i) for i in text.splitlines()]
	file.close()
	
	return bonus_points, matrix

def main(win, width):
	ROWS = 50
	grid = make_grid(ROWS, width)

	messagebox.showinfo("Help", "F1 Help\nPress 1 to use DFS\nPress 2 to use BFS\nPress 3 to use Greedy\nPress 4 to use A*\nPress 5 to show current algorithm\nPress O to open a maze from file\nPress C to clear maze")

	bonus_points = {}
	mode = 'none'

	start = None
	end = None

	run = True
	while run:
		draw(win, grid, ROWS, width)
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				run = False

			if pygame.mouse.get_pressed()[0]: # LEFT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				if not start and spot != end:
					start = spot
					start.make_start()

				elif not end and spot != start:
					end = spot
					end.make_end()

				elif spot != end and spot != start:
					spot.make_barrier()

			elif pygame.mouse.get_pressed()[2]: # RIGHT
				pos = pygame.mouse.get_pos()
				row, col = get_clicked_pos(pos, ROWS, width)
				spot = grid[row][col]
				spot.reset()
				if spot == start:
					start = None
				elif spot == end:
					end = None

			elif pygame.mouse.get_pressed()[1]:
				point = simpledialog.askinteger("","Input bonus point")
				if point:
					pos = pygame.mouse.get_pos()
					row, col = get_clicked_pos(pos, ROWS, width)
					spot = grid[row][col]
					spot.make_bonus()
					bonus_points[spot.get_pos()] = point

			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_1:
					mode = 'DFS'

				if event.key == pygame.K_2:
					mode = 'BFS'

				if event.key == pygame.K_3:
					mode = 'Greedy'

				if event.key == pygame.K_4:
					mode = 'A*'

				if event.key == pygame.K_5:
					messagebox.showinfo("Current Algorithm", mode)
				
				if event.key == pygame.K_F1:
					messagebox.showinfo("Help", "F1 Help\nPress 1 to use DFS\nPress 2 to use BFS\nPress 3 to use Greedy\nPress 4 to use A*\nPress 5 to show current algorithm\nPress O to open a maze from file\nPress C to clear maze")

				if event.key == pygame.K_SPACE and start and end:
					for row in grid:
						for spot in row:
							spot.update_neighbors(grid)		

					if mode == 'DFS':
						DFS(lambda: draw(win, grid, ROWS, width), start, end)

					if mode == 'BFS':
						BFS(lambda: draw(win, grid, ROWS, width), start, end)

					if mode == 'Greedy':
						Greedy(lambda: draw(win, grid, ROWS, width), grid, start, end, bonus_points)

					if mode == 'A*':
						astar(lambda: draw(win, grid, ROWS, width), grid, start, end, bonus_points)

					if mode == 'none':
						messagebox.showwarning("Warning","You're not choosing any algorithm\nClose this and\nF1 Help\nPress 1 to use DFS\nPress 2 to use BFS\nPress 3 to use Greedy\nPress 4 to use A*\nPress 5 to show current algorithm\nPress O to open a maze from file\nPress C to clear maze")


				if event.key == pygame.K_o:
					if start or end: 
						start = None
						end = None
						grid = make_grid(ROWS, width)

					bonus_points, matrix = open_file()

					for i in range(len(matrix)):
						for j in range(len(matrix[0])):
							row, col = get_clicked_pos([j*16, i*16], ROWS, width)
							if matrix[i][j] == 'S':
								spot = grid[row][col]
								start = spot
								start.make_start()

							elif matrix[i][j] == '+':
								spot = grid[row][col]
								spot.make_bonus()

							elif matrix[i][j] == 'x':
								spot = grid[row][col]
								spot.make_barrier()

							elif matrix[0][j] == ' ' and i == 0:
								spot = grid[row][col]
								end = spot
								end.make_end()
							
							elif matrix[-1][j] == ' ' and i == len(matrix) - 1:
								spot = grid[row][col]
								end = spot
								end.make_end()

							elif matrix[i][0] == ' 'and j == 0:
								spot = grid[row][col]
								end = spot
								end.make_end()

							elif matrix[i][-1] == ' ' and j == len(matrix[0]) - 1:
								spot = grid[row][col]
								end = spot
								end.make_end()

				if event.key == pygame.K_c:
					start = None
					end = None
					grid = make_grid(ROWS, width)

	pygame.quit()

main(WIN, WIDTH)