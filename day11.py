from bisect import bisect

from utils import profile_and_print_result, get_line_content


def has_no_galaxy(line: list) -> bool:
    return "#" not in line


def get_empty_lines_coordinates(universe: list) -> [int]:
    return [r_p for r_p in range(len(universe)) if has_no_galaxy(universe[r_p])]


def get_empty_columns_coordinates(universe: list) -> [int]:
    col_to_expand = []
    for pos in range(len(universe)):
        col = [line[pos] for line in universe]
        if has_no_galaxy(col):
            col_to_expand.append(pos)
    return col_to_expand


def get_empty_space(positions: [int], pos: int) -> int:
    """
    Counts how many values in positions are lower than pos.
    Assumes the list is in ascending order.
    Basically counts the expanding space between 0 and pos
    """
    return bisect(positions, pos)


def get_galaxies_coordinates(universe: list, expansion_factor: int = 1) -> [(int, int)]:
    empty_rows = get_empty_lines_coordinates(universe)
    empty_cols = get_empty_columns_coordinates(universe)

    real_coord = []
    for pos_row in range(len(universe)):
        for pos_col in range(len(universe[pos_row])):
            if universe[pos_row][pos_col] == "#":
                empty_r_size = get_empty_space(empty_rows, pos_row) * expansion_factor
                empty_c_size = get_empty_space(empty_cols, pos_col) * expansion_factor
                real_coord.append((pos_row + empty_r_size, pos_col + empty_c_size))
    return real_coord


def get_distance(coord1: (int, int), coord2: (int, int)) -> (int, int):
    return abs(coord1[0] - coord2[0]), abs(coord1[1] - coord2[1])


def get_distances(current_galaxy_pos: int, real_coord: [int]) -> [(int, int)]:
    """
    Gets the distance between one galaxy and the remaining galaxies
    next on line, does not calculate the pairs before.
    """
    distances = []
    for next_pos in range(current_galaxy_pos + 1, len(real_coord)):
        distance = get_distance(real_coord[current_galaxy_pos], real_coord[next_pos])
        distances.append(distance)
    return distances


def day11_part1():
    universe = get_line_content("input1_day11")

    # Gets the coordinates after expansion
    # Calculate the coordinate distances between pairs of galaxies
    # Gets the total steps between pairs of galaxies

    real_coord = get_galaxies_coordinates(universe)
    coord_distances = [get_distances(pos, real_coord) for pos in range(len(real_coord))]
    min_steps = [[row + col for row, col in distance] for distance in coord_distances]

    return sum(map(sum, min_steps))


def day11_part2():
    universe = get_line_content("input1_day11")

    # Gets the coordinates after expansion
    # Calculate the coordinate distances between pairs of galaxies
    # Gets the total steps between pairs of galaxies

    real_coord = get_galaxies_coordinates(universe, expansion_factor=1000000-1)
    coord_distances = [get_distances(pos, real_coord) for pos in range(len(real_coord))]
    min_steps = [[row + col for row, col in distance] for distance in coord_distances]

    return sum(map(sum, min_steps))


profile_and_print_result(day11_part1)
profile_and_print_result(day11_part2)

# Result => 10494813. Time taken 0.09224200248718262 (s)
# Result => 840988812853. Time taken 0.1004788875579834 (s)
