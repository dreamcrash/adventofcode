import math
from functools import reduce
from math import sqrt

from utils import profile_and_print_result, find_all_digits


def get_total_way(time: int, distance: int):
    for t0 in range(0, time):
        if (time - t0) * t0 > distance:
            return time - 2 * t0 + 1


def get_total_ways(file_input: [str]):
    times = find_all_digits(file_input[0])
    distances = find_all_digits(file_input[1])
    ways = [get_total_way(t, d) for t, d in zip(times, distances)]
    return reduce(lambda x, y: x * y, ways, 1)


def day6_part1():
    file_input = open("input1_day6").read().split("\n")
    return get_total_ways(file_input)


def day6_part2():
    file_input = open("input1_day6").read().split("\n")
    file_input = [fi.replace(" ", "") for fi in file_input]
    return get_total_ways(file_input)


def day6_part2_faster():
    file_input = open("input1_day6").read().split("\n")
    file_input = [fi.replace(" ", "") for fi in file_input]
    time = find_all_digits(file_input[0])[0]
    distance = find_all_digits(file_input[1])[0]

    # (time - t0) * t0 > distance
    # -t0^2 + time * t0 - distance > 0
    # Using quadratic formula

    l1 = (-time + sqrt(pow(time, 2) - 4 * (-1) * (-distance))) / (2 * (-1))
    l2 = (-time - sqrt(pow(time, 2) - 4 * (-1) * (-distance))) / (2 * (-1))
    return round(l2 - 0.5) - round(l1 + 0.5) + 1


profile_and_print_result(day6_part1)
profile_and_print_result(day6_part2)
profile_and_print_result(day6_part2_faster)


#
# Result => 2612736. Time taken 0.00029015541076660156 (s)
# Result => 29891250. Time taken 1.0031499862670898 (s)
# Result => 29891250. Time taken 0.00023412704467773438 (s)
