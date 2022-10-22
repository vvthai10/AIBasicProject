from operator import length_hint


def read_file(file_name: str = 'maze.txt'):
    f = open(file_name, 'r')
    n_bonus_points, n_pickup_points, n_portal = map(int, next(f)[:-1].split(' '))
    bonus_points = []
    pickup_points = []
    portals = {}
    for i in range(n_bonus_points):
        x, y, reward = map(int, next(f)[:-1].split(' '))
        bonus_points.append((x, y, reward))

    for i in range(n_pickup_points):
        x, y = map(int, next(f)[:-1].split(' '))
        pickup_points.append((x, y))

    for i in range(n_portal):
        pos1, pos2 = map(str, next(f)[:-1].split('-'))
        x1, y1 = map(int, pos1.split(' '))
        x2, y2 = map(int, pos2.split(' '))
        portals[(x1, y1)] = (x2, y2)
        portals[(x2, y2)] = (x1, y1)

    text = f.read()
    maze = [list(i) for i in text.splitlines()]
    f.close()

    return maze, bonus_points, pickup_points, portals
