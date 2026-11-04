from collections import deque


def bfs_layers(graph: list[list[int]], start: int) -> int:
    """Number of BFS layers from start, or -1 if an edge joins
    two nodes of the same layer (an odd cycle)."""
    dist = {start: 0}
    queue = deque([start])
    deepest = 0
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            if nxt not in dist:
                dist[nxt] = dist[node] + 1
                deepest = dist[nxt]     # BFS: never decreases
                queue.append(nxt)
            elif dist[nxt] == dist[node]:
                return -1               # same layer: odd cycle
    return deepest + 1


def max_groups(n: int, edges: list[list[int]]) -> int:
    """Most groups for nodes 1..n so that every edge joins
    consecutive groups, or -1 if that is impossible."""
    graph: list[list[int]] = [[] for _ in range(n + 1)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # Label each component by its smallest node (iterative DFS).
    comp = [0] * (n + 1)
    for start in range(1, n + 1):
        if comp[start]:
            continue
        comp[start] = start
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if not comp[nxt]:
                    comp[nxt] = start
                    stack.append(nxt)

    # Best number of layers per component, over every start.
    best = [0] * (n + 1)
    for start in range(1, n + 1):
        layers = bfs_layers(graph, start)
        if layers == -1:
            return -1
        c = comp[start]
        best[c] = max(best[c], layers)
    return sum(best)
