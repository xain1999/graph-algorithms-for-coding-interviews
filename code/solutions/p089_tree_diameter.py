from collections import deque


def tree_diameter(edges: list[list[int]]) -> int:
    """Number of edges on a longest path in the tree."""
    n = len(edges) + 1
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    def farthest(start: int) -> tuple[int, int]:
        """BFS from start; return a farthest node and its distance."""
        dist = [-1] * n
        dist[start] = 0
        queue = deque([start])
        node = start
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if dist[nxt] == -1:
                    dist[nxt] = dist[node] + 1
                    queue.append(nxt)
        return node, dist[node]     # the last node popped is farthest

    end, _ = farthest(0)            # pass 1: one end of a diameter
    _, length = farthest(end)       # pass 2: the other end
    return length
