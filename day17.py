from dataclasses import dataclass

from utils import get_line_content, profile_and_print_result
import heapq

INFINITY = float("inf")


@dataclass(frozen=True)
class NodeState:
    heat_loss: int
    node: (int, int)
    direction: (int, int)
    same_dir: int

    def __lt__(self, other):
        return self.heat_loss < other.heat_loss


class DijkstraPriorityQueue:
    def __init__(self):
        self.queue = []
        self.state_seen = set()

    def extract_min(self) -> NodeState:
        return heapq.heappop(self.queue)

    def add(self, state: NodeState):
        look_up_key = (state.node, state.direction, state.same_dir)
        if look_up_key not in self.state_seen:
            heapq.heappush(self.queue, state)
            self.state_seen.add(look_up_key)


@dataclass(frozen=True)
class Dijkstra:
    graph: [[int]]

    def in_limit(self, v: (int, int), shift: (int, int)) -> bool:
        r, c = shift
        return 0 <= v[0] + r < len(self.graph) and 0 <= v[1] + c < len(self.graph)

    def neighbors_dirs(self, node: (int, int)) -> [(int, int)]:
        return [d for d in {(-1, 0), (1, 0), (0, -1), (0, 1)} if self.in_limit(node, d)]

    def get_state(self, node_state: NodeState, v_dir: (int, int), same_dir: int):
        node_row, node_col = node_state.node
        v_row, v_col = node_row + v_dir[0], node_col + v_dir[1]
        heat_loss = node_state.heat_loss + self.graph[v_row][v_col]
        return NodeState(heat_loss, (v_row, v_col), v_dir, same_dir)

    @staticmethod
    def is_opposite(node_dir: str, neigh_dir: (int, int)) -> bool:
        return node_dir[0] + neigh_dir[0] == 0 and node_dir[1] == neigh_dir[1] == 0

    @staticmethod
    def same_direction(node_dir: (int, int), neigh_dir: (int, int)):
        return node_dir == neigh_dir

    def filtered_neighbors(self, node_state: NodeState) -> [NodeState]:
        def is_not_opposite(neigh_dir: (int, int)) -> bool:
            return node_dir[0] + neigh_dir[0] != 0 or node_dir[1] + neigh_dir[1] != 0

        result = []
        node_dir = node_state.direction
        same_dir = node_state.same_dir

        for v_dir in filter(is_not_opposite, self.neighbors_dirs(node_state.node)):
            if self.same_direction(node_dir, v_dir):
                if same_dir < 3:
                    result.append(self.get_state(node_state, v_dir, same_dir + 1))
            else:
                result.append(self.get_state(node_state, v_dir, 1))
        return result

    def spsp(self, source: (int, int), destination: (int, int)) -> int:
        # Based on https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue

        Q = DijkstraPriorityQueue()
        state = NodeState(heat_loss=0, node=source, direction=(0, 1), same_dir=0)

        while state.node != destination:
            for vertex_state in self.filtered_neighbors(state):
                Q.add(vertex_state)

            state = Q.extract_min()
        return state.heat_loss


def day17_part1():
    puzzle = [[int(char) for char in line] for line in get_line_content("input1_day17")]

    source, destination = (0, 0), (len(puzzle) - 1, len(puzzle) - 1)
    return Dijkstra(puzzle).spsp(source, destination)


profile_and_print_result(day17_part1)


# Result => 767. Time taken 2.0909299850463867 (s)
