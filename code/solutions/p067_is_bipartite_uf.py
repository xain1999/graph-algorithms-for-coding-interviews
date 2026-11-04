def is_bipartite_uf(graph: list[list[int]]) -> bool:
    """Union-find: all neighbors of a node must share one side."""
    n = len(graph)
    parent = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    # Pass 1: the neighbors of each node go on the same side.
    for node in range(n):
        for nxt in graph[node]:
            ra, rb = find(graph[node][0]), find(nxt)
            if ra != rb:                    # union by size
                if size[ra] < size[rb]:
                    ra, rb = rb, ra
                parent[rb] = ra
                size[ra] += size[rb]
    # Pass 2: an edge inside one set means a forced clash.
    for node in range(n):
        for nxt in graph[node]:
            if find(node) == find(nxt):
                return False
    return True
