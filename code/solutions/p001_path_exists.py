def valid_path(n: int, edges: list[list[int]],
               source: int, destination: int) -> bool:
    """True if destination can be reached from source."""
    # Edge list -> adjacency list: graph[u] lists u's neighbors.
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)      # undirected: store both directions
        graph[v].append(u)

    seen = {source}
    stack = [source]
    while stack:
        node = stack.pop()      # last in, first out: go deep
        if node == destination:
            return True
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)   # mark when pushed, not when popped
                stack.append(nxt)
    return False
