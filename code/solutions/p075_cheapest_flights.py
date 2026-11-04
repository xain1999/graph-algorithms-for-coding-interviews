def find_cheapest_price(n: int, flights: list[list[int]], src: int,
                        dst: int, k: int) -> int:
    """Cheapest src -> dst price with at most k stops, or -1."""
    INF = float("inf")
    cost = [INF] * n                    # cheapest with <= r flights
    cost[src] = 0
    for _ in range(k + 1):              # k stops = k + 1 flights
        new_cost = cost[:]              # read old, write new
        for a, b, price in flights:
            if cost[a] + price < new_cost[b]:
                new_cost[b] = cost[a] + price
        cost = new_cost
    return -1 if cost[dst] == INF else int(cost[dst])
