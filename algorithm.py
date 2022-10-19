from queue import PriorityQueue
import math
import pygame

FPS = 30

def reconstruct_path(way, grid, draw, clock):
    way.reverse()
    cost = 0
    print("List bonus have: ")
    total = 0
    for current in way:
        print(grid[current[0]][current[1]].bonus)
        total += grid[current[0]][current[1]].bonus
        node = grid[current[0]][current[1]]
        node.make_path()
        #chi phí của đường đi xuat ra file ở đây các node.bonus = 0
        #sưa lại bên chỗ cài đặt node
        cost = cost + 1 + node.bonus
        clock.tick(FPS)
        draw()
    print ("chi phi duong di la ", cost)
    
    print(total)
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

    dist = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]
    dist[start.get_pos()[0]][start.get_pos()[1]] = 0

    queue = PriorityQueue()
    queue.put((heuristic_1(start, end), (start.get_pos())))

    while not queue.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

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


def algorithm_bonus_astar(draw, grid, bonus, start, end, clock):

    def check_with_line(point, start, end):
        a = (end[1] - start[1]) / (end[0] - start[0])
        b = end[1] - a * end[0]

        if point[1] - a * point[0] - b >= 0:
            # Nằm phía trên đường thẳng
            return True
        else:
            # Nằm phía dưới đường thẳng
            return False


    def check_in_range(point, start, end):
        max_r = max(start[0], end[0]) + 2
        min_r = min(start[0], end[0]) - 2
        max_c = max(start[1], end[1]) + 2
        min_c = min(start[1], end[1]) - 2

        if point[0] in range(min_r, max_r) and point[1] in range(min_c, max_c):
            return True

        return False

    def calc_space(A, B):
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
            num_bonus, (x_cur, y_cur) = bonus.get()
            if check_in_range((x_cur, y_cur), start.get_pos(), end.get_pos()):
                space = calc_space((x_cur, y_cur), start.get_pos())
                if check_with_line((x_cur, y_cur), start.get_pos(), end.get_pos()):
                    up_total += num_bonus
                    up_bonus[space] = (x_cur, y_cur, num_bonus)
                else:
                    down_bonus[space] = (x_cur, y_cur, num_bonus)
                    down_total += num_bonus

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

            print(up_bonus, down_bonus)
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
            print(up_bonus, down_bonus)
            return down_bonus, up_bonus
            
    def heuristic_1(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def heuristic_2(neighbor, end):
        x1, y1 = neighbor.get_pos()
        x2, y2 = end.get_pos()

        return abs(x1-x2) + abs(y1-y2)


    '''
        =========================== START OF MAIN FUNCTION =========================== 
    '''
    way = []
    open = PriorityQueue()
    closed = []
    parents = {}
    total_bonus = 0

    # Khởi tạo hàm chi phí ban đầu
    g = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    # g_start = 1
    # (f_n, (pos))
    cur_start = start
    g[start.get_pos()[0]][start.get_pos()[1]] = 1

    bonus_priorities, bonus_other = compact_bonus(bonus, start, end)

    '''
        - Với mỗi điểm trong bonus_priorities sẽ duyệt, sau khi duyệt, kiểm tra vị trí các điểm gần nhất thỏa điều kiện F thì sẽ duyệt các điểm đó cho 
        - Hàm F sẽ là tính khoảng cách giữa điểm đang xét tới 1 điểm lớn nhất bên kia + điểm bên kia + tới điểm tiếp theo bên này + bonus:
            - Nếu nó vẫn < 0 thì mình sẽ duyệt ngược lại thì xét các điểm nhỏ dần
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
                    g_n = 1 + g[r][c]
                    g[r_new][c_new] = g_n
                    h_n = heuristic_1(neighbor, cur_end) 
                    f_n = g_n + h_n
                    open.put((f_n, (r_new, c_new)))

                    parents[(r_new, c_new)] = (r, c)

            clock.tick(FPS)
            draw()

    open = PriorityQueue()
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
                g_n = 1 + g[x_cur][y_cur]
                g[x_new][y_new] = g_n
                h_n = heuristic_1(neighbor, end) 
                f_n = g_n + h_n
                open.put((f_n, (x_new, y_new)))

                parents[(x_new, y_new)] = (x_cur, y_cur)
        
        clock.tick(FPS)
        draw()

