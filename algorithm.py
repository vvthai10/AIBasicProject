from queue import PriorityQueue

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
  