import math
from math import sqrt

from utils import profile_and_print_result, find_all_digits


def get_total_ways(file_name: str):
    file_input = open(file_name).read().split("\n")
    times = find_all_digits(file_input[0])
    distances = find_all_digits(file_input[1])

    total = 1
    for time, distance in zip(times, distances):
        total *= sum(1 for t0 in range(0, time) if (time - t0) * t0 > distance)

    return total


def day6_part1():
    return get_total_ways("input1_day6")


def day6_part2():
    return get_total_ways("input2_day6")


def day6_part2_faster():
    file_input = open("input2_day6").read().split("\n")
    time = find_all_digits(file_input[0])[0]
    distance = find_all_digits(file_input[1])[0]

    # (time - t0) * t0 > distance
    # -t0^2 + time * t0 - distance > 0
    # Using quadratic formula

    l1 = (-time + sqrt(pow(time, 2) - 4 * (-1) * (-distance))) / (2 * (-1))
    l2 = (-time - sqrt(pow(time, 2) - 4 * (-1) * (-distance))) / (2 * (-1))
    return math.floor(l2 + 0.5) - round(l1 + 0.5) + 1


profile_and_print_result(day6_part1)
profile_and_print_result(day6_part2)
profile_and_print_result(day6_part2_faster)


#
#Result => 2612736. Time taken 0.0004260540008544922 (s)
#Result => 29891250. Time taken 7.526825189590454 (s)
#Result => 29891250. Time taken 0.00022912025451660156 (s
