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
    print("List bonus have: ")
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
    print ("Chi phi duong di la: ", cost)
    
    return way, cost
    

def algorithm_dfs(draw, grid, start, end, clock):
    way = [] # Đường đi đúng nhất từ điểm bắt đầu cho tới điểm cuối
    path = [] # Tất cả các điểm được duyệt qua trong việc tìm kiếm đường đi
    parents = {} # Lưu điểm cha của các điểm được duyệt

    stack = []
    stack.append(start.get_pos())

    while len(stack) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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

    while(len(priorityQueue) != 0):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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
            return reconstruct_path(way, grid, draw, clock)
            
            
        
        for neighbor in node.neighbors:
            if not neighbor.get_pos() in path:
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
    
    return [], 0

def algorithm_bfs(draw, grid, start, end, clock):
    way = []
    path = []
    parents = {}

    queue = []
    queue.append(start.get_pos())

    while len(queue) != 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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

            return reconstruct_path(way, grid, draw, clock)
            

        for neighbor in node.neighbors:
            # WARNING!!!!!!!!
            if not neighbor.get_pos() in path:
                queue.append(neighbor.get_pos())
                parents[neighbor.get_pos()] = pos
        
        clock.tick(FPS)
        draw()

    return [], 0

def algorithm_greedy_bfs_heuristic_1(draw, grid, start, end, clock):

    def heuristic_1(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return (x1-x2)**2 + (y1-y2)**2

    way = []
    path = []
    parents = {}

    dist = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    dist[start.get_pos()[0]][start.get_pos()[1]] = 0

    # queue = PriorityQueue()
    # queue.put((heuristic_2(start, end), (start.get_pos())))

    queue = {}
    queue[start.get_pos()] = heuristic_1(start, end)

    #while not queue.empty():
    while not len(queue) == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # value_heuristic, (x_pos, y_pos) = queue.get()
        # pos = (x_pos, y_pos)
        (x_pos, y_pos) = getItem(queue)
        value_heuristic = queue[(x_pos, y_pos)]
        pos = (x_pos,y_pos)
        queue.pop((x_pos, y_pos))

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
                if not (x_n, y_n) in queue:
                    queue[neighbor.get_pos()] = value
                    parents[neighbor.get_pos()] = pos
                else:
                    if(queue[neighbor.get_pos()] > value):
                        queue[neighbor.get_pos()] = value
                        parents[neighbor.get_pos()] = pos
        clock.tick(FPS)
        draw()

    return [], 0


    def heuristic_1(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return (x1 - x2) ** 2 + (y1 - y2) ** 2

def algorithm_greedy_bfs_heuristic_2(draw, grid, start, end, clock):

    def heuristic_2(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return abs(x1-x2) + abs(y1-y2)

    way = []
    path = []
    parents = {}

    dist = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    dist[start.get_pos()[0]][start.get_pos()[1]] = 0

    # queue = PriorityQueue()
    # queue.put((heuristic_2(start, end), (start.get_pos())))

    queue = {}
    queue[start.get_pos()] = heuristic_2(start, end)

    #while not queue.empty():
    while not len(queue) == 0:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        # value_heuristic, (x_pos, y_pos) = queue.get()
        # pos = (x_pos, y_pos)
        (x_pos, y_pos) = getItem(queue)
        value_heuristic = queue[(x_pos, y_pos)]
        pos = (x_pos,y_pos)
        queue.pop((x_pos, y_pos))

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
                value = heuristic_2(neighbor, end)
                if not (x_n, y_n) in queue:
                    queue[neighbor.get_pos()] = value
                    parents[neighbor.get_pos()] = pos
                else:
                    if(queue[neighbor.get_pos()] > value):
                        queue[neighbor.get_pos()] = value
                        parents[neighbor.get_pos()] = pos
        clock.tick(FPS)
        draw()

    return [], 0


    def heuristic_1(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return (x1 - x2) ** 2 + (y1 - y2) ** 2



'''def algorithm_astar_heuristic_1(draw, grid, start, end, clock):

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
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                
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
'''
'''def algorithm_astar_heuristic_2(draw, grid, start, end, clock):

    def mahattan_dis(neighbor, end): #heuristic
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return abs(x1 - x2)  + abs(y1 - y2)

    
    # main
    way = []
    open = PriorityQueue()
    closed = []
    parents = {}

    # Khởi tạo hàm chi phí ban đầu
    g = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # g_start = 1
    # (f_n, (pos))
    open.put(( 1 + mahattan_dis(start, end), (start.get_pos())))

    while not open.empty():
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
                
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
                h_n = mahattan_dis(neighbor, end) 
                f_n = g_n + h_n
                


                open.put((f_n, (x_new, y_new)))

                parents[(x_new, y_new)] = (x_cur, y_cur)
        
        clock.tick(FPS)
        draw()
    return [], 0
'''
def algorithm_astar_heuristic_1(draw, grid, start, end, clock):

    def euclid_dis(neighbor, end): #heuristic
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    
    # main
    way = []
    #open = PriorityQueue()
    open = {}
    closed = []
    parents = {}

    # Khởi tạo hàm chi phí ban đầu
    g = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # g_start = 1
    # (f_n, (pos))
    #open.put(( 1 + mahattan_dis(start, end), (start.get_pos())))
    open[start.get_pos()] = 1 + euclid_dis(start, end)
    #while not open.empty():
    while(not len(open) == 0):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
                
        #f_prev, (x_cur, y_cur) = open.get()
        (x_cur, y_cur) = getItem(open)
        f_prev = open[(x_cur,y_cur)]
        open.pop((x_cur,y_cur))
        if(grid[x_cur][y_cur].is_end()):
            print("Finally\n")
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]
            while(parent != pos_start):
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
                if not (x_new,y_new) in open:
                    open[(x_new, y_new)] = f_n
                    parents[(x_new, y_new)] = (x_cur, y_cur)
                else:
                    if(open[(x_new,y_new)] > f_n):
                        open[(x_new, y_new)] = f_n
                        parents[(x_new, y_new)] = (x_cur, y_cur)
                #open.put((f_n, (x_new, y_new)))

                #parents[(x_new, y_new)] = (x_cur, y_cur)
        
        clock.tick(FPS)
        draw()
    return [], 0

def algorithm_astar_heuristic_2(draw, grid, start, end, clock):

    def mahattan_dis(neighbor, end): #heuristic
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return abs(x1 - x2)  + abs(y1 - y2)

    
    # main
    way = []
    #open = PriorityQueue()
    open = {}
    closed = []
    parents = {}

    # Khởi tạo hàm chi phí ban đầu
    g = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # g_start = 1
    # (f_n, (pos))
    #open.put(( 1 + mahattan_dis(start, end), (start.get_pos())))
    open[start.get_pos()] = 1 + mahattan_dis(start, end)
    #while not open.empty():
    while(not len(open) == 0):
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         pygame.quit()
                
        #f_prev, (x_cur, y_cur) = open.get()
        (x_cur, y_cur) = getItem(open)
        f_prev = open[(x_cur,y_cur)]
        open.pop((x_cur,y_cur))
        if(grid[x_cur][y_cur].is_end()):
            print("Finally\n")
            pos_start = start.get_pos()

            child = end.get_pos()
            parent = parents[child]
            while(parent != pos_start):
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
                h_n = mahattan_dis(neighbor, end) 
                f_n = g_n + h_n
                if not (x_new,y_new) in open:
                    open[(x_new, y_new)] = f_n
                    parents[(x_new, y_new)] = (x_cur, y_cur)
                else:
                    if(open[(x_new,y_new)] > f_n):
                        open[(x_new, y_new)] = f_n
                        parents[(x_new, y_new)] = (x_cur, y_cur)
                #open.put((f_n, (x_new, y_new)))

                #parents[(x_new, y_new)] = (x_cur, y_cur)
        
        clock.tick(FPS)
        draw()
    return [], 0

def algorithm_bonus_astar(draw, grid, bonus, start, end, clock):

    def check_space_with_line(point, start, end):
        a = (end[1] - start[1]) / (end[0] - start[0])
        b = end[1] - a * end[0]

        if point[1] - a * point[0] - b >= 0:
            # Nằm phía trên đường thẳng
            return True
        else:
            # Nằm phía dưới đường thẳng
            return False
    
    def check_in_space(point, start, end, qppoxi):
        max_r = max(start[0], end[0]) + qppoxi
        min_r = min(start[0], end[0]) - qppoxi
        max_c = max(start[1], end[1]) + qppoxi
        min_c = min(start[1], end[1]) - qppoxi

        if point[0] in range(min_r, max_r) and point[1] in range(min_c, max_c):
            return True

        return False
    
    def calc_space_2_point(A, B):
        return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 )

    def calc_space_with_line(point, start, end):
        a = (end[1] - start[1]) / (end[0] - start[0])
        b = end[1] - a * end[0]

        return abs(a * point[0] - point[1] + b ) / math.sqrt(a ** 2 + 1) 

    def compact_bonus(bonus, start, end):
        up_total = 0
        down_total = 0
        up_bonus = {}
        down_bonus = {}
        while not bonus.empty():
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            val, (r, c) = bonus.get()
            if check_in_space((r, c), start.get_pos(), end.get_pos(), 2):
                space = calc_space_2_point((r, c), start.get_pos())
                if check_space_with_line((r, c), start.get_pos(), end.get_pos()):
                    up_total += val
                    up_bonus[space] = (r, c, val)
                else:
                    down_bonus[space] = (r, c, val)
                    down_total += val

            # Bên nhiều điểm là sắp xếp theo thứ tự tăng dần khoảng cách so với điểm bắt đầu
            # Bên it điểm là sắp xếp theo khoảng cách xa dần với thằng đường nối giữa bắt đầu và kết thúc
            
        if up_total < down_total:
            # Sẽ ưu tiên duyệt các điểm bên trên + các điểm gần đường chéo bên dưới
            bonus_other = {}
            for item in down_bonus:
                (r, c, num) = down_bonus[item]
                bonus_other[num] = (r, c)

            down_bonus = bonus_other
            up_bonus = dict(sorted(up_bonus.items()))
            down_bonus = dict(sorted(down_bonus.items()))

            # print(up_bonus, down_bonus)
            return up_bonus, down_bonus
        else:
            # Sẽ ưu tiên duyệt các điểm bên dưới + các điểm gần đường chéo bên trên
            bonus_other = {}
            for item in up_bonus:
                (r, c, num) = up_bonus[item]
                space = calc_space_with_line((r, c), start.get_pos(), end.get_pos())
                bonus_other[num] = (r, c)

            up_bonus = bonus_other     
            up_bonus = dict(sorted(up_bonus.items()))
            down_bonus = dict(sorted(down_bonus.items()))
            
            # print(up_bonus, down_bonus)
            return down_bonus, up_bonus

    def heuristic_1(neighbor, end):
        x1, y1 = neighbor
        x2, y2 = end

        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def heuristic_2(neighbor, end):
        x1, y1 = neighbor
        x2, y2 = end

        return abs(x1-x2) + abs(y1-y2)

    WAYS_TOTAL = []
    open = PriorityQueue()
    closed = []
    closed_bonus = []
    parents = {}

    pos_start = start.get_pos()
    pos_end = end.get_pos()
    g = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    g[pos_start[0]][pos_start[1]] = 0; 

    bonus_priorities, bonus_other = compact_bonus(bonus, start, end)
    
    bonus_queue = PriorityQueue()
    for item_pri in bonus_priorities:
        r, c, val = bonus_priorities[item_pri]
        bonus_queue.put((item_pri,(r, c, val)))

    isCheckOther = True
    while not bonus_queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        space_with_start, (r, c, val) = bonus_queue.get()

        open = PriorityQueue()
        
        pos_end = (r, c)

        open.put(( g[pos_start[0]][pos_start[1]] + heuristic_1(pos_start, pos_end), (pos_start)))
        while not open.empty():
            f_prev, (r, c) = open.get()

            if(grid[r][c].is_end()):
                child = (r, c)
                parent = parents[child]
                ways = []
                ways.append(child)
                while(parent != pos_start):
                    ways.append(parent)
                    child = parent
                    parent = parents[child]
                ways.append(pos_start)
                ways.reverse()
                WAYS_TOTAL.extend(ways)
                parents = {}
                closed = []
                # clean_path_parents_is_used()
                WAYS_TOTAL.reverse()
                return reconstruct_path(WAYS_TOTAL, grid, draw, clock)

            if (r, c) == pos_end:
                child = pos_end
                parent = parents[child]
                ways = []
                ways.append(child)
                while(parent != pos_start):
                    ways.append(parent)
                    child = parent
                    parent = parents[child]
                ways.append(pos_start)
                ways.reverse()
                WAYS_TOTAL.extend(ways)
                
                if isCheckOther:
                    isCheckOther = False
                    # Tới khi đến được 1 nút thuộc bonus ưu tiên thì tìm 1 điểm bên kia có thể đi được
                    pos_start = pos_end
                    isZero = False
                    # Tìm cái điểm tiếp theo của điểm hiện tại, nếu hết thì tìm tới điểm kết thúc
                    if not bonus_queue.empty():
                        space_next_with_start, (r_next, c_next, val_next) = bonus_queue.get()
                    else:
                        isZero = True
                        r_next, c_next = end.get_pos()
                    # Tìm điểm thỏa mãn        
                    for item_other in bonus_other:
                        print(f"Type of NNNNNNN {type(bonus_other)}")
                        val_other = item_other
                        (r_other, c_other) = bonus_other[item_other]
                        if not (r_other, c_other) in closed and not (r_other, c_other) in closed_bonus:
                            closed_bonus.append((r_other, c_other))
                            # Check điều kiên của hàm F (cur -> other) + (other -> next) + bonus_cur_new vs (cur -> next)
                            l_cur_other = calc_space_2_point((r, c), (r_other, c_other))
                            l_other_next = calc_space_2_point((r_other, c_other), (r_next, c_next))
                            l_cur_next = calc_space_2_point((r, c), (r_next, c_next))

                            if(l_cur_other + l_other_next + val_other <= l_cur_next):
                                # Thêm ngược điểm mới vào với khoảng cách là sẽ mặc định nhỏ hơn điểm next 1 đơn vị để nó sắp lên đầu
                                bonus_queue.put((0, (r_other, c_other, val_other)))
                                
                                parents = {}
                                closed = []
                                break
                        
                    if not isZero:  bonus_queue.put((space_next_with_start, (r_next, c_next, val_next)))
                    
                    parents = {}
                    closed = []
                    break
                else:
                    isCheckOther = True
                    pos_start = pos_end
                    parents = {}
                    closed = []
                    break

            
            grid[r][c].make_open()

            closed.append((r, c))

            for neighbor in grid[r][c].neighbors:
                # WARNING!!!!!!!!
                r_new, c_new = neighbor.get_pos()
                if not (r_new, c_new) in closed:
                    g_n = 1 + g[r][c]
                    g[r_new][c_new] = g_n
                    h_n = heuristic_1((r_new, c_new), pos_end) 
                    f_n = g_n + h_n
                    open.put((f_n, (r_new, c_new)))

                    parents[(r_new, c_new)] = (r, c)

            clock.tick(FPS)
            draw()

    open = PriorityQueue()
    open.put(( g[pos_start[0]][pos_start[1]] + heuristic_1(pos_start, end.get_pos()), (pos_start)))
    while not open.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        f_prev, (r, c) = open.get()

        if(grid[r][c].is_end()):
            child = (r, c)
            parent = parents[child]
            ways = []
            ways.append(child)
            while(parent != pos_start):
                ways.append(parent)
                child = parent
                parent = parents[child]
            ways.append(pos_start)
            ways.reverse()
            WAYS_TOTAL.extend(ways)
            # clean_path_parents_is_used()
            WAYS_TOTAL.reverse()
            return reconstruct_path(WAYS_TOTAL, grid, draw, clock)
        
        grid[r][c].make_open()

        closed.append((r, c))
        for neighbor in grid[r][c].neighbors:
            r_new, c_new = neighbor.get_pos()
            if not (r_new, c_new) in closed:
                g_n = 1 + g[r][c]
                g[r_new][c_new] = g_n
                h_n = heuristic_1(neighbor.get_pos(), end.get_pos()) 
                f_n = g_n + h_n
                open.put((f_n, (r_new, c_new)))

                parents[(r_new, c_new)] = (r, c)
        
        clock.tick(FPS)
        draw()
    return [], 0


def algorithm_handle_bonus_pickup(draw, grid, bonus, pickups, start, end, clock):
    WAYS_TOTAL = []
    pickup_checked = []

    def check_points_in_area(top, down, point, approxi):
        max_r = max(top[0], down[0]) + approxi
        min_r = min(top[0], down[0]) - approxi
        max_c = max(top[1], down[1]) + approxi
        min_c = min(top[1], down[1]) - approxi

        # print(f"check {point} in range {top} and {down}")
        if point[0] in range(min_r, max_r) and point[1] in range(min_c, max_c):
            return True

        return False

    def calc_space_2_points(A, B):
        return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 )

    def get_points_areas():
        end_pos = end.get_pos()
        start_pos = start.get_pos()

        # Phạm vi khu vực 1: Start => góc dưới ngược với góc của điểm end
        r_bottom = (len(grid) - 1) if (end_pos[0] > start_pos[0]) else 0
        c_bottom = (len(grid[0])  - 1) if (end_pos[1] < start_pos[1]) else 0

        # Phạm vi khu vực 1: Start => góc trên ngược với góc của điểm end
        r_top = (len(grid) - 1) if (end_pos[0] < start_pos[0]) else 0
        c_top = (len(grid[0])  - 1) if (end_pos[1] < start_pos[1]) else 0

        # Phạm vi 3 là start -> center
        # Phạm vi 4 là center -> end
        c_center = (start_pos[1] + end_pos[1]) // 2

        # Sắp xếp các điêm từ gần đến xa
        pickups_1 = PriorityQueue()
        bonus_1 = PriorityQueue()

        # Sắp xếp từ gần tới xa
        pickups_2 = PriorityQueue()
        bonus_2 = PriorityQueue()

        # Sắp xếp từ start -> center
        pickups_3 = PriorityQueue()
        bonus_3 = PriorityQueue()

        # Sắp xếp từ center -> end
        pickups_4 = PriorityQueue()
        bonus_4 = PriorityQueue()

        c_max = max(c_center, start_pos[1])
        c_min = min(c_center, start_pos[1])
        
        print(f"S1 {start_pos, (r_bottom, c_bottom)}")
        print(f"S2 {start_pos, (r_top, c_top)}")
        print(f"S3 {(c_min, c_max)}")
        print(f"S4 another")


        while not pickups.empty():
            (r_cur, c_cur) = pickups.get()
            print(f"Pick up: {(r_cur, c_cur)}")
            if check_points_in_area(start_pos, (r_bottom, c_bottom), (r_cur, c_cur), 0):
                pickups_1.put((calc_space_2_points(start_pos, (r_cur, c_cur)), (r_cur, c_cur)))
            elif check_points_in_area(start_pos, (r_top, c_top), (r_cur, c_cur), 0):
                pickups_2.put((calc_space_2_points(start_pos, (r_cur, c_cur)), (r_cur, c_cur)))
            elif c_cur in range(c_min, c_max):
                pickups_3.put((calc_space_2_points(start_pos, (r_cur, c_cur)), (r_cur, c_cur)))
            else:
                pickups_4.put((calc_space_2_points(start_pos, (r_cur, c_cur)), (r_cur, c_cur)))

        while not bonus.empty():
            value, (r_cur, c_cur) = bonus.get()
            # print(f"Bonus: {(r_cur, c_cur)}")
            if check_points_in_area(start_pos, (r_bottom, c_bottom), (r_cur, c_cur), 0):
                bonus_1.put((value, (r_cur, c_cur)))
            elif check_points_in_area(start_pos, (r_top, c_top), (r_cur, c_cur), 0):
                bonus_2.put((value, (r_cur, c_cur)))
            elif check_points_in_area((len(grid) - 1, start_pos[1]), (0, c_center), (r_cur, c_cur), 0):
                bonus_3.put((value, (r_cur, c_cur)))
            else:
                bonus_4.put((value, (r_cur, c_cur)))
        
        '''
        while not bonus_1.empty():
            value, (r, c) = bonus_1.get()
            print(f"Bonus 1 value{value}, Pos: {(r, c)}")
        while not bonus_2.empty():
            value, (r, c) = bonus_2.get()
            print(f"Bonus 2 value{value}, Pos: {(r, c)}")
        while not bonus_3.empty():
            value, (r, c) = bonus_3.get()
            print(f"Bonus 3 value{value}, Pos: {(r, c)}")
        while not bonus_4.empty():
            value, (r, c) = bonus_4.get()
            print(f"Bonus 4 value{value}, Pos: {(r, c)}")
        '''

        return pickups_1, pickups_2, pickups_3, pickups_4, bonus_1, bonus_2, bonus_3, bonus_4 

    # def clean_path_parents_is_used(parents, closed):
    #     parents = {}
    #     for point in closed:
    #         if grid[point[0]][point[1]].is_open() :
    #             closed.remove(point)

    #     return parents, closed

    def handle_pickups(pickups, bonus, start_cur_pos, end_cur_pos ):
        closed = []
        parents = {}

        while not pickups.empty():
            space, (end_cur_pos) = pickups.get()
            
            # Đầu tiên kiểm tra có điểm bonus nào trong khoảng này mà kc từ start -> pickup <= start -> bonus + bonus -> pickup + value
            backup_bonus = PriorityQueue()
            while not bonus.empty():
                value, (bonus_pos) = bonus.get()
                if check_points_in_area(start_cur_pos, end_cur_pos, bonus_pos, 2):
                    start_pickup = calc_space_2_points(start_cur_pos, end_cur_pos)
                    start_bonus = calc_space_2_points(start_cur_pos, bonus_pos)
                    bonus_pickup = calc_space_2_points(bonus_pos, end_cur_pos)

                    # Nếu này là điểm được chọn
                    # print(f"1 {grid[bonus_pos[0]][bonus_pos[1]].bonus}")
                    if start_pickup <= start_bonus + bonus_pickup + grid[bonus_pos[0]][bonus_pos[1]].bonus:
                        # print(f"Choose bonus: {bonus_pos}")
                        pickups.put((space, end_cur_pos))
                        end_cur_pos = bonus_pos
                        while not backup_bonus.empty():
                            v, (r, c) = backup_bonus.get()
                            bonus.put((v, (r, c)))
                        break
                    else:
                        backup_bonus.put((value, bonus_pos))
                else:
                    backup_bonus.put((value, bonus_pos))
            
            while not backup_bonus.empty():
                v, (r, c) = backup_bonus.get()
                bonus.put((v, (r, c)))  

            opens = PriorityQueue()
            g[start_cur_pos[0]][start_cur_pos[1]] = grid[start_cur_pos[0]][start_cur_pos[1]].bonus
            # g[start_cur_pos[0]][start_cur_pos[1]] = 1
            g_n = g[start_cur_pos[0]][start_cur_pos[1]]
            h_n = heuristic_1(start_cur_pos, end_cur_pos)
            f_n = g_n + h_n
            opens.put((f_n, start_cur_pos))

            while not opens.empty():
                f_prev, (cur_pos) = opens.get()
                print(f"Start with pos: {cur_pos} to end: {end_cur_pos}")
                
                closed.append(cur_pos)

                if cur_pos == end_cur_pos:
                    # Xây dựng đoạn đường từ điểm kết thúc hiện tại tới điểm đã xuất phát
                    child = end_cur_pos
                    parent = parents[child]
                    ways = []
                    ways.append(child)
                    while(parent != start_cur_pos):
                        ways.append(parent)
                        child = parent
                        parent = parents[child]
                    ways.append(start_cur_pos)
                    ways.reverse()
                    WAYS_TOTAL.extend(ways)
                    parents = {}
                    closed = []
                    pickup_checked.append(end_cur_pos)
                    start_cur_pos = end_cur_pos
                    break
                
                # Kiểm tra điểm đang đi có đang là bonus không
                backup_bonus = PriorityQueue()
                while not bonus.empty():
                    v, (r, c) = bonus.get()
                    if (r, c) != cur_pos:
                        backup_bonus.put((v, (r, c))) 
                    # else:
                    #     print(f"Cur pos {(r, c)} is bonus")
                
                while not backup_bonus.empty():
                    v, (r, c) = backup_bonus.get()
                    bonus.put((v, (r, c))) 

                backup_bonus = PriorityQueue()
                while not pickups.empty():
                    v, (r, c) = pickups.get()
                    if (r, c) != cur_pos:
                        backup_bonus.put((v, (r, c))) 
                    # else:
                    #     print(f"Cur pos {(r, c)} is pickup")

                while not backup_bonus.empty():
                    v, (r, c) = backup_bonus.get()
                    pickups.put((v, (r, c))) 

                grid[cur_pos[0]][cur_pos[1]].make_open()

                for neighbor in grid[cur_pos[0]][cur_pos[1]].neighbors:
                    # WARNING!!!!!!!!
                    new_pos = neighbor.get_pos()
                    if not new_pos in closed and not new_pos in pickup_checked:
                        # print(f"\tAdd neighbor {new_pos}")
                        # NOTE: g[r][c].get_bonus()
                        g_n =  g[cur_pos[0]][cur_pos[1]] + grid[new_pos[0]][new_pos[1]].bonus
                        # g_n =  g[cur_pos[0]][cur_pos[1]] + 1
                        g[new_pos[0]][new_pos[1]] = g_n
                        h_n = heuristic_1(new_pos, end_cur_pos) 
                        f_n = g_n + h_n
                        opens.put((f_n, new_pos))

                        # grid[new_pos[0]][new_pos[1]].parents.append(cur_pos)
                        parents[new_pos] = cur_pos
                
                clock.tick(FPS)
                draw()
        return start_cur_pos, end_cur_pos

    def heuristic_1(neighbor, end):
        x1, y1 = neighbor
        x2, y2 = end

        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def heuristic_2(neighbor, end):
        x1, y1 = neighbor
        x2, y2 = end

        return abs(x1-x2) + abs(y1-y2)

    pickups_1, pickups_2, pickups_3, pickups_4, bonus_1, bonus_2, bonus_3, bonus_4  = get_points_areas()

    opens = PriorityQueue()
    closed = []
    parents = {}

    # Tính toán hàm g
    g = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    start_pos = start.get_pos()
    end_pos = end.get_pos()

    start_cur_pos = start_pos
    end_cur_pos = None

    start_cur_pos, end_cur_pos = handle_pickups(pickups_1, bonus_1, start_cur_pos, end_cur_pos)
    print(f"Finish 1: {start_cur_pos} and {end_cur_pos}")
    start_cur_pos, end_cur_pos = handle_pickups(pickups_2, bonus_2, start_cur_pos, end_cur_pos)
    print(f"Finish 2: {start_cur_pos} and {end_cur_pos}")
    start_cur_pos, end_cur_pos = handle_pickups(pickups_3, bonus_3, start_cur_pos, end_cur_pos)
    print(f"Finish 3: {start_cur_pos} and {end_cur_pos}")
    start_cur_pos, end_cur_pos = handle_pickups(pickups_4, bonus_4, start_cur_pos, end_cur_pos)
    print(f"Finish 4: {start_cur_pos} and {end_cur_pos}")

    # Từ cur -> end + các điểm bonus có thể ăn được
    # Sẽ check trong bonus_4 thôi và trong cái diện tích giới hạn

    # clean_path_is_used()
    bonus_other = PriorityQueue()
    end_cur_pos = end_pos

    while not bonus_4.empty():
        value, (bonus_pos) = bonus_4.get()
        # print(value)
        if check_points_in_area(start_cur_pos, end_pos, bonus_pos, 2):
            bonus_other.put((calc_space_2_points(start_cur_pos, bonus_pos), value, bonus_pos))

    while not bonus_other.empty():
        space, value, (bonus_pos) = bonus_other.get()
        
        len_1 = calc_space_2_points(start_cur_pos, end_pos)
        len_2 = value + calc_space_2_points(start_cur_pos, bonus_pos) + calc_space_2_points(bonus_pos, end_pos)

        if len_1 <= len_2:
            end_cur_pos = bonus_pos
            opens = PriorityQueue()
            g[start_cur_pos[0]][start_cur_pos[1]] = grid[start_cur_pos[0]][start_cur_pos[1]].bonus
            # g[start_cur_pos[0]][start_cur_pos[1]] = 1
            g_n = g[start_cur_pos[0]][start_cur_pos[1]]
            h_n = heuristic_1(start_cur_pos, end_cur_pos)
            f_n = g_n + h_n
            opens.put((f_n, start_cur_pos))

            while not opens.empty():
                f_prev, (cur_pos) = opens.get()
                # print(f"Start with pos: {cur_pos}")
                
                closed.append(cur_pos)

                if cur_pos == end_cur_pos:
                    # Xây dựng đoạn đường từ điểm kết thúc hiện tại tới điểm đã xuất phát
                    child = end_cur_pos
                    parent = parents[child]
                    ways = []
                    ways.append(child)
                    while(parent != start_cur_pos):
                        ways.append(parent)
                        child = parent
                        parent = parents[child]
                    ways.append(start_cur_pos)
                    ways.reverse()
                    WAYS_TOTAL.extend(ways)
                    parents = {}
                    closed = []
                    start_cur_pos = end_cur_pos
                    break
                
                grid[cur_pos[0]][cur_pos[1]].make_open()

                for neighbor in grid[cur_pos[0]][cur_pos[1]].neighbors:
                    # WARNING!!!!!!!!
                    new_pos = neighbor.get_pos()
                    if not new_pos in closed:
                        # print(f"\tAdd neighbor {new_pos}")
                        # NOTE: g[r][c].get_bonus()
                        g_n = g[cur_pos[0]][cur_pos[1]] + grid[new_pos[0]][new_pos[1]].bonus
                        # g_n = g[cur_pos[0]][cur_pos[1]] + 1
                        g[new_pos[0]][new_pos[1]] = g_n
                        h_n = heuristic_1(new_pos, end_cur_pos) 
                        f_n = g_n + h_n
                        opens.put((f_n, new_pos))

                        parents[new_pos] = cur_pos
                        # grid[new_pos[0]][new_pos[1]].parents.append(cur_pos)
                
                clock.tick(FPS)
                draw()
        
    # Từ điểm hiện tại đến cuối đường
    end_cur_pos = end_pos
    opens = PriorityQueue()
    # g[start_cur_pos[0]][start_cur_pos[1]] = grid[start_cur_pos[0]][start_cur_pos[1]].bonus
    g_n = g[start_cur_pos[0]][start_cur_pos[1]]
    h_n = heuristic_1(start_cur_pos, end_cur_pos)
    f_n = g_n + h_n
    opens.put((f_n, start_cur_pos))

    while not opens.empty():
        f_prev, (cur_pos) = opens.get()
        # print(f"Start with pos: {cur_pos}")
        
        closed.append(cur_pos)

        if cur_pos == end_cur_pos:
            # start_cur_pos = end_cur_pos
            # Xây dựng đoạn đường từ điểm kết thúc hiện tại tới điểm đã xuất phát
            child = end_pos
            parent = parents[child]
            ways = []
            ways.append(child)
            while(parent != start_cur_pos):
                ways.append(parent)
                child = parent
                parent = parents[child]
            ways.append(start_cur_pos)
            ways.reverse()
            WAYS_TOTAL.extend(ways)
            # clean_path_parents_is_used()

                    
            # print(WAYS_TOTAL)
            WAYS_TOTAL.reverse()
            
            #print(g[end_pos[0]][end_pos[1]])



            return reconstruct_path(WAYS_TOTAL, grid, draw, clock)
        
        if cur_pos != start_pos and cur_pos != end_pos:
            grid[cur_pos[0]][cur_pos[1]].make_open()

        for neighbor in grid[cur_pos[0]][cur_pos[1]].neighbors:
            # WARNING!!!!!!!!
            new_pos = neighbor.get_pos()
            if not new_pos in closed:
                # print(f"\tAdd neighbor {new_pos}")
                # NOTE: g[r][c].get_bonus()
                g_n = g[cur_pos[0]][cur_pos[1]] + grid[new_pos[0]][new_pos[1]].bonus
                # g_n = g[cur_pos[0]][cur_pos[1]] + 1
                g[new_pos[0]][new_pos[1]] = g_n
                h_n = heuristic_1(new_pos, end_cur_pos) 
                f_n = g_n + h_n
                opens.put((f_n, new_pos))

                parents[new_pos] = cur_pos
                # grid[new_pos[0]][new_pos[1]].parents.append(cur_pos)
        
        clock.tick(FPS)
        draw()

def algorithm_handle_all(draw, grid, bonus_list, pickup_list, portal_list, start, end, clock):
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
        # node.bonus = 0
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
