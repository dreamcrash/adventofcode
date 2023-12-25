from utils import profile_and_print_result, get_line_content
from collections import deque


def swap_if_possible_and_get_row(spaces: deque, row: int) -> int:
    if len(spaces) > 0:
        free_row = spaces.popleft()
        spaces.append(row)
        return free_row
    return row


def check_pos_and_get_count(spaces: deque, board: [[]], row: int, col: int) -> int:
    if board[row][col] == ".":
        spaces.append(row)
    elif board[row][col] == "O":
        return len(board) - swap_if_possible_and_get_row(spaces, row)
    elif board[row][col] == "#":
        spaces.clear()
    return 0


def get_col_count(board: [[]], col: int) -> int:
    spaces = deque()
    rows = len(board)
    return sum(check_pos_and_get_count(spaces, board, row, col) for row in range(rows))


def day14_part1():
    file_content = get_line_content("input1_day14")
    board = [list(row) for row in file_content]
    return sum(get_col_count(board, col) for col in range(len(board[0])))


profile_and_print_result(day14_part1)


# Result => 113525. Time taken 0.004829883575439453 (s)
