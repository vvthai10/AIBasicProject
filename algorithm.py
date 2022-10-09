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
  