import math
from queue import Queue
from init import *

# config: heat_value


def next_gen_config(current_config):  # use for both heat and distance
    heat_value = current_config
    return heat_value + 1


def update_node(point, config, is_distance=False):  # use for both heat and dis
    if is_distance:
        if point.min_distance == -1:  # node isn't marked yet
            point.min_distance = config
        else:
            point.min_distance = min(config, point.min_distance)
    else:
        point.heat_value = min(config, point.heat_value)


def minimal_congif(config, is_distance=False):
    if is_distance:
        return False
    cancel_threshhold = 0
    if (abs(config) >= abs(cancel_threshhold)):
        return False
    else:
        return True


def mark_trace(grid, source_node, root_value, portal_list, is_distance=False):
    if len(portal_list):
        using_portal = True
    else:        
        using_portal = False
    
    if is_distance:
        source_node.min_distance += root_value
    else:
        source_node.heat_value += root_value
    closed = []

    queue = Queue()
    config = root_value
    queue.put((config, source_node)) # edit if start on portal

    while not queue.empty():
        (config, point) = queue.get()
        if point in closed:
            continue

        new_config = next_gen_config(config)

        # if heat val is significant enough
        if not minimal_congif(new_config, is_distance):
            point.update_neighbors(grid)
            for neighbor in point.neighbors:
                # closed node won't be update
                if is_distance:
                    if not neighbor in closed and not neighbor.is_pickups():                        
                        update_node(neighbor, new_config, is_distance)
                        neighbor_pos = neighbor.get_pos()
                        if using_portal and neighbor_pos in portal_list:                            
                            destination_pos = portal_list[neighbor_pos]
                            destination_node = grid[destination_pos[0]][destination_pos[1]]
                            update_node(destination_node, new_config, is_distance)
                            queue.put((new_config, destination_node))
                        else:
                            queue.put((new_config, neighbor))
                else:
                    if not neighbor in closed and not neighbor.is_bonus():
                        update_node(neighbor, new_config, is_distance)
                        neighbor_pos = neighbor.get_pos()
                        if using_portal and neighbor_pos in portal_list:                            
                            destination_pos = portal_list[neighbor_pos]
                            destination_node = grid[destination_pos[0]][destination_pos[1]]
                            update_node(destination_node, new_config, is_distance)
                            queue.put((new_config, destination_node))
                        else:
                            queue.put((new_config, neighbor))

        closed.append(point)


def sigmoid(x):
    return 1/(1+math.exp(-x))


def distance(a, b, rect_size=SIZE):
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)/rect_size


def step_distance(a, b, rect_size=SIZE):
    return (abs(a.x-b.x) + abs(a.y-b.y))/rect_size


def max_heat(grid):
    ans = 0
    for row in grid:
        for node in row:
            ans = max(ans, abs(node.heat_value))
    return ans


def update_bonus_grid(grid, point_list, portal_list =[]):        
    # clone bonus_list
    tmpQ = point_list.copy()

    # reset heat grid
    for row in grid:
        for node in row:
            node.heat_value = 0

    # mark new heat sources
    while len(tmpQ) != 0:
        pos_x, pos_y, value = tmpQ[0]
        tmpQ.pop(0)
        point = grid[pos_x][pos_y]
        mark_trace(grid, point, value, portal_list)


def update_distance_grid(grid, point_list, portal_list):
    # clone bonus_list
    tmpQ = point_list.copy()

    # reset heat grid
    for row in grid:
        for node in row:
            node.reset_distance()

    # mark new heat sources
    while len(tmpQ) != 0:
        pos_x, pos_y = tmpQ[0]
        tmpQ.pop(0)
        point = grid[pos_x][pos_y]
        mark_trace(grid, point, 0, portal_list, is_distance=True)


def check_bonus_list(node, point_list):
    return (node.y/SIZE, node.x/SIZE, node.bonus) in point_list


def check_pickup_list(node, point_list):
    return (node.y/SIZE, node.x/SIZE) in point_list

