def closest_meeting_node(edges: list[int], node1: int,
                         node2: int) -> int:
    """Closest node reachable from both starts, or -1 if none."""
    n = len(edges)

    def walk(start: int) -> list[int]:
        """Distance from start to every node on its path, else -1."""
        dist = [-1] * n
        node, d = start, 0
        while node != -1 and dist[node] == -1:  # stop at a dead end
            dist[node] = d                       # or on a revisit
            node, d = edges[node], d + 1
        return dist

    dist1, dist2 = walk(node1), walk(node2)
    best, best_cost = -1, n             # every distance is below n
    for v in range(n):
        if dist1[v] != -1 and dist2[v] != -1:
            cost = max(dist1[v], dist2[v])
            if cost < best_cost:        # strict: ties keep smaller v
                best, best_cost = v, cost
    return best
