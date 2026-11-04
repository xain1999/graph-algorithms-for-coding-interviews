from collections import deque


def bfs_order(graph: list[list[int]], start: int) -> list[int]:
    """Nodes reachable from start, in breadth-first order."""
    seen = {start}
    order: list[int] = []
    queue = deque([start])
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)           # mark when enqueued
                queue.append(nxt)
    return order
