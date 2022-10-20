from contextlib import nullcontext
from pickle import TRUE
from queue import PriorityQueue, Queue
from typing import List
import pygame
import sys
import pygame.camera
from pygame.locals import *
from handle_file_maze import *
from algorithm import algorithm_bonus_astar, algorithm_bonus_pickup_astar, algorithm_dfs, algorithm_bfs, algorithm_ucs, algorithm_greedy_bfs, algorithm_astar
from make_video import Video
import matplotlib.pyplot as plt
from handle_file_maze import *
import algorithm as algo
from make_video import Video
import utility as util
from utility import SIZE as SIZE

WIDTH = 800
HEIGHT = 600
FPS = 10

RED = (255, 0, 0)
GREEN = (144, 229, 150)
BLUE = (158, 219, 227)
YELLOW = (255, 255, 0)  # meaning?
WHITE = (255, 255, 255)
BLACK = (56, 55, 56)
PURPLE = (175, 117, 173)
ORANGE = (234, 194, 84)
GREY = (126, 126, 121)
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
        self.costs = {}  # cost from this node to near node
        self.row = row
        self.col = col
        self.x = col * size
        self.y = row * size
        self.color = WHITE
        self.neighbors = []
        self.size = size
        self.bonus = 0  # always negative or 0
        self.total_rows = total_rows
        self.total_cols = total_cols
        self.alpha = 255
        self.parents = []

        # heatmap related
        self.heat_value = 0  # alway negative
        pygame.init()
        self.normal_font = pygame.font.SysFont('Arial', 12)
        self.bold_font = pygame.font.SysFont('Arial', 16, bold=True)
        # distance map related
        self.min_distance = -1  # always positive
        # portal related
        self.destination = self
        self.portal_num = -1 # always >= 0

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
    def is_portal(self):
        return self.color == GREY

    def reset(self):
        self.color = WHITE

    def reset_distance(self):
        self.min_distance = -1

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
    
        
    def make_portal(self, nums, des):
        self.color = GREY
        self.portal_num = nums
        self.destination = des

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
        if not self.is_wall() and self.is_portal():
            screen.blit(self.normal_font.render(str(self.destination), True, (0, 0, 0)),
                        (self.x + self.size/8, self.y + self.size/4))

    def draw_heatmap(self, screen):
        self.change_alpha()
        s = pygame.Surface((self.size, self.size))  # the size of your rect
        s.set_alpha(self.alpha)                # alpha level
        s.fill(self.color)           # this fills the entire surface
        screen.blit(s, (self.x, self.y))
        # if not wall
        if not self.is_wall():
            if self.is_bonus():
                screen.blit(self.bold_font.render(str(round(self.heat_value, 2)), True, (0, 0, 0)),
                            (self.x + self.size/4, self.y + self.size/4))
            elif self.heat_value != 0:
                screen.blit(self.normal_font.render(str(round(self.heat_value, 2)), True, (0, 0, 0)),
                            (self.x + self.size/4, self.y + self.size/4))

    def draw_distance_map(self, screen):
        self.change_alpha()
        s = pygame.Surface((self.size, self.size))  # the size of your rect
        s.set_alpha(self.alpha)                # alpha level
        s.fill(self.color)           # this fills the entire surface
        screen.blit(s, (self.x, self.y))
        # if not wall
        if not self.is_wall() and not self.is_pickups():
            screen.blit(self.normal_font.render(str(round(self.min_distance, 2)), True, (0, 0, 0)),
                        (self.x + self.size/4, self.y + self.size/4))

    def draw_portal(self, screen):
        self.change_alpha()
        s = pygame.Surface((self.size, self.size))  # the size of your rect
        s.set_alpha(self.alpha)                # alpha level
        s.fill(self.color)           # this fills the entire surface
        screen.blit(s, (self.x, self.y))
        # if not wall
        if not self.is_wall() and self.is_portal():
            screen.blit(self.normal_font.render(str(self.destination), True, (0, 0, 0)),
                        (self.x + self.size/8, self.y + self.size/4))
            
    def draw_all_map(self, screen):
        self.change_alpha()
        s = pygame.Surface((self.size, self.size))  # the size of your rect
        s.set_alpha(self.alpha)                # alpha level
        s.fill(self.color)           # this fills the entire surface
        screen.blit(s, (self.x, self.y))
        # if not wall
        if not self.is_wall():
            if not self.is_pickups():
                screen.blit(self.normal_font.render(str(round(self.min_distance + self.heat_value, 2)), True, (0, 0, 0)),
                            (self.x + self.size/4, self.y + self.size/4))

    def update_neighbors(self, grid):
        self.neighbors = []
        # DOWN
        if self.row < self.total_rows - 1 and not grid[self.row + 1][self.col].is_wall():
            self.neighbors.append(grid[self.row + 1][self.col])
            self.costs[self.row + 1, self.col] = 1  # random.randint(1,30)

        if self.row > 0 and not grid[self.row - 1][self.col].is_wall():  # UP
            self.neighbors.append(grid[self.row - 1][self.col])
            self.costs[(self.row - 1), self.col] = 1  # random.randint(1,30)

        # RIGHT
        if self.col < self.total_cols - 1 and not grid[self.row][self.col + 1].is_wall():
            self.neighbors.append(grid[self.row][self.col + 1])
            self.costs[self.row, (self.col + 1)] = 1  # random.randint(1,30)

        if self.col > 0 and not grid[self.row][self.col - 1].is_wall():  # LEFT
            self.neighbors.append(grid[self.row][self.col - 1])
            self.costs[self.row, (self.col-1)] = 1  # random.randint(1,30)

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


