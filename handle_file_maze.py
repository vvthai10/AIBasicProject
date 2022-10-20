from importlib.resources import path
import os


def read_file(file_name: str = 'maze.txt'):
  f=open(file_name,'r')
  # n_bonus_points, n_pickup_points, n_portal = map(int, next(f)[:-1].split(' '))
  n_points, n_portal = map(int, next(f)[:-1].split(' '))
  points = []
  portals = {}
  for i in range(n_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    points.append((x, y, reward))

  # for i in range(n_pickup_points):
  #   x, y = map(int, next(f)[:-1].split(' '))
  #   pickup_points.append((x, y))

  
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

