from contextlib import nullcontext
from copy import copy
from pickle import TRUE
from queue import PriorityQueue
import pygame, sys, os
import pygame.camera
from pygame.locals import *
import math
import random
from handle_file_maze import *
from algorithm import algorithm_dfs, algorithm_bfs, algorithm_ucs, algorithm_greedy_bfs, algorithm_astar
from make_video import Video
import matplotlib.pyplot as plt
import copy
WIDTH = 800
HEIGHT = 600
FPS = 10

RED = (255, 0, 0)
GREEN = (144, 229, 150)
BLUE = (51, 143, 165)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)
BLACK = (56, 55, 56)
PURPLE = (175, 117, 173)
ORANGE = (234, 194 ,84)
GREY = (126,126,121)
TURQUOISE = (47, 66, 206)

# Build all need to visualization
"""
Description: Node is cell in matrix, it has another state with different color:
- White: Can go
- Black: Wall
- Orange: Start
- Turquoise: End
- Green: Process find way
- Purple: Correct way
- Yellow: Bonus point
"""
class Node:
    def __init__(self, row, col, size, total_rows, total_cols):
        self.costs = {}   #cost from this node to near node
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.bonus = 0
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.alpha = 255
        self.parents = []


    def change_alpha(self):
        if self.alpha > 100 and (self.color == GREEN or self.color == PURPLE):
            self.alpha = self.alpha - 20
    def get_pos(self):
        return self.row, self.col

    # It use in A* ~ I don't sure.
    def is_closed(self):
        return self.color == RED

    def is_open(self):
        return self.color == GREEN
    
    def is_wall(self):
        return self.color == BLACK

    def is_start(self):
        return self.color == ORANGE

    def is_end(self):
        return self.color == TURQUOISE

    def is_bonus(self):
        return self.color == YELLOW
    
    def is_pickups(self):
        return self.color == BLUE

    def reset(self):
        self.color = WHITE

    def make_start(self):
        self.color = ORANGE

    def make_open(self):
        if self.color != ORANGE and self.color != TURQUOISE and self.color != YELLOW and self.color != BLUE:
            self.color = GREEN
            self.alpha = 255
        else:
            self.alpha = 200
    
    # It use in A* ~ I don't sure.
    def make_closed(self):
        self.color = RED

    def make_wall(self):
        self.color = BLACK

    def make_end(self):
        self.color = TURQUOISE

    def make_bonus(self):
        self.color = YELLOW

    def make_pickups(self):
        self.color = BLUE
    
    def make_path(self):
        if self.color != ORANGE and self.color != TURQUOISE and self.color != YELLOW and self.color != BLUE:
            self.color = PURPLE
            self.alpha = 255
        else:
            self.alpha = 120

    def draw(self, screen):
        self.change_alpha()
        s = pygame.Surface((self.size, self.size))  # the size of your rect
        s.set_alpha(self.alpha)                # alpha level
        s.fill(self.color)           # this fills the entire surface
        screen.blit(s, (self.x, self.y))
        # pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def update_neighbors(self, grid):
        self.neighbors = []
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall(): # DOWN
            self.neighbors.append(grid[self.row + 1][self.col])
            self.costs[self.row + 1, self.col] = 1#random.randint(1,30)

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall(): # UP
            self.neighbors.append(grid[self.row - 1][self.col])
            self.costs[(self.row - 1), self.col] =1 #random.randint(1,30)

        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_wall(): # RIGHT
            self.neighbors.append(grid[self.row][self.col + 1])
            self.costs[self.row, (self.col + 1)] = 1#random.randint(1,30)

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall(): # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
            self.costs[self.row, (self.col-1)] = 1#random.randint(1,30)
    
    def __lt__(self, other):
        return False

def make_grid(rows, cols):
    grid = []
    for i in range(rows):
        grid.append([])
        for j in range(cols):
            node = Node(i, j, SIZE, rows, cols)
            
            grid[i].append(node)

    return grid

def draw_grid(screen, rows, cols, width, height):
    for i in range(rows):
        pygame.draw.line(screen, GREY, (0, i * SIZE), (width, i * SIZE))
        for j in range(cols):
            pygame.draw.line(screen, GREY, (j * SIZE, 0), (j * SIZE, height))

def draw(screen, grid, rows, cols, width, height):
    screen.fill(WHITE)
    
    for row in grid:
        for node in row:
            node.draw(screen)
    
    draw_grid(screen, rows, cols, width, height)
    video.make_png(screen)

    pygame.display.update()

def merge_maze_grid(maze, grid, ROWS,COLS):

    start = None
    end = None

    for i in range(ROWS):
        for j in range(COLS):
            node = grid[i][j]
            if(maze[i][j] == 'S' or maze[i][j] == '*'):
                start = node
                start.make_start()
            elif maze[i][j] == ' ':
                if (i==0) or (i==len(maze)-1) or (j==0) or (j==len(maze[0])-1):
                    end = node
                    end.make_end()
            else:
                node.make_wall()
    
    return start, end

