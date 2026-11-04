import heapq


def cheapest_costs(n: int, roads: list[list[int]],
                   source: int) -> list[int]:
    """Cheapest cost from source to every depot, -1 if unreachable."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, cost in roads:
        graph[u].append((v, cost))      # one-way road
    INF = float("inf")
    dist = [INF] * n
    dist[source] = 0
    heap = [(0, source)]                # (cost so far, depot)
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                    # stale entry: skip it
        for nxt, cost in graph[node]:
            nd = d + cost
            if nd < dist[nxt]:          # found a cheaper way
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return [-1 if d == INF else int(d) for d in dist]
