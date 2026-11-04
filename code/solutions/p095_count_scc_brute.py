def count_scc_brute(n: int, edges: list[list[int]]) -> int:
    """Group nodes that reach each other, via all-pairs search."""
    graph: list[list[int]] = [[] for _ in range(n)]
    for u, v in edges:
        graph[u].append(v)

    reach: list[set[int]] = []
    for start in range(n):          # one DFS per node
        seen = {start}
        stack = [start]
        while stack:
            node = stack.pop()
            for nxt in graph[node]:
                if nxt not in seen:
                    seen.add(nxt)
                    stack.append(nxt)
        reach.append(seen)

    placed = [False] * n
    count = 0
    for u in range(n):
        if not placed[u]:
            count += 1
            for v in reach[u]:      # u's mutual partners
                if u in reach[v]:
                    placed[v] = True
    return count
