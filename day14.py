from __future__ import annotations

from dataclasses import dataclass

from utils import profile_and_print_result, get_line_content
from collections import deque


@dataclass(frozen=True)
class BoardCycleHistory:
    board_manager: BoardManager
    board_states: list
    total_cycles: int

    def cycle(self) -> bool:
        self.board_manager.cycle()

        if self.board_manager.board in self.board_states:
            return True
        self.board_states.append(self.board_manager.get_board_copy())
        return False

    def get_count(self) -> int:
        board = self.board_manager.board
        being_cycle = self.board_states.index(board)
        cycle_length = len(self.board_states) - being_cycle
        final_state = being_cycle + (self.total_cycles - being_cycle) % cycle_length
        return BoardManager(self.board_states[final_state]).get_count()


class BoardManager:
    def __init__(self, board: [[str]]):
        self.board = board
        self.rock = "O"
        self.space = "."
        self.shaped_rock = "#"

    def get_board_copy(self) -> [[str]]:
        return [r.copy() for r in self.board]

    def _transpose(self) -> BoardManager:
        self.board = list(map(list, zip(*self.board)))
        return self

    def _flip_vertically(self) -> BoardManager:
        self.board = [row[::-1] for row in self.board]
        return self

    def rotate_90_anti_clockwise(self) -> BoardManager:
        return self._transpose()._flip_vertically()

    def is_rock(self, row: int, col: int) -> bool:
        return self.board[row][col] == self.rock

    def tilting(self) -> BoardManager:
        for col in range(len(self.board[0])):
            spaces = deque()
            for row in range(len(self.board)):
                if self.board[row][col] == self.space:
                    spaces.append(row)
                elif len(spaces) and self.is_rock(row, col):
                    free_row = spaces.popleft()
                    self.board[free_row][col] = self.rock
                    self.board[row][col] = self.space
                    spaces.append(row)
                elif self.board[row][col] == self.shaped_rock:
                    spaces.clear()
        return self

    def cycle(self):
        (
            self.tilting()
            .rotate_90_anti_clockwise()
            .tilting()
            .rotate_90_anti_clockwise()
            .tilting()
            .rotate_90_anti_clockwise()
            .tilting()
            .rotate_90_anti_clockwise()
        )

    def get_count_per_row(self, col: [str]) -> int:
        rows = len(self.board)
        return sum(rows - r for r in range(rows) if self.is_rock(r, col))

    def get_count(self) -> int:
        return sum(self.get_count_per_row(col) for col in range(len(self.board[0])))


def read_board() -> [[str]]:
    return list(map(list, get_line_content("input1_day14")))


def day14_part1() -> int:
    return BoardManager(read_board()).tilting().get_count()


def day14_part2() -> int:
    board = read_board()
    board_cycle = BoardCycleHistory(BoardManager(board), [board.copy()], 1000000000)

    while not board_cycle.cycle():
        pass

    return board_cycle.get_count()


profile_and_print_result(day14_part1)
profile_and_print_result(day14_part2)


# Result => 113525. Time taken 0.008890867233276367 (s)
# Result => 101292. Time taken 3.340752124786377 (s)

