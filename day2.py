import re

from utils import profile_and_print_result, get_line_content


def get_max_color_occurrences(color: str, game: str) -> int:
    occurrences = re.findall(rf"(\d+) {color}", game)
    return max(list(map(int, occurrences)))


def check_if_game_possible(color: str, game: str, max_value: int) -> bool:
    return get_max_color_occurrences(color, game) <= max_value


def day2_part1():
    sum_of_the_ids_of_possible_games = 0
    for file_line in get_line_content("input1_day2"):
        game_id = re.search(r"Game (\d+):", file_line).group(1)

        if (
            check_if_game_possible("red", file_line, 12)
            and check_if_game_possible("green", file_line, 13)
            and check_if_game_possible("blue", file_line, 14)
        ):
            sum_of_the_ids_of_possible_games += int(game_id)

    return sum_of_the_ids_of_possible_games


def day2_part2():
    powers = 0
    for file_line in get_line_content("input1_day2"):
        fewer_reds = get_max_color_occurrences("red", file_line)
        fewer_greens = get_max_color_occurrences("green", file_line)
        fewer_blues = get_max_color_occurrences("blue", file_line)
        powers += fewer_reds * fewer_greens * fewer_blues

    return powers


profile_and_print_result(day2_part1)
profile_and_print_result(day2_part2)

# Ex:
# Result => 2541. Time taken 0.0029888153076171875 (s)
# Result => 66016. Time taken 0.002270936965942383 (s)
