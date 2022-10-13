from queue import PriorityQueue
import math

FPS = 5

def reconstruct_path(way, grid, draw, clock):
    way.reverse()
    for current in way:
        node = grid[current[0]][current[1]]
        node.make_path()
        
        clock.tick(FPS)
        draw()


def algorithm_dfs(draw, grid, start, end, clock):
    way = [] # Đường đi đúng nhất từ điểm bắt đầu cho tới điểm cuối
    path = [] # Tất cả các điểm được duyệt qua trong việc tìm kiếm đường đi
    parents = {} # Lưu điểm cha của các điểm được duyệt

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
            return True

        for neighbor in node.neighbors:
            if not neighbor.get_pos() in path:
                stack.append(neighbor.get_pos())
                parents[neighbor.get_pos()] = pos

        clock.tick(FPS)
        draw()

    return False
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

    while(len(priorityQueue) != 0):
        pos = getItem(priorityQueue)
        cost = priorityQueue[pos]   # chi phi de toi diem hien tai co vi tri pos
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
            return True
        
        for neighbor in node.neighbors:
            if not neighbor.get_pos() in path :
                #nếu điểm kế tiếp chua có trong hàng đợi thì thêm
                if not neighbor.get_pos() in priorityQueue:
                    priorityQueue[neighbor.get_pos()] = (cost + node.costs[neighbor.get_pos()])
                    parents[neighbor.get_pos()] = pos
                else: # nếu có rồi mà tồn tại điểm làm cho chi phí thấp hơn thì thêm vào 
                    if(node.costs[neighbor.row, neighbor.col] + cost < priorityQueue[neighbor.get_pos()]):
                        priorityQueue[neighbor.get_pos()] = node.costs[neighbor.row, neighbor.col] + cost
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
            while(parent != pos_start):
                way.append(parent)
                child = parent
                parent = parents[child]

            reconstruct_path(way, grid, draw, clock)
            return True

        for neighbor in node.neighbors:
            # WARNING!!!!!!!!
            if not neighbor.get_pos() in path:
                queue.append(neighbor.get_pos())
                parents[neighbor.get_pos()] = pos
        
        clock.tick(FPS)
        draw()

    return False

