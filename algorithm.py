from dis import dis
from http.client import FOUND
from queue import PriorityQueue, Queue
import utility as util
import math

FPS = 5


def reconstruct_path(way, grid, draw, clock):
    way.reverse()
    total_cost = 0
    for current in way:
        node = grid[current[0]][current[1]]
        total_cost = total_cost + 1 + node.bonus
        node.make_path()

        clock.tick(FPS)
        draw()
    print("total cost: ", total_cost)


def algorithm_dfs(draw, grid, start, end, clock):
    way = []  # Đường đi đúng nhất từ điểm bắt đầu cho tới điểm cuối
    path = []  # Tất cả các điểm được duyệt qua trong việc tìm kiếm đường đi
    parents = {}  # Lưu điểm cha của các điểm được duyệt

    stack = []
    stack.append(start.get_pos())

    while len(stack) != 0:
        pos = stack.pop()

        if pos in path:
            continue

        path.append(pos)

        node = grid[pos[0]][pos[1]]
        if node != start and node != end:
            node.make_open()

        # Khi điểm đang duyệt là điểm đích -> ngưng duyệt và tìm kiếm đường đi nhờ vào parent.
        if pos == end.get_pos():
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]

            while (parent != pos_start):
                way.append(parent)
                child = parent
                parent = parents[child]

            # print(f"Ways: {ways}")
            # In ra đường đi
            reconstruct_path(way, grid, draw, clock)
            print("chi phi duong di la dfs: ", len(way))
            return True

        for neighbor in node.neighbors:
            if not neighbor.get_pos() in path:
                stack.append(neighbor.get_pos())
                parents[neighbor.get_pos()] = pos

        clock.tick(FPS)
        draw()

    return False
# lay item co chi phi nho nhat trong hang doi


def getItem(priorityQueue):
    temp = list(priorityQueue.keys())[0]
    for item in priorityQueue:
        if priorityQueue[temp] > priorityQueue[item]:
            temp = item

    return temp


def algorithm_ucs(draw, grid, start, end, clock):
    way = []  # Đường đi đúng nhất từ điểm bắt đầu cho tới điểm cuối
    path = []  # Tất cả các điểm được duyệt qua trong việc tìm kiếm đường đi
    parents = {}  # Lưu điểm cha của các điểm được duyệt

    priorityQueue = {}
    priorityQueue[start.get_pos()] = 0

    while (len(priorityQueue) != 0):
        pos = getItem(priorityQueue)
        # chi phi de toi diem hien tai co vi tri pos
        cost = priorityQueue[pos]
        priorityQueue.pop(pos)      # xoa ra khoi hang doi
        if pos in path:
            continue

        path.append(pos)
        node = grid[pos[0]][pos[1]]
        if node != start and node != end:
            node.make_open()

        if pos == end.get_pos():
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]

            while (parent != pos_start):
                way.append(parent)
                child = parent
                parent = parents[child]

            # print(f"Ways: {ways}")
            # In ra đường đi
            reconstruct_path(way, grid, draw, clock)
            print("chi phi duong di cua ucs: ", len(way))
            return True

        for neighbor in node.neighbors:
            if not neighbor.get_pos() in path:
                # nếu điểm kế tiếp chua có trong hàng đợi thì thêm
                if not neighbor.get_pos() in priorityQueue:
                    priorityQueue[neighbor.get_pos()] = (
                        cost + node.costs[neighbor.get_pos()])
                    parents[neighbor.get_pos()] = pos
                else:  # nếu có rồi mà tồn tại điểm làm cho chi phí thấp hơn thì thêm vào
                    if (node.costs[neighbor.row, neighbor.col] + cost < priorityQueue[neighbor.get_pos()]):
                        priorityQueue[neighbor.get_pos(
                        )] = node.costs[neighbor.row, neighbor.col] + cost
                        parents[neighbor.get_pos()] = pos

        clock.tick(FPS)
        draw()

    return False


