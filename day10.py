import math
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


def solve(puzzle_input: [[str]]) -> [(int, int)]:
    path = []
    row, col, direction = next_valid_pos_from_s(puzzle_input)

    while puzzle_input[row][col] != "S":
        pos = puzzle_input[row][col]
        path.append((row, col))
        row, col, direction = POS_MOVE_MAP[pos][direction](row, col)

    path.append((row, col))
    return path


def count_symbols(path, puzzle, row, org_col: int) -> (int, int):
    count = 0
    for col in range(org_col, len(puzzle[row])):
        if puzzle[row][col] != ".":
            count += 1
    return count


def day10_part1():
    return int(len(solve(get_line_content("input1_day10"))) / 2)


def apply_shoelace_formula(path: [(int, int)]) -> int:
    diagonal = zip(path, path[1:] + [path[0]])
    return abs(sum((x1 * y2) - (x2 * y1) for (x1, y1), (x2, y2) in diagonal))


def get_area(path: [(int, int)]) -> int:
    return int(apply_shoelace_formula(path) / 2)


def apply_picks_theorem(points: [(int, int)]) -> int:
    # https://en.wikipedia.org/wiki/Pick%27s_theorem
    # Let 'i' be the number of integer points interior to the polygon, and let
    # 'b' be the number of integer points on its boundary (including both vertices and points along the sides).
    # Then the area 'A' of this polygon is:
    # A = i + b/2 - 1

    # We can calculate 'A' using https://en.wikipedia.org/wiki/Shoelace_formula
    # then i = A - b/2 + 1
    return int(get_area(points) - len(points)/2 + 1)


def day10_part2():
    path = solve(get_line_content("input1_day10"))
    return apply_picks_theorem(path)


profile_and_print_result(day10_part1)
profile_and_print_result(day10_part2)

# Result => 6738. Time taken 0.01200103759765625 (s)
# Result => 579. Time taken 0.015379905700683594 (s)
