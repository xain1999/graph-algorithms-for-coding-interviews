from collections import deque
from itertools import permutations


def shortest_path_length_brute(graph: list[list[int]]) -> int:
    """Try every visiting order, using BFS distances between nodes."""
    n = len(graph)
    dist = []                           # dist[a][b], one BFS per node
    for source in range(n):
        d = [-1] * n
        d[source] = 0
        queue = deque([source])
        while queue:
            node = queue.popleft()
            for nxt in graph[node]:
                if d[nxt] == -1:
                    d[nxt] = d[node] + 1
                    queue.append(nxt)
        dist.append(d)

    best = -1
    for order in permutations(range(n)):
        legs = [dist[a][b] for a, b in zip(order, order[1:])]
        if -1 in legs:
            continue                    # some node is unreachable
        if best == -1 or sum(legs) < best:
            best = sum(legs)
    return best
