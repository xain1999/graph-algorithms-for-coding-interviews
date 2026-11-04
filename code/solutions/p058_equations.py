def equations_possible(equations: list[str]) -> bool:
    """True if letters can get values satisfying every equation."""
    parent = list(range(26))            # one node per letter

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]   # path halving
            x = parent[x]
        return x

    # Pass 1: every equality merges two groups.
    for eq in equations:
        if eq[1] == "=":
            a, b = ord(eq[0]) - 97, ord(eq[3]) - 97
            parent[find(a)] = find(b)

    # Pass 2: the groups are final; check every inequality.
    for eq in equations:
        if eq[1] == "!":
            a, b = ord(eq[0]) - 97, ord(eq[3]) - 97
            if find(a) == find(b):
                return False
    return True
