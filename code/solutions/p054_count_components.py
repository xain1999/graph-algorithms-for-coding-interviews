class UnionFind:
    """Disjoint sets over 0..n-1 with path halving and union by
    size: each operation takes nearly constant time."""

    def __init__(self, n: int) -> None:
        self.parent = list(range(n))    # every node is its own root
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


def count_components(n: int, edges: list[list[int]]) -> int:
    """Number of connected components: n minus successful unions."""
    uf = UnionFind(n)
    components = n                      # every node starts alone
    for u, v in edges:
        if uf.union(u, v):
            components -= 1             # two components became one
    return components
