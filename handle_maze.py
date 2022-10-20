import pygame
from init import *
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
from init import *
from handle_visualize import make_image, Video

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

def draw(screen, grid, rows, cols, width, height, video):
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
