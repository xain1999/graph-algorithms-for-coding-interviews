import random

import networkx as nx

from templates.grid_flood import flood

# The grid of the Chapter 4 opener figure (1 = land, 0 = water).
OPENER = [
    [1, 1, 0, 0, 0, 1],
    [1, 0, 0, 1, 0, 0],
    [0, 0, 1, 1, 1, 0],
    [0, 0, 0, 1, 0, 0],
    [1, 0, 0, 0, 0, 1],
]


def test_opener_regions():
    seen = [[False] * 6 for _ in range(5)]
    assert flood(OPENER, 2, 2, seen) == 5
    assert flood(OPENER, 0, 0, seen) == 3
    assert not seen[0][5]


def test_matches_networkx_components():
    rng = random.Random(4)
    for _ in range(300):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        grid = [[rng.randint(0, 1) for _ in range(cols)]
                for _ in range(rows)]
        g = nx.grid_2d_graph(rows, cols)
        g.remove_edges_from([(a, b) for a, b in list(g.edges)
                             if grid[a[0]][a[1]] != grid[b[0]][b[1]]])
        r, c = rng.randrange(rows), rng.randrange(cols)
        seen = [[False] * cols for _ in range(rows)]
        assert flood(grid, r, c, seen) == len(
            nx.node_connected_component(g, (r, c)))


def test_large_grid_no_recursion_limit():
    grid = [[1] * 400 for _ in range(400)]
    seen = [[False] * 400 for _ in range(400)]
    assert flood(grid, 0, 0, seen) == 160_000
