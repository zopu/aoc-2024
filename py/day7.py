import re


def find_match(target, components):
    if len(components) == 0:
        return False
    if len(components) == 1:
        return target == components[0]
    if find_match(target - components[len(components) - 1], components[:-1]):
        return True
    if find_match(target / components[len(components) - 1], components[:-1]):
        return True
    return False


def find_match_p2(target, components):
    if len(components) == 0:
        return False
    if len(components) == 1:
        return target == components[0]
    if find_match_p2(target - components[len(components) - 1], components[:-1]):
        return True
    if find_match_p2(target / components[len(components) - 1], components[:-1]):
        return True
    if len(components) > 1:
        # To combine the rest as if we're cononcatenating strings
        # That's equivalent to multiplying the rest by a power of 10
        # and then adding the digits from the last number
        # so we do that in inverse here
        new_target = target - components[len(components) - 1]
        num_digits = len(str(components[len(components) - 1]))
        new_target /= 10**num_digits
        return find_match_p2(new_target, components[:-1])
    return False


def main():
    input = open("../input/real/day7_1.txt")
    lines = [[int(n) for n in re.findall(r"\d+", line)] for line in input.readlines()]

    # n^2 first
    sum = 0
    for line in lines:
        if find_match(line[0], line[1:]):
            sum += line[0]

    # Part 1
    print(sum)

    sum = 0
    for line in lines:
        if find_match_p2(line[0], line[1:]):
            sum += line[0]

    print(sum)


if __name__ == "__main__":
    main()
