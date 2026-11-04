def kruskal(n: int, edges: list[list[int]]) -> int:
    """Total weight of a minimum spanning tree, or -1 if the
    graph is disconnected. edges holds [u, v, w]."""
    parent = list(range(n))
    size = [1] * n

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    total, used = 0, 0
    for u, v, w in sorted(edges, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru == rv:
            continue                    # would close a cycle
        if size[ru] < size[rv]:
            ru, rv = rv, ru
        parent[rv] = ru
        size[ru] += size[rv]
        total += w
        used += 1
        if used == n - 1:
            break
    return total if used == n - 1 else -1
