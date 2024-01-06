from collections import deque
from dataclasses import dataclass
from typing import Any, Callable


@dataclass(frozen=True)
class GraphPath:
    # {e1: v1, e2:v1 .....}
    # Represent path from v1 to e1
    path: {Any: Any}

    @property
    def nodes(self) -> {Any}:
        return set(self.path)

    def contains(self, e) -> bool:
        return e in self.path

    def add(self, e: Any, v: Any):
        self.path.update({e: v})

    def transverse(self, org: Any, dst: Any, func: Callable) -> list:
        r = []
        v = dst
        while v != org:
            u = self.path[v]
            r.append(func(u, v))
            v = u
        return r


@dataclass(frozen=True)
class GraphHandler:
    # vector1 -> {e1:w1, e2:w2, e3:w3}
    # vector2 -> ....
    # w = -1 means not connected
    graph: {Any: {Any, int}}

    def init_weights(self, w: int):
        for v, edges in self.graph.items():
            for e in edges:
                self.graph[v][e] = w

    @property
    def nodes(self) -> list:
        return list(self.graph.keys())

    def neighbors(self, v: Any) -> list:
        return self.graph[v].items()

    def reachable_neighbors(self, v: Any) -> list:
        return [e for e, w in self.neighbors(v) if w > 0]

    def get_weight(self, v: Any, e: Any) -> int:
        return self.graph[v][e]

    def add_weight(self, v: Any, e: Any, w: int):
        self.graph[v][e] += w

    def sub_weight(self, v: Any, e: Any, w: int):
        self.graph[v][e] -= w

    # Implementation based on https://favtutor.com/blogs/breadth-first-search-python
    def bfs(self, source: str) -> GraphPath:
        path = GraphPath({})
        queue = deque([source])
        while queue:
            v = queue.popleft()
            for e in self.reachable_neighbors(v):
                if not path.contains(e):
                    path.add(e, v)
                    queue.append(e)
        return path
