from dis import dis
from http.client import FOUND
from queue import PriorityQueue, Queue
import utility as util
import math

FPS = 30


def reconstruct_path(way, grid, draw, clock):
    way.reverse()
    total_cost = 0
    for current in way:
        node = grid[current[0]][current[1]]
        total_cost = total_cost + 1 + node.bonus
        node.make_path()
        #chi phí của đường đi xuat ra file ở đây các node.bonus = 0
        #sưa lại bên chỗ cài đặt node
        clock.tick(FPS)
        draw()

    return way, total_cost
    

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
            return reconstruct_path(way, grid, draw, clock)
            
        

        for neighbor in node.neighbors:
            if not neighbor.get_pos() in path:
                stack.append(neighbor.get_pos())
                parents[neighbor.get_pos()] = pos

        clock.tick(FPS)
        draw()

    return [], 0
#lay item co chi phi nho nhat trong hang doi
def getItem(priorityQueue):
    temp = list(priorityQueue.keys())[0]
    for item in priorityQueue:
        if priorityQueue[temp] > priorityQueue[item]:
            temp = item
    return temp

def algorithm_ucs(draw,grid,start,end,clock):
    way = [] # Đường đi đúng nhất từ điểm bắt đầu cho tới điểm cuối
    path = [] # Tất cả các điểm được duyệt qua trong việc tìm kiếm đường đi
    parents = {} # Lưu điểm cha của các điểm được duyệt

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
            return reconstruct_path(way, grid, draw, clock)
            
            
        
        for neighbor in node.neighbors:
            if not neighbor.get_pos() in path:
                #nếu điểm kế tiếp chua có trong hàng đợi thì thêm
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
    
    return [], 0

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

            return reconstruct_path(way, grid, draw, clock)
            

        for neighbor in node.neighbors:
            # WARNING!!!!!!!!
            if not neighbor.get_pos() in path:
                queue.append(neighbor.get_pos())
                parents[neighbor.get_pos()] = pos

        clock.tick(FPS)
        draw()

    return [], 0


def algorithm_greedy_bfs(draw, grid, start, end, clock, bonus_q=Queue()):

    def heuristic_1(point, end):
        x1, y1 = point.get_pos()
        x2, y2 = end.get_pos()
        return abs(x1 - x2) + abs(y1 - y2)

    way = []
    path = []
    parents = {}

    dist = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    dist[start.get_pos()[0]][start.get_pos()[1]] = 0

    queue = PriorityQueue()
    queue.put((heuristic_1(start, end), (start.get_pos())))

    while not queue.empty():
        value_heuristic, (x_pos, y_pos) = queue.get()
        pos = (x_pos, y_pos)

        if pos in path:
            continue

        path.append(pos)

        if pos == end.get_pos():
                    pos_start = start.get_pos()

                    child = end.get_pos()
                    parent = parents[child]
                    while(parent != pos_start):
                        way.append(parent)
                        child = parent
                        parent = parents[child]

                   
                    print(f"Chi phi duong di voi thuat toan Greedy_BFS: {dist[end.get_pos()[0]][end.get_pos()[1]]}")
                    return  reconstruct_path(way, grid, draw, clock)

        node = grid[pos[0]][pos[1]]
        if node != start and node != end:
            node.make_open()

        for neighbor in node.neighbors:
            (x_n, y_n) = neighbor.get_pos()
            # WARNING!!!!!!!!
            if not (x_n, y_n) in path:
                dist[x_n][y_n] = dist[pos[0]][pos[1]] + 1;
                value = heuristic_1(neighbor, end) 
                queue.put((value, neighbor.get_pos()))
                parents[neighbor.get_pos()] = pos
    
        clock.tick(FPS)
        draw()

    return [], 0


