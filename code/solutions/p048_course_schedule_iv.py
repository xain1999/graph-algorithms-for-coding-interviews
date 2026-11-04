from collections import deque


def check_if_prerequisite(n: int, prerequisites: list[list[int]],
                          queries: list[list[int]]) -> list[bool]:
    """For each query [u, v]: must course u come before course v?"""
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for before, after in prerequisites:     # edge before -> after
        graph[before].append(after)
        indegree[after] += 1

    # ancestors[v]: every course that must be taken before v
    ancestors: list[set[int]] = [set() for _ in range(n)]
    queue = deque(v for v in range(n) if indegree[v] == 0)
    while queue:
        node = queue.popleft()          # ancestors[node] is complete
        for nxt in graph[node]:
            ancestors[nxt] |= ancestors[node]
            ancestors[nxt].add(node)
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return [u in ancestors[v] for u, v in queries]
