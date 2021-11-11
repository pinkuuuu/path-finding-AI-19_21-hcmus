#import visualize
import pygame
from queue import PriorityQueue

def DFS(draw, start): #draw is class Node's draw function
    stack = []
    stack.append([start]) # stack stores the whole path instead of nodes
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
        path = stack.pop(-1)
        current = path[-1]
        if current.is_end():
            for node in path:
                node.make_path()
            return True         
        if current.is_open():
            current.make_visited()
        for neighbor in current.neighbors:
            if not neighbor.is_barrier() and not neighbor.is_visited() and not neighbor.is_start():
                new_path = list(path)
                new_path.append(neighbor)
                stack.append(new_path)
                if not neighbor.is_end():
                    neighbor.make_open()
        
        draw()

    return False

def BFS(draw, start): #draw is class Node's draw function
    queue = []
    queue.append([start]) # queue stores the whole path instead of nodes
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        path = queue.pop(0)
        current = path[-1]
        if current.is_end():
            for node in path:
                node.make_path()
            return True
        if current.is_open():
            current.make_visited()
        for neighbor in current.neighbors:
            if not neighbor.is_barrier() and not neighbor.is_visited() and not neighbor.is_start() and not neighbor.is_open():
                new_path = list(path)
                new_path.append(neighbor)
                queue.append(new_path)
                if not neighbor.is_end():
                    neighbor.make_open()

        draw()
        
    return False

def h(p1, p2): # heuristic function (Manhattan distance)
    x1, y1 = p1
    x2, y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def greedy(draw, grid, start, end):
    count = 0 # if there's 2 equal f_score we priority the one came in first
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # open_set stores (f_score, insert order, node)
    came_from = {} # dictionary keep track of path
    f_score = {node: float("inf") for row in grid for node in row} # f_score = heuristic(mentioned node -> end node)
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} # bcuz you cant keep track of what's in a Priority queue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] # indexing 2 to get the node itself
        open_set_hash.remove(current)
        if current.is_end():
            current.make_path()
            while current in came_from:
                current = came_from[current]
                current.make_path()
            return True
        if current.is_open():
            current.make_visited()
        for neighbor in current.neighbors:
            if not neighbor.is_visited() and not neighbor.is_start():    
                if neighbor.is_bonus():
                    f_score[neighbor] = h(neighbor.get_pos(), end.get_pos()) - 1
                else:
                    f_score[neighbor] = h(neighbor.get_pos(), end.get_pos())
                came_from[neighbor] = current
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_end():
                        neighbor.make_open()

        draw()

    return False

def astar(draw, grid, start, end):
    count = 0 # if there's 2 equal f_score we priority the one came in first
    open_set = PriorityQueue()
    open_set.put((0, count, start)) # open_set stores (f_score, insert order, node)
    came_from = {} # dictionary keep track of path
    g_score = {node: float("inf") for row in grid for node in row} # g_score = distance from start to the mentioned node
    g_score[start] = 0
    f_score = {node: float("inf") for row in grid for node in row} # f_score = g_score + heuristic(mentioned node -> end node)
    f_score[start] = h(start.get_pos(), end.get_pos())

    open_set_hash = {start} # bcuz you cant keep track of what's in a Priority queue

    while not open_set.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = open_set.get()[2] # indexing 2 to get the node itself
        open_set_hash.remove(current)
        if current.is_end():
            current.make_path()
            while current in came_from:
                current = came_from[current]
                current.make_path()
            return True
        
        for neighbor in current.neighbors:
            if neighbor.is_bonus():
                temp_g_score = g_score[current]
            else:
                temp_g_score = g_score[current] + 1

            if temp_g_score < g_score[neighbor]: # indicating that there's a better path to this neighbor node
                g_score[neighbor] = temp_g_score
                f_score[neighbor] = g_score[neighbor] + h(neighbor.get_pos(), end.get_pos())
                came_from[neighbor] = current
                if neighbor not in open_set_hash:
                    count += 1
                    open_set.put((f_score[neighbor], count, neighbor))
                    open_set_hash.add(neighbor)
                    if not neighbor.is_end():
                        neighbor.make_open()

        draw()

        if current.is_open():
            current.make_visited()

    return False
