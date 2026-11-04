from collections import deque


def zero_one_bfs(graph: list[list[tuple[int, int]]],
                 source: int) -> list[float]:
    """Shortest paths when every weight is 0 or 1, in O(V + E)."""
    dist = [float("inf")] * len(graph)
    dist[source] = 0
    dq = deque([source])
    while dq:
        node = dq.popleft()
        for nxt, w in graph[node]:
            if dist[node] + w < dist[nxt]:
                dist[nxt] = dist[node] + w
                if w == 0:
                    dq.appendleft(nxt)  # same distance: front
                else:
                    dq.append(nxt)      # one more: back
    return dist
