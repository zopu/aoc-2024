import re


def main():
    input = open("../input/real/day3_1.txt")
    part1 = sum(
        [
            int(a) * int(b)
            for (a, b) in re.findall(
                r"mul\((\d+),(\d+)\)", input.read().replace("\n", "")
            )
        ]
    )
    print(part1)

    input = open("../input/real/day3_1.txt")
    uptodont = re.split(r"don't\(\)", input.read().replace("\n", ""))
    oksplits = [re.split(r"do\(\)", substr) for substr in uptodont[1:]]
    ok = [uptodont[0]]
    for s in oksplits:
        if len(s) > 1:
            ok.extend(s[1:])

    part2 = sum(
        [
            sum(
                [int(a) * int(b) for (a, b) in re.findall(r"mul\((\d+),(\d+)\)", split)]
            )
            for split in ok
        ]
    )
    print(part2)


if __name__ == "__main__":
    main()
