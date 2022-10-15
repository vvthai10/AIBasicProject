import math
from queue import Queue

def sigmoid(x):
        return 1/(1+math.exp(-x))

def next_gen_heat(current_config):
        distance, heat_value = current_config
        return distance+1, heat_value / 2

def mark_heat_trace(grid, heat_source, heat_val):
    cancel_threshhold = 0.5
    heat_source.heat_value += heat_val
    closed = []

    queue = Queue()
    config = (1, heat_val)
    queue.put((config, heat_source))

    while not queue.empty():
        (cur_config, current_point) = queue.get()
        if current_point in closed:
            continue

        new_config = next_gen_heat(cur_config)

        # if heat val is significant enough
        if (abs(new_config[1]) >= abs(cancel_threshhold)):
            current_point.update_neighbors(grid)
            for neighbor in current_point.neighbors:
                # closed node won't gain heat val
                if not neighbor in closed:
                    neighbor.heat_value += new_config[1]
                    queue.put((new_config, neighbor))

        closed.append(current_point)
        
def delete_heat(grid, heat_source, heat_val):
    mark_heat_trace(grid, heat_source, -1* heat_val)