def read_file(file_name: str = 'maze.txt'):
  f=open(file_name,'r')
  n_bonus_points, n_pickup_points = map(int, next(f)[:-1].split(' '))
  bonus_points = []
  pickup_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))

  for i in range(n_pickup_points):
    x, y = map(int, next(f)[:-1].split(' '))
    pickup_points.append((x, y))

  text=f.read()
  maze=[list(i) for i in text.splitlines()]
  f.close()

  return maze, bonus_points, pickup_points