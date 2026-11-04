WHITE, GRAY, BLACK = 0, 1, 2    # unvisited, on the path, finished


def can_finish_dfs(n: int, prerequisites: list[list[int]]) -> bool:
    """Three-color DFS: reaching a GRAY course closes a cycle."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for course, pre in prerequisites:
        graph[pre].append(course)

    color = [WHITE] * n
    for start in range(n):
        if color[start] != WHITE:
            continue
        color[start] = GRAY
        stack = [(start, iter(graph[start]))]
        while stack:
            node, children = stack[-1]
            for nxt in children:
                if color[nxt] == GRAY:
                    return False        # back edge: a cycle
                if color[nxt] == WHITE:
                    color[nxt] = GRAY
                    stack.append((nxt, iter(graph[nxt])))
                    break
            else:                       # every child is finished
                stack.pop()
                color[node] = BLACK
    return True
