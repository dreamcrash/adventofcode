from utils import profile_and_print_result, find_all_digits, get_line_content


def from_file_to_pair_of_number_lists() -> (list, list):
    winning_numbers = []
    my_numbers = []
    for file_line in get_line_content("input1_day4"):
        numbers_lists = file_line[file_line.find(":") + 1 :].split("|")
        winning_numbers.append(find_all_digits(numbers_lists[0]))
        my_numbers.append(find_all_digits(numbers_lists[1]))

    return winning_numbers, my_numbers


def day4_part1():
    result = 0
    winning_numbers, my_numbers = from_file_to_pair_of_number_lists()
    for w_n, m_n in zip(winning_numbers, my_numbers):
        same_number = set(m_n).intersection(set(w_n))
        result += pow(2, len(same_number) - 1) if same_number else 0

    return result


def count_instances(same_numbers: list, begin_card_id: int, end_card_id: int):
    total_instances = 0
    for card_id in range(begin_card_id, end_card_id):
        instances = same_numbers[card_id]
        end = card_id + instances + 1
        total_instances += instances + count_instances(same_numbers, card_id + 1, end)
    return total_instances


def day4_part2():
    winning_numbers, my_numbers = from_file_to_pair_of_number_lists()

    same_numbers = [
        len(set(m_n).intersection(set(w_n)))
        for w_n, m_n in zip(winning_numbers, my_numbers)
    ]

    sum_ = count_instances(same_numbers, 0, len(same_numbers))
    return sum_ + len(same_numbers)


def day4_part2_faster_solution():
    """
    With this solution I perform the calculation in reverse and therefore
    I can cache and reuse some of the calculations
    """
    winning_numbers, my_numbers = from_file_to_pair_of_number_lists()

    same_numbers = [
        len(set(m_n).intersection(set(w_n)))
        for w_n, m_n in zip(winning_numbers, my_numbers)
    ]

    cached_results = [1] * len(same_numbers)
    for card_id in range(len(same_numbers) - 1, -1, -1):
        instances = same_numbers[card_id]
        for card_id_copy in list(range(card_id + 1, card_id + instances + 1)):
            cached_results[card_id] += cached_results[card_id_copy]

    return sum(cached_results)


profile_and_print_result(day4_part1)
profile_and_print_result(day4_part2)
profile_and_print_result(day4_part2_faster_solution)

# Ex
# Result => 17803. Time taken 0.00452113151550293 (s)
# Result => 5554894. Time taken 3.463101863861084 (s)
# Result => 5554894. Time taken 0.004187107086181641 (s) (853 times faster)
