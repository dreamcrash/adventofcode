from utils import get_line_content, profile_and_print_result

# Using Shoelace formula
# https://en.wikipedia.org/wiki/Shoelace_formula
# Video explanation https://www.youtube.com/watch?v=FSWPX0XB7a0


def extract_points(dig_plan: [(str, str, str)]) -> [(int, int)]:
    current_row = 0
    current_col = 0
    points = [(current_row, current_col)]
    for direction, length, _ in dig_plan:
        if direction == "R":
            current_col += int(length)
        elif direction == "L":
            current_col -= int(length)
        elif direction == "D":
            current_row += int(length)
        else:
            current_row -= int(length)
        points.append((current_row, current_col))
    return points


def get_area(points: [(int, int)]) -> int:
    area = 0
    for point_pos in range(len(points) - 1):
        x1, y1 = points[point_pos]
        x2, y2 = points[point_pos + 1]
        area += (x1 * y2) - (x2 * y1)
    return abs(area)


def day18_part1():
    dig_plan = [r.split() for r in get_line_content("input1_day18")]
    perimeter = sum(int(l) for _, l, _ in dig_plan)
    points = extract_points(dig_plan)
    return int(0.5 * (get_area(points) + perimeter) + 1)


profile_and_print_result(day18_part1)

# 58550 47452118468566
