from collections import defaultdict
from collections.abc import Hashable


def build_graph(n: int, edges: list[list[int]],
                directed: bool = False) -> list[list[int]]:
    """Adjacency list for nodes labeled 0..n-1."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)          # undirected: both directions
    return graph


def build_graph_dict(
    edges: list[tuple[Hashable, Hashable]], directed: bool = False
) -> dict[Hashable, list[Hashable]]:
    """Adjacency list for arbitrary labels (strings, tuples...)."""
    graph: dict[Hashable, list[Hashable]] = defaultdict(list)
    for u, v in edges:
        graph[u].append(v)
        if not directed:
            graph[v].append(u)
    return graph
