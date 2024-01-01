from dataclasses import dataclass

from Graph import GraphHandler
from utils import profile_and_print_result, get_line_content

# Using max flow mix cut algorithm as described on
# https://www.cs.princeton.edu/courses/archive/spring06/cos226/lectures/maxflow.pdf

# Using 'NetworkX' already provides function for graphs and max flow mix cut logic


CAPACITY = 1
INFINITY = float("inf")


def build_graph(puzzle: [(str, [str])]) -> dict:
    graph = {}
    for v, edges in puzzle:
        v_edges = graph.get(v, {})
        for e in edges:
            e_edges = graph.get(e, {})
            v_edges.update({e: 0})
            e_edges.update({v: 0})
            graph.update({e: e_edges})
        graph.update({v: v_edges})

    return graph


@dataclass(frozen=True)
class GraphController:
    graph: GraphHandler

    def augment_flow(self, aug_path: {str}, sink: str, source: str, flow: int):
        def augmenting_path(u: str, v: str):
            # Augmenting path = path in residual graph.
            # - Decrease flow along backward edges.
            # - Increase flow along forward edges.
            self.graph.sub_weight(u, v, flow)
            self.graph.add_weight(v, u, flow)

        aug_path.transverse(source, sink, augmenting_path)

    def get_bottleneck_capacity(self, aug_path: {str}, source: str, sink: str) -> int:
        def get_capacity(u: str, v: str):
            return self.graph.get_weight(u, v)

        return min(aug_path.transverse(source, sink, get_capacity))

    def max_flow_min_cut(self, aug_path: {str}, source: str, sink: str):
        bottle = self.get_bottleneck_capacity(aug_path, source, sink)

        self.augment_flow(aug_path, sink, source, bottle)

        # keep track of total flow sent from s (source) to t (sink)
        return bottle

    def ford_fulkerson_algorithm(self, source: str, sink: str) -> (int, str):
        self.graph.init_weights(CAPACITY)
        max_flow = 0
        while True:
            augmented_path = self.graph.bfs(source)

            # We stop as soon as there is no connection between the source and the sink
            if not augmented_path.contains(sink):
                return max_flow, augmented_path.nodes

            # keep track of total flow sent from s (source) to t (sink)
            max_flow += self.max_flow_min_cut(augmented_path, source, sink)


def solution(graph: dict):
    graph = GraphHandler(graph)
    nodes = graph.nodes
    source = nodes.pop(0)
    gc = GraphController(graph)
    for sink in nodes:
        max_flow, group1 = gc.ford_fulkerson_algorithm(source, sink)

        # The value of the max flow is equal to the capacity of the min cut.
        # Max flow of 3 means there are three cuts that broke the graph between
        # two groups, one containing the source and the other the sink
        if max_flow == 3:
            g2 = set(nodes) - group1
            return len(group1) * len(g2)
    return None


def day25_part1() -> int:
    puzzle_input = get_line_content("input1_day25")
    puzzle_input = [v.split(":") for v in puzzle_input]
    puzzle_input = [(v[0], v[1].split()) for v in puzzle_input]
    return solution(build_graph(puzzle_input))


def day25_networkx_solution() -> int:
    puzzle_input = get_line_content("input1_day25")
    puzzle_input = [v.split(":") for v in puzzle_input]
    puzzle_input = [(v[0], v[1].split()) for v in puzzle_input]

    import networkx

    graph = networkx.Graph()
    for v, edges in puzzle_input:
        for e in edges:
            graph.add_edge(v, e, capacity=1)

    source, *sinks = graph.nodes
    for sink in sinks:
        min_cut, nodes = networkx.minimum_cut(graph, source, sink)
        if min_cut == 3:
            return len(nodes[0]) * len(nodes[1])


profile_and_print_result(day25_part1)
profile_and_print_result(day25_networkx_solution)


# Result => 614655. Time taken 0.05007481575012207 (s)
# Result => 614655. Time taken 0.27106499671936035 (s)
