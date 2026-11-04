class UnionFind:
    """Disjoint sets over integer keys, each created on first use."""

    def __init__(self) -> None:
        self.parent: dict[int, int] = {}
        self.size: dict[int, int] = {}
        self.count = 0                  # number of separate sets

    def find(self, x: int) -> int:
        if x not in self.parent:        # a new key: a set of its own
            self.parent[x], self.size[x] = x, 1
            self.count += 1
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]  # halve
            x = self.parent[x]
        return x

    def union(self, a: int, b: int) -> None:
        ra, rb = self.find(a), self.find(b)
        if ra != rb:
            if self.size[ra] < self.size[rb]:
                ra, rb = rb, ra         # hang the smaller tree
            self.parent[rb] = ra
            self.size[ra] += self.size[rb]
            self.count -= 1


def remove_stones(stones: list[list[int]]) -> int:
    """Most stones removable: the stones minus the linked groups."""
    uf = UnionFind()
    for row, col in stones:
        uf.union(row, ~col)     # ~col == -col - 1: a column key
    return len(stones) - uf.count
