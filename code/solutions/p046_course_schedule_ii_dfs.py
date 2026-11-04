WHITE, GRAY, BLACK = 0, 1, 2    # unvisited, on the path, finished


def find_order_dfs(n: int,
                   prerequisites: list[list[int]]) -> list[int]:
    """Reverse DFS finishing order, or [] if there is a cycle."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for course, pre in prerequisites:
        graph[pre].append(course)

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
            else:                       # everything after it is done
                stack.pop()
                color[node] = BLACK
                finished.append(node)
    return finished[::-1]
