import pygame
from pygame.event import get
import algorithms as pathfinding
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import messagebox

WIDTH = 800
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("Pathfinding Algorithms")

YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
PURPLE = (128, 0, 128)
GREY = (128, 128, 128)
CYAN = (0,255,255)
RED = (255, 0, 0)
AZURE = (0, 128, 255)
GREEN = (3, 172, 19)
LOSS = (163, 44, 196)
BONUS = (242, 107, 138)

class Node:
    def __init__(self, row, col, width, point, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.point = point
        self.total_rows = total_rows
        self.total_cols = total_cols
    
    def get_pos(self):
        return self.col, self.row

    def get_point(self):
        return self.point

    def set_point(self, point):
        self.point = point
    
    def is_visited(self):
        return self.color == CYAN
    
    def is_open(self):
        return self.color == AZURE
    
    def is_barrier(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == GREEN
    
    def is_end(self):
        return self.color == RED

    def is_bonus(self):
        return self.color == BONUS

    def is_loss(self):
        return self.color == LOSS
    
    def reset(self):
        self.color = WHITE
        self.point = 1

    def make_visited(self):
        self.color = CYAN
    
    def make_open(self):
        self.color = AZURE

    def make_barrier(self):
        self.color = BLACK
    
    def make_start(self):
        self.color = GREEN
    
    def make_end(self):
        self.color = RED

    def make_bonus(self):
        self.color = BONUS

    def make_loss(self):
        self.color = LOSS

    def make_path(self):
        self.color = YELLOW
    
    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.width))

    def update_neighbors(self,grid):
        self.neighbors = []

        if self.row > 0 and not grid[self.row - 1][self.col].is_barrier(): #UP
            self.neighbors.append(grid[self.row - 1][self.col]) 

        if self.col > 0 and not grid[self.row][self.col - 1].is_barrier(): #LEFT
            self.neighbors.append(grid[self.row][self.col - 1])

        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_barrier(): #DOWN
            self.neighbors.append(grid[self.row + 1][self.col])

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_barrier(): #RIGHT
            self.neighbors.append(grid[self.row][self.col + 1]) 

    def __lt__(self, other):
        return False

def make_grid(rows, cols, width):
    grid = []
    gap = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(i, j, gap, 1, rows, cols)
            grid[i].append(node)
    
    return grid

def draw_grid(win, rows, cols, width):
    gap = width // rows
    for i in range(rows):
        pygame.draw.line(win, GREY, (0, i*gap), (width, i*gap))
        for j in range(cols):
            pygame.draw.line(win, GREY, (j*gap,0), (j*gap, width))
    
def draw(win, grid, rows, cols, width):
    win.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(win)

    draw_grid(win, rows, cols, width)
    pygame.display.update()

def get_clicked_pos(pos, rows, width):
    gap = width // rows
    x,y = pos

    row = x // gap
    col = y // gap

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
    ROWS = 23
    grid = make_grid(ROWS, ROWS, width)

    messagebox.showinfo("Help", "F1 Help\nPress 1 to use DFS\nPress 2 to use BFS\nPress 3 to use Greedy\nPress 4 to use A*\nPress 5 to show current algorithm\nPress O to open a maze from file\nPress R to clear maze")

    bonus_points = {}
    mode = 'none'

    start = None
    end = None

    run = True
    started = False
    while run:
        draw(win, grid, ROWS, ROWS, width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if started:
                continue

            if pygame.mouse.get_pressed()[0]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]

                if not start and node != end:
                    start = node
                    start.make_start()

                elif not end and node != start:
                    end = node
                    end.make_end()
                
                elif node != end and node != start:
                    node.make_barrier()

            elif pygame.mouse.get_pressed()[2]:
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos, ROWS, width)
                node = grid[row][col]
                node.reset()

                if node == start:
                    start = None
                elif node == end:
                    end = None
                    
            elif pygame.mouse.get_pressed()[1]:
                pos = pygame.mouse.get_pos()
                point = simpledialog.askinteger("","Input bonus point")
                if point:
                    row, col = get_clicked_pos(pos, ROWS, width)
                    node = grid[row][col]
                    node.set_point(point)

                if point == 0:
                    return True

                elif point < 0:
                    node.make_bonus()

                elif point > 0:
                    node.make_loss()
            
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
                    messagebox.showinfo("Help", "F1 Help\nPress 1 to use DFS\nPress 2 to use BFS\nPress 3 to use Greedy\nPress 4 to use A*\nPress 5 to show current algorithm\nPress O to open a maze from file\nPress R to clear maze")

                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                
                    if mode == 'DFS':
                        pathfinding.DFS(lambda: draw(win, grid, ROWS, ROWS, width), start, end)

                    if mode == 'BFS':
                        pathfinding.BFS(lambda: draw(win, grid, ROWS, ROWS, width), start, end)

                    if mode == 'Greedy':
                        pathfinding.greedy(lambda: draw(win, grid, ROWS, ROWS, width), grid, start, end)

                    if mode == 'A*':
                        pathfinding.astar(lambda: draw(win, grid, ROWS, ROWS, width), grid, start, end)

                    if mode == 'none':
                        messagebox.showwarning("Warning","You're not choosing any algorithm\nClose this and\nF1 Help\nPress 1 to use DFS\nPress 2 to use BFS\nPress 3 to use Greedy\nPress 4 to use A*\nPress 5 to show current algorithm\nPress O to open a maze from file\nPress R to clear maze")


                if event.key == pygame.K_o:
                    if start or end: 
                        start = None
                        end = None
                        grid = make_grid(ROWS, ROWS, width)

                    bonus_points, matrix = open_file()

                    for i in range(len(matrix)):
                        for j in range(len(matrix[0])):
                            # row, col = get_clicked_pos([j*16, i*16], ROWS, width)
                            if matrix[i][j] == 'S':
                                node = grid[j][i]
                                start = node
                                start.make_start()

                            elif matrix[i][j] == '+':
                                node = grid[j][i]
                                node.set_point(bonus_points[(i, j)])

                                if bonus_points[node.get_pos()] < 0:
                                    node.make_bonus()

                                if bonus_points[node.get_pos()] > 0:
                                    node.make_loss()

                            elif matrix[i][j] == 'x':
                                node = grid[j][i]
                                node.make_barrier()

                            elif matrix[0][j] == ' ' and i == 0:
                                node = grid[j][i]
                                end = node
                                end.make_end()

                            elif matrix[-1][j] == ' ' and i == len(matrix) - 1:
                                node = grid[j][i]
                                end = node
                                end.make_end()

                            elif matrix[i][0] == ' ' and j == 0:
                                node = grid[j][i]
                                end = node
                                end.make_end()

                            elif matrix[i][-1] == ' ' and j == len(matrix[0]) - 1:
                                node = grid[j][i]
                                end = node
                                end.make_end()

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not started:
                    for row in grid:
                        for node in row:
                            node.reset()
                            if node == start:
                                start = None
                            elif node == end:
                                end = None
    pygame.quit()

main(WIN, WIDTH)