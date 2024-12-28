dirs = [[1, 0, "S"], [-1, 0, "N"], [0, 1, "E"], [0, -1, "W"]]


def neighour_dirs_in_distance(dist):
    nbs = set()
    for i in range(dist + 1):
        nbs.add((dist - i, i))
        nbs.add((-dist + i, i))
        nbs.add((dist - i, -i))
        nbs.add((-dist + i, -i))
    return nbs


def neighour_dirs_in_distance_inclusive(dist):
    nbs = set()
    for d in range(2, dist + 1):
        for i in range(d + 1):
            nbs.add((d - i, i))
            nbs.add((-d + i, i))
            nbs.add((d - i, -i))
            nbs.add((-d + i, -i))
    return nbs


def in_bounds(grid, pos):
    if pos[0] < 0 or pos[0] >= len(grid):
        return False
    if pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return False
    return True


# extras of the form [[(row, col), char]]
def print_grid(grid, extras=[]):
    for i in range(len(grid)):
        s = grid[i].copy()
        for extra in extras:
            if i == extra[0][0]:
                s[extra[0][1]] = extra[1]
        print("".join(s))


# Returns a grid of ints with distances from the start (or -1 if unreachable)
def floodfill_distance(grid, start):
    dist_grid = []
    for i in range(len(grid)):
        dist_grid.append([-1] * len(grid[i]))
    q = [(0, start[0], start[1])]
    while q:
        (d, px, py) = q.pop()
        existing = dist_grid[px][py]
        if existing != -1 and existing <= d:
            continue
        if grid[px][py] == "#":
            continue
        dist_grid[px][py] = d
        neighbors = [(px + d[0], py + d[1]) for d in dirs]
        for n in neighbors:
            if in_bounds(grid, n) and grid[n[0]][n[1]] == ".":
                q.append((d + 1, n[0], n[1]))
    return dist_grid


def main():
    f = open("../input/real/day20_1.txt")

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

    dist_from_start = floodfill_distance(grid, start)
    dist_from_end = floodfill_distance(grid, end)

    # Collect cheats
    neighbour_dirs = neighour_dirs_in_distance(2)
    threshold = 100
    cheats = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if dist_from_start[i][j] != -1:
                for dir in neighbour_dirs:
                    npx, npy = i + dir[0], j + dir[1]
                    if not in_bounds(grid, [npx, npy]):
                        continue
                    de_start = dist_from_end[i][j]
                    de_end = dist_from_end[npx][npy]
                    if de_end == -1:
                        continue
                    if de_start != -1 and de_start <= de_end + threshold:
                        continue
                    cheats.add((i, j, npx, npy))

    no_cheat = dist_from_end[start[0]][start[1]]
    sum = 0
    for cheat in cheats:
        dist = (
            dist_from_start[cheat[0]][cheat[1]] + 2 + dist_from_end[cheat[2]][cheat[3]]
        )
        if no_cheat - dist >= threshold:
            sum += 1

    print(f"Part 1: {sum}")

    neighbour_dirs = neighour_dirs_in_distance_inclusive(20)
    threshold = 100
    cheats = set()
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if dist_from_start[i][j] != -1:
                for dir in neighbour_dirs:
                    npx, npy = i + dir[0], j + dir[1]
                    if not in_bounds(grid, [npx, npy]):
                        continue
                    de_start = dist_from_end[i][j]
                    de_end = dist_from_end[npx][npy]
                    if de_end == -1:
                        continue
                    if de_start != -1 and de_start <= de_end + threshold:
                        continue
                    cheats.add((i, j, npx, npy))

    no_cheat = dist_from_end[start[0]][start[1]]
    sum = 0
    for cheat in cheats:
        dist = (
            dist_from_start[cheat[0]][cheat[1]]
            + dist_from_end[cheat[2]][cheat[3]]
            + abs(cheat[0] - cheat[2])
            + abs(cheat[1] - cheat[3])
        )
        if no_cheat - dist >= threshold:
            sum += 1

    print(f"Part 2: {sum}")


if __name__ == "__main__":
    main()
