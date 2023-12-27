from utils import get_line_content, profile_and_print_result

# Using Shoelace formula
# https://en.wikipedia.org/wiki/Shoelace_formula
# Video explanation https://www.youtube.com/watch?v=FSWPX0XB7a0


def extract_points(dig_plan: [(str, str, str)]) -> [(int, int)]:
    direction_map = {"R": (0, 1), "D": (1, 0), "L": (0, -1), "U": (-1, 0)}
    direction_map.update({"0": (0, 1), "1": (1, 0), "2": (0, -1), "3": (-1, 0)})
    current_row = current_col = 0
    points = [(current_row, current_col)]
    for direction, length, _ in dig_plan:
        x, y = direction_map[direction]
        current_row += x * int(length)
        current_col += y * int(length)
        points.append((current_row, current_col))
    return points


def get_area(points: [(int, int)]) -> int:
    diagonal = zip(points[:-1], points[1:])
    return abs(sum((x1 * y2) - (x2 * y1) for (x1, y1), (x2, y2) in diagonal))


def apply_shoelace_formula(dig_plan: [(str, str, str)]) -> int:
    perimeter = sum(int(l) for _, l, _ in dig_plan)
    points = extract_points(dig_plan)
    return int(0.5 * (get_area(points) + perimeter) + 1)


def day18_part1():
    dig_plan = [r.split() for r in get_line_content("input1_day18")]
    return apply_shoelace_formula(dig_plan)


def correct_dig_plan(dig_plan: [(str, str, str)]) -> [(str, str, str)]:
    return [[c[-2], int(c[2:7], base=16), c] for _, _, c in dig_plan]


def day18_part2():
    dig_plan = [r.split() for r in get_line_content("input1_day18")]
    return apply_shoelace_formula(correct_dig_plan(dig_plan))


profile_and_print_result(day18_part1)
profile_and_print_result(day18_part2)


# Result => 58550. Time taken 0.0013971328735351562 (s)
# Result => 47452118468566. Time taken 0.0016598701477050781 (s)
