from collections import deque


def minimum_time(n: int, relations: list[list[int]],
                 time: list[int]) -> int:
    """Months to finish all n courses with unlimited parallelism."""
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for before, after in relations:     # courses are numbered 1..n
        graph[before - 1].append(after - 1)
        indegree[after - 1] += 1

    start = [0] * n                     # latest finish of a prereq
    queue = deque(c for c in range(n) if indegree[c] == 0)
    total = 0
    while queue:
        course = queue.popleft()        # all prereqs are finished
        finish = start[course] + time[course]
        total = max(total, finish)
        for nxt in graph[course]:
            start[nxt] = max(start[nxt], finish)
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return total
