from collections import deque


def min_reorder_sets(n: int, connections: list[list[int]]) -> int:
    """BFS on the undirected tree; look roads up in a set."""
    roads = {(a, b) for a, b in connections}
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in connections:
        graph[a].append(b)
        graph[b].append(a)

    flips = 0
    seen = [False] * n
    seen[0] = True
    queue = deque([0])
    while queue:
        city = queue.popleft()
        for nxt in graph[city]:
            if not seen[nxt]:
                seen[nxt] = True
                if (city, nxt) in roads:    # points away from 0
                    flips += 1
                queue.append(nxt)
    return flips
