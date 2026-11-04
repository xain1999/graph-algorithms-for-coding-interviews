import heapq
import math


def max_probability_log(n: int, edges: list[list[int]],
                        succ_prob: list[float], start: int,
                        end: int) -> float:
    """Plain Dijkstra on weights -log(p), then undo the log."""
    graph: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for (a, b), p in zip(edges, succ_prob):
        if p > 0:                       # p = 0 is no road at all
            w = -math.log(p)            # >= 0 because p <= 1
            graph[a].append((b, w))
            graph[b].append((a, w))

    dist = [math.inf] * n
    dist[start] = 0.0
    heap = [(0.0, start)]
    while heap:
        d, node = heapq.heappop(heap)
        if d > dist[node]:
            continue
        if node == end:
            return math.exp(-d)
        for nxt, w in graph[node]:
            if d + w < dist[nxt]:
                dist[nxt] = d + w
                heapq.heappush(heap, (d + w, nxt))
    return 0.0