def draw(screen, grid, rows, cols, width, height, addtional_map="none"):
    screen.fill(WHITE)

    for row in grid:
        for node in row:
            if addtional_map.lower() != "none":
                if addtional_map.lower() == "heat":
                    node.draw_heatmap(screen)
                elif addtional_map.lower() == "distance":
                    node.draw_distance_map(screen)
                else:
                    node.draw_all_map(screen)
            else:
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
                if (i == 0) or (i == len(maze)-1) or (j == 0) or (j == len(maze[0])-1):
                    end = node
                    end.make_end()
            else:
                node.make_wall()

    return start, end

def merge_portal_grid(portal_list, grid):    
    portal_queue = PriorityQueue()
    nums = 0    
    for point_pos in portal_list:
        portal_queue.put(((point_pos[0], point_pos[1])))      
        destination = portal_list[point_pos]
        nums = nums + 1
        grid[point_pos[0]][point_pos[1]].make_portal(nums, destination)
        grid[destination[0]][destination[1]].make_portal(nums, point_pos)

    return portal_queue

def merge_bonus_grid(bonus_points, grid):
    # Sẽ sử dụng priority queue để lưu danh sách các điểm thưởng, điểm thưởng sẽ được chuyển thành dương để dễ lưu
    bonus_queue = PriorityQueue()
    i = 0
    for point in bonus_points:
        bonus_queue.put((point[2], (point[0], point[1])))
        grid[point[0]][point[1]].bonus = point[2]
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
def visualize_maze_by_image(matrix, bonus, pickup, portal, start, end, route: list,saveDir = None ):
    """
    Args:
      1. matrix: The matrix read from the input file,
      2. bonus: The array of bonus points,
      3. start, end: The starting and ending points,
      4. route: The route from the starting point to the ending one, defined by an array of (x, y), e.g. route = [(1, 2), (1, 3), (1, 4)]
    """
    #1. Define walls and array of direction based on the route
    route.reverse()
    if(route[len(route)- 1] != start.get_pos()):
        route.append(start.get_pos())
    route.reverse()
    if(route[len(route)- 1] != end.get_pos()):
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
    if(bonus):
        plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                    marker='P',s=100,color='green')

    if(pickup):
        plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                    marker='D',s=100,color='blue')

    if(portal):
        plt.scatter([i[1] for i in bonus],[-i[0] for i in bonus],
                    marker='H',s=100,color='pink')
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
    bonus_points = []
    pickup_points = []
    portal_points = []
    
    for level in levels:
        for file in files[level]:
            if(level == "advance"):
                maze, bonus_points, pickup_points, portal_points = read_file_advance("./input/" + level + "/" + file)
            else:
                maze, bonus_points, pickup_points = read_file_normal("./input/" + level + "/" + file)
            
            
            ROWS = len(maze)
            COLS = len(maze[0])
            WIDTH = COLS * SIZE
            HEIGHT = ROWS * SIZE
            way = []
            cost = 0
            start = None
            end = None

            algs = []
            no_bonus_alg = ["dfs","bfs","ucs","gbfs","astar"]
            bonus_alg = ["algo1", "algo2"]
            if(level == "level_1"):
                algs = no_bonus_alg
            else:
                algs = bonus_alg
            for alg in algs:
                grid = make_grid(ROWS, COLS)
                start, end = merge_maze_grid(maze, grid,ROWS,COLS)
                bonus_queue = merge_bonus_grid(bonus_points, grid)
                pickup_queue = merge_pickups_grid(pickup_points,grid)
                portal_queue = merge_portal_grid(portal_points,grid)
                if(not level == "level_1"):
                    util.update_bonus_grid(grid, bonus_points, portal_points)
                    util.update_distance_grid(grid, pickup_points, portal_points)
                for row in grid:
                    for node in row:
                        node.update_neighbors(grid)            
                
                SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
                is_alg_do = False # kiem tra co thuat toan nao chay  khong
                if level == "level_1":
                    if(alg == "dfs"):
                        way, cost = algorithm_dfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                        is_alg_do = True
                    elif(alg== "bfs"):
                        way,cost = algorithm_bfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                        is_alg_do = True                        
                    elif(alg == "ucs"):
                        way, cost = algorithm_ucs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                        is_alg_do = True
                    elif(alg == "gbfs"):
                        way, cost =algorithm_greedy_bfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                        is_alg_do = True
                    else:
                        way, cost = algorithm_astar(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, start, end, clock)
                        is_alg_do = True
                elif level == "level_2":
                    if(alg == "algo1"):
                        way, cost = algorithm_bonus_astar(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, bonus_queue, start, end, clock)
                        is_alg_do = True
                    if(alg == "algo2"):
                        way, cost = algorithm_bonus_pickup_astar(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, bonus_points, pickup_points, portal_points, start, end,clock)
                        is_alg_do = True
                elif level == "level_3":
                    if(alg == "algo2"):
                        way, cost = algorithm_bonus_pickup_astar(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, bonus_points, pickup_points, portal_points, start, end,clock)
                        is_alg_do = True
                elif level == "advance":
                    if(alg == "algo2"):
                        way, cost = algorithm_bonus_pickup_astar(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT), grid, bonus_points, pickup_points, portal_points, start, end,clock)
                        is_alg_do = True
                if(is_alg_do):
                    dir_output = level + "\\" + file.split(".")[0] + "\\" + alg
                    create_folder(dir_output)               
                    write_file(dir_output + "\\" + alg + ".txt", cost )
                    video.make_mp4(dir_output+ "\\" + alg)
                    video.destroy_png()
                    if(level == "advance"):
                        maze, bonus_points, pickup_points, portal_points = read_file_advance("./input/" + level + "/" + file)
                    else:
                        maze, bonus_points, pickup_points = read_file_normal("./input/" + level + "/" + file)
            
                    visualize_maze_by_image(maze,bonus_points, pickup_points, portal_points,start,end,way,DIR_OUTPUT + dir_output + "\\" + alg )
                pygame.quit()
               


            


