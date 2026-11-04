def tree_diameter_arms(edges: list[list[int]]) -> int:
    """One pass: join the two longest downward arms at each node."""
    n = len(edges) + 1
    graph: list[list[int]] = [[] for _ in range(n)]
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)

    # Root at 0. The list grows while we read it (a BFS queue that is
    # never popped), so every parent comes before its children.
    parent = [-1] * n
    order = [0]
    for node in order:
        for nxt in graph[node]:
            if nxt != parent[node]:
                parent[nxt] = node
                order.append(nxt)

    down = [0] * n      # longest downward path from each node (edges)
    best = 0
    for node in reversed(order):        # children before parents
        p = parent[node]
        if p != -1:
            arm = down[node] + 1        # path from p through node
            best = max(best, down[p] + arm)
            down[p] = max(down[p], arm)
    return best
