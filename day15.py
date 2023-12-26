from utils import profile_and_print_result, get_line_as_string_content


def hash_algorithm(value: str) -> int:
    current_hash_value = 0
    for c in value:
        current_hash_value = ((current_hash_value + ord(c)) * 17) % 256
    return current_hash_value


def day15_part1() -> int:
    input_v = get_line_as_string_content("input1_day15")
    return sum(hash_algorithm(v) for v in input_v.split(","))


profile_and_print_result(day15_part1)

# Result => 506869. Time taken 0.0069539546966552734 (s)
