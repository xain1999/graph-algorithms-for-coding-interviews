import heapq


def prim(graph: list[list[tuple[int, int]]]) -> int:
    """MST weight of a connected undirected graph, growing one
    tree from node 0; graph[u] holds (v, w) pairs."""
    n = len(graph)
    in_tree = [False] * n
    heap = [(0, 0)]                     # (cost to attach, node)
    total = added = 0
    while heap and added < n:
        w, node = heapq.heappop(heap)
        if in_tree[node]:
            continue
        in_tree[node] = True
        total += w
        added += 1
        for nxt, cost in graph[node]:
            if not in_tree[nxt]:
                heapq.heappush(heap, (cost, nxt))
    return total if added == n else -1
