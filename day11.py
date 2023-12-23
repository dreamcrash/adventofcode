from bisect import bisect

from utils import profile_and_print_result, get_line_content


def get_empty_space(positions: [int], pos: int) -> int:
    """
    Counts how many values in positions are lower than pos. Assumes the list is in ascending order.
    """
    return bisect(positions, pos)


def add_expansion(size: int, exp_factor: int, rows: [int], cols: [int]) -> [(int, int)]:
    empty_rows = [i for i in range(size) if i not in rows]
    empty_cols = [i for i in range(size) if i not in cols]

    real_coord = []
    for pos_row, pos_col in zip(rows, cols):
        empty_r_size = get_empty_space(empty_rows, pos_row) * exp_factor
        empty_c_size = get_empty_space(empty_cols, pos_col) * exp_factor
        real_coord.append((pos_row + empty_r_size, pos_col + empty_c_size))
    return real_coord


def get_galaxies_coordinates(universe: list, expansion_factor) -> [(int, int)]:
    rows, cols = [], []
    for pos_row in range(len(universe)):
        for pos_col in range(len(universe[pos_row])):
            if universe[pos_row][pos_col] == "#":
                rows.append(pos_row)
                cols.append(pos_col)

    return add_expansion(len(universe), expansion_factor, rows, cols)


def distance(coord1: (int, int), coord2: (int, int)) -> (int, int):
    return abs(coord1[0] - coord2[0]), abs(coord1[1] - coord2[1])


def get_distances(current_galaxy_pos: int, real_coord: [int]) -> [(int, int)]:
    """
    Gets the distance between one galaxy and the remaining galaxies
    next on line, does not calculate the pairs before.
    """
    return [
        distance(real_coord[current_galaxy_pos], real_coord[next_pos])
        for next_pos in range(current_galaxy_pos + 1, len(real_coord))
    ]


def get_min_steps(expansion_factor: int) -> int:
    universe = get_line_content("input1_day11")

    # Gets the coordinates after expansion
    # Calculate the coordinate distances between pairs of galaxies
    # Gets the total steps between pairs of galaxies

    real_coord = get_galaxies_coordinates(universe, expansion_factor)
    coord_distances = [get_distances(pos, real_coord) for pos in range(len(real_coord))]
    return sum([sum(r + c for r, c in dist) for dist in coord_distances])


def day11_part1():
    return get_min_steps(expansion_factor=1)


def day11_part2():
    return get_min_steps(expansion_factor=1000000 - 1)


profile_and_print_result(day11_part1)
profile_and_print_result(day11_part2)

# Result => 10494813. Time taken 0.08510017395019531 (s)
# Result => 840988812853. Time taken 0.08567595481872559 (s)
