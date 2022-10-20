from queue import PriorityQueue
import math

FPS = 10

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
            print("Chi phi duong di cua thuat toan DFS la: ", len(way))
            return True

        for neighbor in node.neighbors:
            if not neighbor.get_pos() in path:
                stack.append(neighbor.get_pos())
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
            print("Chi phi duong di cua thuat toan BFS: " , len(way))
            return True

        for neighbor in node.neighbors:
            # WARNING!!!!!!!!
            if not neighbor.get_pos() in path:
                queue.append(neighbor.get_pos())
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
            print("chi phi duong di cua ucs: ", len(way))
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

                    reconstruct_path(way, grid, draw, clock)
                    print(f"Chi phi duong di voi thuat toan Greedy_BFS: {dist[end.get_pos()[0]][end.get_pos()[1]]}")
                    return True

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
    open.put(( 1 + heuristic_1(start, end), (start.get_pos())))

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
            print(f"Chi phí đường đi của thuật toán A*: {g[x_cur][y_cur]}" )
            return True
        
        if not grid[x_cur][y_cur].is_start():
            grid[x_cur][y_cur].make_open()

        closed.append((x_cur, y_cur))
        for neighbor in grid[x_cur][y_cur].neighbors:
            # WARNING!!!!!!!!
            x_new, y_new = neighbor.get_pos()
            if not (x_new, y_new) in closed:
                g_n = 1 + g[x_cur][y_cur]
                g[x_new][y_new] = g_n;
                h_n = heuristic_1(neighbor, end) 
                f_n = g_n + h_n
                open.put((f_n, (x_new, y_new)))

                parents[(x_new, y_new)] = (x_cur, y_cur)
        
        clock.tick(FPS)
        draw()


# Cách 1: Dùng góc nhọn + điểm cao nhất -> Thất bại
# Cách 2: ...
# Cách 3: Dùng các điểm trong phạm vi giới hạn trong hình nhật từ điểm hiện tại đến kết thúc
    #Lọc ra những điểm nằm cùng phía -> Sắp xếp xa dần điểm đầu, sẽ có 2 nữa trên dưới với đường phân cách là đường chéo hcn đầu cuối
    # Sẽ dùng h_n tính khoảng cách từ nó tới đính và khoảng cách từ nó tới điểm gần đó + gần đó tới đích + bonus -> Nếu chi phí rẻ hơn thì đi ko thì thôi.
# Sẽ tìm khoảng cách từ điểm hiện tại cho tới điểm thỏa mãn


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
    g[start.get_pos()[0]][start.get_pos()[1]] = 0;

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

