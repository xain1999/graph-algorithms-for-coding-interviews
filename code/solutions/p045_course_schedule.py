from collections import deque


def can_finish(n: int, prerequisites: list[list[int]]) -> bool:
    """True if all n courses can be taken: no prerequisite cycle."""
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for course, pre in prerequisites:   # pair [course, pre]
        graph[pre].append(course)       # edge pre -> course
        indegree[course] += 1

    queue = deque(c for c in range(n) if indegree[c] == 0)
    taken = 0
    while queue:
        course = queue.popleft()        # all its prerequisites done
        taken += 1
        for nxt in graph[course]:
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return taken == n                   # leftovers mean a cycle
