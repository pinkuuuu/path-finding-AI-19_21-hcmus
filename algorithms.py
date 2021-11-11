#import visualize
import pygame

def DFS(draw, start): #draw is class Node's draw function
    stack = []
    stack.append([start])
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
    queue.append([start])
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