import heapq


def dijkstra(graph: list[list[tuple[int, int]]],
             source: int) -> list[float]:
    """Cheapest cost from source to every node; graph[u] holds
    (v, w) pairs with w >= 0. Unreachable nodes stay at inf."""
    dist = [float("inf")] * len(graph)
    dist[source] = 0
    heap = [(0, source)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                    # stale: improved already
        for nxt, w in graph[node]:
            nd = d + w
            if nd < dist[nxt]:
                dist[nxt] = nd
                heapq.heappush(heap, (nd, nxt))
    return dist
