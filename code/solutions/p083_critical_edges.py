def mst_weight(n: int, edges: list[list[int]], order: list[int],
               skip: int = -1, force: int = -1) -> float:
    """Kruskal over `order`, leaving out edge `skip` and taking edge
    `force` first; infinity if the edges cannot connect all n."""
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    total = used = 0
    first = [force] if force >= 0 else []
    for i in first + order:
        if i == skip:
            continue
        a, b, w = edges[i]
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            total += w
            used += 1
    return total if used == n - 1 else float("inf")


def critical_edges(n: int,
                   edges: list[list[int]]) -> list[list[int]]:
    """[critical edge indices, pseudo-critical edge indices]."""
    order = sorted(range(len(edges)), key=lambda i: edges[i][2])
    best = mst_weight(n, edges, order)
    critical, pseudo = [], []
    for i in range(len(edges)):
        if mst_weight(n, edges, order, skip=i) > best:
            critical.append(i)          # no MST can do without it
        elif mst_weight(n, edges, order, force=i) == best:
            pseudo.append(i)            # some MST uses it, not all
    return [critical, pseudo]