def algorithm_bfs(draw, grid, start, end, clock):
    way = []
    path = []
    parents = {}

    queue = []
    queue.append(start.get_pos())

    while len(queue) != 0:
        pos = queue.pop(0)

        if pos in path:
            continue

        path.append(pos)

        node = grid[pos[0]][pos[1]]
        if node != start and node != end:
            node.make_open()

        if pos == end.get_pos():
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]
            while (parent != pos_start):
                way.append(parent)
                child = parent
                parent = parents[child]

            reconstruct_path(way, grid, draw, clock)
            print("chi phi duong di la cua bfs: ", len(way))
            return True

        for neighbor in node.neighbors:
            # WARNING!!!!!!!!
            if not neighbor.get_pos() in path:
                queue.append(neighbor.get_pos())
                parents[neighbor.get_pos()] = pos

        clock.tick(FPS)
        draw()

    return False


def algorithm_greedy_bfs(draw, grid, start, end, clock, bonus_q=Queue()):

    def heuristic_1(point, end):
        x1, y1 = point.get_pos()
        x2, y2 = end.get_pos()
        return abs(x1 - x2) + abs(y1 - y2)

    way = []
    path = []
    parents = {}

    queue = PriorityQueue()

    queue.put((heuristic_1(start, end), (start.get_pos())))

    while not queue.empty():
        value_heuristic, (x_pos, y_pos) = queue.get()
        pos = (x_pos, y_pos)

        if pos in path:
            continue

        path.append(pos)

        node = grid[pos[0]][pos[1]]
        if node != start and node != end:
            node.make_open()

        if pos == end.get_pos():
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]
            while (parent != pos_start):
                way.append(parent)
                child = parent
                parent = parents[child]

            reconstruct_path(way, grid, draw, clock)
            return True

        for neighbor in node.neighbors:
            # WARNING!!!!!!!!
            if not neighbor.get_pos() in path:
                value = heuristic_1(neighbor, end)
                if value <= value_heuristic:
                    queue.put((value, neighbor.get_pos()))
                    parents[neighbor.get_pos()] = pos

        clock.tick(FPS)
        draw()

    return False


def algorithm_astar(draw, grid, start, end, clock):

    def heuristic_1(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def heuristic_2(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return abs(x1-x2) + abs(y1-y2)

    # main
    way = []
    open = PriorityQueue()
    closed = []
    parents = {}

    # Khởi tạo hàm chi phí ban đầu
    g = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # g_start = 1
    # (f_n, (pos))
    open.put((1 + heuristic_1(start, end), (start.get_pos())))

    while not open.empty():
        f_prev, (x_cur, y_cur) = open.get()

        if (grid[x_cur][y_cur].is_end()):
            print("Finally\n")
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]
            while (parent != pos_start):
                way.append(parent)
                child = parent
                parent = parents[child]

            reconstruct_path(way, grid, draw, clock)
            return True

        if not grid[x_cur][y_cur].is_start():
            grid[x_cur][y_cur].make_open()

        closed.append((x_cur, y_cur))
        for neighbor in grid[x_cur][y_cur].neighbors:
            # WARNING!!!!!!!!
            x_new, y_new = neighbor.get_pos()
            if not (x_new, y_new) in closed:
                g_n = 1 + g[x_cur][y_cur]
                h_n = heuristic_1(neighbor, end)
                f_n = g_n + h_n
                open.put((f_n, (x_new, y_new)))

                parents[(x_new, y_new)] = (x_cur, y_cur)

        clock.tick(FPS)
        draw()


# Cách 1: Dùng góc nhọn + điểm cao nhất -> Thất bại
# Cách 2: ...
# Cách 3: Dùng các điểm trong phạm vi giới hạn trong hình nhật từ điểm hiện tại đến kết thúc
    # Lọc ra những điểm nằm cùng phía -> Sắp xếp xa dần điểm đầu, sẽ có 2 nữa trên dưới với đường phân cách là đường chéo hcn đầu cuối
    # Sẽ dùng h_n tính khoảng cách từ nó tới đính và khoảng cách từ nó tới điểm gần đó + gần đó tới đích + bonus -> Nếu chi phí rẻ hơn thì đi ko thì thôi.
# Sẽ tìm khoảng cách từ điểm hiện tại cho tới điểm thỏa mãn


def algorithm_bonus_astar(draw, grid, bonus_list, pick_up_list, start, end, clock):
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
            reconstruct_path(way, grid, draw, clock)
            return True
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
            if not check_parent(node, neighbor, parents, checkpoint_pos) and not neighbor  in closed:
                value = heuristic(neighbor)
                open.put((value, neighbor))
                parents[neighbor.get_pos()] = pos
        
        closed.append(node)
        clock.tick(FPS)
        draw()
    return False
