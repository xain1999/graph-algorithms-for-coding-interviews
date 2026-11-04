def most_connected_node_brute(n: int, edges: list[list[int]]) -> int:
    """Count each node's edges by rescanning the whole edge list."""
    best, best_degree = 0, -1
    for node in range(n):
        degree = sum(1 for u, v in edges if node in (u, v))
        if degree > best_degree:
            best, best_degree = node, degree
    return best
