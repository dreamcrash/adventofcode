from utils import (
    profile_and_print_result,
    find_all_digits,
)


def split_list_in_n(list_to_split: list, n) -> [[int]]:
    """
    Splits a list into a list of list (where each sub list is of size 3)
    """
    return [list_to_split[i : i + n] for i in range(0, len(list_to_split), n)]


def find_mapping_value(seed: int, mapping_lines: [[int]]) -> int:
    for d_range_start, source_range_start, range_length in mapping_lines:
        if source_range_start <= seed <= source_range_start + range_length:
            return d_range_start - source_range_start + seed
    return seed


def find_location(mapping_pos: int, mapping: [[int]]) -> int:
    for maps in mapping:
        mapping_pos = find_mapping_value(mapping_pos, maps)
    return mapping_pos


def extract_seeds_and_mappings_from_input():
    seeds, *mappings = open("input1_day5").read().split("\n\n")
    seeds = find_all_digits(seeds)
    return seeds, [split_list_in_n(find_all_digits(mapping), 3) for mapping in mappings]


def day5_part1():
    seeds, mappings = extract_seeds_and_mappings_from_input()
    return min(find_location(seed, mappings) for seed in seeds)


def get_overlapping_range(maps_level: [int], range_start:int, range_end:int):
    for dst_start, org_start, length in maps_level:
        if org_start < range_end and range_start < org_start + length:
            return dst_start, org_start, length
    return None


def next_maps_ranges(current_ranges: [(int, int)], maps_level: [int]) -> [(int, int)]:
    next_ranges = []

    while current_ranges:
        range_start, range_end = current_ranges.pop(0)

        overlapping_range = get_overlapping_range(maps_level, range_start, range_end)

        if overlapping_range:
            dst_start, org_start, length = overlapping_range
            org_end = org_start + length

            # Overlaps
            # To get the code below I started by enumerating all the conditions
            # and the worked backwards to generalize the conditions and reduce
            # the code size

            # [..........] (range_start, range_end)
            #    [....]    (source_start, source_end)
            # overlapping => (source_start, source_end)
            # and
            # [....]       (range_start, range_end)
            #    [....]    (source_start, source_end)
            # overlapping => (source_start, range_end)
            # Generic overlapping => (source_start, min(source_end, range_end))

            #    [....]    (range_start, range_end)
            # [..........] (source_start, source_end)
            # overlapping => (range_start, range_end)
            # and
            #      [....]  (range_start, range_end)
            # [.......]    (source_start, source_end)
            # overlapping => (range_start, source_end)
            # Generic overlapping => (range_start, min(source_end, range_end))

            # Generic overlapping => (max(range_start, source_start), min(source_end, range_end))

            next_range_start = max(org_start, range_start) - org_start + dst_start
            next_range_end = min(range_end, org_end) - org_start + dst_start

            if range_start < org_start:
                current_ranges.append((range_start, org_start))

            if range_end > org_end:
                current_ranges.append((org_end, range_end))

            next_ranges.append((next_range_start, next_range_end))
        else:
            # 1:1 mapping
            next_ranges.append((range_start, range_end))

    return next_ranges


def find_range_locations(maps: [[int]], current_ranges: [(int, int)]) -> [(int, int)]:
    for mappings_level in maps:
        current_ranges = next_maps_ranges(current_ranges, mappings_level)

    return current_ranges


def day5_part2():
    seeds, mappings = extract_seeds_and_mappings_from_input()
    seed_ranges = [(start, start + size) for start, size in split_list_in_n(seeds, 2)]
    return min(location[0] for location in find_range_locations(mappings, seed_ranges))


profile_and_print_result(day5_part1)
profile_and_print_result(day5_part2)

# Ex
#Result => 388071289. Time taken 0.0011110305786132812 (s)
#Result => 84206669. Time taken 0.002232074737548828 (s)
