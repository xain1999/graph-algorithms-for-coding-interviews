def closest_meeting_node_brute(edges: list[int], node1: int,
                               node2: int) -> int:
    """Try every node; walk from both starts to measure distances."""
    n = len(edges)

    def steps_to(start: int, target: int) -> int:
        """Edges from start to target, or -1 if never reached."""
        node = start
        for d in range(n):              # a simple path has < n edges
            if node == target:
                return d
            node = edges[node]
            if node == -1:
                return -1
        return -1

    best, best_cost = -1, n
    for v in range(n):
        d1, d2 = steps_to(node1, v), steps_to(node2, v)
        if d1 != -1 and d2 != -1 and max(d1, d2) < best_cost:
            best, best_cost = v, max(d1, d2)
    return best
