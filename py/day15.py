def in_bounds(grid, pos):
    if pos[0] < 0 or pos[0] >= len(grid):
        return False
    if pos[1] < 0 or pos[1] >= len(grid[pos[0]]):
        return False
    return True


def print_grid(grid, robot):
    for i in range(len(grid)):
        if i == robot[0]:
            s = grid[i].copy()
            s[robot[1]] = "@"
            print("".join(s))
        else:
            print("".join(grid[i]))


def move(grid, pos, dir, char=None):
    new_pos = [pos[0] + dir[0], pos[1] + dir[1]]
    if not in_bounds(grid, new_pos):
        return pos
    if grid[new_pos[0]][new_pos[1]] == ".":
        if char is not None:
            grid[new_pos[0]][new_pos[1]] = char
        grid[pos[0]][pos[1]] = "."
        return new_pos
    if grid[new_pos[0]][new_pos[1]] == "#":
        return pos
    if grid[new_pos[0]][new_pos[1]] == "O":
        mv = move(grid, new_pos, dir, "O")
        if mv != new_pos:
            # char has been moved
            if char is not None:
                grid[new_pos[0]][new_pos[1]] = char
                grid[pos[0]][pos[1]] = "."
            return new_pos
    return pos


def can_move(grid, pos, dir):
    new_pos = [pos[0] + dir[0], pos[1] + dir[1]]
    # print(new_pos, dir)
    if not in_bounds(grid, new_pos):
        return False
    match (grid[new_pos[0]][new_pos[1]], dir):
        case (".", _):
            return True
        case ("#", _):
            return False
        # Up/down cases need to check both sides independently
        case ("[", [1, 0]) | ("[", [-1, 0]):
            return can_move(grid, new_pos, dir) and can_move(
                grid, [new_pos[0], new_pos[1] + 1], dir
            )
        case ("]", [1, 0]) | ("]", [-1, 0]):
            return can_move(grid, [new_pos[0], new_pos[1] - 1], dir) and can_move(
                grid, new_pos, dir
            )
        # Going left
        case ("]", [0, -1]):
            return can_move(grid, [new_pos[0], new_pos[1] - 1], dir)
        # Going right
        case ("[", [0, 1]):
            return can_move(grid, [new_pos[0], new_pos[1] + 1], dir)
        case _:
            print("char: ", grid[new_pos[0]][new_pos[1]])
            print(dir)
            raise Exception("Unhandled case")


def shift_box(grid, pos, dir):
    # Assumes that pos is the location of the lhs of the box i.e. "["
    # print(f"Shifting box at {pos} in direction {dir}")
    new_pos_l = [pos[0] + dir[0], pos[1] + dir[1]]
    new_pos_r = [pos[0] + dir[0], pos[1] + dir[1] + 1]
    # print(grid[new_pos_l[0]][new_pos_l[1]], grid[new_pos_r[0]][new_pos_r[1]])
    match (grid[new_pos_l[0]][new_pos_l[1]], grid[new_pos_r[0]][new_pos_r[1]], dir):
        case (".", ".", _):
            # Nothing to do
            pass
        case ("[", "]", _):
            shift_box(grid, new_pos_l, dir)
        case ("]", ".", [0, 1]):  # Right:
            pass
        case ("]", ".", _):
            shift_box(grid, [new_pos_l[0], new_pos_l[1] - 1], dir)
        case (".", "[", [0, -1]):  # Left:
            pass
        case (".", "[", _):
            shift_box(grid, [new_pos_r[0], new_pos_r[1]], dir)
        case ("]", "[", [_, 0]):  # Up/down
            shift_box(grid, [new_pos_l[0], new_pos_l[1] - 1], dir)
            shift_box(grid, [new_pos_r[0], new_pos_r[1]], dir)
        case ("]", "[", [0, -1]):  # Left
            shift_box(grid, [new_pos_l[0], new_pos_l[1] - 1], dir)
        case ("]", "[", [0, 1]):  # Right
            shift_box(grid, [new_pos_r[0], new_pos_r[1]], dir)
        case _:
            raise Exception("Unhandled case")
    grid[new_pos_l[0]][new_pos_l[1]] = "["
    grid[new_pos_r[0]][new_pos_r[1]] = "]"
    # Now clear the squares we vacated
    match dir:
        case [_, 0]:
            grid[pos[0]][pos[1]] = "."
            grid[pos[0]][pos[1] + 1] = "."
        case [0, -1]:  # Left
            grid[pos[0]][pos[1] + 1] = "."
        case [0, 1]:  # Right
            grid[pos[0]][pos[1]] = "."


