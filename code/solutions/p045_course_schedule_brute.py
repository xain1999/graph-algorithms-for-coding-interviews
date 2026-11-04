def can_finish_brute(n: int, prerequisites: list[list[int]]) -> bool:
    """For every course, search for a way back to itself."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for course, pre in prerequisites:
        graph[pre].append(course)       # edge pre -> course

    for start in range(n):
        seen = [False] * n
        stack = list(graph[start])
        while stack:
            node = stack.pop()
            if node == start:
                return False            # start lies on a cycle
            if not seen[node]:
                seen[node] = True
                stack.extend(graph[node])
    return True
