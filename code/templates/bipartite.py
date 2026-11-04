from collections import deque


def two_color(graph: list[list[int]]) -> list[int] | None:
    """Colors 0/1 with every edge joining different colors,
    or None if the undirected graph is not bipartite."""
    color = [-1] * len(graph)
    for start in range(len(graph)):     # every component
        if color[start] != -1:
            continue
        color[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if color[nxt] == -1:
                    color[nxt] = 1 - color[node]    # the other side
                    queue.append(nxt)
                elif color[nxt] == color[node]:
                    return None                    # odd cycle
    return color