"""
Start simulation
"""


def main(screen, maze, bonus_points, pickup_points, portal_list, width, height):

    grid = make_grid(ROWS, COLS)

    start = None
    end = None    
    start, end = merge_maze_grid(maze, grid, ROWS, COLS)
    merge_bonus_grid(bonus_points=bonus_points, grid=grid)
    merge_pickups_grid(pickup_points, grid)
    merge_portal_grid(portal_list, grid)
    util.update_bonus_grid(grid, bonus_points, portal_list)
    util.update_distance_grid(grid, pickup_points, portal_list)

    # draw once and wait for input (KEY space)
    # draw(screen, grid, ROWS, COLS, width, height, heatmap=include_heatmap)
    # wait()
    addtional_map = 'none'
    run = True
    while run:
        draw(screen, grid, ROWS, COLS, width, height, addtional_map)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

# NOTE: Phần này dùng để khi nhấn phím cách thì thuật toán mới chạy được
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    # if event.key == pygame.K_SPACE and start and end:
                #      run = False


# NOTE: Phần này là mặc định vào chương trình là thuật toán tự chạy và lưu video luôn
        # for row in grid:
        #     for node in row:
        #         node.update_neighbors(grid)
        # algorithm_dfs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
        # # algorithm_bfs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
        # run = False
    algo.algorithm_bonus_pickup_astar(lambda: draw(
                        screen, grid, ROWS, COLS, width, height, addtional_map), grid, bonus_points, pickup_points,portal_list, start, end, clock)
                
    pygame.quit()


"""
Start simulation
"""
# maze_name = '6'
# maze, bonus_points, pickup_points, portal_list = read_file(
#     "./maze/maze_" + maze_name + ".txt")

# ROWS = len(maze)
# COLS = len(maze[0])


# WIDTH = COLS * SIZE
# HEIGHT = ROWS * SIZE

# print(WIDTH, HEIGHT)

# SCREEN = pygame.display.set_mode((WIDTH,  HEIGHT))
video = Video((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation of finding the way")
clock = pygame.time.Clock()

#main(SCREEN, maze, bonus_points, WIDTH, HEIGHT)
run()
#Build video from image.
# video.make_mp4("maze")
#video.destroy_png()


# main(SCREEN, maze, bonus_points, pickup_points, portal_list, WIDTH, HEIGHT)

# #Build video from image.
# video.make_mp4("maze_" + maze_name + "_heat")
# video.destroy_png()