def merge_bonus_grid(bonus_points, grid):
    # Sẽ sử dụng priority queue để lưu danh sách các điểm thưởng, điểm thưởng sẽ được chuyển thành dương để dễ lưu
    bonus_queue = PriorityQueue()
    i = 0
    for point in bonus_points:
        bonus_queue.put((point[2], (point[0], point[1])))
        grid[point[0]][point[1]].make_bonus()
        grid[point[0]][point[1]].bonus = point[2]
        i += 1
    
    print(i)
    return bonus_queue

def merge_pickups_grid(pickup_points, grid):
    # Sẽ sử dụng priority queue để lưu danh sách các điểm thưởng, điểm thưởng sẽ được chuyển thành dương để dễ lưu
    pickups_queue = PriorityQueue()

    for point in pickup_points:
        pickups_queue.put(((point[0], point[1])))
        grid[point[0]][point[1]].make_pickups()
        grid[point[0]][point[1]].bonus = 0

    return pickups_queue
#lưu đường đi ra khỏi mê cung thành file .png
def visualize_maze_by_image(matrix, bonus, start, end, route: list,saveDir = None):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    route.reverse()
    route.append(start.get_pos())
    route.reverse()
    route.append(end.get_pos())
    walls=[(i,j) for i in range(len(matrix)) for j in range(len(matrix[0])) if matrix[i][j]=='x']

    if route:
        direction=[]
        for i in range(1,len(route)):
            if route[i][0]-route[i-1][0]>0:
                direction.append('v') #^
            elif route[i][0]-route[i-1][0]<0:
                direction.append('^') #v        
            elif route[i][1]-route[i-1][1]>0:
                direction.append('>')
            else:
                direction.append('<')

        direction.pop(0)

    #2. Drawing the map
    ax=plt.figure(dpi=100).add_subplot(111)

    for i in ['top','bottom','right','left']:
        ax.spines[i].set_visible(False)

    plt.scatter([i[1] for i in walls],[-i[0] for i in walls],
                marker='X',s=100,color='black')
    if(not bonus.empty()):
        plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                    marker='P',s=100,color='green')

    plt.scatter(start.col,-start.row,marker='*',
                s=100,color='gold')

    if route:
        for i in range(len(route)-2):
            plt.scatter(route[i+1][1],-route[i+1][0],
                        marker=direction[i],color='silver')

    plt.text(end.col,-end.row,'EXIT',color='red',
         horizontalalignment='center',
         verticalalignment='center')
    plt.xticks([])
    plt.yticks([])
    plt.savefig(saveDir + ".png")
    


def run():
    levels, files = list_file()

    
    for level in levels:
        for file in files[level]:
            maze, bonus_points, pickup_point = read_file("./input/" + level + "/" + file)
            
            ROWS = len(maze)
            COLS = len(maze[0])
            WIDTH = COLS * SIZE
            HEIGHT = ROWS * SIZE
            way = []
            cost = 0
            start = None
            end = None

            algs = ["dfs","bfs","ucs","gbfs","astar"]
            for alg in algs:
                grid = make_grid(ROWS, COLS)
                start, end = merge_maze_grid(maze, grid,ROWS,COLS)
                bonus_queue = merge_bonus_grid(bonus_points, grid)
                for row in grid:
                    for node in row:
                        node.update_neighbors(grid)            
                
                SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
                if level == "level_1":
                    if(alg == "dfs"):
                        way, cost = algorithm_dfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                    elif(alg== "bfs"):
                        way,cost = algorithm_bfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                    elif(alg == "ucs"):
                        way, cost = algorithm_ucs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                    elif(alg == "gbfs"):
                        way, cost =algorithm_greedy_bfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                    else:
                        way, cost = algorithm_astar(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                elif level == "level_2":
                    temp="level_2"
                elif level == "level_3":
                    temp="level_3"
                elif level == "advance":
                    temp="advance"
                dir_output = level + "\\" + file.split(".")[0] + "\\" + alg
                create_folder(dir_output)               
                write_file(dir_output + "\\" + alg + ".txt", cost )
                video.make_mp4(dir_output+ "\\" + alg)
                video.destroy_png()
                visualize_maze_by_image(maze,bonus_queue,start,end,way,DIR_OUTPUT + dir_output + "\\" + alg )
                pygame.quit()
               


            


"""
Start simulation
"""

# bonus_points, maze = read_file("./maze/maze_3.txt")

# ROWS = len(maze)
# COLS = len(maze[0])

SIZE = 32

# WIDTH = COLS * SIZE
# HEIGHT = ROWS * SIZE

# print(WIDTH, HEIGHT)

# SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
video = Video((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation of finding the way")
clock = pygame.time.Clock()

#main(SCREEN, maze, bonus_points, WIDTH, HEIGHT)
run()
#Build video from image.
# video.make_mp4("maze")
#video.destroy_png()

