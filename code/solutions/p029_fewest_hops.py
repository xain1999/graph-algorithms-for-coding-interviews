from collections import deque


def fewest_hops(n: int, edges: list[list[int]],
                source: int, target: int) -> int:
    """Fewest edges on a path from source to target, or -1."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)      # undirected: store both directions
        graph[v].append(u)

    if source == target:
        return 0
    dist = [-1] * n             # -1 = not discovered yet
    dist[source] = 0
    queue = deque([source])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if dist[nxt] == -1:
                dist[nxt] = dist[node] + 1  # mark on enqueue
                if nxt == target:
                    return dist[nxt]        # already final
                queue.append(nxt)
    return -1                   # target is in another component
