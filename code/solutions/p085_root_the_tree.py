from collections import deque


def root_tree(n: int, edges: list[list[int]], root: int) -> list[int]:
    """Parent of every node when the tree hangs from root."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    parent = [-1] * n
    queue = deque([root])
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt != parent[node]:     # all others are children
                parent[nxt] = node
                queue.append(nxt)
    return parent
