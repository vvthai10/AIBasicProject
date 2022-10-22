from algorithms.shared_function import *


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

            way.insert(0,end.get_pos())   
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
                queue.put((value,(x_n,y_n)))
                parents[neighbor.get_pos()] = pos

        clock.tick(FPS)
        draw()

    return [], 0

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

    queue = PriorityQueue()
    queue.put((heuristic_2(start, end), (start.get_pos())))



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

            way.insert(0,end.get_pos())   
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
                queue.put((value,(x_n,y_n)))
                parents[neighbor.get_pos()] = pos

        clock.tick(FPS)
        draw()

    return [], 0
