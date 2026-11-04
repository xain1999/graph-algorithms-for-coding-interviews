def has_cycle_recursive(n: int, edges: list[list[int]]) -> bool:
    """Recursive DFS with a parent; for graphs that are not deep."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    seen = [False] * n

    def visit(node: int, parent: int) -> bool:
        seen[node] = True
        for nxt in graph[node]:
            if nxt == parent:
                continue
            if seen[nxt] or visit(nxt, node):
                return True
        return False

    for start in range(n):
        if not seen[start] and visit(start, -1):
            return True
    return False
