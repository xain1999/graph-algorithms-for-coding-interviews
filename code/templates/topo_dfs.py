WHITE, GRAY, BLACK = 0, 1, 2    # unvisited, on the path, finished


def topo_order_dfs(n: int, edges: list[list[int]]) -> list[int]:
    """Topological order by DFS finishing times, or [] on a cycle."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    color = [WHITE] * n
    finished: list[int] = []
    for start in range(n):
        if color[start] != WHITE:
            continue
        color[start] = GRAY
        stack = [(start, iter(graph[start]))]
        while stack:
            node, children = stack[-1]
            for nxt in children:
                if color[nxt] == GRAY:
                    return []           # back edge: a cycle
                if color[nxt] == WHITE:
                    color[nxt] = GRAY
                    stack.append((nxt, iter(graph[nxt])))
                    break
            else:                       # no unvisited child is left
                stack.pop()
                color[node] = BLACK
                finished.append(node)
    return finished[::-1]               # reverse finishing order
