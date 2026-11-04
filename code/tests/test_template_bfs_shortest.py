import random

from templates.bfs_shortest import bfs_distances


def test_small_graph_layers():
    # The graph drawn in the Chapter 5 opener.
    graph = {
        "S": ["A", "B", "C"], "A": ["S", "D"], "B": ["S", "D", "E"],
        "C": ["S", "F"], "D": ["A", "B", "G"], "E": ["B", "H"],
        "F": ["C", "H"], "G": ["D"], "H": ["E", "F"],
    }
    dist = bfs_distances(["S"], graph.__getitem__)
    assert dist == {"S": 0, "A": 1, "B": 1, "C": 1, "D": 2, "E": 2,
                    "F": 2, "G": 3, "H": 3}


def test_multi_source_on_grid():
    rows, cols = 3, 4

    def nbrs(cell):
        r, c = cell
        for nr, nc in ((r + 1, c), (r - 1, c), (r, c + 1), (r, c - 1)):
            if 0 <= nr < rows and 0 <= nc < cols:
                yield nr, nc

    dist = bfs_distances([(0, 0), (2, 3)], nbrs)
    for (r, c), d in dist.items():
        assert d == min(r + c, (2 - r) + (3 - c))


def test_matches_layer_by_layer_reference():
    rng = random.Random(5)
    for _ in range(300):
        n = rng.randint(1, 12)
        adj = {u: [v for v in range(n) if v != u and rng.random() < 0.25] for u in range(n)}
        got = bfs_distances([0], adj.__getitem__)
        # reference: explicit layer-by-layer expansion
        ref = {0: 0}
        seen = {0}
        level = 0
        layer = [0]
        while layer:
            level += 1
            nxt_layer = []
            for u in layer:
                for v in adj[u]:
                    if v not in seen:
                        seen.add(v)
                        ref[v] = level
                        nxt_layer.append(v)
            layer = nxt_layer
        assert got == ref
