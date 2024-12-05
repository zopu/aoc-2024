def fix(update, rules_dict):
    for i in range(len(update)):
        if update[i] in rules_dict:
            for must_be_before in rules_dict[update[i]]:
                try:
                    idx = update[i:].index(must_be_before)
                    # swap the two
                    update[i], update[i + idx] = (
                        update[i + idx],
                        update[i],
                    )
                    # print(update)
                    return fix(update, rules_dict)
                except ValueError:
                    pass
    return update


def main():
    input = open("../input/real/day5_1.txt")
    rules = []
    updates = []
    for line in input:
        if "|" in line:
            rules.append([int(a) for a in line.strip().split("|")])
        if "," in line:
            updates.append([int(a) for a in line.strip().split(",")])

    # Convert rules to a dict of {page: pages before}
    rules_dict = {}
    for r in rules:
        if r[1] not in rules_dict:
            rules_dict[r[1]] = []
        rules_dict[r[1]].append(r[0])

    sum_p1 = 0
    sum_p2 = 0
    for update in updates:
        rules_ok = True
        for i in range(len(update)):
            if update[i] in rules_dict:
                for must_be_before in rules_dict[update[i]]:
                    if must_be_before in update[i:]:
                        rules_ok = False
        if rules_ok:
            mid = len(update) // 2
            sum_p1 += update[mid]
        else:
            fix(update, rules_dict)
            mid = len(update) // 2
            sum_p2 += update[mid]

    print(sum_p1)
    print(sum_p2)


if __name__ == "__main__":
    main()
