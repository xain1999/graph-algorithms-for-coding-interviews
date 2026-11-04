from collections import deque


def check_if_prerequisite_bits(n: int,
                               prerequisites: list[list[int]],
                               queries: list[list[int]]
                               ) -> list[bool]:
    """The same pass, with one integer bitmask per course."""
    graph: list[list[int]] = [[] for _ in range(n)]
    indegree = [0] * n
    for before, after in prerequisites:
        graph[before].append(after)
        indegree[after] += 1

    # bit u of mask[v] is 1 when course u must come before v
    mask = [0] * n
    queue = deque(v for v in range(n) if indegree[v] == 0)
    while queue:
        node = queue.popleft()
        for nxt in graph[node]:
            mask[nxt] |= mask[node] | (1 << node)
            indegree[nxt] -= 1
            if indegree[nxt] == 0:
                queue.append(nxt)
    return [(mask[v] >> u) & 1 == 1 for u, v in queries]
