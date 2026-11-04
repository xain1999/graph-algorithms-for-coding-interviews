from itertools import product


def is_bipartite_brute(graph: list[list[int]]) -> bool:
    """Try every assignment of two colors to the nodes."""
    n = len(graph)
    for color in product((0, 1), repeat=n):
        if all(color[u] != color[v]
               for u in range(n) for v in graph[u]):
            return True
    return False
