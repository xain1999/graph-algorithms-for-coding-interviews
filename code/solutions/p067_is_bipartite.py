from collections import deque


def is_bipartite(graph: list[list[int]]) -> bool:
    """True if two colors can give every edge different ends."""
    color = [-1] * len(graph)           # -1: not colored yet
    for start in range(len(graph)):     # every component, not just 0
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if color[nxt] == -1:
                    color[nxt] = 1 - color[node]
                    queue.append(nxt)
                elif color[nxt] == color[node]:
                    return False        # edge inside one color
    return True
