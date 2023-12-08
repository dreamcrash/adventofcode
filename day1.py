from typing import Optional

from utils import profile_and_print_result

NUMBERS = {
    "o": {"n": {"e": 1}},  # 1
    "t": {"w": {"o": 2}, "h": {"r": {"e": {"e": 3}}}},  # two and three
    "f": {"o": {"u": {"r": 4}}, "i": {"v": {"e": 5}}},  # four and five
    "s": {"i": {"x": 6}, "e": {"v": {"e": {"n": 7}}}},  # six and seven
    "e": {"i": {"g": {"h": {"t": 8}}}},  # 8 eight
    "n": {"i": {"n": {"e": 9}}},  # nine
}


def extract_calibration_value(string: str) -> int:
    string = string.rstrip()
    numbers = [int(s) for s in string if s.isdigit()]
    return numbers[0] * 10 + numbers[-1] if len(numbers) else 0


def day1_part1():
    sum_calibrations = 0
    with open("input1_day1") as file:
        for line in file:
            sum_calibrations = sum_calibrations + extract_calibration_value(line)
    return sum_calibrations


def convert_number(global_line_pos: int, line: [str]) -> Optional[int]:
    """
    It goes throw the line, starting from a given position,
    char-by-char and checks if the current substring contains
    a number spelled. If yes, then it returns the corresponded number
    otherwise it returns None.
    """
    sequence = NUMBERS

    for relative_line_pos in range(global_line_pos, len(line)):
        current_char = line[relative_line_pos]

        # Update to next element in the sequence
        sequence = sequence.get(current_char)

        # A complete match was found
        if isinstance(sequence, int):
            return sequence
        elif not sequence:
            break
    return None


def parser_line(global_line_pos: int, line: [str]) -> str:
    element = convert_number(global_line_pos, line)
    return str(element) if element else line[global_line_pos]


def day1_part2():
    """
    Decided to do the second part 'more manually' without relying on the 're' module
    to be a bit more challenging
    """
    sum_calibrations = 0
    with open("input1_day1") as file:
        for file_line in file:
            line = file_line.rstrip()
            new_line = [parser_line(pos, line) for pos in range(0, len(line))]

            value = extract_calibration_value("".join(new_line))
            sum_calibrations += value
    return sum_calibrations


profile_and_print_result(day1_part1)
profile_and_print_result(day1_part2)

# Ex
# Result => 54630. Time taken 0.004485130310058594 (s)
# Result => 54770. Time taken 0.03564620018005371 (s)
