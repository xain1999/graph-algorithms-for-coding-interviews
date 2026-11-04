from itertools import combinations


def critical_edges_brute(n: int,
                         edges: list[list[int]]) -> list[list[int]]:
    """List every spanning tree, keep the lightest ones, and count
    in how many of them each edge appears."""
    trees: list[tuple[int, ...]] = []
    best = None
    for subset in combinations(range(len(edges)), n - 1):
        parent = list(range(n))

        def find(x: int) -> int:
            while parent[x] != x:
                x = parent[x]
            return x

        is_tree = True
        for i in subset:
            ra, rb = find(edges[i][0]), find(edges[i][1])
            if ra == rb:
                is_tree = False         # a cycle: not a tree
                break
            parent[ra] = rb
        if not is_tree:
            continue
        weight = sum(edges[i][2] for i in subset)
        if best is None or weight < best:
            best, trees = weight, []
        if weight == best:
            trees.append(subset)
    critical, pseudo = [], []
    for i in range(len(edges)):
        count = sum(1 for t in trees if i in t)
        if count == len(trees):
            critical.append(i)
        elif count > 0:
            pseudo.append(i)
    return [critical, pseudo]
