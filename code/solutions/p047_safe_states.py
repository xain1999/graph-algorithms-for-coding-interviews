WHITE, GRAY, BLACK = 0, 1, 2    # unvisited, on path or unsafe, safe


def eventual_safe_nodes(graph: list[list[int]]) -> list[int]:
    """Sorted nodes from which every path ends at a terminal node."""
    n = len(graph)
    color = [WHITE] * n
    for start in range(n):
        if color[start] != WHITE:
            continue
        color[start] = GRAY
        stack = [(start, iter(graph[start]))]
        while stack:
            node, children = stack[-1]
            for nxt in children:
                if color[nxt] == GRAY:  # a cycle, or known unsafe
                    stack.clear()       # the whole path is unsafe
                    break
                if color[nxt] == WHITE:
                    color[nxt] = GRAY
                    stack.append((nxt, iter(graph[nxt])))
                    break
            else:                       # every child is safe
                stack.pop()
                color[node] = BLACK
    return [v for v in range(n) if color[v] == BLACK]
