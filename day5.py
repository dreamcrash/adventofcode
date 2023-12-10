from utils import (
    get_line_as_string_content,
    profile_and_print_result,
    get_digits_between_strings,
)

FILE_HEADERS = [
    "seeds: ",
    "seed-to-soil map:",
    "soil-to-fertilizer map:",
    "fertilizer-to-water map:",
    "water-to-light map:",
    "light-to-temperature map:",
    "temperature-to-humidity map:",
    "humidity-to-location map:",
    "",
]


def get_digits_from_file(file_content: str) -> [int]:
    content_parsed = []
    for pos in range(0, len(FILE_HEADERS) - 1):
        start_str = FILE_HEADERS[pos]
        end_str = FILE_HEADERS[pos + 1]
        digits = get_digits_between_strings(file_content, start_str, end_str)
        content_parsed.append(digits)
    return content_parsed


def split_list_in_3(list_to_split: list) -> [[int]]:
    """
    Splits a list into a list of list (where each sub list is of size 3)
    """
    return [list_to_split[i : i + 3] for i in range(0, len(list_to_split), 3)]


def find_mapping_value(seed: int, mapping_lines: [int]) -> int:
    for d_range_start, source_range_start, range_length in mapping_lines:
        if source_range_start <= seed <= source_range_start + range_length:
            return d_range_start - source_range_start + seed
    return seed


def find_location(mapping_pos: int, content_parsed: [int]) -> int:
    for maps in content_parsed:
        mapping_pos = find_mapping_value(mapping_pos, maps)
    return mapping_pos


def sort_mappings_ranges(mappings: [[int]]) -> [[int]]:
    return [split_list_in_3(mappings[p]) for p in range(1, len(mappings))]


def day5_part1():
    file_content = get_line_as_string_content("input1_day5")
    content_parsed = get_digits_from_file(file_content)
    seeds = content_parsed.pop(0)
    mappings = [split_list_in_3(mapping) for mapping in content_parsed]
    return min(find_location(seed, mappings) for seed in seeds)


profile_and_print_result(day5_part1)
