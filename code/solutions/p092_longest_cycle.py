def longest_cycle(edges: list[int]) -> int:
    """Length of the longest cycle, or -1 if there is no cycle."""
    n = len(edges)
    stamp = [0] * n             # 0 = never visited
    clock = 1
    best = -1
    for start in range(n):
        if stamp[start]:
            continue
        first = clock           # stamps >= first belong to this walk
        node = start
        while node != -1 and not stamp[node]:
            stamp[node] = clock
            clock += 1
            node = edges[node]
        # Back on a node of this walk: the walk closed a new cycle.
        if node != -1 and stamp[node] >= first:
            best = max(best, clock - stamp[node])
    return best
