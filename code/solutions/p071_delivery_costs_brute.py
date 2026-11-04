def cheapest_costs_brute(n: int, roads: list[list[int]],
                         source: int) -> list[int]:
    """Bellman-Ford: relax every road up to n - 1 times."""
    INF = float("inf")
    dist = [INF] * n
    dist[source] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, cost in roads:
            if dist[u] + cost < dist[v]:
                dist[v] = dist[u] + cost
                changed = True
        if not changed:                 # nothing moved: done early
            break
    return [-1 if d == INF else int(d) for d in dist]
