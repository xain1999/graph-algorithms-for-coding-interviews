def has_cycle(n: int, edges: list[list[int]]) -> bool:
    """True if the undirected graph contains a cycle."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    seen = [False] * n
    for start in range(n):          # the graph may be disconnected
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, -1)]       # (node, node we came from)
        while stack:
            node, parent = stack.pop()
            for nxt in graph[node]:
                if nxt == parent:
                    continue        # the edge we arrived by
                if seen[nxt]:
                    return True     # a second way into nxt
                seen[nxt] = True
                stack.append((nxt, node))
    return False
