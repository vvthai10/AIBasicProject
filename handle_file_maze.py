from importlib.resources import path
import os


def read_file(file_name: str = 'maze.txt'):
  f = open(file_name,'r')
  n_points = int(next(f)[:-1])
  points = []
  portals = {}
  
  print(f"points: {n_points}")
  for i in range(n_points):
    line = next(f)[:-1]
    if len(line.split(' ')) == 3:
      x, y, reward = map(int, line.split(' '))
      points.append((x, y, reward))
    else:
      x1, y1, x2, y2 = map(int, line.split(' '))
      portals[(x1, y1)] = (x2, y2)
      portals[(x2, y2)] = (x1, y1)
      
  
  bonus_points = []
  pickup_points = []

  for point in points:
    if point[2] == 0:
      pickup_points.append((point[0], point[1]))
    else:
      bonus_points.append((point[0], point[1], point[2]))
     
  text=f.read()
  maze=[list(i) for i in text.splitlines()]
  f.close()

  return maze, bonus_points, pickup_points, portals



def write_file(file_name, cost = 0):
    f = open(DIR_OUTPUT + file_name,'w')
    f.write(str(cost))
    f.close()

DIR_INPUT = "./input/"
def list_file():
  #tất cả các folder trong input : level1,level2,...
  dir_list = os.listdir(DIR_INPUT)
  files = {} # chứa tên file trong các folder:  files[level1] = ['input1.txt','input2.txt',...]
  for level in dir_list:
    files[level] = os.listdir(DIR_INPUT + level)
  
  return dir_list, files

DIR_OUTPUT = "./output/"
def create_folder(directory):
  if(not os.path.exists(DIR_OUTPUT + directory)):
    os.makedirs(DIR_OUTPUT + directory)