def algorithm_astar(draw, grid, start, end, clock):

    def euclid_dis(neighbor, end): #heuristic
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return (x1 - x2) ** 2 + (y1 - y2) ** 2


    # main
    way = []
    open = PriorityQueue()
    closed = []
    parents = {}

    # Khởi tạo hàm chi phí ban đầu
    g = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # g_start = 1
    # (f_n, (pos))
    open.put(( 1 + euclid_dis(start, end), (start.get_pos())))

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

            
            print(f"Chi phí đường đi của thuật toán A*: {g[x_cur][y_cur]}" )
            return reconstruct_path(way, grid, draw, clock)
        
        if not grid[x_cur][y_cur].is_start():
            grid[x_cur][y_cur].make_open()

        closed.append((x_cur, y_cur))
        for neighbor in grid[x_cur][y_cur].neighbors:
            # WARNING!!!!!!!!
            x_new, y_new = neighbor.get_pos()
            if not (x_new, y_new) in closed:
                g_n = 1 + g[x_cur][y_cur]
                g[x_new][y_new] = g_n;
                h_n = euclid_dis(neighbor, end) 
                f_n = g_n + h_n
                open.put((f_n, (x_new, y_new)))

                parents[(x_new, y_new)] = (x_cur, y_cur)
        
        clock.tick(FPS)
        draw()
    return [], 0


# Cách 1: Dùng góc nhọn + điểm cao nhất -> Thất bại
# Cách 2: ...
# Cách 3: Dùng các điểm trong phạm vi giới hạn trong hình nhật từ điểm hiện tại đến kết thúc
    #Lọc ra những điểm nằm cùng phía -> Sắp xếp xa dần điểm đầu, sẽ có 2 nữa trên dưới với đường phân cách là đường chéo hcn đầu cuối
    # Sẽ dùng h_n tính khoảng cách từ nó tới đính và khoảng cách từ nó tới điểm gần đó + gần đó tới đích + bonus -> Nếu chi phí rẻ hơn thì đi ko thì thôi.
# Sẽ tìm khoảng cách từ điểm hiện tại cho tới điểm thỏa mãn


'''
    # Sẽ chuyển thằng bonus_priorities thành priority queue
    isCheckOther = True
    bonus_queue = PriorityQueue()
    for item_pri in bonus_priorities:
        r, c, num_bonus = bonus_priorities[item_pri]
        bonus_queue.put((item_pri,(r, c, num_bonus)))
    while not bonus_queue.empty():
        space_with_start, (r, c, num_bonus) = bonus_queue.get()

        open = PriorityQueue()
        cur_end = grid[r][c]

        pos_start = (cur_start.get_pos()[0], cur_start.get_pos()[1])
        pos_end = (r, c)

        g[pos_start[0]][pos_start[1]] = grid[pos_start[0]][pos_start[1]].bonus
        open.put(( g[pos_start[0]][pos_start[1]] + heuristic_1(cur_start, cur_end), (cur_start.get_pos())))
        while not open.empty():
            f_prev, (r, c) = open.get()

            if (r, c) == pos_end :
                print(num_bonus)
                if isCheckOther:
                    isCheckOther = False
                    # Tới khi đến được 1 nút thuộc bonus ưu tiên thì tìm 1 điểm bên kia có thể đi được
                    cur_start = cur_end
                    isZero = False
                    # Tìm cái điểm tiếp theo của điểm hiện tại, nếu hết thì tìm tới điểm kết thúc
                    if not bonus_queue.empty():
                        space_next_with_start, (r_next, c_next, num_bonus_next) = bonus_queue.get()
                    else:
                        isZero = True
                        r_next, c_next = end.get_pos()
                    # Tìm điểm thỏa mãn        
                    for item_other in bonus_other:
                        num_bonus_other = item_other
                        (r_other, c_other) = bonus_other[item_other]
                        if not (r_other, c_other) in closed:
                            # Check điều kiên của hàm F (cur -> other) + (other -> next) + bonus_cur_new vs (cur -> next)
                            l_cur_other = calc_space((r, c), (r_other, c_other))
                            l_other_next = calc_space((r_other, c_other), (r_next, c_next))
                            l_cur_next = calc_space((r, c), (r_next, c_next))

                            if(l_cur_other + l_other_next + num_bonus_other <= l_cur_next):
                                # Thêm ngược điểm mới vào với khoảng cách là sẽ mặc định nhỏ hơn điểm next 1 đơn vị để nó sắp lên đầu
                                bonus_queue.put((10, (r_other, c_other, num_bonus_other)))
                                break
                        
                    if not isZero:  bonus_queue.put((space_next_with_start, (r_next, c_next, num_bonus_next)))
                    break
                else:
                    isCheckOther = True
                    cur_start = cur_end
                    break
            

            if not grid[r][c].is_start():
                grid[r][c].make_open()

            closed.append((r, c))
            for neighbor in grid[r][c].neighbors:
                # WARNING!!!!!!!!
                r_new, c_new = neighbor.get_pos()
                if not (r_new, c_new) in closed:
                    g_n =  g[r][c] + grid[r_new][c_new].bonus
                    g[r_new][c_new] = g_n
                    h_n = heuristic_1(neighbor, cur_end) 
                    f_n = g_n + h_n
                    open.put((f_n, (r_new, c_new)))

                    parents[(r_new, c_new)] = (r, c)

            clock.tick(FPS)
            draw()

    open = PriorityQueue()
    # g[cur_start[0]][cur_start[1]] = grid[cur_start[0]][cur_start[1]].bonus
    open.put(( g[cur_start.get_pos()[0]][cur_start.get_pos()[1]] + heuristic_1(cur_start, end), (cur_start.get_pos())))
    while not open.empty():
        f_prev, (x_cur, y_cur) = open.get()

        if(grid[x_cur][y_cur].is_end()):
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]
            while(parent != pos_start):
                way.append(parent)
                child = parent
                parent = parents[child]

                    
            print(g[end.get_pos()[0]][end.get_pos()[1]])

            reconstruct_path(way, grid, draw, clock)
            return True

        if not grid[x_cur][y_cur].is_start():
            grid[x_cur][y_cur].make_open()

        closed.append((x_cur, y_cur))
        for neighbor in grid[x_cur][y_cur].neighbors:
            # WARNING!!!!!!!!
            x_new, y_new = neighbor.get_pos()
            if not (x_new, y_new) in closed:
                g_n =  g[r][c] + grid[r_new][c_new].bonus
                g[r_new][c_new] = g_n
                h_n = heuristic_1(neighbor, end) 
                f_n = g_n + h_n
                open.put((f_n, (x_new, y_new)))

                parents[(x_new, y_new)] = (x_cur, y_cur)

        clock.tick(FPS)
        draw()
'''


