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


def valid_tree(n: int, edges: list[list[int]]) -> bool:
    """True if the n nodes and the edges form exactly one tree."""
    if len(edges) != n - 1:
        return False                    # a tree has exactly n-1 edges
    uf = UnionFind(n)
    for u, v in edges:
        if not uf.union(u, v):
            return False                # already joined: a cycle
    return True                         # n-1 merges leave one set
