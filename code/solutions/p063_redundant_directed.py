class UnionFind:
    """Disjoint sets over 0..n-1 with path halving and union by
    size: each operation takes nearly constant time."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))
        self.size = [1] * n

    def find(self, x: int) -> int:
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # halve
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> bool:
        """Merge the sets of a and b; False if already together."""
        ra, rb = self.find(a), self.find(b)
        if ra == rb:
            return False
        if self.size[ra] < self.size[rb]:
            ra, rb = rb, ra             # hang the smaller tree
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def find_redundant_directed(edges: list[list[int]]) -> list[int]:
    """Edge whose removal leaves a rooted tree (latest if tied)."""
    n = len(edges)
    parent = [0] * (n + 1)              # 0: no parent seen yet
    first: list[int] | None = None      # the two edges that enter
    second: list[int] | None = None     # the same node, in order
    for u, v in edges:
        if parent[v]:
            first, second = [parent[v], v], [u, v]
        else:
            parent[v] = u

    uf = UnionFind(n + 1)
    for u, v in edges:
        if [u, v] == second:
            continue                    # try life without it
        if not uf.union(u, v):          # [u, v] closes a cycle
            return first if first else [u, v]
    assert second is not None           # no cycle: a double parent
    return second
