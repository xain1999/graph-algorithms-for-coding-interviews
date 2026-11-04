def find_redundant_connection_brute(
        edges: list[list[int]]) -> list[int]:
    """Before adding each edge, search for a path between its ends."""
    n = len(edges)
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for u, v in edges:
        seen = {u}                      # DFS over earlier edges
        stack = [u]
        while stack and v not in seen:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        if v in seen:
            return [u, v]               # a second route from u to v
        graph[u].append(v)
        graph[v].append(u)
    return []                           # not reached for valid input
