from __future__ import annotations

from utils import profile_and_print_result, get_line_content
from collections import deque


class BoardCycleHistory:
    def __init__(self, board_manager: BoardManager, total_cycles: int):
        self.board_manager = board_manager
        self.board_states = [board_manager.board]
        self.total_cycles = total_cycles

    def cycle(self):
        self.board_manager.cycle()
        if self.board_manager.board in self.board_states:
            return True
        self.board_states.append(self.board_manager.board)
        return False

    def get_final_state(self) -> BoardManager:
        board = self.board_manager.board
        being_cycle = self.board_states.index(board)
        cycle_length = len(self.board_states) - being_cycle
        final_state = being_cycle + (self.total_cycles - being_cycle) % cycle_length
        return BoardManager(self.board_states[final_state])


class BoardManager:
    def __init__(self, board: [[str]]):
        self.board = board
        self.rock = "O"
        self.space = "."
        self.shaped_rock = "#"

    def transpose(self) -> BoardManager:
        self.board = list(map(list, zip(*self.board)))
        return self

    def flip_vertically(self):
        self.board = [row[::-1] for row in self.board]
        return self

    def rotate_90_anti_clockwise(self) -> BoardManager:
        return self.transpose().flip_vertically()

    def tilting(self):
        for row in self.board:
            spaces = deque()
            for pos in range(len(row) - 1, -1, -1):
                if row[pos] == self.space:
                    spaces.append(pos)
                elif row[pos] == self.rock and len(spaces):
                    free_col = spaces.popleft()
                    row[free_col] = self.rock
                    row[pos] = self.space
                    spaces.append(pos)
                elif row[pos] == self.shaped_rock:
                    spaces.clear()
        return self

    def cycle(self):
        for _ in range(4):
            self.rotate_90_anti_clockwise().tilting()
        return self

    @staticmethod
    def get_count_per_row(row: [str]) -> int:
        return sum(pos + 1 for pos in range(len(row)) if row[pos] == "O")

    def get_count(self) -> int:
        return sum(self.get_count_per_row(row) for row in self.board)


def read_board() -> [[str]]:
    return list(map(list, get_line_content("input1_day14")))


def day14_part1() -> int:
    return BoardManager(read_board()).rotate_90_anti_clockwise().tilting().get_count()


def day14_part2() -> int:
    board_manager = BoardManager(read_board())
    board_cycle_history = BoardCycleHistory(board_manager, total_cycles=1000000000)

    while not board_cycle_history.cycle():
        pass

    return board_cycle_history.get_final_state().rotate_90_anti_clockwise().get_count()


profile_and_print_result(day14_part1)
profile_and_print_result(day14_part2)


# Result => 113525. Time taken 0.005136013031005859 (s)
# Result => 101292. Time taken 2.180093288421631 (s)


# Day 14 Part 1: 113525
# Result => None. Time taken 0.006552934646606445 (s)
# Day 14 Part 2: 101292
# Result => None. Time taken 3.947263240814209 (s)
