
from algorithms.algorithm_dfs import algorithm_dfs
from algorithms.algorithm_bfs import algorithm_bfs
from algorithms.algorithm_ucs import algorithm_ucs
from algorithms.algorithm_gbfs import algorithm_greedy_bfs_heuristic_1, algorithm_greedy_bfs_heuristic_2
from algorithms.algorithm_astar import algorithm_astar_heuristic_1, algorithm_astar_heuristic_2
from algorithms.algorithm_advance import algorithm_bonus_astar, algorithm_handle_bonus_pickup, algorithm_handle_all

'''
def algorithm_bonus_astar(draw, grid, bonus_list, start, end, clock):
    def h_x(point):
        return util.distance(point, end)

    def g_x(point, bonus_list=bonus_list):
        if (point.is_bonus()
                and (point.y/util.SIZE, point.x/util.SIZE, point.bonus) in bonus_list):
            return point.heat_value + point.bonus * 10  # edit thiss
        else:
            return point.heat_value

    def heuristic(target):
        return h_x(target) + g_x(target)

    def check_parent(leaf_node, node_to_check, parent_list, pos_root):
        child = leaf_node.get_pos()
        parent = parent_list.get(child)
        if not parent:
            return False
        while parent != pos_root:
            if parent == node_to_check.get_pos():
                return True
            child = parent
            parent = parent_list[child]
        return False

    way = []
    closed = []
    open = PriorityQueue()   # contain nodes (f_n, node)
    parents = {}             # contain positions
    checkpoint_pos = start.get_pos()
    open.put((heuristic(start), start))

    while not open.empty():
        value_heuristic, node = open.get()
        pos = node.get_pos()
        if pos == end.get_pos():  # reach the end
            tmp_way = [pos]
            child = node.get_pos()
            parent = parents[child]
            while parent != checkpoint_pos:
                tmp_way.append(parent)
                child = parent
                parent = parents[child]
            tmp_way.append(checkpoint_pos)
            tmp_way.reverse()
            way = way + tmp_way
            
            way.reverse()   #phục vụ cho việc vẽ ra file .png
            return reconstruct_path(way, grid, draw, clock)
        elif node != start:
            node.make_open()

        # check if reach bonus point
        if node.bonus < 0:
            # delete node from bonus queue
            bonus_list.remove((node.y/util.SIZE, node.x/util.SIZE, node.bonus))
            # re-draw heat grid
            util.update_bonus_grid(grid, bonus_list)

            # find this part of the way
            tmp_way = []
            child = node.get_pos()
            parent = parents.get(child)
            if parent:  # if not run reverse
                while parent != checkpoint_pos:
                    tmp_way.append(parent)
                    child = parent
                    parent = parents[child]
                tmp_way.append(checkpoint_pos)
                tmp_way.reverse()

            # add tmp_way to way
            way = way + tmp_way
            # update checkpoint
            checkpoint_pos = node.get_pos()
            # reset queues
            parents.clear()
            open = PriorityQueue()
            closed = []
            open.put((heuristic(node), node))

        # open new node
        for neighbor in node.neighbors:
            if not check_parent(node, neighbor, parents, checkpoint_pos) and not neighbor in closed:
                value = heuristic(neighbor)
                open.put((value, neighbor))
                parents[neighbor.get_pos()] = pos

        closed.append(node)
        clock.tick(FPS)
        draw()
    return [], 0
'''
