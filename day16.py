from __future__ import annotations
from collections import deque
from utils import profile_and_print_result, get_line_content


def read_board() -> [[str]]:
    return list(map(list, get_line_content("input1_day16")))


class BeanMovement:
    def __init__(self, board: [[str]]):
        self.board = board
        self.beans = [["." for _ in range(len(board))] for _ in range(len(board))]

    def move(self, row: int, col: int, sign: str, split: str, backslash, forward_slash):
        self.beans[row][col] = "#"
        current_value = self.board[row][col]

        if current_value == sign:
            return []

        if current_value == "\\":
            return [(backslash, row, col)]

        if current_value == split:
            return [(backslash, row, col), (forward_slash, row, col)]

        if current_value == "/":
            return [(forward_slash, row, col)]

        if current_value == ".":
            self.board[row][col] = sign

        return None

    def move_left(self, row: int, col: int) -> [(int, int, int)]:
        for col_pos in range(col - 1, -1, -1):
            r = self.move(row, col_pos, "<", "|", self.move_up, self.move_down)
            if r is not None:
                return r
        return []

    def move_right(self, row: int, col: int) -> [(int, int, int)]:
        for col_pos in range(col + 1, len(self.board)):
            r = self.move(row, col_pos, ">", "|", self.move_down, self.move_up)
            if r is not None:
                return r
        return []

    def move_up(self, row: int, col: int) -> [(int, int, int)]:
        for row_pos in range(row - 1, -1, -1):
            r = self.move(row_pos, col, "^", "-", self.move_left, self.move_right)
            if r is not None:
                return r
        return []

    def move_down(self, row: int, col: int) -> [(int, int, int)]:
        for row_pos in range(row + 1, len(self.board)):
            r = self.move(row_pos, col, "v", "-", self.move_right, self.move_left)
            if r is not None:
                return r
        return []

    def move_bean(self, entry) -> BeanMovement:
        paths = deque()
        paths.append(entry)
        while len(paths):
            path = paths.popleft()
            direction_method, current_row, current_col = path

            new_path = direction_method(current_row, current_col)

            new_path = self.remove_invalid_paths(new_path)
            paths.extend(new_path)
        return self

    def count_beans(self):
        count = 0
        for row in range(len(self.beans)):
            for col in range(len(self.beans)):
                if self.beans[row][col] == "#":
                    count += 1
        return count

    def remove_invalid_paths(self, new_path):
        def is_in_range(r, c):
            return 0 <= r < len(self.board) and 0 <= c < len(self.board)

        return [(d, r, c) for d, r, c in new_path if is_in_range(r, c)]

    def from_left_to_right(self, row: int = 0) -> BeanMovement:
        return self.move_bean((self.move_right, row, -1))

    def from_top_to_down(self, col: int) -> BeanMovement:
        return self.move_bean((self.move_down, -1, col))

    def from_right_to_left(self, row: int) -> BeanMovement:
        return self.move_bean((self.move_left, row, len(self.board)))

    def from_down_to_up(self, col: int) -> BeanMovement:
        return self.move_bean((self.move_up, len(self.board), col))


def day16_part1():
    return BeanMovement(read_board()).from_left_to_right().count_beans()


def get_max_beans(entry: int) -> int:
    def bean_movement():
        return BeanMovement(read_board())

    return max(
        bean_movement().from_down_to_up(entry).count_beans(),
        bean_movement().from_top_to_down(entry).count_beans(),
        bean_movement().from_right_to_left(entry).count_beans(),
        bean_movement().from_left_to_right(entry).count_beans(),
    )


def day16_part2():
    return max(get_max_beans(pos) for pos in range(len(read_board())))


profile_and_print_result(day16_part1)
profile_and_print_result(day16_part2)


# Result => 7046. Time taken 0.01368093490600586 (s)
# Result => 7313. Time taken 3.4262239933013916 (s)
