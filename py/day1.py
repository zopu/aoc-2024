import re


def main():
    input = open("../input/real/day1_1.txt")
    l = []  # noqa: E741
    r = []
    for line in input:
        nums = re.findall(r"\d+", line)
        l.append(int(nums[0]))
        r.append(int(nums[1]))

    l.sort()
    r.sort()
    sum = 0
    for a, b in zip(l, r):
        sum += abs(a - b)

    # Part 1
    print(sum)

    sum = 0
    j = 0
    last_sim_score = 0
    for i in range(len(l)):
        if i < len(l) and l[i] == l[i - 1]:
            sum += last_sim_score
            continue
        if j >= len(r) - 1:
            break
        while r[j] < l[i]:
            j += 1
        sim_score = 0
        while r[j] == l[i]:
            sim_score += l[i]
            j += 1
        sum += sim_score
        last_sim_score = sim_score

    # Part 2
    print(sum)


if __name__ == "__main__":
    main()
