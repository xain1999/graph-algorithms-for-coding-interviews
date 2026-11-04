from collections import deque


def largest_path_value_by_color(colors: str,
                                edges: list[list[int]]) -> int:
    """One longest-path pass per color, along one Kahn order."""
    n = len(colors)
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for u, v in edges:
        graph[u].append(v)
        indegree[v] += 1

    queue = deque(v for v in range(n) if indegree[v] == 0)
    order: list[int] = []
    while queue:
        node = queue.popleft()
        order.append(node)
        for nxt in graph[node]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    if len(order) < n:
        return -1                       # a cycle

    best = 0
    for color in set(colors):           # at most 26 passes
        # most nodes of this color on a path ending at v
        here = [0] * n
        for node in order:
            here[node] += colors[node] == color
            best = max(best, here[node])
            for nxt in graph[node]:
                here[nxt] = max(here[nxt], here[node])
    return best
