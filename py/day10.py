dirs = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def in_bounds(grid, pos):
    if pos[0] < 0 or pos[0] >= len(grid):
        return False
    if pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return False
    return True


# Returns a set of reachable 9 locations from here
def find_trail_ends(grid, from_pos, from_height):
    found_nines = set()
    for dir in dirs:
        if from_height == 9:
            return {from_pos}
        pos = (from_pos[0] + dir[0], from_pos[1] + dir[1])
        if in_bounds(grid, pos) and grid[pos[0]][pos[1]] == from_height + 1:
            found_nines.update(find_trail_ends(grid, pos, from_height + 1))
    return found_nines


def count_trails(grid, from_pos, from_height):
    total = 0
    for dir in dirs:
        if from_height == 9:
            return 1
        pos = (from_pos[0] + dir[0], from_pos[1] + dir[1])
        if in_bounds(grid, pos) and grid[pos[0]][pos[1]] == from_height + 1:
            total += count_trails(grid, pos, from_height + 1)
    return total


def main():
    input = open("../input/real/day10_1.txt")
    grid = [[int(c) for c in line.strip()] for line in input.readlines()]

    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                # Have a trailhead
                rn = find_trail_ends(grid, (i, j), 0)
                total += len(rn)

    # Part 1
    print(total)

    total = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == 0:
                rating = count_trails(grid, (i, j), 0)
                total += rating

    # Part 2
    print(total)


if __name__ == "__main__":
    main()
