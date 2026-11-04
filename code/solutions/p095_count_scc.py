def count_scc(n: int, edges: list[list[int]]) -> int:
    """Number of strongly connected components (Kosaraju)."""
    graph: list[list[int]] = [[] for _ in range(n)]
    reverse: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)
        reverse[v].append(u)

    # Pass 1: iterative DFS, recording nodes as they finish.
    seen = [False] * n
    finished: list[int] = []
    for start in range(n):
        if seen[start]:
            continue
        seen[start] = True
        stack = [(start, iter(graph[start]))]
        while stack:
            node, children = stack[-1]
            for nxt in children:
                if not seen[nxt]:
                    seen[nxt] = True
                    stack.append((nxt, iter(graph[nxt])))
                    break
            else:                       # all children done
                stack.pop()
                finished.append(node)

    # Pass 2: reversed graph, latest finisher first.
    assigned = [False] * n
    count = 0
    for start in reversed(finished):
        if assigned[start]:
            continue
        count += 1                      # a new component
        assigned[start] = True
        stack2 = [start]
        while stack2:
            node = stack2.pop()
            for prev in reverse[node]:
                if not assigned[prev]:
                    assigned[prev] = True
                    stack2.append(prev)
    return count
