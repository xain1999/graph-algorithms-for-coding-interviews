import heapq


def max_probability(n: int, edges: list[list[int]],
                    succ_prob: list[float], start: int,
                    end: int) -> float:
    """Highest product of edge probabilities from start to end."""
    graph: list[list[tuple[int, float]]] = [[] for _ in range(n)]
    for (a, b), p in zip(edges, succ_prob):
        graph[a].append((b, p))         # undirected: both ways
        graph[b].append((a, p))

    best = [0.0] * n                    # 0.0 = not reached yet
    best[start] = 1.0
    heap = [(-1.0, start)]              # negated: a max-heap
    while heap:
        neg, node = heapq.heappop(heap)
        prob = -neg
        if prob < best[node]:
            continue                    # stale entry
        if node == end:
            return prob                 # popped = final
        for nxt, p in graph[node]:
            cand = prob * p
            if cand > best[nxt]:
                best[nxt] = cand
                heapq.heappush(heap, (-cand, nxt))
    return 0.0
