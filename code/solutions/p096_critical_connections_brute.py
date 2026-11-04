def critical_connections_brute(
        n: int, connections: list[list[int]]) -> list[list[int]]:
    """Remove each cable in turn and test if its ends still meet."""
    bridges: list[list[int]] = []
    for skip, (a, b) in enumerate(connections):
        graph: list[list[int]] = [[] for _ in range(n)]
        for i, (u, v) in enumerate(connections):
            if i != skip:
                graph[u].append(v)
                graph[v].append(u)
        seen = {a}
        stack = [a]
        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        if b not in seen:               # a and b fell apart
            bridges.append([a, b])
    return bridges
