from collections import deque


def find_order(n: int, prerequisites: list[list[int]]) -> list[int]:
    """A valid order of all n courses, or [] if there is none."""
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for course, pre in prerequisites:   # pair [course, pre]
        graph[pre].append(course)       # edge pre -> course
        indegree[course] += 1

    queue = deque(c for c in range(n) if indegree[c] == 0)
    order: list[int] = []
    while queue:
        course = queue.popleft()
        order.append(course)            # all its prerequisites done
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return order if len(order) == n else []
