from utils import profile_and_print_result, get_line_content, find_all_digits


def try_hash(spring: str, counts: [int], cache: dict, key: (int, int, int)) -> int:
    return cache[key] if key in cache else get_count(spring, counts, cache, key)


def match(counts: [int], ec_pos: int, cc_hash: int) -> bool:
    all_hash_read = cc_hash == 0 and ec_pos == len(counts)
    is_count_correct = ec_pos == len(counts) - 1 and counts[ec_pos] == cc_hash
    return all_hash_read or is_count_correct


def get_count(spring: str, counts: [int], cache: dict, key=(0, 0, 0)) -> int:
    s_pos, ec_pos, cc_hash = key
    if ec_pos >= len(counts) or cc_hash > counts[ec_pos]:
        cache.update({key: 0})
        return 0

    count = 0
    for pos in range(s_pos, len(spring)):
        if spring[pos] == "#":
            cc_hash += 1
        else:
            if spring[pos] == "?":
                count += try_hash(spring, counts, cache, (pos + 1, ec_pos, cc_hash + 1))
            # Assuming '.'
            if ec_pos < len(counts) and 0 < cc_hash == counts[ec_pos]:
                ec_pos += 1
                cc_hash = 0
            elif cc_hash > 0:
                break

    result = count + 1 if match(counts, ec_pos, cc_hash) else count
    cache.update({key: result})
    return result


def day12_part1() -> int:
    puzzle = get_line_content("input1_day12")
    puzzle = [v.split() for v in puzzle]
    puzzle = [(v1, find_all_digits(v2)) for v1, v2 in puzzle]
    return sum(get_count(spring, digits, dict()) for spring, digits in puzzle)


def day12_part2() -> int:
    puzzle = get_line_content("input1_day12")
    puzzle = [v.split() for v in puzzle]
    puzzle = [
        (v1 + "?" + v1 + "?" + v1 + "?" + v1 + "?" + v1, find_all_digits(v2) * 5)
        for v1, v2 in puzzle
    ]
    return sum(get_count(spring, digits, dict()) for spring, digits in puzzle)


profile_and_print_result(day12_part1)
profile_and_print_result(day12_part2)

# Result => 7173. Time taken 0.08690690994262695 (s)
# Result => 29826669191291. Time taken 1.9400219917297363 (s)
