from collections import defaultdict, deque


def num_buses_brute(routes: list[list[int]], source: int,
                    target: int) -> int:
    """BFS over stops; one ride joins every pair on the same route."""
    graph = defaultdict(set)
    for stops in routes:
        for a in stops:                 # quadratic in route length
            for b in stops:
                if a != b:
                    graph[a].add(b)

    dist = {source: 0}
    queue = deque([source])
    while queue:
        stop = queue.popleft()
        if stop == target:
            return dist[stop]
        for nxt in graph[stop]:
            if nxt not in dist:
                dist[nxt] = dist[stop] + 1
                queue.append(nxt)
    return -1
