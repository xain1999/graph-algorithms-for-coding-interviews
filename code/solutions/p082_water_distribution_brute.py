def min_cost_to_supply_water_brute(n: int, wells: list[int],
                                   pipes: list[list[int]]) -> int:
    """Try every set of wells and every set of pipes: O(2^(n+m))."""
    m = len(pipes)
    best = None
    for mask in range(1 << (n + m)):
        # Bits 0..n-1 choose wells, bits n..n+m-1 choose pipes.
        cost = 0
        graph: list[list[int]] = [[] for _ in range(n + 1)]
        has_water = [False] * (n + 1)
        for h in range(1, n + 1):
            if mask >> (h - 1) & 1:
                cost += wells[h - 1]
                has_water[h] = True
        for j, (a, b, c) in enumerate(pipes):
            if mask >> (n + j) & 1:
                cost += c
                graph[a].append(b)
                graph[b].append(a)
        # Water flows from every well along the chosen pipes.
        stack = [h for h in range(1, n + 1) if has_water[h]]
        while stack:
            u = stack.pop()
            for v in graph[u]:
                if not has_water[v]:
                    has_water[v] = True
                    stack.append(v)
        if all(has_water[1:]) and (best is None or cost < best):
            best = cost
    assert best is not None
    return best
