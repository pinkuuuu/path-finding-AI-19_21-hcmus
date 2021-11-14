def read_file(file_name):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = {}
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points[(x, y)] = reward

  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()

  return bonus_points, matrix