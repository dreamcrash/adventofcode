from utils import profile_and_print_result, get_line_content, find_all_digits


def get_count(spring, exp_count, s_pos=0, ec_pos=0, cc_hash=0):
    count = 0

    for pos in range(s_pos, len(spring)):
        if spring[pos] == "#":
            cc_hash += 1
        else:
            if spring[pos] == "?":
                # Assuming #
                count += get_count(spring, exp_count, pos + 1, ec_pos, cc_hash + 1)

            # Assuming '.'
            if ec_pos < len(exp_count) and 0 < cc_hash == exp_count[ec_pos]:
                ec_pos += 1
                cc_hash = 0
            elif cc_hash > 0:
                return count

    all_hash_read = cc_hash == 0 and ec_pos == len(exp_count)
    is_count_correct = ec_pos == len(exp_count) - 1 and exp_count[ec_pos] == cc_hash
    return count + 1 if all_hash_read or is_count_correct else count


def day12_part1():
    puzzle = get_line_content("input1_day12")
    puzzle = [v.split() for v in puzzle]
    puzzle = [(v1, find_all_digits(v2)) for v1, v2 in puzzle]

    return sum(get_count(spring, digits) for spring, digits in puzzle)


profile_and_print_result(day12_part1)

# Result => 7173. Time taken 0.16173219680786133 (s)

