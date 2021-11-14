import os
import readfile
import algorithms
import visualize
import sys

print(sys.argv)

bonus_points, matrix = readfile.read_file(sys.argv[1])
walls = [(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']
direction = [(-1,0), (0,-1), (1,0), (0,1)]

print(f'The height of the matrix: {len(matrix)}')
print(f'The width of the matrix: {len(matrix[0])}')

for i in range(len(matrix)):
    for j in range(len(matrix[0])):
        if matrix[i][j]=='S':
            start=(i,j)

        elif matrix[i][j]==' ':
            if (i==0) or (i==len(matrix)-1) or (j==0) or (j==len(matrix[0])-1):
                end=(i,j)
                
        else:
            pass

if sys.argv[2] == 'DFS':
    route = algorithms.DFS(start, end, walls, direction, [start], [start])
elif sys.argv[2] == 'BFS':
    route = algorithms.BFS(start, end, walls, direction)
elif sys.argv[2] == 'Greedy':
    route = algorithms.Greedy(start, end, walls, direction, bonus_points)
elif sys.argv[2] == 'AStar':
    route = algorithms.AStar(start, end, walls, direction, bonus_points)


visualize.visualize_maze(matrix, bonus_points, start, end, route)