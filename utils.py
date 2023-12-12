import re
import time


def get_digits_between_strings(line: str, start_str: str, end_str: str) -> [int]:
    pattern = re.compile(rf"{start_str}\s*([\d\s]+){end_str}")
    match = pattern.search(line)

    return [int(d) for d in match.group(1).strip().split()] if match else []


def get_line_content(filename: str) -> list:
    return get_line_as_string_content(filename).split("\n")


def get_line_as_string_content(filename: str) -> str:
    return open(filename, "r").read()


def find_all_digits(line: str) -> [int]:
    return [int(d) for d in re.findall(r"(\d+)", line)]


def profile_and_print_result(func):
    start = time.time()
    result = func()
    end = time.time()

    print(f"Result => {result}. Time taken {end-start} (s)")
