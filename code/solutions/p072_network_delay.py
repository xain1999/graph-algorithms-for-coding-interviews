import heapq


def network_delay_time(times: list[list[int]], n: int,
                       k: int) -> int:
    """Time until all n nodes hear from k, or -1 if some never do."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n + 1)]
    for u, v, w in times:               # nodes are 1..n; 0 unused
        graph[u].append((v, w))

    INF = float("inf")
    dist = [INF] * (n + 1)
    dist[k] = 0
    heap = [(0, k)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                    # stale entry
        for nxt, w in graph[node]:
            if d + w < dist[nxt]:
                dist[nxt] = d + w
                heapq.heappush(heap, (d + w, nxt))

    slowest = max(dist[1:])             # skip the unused slot 0
    return -1 if slowest == INF else int(slowest)
