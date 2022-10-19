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
from handle_maze import *

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
def run():
    level, files = list_file()

    print(files)
    print(level)

    no_bonus_alg = ["dfs","bfs","ucs","gbfs","astar"]
    for file in files[level[0]]:
        maze, bonus_points, pickup_point = read_file("./input/" + level[0] + "/" + file)
        
        ROWS = len(maze)
        COLS = len(maze[0])
        WIDTH = COLS * SIZE
        HEIGHT = ROWS * SIZE
        way = []
        cost = 0
        start = None
        end = None

        for alg in no_bonus_alg:
            grid = make_grid(ROWS, COLS)
            start, end = merge_maze_grid(maze, grid,ROWS,COLS)
            bonus_queue = merge_bonus_grid(bonus_points, grid)
            for row in grid:
                for node in row:
                    node.update_neighbors(grid)            
            
            SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)
            if(alg == "dfs"):
                way, cost = algorithm_dfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
            elif(alg== "bfs"):
                way,cost = algorithm_bfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
            elif(alg == "ucs"):
                way, cost = algorithm_ucs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
            elif(alg == "gbfs"):
                way, cost =algorithm_greedy_bfs(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
            else:
                way, cost = algorithm_astar(lambda: draw(SCREEN, grid, ROWS, COLS, WIDTH, HEIGHT, video), grid, start, end, clock)
            
            dir_output = level[0] + "\\" + file.split(".")[0] + "\\" + alg
            create_folder(dir_output)               
            write_file(dir_output + "\\" + alg + ".txt", cost )
            video.make_mp4(dir_output+ "\\" + alg)
            video.destroy_png()
            make_image(maze,bonus_queue,start,end,way,DIR_OUTPUT + dir_output + "\\" + alg )
            pygame.quit()
            


"""
Start simulation
"""

# bonus_points, maze = read_file("./maze/maze_3.txt")

# ROWS = len(maze)
# COLS = len(maze[0])

# WIDTH = COLS * SIZE
# HEIGHT = ROWS * SIZE

# print(WIDTH, HEIGHT)

# SCREEN = pygame.display.set_mode((WIDTH, HEIGHT), flags=pygame.HIDDEN)
video = Video((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation of finding the way")
clock = pygame.time.Clock()

#main(SCREEN, maze, bonus_points, WIDTH, HEIGHT)
run()
#Build video from image.
# video.make_mp4("maze")
# video.destroy_png()

