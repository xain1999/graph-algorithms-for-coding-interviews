import heapq


def min_cost_to_supply_water_prim(n: int, wells: list[int],
                                  pipes: list[list[int]]) -> int:
    """Same virtual node, then Prim with a heap from node 0."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n + 1)]
    for house, cost in enumerate(wells, start=1):
        graph[0].append((house, cost))
        graph[house].append((0, cost))
    for a, b, cost in pipes:
        graph[a].append((b, cost))
        graph[b].append((a, cost))
    in_tree = [False] * (n + 1)
    heap = [(0, 0)]                     # (cost to attach, node)
    total = added = 0
    while heap and added < n + 1:
        cost, node = heapq.heappop(heap)
        if in_tree[node]:
            continue                    # stale entry
        in_tree[node] = True
        total += cost
        added += 1
        for nxt, w in graph[node]:
            if not in_tree[nxt]:
                heapq.heappush(heap, (w, nxt))
    return total
