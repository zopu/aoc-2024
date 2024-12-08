import math


def in_bounds(grid, pos):
    if pos[0] < 0 or pos[0] >= len(grid):
        return False
    if pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return False
    return True


def norm_direction(a, b):
    raw_dir = (b[0] - a[0], b[1] - a[1])
    l = math.sqrt(raw_dir[0] ** 2 + raw_dir[1] ** 2)  # noqa: E741
    if l == 0:
        return (0, 0)
    dir = (raw_dir[0] / l, raw_dir[1] / l)
    if dir[0] < 0:
        dir = (-dir[0], -dir[1])
    return dir


def close_enough(a, b, threshold):
    return abs(a[0] - b[0]) < threshold and abs(a[1] - b[1]) < threshold


def main():
    input = open("../input/real/day8_1.txt")
    grid = [list(line.strip()) for line in input.readlines()]

    # Scan the grid for an index of all the letters
    char_locations = {}
    for i, line in enumerate(grid):
        for j, elem in enumerate(line):
            if elem not in [".", "\n"]:
                elem_locs = char_locations.get(elem, [])
                elem_locs.append((i, j))
                char_locations[elem] = elem_locs

    antinodes = [["." for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for char in char_locations:
        for a in char_locations[char]:
            for b in char_locations[char]:
                if a == b:
                    continue
                # Find the coordinates of the four points
                # on the line between a and b
                # where the distance from b is 2* the distance from a

                # WTF why does this work with only one point?
                # (How does it get the points that are between a and b?)
                p1 = (a[0] - (b[0] - a[0]), a[1] - (b[1] - a[1]))
                if in_bounds(grid, p1):
                    antinodes[p1[0]][p1[1]] = "X"

    print("Part 1: ", sum([row.count("X") for row in antinodes]))

    antinodes = [["." for _ in range(len(grid[0]))] for _ in range(len(grid))]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if antinodes[i][j] == "X":
                continue
            if grid[i][j] != ".":
                antinodes[i][j] = "X"
                continue
            for char in char_locations:
                dirs = [
                    norm_direction((i, j), antenna) for antenna in char_locations[char]
                ]
                dirs.sort()
                for k in range(len(dirs) - 1):
                    if close_enough(dirs[k], dirs[k + 1], 0.0000001):
                        antinodes[i][j] = "X"

    print("Part 2: ", sum([row.count("X") for row in antinodes]))


if __name__ == "__main__":
    main()
