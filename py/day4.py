def check(grid, i, j, char):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[i]):
        return False
    return grid[i][j] == char


def get(grid, i, j):
    if i < 0 or i >= len(grid) or j < 0 or j >= len(grid[i]):
        return "."
    return grid[i][j]


def main():
    # input = open("../input/sample/day4_1.txt")
    input = open("../input/real/day4_1.txt")
    grid = []
    for line in input:
        grid.append([c for c in line.strip()])
    sum = 0
    dirs = [[1, 0], [-1, 0], [0, 1], [0, -1], [1, 1], [1, -1], [-1, 1], [-1, -1]]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "X":
                for dir in dirs:
                    if (
                        check(grid, i + dir[0], j + dir[1], "M")
                        and check(grid, i + dir[0] * 2, j + dir[1] * 2, "A")
                        and check(grid, i + dir[0] * 3, j + dir[1] * 3, "S")
                    ):
                        sum += 1
    # Part 1
    print(sum)

    sum = 0
    dirs = [[1, 1], [-1, -1], [1, 1], [-1, -1]]
    inverses = [[1, -1], [1, -1], [-1, 1], [-1, 1]]
    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if grid[i][j] == "A":
                for dir in zip(dirs, inverses):
                    if (
                        check(grid, i + dir[0][0], j + dir[0][1], "M")
                        and check(grid, i - dir[0][0], j - dir[0][1], "S")
                        and check(grid, i + dir[1][0], j + dir[1][1], "M")
                        and check(grid, i - dir[1][0], j - dir[1][1], "S")
                    ):
                        sum += 1
    # Part 2
    print(sum)


if __name__ == "__main__":
    main()
