import math
from queue import PriorityQueue
import re


dirs = [[1, 0, "S"], [-1, 0, "N"], [0, 1, "E"], [0, -1, "W"]]


def in_bounds(grid, pos):
    if pos[0] < 0 or pos[0] >= len(grid):
        return False
    if pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return False
    return True


def print_grid(grid, t):
    for i in range(len(grid)):
        line = grid[i]
        line_str = []
        for e in line:
            if e == -1 or e >= t:
                line_str.append(" ")
            else:
                line_str.append(str(e))
        print("".join(line_str))


def find_shortest_path_len(grid, start, end, t):
    open_q = PriorityQueue()
    open_q.put((0, 0, start))
    closed_list = set()
    while not open_q.empty():
        (_, g_parent, pos) = open_q.get()
        if pos in closed_list:
            continue
        closed_list.add(pos)
        if pos == end:
            return g_parent
        for d in dirs:
            np = (pos[0] + d[0], pos[1] + d[1])
            if np in closed_list:
                continue
            if not in_bounds(grid, np):
                continue
            val = grid[np[0]][np[1]]
            if val < t and val != -1:
                continue
            h = math.sqrt((end[0] - np[0]) ** 2 + (end[1] - np[1]) ** 2)
            g = g_parent + 1
            f = g + h

            found_lower = False
            for _, og, opos in open_q.queue:
                if opos == np and og < g:
                    found_lower = True
                    break
            if found_lower:
                continue
            open_q.put((f, g, np))
    return -1


def main():
    f = open("../input/real/day18_1.txt")
    # f = open("../input/sample/day18_1.txt")
    coords = [re.findall(r"(\d+)", line) for line in f.readlines()]
    incoming = [(int(x), int(y)) for [x, y] in coords]
    # X, Y = 7, 7
    # T = 12
    X, Y = 71, 71
    T = 1024
    grid = []
    for _ in range(X):
        line = []
        for _ in range(Y):
            line.append(-1)
        grid.append(line)

    for i, (a, b) in enumerate(incoming):
        if grid[a][b] == -1:
            grid[a][b] = i
    print_grid(grid, T)

    shp = find_shortest_path_len(grid, (0, 0), (X - 1, Y - 1), T)

    i = T
    while True:
        shp = find_shortest_path_len(grid, (0, 0), (X - 1, Y - 1), i)
        if shp == -1:
            print("No path found")
            print(incoming[i - 1])
            break
        i += 1


if __name__ == "__main__":
    main()
