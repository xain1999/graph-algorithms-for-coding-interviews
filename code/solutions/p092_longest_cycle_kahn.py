from collections import deque


def longest_cycle_kahn(edges: list[int]) -> int:
    """Peel off nodes of in-degree 0; only cycles remain."""
    n = len(edges)
    indegree = [0] * n
    for target in edges:
        if target != -1:
            indegree[target] += 1
    queue = deque(v for v in range(n) if indegree[v] == 0)
    removed = [False] * n
    while queue:
        node = queue.popleft()
        removed[node] = True
        target = edges[node]
        if target != -1:
            indegree[target] -= 1
            if indegree[target] == 0:
                queue.append(target)

    best = -1
    for start in range(n):              # every survivor is on a cycle
        if removed[start]:
            continue
        length, node = 0, start
        while not removed[node]:
            removed[node] = True        # measure each cycle once
            length += 1
            node = edges[node]
        best = max(best, length)
    return best
