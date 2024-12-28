import collections
import math
import re


def quadrant(x, y, X, Y):
    mid_x = math.floor(X / 2)
    mid_y = math.floor(Y / 2)
    if x == mid_x or y == mid_y:
        return None
    if x < mid_x and y < mid_y:
        return 0
    if x > mid_x and y < mid_y:
        return 1
    if x < mid_x and y > mid_y:
        return 2
    return 3


def get_positions(parsed, grid_size, steps):
    return [
        [
            (parsed[i][0] + parsed[i][2] * steps) % grid_size[0],
            (parsed[i][1] + parsed[i][3] * steps) % grid_size[1],
        ]
        for i in range(len(parsed))
    ]


def print_positions(poss, grid_size):
    for j in range(grid_size[1]):
        for i in range(grid_size[0]):
            if [i, j] in poss:
                print("X", end="")
            else:
                print(".", end="")
        print()


def clustered(poss):
    dirs = [(1, 0), (0, 1), (-1, 0), (0, -1)]
    count = 0
    for p in poss:
        if any([p[0] + d[0], p[1] + d[1]] in poss for d in dirs):
            count += 1
        if count > 250:
            return True
    return False


def main():
    inp = open("../input/real/day14_1.txt")

    parsed = [[int(n) for n in re.findall(r"-?\d+", line)] for line in inp]
    steps = 100
    grid_size = [101, 103]
    # grid_size = [11, 7]  # for sample
    final_pos = get_positions(parsed, grid_size, steps)

    qa = [quadrant(p[0], p[1], grid_size[0], grid_size[1]) for p in final_pos]
    counter = collections.Counter(qa)

    # Part 1
    print(counter[0] * counter[1] * counter[2] * counter[3])

    step_count = 0
    while True:
        poss = get_positions(parsed, grid_size, step_count)
        if clustered(poss):
            # print_positions(poss, grid_size)

            # Part 2
            print(step_count)
            break
        step_count += 1

    # Part 2
    print(step_count)


if __name__ == "__main__":
    main()
