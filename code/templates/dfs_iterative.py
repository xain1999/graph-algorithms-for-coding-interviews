def dfs_iterative(graph: list[list[int]], start: int) -> list[int]:
    """Same order as dfs_recursive, with an explicit stack."""
    seen: set[int] = set()
    order: list[int] = []
    stack = [start]
    while stack:
        node = stack.pop()
        if node in seen:                # pushed twice: skip the copy
            continue
        seen.add(node)
        order.append(node)
        for nxt in reversed(graph[node]):   # so the first neighbor
            if nxt not in seen:             # is popped first
                stack.append(nxt)
    return order
