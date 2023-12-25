from utils import profile_and_print_result, get_line_content
from collections import deque


def swap_if_possible_and_get_col(spaces: deque, col: int) -> int:
    if len(spaces) > 0:
        free_col = spaces.popleft()
        spaces.append(col)
        return free_col
    return col


def check_pos_and_get_count(spaces: deque, row: [int], col: int) -> int:
    if row[col] == ".":
        spaces.append(col)
    elif row[col] == "O":
        return len(row) - swap_if_possible_and_get_col(spaces, col)
    elif row[col] == "#":
        spaces.clear()
    return 0


def get_row_count(row: [int]) -> int:
    spaces = deque()
    return sum(check_pos_and_get_count(spaces, row, col) for col in range(len(row)))


def day14_part1():
    file_content = get_line_content("input1_day14")
    # Transposing the board
    board = list(map(list, map(list, zip(*file_content))))
    return sum(get_row_count(row) for row in board)


profile_and_print_result(day14_part1)


# Result => 113525. Time taken 0.004829883575439453 (s)