def shift_boxes(grid, pos, dir, char):
    print(f"Shifting {char} at {pos} in direction {dir}")
    print("Grid line: ", "".join(grid[pos[0]]))
    new_pos = [pos[0] + dir[0], pos[1] + dir[1]]
    existing_char = grid[new_pos[0]][new_pos[1]]
    grid[new_pos[0]][new_pos[1]] = "."
    match existing_char:
        case ".":
            grid[new_pos[0]][new_pos[1]] = char
            print("Shifted without moving")
        case "#":
            raise Exception("Shouldn't encounter a wall")
        case "[":
            shift_boxes(grid, new_pos, dir, "[")
            shift_boxes(grid, [new_pos[0], new_pos[1] + 1], dir, "]")
            grid[new_pos[0]][new_pos[1]] = char
            grid[new_pos[0]][new_pos[1] + 1] = "."
            print("Shifted")
        case "]":
            shift_boxes(grid, [new_pos[0], new_pos[1] - 1], dir, "[")
            shift_boxes(grid, new_pos, dir, "]")
            grid[new_pos[0]][new_pos[1]] = char
            grid[new_pos[0]][new_pos[1] - 1] = "."
            print("Shifted")


def move_p2(grid, pos, dir):
    new_pos = [pos[0] + dir[0], pos[1] + dir[1]]
    if not can_move(grid, pos, dir):
        return pos
    match grid[new_pos[0]][new_pos[1]]:
        case ".":
            pass
        case "]":
            shift_box(grid, [new_pos[0], new_pos[1] - 1], dir)
        case "[":
            shift_box(grid, new_pos, dir)
    return new_pos


def main():
    f = open("../input/real/day15_1.txt")

    # Read the grid
    grid = []
    for line in f:
        if line.strip() == "":
            break
        grid.append([c for c in line.strip()])

    # Read the instructions
    instructions = list(f.read().strip().replace("\n", ""))

    # Find the robot
    robot = [-1, -1]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "@":
                grid[i][j] = "."
                robot = [i, j]
                break
    robot_start = robot.copy()

    # robot = [6, 4]
    grid_p1 = [line.copy() for line in grid]
    print_grid(grid_p1, robot)
    dirs = {"<": [0, -1], ">": [0, 1], "^": [-1, 0], "v": [1, 0]}
    for i in instructions:
        dir = dirs[i]
        robot = move(grid_p1, robot, dir)

    sum = 0
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "O":
                sum += 100 * i + j
    # Part 1
    print(sum)

    robot = robot_start
    print_grid(grid, robot)

    # Double up the grid
    grid_p2 = []
    for i in range(len(grid)):
        line = grid[i]
        current_line = []
        for j in range(len(line)):
            ch = line[j]
            # if robot == [i, j]:
            #     current_line.append("@.")
            if ch == "O":
                current_line.append("[")
                current_line.append("]")
            if ch == "#":
                current_line.append("#")
                current_line.append("#")
            if ch == ".":
                current_line.append(".")
                current_line.append(".")
        grid_p2.append(current_line)
    robot = [robot[0], robot[1] * 2]
    print_grid(grid_p2, robot)

    for i in instructions:
        dir = dirs[i]
        robot = move_p2(grid_p2, robot, dir)

    print_grid(grid_p2, robot)

    sum = 0
    for i in range(len(grid_p2)):
        for j in range(len(grid_p2[i])):
            if grid_p2[i][j] == "[":
                sum += 100 * i + j
    # Part 2
    print(sum)


if __name__ == "__main__":
    main()
