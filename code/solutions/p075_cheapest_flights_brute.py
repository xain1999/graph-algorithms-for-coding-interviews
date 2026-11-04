def find_cheapest_price_brute(n: int, flights: list[list[int]],
                              src: int, dst: int, k: int) -> int:
    """Try every route of at most k + 1 flights (exponential)."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b, price in flights:
        graph[a].append((b, price))
    best = -1
    stack = [(src, 0, 0)]               # (city, flights used, cost)
    while stack:
        city, used, cost = stack.pop()
        if city == dst:
            if best == -1 or cost < best:
                best = cost
            continue                    # going on only adds cost
        if used == k + 1:
            continue
        for nxt, price in graph[city]:
            stack.append((nxt, used + 1, cost + price))
    return best
