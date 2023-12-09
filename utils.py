import re
import time


def get_line_content(filename: str) -> list:
    return open(filename, "r").read().split("\n")


def find_all_digits(line: str) -> list:
    return re.findall(r"(\d+)", line)


def profile_and_print_result(func):
    start = time.time()
    result = func()
    end = time.time()

    print(f"Result => {result}. Time taken {end-start} (s)")
