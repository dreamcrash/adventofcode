from abc import abstractmethod
from dataclasses import dataclass

from utils import get_line_content, profile_and_print_result
import heapq


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

    def has_elements(self):
        return self.queue

    def extract_min(self) -> NodeState:
        return heapq.heappop(self.queue)

    def add(self, state: NodeState):
        look_up_key = (state.node, state.direction, state.same_dir)
        if look_up_key not in self.state_seen:
            heapq.heappush(self.queue, state)
            self.state_seen.add(look_up_key)


class Dijkstra:
    def __init__(self, graph: [[int]], source: (int, int)):
        self.graph = graph
        self.source = source

    def in_limit(self, v: (int, int), shift: (int, int)) -> bool:
        r, c = shift
        return 0 <= v[0] + r < len(self.graph) and 0 <= v[1] + c < len(self.graph)

    def neighbors_dirs(self, node: (int, int)) -> [(int, int)]:
        return [d for d in {(-1, 0), (1, 0), (0, -1), (0, 1)} if self.in_limit(node, d)]

    def get_state(self, node_state: NodeState, v_dir: (int, int), same_dir: int):
        v_row, v_col = node_state.node[0] + v_dir[0], node_state.node[1] + v_dir[1]
        heat_loss = node_state.heat_loss + self.graph[v_row][v_col]
        return NodeState(heat_loss, (v_row, v_col), v_dir, same_dir)

    @abstractmethod
    def different_direction_condition(self, same_dir: int) -> bool:
        raise NotImplemented

    @abstractmethod
    def same_direction_condition(self, same_dir: int) -> bool:
        raise NotImplemented

    def filtered_neighbors(self, node_state: NodeState) -> [NodeState]:
        def is_not_opposite(neigh_dir: (int, int)) -> bool:
            return node_dir[0] + neigh_dir[0] != 0 or node_dir[1] + neigh_dir[1] != 0

        result = []
        node_dir = node_state.direction
        same_dir = node_state.same_dir

        neighbors_dirs = self.neighbors_dirs(node_state.node)

        for v_dir in filter(is_not_opposite, neighbors_dirs):
            if node_dir != v_dir:
                if self.different_direction_condition(same_dir):
                    result.append(self.get_state(node_state, v_dir, 1))
            elif self.same_direction_condition(same_dir):
                result.append(self.get_state(node_state, v_dir, same_dir + 1))
        return result

    @abstractmethod
    def node_found(self, state: NodeState):
        raise NotImplemented

    def spsp(self) -> int:
        # Based on https://en.wikipedia.org/wiki/Dijkstra%27s_algorithm#Using_a_priority_queue

        Q = DijkstraPriorityQueue()
        Q.add(NodeState(heat_loss=0, node=self.source, direction=(1, 0), same_dir=0))
        Q.add(NodeState(heat_loss=0, node=self.source, direction=(0, 1), same_dir=0))

        while Q.has_elements():
            state = Q.extract_min()

            if self.node_found(state):
                return state.heat_loss

            for vertex_state in self.filtered_neighbors(state):
                Q.add(vertex_state)

        return -1


class DijkstraPart1(Dijkstra):
    def __init__(self, graph: [[int]]):
        super().__init__(graph, (0, 0))
        self.dst = (len(graph) - 1, len(graph) - 1)

    def node_found(self, state: NodeState):
        return state.node == self.dst

    def different_direction_condition(self, same_dir: int) -> bool:
        return True

    def same_direction_condition(self, same_dir: int) -> bool:
        return same_dir < 3


class DijkstraPart2(Dijkstra):
    def __init__(self, graph: [[int]]):
        super().__init__(graph, (0, 0))
        self.dst = (len(graph) - 1, len(graph) - 1)

    def node_found(self, state: NodeState):
        return state.node == self.dst and state.same_dir >= 4

    def different_direction_condition(self, same_dir: int) -> bool:
        return same_dir >= 4

    def same_direction_condition(self, same_dir: int) -> bool:
        return same_dir < 10


def read_puzzle():
    return [[int(char) for char in line] for line in get_line_content("input1_day17")]


def day17_part1():
    return DijkstraPart1(read_puzzle()).spsp()


def day17_part2():
    return DijkstraPart2(read_puzzle()).spsp()


profile_and_print_result(day17_part1)
profile_and_print_result(day17_part2)


# Result => 767. Time taken 2.0909299850463867 (s)
