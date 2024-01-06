from dataclasses import dataclass

from utils import get_line_content, profile_and_print_result
import heapq

INFINITY = float("inf")

DIRECTION = {(-1, 0), (1, 0), (0, -1), (0, 1)}


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

    def in_limit(self, node: (int, int)):
        return 0 <= node[0] < len(self.graph) and 0 <= node[1] < len(self.graph)

    def neighbors(self, node: (int, int)) -> [(int, int)]:
        return filter(self.in_limit, [(node[0] + r, node[1] + c) for r, c in DIRECTION])

    @staticmethod
    def get_direction(node, v_row, v_col):
        node_row, node_col = node
        if node_row == v_row and node_col != v_col:
            return "r" if node_col < v_col else "l"
        return "d" if node_row < v_row else "u"

    @staticmethod
    def is_opposite_direction(node_dir: str, neigh_dir: str) -> bool:
        return (node_dir, neigh_dir) in {("r", "l"), ("l", "r"), ("u", "d"), ("d", "u")}

    def filtered_neighbors(self, node: (int, int), node_dir: str, same_dir: int):
        result = []
        vertex = self.neighbors(node)

        for v_row, v_col in vertex:
            v_dir = self.get_direction(node, v_row, v_col)

            if not self.is_opposite_direction(node_dir, v_dir):
                c = same_dir if node_dir == v_dir else 0

                if c < 3:
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
