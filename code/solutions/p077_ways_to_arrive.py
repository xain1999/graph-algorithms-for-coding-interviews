import heapq

MOD = 10**9 + 7


def count_paths(n: int, roads: list[list[int]]) -> int:
    """Number of fastest routes from 0 to n - 1, modulo 10^9 + 7."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, time in roads:
        graph[u].append((v, time))
        graph[v].append((u, time))

    dist = [float("inf")] * n
    ways = [0] * n
    dist[0], ways[0] = 0, 1
    heap = [(0, 0)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue                    # stale: never count it twice
        # node is final here, and so is ways[node]
        for nxt, time in graph[node]:
            nd = d + time
            if nd < dist[nxt]:          # strictly faster: start over
                dist[nxt] = nd
                ways[nxt] = ways[node]
                heapq.heappush(heap, (nd, nxt))
            elif nd == dist[nxt]:       # a tie: one more way in
                ways[nxt] = (ways[nxt] + ways[node]) % MOD
    return ways[n - 1]
