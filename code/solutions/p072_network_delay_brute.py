def network_delay_time_brute(times: list[list[int]], n: int,
                             k: int) -> int:
    """Bellman-Ford: relax every edge until nothing changes."""
    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[k] = 0
    for _ in range(n - 1):
        changed = False
        for u, v, w in times:
            if dist[u] + w < dist[v]:
                dist[v] = dist[u] + w
                changed = True
        if not changed:
            break
    slowest = max(dist[1:])
    return -1 if slowest == INF else int(slowest)
