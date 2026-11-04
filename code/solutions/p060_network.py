def make_connected(n: int, cables: list[list[int]]) -> int:
    """Fewest cable moves that connect all n computers, or -1."""
    if len(cables) < n - 1:
        return -1                       # too few cables in total
    parent = list(range(n))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    groups = n
    for a, b in cables:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[ra] = rb
            groups -= 1                 # two networks became one
    return groups - 1
