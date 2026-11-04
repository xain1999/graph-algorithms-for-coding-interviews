def most_connected_node_adj(n: int, edges: list[list[int]]) -> int:
    """Same answer, read off an adjacency list."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    # max() keeps the first node it meets among equal degrees
    return max(range(n), key=lambda node: len(graph[node]))
