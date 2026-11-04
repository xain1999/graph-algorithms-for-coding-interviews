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


DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


def swim_in_water_uf(grid: list[list[int]]) -> int:
    """Flood cells in height order until the corners join."""
    n = len(grid)
    cells = sorted((grid[r][c], r, c)
                   for r in range(n) for c in range(n))
    uf = UnionFind(n * n)
    wet = [[False] * n for _ in range(n)]
    for h, r, c in cells:
        wet[r][c] = True
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if 0 <= nr < n and 0 <= nc < n and wet[nr][nc]:
                uf.union(r * n + c, nr * n + nc)
        if uf.find(0) == uf.find(n * n - 1):
            return h
    raise ValueError("unreachable: all cells are wet at the end")
