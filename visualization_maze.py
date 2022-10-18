from pickle import TRUE
from queue import PriorityQueue, Queue
import pygame
import sys
import pygame.camera
from pygame.locals import *
from handle_file_maze import read_file
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
        # heatmap related
        self.heat_value = 0  # alway negative
        pygame.init()
        self.normal_font = pygame.font.SysFont('Arial', 12)
        self.bold_font = pygame.font.SysFont('Arial', 16, bold=True)
        # distance map related
        self.min_distance = -1 # always positive

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
        self.color = PURPLE
        self.alpha = 255

    def draw(self, screen):
        self.change_alpha()
        s = pygame.Surface((self.size, self.size))  # the size of your rect
        s.set_alpha(self.alpha)                # alpha level
        s.fill(self.color)           # this fills the entire surface
        screen.blit(s, (self.x, self.y))

    def draw_distance_map(self, screen):
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
        if not self.is_wall():            
            screen.blit(self.normal_font.render(str(round(self.min_distance, 2)), True, (0, 0, 0)),
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


def draw(screen, grid, rows, cols, width, height, heatmap=False):
    screen.fill(WHITE)

    for row in grid:
        for node in row:
            if heatmap:
                max_heat = util.max_heat(grid)
                # update_heat_gradient(grid, max_heat)
                node.draw_heatmap(screen)
            else:
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
            if (maze[i][j] == 'S'):
                start = node
                start.make_start()
            elif maze[i][j] == ' ':
                if (i == 0) or (i == len(maze)-1) or (j == 0) or (j == len(maze[0])-1):
                    end = node
                    end.make_end()
            else:
                node.make_wall()

    return start, end


def merge_bonus_grid(bonus_points, grid):
    # Sẽ sử dụng priority queue để lưu danh sách các điểm thưởng, điểm thưởng sẽ được chuyển thành dương để dễ lưu
    bonus_queue = PriorityQueue()

    for point in bonus_points:
        bonus_queue.put((point[2], (point[0], point[1])))
        grid[point[0]][point[1]].bonus = point[2]
        grid[point[0]][point[1]].make_bonus()

    return bonus_queue


def main(screen, maze, bonus_points, width, height):

    grid = make_grid(ROWS, COLS)

    start = None
    end = None
    include_heatmap = True

    start, end = merge_maze_grid(maze, grid)
    merge_bonus_grid(bonus_points, grid)
    util.update_grid(grid, bonus_points)

    # draw once and wait for input (KEY space)
    # draw(screen, grid, ROWS, COLS, width, height, heatmap=include_heatmap)
    # wait()
    run = True
    while run:
        draw(screen, grid, ROWS, COLS, width, height, heatmap=include_heatmap)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

# NOTE: Phần này dùng để khi nhấn phím cách thì thuật toán mới chạy được
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for node in row:
                            node.update_neighbors(grid)

                    algo.algorithm_bonus_astar(lambda: draw(
                        screen, grid, ROWS, COLS, width, height, heatmap=include_heatmap), grid, bonus_points, start, end, clock)
                # if event.key == pygame.K_SPACE and start and end:
                #      run = False


# NOTE: Phần này là mặc định vào chương trình là thuật toán tự chạy và lưu video luôn
        # for row in grid:
        #     for node in row:
        #         node.update_neighbors(grid)
        # algorithm_dfs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
        # # algorithm_bfs(lambda: draw(screen, grid, ROWS, COLS, width, height), grid, start, end, clock)
        # run = False

    pygame.quit()


"""
Start simulation
"""
maze_name = '5'
maze, bonus_points, pickup_points = read_file("./maze/maze_" + maze_name + ".txt")

ROWS = len(maze)
COLS = len(maze[0])


WIDTH = COLS * SIZE
HEIGHT = ROWS * SIZE

print(WIDTH, HEIGHT)

SCREEN = pygame.display.set_mode((WIDTH, HEIGHT))
video = Video((WIDTH, HEIGHT))
pygame.display.set_caption("Simulation of finding the way")
clock = pygame.time.Clock()
video.destroy_png()
main(SCREEN, maze, bonus_points, WIDTH, HEIGHT)

# Build video from image.
video.make_mp4("maze_" + maze_name + "_heat")
video.destroy_png()
