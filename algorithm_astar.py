from function import *


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

            way.insert(0,end.get_pos())   
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

            way.insert(0,end.get_pos())   
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
