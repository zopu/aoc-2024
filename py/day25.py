from itertools import batched, product


def read_lock(str8lines):
    lock = [0] * 5
    for line in str8lines[1:-1]:
        for i, char in enumerate(line):
            if char == "#":
                lock[i] += 1
    return lock


def read_key(str8lines):
    key = [0] * 5
    for line in str8lines[-3:0:-1]:
        for i, char in enumerate(line):
            if char == "#":
                key[i] += 1
    return key


def is_fit(key, lock):
    print(f"checking {key} vs {lock}")
    for edge, pin in zip(key, lock):
        if (5 - pin) < edge:
            return False
    return True


def main():
    f = open("../input/real/day25_1.txt")
    bd = batched([line for line in f.readlines()], 8)
    locks = []
    keys = []
    for b in bd:
        if b[0].startswith("#"):
            locks.append(read_lock(b))
        else:
            keys.append(read_key(b))
    print("locks")
    print(locks)
    print("keys")
    print(keys)

    sum = 0
    for key, lock in product(keys, locks):
        if is_fit(key, lock):
            sum += 1
        # print(f"{key} vs {lock}: {ft}")
    print(f"Part 1: {sum}")


if __name__ == "__main__":
    main()
