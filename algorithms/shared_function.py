from http.client import FOUND
import math
import pygame
from queue import PriorityQueue, Queue
from init import *
import utility as util
from dis import dis

def reconstruct_path(way, grid, draw, clock):
    way.reverse()
    cost = 0
    # print("List bonus have: ")
    total = 0
    for current in way:
        # print(grid[current[0]][current[1]].bonus)
        # total += grid[current[0]][current[1]].bonus
        node = grid[current[0]][current[1]]
        node.make_path()
        #chi phí của đường đi xuat ra file ở đây các node.bonus = 0
        #sưa lại bên chỗ cài đặt node
        cost = cost  + node.get_bonus()
        clock.tick(FPS)
        draw()
    print ("Road costs: ", cost)
    
    return way, cost
def getItem(priorityQueue):
    temp = list(priorityQueue.keys())[0]
    for item in priorityQueue:
        if priorityQueue[temp] > priorityQueue[item]:
            temp = item
    
    return temp
