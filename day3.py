import re
from curses.ascii import isalnum

from utils import profile_and_print_result, find_all_digits


def create_matrix_with_padding(file_name: str):
    with open(file_name) as file:
        matrix = [line.split("\n")[0] for line in file]
        matrix.insert(0, "\n")
        matrix.append("\n")
        return matrix


def is_special_symbol(value: str):
    return value != "." and not isalnum(value)


def get_special_symbols_pos(line: str):
    return [p for p in range(0, len(line)) if is_special_symbol(line[p])]


def is_in_interval(start_pos: int, end_pos: int, positions: list) -> bool:
    return any(start_pos - 1 <= ss_pos <= end_pos + 1 for ss_pos in positions)


def is_valid_number(ss_positions: [list], digit: str, digit_start_pos: int) -> bool:
    digit_end_pos = digit_start_pos + len(digit) - 1
    return any(is_in_interval(digit_start_pos, digit_end_pos, p) for p in ss_positions)


def get_pos_within_interval(start_pos: int, end_pos: int, positions: list) -> list:
    return [p for p in positions if start_pos - 1 <= p <= end_pos + 1]


def day3_part1():
    digit_sum = 0
    matrix = create_matrix_with_padding("input1_day3")
    ss_positions = [get_special_symbols_pos(r) for r in matrix]
    for row_pos in range(1, len(matrix) - 1):
        current_line = matrix[row_pos]

        digits_in_line = find_all_digits(current_line)
        pos_of_digits_in_line = [m.start() for m in re.finditer(r"(\d+)", current_line)]

        ss_relevant_pos = [
            ss_positions[row_pos + 1],
            ss_positions[row_pos],
            ss_positions[row_pos - 1],
        ]
        for digit, digit_pos in zip(digits_in_line, pos_of_digits_in_line):
            if is_valid_number(ss_relevant_pos, digit, digit_pos):
                digit_sum += int(digit)

    return digit_sum


def add_gear_coord(current_digit, digit_start_pos, gear_coord, line_yy_pos, gear_pos):
    """
    Adds the gear coordinates connected to the given number
    """
    digit_end_pos = digit_start_pos + len(current_digit) - 1
    line_gear_pos = gear_pos[line_yy_pos]
    ss_pos = get_pos_within_interval(digit_start_pos, digit_end_pos, line_gear_pos)
    for p in ss_pos:
        coord = (p, line_yy_pos)
        digit = int(current_digit)
        v = gear_coord.get(coord)
        v.append(digit) if v else gear_coord.update({coord: [digit]})


def day3_part2():
    matrix = create_matrix_with_padding("input1_day3")
    gear_positions = [[p for p in range(0, len(r)) if r[p] == "*"] for r in matrix]
    gears = dict()
    for row_pos in range(1, len(matrix) - 1):
        current_line = matrix[row_pos]
        digits_in_line = find_all_digits(current_line)
        pos_of_digits_in_line = [m.start() for m in re.finditer(r"(\d+)", current_line)]

        for digit, digit_start_pos in zip(digits_in_line, pos_of_digits_in_line):
            add_gear_coord(digit, digit_start_pos, gears, row_pos + 1, gear_positions)
            add_gear_coord(digit, digit_start_pos, gears, row_pos, gear_positions)
            add_gear_coord(digit, digit_start_pos, gears, row_pos - 1, gear_positions)

    return sum(v[0] * v[1] for v in gears.values() if len(v) == 2)


profile_and_print_result(day3_part1)
profile_and_print_result(day3_part2)

# Ex:
# Result => 532428. Time taken 0.02220010757446289 (s)
# Result => 84051670. Time taken 0.00934600830078125 (s)
