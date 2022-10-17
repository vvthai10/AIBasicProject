import math
from queue import Queue

SIZE = 32
# config: heat_value


def next_gen_heat(current_config):
    heat_value = current_config
    return heat_value + 1


def update_heat(point, config):
    point.heat_value = min(config, point.heat_value)


def minimal_congif(config):
    cancel_threshhold = 0
    if (abs(config) >= abs(cancel_threshhold)):
        return False
    else:
        return True


def mark_heat_trace(grid, heat_source, heat_val):
    heat_source.heat_value += heat_val
    closed = []

    queue = Queue()
    config = heat_val
    queue.put((config, heat_source))

    while not queue.empty():
        (cur_config, current_point) = queue.get()
        if current_point in closed:
            continue

        new_config = next_gen_heat(cur_config)

        # if heat val is significant enough
        if not minimal_congif(new_config):
            current_point.update_neighbors(grid)
            for neighbor in current_point.neighbors:
                # closed node won't gain heat val
                if not neighbor in closed and neighbor.bonus == 0:
                    update_heat(neighbor, new_config)
                    queue.put((new_config, neighbor))

        closed.append(current_point)


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


def update_heat_grid(grid, bonus_list):
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
        mark_heat_trace(grid, point, heat_val)
