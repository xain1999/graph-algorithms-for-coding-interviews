from collections import deque


def bfs_levels(graph: list[list[int]], start: int) -> list[list[int]]:
    """Nodes grouped by their distance (in edges) from start."""
    seen = {start}
    levels: list[list[int]] = []
    queue = deque([start])
    while queue:
        level = []
        for _ in range(len(queue)):     # exactly the current layer
            node = queue.popleft()
            level.append(node)
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    queue.append(nxt)
        levels.append(level)
    return levels
