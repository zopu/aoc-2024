from functools import cache
import re

towels = []
regex = ""


@cache
def count_matches(pattern):
    if len(pattern) == 0:
        return 1
    m = re.fullmatch(regex, pattern)
    if m is None:
        return 0
    sum = 0
    for t in towels:
        if len(pattern) >= len(t) and pattern[0 : len(t)] == t:
            sum += count_matches(pattern[len(t) :])
    return sum


def main():
    global towels, regex
    f = open("../input/real/day19_1.txt")
    towels = f.readline().strip().split(", ")
    print(towels)
    regex = "(" + "|".join(towels) + ")+"
    print(regex)
    f.readline()  # skip  the empty line
    sum = 0
    patterns = [line.strip() for line in f.readlines()]
    for pattern in patterns:
        m = re.fullmatch(regex, pattern)
        if m is not None:
            sum += 1

    # Part 1
    print(sum)

    sum = 0
    for pattern in patterns:
        sum += count_matches(pattern)

    print(sum)


if __name__ == "__main__":
    main()
