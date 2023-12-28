import re
from itertools import product
from utils import profile_and_print_result, get_line_content, find_all_digits


def get_permutations(list_size: int) -> [str]:
    return list(product(["#", "."], repeat=list_size))


def match(spring: [str], expected_counts: [int]) -> bool:
    return expected_counts == [len(x) for x in re.findall(r'#+', spring)]


def replace_unknown(spring: [str], permutation: [str]) -> [str]:
    r = []
    replaced = 0
    for pos in range(len(spring)):
        if spring[pos] == "?":
            r.append(permutation[replaced])
            replaced += 1
        else:
            r.append(spring[pos])
    return "".join(r)


def day12_part1():
    puzzle = get_line_content("input1_day12")
    puzzle = [v.split() for v in puzzle]
    puzzle = [(v1, find_all_digits(v2)) for v1, v2 in puzzle]

    possible_configurations = 0
    for spring, digits in puzzle:
        count_unknown = spring.count("?")

        permutations = get_permutations(count_unknown)
        guesses = [replace_unknown(spring, p) for p in permutations]
        tmp = len([g for g in guesses if match(g, digits)])
        possible_configurations += tmp

    return possible_configurations


profile_and_print_result(day12_part1)

# Result => 7173. Time taken 42.718852043151855 (s)
