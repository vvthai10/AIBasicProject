from contextlib import nullcontext
from pickle import TRUE
from queue import PriorityQueue
import pygame, sys, os
import pygame.camera
from pygame.locals import *
import math
import random
from handle_file_maze import read_file
from algorithm import algorithm_dfs, algorithm_bfs, algorithm_ucs, algorithm_greedy_bfs, algorithm_astar, algorithm_bonus_astar, algorithm_bonus_pickup_astar
from make_video import Video

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
        self.bonus = 1
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

def merge_maze_grid(maze, grid):

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

def main(screen, maze, bonus_points, pickup_points, width, height):
    grid = make_grid(ROWS, COLS)

    start = None
    end = None

    start, end = merge_maze_grid(maze, grid)
    bonus_queue = merge_bonus_grid(bonus_points, grid)
    pickups_queue = merge_pickups_grid(pickup_points, grid)

    run = True
    while run:
        draw(screen, grid, ROWS, COLS, width, height)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

# NOTE: Phần này dùng để khi nhấn phím cách thì thuật toán mới chạy được
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)
                    
                    # check = algorithm_dfs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
                    # check = algorithm_bfs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
                    # check = algorithm_ucs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
                    # check = algorithm_greedy_bfs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
                    # check = algorithm_astar(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
                    check = algorithm_bonus_astar(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, bonus_queue, start, end, clock)
                    # check = algorithm_bonus_pickup_astar(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, bonus_queue, pickups_queue, start, end, clock)
                    print(check)

                
# NOTE: Phần này là mặc định vào chương trình là thuật toán tự chạy và lưu video luôn
        # for row in grid:
        #     for node in row:
        #         node.update_neighbors(grid)
        # algorithm_dfs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
        # algorithm_bfs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
        # run = False

    
    
    pygame.quit()

    
"""
Start simulation
"""

maze, bonus_points, pickup_points = read_file("./maze/maze_6.txt")

ROWS = len(maze)
COLS = len(maze[0])

SIZE = 32

WIDTH = COLS * SIZE
HEIGHT = ROWS * SIZE

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
video = Video((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation of finding the way")
clock = pygame.time.Clock()

video.destroy_png()
main(SCREEN, maze, bonus_points, pickup_points, WIDTH, HEIGHT)

# Build video from image.
video.make_mp4("maze_6")
video.destroy_png()
