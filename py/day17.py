import re


def tick(program, ip, r, output):
    # print(f"ip={ip}")
    opcode = program[ip]
    operand = program[ip + 1]
    ip += 2
    combo = operand
    match operand:
        case 4:
            combo = r[0]
        case 5:
            combo = r[1]
        case 6:
            combo = r[2]
    match opcode:
        case 0:
            # print("adv")
            r[0] = r[0] >> combo
        case 1:
            # print("bxl")
            r[1] = r[1] ^ operand
        case 2:
            # print("bst")
            r[1] = combo % 8
        case 3:
            # print("jnz")
            if r[0] != 0:
                ip = operand
        case 4:
            # print("bxc")
            r[1] = r[1] ^ r[2]
        case 5:
            # print("out")
            output.append(combo % 8)
        case 6:
            # print("bdv")
            r[1] = r[0] >> combo
        case 7:
            # print("cdv")
            r[2] = r[0] >> combo
    return ip


def find_next_three_bits_possibilities(existing_bit_groups, program):
    ra = sum([bg[1] << (3 * bg[0]) for bg in enumerate(existing_bit_groups)])

    possibilities = set()
    for i in range(1024):  # 10 bits of context
        r = [ra + (i << (3 * len(existing_bit_groups))), 0, 0]
        ip = 0
        output = []
        while len(output) < len(existing_bit_groups) + 1 and ip < len(program):
            ip = tick(program, ip, r, output)
        if len(output) >= len(existing_bit_groups) + 1 and all(
            [program[i] == output[i] for i in range(len(output))]
        ):
            possibilities.add(i % 8)
    return possibilities


def find_all_bits(existing_bit_groups, program):
    if len(existing_bit_groups) == len(program):
        return [existing_bit_groups]
    next_possible = find_next_three_bits_possibilities(existing_bit_groups, program)
    if len(next_possible) == 0:
        return None
    for np in next_possible:
        ebg = existing_bit_groups + [np]
        ab = find_all_bits(ebg, program)
        if ab is not None:
            return ab
    return None


def main():
    f = open("../input/real/day17_1.txt")
    r = [0, 0, 0]
    program = []
    for line in f.readlines():
        if line.startswith("Register "):
            matched = re.match(r"Register ([ABC]): (\d+)", line)
            if matched is not None:
                match matched.group(1):
                    case "A":
                        r[0] = int(matched.group(2))
                    case "B":
                        r[1] = int(matched.group(2))
                    case "C":
                        r[2] = int(matched.group(2))
        if line.startswith("Program:"):
            program = [int(n) for n in re.findall(r"(\d+)", line)]

    ip = 0
    output = []
    while ip < len(program):
        ip = tick(program, ip, r, output)

    # Part 1
    print(",".join([str(o) for o in output]))

    possibilities = set()
    for a in range(8):
        for b in range(1024):
            r = [(b << 3) + a, 0, 0]
            # print(r)
            ip = 0
            output = []
            while len(output) < 2 and ip < len(program):
                ip = tick(program, ip, r, output)
            if output == [program[0], program[1]]:
                possibilities.add(a)

    for p in possibilities:
        ab = find_all_bits([p], program)
        if ab is not None:
            for seq in ab:
                ra = sum([bg[1] << (3 * bg[0]) for bg in enumerate(seq)])

                # Part 2
                print(ra)


if __name__ == "__main__":
    main()
