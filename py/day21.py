from functools import lru_cache

keypad = {
    "7": (0, 0),
    "8": (0, 1),
    "9": (0, 2),
    "4": (1, 0),
    "5": (1, 1),
    "6": (1, 2),
    "1": (2, 0),
    "2": (2, 1),
    "3": (2, 2),
    "0": (3, 1),
    "A": (3, 2),
}

dirpad = {
    "^": (0, 1),
    "A": (0, 2),
    "<": (1, 0),
    "v": (1, 1),
    ">": (1, 2),
}

dirpad_dirs = {
    "^": (-1, 0),
    "<": (0, -1),
    "v": (1, 0),
    ">": (0, 1),
}

move_keys = {
    (-1, 0): "^",
    (0, -1): "<",
    (1, 0): "v",
    (0, 1): ">",
}


# Precalculate the shortest valid moves between all pairs of keys on the keypad
# at one layer up
def build_pad_moves(pad, avoid_spot):
    moves = {}
    for i in pad.keys():
        for j in pad.keys():
            if i == j:
                continue
            iposx, iposy = pad[i]
            jposx, jposy = pad[j]
            dx = jposx - iposx
            dy = jposy - iposy
            xmoves = []
            for _ in range(abs(dx)):
                key = move_keys[(int(dx / abs(dx)), 0)]
                xmoves.append(key)
            ymoves = []
            for _ in range(abs(dy)):
                key = move_keys[(0, int(dy / abs(dy)))]
                ymoves.append(key)
            moves[(i, j)] = []
            if abs(dx) > 0:
                mid_point = (iposx + dx, iposy)
                if mid_point != avoid_spot:
                    moves[(i, j)].append("".join(xmoves) + "".join(ymoves))
            if abs(dy) > 0:
                mid_point = (iposx, iposy + dy)
                if mid_point != avoid_spot:
                    moves[(i, j)].append("".join(ymoves) + "".join(xmoves))
    return moves


def best_move_next_level(pad_moves, movestr, frm="A"):
    result = ["."] * (len(movestr) * 6)
    result_len = 0
    last = frm
    for c in movestr:
        if last == c:
            result[result_len] = "A"
            result_len += 1
            continue
        options = pad_moves[(last, c)]
        best = options[0]
        for o in options:
            if cmp_options(o, best):
                best = o
        for bc in best:
            result[result_len] = bc
            result_len += 1
        result[result_len] = "A"
        result_len += 1
        last = c
    return "".join(result[:result_len])


@lru_cache(maxsize=None)
def best_dirmove_next_level(movestr):
    result = ["."] * (len(movestr) * 5)
    result_len = 0
    last = "A"
    for c in movestr:
        if last == c:
            result[result_len] = "A"
            result_len += 1
            continue
        options = dirpad_moves[(last, c)]
        best = options[0]
        for o in options:
            if cmp_options(o, best):
                best = o
        for bc in best:
            result[result_len] = bc
            result_len += 1
        result[result_len] = "A"
        result_len += 1
        last = c
    return "".join(result[:result_len])


def cmp_options(a, b):
    if len(a) != len(b):
        return len(b) > len(a)
    for ca, cb in zip(a, b):
        if ca == cb:
            continue
        match ca, cb:
            case "<", _:
                return True
            case _, "<":
                return False
            case "v", _:
                return True
            case _, "v":
                return False
            case "^", _:
                return True
            case _, "^":
                return False
            case ">", _:
                return True
            case _, ">":
                return False
    return False


@lru_cache(maxsize=None)
def best_dirmove_len(movestr, depth):
    result_len = 0
    last = "A"
    for c in movestr:
        if last == c:
            result_len += 1  # Hit "A"
            continue
        options = dirpad_moves[(last, c)]
        best = options[0]
        for o in options:
            if cmp_options(o, best):
                best = o
        if depth == 1:
            result_len += len(best) + 1
        else:
            result_len += best_dirmove_len(best + "A", depth - 1)
        last = c
    return result_len


def solve(codes, num_robots):
    sum = 0
    for code in codes:
        top_layer_len = 0
        last = "A"
        for c in code:
            layer = best_move_next_level(keypad_moves, c, frm=last)
            top_layer_len += best_dirmove_len(layer, num_robots)
            last = c
        complexity = top_layer_len * int("".join(code[0:-1]))
        sum += complexity
    return sum


def main():
    f = open("../input/real/day21_1.txt")
    codes = [list(line.strip()) for line in f.readlines()]

    # Index of possible moves at next level up to go from key A to key B
    # (A, B) -> ["setofmoves", "setofmoves", ...]
    global keypad_moves
    keypad_moves = build_pad_moves(keypad, avoid_spot=(3, 0))
    global dirpad_moves
    dirpad_moves = build_pad_moves(dirpad, avoid_spot=(0, 0))

    # Tests
    # _ = moves_next_level(keypad_moves, "20")
    # _ = moves_next_level(dirpad_moves, "v^A")

    print(f"Part 1: {solve(codes, 2)}")
    print(f"Part 2: {solve(codes, 25)}")


if __name__ == "__main__":
    main()
