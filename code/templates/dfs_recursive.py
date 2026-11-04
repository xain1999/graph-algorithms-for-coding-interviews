def dfs_recursive(graph: list[list[int]], start: int) -> list[int]:
    """Nodes reachable from start, in depth-first order."""
    seen = {start}
    order: list[int] = []

    def visit(node: int) -> None:
        order.append(node)
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                visit(nxt)              # go deep before going wide

    visit(start)
    return order
