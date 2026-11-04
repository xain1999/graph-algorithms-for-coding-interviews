from collections import deque


def valid_path_bfs(n: int, edges: list[list[int]],
                   source: int, destination: int) -> bool:
    """Same search with a queue: explore the graph ring by ring."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    seen = {source}
    queue = deque([source])
    while queue:
        node = queue.popleft()  # first in, first out: go wide
        if node == destination:
            return True
        for nxt in graph[node]:
            if nxt not in seen:
                seen.add(nxt)
                queue.append(nxt)
    return False
