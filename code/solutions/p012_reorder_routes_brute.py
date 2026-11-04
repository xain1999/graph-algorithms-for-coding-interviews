from collections import deque


def min_reorder_brute(n: int, connections: list[list[int]]) -> int:
    """Flip one wrong-way road at a time until all reach city 0."""
    roads = [(a, b) for a, b in connections]    # a copy we may flip
    flips = 0
    while True:
        # Which cities can drive to 0? BFS backwards from 0.
        into: list[list[int]] = [[] for _ in range(n)]
        for a, b in roads:
            into[b].append(a)
        ok = [False] * n
        ok[0] = True
        queue = deque([0])
        while queue:
            city = queue.popleft()
            for prev in into[city]:
                if not ok[prev]:
                    ok[prev] = True
                    queue.append(prev)
        if all(ok):
            return flips
        # A road from a good city to a stuck one must be reversed.
        for i, (a, b) in enumerate(roads):
            if ok[a] and not ok[b]:
                roads[i] = (b, a)
                flips += 1
                break
