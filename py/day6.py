def turn_right(dir):
    if dir == [1, 0]:
        return [0, -1]
    if dir == [0, 1]:
        return [1, 0]
    if dir == [-1, 0]:
        return [0, 1]
    if dir == [0, -1]:
        return [-1, 0]
    return dir


def in_bounds(grid, pos):
    if pos[0] < 0 or pos[0] >= len(grid):
        return False
    if pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return False
    return True


def check_for_loop(grid, start_pos, dir):
    # Seen dirs is a 4-bit number where each bit represents a direction
    # and the value is each of the directions we've seen at the current position
    # combined.
    # 0b0001 = up
    # 0b0010 = right
    # 0b0100 = down
    # 0b1000 = left
    seen_dirs = [[0 for _ in row] for row in grid]
    pos = start_pos
    while True:
        next_pos = [pos[0] + dir[0], pos[1] + dir[1]]
        if not in_bounds(grid, next_pos):
            return False
        if grid[next_pos[0]][next_pos[1]] in ["#", "O"]:
            dir = turn_right(dir)
            continue
        pos = next_pos
        sd = seen_dirs[pos[0]][pos[1]]
        if dir == [-1, 0]:
            if sd & 1 == 1:
                return True
            seen_dirs[pos[0]][pos[1]] |= 1
        if dir == [0, 1]:
            if sd & 2 == 2:
                return True
            seen_dirs[pos[0]][pos[1]] |= 2
        if dir == [1, 0]:
            if sd & 4 == 4:
                return True
            seen_dirs[pos[0]][pos[1]] |= 4
        if dir == [0, -1]:
            if sd & 8 == 8:
                return True
            seen_dirs[pos[0]][pos[1]] |= 8


def main():
    input = open("../input/real/day6_1.txt")
    grid = [list(line) for line in input.readlines()]
    start_pos = [0, 0]
    start_dir = [1, 0]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            elem = grid[i][j]
            if grid[i][j] in ["^", "v", "<", ">"]:
                start_pos = [i, j]
                if elem == "^":
                    start_dir = [-1, 0]
                elif elem == "v":
                    start_dir = [1, 0]
                elif elem == "<":
                    start_dir = [0, -1]
                elif elem == ">":
                    start_dir = [0, 1]
                grid[i][j] = "."

    pos = start_pos
    dir = start_dir
    while True:
        grid[pos[0]][pos[1]] = "X"
        next_pos = [pos[0] + dir[0], pos[1] + dir[1]]
        if not in_bounds(grid, next_pos):
            break
        if grid[next_pos[0]][next_pos[1]] == "#":
            dir = turn_right(dir)
            continue
        pos = next_pos

    # Part 1
    print(sum([row.count("X") for row in grid]))

    count_loop_positions = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                grid[i][j] = "O"
                pos = start_pos
                dir = start_dir
                if check_for_loop(grid, pos, dir):
                    count_loop_positions += 1
                grid[i][j] = "X"

    # Part 2
    print(count_loop_positions)


if __name__ == "__main__":
    main()
