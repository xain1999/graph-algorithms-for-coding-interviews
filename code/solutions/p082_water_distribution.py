def min_cost_to_supply_water(n: int, wells: list[int],
                             pipes: list[list[int]]) -> int:
    """Cheapest mix of wells and pipes that brings water to every
    house 1..n."""
    # Virtual node 0 is the water source: a well at house h is an
    # edge 0-h whose weight is the cost of digging that well.
    edges = [(cost, 0, house)
             for house, cost in enumerate(wells, start=1)]
    for a, b, cost in pipes:
        edges.append((cost, a, b))
    edges.sort()

    parent = list(range(n + 1))
    size = [1] * (n + 1)

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    total = used = 0
    for cost, a, b in edges:
        ra, rb = find(a), find(b)
        if ra == rb:
            continue                        # would close a cycle
        if size[ra] < size[rb]:
            ra, rb = rb, ra
        parent[rb] = ra
        size[ra] += size[rb]
        total += cost
        used += 1
        if used == n:                       # n + 1 nodes, n edges
            break
    return total
