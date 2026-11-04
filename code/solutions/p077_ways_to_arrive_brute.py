def count_paths_brute(n: int, roads: list[list[int]]) -> int:
    """List every simple route from 0 to n - 1 (exponential)."""
    graph: list[list[tuple[int, int]]] = [[] for _ in range(n)]
    for u, v, time in roads:
        graph[u].append((v, time))
        graph[v].append((u, time))
    best, count = float("inf"), 0
    stack = [(0, 0, 1)]                 # (node, time, visited mask)
    while stack:
        node, time, mask = stack.pop()
        if node == n - 1:
            if time < best:
                best, count = time, 1
            elif time == best:
                count += 1
            continue
        for nxt, t in graph[node]:
            if not mask >> nxt & 1:
                stack.append((nxt, time + t, mask | 1 << nxt))
    return count % (10**9 + 7)
