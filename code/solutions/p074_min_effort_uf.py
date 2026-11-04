class UnionFind:
    """Disjoint sets over 0..n-1, path halving + union by size."""

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
            ra, rb = rb, ra
        self.parent[rb] = ra
        self.size[ra] += self.size[rb]
        return True


def minimum_effort_uf(heights: list[list[int]]) -> int:
    """Kruskal-style: add steps from smallest until corners join."""
    rows, cols = len(heights), len(heights[0])
    steps = []                          # (difference, cell, cell)
    for r in range(rows):
        for c in range(cols):
            cell = r * cols + c
            if r + 1 < rows:
                diff = abs(heights[r + 1][c] - heights[r][c])
                steps.append((diff, cell, cell + cols))
            if c + 1 < cols:
                diff = abs(heights[r][c + 1] - heights[r][c])
                steps.append((diff, cell, cell + 1))
    steps.sort()
    uf = UnionFind(rows * cols)
    last = rows * cols - 1
    for diff, a, b in steps:
        uf.union(a, b)
        if uf.find(0) == uf.find(last):
            return diff                 # largest step used so far
    return 0                            # a single cell, no steps
