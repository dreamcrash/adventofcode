import re
from math import gcd

from utils import profile_and_print_result, get_line_content


def create_graph(connections: [str]) -> dict:
    graph = {}
    pattern = r"(\w+)\s*=\s*\((\w+),\s*(\w+)\)"
    for c in connections:
        match = re.match(pattern, c)
        if match:
            value = match.group(1)
            left = match.group(2)
            right = match.group(3)
            graph.update({value: (left, right)})
    return graph


def compute_lcm(values):
    lcm = 1
    for i in values:
        lcm = lcm * i // gcd(lcm, i)
    return lcm


def get_number_of_steps(node: str, route: str, graph: dict, stop_condition):
    steps = 0
    current = graph.get(node)
    while not stop_condition(node):
        for r in route:
            node = current[0] if r == "L" else current[1]
            current = graph.get(node)
            steps += 1
            if stop_condition(node):
                break
    return steps


def day8_part1():
    def stop_condition(node):
        return node == "ZZZ"

    route, *connections = get_line_content("input1_day8")
    graph = create_graph(connections)
    return get_number_of_steps("AAA", route, graph, stop_condition)


def day8_part2():
    def stop_condition(node):
        return node[-1] == "Z"

    route, *connections = get_line_content("input1_day8")
    graph = create_graph(connections)
    nodes_end_a = [node for node in graph.keys() if node[-1] == "A"]

    steps = [get_number_of_steps(node, route, graph, stop_condition) for node in nodes_end_a]
    return compute_lcm(steps)


profile_and_print_result(day8_part1)
profile_and_print_result(day8_part2)


#
# Result => 19783. Time taken 0.011659860610961914 (s)
# Result => 9177460370549. Time taken 0.04223322868347168 (s)
