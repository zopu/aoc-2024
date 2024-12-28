from queue import PriorityQueue

dirs = [[1, 0, "S"], [-1, 0, "N"], [0, 1, "E"], [0, -1, "W"]]


def in_bounds(grid, pos):
    if pos[0] < 0 or pos[0] >= len(grid):
        return False
    if pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return False
    return True


def is_node(grid, pos):
    # If more than two directions are possible, it's a node
    [i, j] = pos
    if grid[i][j] == ".":
        count = 0
        for dir in dirs:
            [ni, nj] = [i + dir[0], j + dir[1]]
            if in_bounds(grid, [ni, nj]) and grid[ni][nj] == ".":
                count += 1
            if count > 2:
                return True
    return False


# extras of the form [[(row, col), char]]
def print_grid(grid, extras=[]):
    for i in range(len(grid)):
        s = grid[i].copy()
        for extra in extras:
            if i == extra[0][0]:
                s[extra[0][1]] = extra[1]
        print("".join(s))


# returns [next_node, cost, end_direction, length]
def follow_edge(grid, nodes, pos, dir):
    next_pos = (pos[0] + dir[0], pos[1] + dir[1])
    if next_pos in nodes:
        return [next_pos, 1, dir, 1]

    if grid[next_pos[0] + dir[0]][next_pos[1] + dir[1]] == ".":
        [next_node, cost, end_dir, length] = follow_edge(grid, nodes, next_pos, dir)
        return [next_node, cost + 1, end_dir, length + 1]

    [dlx, dly] = [-1 * dir[1], dir[0]]
    [nx, ny] = [next_pos[0] + dlx, next_pos[1] + dly]
    if grid[nx][ny] == ".":
        [next_node, cost, end_dir, length] = follow_edge(
            grid, nodes, next_pos, [dlx, dly]
        )
        return [next_node, cost + 1001, end_dir, length + 1]
    [drx, dry] = [dir[1], -1 * dir[0]]
    [nx, ny] = [next_pos[0] + drx, next_pos[1] + dry]
    if grid[nx][ny] == ".":
        [next_node, cost, end_dir, length] = follow_edge(
            grid, nodes, next_pos, [drx, dry]
        )
        return [next_node, cost + 1001, end_dir, length + 1]
    return [None, -1, None, -1]


def main():
    f = open("../input/real/day16_1.txt")
    grid = [list(line.strip()) for line in f.readlines()]
    start = (0, 0)
    end = (0, 0)
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "S":
                start = (i, j)
                grid[i][j] = "."
            if grid[i][j] == "E":
                end = (i, j)
                grid[i][j] = "."
    print_grid(grid, [[start, "S"], [end, "E"]])

    # Create a directed graph where each edge is of the form:
    # [i, j, direction, end_direction, cost]
    # where direction is one of "N", "S", "E", "W"
    nodes = [(start[0], start[1]), (end[0], end[1])]
    edges = {}
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if is_node(grid, (i, j)):
                nodes.append((i, j))
                edges[(i, j)] = []

    edges[(start[0], start[1])] = []
    edges[(end[0], end[1])] = []

    # Compute the edges for each node
    for n in nodes:
        for dir in dirs:
            if (
                in_bounds(grid, [n[0] + dir[0], n[1] + dir[1]])
                and grid[n[0] + dir[0]][n[1] + dir[1]] == "."
            ):
                [to_node, cost, end_dir, length] = follow_edge(grid, nodes, n, dir)
                if to_node is not None:
                    edges[(n[0], n[1])].append([to_node, dir, end_dir, cost, length])

    best_cost = -1
    q = PriorityQueue()
    q.put((0, start, (0, 1), []))  # total cost, node, direction, visited list
    earliest_visited = {}
    for n in nodes:
        for d in dirs:
            earliest_visited[(n, d[0], d[1])] = -1
    best_paths = []
    while True:
        (cost, node, dir, path) = q.get()
        if best_cost != -1 and cost > best_cost:
            break
        if earliest_visited[(node, dir[0], dir[1])] != -1:
            if earliest_visited[(node, dir[0], dir[1])] < cost:
                continue
        else:
            earliest_visited[(node, dir[0], dir[1])] = cost
        if node == end:
            best_paths.append(path + [end])
            if best_cost == -1:
                best_cost = cost
                continue
        for [to, edge_dir, end_dir, edge_cost, length] in edges[node]:
            turn_cost = 0
            if edge_dir == -1 * dir:
                continue  # Don't go backwards
            if edge_dir[0] != dir[0] or edge_dir[1] != dir[1]:
                turn_cost = 1000
            total_cost = cost + edge_cost + turn_cost
            p = path.copy()
            p.append((node, to, edge_dir))
            q.put((total_cost, to, end_dir, p))

    # Part 1
    print(best_cost)

    best_path_edges = set()
    for path in best_paths:
        # Iterate over pairs of nodes, find the edge, add it to the set
        for i in range(len(path) - 1):
            for [to, edge_dir, end_dir, edge_cost, length] in edges[path[i][0]]:
                if to == path[i][1] and edge_dir == path[i][2]:
                    best_path_edges.add((path[i][0], to, edge_dir[2], length))
    sum = 0
    node_set = set()
    for e in best_path_edges:
        sum += e[3] - 1  # -1 bedcause we don't want to double count the end node
        node_set.add(e[0])
        node_set.add(e[1])

    sum += len(node_set)

    # Part 2
    print(sum)


if __name__ == "__main__":
    main()
