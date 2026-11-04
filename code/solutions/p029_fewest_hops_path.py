from collections import deque


def shortest_route(n: int, edges: list[list[int]],
                   source: int, target: int) -> list[int]:
    """Nodes of one fewest-edge path, source first ([] if none)."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    parent: dict[int, int | None] = {source: None}
    queue = deque([source])
    while queue and target not in parent:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in parent:
                parent[nxt] = node      # who discovered nxt
                queue.append(nxt)

    if target not in parent:
        return []
    route: list[int] = []
    step: int | None = target
    while step is not None:             # walk back to the source
        route.append(step)
        step = parent[step]
    return route[::-1]
