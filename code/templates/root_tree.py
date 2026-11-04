from collections import deque


def root_tree(n: int, edges: list[list[int]],
              root: int = 0) -> tuple[list[int], list[int]]:
    """Parent of every node (-1 for the root) and a BFS order in
    which every parent comes before its children."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)
    parent = [-1] * n
    order = [root]
    seen = [False] * n
    seen[root] = True
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if not seen[nxt]:
                seen[nxt] = True
                parent[nxt] = node
                order.append(nxt)
                queue.append(nxt)
    return parent, order
