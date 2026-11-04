from templates.components import count_components


def has_cycle_by_counting(n: int, edges: list[list[int]]) -> bool:
    """A forest with c components has exactly n - c edges."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    return len(edges) > n - count_components(graph)
