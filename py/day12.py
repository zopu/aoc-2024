def in_bounds(grid, pos):
    if pos[0] < 0 or pos[0] >= len(grid):
        return False
    if pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return False
    return True


def find_region(grid, start_pos, region=[set(), set()]):
    char = grid[start_pos[0]][start_pos[1]]
    if char == ".":
        return
    region[0].add(start_pos)
    dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]]
    for d in dirs:
        n = (start_pos[0] + d[0], start_pos[1] + d[1])
        if in_bounds(grid, n) and grid[n[0]][n[1]] == char and n not in region[0]:
            find_region(grid, n, region)
        else:
            # Add the edge
            if n not in region[0]:
                region[1].add((start_pos[0], start_pos[1], d[0], d[1]))


def mark_region(grid, region):
    for r in region[0]:
        grid[r[0]][r[1]] = "."


def count_sides(edges):
    # We can discount an edge if it is adjacent to another edge (IN ONE DIRECTION only)
    count = len(edges)
    n_edges = [e for e in edges if e[2] == -1 and e[3] == 0]
    n_edges.sort(key=lambda e: e[1])
    n_edges.sort(key=lambda e: e[0])
    for i in range(len(n_edges) - 1):
        if n_edges[i][0] == n_edges[i + 1][0]:  # same row
            j = n_edges[i][1]
            if n_edges[i + 1][1] == j + 1:  # adjacent columns
                count -= 1
    w_edges = [e for e in edges if e[2] == 0 and e[3] == -1]
    w_edges.sort(key=lambda e: e[0])
    w_edges.sort(key=lambda e: e[1])
    for i in range(len(w_edges) - 1):
        if w_edges[i][1] == w_edges[i + 1][1]:  # same column
            j = w_edges[i][0]
            if w_edges[i + 1][0] == j + 1:  # adjacent rows
                count -= 1
    s_edges = [e for e in edges if e[2] == 1 and e[3] == 0]
    s_edges.sort(key=lambda e: e[1])
    s_edges.sort(key=lambda e: e[0])
    for i in range(len(s_edges) - 1):
        if s_edges[i][0] == s_edges[i + 1][0]:  # same row
            j = s_edges[i][1]
            if s_edges[i + 1][1] == j + 1:  # adjacent columns
                count -= 1
    e_edges = [e for e in edges if e[2] == 0 and e[3] == 1]
    e_edges.sort(key=lambda e: e[0])
    e_edges.sort(key=lambda e: e[1])
    for i in range(len(e_edges) - 1):
        if e_edges[i][1] == e_edges[i + 1][1]:  # same column
            j = e_edges[i][0]
            if e_edges[i + 1][0] == j + 1:  # adjacent rows
                count -= 1
    return count


def main():
    input = open("../input/real/day12_1.txt")
    grid = [list(line.strip()) for line in input.readlines()]

    regions = []
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] != ".":
                r = [set(), set()]
                find_region(grid, (i, j), r)
                mark_region(grid, r)
                if len(r) > 0:
                    regions.append(r)

    sum = 0
    for r in regions:
        sum += len(r[0]) * len(r[1])

    # Part 1
    print(sum)

    sum = 0
    for r in regions:
        sides = count_sides(r[1])
        sum += len(r[0]) * sides

    # Part 2
    print(sum)


if __name__ == "__main__":
    main()
