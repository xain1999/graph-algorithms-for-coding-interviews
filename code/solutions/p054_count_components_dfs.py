def count_components_dfs(n: int, edges: list[list[int]]) -> int:
    """Chapter 2's components template on an adjacency list."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        graph[v].append(u)

    seen = [False] * n
    count = 0
    for start in range(n):
        if seen[start]:
            continue
        count += 1                      # a new, untouched component
        seen[start] = True
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append(nxt)
    return count
