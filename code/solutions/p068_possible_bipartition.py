from collections import deque


def possible_bipartition(n: int, dislikes: list[list[int]]) -> bool:
    """Can people 1..n form two groups with no dislike inside?"""
    graph: list[list[int]] = [[] for _ in range(n + 1)]  # 0 unused
    for a, b in dislikes:
        graph[a].append(b)
        graph[b].append(a)

    group = [-1] * (n + 1)              # -1: no group yet
    for start in range(1, n + 1):       # labels start at 1
        if group[start] != -1:
            continue
        group[start] = 0
        queue = deque([start])
        while queue:
            person = queue.popleft()
            for other in graph[person]:
                if group[other] == -1:
                    group[other] = 1 - group[person]
                    queue.append(other)
                elif group[other] == group[person]:
                    return False
    return True
