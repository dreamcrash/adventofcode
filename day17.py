from utils import get_line_content, profile_and_print_result
import heapq

INFINITY = float("inf")


class DijkstraPriorityQueue:
    def __init__(self):
        self.queue = []
        self.state_seen = set()

    def extract_min(self):
        return heapq.heappop(self.queue)

    def add_with_priority(self, l, n, d, c):
        if (n, d, c) not in self.state_seen:
            heapq.heappush(self.queue, (l, n, d, c))
            self.state_seen.add((n, d, c))

    def is_empty(self) -> bool:
        return len(self.queue) <= 0


class Dijkstra:
    def __init__(self, graph: [[int]]):
        self.graph = graph

    def neighbors(self, node: (int, int)) -> [(int, int)]:
        row, col = node
        n = []
        if 0 < row:
            n.append((row - 1, col))
        if row < len(self.graph) - 1:
            n.append((row + 1, col))
        if 0 < col:
            n.append((row, col - 1))
        if col < len(self.graph) - 1:
            n.append((row, col + 1))
        return n

    def filter_based_on_problem_restrictions(
        self, node: (int, int), direction: str, same_dir: int, vertex: [(int, int)]
    ):
        result = []
        for v in vertex:
            curr_node = node
            # Moving horizontally
            if curr_node[0] == v[0] and curr_node[1] != v[1]:
                if curr_node[1] < v[1]:
                    d = "r"
                else:
                    d = "l"
            # Moving vertically
            else:
                if curr_node[0] < v[0]:
                    d = "d"
                else:
                    d = "u"

            if direction == "r" and d == "l" or direction == "l" and d == "r":
                continue
            if direction == "u" and d == "d" or direction == "d" and d == "u":
                continue

            if direction == d:
                c = same_dir
            else:
                c = 0

            if c < 3:
                heat_loss = self.get_heat_loss(v)
                result.append((heat_loss, v, d, c + 1))
            else:
                continue
        return result

    def get_heat_loss(self, v: (int, int)):
        row, col = v
        return self.graph[row][col]

    def spsp(self, source: (int, int), destination: (int, int)) -> int:
        # Based on https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue

        Q = DijkstraPriorityQueue()
        heat_loss, node, direction, same_dir = 0, source, "r", 0
        
        while node != destination:
            potential_neighbors = self.neighbors(node)
            neighbors = self.filter_based_on_problem_restrictions(
                node, direction, same_dir, potential_neighbors
            )
            for h_l, v, d, c in neighbors:
                alt = heat_loss + h_l
                Q.add_with_priority(alt, v, d, c)

            heat_loss, node, direction, same_dir = Q.extract_min()
        return heat_loss


def day17_part1():
    puzzle = [[int(char) for char in line] for line in get_line_content("input1_day17")]

    source, destination = (0, 0), (len(puzzle) - 1, len(puzzle) - 1)
    return Dijkstra(puzzle).spsp(source, destination)


profile_and_print_result(day17_part1)


# Result => 767. Time taken 2.0909299850463867 (s)