from dataclasses import dataclass

from utils import get_line_content, profile_and_print_result
import heapq

INFINITY = float("inf")

DIRECTION = {(-1, 0): "d", (1, 0): "u", (0, -1): "l", (0, 1): "r"}


@dataclass(frozen=True)
class DijkstraPriorityQueue:
    queue = []
    state_seen = set()

    def extract_min(self):
        return heapq.heappop(self.queue)

    def add(self, heat_loss: int, node: (int, int), direction: str, same_dir: int):
        look_up_key = (node, direction, same_dir)
        if look_up_key not in self.state_seen:
            heapq.heappush(self.queue, (heat_loss, node, direction, same_dir))
            self.state_seen.add(look_up_key)


@dataclass(frozen=True)
class Dijkstra:
    graph: [[int]]

    def in_limit(self, v: (int, int), shift: (int, int)) -> bool:
        r, c = shift
        return 0 <= v[0] + r < len(self.graph) and 0 <= v[1] + c < len(self.graph)

    def neighbors_directions(self, node: (int, int)) -> [(int, int)]:
        return [(s, d) for (s, d) in DIRECTION.items() if self.in_limit(node, s)]

    @staticmethod
    def is_opposite_direction(node_dir: str, neigh_dir: str) -> bool:
        return (node_dir, neigh_dir) in {("r", "l"), ("l", "r"), ("u", "d"), ("d", "u")}

    def filtered_neighbors(self, node: (int, int), node_dir: str, same_dir: int):
        result = []
        directions = self.neighbors_directions(node)
        for (v_shift_row, v_shift_col), v_dir in directions:
            c = same_dir if node_dir == v_dir else 0

            if c < 3 and not self.is_opposite_direction(node_dir, v_dir):
                v_row, v_col = node[0] + v_shift_row, node[1] + v_shift_col
                heat_loss = self.graph[v_row][v_col]
                result.append((heat_loss, (v_row, v_col), v_dir, c + 1))
        return result

    def spsp(self, source: (int, int), destination: (int, int)) -> int:
        # Based on https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue

        Q = DijkstraPriorityQueue()
        heat_loss, node, direction, same_dir = 0, source, "r", 0

        while node != destination:
            for h_l, v, d, c in self.filtered_neighbors(node, direction, same_dir):
                Q.add(heat_loss + h_l, v, d, c)

            heat_loss, node, direction, same_dir = Q.extract_min()
        return heat_loss


def day17_part1():
    puzzle = [[int(char) for char in line] for line in get_line_content("input1_day17")]

    source, destination = (0, 0), (len(puzzle) - 1, len(puzzle) - 1)
    return Dijkstra(puzzle).spsp(source, destination)


profile_and_print_result(day17_part1)


# Result => 767. Time taken 2.0909299850463867 (s)
