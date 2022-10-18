import math
from queue import Queue

SIZE = 32
# config: heat_value


def next_gen_config(current_config): # use for both heat and distance
    heat_value = current_config
    return heat_value + 1


def update_node(point, config): # use for both heat and dis
    point.heat_value = min(config, point.heat_value)


def minimal_congif(config, is_distance = False):
    if is_distance:
        return False
    cancel_threshhold = 0
    if (abs(config) >= abs(cancel_threshhold)):
        return False
    else:
        return True


def mark_trace(grid, source_node, root_value, is_distance = False):
    if is_distance:
        source_node.distance = 0
    else:
        source_node.heat_value += root_value
    closed = []

    queue = Queue()
    config = root_value
    queue.put((config, source_node))

    while not queue.empty():
        (config, point) = queue.get()
        if point in closed:
            continue

        new_config = next_gen_config(config)

        # if heat val is significant enough
        if not minimal_congif(new_config):
            point.update_neighbors(grid)
            for neighbor in point.neighbors:
                # closed node won't gain heat val
                if not neighbor in closed and neighbor.bonus == 0:
                    update_node(neighbor, new_config, is_distance)
                    queue.put((new_config, neighbor))

        closed.append(point)


def sigmoid(x):
    return 1/(1+math.exp(-x))


def distance(a, b, rect_size=SIZE):
    return math.sqrt((a.x-b.x)**2 + (a.y-b.y)**2)/rect_size


def max_heat(grid):
    ans = 0
    for row in grid:
        for node in row:
            ans = max(ans, abs(node.heat_value))
    return ans


def update_bonus_grid(grid, point_list, is_distance = False):
    # clone bonus_list
    tmpQ = point_list.copy()

    # reset heat grid
    for row in grid:
        for node in row:
            if is_distance:
                node.min_distance = -1
            else:
                node.heat_value = 0

    # mark new heat sources
    while len(tmpQ) != 0:
        pos_x, pos_y, value = tmpQ[0]
        tmpQ.pop(0)
        point = grid[pos_x][pos_y]
        mark_trace(grid, point, value, is_distance)


def update_dis_grid(grid, bonus_list):
    # clone bonus_list
    tmpQ = bonus_list.copy()

    # reset heat grid
    for row in grid:
        for node in row:
            node.heat_value = 0

    # mark new heat sources
    while len(tmpQ) != 0:
        pos_x, pos_y, heat_val = tmpQ[0]
        tmpQ.pop(0)
        point = grid[pos_x][pos_y]
        mark_trace(grid, point, heat_val)