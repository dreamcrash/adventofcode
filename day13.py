from utils import get_line_as_string_content, profile_and_print_result


def trans_col(mirror: [str], col):
    return "".join(mirror_row[col] for mirror_row in mirror)


def transpose(mirror: [str]):
    return [trans_col(mirror, col) for col in range(len(mirror[0]))]

def found_mirror(mirror: [str], row_pos: int):
    positions = 0
    while True:
        if row_pos - positions < 0 or row_pos + positions + 1 >= len(mirror):
            return positions > 0
        if mirror[row_pos - positions] != mirror[row_pos + positions + 1]:
            return False
        positions += 1


def get_reflection(mirror: [str]) -> int:
    for pos in range(0, len(mirror)):
        if found_mirror(mirror, pos):
            return pos + 1
    return 0


def get_reflections(mirrors: [[str]]) -> int:
    return sum(get_reflection(m) for m in mirrors)


def day13_part1():
    file_content = get_line_as_string_content("input1_day13").split("\n\n")
    mirrors = [line.split() for line in file_content]
    trans_mirrors = [transpose(m) for m in mirrors]
    return get_reflections(trans_mirrors) + get_reflections(mirrors) * 100


def found_smudge(mirror: [str], row_pos: int):
    total_differences = 0
    positions = 0
    while True:
        if row_pos - positions < 0 or row_pos + positions + 1 >= len(mirror):
            return positions > 0 and total_differences == 1
        row_below = mirror[row_pos - positions]
        row_above = mirror[row_pos + positions + 1]
        total_differences += sum(1 for c1, c2 in zip(row_below, row_above) if c1 != c2)
        if total_differences > 1:
            return False
        positions += 1


def get_smudge_pos(mirror: [str]) -> int:
    for pos in range(0, len(mirror)):
        if found_smudge(mirror, pos):
            return pos + 1
    return 0


def get_smudge_reflections(mirrors: [[str]]):
    return sum(get_smudge_pos(m) for m in mirrors)


def day13_part2():
    file_content = get_line_as_string_content("input1_day13").split("\n\n")
    mirrors = [line.split() for line in file_content]
    trans_mirrors = [transpose(m) for m in mirrors]
    return get_smudge_reflections(trans_mirrors) + get_smudge_reflections(mirrors) * 100


profile_and_print_result(day13_part1)
profile_and_print_result(day13_part2)


# Result => 30487. Time taken 0.004399776458740234 (s)
# Result => 31954. Time taken 0.0077779293060302734 (s)
