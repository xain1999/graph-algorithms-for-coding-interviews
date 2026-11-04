def euler_path(edges: list[list[int]], start: int) -> list[int]:
    """Nodes of a path using every directed edge exactly once,
    starting at `start` (the caller checks that one exists)."""
    graph: dict[int, list[int]] = {}
    for u, v in edges:
        graph.setdefault(u, []).append(v)
    stack = [start]
    path: list[int] = []
    while stack:
        node = stack[-1]
        if graph.get(node):
            stack.append(graph[node].pop())     # walk an unused edge
        else:
            path.append(stack.pop())            # stuck: emit node
    return path[::-1]
