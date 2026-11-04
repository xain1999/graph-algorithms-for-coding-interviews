import heapq

MOD = 10**9 + 7


def count_paths_dag(n: int, roads: list[list[int]]) -> int:
    """Dijkstra for distances, then count on the shortest-path DAG."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, time in roads:
        graph[u].append((v, time))
        graph[v].append((u, time))
    dist = [float("inf")] * n
    dist[0] = 0
    heap = [(0, 0)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        for nxt, time in graph[node]:
            if d + time < dist[nxt]:
                dist[nxt] = d + time
                heapq.heappush(heap, (d + time, nxt))
    # Tight edges (dist[u] + t == dist[v]) form a DAG; walk it in
    # order of distance so every node is complete before it is used.
    ways = [0] * n
    ways[0] = 1
    for node in sorted(range(n), key=lambda x: dist[x]):
        for nxt, time in graph[node]:
            if dist[node] + time == dist[nxt]:
                ways[nxt] = (ways[nxt] + ways[node]) % MOD
    return ways[n - 1]