def algorithm_bonus_pickup_astar(draw, grid, bonus, pickups, start, end, clock):
    def check_points_in_area(top, down, point, approxi):
        max_r = max(top[0], down[0]) + approxi
        min_r = min(top[0], down[0]) - approxi
        max_c = max(top[1], down[1]) + approxi
        min_c = min(top[1], down[1]) - approxi

        print(f"check {point} in range {top} and {down}")
        if point[0] in range(min_r, max_r) and point[1] in range(min_c, max_c):
            return True

        return False

    def calc_space_2_points(A, B):
        return math.sqrt((A[0] - B[0]) ** 2 + (A[1] - B[1]) ** 2 )

    def get_points_areas():
        end_pos = end.get_pos()
        start_pos = start.get_pos()

        # Phạm vi khu vực 1: Start => góc dưới ngược với góc của điểm end
        r_bottom = (len(grid) - 1) if (end_pos[0] < start_pos[0]) else 0
        c_bottom = (len(grid[0])  - 1) if (end_pos[1] == 0) else 0

        # Phạm vi khu vực 1: Start => góc trên ngược với góc của điểm end
        r_top = (len(grid) - 1) if (end_pos[0] > start_pos[0]) else 0
        c_top = (len(grid[0])  - 1) if (end_pos[1] == 0) else 0

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


        while not pickups.empty():
            (r_cur, c_cur) = pickups.get()
            if check_points_in_area(start_pos, (r_bottom, c_bottom), (r_cur, c_cur), 0):
                pickups_1.put((calc_space_2_points(start_pos, (r_cur, c_cur)), (r_cur, c_cur)))
            elif check_points_in_area(start_pos, (r_top, c_top), (r_cur, c_cur), 0):
                pickups_2.put((calc_space_2_points(start_pos, (r_cur, c_cur)), (r_cur, c_cur)))
            elif check_points_in_area((len(grid) - 1, start_pos[1]), (0, c_center), (r_cur, c_cur), 0):
                pickups_3.put((calc_space_2_points(start_pos, (r_cur, c_cur)), (r_cur, c_cur)))
            else:
                pickups_4.put((calc_space_2_points(start_pos, (r_cur, c_cur)), (r_cur, c_cur)))

        while not bonus.empty():
            value, (r_cur, c_cur) = bonus.get()
            if check_points_in_area(start_pos, (r_bottom, c_bottom), (r_cur, c_cur), 0):
                bonus_1.put((value, (r_cur, c_cur)))
            elif check_points_in_area(start_pos, (r_top, c_top), (r_cur, c_cur), 0):
                bonus_2.put((value, (r_cur, c_cur)))
            elif check_points_in_area((len(grid) - 1, start_pos[1]), (0, c_center), (r_cur, c_cur), 0):
                bonus_3.put((value, (r_cur, c_cur)))
            else:
                bonus_4.put((value, (r_cur, c_cur)))
        
        # while not bonus_1.empty():
        #     value, (r, c) = bonus_1.get()
        #     print(f"Bonus 1 value{value}, Pos: {(r, c)}")

        # while not bonus_2.empty():
        #     value, (r, c) = bonus_2.get()
        #     print(f"Bonus 2 value{value}, Pos: {(r, c)}")

        # while not bonus_3.empty():
        #     value, (r, c) = bonus_3.get()
        #     print(f"Bonus 3 value{value}, Pos: {(r, c)}")

        # while not bonus_4.empty():
        #     value, (r, c) = bonus_4.get()
        #     print(f"Bonus 4 value{value}, Pos: {(r, c)}")

        return pickups_1, pickups_2, pickups_3, pickups_4, bonus_1, bonus_2, bonus_3, bonus_4 

    def handle_pickups(pickups, bonus, start_cur_pos, end_cur_pos ):
        while not pickups.empty():
            space, (end_cur_pos) = pickups.get()
            
            # Đầu tiên kiểm tra có điểm bonus nào trong khoảng này mà kc từ start -> pickup <= start -> bonus + bonus -> pickup + value
            backup_bonus = PriorityQueue()
            while not bonus.empty():
                value, (bonus_pos) = bonus.get()
                print(f"Check {bonus_pos} with: {value} in range ")
                if check_points_in_area(start_cur_pos, end_cur_pos, bonus_pos, 2):
                    print("Hello")
                    start_pickup = calc_space_2_points(start_cur_pos, end_cur_pos)
                    start_bonus = calc_space_2_points(start_cur_pos, bonus_pos)
                    bonus_pickup = calc_space_2_points(bonus_pos, end_cur_pos)

                    # Nếu này là điểm được chọn
                    if start_pickup <= start_bonus + bonus_pickup + value:
                        print(f"Choose bonus: {bonus_pos}")
                        pickups.put((space, end_cur_pos))
                        end_cur_pos = bonus_pos
                        while not backup_bonus.empty():
                            v, (r, c) = backup_bonus.get()
                            bonus.put(v, (r, c))
                        break
                    else:
                        backup_bonus.put((space, bonus_pos))
                else:
                    backup_bonus.put((space, bonus_pos))
            
            while not backup_bonus.empty():
                v, (r, c) = backup_bonus.get()
                bonus.put(v, (r, c))  

            g[start_cur_pos[0]][start_cur_pos[1]] = 1
            g_n = g[start_cur_pos[0]][start_cur_pos[1]]
            h_n = heuristic_1(start_cur_pos, end_cur_pos)
            f_n = g_n + h_n
            opens.put((f_n, start_cur_pos))

            while not opens.empty():
                f_prev, (cur_pos) = opens.get()

                closed.append(cur_pos)

                if cur_pos == end_cur_pos:
                    print(f"From {start_cur_pos} to {end_cur_pos}")
                    start_cur_pos = end_cur_pos
                    break

                if cur_pos != start_pos and cur_pos != end_pos:
                    grid[cur_pos[0]][cur_pos[1]].make_open()

                for neighbor in grid[cur_pos[0]][cur_pos[1]].neighbors:
                    # WARNING!!!!!!!!
                    new_pos = neighbor.get_pos()
                    if not new_pos in closed:
                        # NOTE: g[r][c].get_bonus()
                        g_n = 1 + g[cur_pos[0]][cur_pos[1]]
                        g[new_pos[0]][new_pos[1]] = g_n
                        h_n = heuristic_1(new_pos, end_cur_pos) 
                        f_n = g_n + h_n
                        opens.put((f_n, new_pos))

                        parents[new_pos] = cur_pos
                
                clock.tick(FPS)
                draw()

    def heuristic_1(neighbor, end):
        x1, y1 = neighbor
        x2, y2 = end

        return (x1 - x2) ** 2 + (y1 - y2) ** 2

    def heuristic_2(neighbor, end):
        x1, y1 = neighbor
        x2, y2 = end

        return abs(x1-x2) + abs(y1-y2)


    pickups_1, pickups_2, pickups_3, pickups_4, bonus_1, bonus_2, bonus_3, bonus_4  = get_points_areas()

    way = []
    opens = PriorityQueue()
    closed = []
    parents = {}

    # Tính toán hàm g
    g = [[0 for _ in range(len(grid[0]))] for _ in range(len(grid))]

    start_pos = start.get_pos()
    end_pos = end.get_pos()

    start_cur_pos = start_pos
    end_cur_pos = None

    # handle_pickups(pickups_1, bonus_1)
    # handle_pickups(pickups_2, bonus_2)
    handle_pickups(pickups_3, bonus_3, start_cur_pos, end_cur_pos)
    # handle_pickups(pickups_4, bonus_4)
    print("Finish")
    







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