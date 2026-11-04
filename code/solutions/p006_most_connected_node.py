def most_connected_node(n: int, edges: list[list[int]]) -> int:
    """Node with the most edges; ties go to the smallest label."""
    degree = [0] * n
    for u, v in edges:
        degree[u] += 1              # an undirected edge touches
        degree[v] += 1              # both of its ends

    best = 0
    for node in range(1, n):
        if degree[node] > degree[best]:     # strict: on a tie,
            best = node                     # keep the smaller label
    return best