def algorithm_bonus_pickup_astar(draw, grid, bonus_list, pickup_list, portal_list, start, end, clock):
    def h_x(point):
        if pickup_list:  # ignore end while this are pick up point
            return point.min_distance
        else:
            return util.distance(point, end)

    def g_x(point):
        if point.is_bonus():
            return point.heat_value + point.bonus * 2.5  # prioritize near by bonus point
        else:
            return point.heat_value

    def heuristic(target):
        return h_x(target) + g_x(target)

    def remove_pickup(grid, node, pickup_list, portal_list):
        pickup_list.remove((node.y/util.SIZE, node.x/util.SIZE))
        node.reset()
        node.make_open()
        util.update_distance_grid(grid, pickup_list, portal_list)

    def remove_bonus(grid, node, bonus_list, portal_list):
        bonus_list.remove((node.y/util.SIZE, node.x/util.SIZE, node.bonus))
        node.reset()
        node.make_open()
        util.update_bonus_grid(grid, bonus_list, portal_list)

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


    if len(portal_list):
        portal_flag = True
    else:
        portal_flag = False
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
        if util.check_bonus_list(node, bonus_list):
            remove_bonus(grid, node, bonus_list, portal_list)

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

        # check if reach bonus point
        elif util.check_pickup_list(node, pickup_list):
            remove_pickup(grid, node, pickup_list, portal_list)

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
                neighbor_pos = neighbor.get_pos()
                value = heuristic(neighbor)
                if portal_flag and neighbor_pos in portal_list:                            
                    destination_pos = portal_list[neighbor_pos]
                    neighbor = grid[destination_pos[0]][destination_pos[1]]                                                            
                    neighbor_pos = neighbor.get_pos()
                open.put((value, neighbor))
                parents[neighbor.get_pos()] = pos

        closed.append(node)
        clock.tick(FPS)
        draw()
    return [], 0


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
