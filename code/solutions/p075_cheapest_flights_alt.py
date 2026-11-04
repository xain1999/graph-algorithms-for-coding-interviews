import heapq


def find_cheapest_price_dijkstra(n: int, flights: list[list[int]],
                                 src: int, dst: int, k: int) -> int:
    """Dijkstra on (city, flights used) states."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b, price in flights:
        graph[a].append((b, price))
    best = {(src, 0): 0}
    heap = [(0, src, 0)]                # (cost, city, flights used)
    while heap:
        cost, city, used = heapq.heappop(heap)
        if city == dst:
            return cost                 # first pop is the cheapest
        if cost > best[(city, used)] or used == k + 1:
            continue
        for nxt, price in graph[city]:
            state = (nxt, used + 1)
            if cost + price < best.get(state, float("inf")):
                best[state] = cost + price
                heapq.heappush(heap, (cost + price, nxt, used + 1))
    return -1
