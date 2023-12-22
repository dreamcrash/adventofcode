from utils import profile_and_print_result


def get_input() -> [[int]]:
    return [[*map(int, line.split())] for line in open("input1_day9")]


def get_history_value(values: [int]) -> int:
    result = 0
    while not all(v == 0 for v in values):
        result += values[-1]
        values = [values[p+1] - values[p] for p in range(len(values) - 1)]
    return result


def day9_part1():
    return sum(get_history_value(line) for line in get_input())


def day9_part2():
    return sum(get_history_value(line[::-1]) for line in get_input())


profile_and_print_result(day9_part1)
profile_and_print_result(day9_part2)


#
# Result => 2175229206. Time taken 0.015954971313476562 (s)
# Result => 942. Time taken 0.015679359436035156 (s)
