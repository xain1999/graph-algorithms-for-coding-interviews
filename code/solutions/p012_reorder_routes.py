def min_reorder(n: int, connections: list[list[int]]) -> int:
    """Roads to reverse so every city can drive to city 0."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for a, b in connections:            # road a -> b
        graph[a].append((b, 1))         # real road: leads away
        graph[b].append((a, 0))         # helper: already points in

    flips = 0
    seen = [False] * n
    seen[0] = True
    stack = [0]
    while stack:
        city = stack.pop()
        for nxt, cost in graph[city]:
            if not seen[nxt]:
                seen[nxt] = True
                flips += cost           # 1 if the road points outward
                stack.append(nxt)
    return flips
