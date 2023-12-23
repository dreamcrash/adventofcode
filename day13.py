from utils import get_line_as_string_content, profile_and_print_result


def trans_col(mirror: [str], col):
    return "".join(mirror_row[col] for mirror_row in mirror)


def transpose(mirror: [str]):
    return [trans_col(mirror, col) for col in range(len(mirror[0]))]


def in_limits(mirror: [str], row_pos: int, shift: int) -> bool:
    return row_pos - shift >= 0 and row_pos + shift + 1 < len(mirror)


def total_difference_between_rows(mirror: [str], row_pos: int, shift: int) -> int:
    row_below = mirror[row_pos - shift]
    row_above = mirror[row_pos + shift + 1]
    return sum(1 for c1, c2 in zip(row_below, row_above) if c1 != c2)


def found_mirror(mirror: [str], row_pos: int, allowed_differences: int):
    total_diff = 0
    positions = 0
    while total_diff <= allowed_differences and in_limits(mirror, row_pos, positions):
        total_diff += total_difference_between_rows(mirror, row_pos, positions)
        positions += 1
    return total_diff == allowed_differences and positions > 0


def get_reflection(mirror: [str], allowed_differences: int) -> int:
    for pos in range(0, len(mirror)):
        if found_mirror(mirror, pos, allowed_differences):
            return pos + 1
    return 0


def get_reflections(mirrors: [[str]], allowed_differences: int) -> int:
    return sum(get_reflection(m, allowed_differences) for m in mirrors)


def get_total_reflections(allowed_differences: int) -> int:
    file_content = get_line_as_string_content("input1_day13").split("\n\n")
    mirrors = [line.split() for line in file_content]
    trans_mirrors = [transpose(m) for m in mirrors]
    cols = get_reflections(trans_mirrors, allowed_differences)
    rows = get_reflections(mirrors, allowed_differences)
    return cols + rows * 100


def day13_part1():
    return get_total_reflections(allowed_differences=0)


def day13_part2():
    return get_total_reflections(allowed_differences=1)


profile_and_print_result(day13_part1)
profile_and_print_result(day13_part2)


# Result => 30487. Time taken 0.004399776458740234 (s)
# Result => 31954. Time taken 0.0077779293060302734 (s)
