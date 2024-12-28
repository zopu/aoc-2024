import re


def tick(stones):
    new_stones = []
    for stone in stones:
        if stone == 0:
            new_stones.append(1)
            continue
        if len(str(stone)) % 2 == 0:
            old = str(stone)
            a = int(old[: len(old) // 2])
            b = int(old[len(old) // 2 :])
            new_stones.append(a)
            new_stones.append(b)
            continue
        new_stones.append(stone * 2024)
    return new_stones


def count_stones_after_steps(stones, steps, memo):
    if steps == 0:
        return len(stones)
    if steps == 1:
        return len(tick(stones))
    sum = 0
    for s in stones:
        memoized_count = memo.get(s, [-1 for _ in range(steps + 1)])
        if len(memoized_count) > steps and memoized_count[steps] != -1:
            sum += memoized_count[steps]
            continue
        result = count_stones_after_steps(tick([s]), steps - 1, memo)
        memoized_count = memo.get(s, [-1 for _ in range(steps + 1)])
        if len(memoized_count) < steps + 1:
            memoized_count += [-1 for _ in range(steps + 1 - len(memoized_count))]
        memoized_count[steps] = result
        memo[s] = memoized_count
        sum += result
    return sum


def main():
    input = open("../input/real/day11_1.txt")
    starting_stones = [int(n) for n in re.findall(r"\d+", input.read())]
    stones = starting_stones
    for _ in range(25):
        stones = tick(stones)

    # Part 1
    print(len(stones))

    memo = {}

    stones = starting_stones
    steps = 75
    c = count_stones_after_steps(stones, steps, memo)

    # Part 2
    print(c)


if __name__ == "__main__":
    main()
