from collections import defaultdict


def find_center_by_degree(edges: list[list[int]]) -> int:
    """Count degrees: the center touches every edge."""
    degree: defaultdict[int, int] = defaultdict(int)
    for u, v in edges:
        degree[u] += 1
        degree[v] += 1

    for node, deg in degree.items():
        if deg == len(edges):   # n - 1 edges, all at the center
            return node
    raise ValueError("the edges do not form a star")
