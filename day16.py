from __future__ import annotations
from collections import deque
from enum import Enum, auto
from typing import Callable, Optional

from utils import profile_and_print_result, get_line_content


def read_board() -> [[str]]:
    return list(map(list, get_line_content("input1_day16")))


def copy_board(board: [[str]]) -> [[str]]:
    return [r.copy() for r in board]


class Direction(Enum):
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()


class BeanMovement:
    def __init__(self, board: [[str]]):
        self.board = board
        self.beans = [["." for _ in range(len(board))] for _ in range(len(board))]

    @staticmethod
    def left(row: int, col: int) -> (str, int, int):
        return Direction.LEFT, row, col - 1

    @staticmethod
    def right(row: int, col: int) -> (str, int, int):
        return Direction.RIGHT, row, col + 1

    @staticmethod
    def up(row: int, col: int) -> (str, int, int):
        return Direction.UP, row - 1, col

    @staticmethod
    def down(row: int, col: int) -> (str, int, int):
        return Direction.DOWN, row + 1, col

    def move(
        self,
        row: int,
        col: int,
        direction: str,
        split: str,
        backslash_direction: Callable,
        forward_slash_direction: Callable,
    ) -> Optional[list]:
        self.beans[row][col] = "#"
        current_value = self.board[row][col]
        if current_value == direction:
            return []

        if current_value == "\\":
            return [backslash_direction(row, col)]

        if current_value == split:
            return [backslash_direction(row, col), forward_slash_direction(row, col)]

        if current_value == "/":
            return [forward_slash_direction(row, col)]

        if current_value == ".":
            self.board[row][col] = direction

        return None

    def move_left(self, row: int, col: int) -> [(int, int, int)]:
        for col_pos in range(col, -1, -1):
            r = self.move(row, col_pos, "<", "|", self.up, self.down)
            if r is not None:
                return r
        return []

    def move_right(self, row: int, col: int) -> [(int, int, int)]:
        for col_pos in range(col, len(self.board)):
            r = self.move(row, col_pos, ">", "|", self.down, self.up)
            if r is not None:
                return r
        return []

    def move_upwards(self, row: int, col: int) -> [(int, int, int)]:
        for row_pos in range(row, -1, -1):
            r = self.move(row_pos, col, "^", "-", self.left, self.right)
            if r is not None:
                return r
        return []

    def move_downwards(self, row: int, col: int) -> [(int, int, int)]:
        for row_pos in range(row, len(self.board)):
            r = self.move(row_pos, col, "v", "-", self.right, self.left)
            if r is not None:
                return r
        return []

    def move_bean(self, entry) -> BeanMovement:
        paths = deque()
        paths.append(entry)
        while len(paths):
            path = paths.popleft()
            direction, current_row, current_col = path

            if direction == Direction.RIGHT:
                new_path = self.move_right(current_row, current_col)
            elif direction == Direction.LEFT:
                new_path = self.move_left(current_row, current_col)
            elif direction == Direction.UP:
                new_path = self.move_upwards(current_row, current_col)
            else:
                new_path = self.move_downwards(current_row, current_col)

            if new_path:
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


def day16_part1():
    return BeanMovement(read_board()).move_bean((Direction.RIGHT, 0, 0)).count_beans()


def get_max_beans(board: [[str]], pos: int) -> int:
    def beans(entry):
        return BeanMovement(copy_board(board)).move_bean(entry).count_beans()

    down = beans((Direction.DOWN, 0, pos))
    up = beans((Direction.UP, len(board) - 1, pos))
    right = beans((Direction.RIGHT, pos, 0))
    left = beans((Direction.LEFT, pos, len(board) - 1))
    return max(down, up, right, left)


def day16_part2():
    board = read_board()
    return max(get_max_beans(board, pos) for pos in range(len(board)))


profile_and_print_result(day16_part1)
profile_and_print_result(day16_part2)


# Result => 7046. Time taken 0.015785932540893555 (s)
# Result => 7313. Time taken 3.8147928714752197 (s)