def algorithm_greedy_bfs(draw, grid, start, end, clock):

    def heuristic_1(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def heuristic_2(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return abs(x1-x2) + abs(y1-y2)

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
            while(parent != pos_start):
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

        if(grid[x_cur][y_cur].is_end()):
            print("Finally\n")
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]
            while(parent != pos_start):
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
                h_n = euclid_dis(neighbor, end) 
                f_n = g_n + h_n
                open.put((f_n, (x_new, y_new)))

                parents[(x_new, y_new)] = (x_cur, y_cur)
        
        clock.tick(FPS)
        draw()


def algorithm_bonus_astar(draw, grid, bonus, start, end, clock):
    def get_cos(a, o, b):
        ao_2 = (a[0] - o[0]) ** 2 + (a[1] - o[1]) ** 2
        bo_2 = (b[0] - o[0]) ** 2 + (b[1] - o[1]) ** 2
        ab_2 = (a[0] - b[0]) ** 2 + (a[1] - b[1]) ** 2

        cos_aob = (ao_2  + bo_2 - ab_2) / (2 * (math.sqrt(ao_2) * math.sqrt(bo_2)))
        return cos_aob
    print(start.get_pos())
    print(end.get_pos())

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
    cur_start = start
    g[start.get_pos()[0]][start.get_pos()[1]] = 1;
    # Duyệt hết tất cả các điểm có trong danh mục điểm thưởng.
    while not bonus.empty():
        num_bonus, (x_cur, y_cur) = bonus.get()

        print(num_bonus)

        # Cách 1: Dùng góc nhọn + điểm cao nhất -> Thất bại
        # Cách 2: Dùng các điểm trong phạm vi giới hạn trong hình nhật từ điểm hiện tại đến kết thúc
            #Lọc ra những điểm nằm cùng phía -> Sắp xếp xa dần điểm đầu, sẽ có 2 nữa trên dưới với đường phân cách là đường chéo hcn đầu cuối
            # Sẽ dùng h_n tính khoảng cách từ nó tới đính và khoảng cách từ nó tới điểm gần đó + gần đó tới đích + bonus -> Nếu chi phí rẻ hơn thì đi ko thì thôi.
        # Sẽ tìm khoảng cách từ điểm hiện tại cho tới điểm thỏa mãn
        if False:
            open = PriorityQueue()

            cur_end = grid[x_cur][y_cur]
            open.put(( g[cur_start.get_pos()[0]][cur_start.get_pos()[1]] + heuristic_1(cur_start, cur_end), (cur_start.get_pos())))
            while not open.empty():
                f_prev, (x_cur, y_cur) = open.get()

                if((x_cur, y_cur) == cur_end.get_pos()):
                    cur_start = cur_end
                    break
                
                if not grid[x_cur][y_cur].is_start():
                    grid[x_cur][y_cur].make_open()

                closed.append((x_cur, y_cur))
                for neighbor in grid[x_cur][y_cur].neighbors:
                    # WARNING!!!!!!!!
                    x_new, y_new = neighbor.get_pos()
                    if not (x_new, y_new) in closed:
                        g_n = 1 + g[x_cur][y_cur]
                        g[x_new][y_new] = g_n
                        h_n = heuristic_1(neighbor, cur_end) 
                        f_n = g_n + h_n
                        open.put((f_n, (x_new, y_new)))

                        parents[(x_new, y_new)] = (x_cur, y_cur)

                clock.tick(FPS)
                draw()

    open = PriorityQueue()
    open.put(( g[cur_start.get_pos()[0]][cur_start.get_pos()[1]] + heuristic_1(cur_start, end), (cur_start.get_pos())))
    while not open.empty():
        f_prev, (x_cur, y_cur) = open.get()

        if(grid[x_cur][y_cur].is_end()):
            print("Finally\n")
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]
            while(parent != pos_start):
                way.append(parent)
                child = parent
                parent = parents[child]

                    
            print("Costs: ")
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
                g_n = 1 + g[x_cur][y_cur]
                g[x_new][y_new] = g_n
                h_n = heuristic_1(neighbor, end) 
                f_n = g_n + h_n
                open.put((f_n, (x_new, y_new)))

                parents[(x_new, y_new)] = (x_cur, y_cur)
        
        clock.tick(FPS)
        draw()












# ============================== VERSION 1 =============================
# ways_total = [] # lưu trữ cả những điểm đã bị pop ra
# ways_true = []  # lưu trữ tuyến đường đi đúng đắn nhất

# def DFS(point, moves, end):
#   if point == end:
#     ways_total.append(point)
#     ways_true.append(point)
#     check = True
#     return True
  
#   ways_total.append(point)
#   ways_true.append(point)

#   check = False;

#   point_up = (point[0] - 1, point[1])
#   point_down = (point[0] + 1, point[1])
#   point_left = (point[0], point[1] - 1)
#   point_right = (point[0], point[1] + 1)
#   if(not check and point_up in moves and ways_true.count(point_up) == 0):
#     check = DFS(point_up, moves, end);
#   if(not check and point_down in moves and ways_true.count(point_down)  == 0):
#     check = DFS(point_down, moves, end);
#   if(not check and point_left in moves and ways_true.count(point_left)  == 0):
#     check = DFS(point_left, moves, end);
#   if(not check and point_right in moves and ways_true.count(point_right)  == 0):
#     check = DFS(point_right, moves, end);
  
#   if(not check): 
#     # print(f"Remove point{point}\n")
#     ways_true.pop()

#   return check

# def WaysFind():
#     return ways_total, ways_true
  