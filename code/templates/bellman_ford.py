def bellman_ford(n: int, edges: list[list[int]], source: int,
                 rounds: int | None = None) -> list[float]:
    """Cheapest costs using at most `rounds` edges (default n - 1).
    Negative weights are fine; negative cycles are not detected."""
    dist = [float("inf")] * n
    dist[source] = 0
    for _ in range(n - 1 if rounds is None else rounds):
        new = dist[:]                   # read old values only
        for u, v, w in edges:
            if dist[u] + w < new[v]:
                new[v] = dist[u] + w
        if new == dist:
            break                       # nothing changed: done early
        dist = new
    return dist
