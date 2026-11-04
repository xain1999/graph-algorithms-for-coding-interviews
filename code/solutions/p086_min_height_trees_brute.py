from collections import deque


def find_min_height_trees_brute(n: int,
                                edges: list[list[int]]) -> list[int]:
    """BFS from every node; keep the nodes of smallest height."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    def height(root: int) -> int:
        dist = [-1] * n
        dist[root] = 0
        queue = deque([root])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if dist[nxt] == -1:
                    dist[nxt] = dist[node] + 1
                    queue.append(nxt)
        return max(dist)

    heights = [height(v) for v in range(n)]
    best = min(heights)
    return [v for v in range(n) if heights[v] == best]
