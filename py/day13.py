import re


def find_min_tokens(machine):
    a = [machine[0], machine[1]]
    b = [machine[2], machine[3]]
    target = [machine[4], machine[5]]

    # Use Cramer's rule
    det = a[0] * b[1] - a[1] * b[0]
    na = (b[1] * target[0] - b[0] * target[1]) / det
    nb = (a[0] * target[1] - a[1] * target[0]) / det
    if na == int(na) and nb == int(nb):
        # have an integer solution
        return int(3 * na + nb)
    return None


def main():
    input = open("../input/real/day13_1.txt")

    machines = re.findall(
        r"Button A: X\+(\d+), Y\+(\d+)\nButton B: X\+(\d+), Y\+(\d+)\nPrize: X=(\d+), Y=(\d+)",
        input.read(),
    )

    sum = 0
    for m in machines:
        mt = find_min_tokens([int(n) for n in m])
        if mt is not None:
            sum += mt

    # Part 1
    print(sum)

    sum = 0
    for m in machines:
        m = [int(n) for n in m]
        m[4] += 10000000000000
        m[5] += 10000000000000
        mt = find_min_tokens(m)
        if mt is not None:
            sum += mt

    # Part 2
    print(sum)


if __name__ == "__main__":
    main()
