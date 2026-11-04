DIRECTIONS = ((1, 0), (-1, 0), (0, 1), (0, -1))


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


def islands_after_each(rows: int, cols: int,
                       added: list[list[int]]) -> list[int]:
    """Number of islands after each cell of `added` becomes land."""
    uf = UnionFind(rows * cols)         # cell (r, c) is r * cols + c
    land = [False] * (rows * cols)      # only land cells are "active"
    islands = 0
    counts = []
    for r, c in added:
        cell = r * cols + c
        if not land[cell]:              # a repeat changes nothing
            land[cell] = True
            islands += 1                # a new island of one cell
            for dr, dc in DIRECTIONS:
                nr, nc = r + dr, c + dc
                if (0 <= nr < rows and 0 <= nc < cols
                        and land[nr * cols + nc]
                        and uf.union(cell, nr * cols + nc)):
                    islands -= 1        # two islands became one
        counts.append(islands)
    return counts
