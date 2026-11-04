def wire_office(n: int, cables: list[list[int]]) -> int:
    """Cheapest total cost to connect all n computers, or -1."""
    parent = list(range(n))             # union-find, Chapter 7

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    total = used = 0
    for u, v, cost in sorted(cables, key=lambda e: e[2]):
        ru, rv = find(u), find(v)
        if ru == rv:
            continue                    # would close a cycle
        parent[ru] = rv                 # joins two groups: keep it
        total += cost
        used += 1
        if used == n - 1:               # the tree is complete
            break
    return total if used == n - 1 else -1
