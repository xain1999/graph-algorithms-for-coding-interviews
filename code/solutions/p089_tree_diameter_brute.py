from collections import deque


def tree_diameter_brute(edges: list[list[int]]) -> int:
    """Run a BFS from every node; keep the largest distance seen."""
    n = len(edges) + 1
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    best = 0
    for start in range(n):
        dist = [-1] * n
        dist[start] = 0
        queue = deque([start])
        while queue:
            node = queue.popleft()
            best = max(best, dist[node])
            for nxt in graph[node]:
                if dist[nxt] == -1:
                    dist[nxt] = dist[node] + 1
                    queue.append(nxt)
    return best
