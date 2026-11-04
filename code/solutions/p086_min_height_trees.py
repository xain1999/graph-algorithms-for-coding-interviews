def find_min_height_trees(n: int,
                          edges: list[list[int]]) -> list[int]:
    """Roots of minimum height: peel leaves until 1 or 2 remain."""
    if n <= 2:
        return list(range(n))
    graph: list[list[int]] = [[] for _ in range(n)]
    degree = [0] * n
    for a, b in edges:
        graph[a].append(b)
        graph[b].append(a)
        degree[a] += 1
        degree[b] += 1

    leaves = [v for v in range(n) if degree[v] == 1]
    remaining = n
    while remaining > 2:
        remaining -= len(leaves)
        next_leaves = []
        for leaf in leaves:
            for nxt in graph[leaf]:
                degree[nxt] -= 1
                if degree[nxt] == 1:    # nxt just became a leaf
                    next_leaves.append(nxt)
        leaves = next_leaves
    return sorted(leaves)
