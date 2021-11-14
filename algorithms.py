def DFS(cur, end, walls, direction, route, visited):
  if route[len(route)-1] == end:
    return route
  
  for k in direction:
    next = tuple(map(lambda i, j: i + j, cur, k))
    if (next not in walls) and (next not in visited):
      route.append(next)
      visited.append(next)
      route = DFS(next, end, walls, direction, route, visited)
      if route[len(route)-1] == end:
        break
      route.pop(len(route)-1)
  return route

def BFS(start, end, walls, direction):
  frontier = [start]
  visited = [start]
  tracker = {start: start}
  check = 0
  while len(frontier) > 0:
    cur = frontier.pop(0)
    for k in direction:
      next = tuple(map(lambda i, j: i + j, cur, k))
      if (next not in walls) and (next not in visited):
        tracker[next] = cur
        if next == end:
          check = 1
          break
        frontier.append(next)
        visited.append(next)
    if check == 1:
      break

  track = end
  route = [end]
  while track != (start):
    track = tracker[track]
    route.append(track)
  
  route.reverse()
  return route

class node:
  def __init__(self, start, cur, end, mode, bonus_points):
    self.cur = cur
    if mode == 'Greedy':
      self.dis = abs(cur[0] - end[0]) + abs(cur[1] - end[1])
    elif mode == 'Astar':
      self.dis = abs(cur[0] - start[0]) + abs(cur[1] - start[1]) + abs(cur[0] - end[0]) + abs(cur[1] - end[1])
    
    if cur in bonus_points:
      self.dis += bonus_points[cur]

  def __lt__(self, other):
    return self.dis < other.dis

def Greedy(start, end, walls, direction, bonus_points):
  frontier = [node(start, start, end, 'Greedy', bonus_points)]
  visited = [start]
  tracker = {start: start}
  check = 0
  while len(frontier) > 0:
    cur = frontier.pop(0).cur
    for k in direction:
      next = tuple(map(lambda i, j: i + j, cur, k))
      if (next not in walls) and (next not in visited):
        tracker[next] = cur
        if next == end:
          check = 1
          break
        frontier.append(node(start, next, end, 'Greedy', bonus_points))
        visited.append(next)
    
    frontier.sort()
    if check == 1:
      break

  track = end
  route = [end]
  while track != (start):
    track = tracker[track]
    route.append(track)
  
  route.reverse()
  return route

def AStar(start, end, walls, direction, bonus_points):
  frontier = [node(start, start, end, 'Astar', bonus_points)]
  visited = [start]
  tracker = {start: start}
  check = 0
  while len(frontier) > 0:
    cur = frontier.pop(0).cur
    for k in direction:
      next = tuple(map(lambda i, j: i + j, cur, k))
      if (next not in walls) and (next not in visited):
        tracker[next] = cur
        if next == end:
          check = 1
          break
        frontier.append(node(start, next, end, 'Astar', bonus_points))
        visited.append(next)
    
    frontier.sort()
    if check == 1:
      break

  track = end
  route = [end]
  while track != (start):
    track = tracker[track]
    route.append(track)
  
  route.reverse()
  return route