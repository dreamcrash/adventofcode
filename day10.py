from utils import get_line_content, profile_and_print_result


def get_s_pos(puzzle_input: [[str]]) -> (int, int):
    for row in range(len(puzzle_input)):
        for col in range(len(puzzle_input)):
            if puzzle_input[row][col] == "S":
                return row, col


def next_valid_pos_from_s(puzzle_input: [[str]]) -> (int, int, str):
    row, col = get_s_pos(puzzle_input)
    if col < len(puzzle_input) and puzzle_input[row][col + 1] == "-":
        return right(row, col)
    elif col < len(puzzle_input) and puzzle_input[row + 1][col] == "|":
        return down(row, col)
    else:
        raise NotImplemented


def down(r, c) -> (int, int, str):
    return r + 1, c, "d"


def up(r, c) -> (int, int, str):
    return r - 1, c, "u"


def right(r, c) -> (int, int, str):
    return r, c + 1, "r"


def left(r, c) -> (int, int, str):
    return r, c - 1, "l"


POS_MOVE_MAP = {
    "|": {"d": down, "u": up, "r": right, "l": left},
    "-": {"d": down, "u": up, "r": right, "l": left},
    "L": {"l": up, "d": right},
    "7": {"r": down, "u": left},
    "J": {"r": up, "d": left},
    "F": {"u": right, "l": down},
}


def solve(puzzle_input: [[str]]):
    longest_path = 0
    row, col, direction = next_valid_pos_from_s(puzzle_input)

    while puzzle_input[row][col] != "S":
        pos = puzzle_input[row][col]
        row, col, direction = POS_MOVE_MAP[pos][direction](row, col)
        longest_path += 1

    return int(longest_path / 2)


def count_symbols(puzzle_input: [[str]]) -> (int, int):
    count = 0
    for row in range(len(puzzle_input)):
        for col in range(len(puzzle_input)):
            if puzzle_input[row][col] != ".":
                count += 1
    return count


def day10_part1():
    return solve(get_line_content("input1_day10"))

profile_and_print_result(day10_part1)
