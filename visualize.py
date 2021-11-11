import pygame
from pygame.event import get
import algorithms as pathfinding

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
GREEN = (0, 255, 0)

class Node:
    def __init__(self, row, col, width, total_rows, total_cols):
        self.row = row
        self.col = col
        self.x = row * width
        self.y = col * width
        self.color = WHITE
        self.neighbors = []
        self.width = width
        self.total_rows = total_rows
        self.total_cols = total_cols
    
    def get_pos(self):
        return self.row, self.col
    
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
    
    def reset(self):
        self.color = WHITE

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
            node = Node(i, j, gap, rows, cols)
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

def main(win, width):
    ROWS = 50
    grid = make_grid(ROWS, ROWS, width)

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

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not started:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    #pathfinding.DFS(lambda: draw(win, grid, ROWS, ROWS, width), start)

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_r and not started:
                    for row in grid:
                        for node in row:
                            node.reset()
    pygame.quit()

main(WIN, WIDTH)