import re


# Returns (is_valid, idx of first problem)
def check(report):
    if report[1] == report[0]:
        return (False, 1)
    if report[1] > report[0]:  # Ascending
        cond = [a >= b or a + 3 < b for (a, b) in zip(report, report[1:])]
    else:  # Descending
        cond = [a <= b or a > b + 3 for (a, b) in zip(report, report[1:])]
    try:
        idx = cond.index(True)
        return (False, idx + 1)
    except ValueError:
        return (True, 0)


def main():
    input = open("../input/real/day2_1.txt")
    parsed = [[int(n) for n in re.findall(r"\d+", line)] for line in input]

    # Part 1
    print([check(r) for r in parsed].count((True, 0)))

    # Part 2
    sum = 0
    for report in parsed:
        c = check(report)
        if c[0]:
            sum += 1
        else:
            tests = [
                report,
                report[: c[1]] + report[c[1] + 1 :],
                report[: c[1] - 1] + report[c[1] :],
                report[1:],
                [report[0]] + report[2:],
            ]

            if any(check(t)[0] for t in tests):
                sum += 1

    print(sum)


if __name__ == "__main__":
    main()
