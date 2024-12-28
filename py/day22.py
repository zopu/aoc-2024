def next_secret(prev):
    prune_mod = 16777216
    # Calculate the result of multiplying the secret number by 64.
    a = prev * 64
    # Then, mix this result into the secret number. Finally, prune the secret number.
    n = a ^ prev
    n = n % prune_mod

    # Calculate the result of dividing the secret number by 32. Round the result down to the nearest integer. Then, mix this result into the secret number. Finally, prune the secret number.
    b = int(n / 32)
    n = b ^ n
    n = n % prune_mod

    # Calculate the result of multiplying the secret number by 2048. Then, mix this result into the secret number. Finally, prune the secret number
    c = n * 2048
    n = c ^ n
    n = n % prune_mod
    return n


def main():
    # f = open("../input/sample/day22_3.txt")
    f = open("../input/real/day22_1.txt")
    inp = [int(line) for line in f.readlines()]

    buyers = []
    sum = 0
    for i, n_0 in enumerate(inp):
        buyers.append([n_0])
        n = n_0
        for _ in range(2000):
            n = next_secret(n)
            buyers[i].append(n)
        sum += n

    print(f"Part 1: {sum}")

    diffs = []
    for b in buyers:
        diffs.append([second % 10 - first % 10 for first, second in zip(b, b[1:])])

    # Generate all possible sequences
    # and a data structure of (seq, buyer)->price
    seqs = set()
    seq_buys = {}
    for bi, buyer in enumerate(diffs):
        for i in range(len(buyer) - 4):
            seq = (buyer[i], buyer[i + 1], buyer[i + 2], buyer[i + 3])
            seqs.add(seq)
            if (seq, bi) not in seq_buys:
                seq_buys[(seq, bi)] = buyers[bi][i + 4] % 10
    print(f"len(seqs): {len(seqs)}")
    print(f"len(diffs[0]): {len(diffs[0])}")
    print(f"len(buyers): {len(buyers)}")

    most_bananas = 0
    for seq in seqs:
        sum = 0
        for i in range(len(buyers)):
            if (seq, i) in seq_buys:
                sum += seq_buys[(seq, i)]
        if sum > most_bananas:
            most_bananas = sum

    print(f"Part 2: {most_bananas}")


if __name__ == "__main__":
    main()
