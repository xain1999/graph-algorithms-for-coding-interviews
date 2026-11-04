def valid_tree_dfs(n: int, edges: list[list[int]]) -> bool:
    """n-1 edges and a DFS from node 0 that reaches every node."""
    if len(edges) != n - 1:
        return False
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    seen = [False] * n
    seen[0] = True
    stack = [0]
    reached = 1
    while stack:
        node = stack.pop()
        for nxt in graph[node]:
            if not seen[nxt]:
                seen[nxt] = True
                reached += 1
                stack.append(nxt)
    return reached == n                 # connected with n-1 edges
