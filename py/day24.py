import re


def gen_value(rules, values, n):
    op, n1, n2 = rules[n]
    if values[n1] is None:
        gen_value(rules, values, n1)
    if values[n2] is None:
        gen_value(rules, values, n2)
    match op:
        case "AND":
            values[n] = values[n1] & values[n2]
        case "OR":
            values[n] = values[n1] | values[n2]
        case "XOR":
            values[n] = values[n1] ^ values[n2]


def check_xor_into_z(rules, i, bad_nodes):
    zi = f"z{i:02d}"
    op, n1, n2 = rules[zi]
    if op != "XOR":
        bad_nodes.append(zi)
        return
    op1, _, _ = rules[n1]
    op2, _, _ = rules[n2]
    # one of op1, op2 should be an XOR and one should be an OR
    match op1, op2:
        case "XOR", "OR":
            check_xor_from_xy(rules, n1, i, bad_nodes)
            check_carry_or(rules, n2, bad_nodes)
        case "OR", "XOR":
            check_carry_or(rules, n1, bad_nodes)
            check_xor_from_xy(rules, n2, i, bad_nodes)
        case "OR", a if a != "XOR":
            bad_nodes.append(n2)
        case a, "OR" if a != "XOR":
            bad_nodes.append(n1)
        case "XOR", a if a != "OR":
            bad_nodes.append(n2)
        case a, "OR" if a != "OR":
            bad_nodes.append(n1)


def check_xor_from_xy(rules, node, i, bad_nodes):
    xi = f"x{i:02d}"
    yi = f"y{i:02d}"
    op, n1, n2 = rules[node]
    if op != "XOR":
        bad_nodes.append(node)
    match n1, n2:
        case a, b if a == xi and b == yi:
            pass
        case a, b if a == yi and b == xi:
            pass
        case a, n if a == yi:
            bad_nodes.append(n)
        case n, b if b == xi:
            bad_nodes.append(n)
        case a, n if a == xi:
            bad_nodes.append(n)
        case n, b if b == xi:
            bad_nodes.append(n)


def check_carry_or(rules, node, bad_nodes):
    op, n1, n2 = rules[node]
    if op != "OR":
        bad_nodes.append(node)
    # Children should both be AND nodes
    op1, _, _ = rules[n1]
    op2, _, _ = rules[n2]
    if op1 != "AND":
        bad_nodes.append(n1)
    if op2 != "AND":
        bad_nodes.append(n2)


def main():
    f = open("../input/real/day24_1.txt")
    rules = {}
    values = {}
    for line in f.readlines():
        m = re.match(r"(\w+): (0|1)", line)
        if m is not None:
            values[m.group(1)] = int(m.group(2))
            continue
        m = re.match(r"(\w+) (AND|OR|XOR) (\w+) -> (\w+)", line)
        if m is not None:
            rules[m.group(4)] = (m.group(2), m.group(1), m.group(3))
            for n in [m.group(1), m.group(3), m.group(4)]:
                if n not in values:
                    values[n] = None

    for n in values.keys():
        if values[n] is None:
            gen_value(rules, values, n)

    zs = [k for k in values.keys() if k.startswith("z")]
    zs.sort()
    zs.reverse()

    output = 0
    for z in zs:
        output = output * 2 + values[z]

    print(f"Part 1: {output}")

    bad_nodes = []
    for i in range(2, 45):  # Manually verified the start/end nodes
        check_xor_into_z(rules, i, bad_nodes)

    bad_nodes.sort()
    print(",".join(bad_nodes))


if __name__ == "__main__":
    main()
