def make_disk(file_map):
    length = sum(file_map)
    disk = [-1 for _ in range(length)]
    ptr = 0
    for i in range(len(file_map)):
        for _ in range(file_map[i]):
            if i % 2 == 0:
                disk[ptr] = int(i / 2)
            else:
                disk[ptr] = -1
            ptr += 1
    return disk


# Mutates disk and space_map
def move_file_to_first_space(disk, file_num, file_size, space_map):
    # First remove the file from the disk
    loc = next(i for i, n in enumerate(disk) if n == file_num)
    for i in range(file_size):
        disk[loc + i] = -1
    space_map.append([file_size, loc])
    space_map = sorted(space_map, key=lambda s: s[1])
    # Then move the file to the first space that is big enough
    for i in range(len(space_map)):
        if space_map[i][0] >= file_size:
            space_map[i][0] -= file_size
            # Move file to new location
            new_loc = space_map[i][1]
            for j in range(file_size):
                disk[new_loc + j] = file_num
            space_map[i][1] += file_size

            return


def main():
    input = open("../input/real/day9_1.txt")
    file_map = [int(char) for char in input.read().strip()]
    length = sum(file_map)
    disk = make_disk(file_map)

    ptr_fwd = 0
    ptr_back = length - 1

    # Assumes that the disk is neither full nor empty
    while disk[ptr_fwd] != -1:
        ptr_fwd += 1
    while disk[ptr_back] == -1:
        ptr_back -= 1

    while ptr_fwd < ptr_back:
        disk[ptr_fwd] = disk[ptr_back]
        disk[ptr_back] = -1

        # Now wind fwd ptr_fwd until it reaches a -1
        while disk[ptr_fwd] != -1 and ptr_fwd < ptr_back:
            ptr_fwd += 1

        # wind back ptr_back until it reaches a non-zero
        while disk[ptr_back] == -1 and ptr_back > ptr_fwd:
            ptr_back -= 1

    # Part 1
    checksum = [i * disk[i] if disk[i] != -1 else 0 for i in range(length)]
    print(sum(checksum))

    disk = make_disk(file_map)

    locations = [sum(file_map[:i]) for i in range(len(file_map))]
    file_sizes = [file_map[i * 2] for i in range((len(file_map) + 1) // 2)]
    space_map = [
        [file_map[i * 2 + 1], locations[i * 2 + 1]] for i in range(len(file_map) // 2)
    ]
    print(disk)
    print(space_map)
    for i in range(len(file_sizes) - 1, 0, -1):
        move_file_to_first_space(disk, i, file_sizes[i], space_map)

        # Combine consecutive spaces in space_map
        space_map = [s for s in space_map if s[0] > 0]
        for j in range(len(space_map) - 1):
            if space_map[j][0] + space_map[j][1] == space_map[j + 1][0]:
                space_map[j][1] += space_map[j + 1][1]
                space_map[j + 1][0] = 0
        space_map = sorted(space_map, key=lambda s: s[1])

    # Part 2
    checksum = [i * disk[i] if disk[i] != -1 else 0 for i in range(length)]
    print(sum(checksum))


if __name__ == "__main__":
    main()
