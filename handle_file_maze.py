from importlib.resources import path
import os


def read_file(file_name: str = 'maze.txt'):
  f=open(file_name,'r')
  n_bonus_points = int(next(f)[:-1])
  bonus_points = []
  for i in range(n_bonus_points):
    x, y, reward = map(int, next(f)[:-1].split(' '))
    bonus_points.append((x, y, reward))

  text=f.read()
  matrix=[list(i) for i in text.splitlines()]
  f.close()

  return bonus_points, matrix
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

