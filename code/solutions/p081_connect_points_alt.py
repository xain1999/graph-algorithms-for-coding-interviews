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


def min_cost_connect_points_kruskal(points: list[list[int]]) -> int:
    """Kruskal on all n(n-1)/2 pairs: O(n^2 log n)."""
    n = len(points)
    edges = []
    for i in range(n):
        xi, yi = points[i]
        for j in range(i + 1, n):
            xj, yj = points[j]
            edges.append((abs(xi - xj) + abs(yi - yj), i, j))
    edges.sort()
    uf = UnionFind(n)
    total = 0
    joined = 0
    for d, i, j in edges:
        if joined == n - 1:
            break                       # the tree is complete
        if uf.union(i, j):
            total += d
            joined += 1
    return total
