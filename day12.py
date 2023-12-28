from itertools import product
from utils import profile_and_print_result, get_line_content, find_all_digits


def get_permutations(spring: [str]) -> [str]:
    return [["#", "."] if s == "?" else s for s in spring]


def match(spring: [str], expected_counts: [int]) -> bool:
    if spring.count("#") != sum(expected_counts):
        return False

    count = pos = 0

    for char in spring:
        if char == "#":
            count += 1
        elif count > 0:
            if expected_counts[pos] != count:
                return False
            pos += 1
            count = 0

    return count == 0 or expected_counts[pos] == count


def get_count(spring: [str], expected_counts: [int]):
    permutations = get_permutations(spring)
    return sum(1 for guess in product(*permutations) if match(guess, expected_counts))


def day12_part1():
    puzzle = get_line_content("input1_day12")
    puzzle = [v.split() for v in puzzle]
    puzzle = [(v1, find_all_digits(v2)) for v1, v2 in puzzle]

    return sum(get_count(spring, digits) for spring, digits in puzzle)


profile_and_print_result(day12_part1)

# Result => 7173. Time taken 4.925787925720215 (s)
