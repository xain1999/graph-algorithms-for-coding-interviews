def find_the_city_brute(n: int, roads: list[list[int]],
                        threshold: int) -> int:
    """Bellman-Ford from every city: n rounds over all roads."""
    best_city, best_count = -1, n
    for src in range(n):
        dist = [float("inf")] * n
        dist[src] = 0
        for _ in range(n - 1):
            changed = False
            for a, b, length in roads:
                for u, v in ((a, b), (b, a)):   # two-way road
                    if dist[u] + length < dist[v]:
                        dist[v] = dist[u] + length
                        changed = True
            if not changed:
                break
        count = sum(1 for j in range(n)
                    if j != src and dist[j] <= threshold)
        if count <= best_count:
            best_city, best_count = src, count
    return best_city
