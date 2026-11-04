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


def limited_paths(n: int, edges: list[list[int]],
                  queries: list[list[int]]) -> list[bool]:
    """For each [u, v, limit]: is there a u-v path whose every
    edge is shorter than limit?"""
    by_length = sorted(edges, key=lambda e: e[2])
    # Answer queries by increasing limit, remembering their index.
    order = sorted(range(len(queries)),
                   key=lambda i: queries[i][2])
    uf = UnionFind(n)
    answers = [False] * len(queries)
    k = 0                               # edges added so far
    for i in order:
        u, v, limit = queries[i]
        while k < len(by_length) and by_length[k][2] < limit:
            a, b, _ = by_length[k]
            uf.union(a, b)
            k += 1
        answers[i] = uf.find(u) == uf.find(v)
    return answers
