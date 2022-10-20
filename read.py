def read_file_advance(file_name: str = 'maze.txt'):
  f = open(file_name,'r')
  n_points = int(next(f)[:-1])
  points = []
  portals = {}
  
  
  for i in range(n_points):
    line = next(f)[:-1]
    print(len(line.split(' ')))
  
  bonus_points = []
  pickup_points = []

  for point in points:
    if point[2] == 0:
      pickup_points.append((point[0], point[1]))
    else:
      bonus_points.append((point[0], point[1], point[2]))

  for i in range(n_portal):
    pos1, pos2 = map(str, next(f)[:-1].split('-'))    
    x1, y1 = map(int, pos1.split(' '))
    x2, y2 = map(int, pos2.split(' '))
    portals[(x1, y1)] = (x2, y2)
    portals[(x2, y2)] = (x1, y1)
    
  text=f.read()
  maze=[list(i) for i in text.splitlines()]
  f.close()

  return maze, bonus_points, pickup_points, portals


read_file_advance("./maze/maze_6.txt")