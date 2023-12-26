from collections import deque

from utils import profile_and_print_result, get_line_content


def read_board() -> [[str]]:
    return list(map(list, get_line_content("input1_day16")))


def move_left(beans, board: [[str]], row: int, col: int) -> [(int, int, int)]:
    for col_pos in range(col, -1, -1):
        current_value = board[row][col_pos]
        beans[row][col_pos] = "#"

        if current_value == "<":
            return []

        if current_value == "-":
            continue

        if current_value == "\\":
            return [("u", row - 1, col_pos)]

        if current_value == "|":
            return [("d", row + 1, col_pos), ("u", row - 1, col_pos)]

        if current_value == "/":
            return [("d", row + 1, col_pos)]

        board[row][col_pos] = "<"
    return []


def move_right(beans, board: [[str]], row: int, col: int) -> [(int, int, int)]:
    for col_pos in range(col, len(board)):
        current_value = board[row][col_pos]
        beans[row][col_pos] = "#"

        if current_value == ">":
            return []

        if current_value == "-":
            continue

        if current_value == "\\":
            return [("d", row + 1, col_pos)]

        if current_value == "|":
            return [("d", row + 1, col_pos), ("u", row - 1, col_pos)]

        if current_value == "/":
            return [("u", row - 1, col_pos)]

        board[row][col_pos] = ">"
    return []


def move_upwards(beans, board: [[str]], row: int, col: int) -> (int, int):
    for row_pos in range(row, -1, -1):
        current_value = board[row_pos][col]
        beans[row_pos][col] = "#"

        if current_value == "^":
            return []

        if current_value == "|":
            continue

        if current_value == "\\":
            return [("l", row_pos, col - 1)]

        if current_value == "-":
            return [("l", row_pos, col - 1), ("r", row_pos, col + 1)]

        if current_value == "/":
            return [("r", row_pos, col + 1)]

        board[row_pos][col] = "^"
    return None


def move_downwards(beans, board: [[str]], row: int, col: int) -> (int, int):
    for row_pos in range(row, len(board)):
        current_value = board[row_pos][col]
        beans[row_pos][col] = "#"

        if current_value == "v":
            return []

        if current_value == "|":
            continue

        if current_value == "\\":
            return [("r", row_pos, col + 1)]

        if current_value == "-":
            return [("l", row_pos, col - 1), ("r", row_pos, col + 1)]

        if current_value == "/":
            return [("l", row_pos, col - 1)]

        board[row_pos][col] = "v"

    return None


def get_bean_count(board, path):
    paths = deque()
    paths.append(path)
    beans = [["." for _ in range(len(board))] for _ in range(len(board))]
    while len(paths):
        path = paths.popleft()
        direction, current_row, current_col = path

        if direction == "r":
            new_path = move_right(beans, board, current_row, current_col)
        elif direction == "l":
            new_path = move_left(beans, board, current_row, current_col)
        elif direction == "u":
            new_path = move_upwards(beans, board, current_row, current_col)
        elif direction == "d":
            new_path = move_downwards(beans, board, current_row, current_col)
        else:
            raise NotImplemented

        if new_path:
            new_path = [
                (d, r, c)
                for d, r, c in new_path
                if 0 <= r < len(board) and 0 <= c < len(board)
            ]
            if new_path:
                paths.extend(new_path)

    count = 0
    for row in range(len(beans)):
        for col in range(len(beans)):
            if beans[row][col] == "#":
                count += 1
    return count


def day16_part1():
    return get_bean_count(read_board(), ("r", 0, 0))


def day16_part2():
    max_bean = -1
    board = read_board()
    for col in range(len(board)):
        max_bean = max(max_bean, get_bean_count(read_board(), ("d", 0, col)))
        max_bean = max(max_bean, get_bean_count(read_board(), ("u", len(board) - 1, col)))

    for row in range(len(board)):
        max_bean = max(max_bean, get_bean_count(read_board(), ("r", row, 0)))
        max_bean = max(max_bean, get_bean_count(read_board(), ("l", row, len(board) - 1)))

    return max_bean


profile_and_print_result(day16_part1)
profile_and_print_result(day16_part2)


# Result => 7046. Time taken 0.007849931716918945 (s)
# Result => 7313. Time taken 2.1181349754333496 (s)