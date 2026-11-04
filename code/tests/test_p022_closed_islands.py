import random

import networkx as nx
import pytest

from solutions.p022_closed_islands import closed_island
from solutions.p022_closed_islands_flag import closed_island_flag

SOLVERS = [closed_island, closed_island_flag]


def grid(*rows):
    return [[int(ch) for ch in row] for row in rows]


EXAMPLE_1 = grid("0011000", "0100110", "0110010", "0001000",
                 "1100011", "0001001")


def nx_closed(g):
    rows, cols = len(g), len(g[0])
    graph = nx.Graph()
    for r in range(rows):
        for c in range(cols):
            if g[r][c] == 1:
                graph.add_node((r, c))
                if r + 1 < rows and g[r + 1][c] == 1:
                    graph.add_edge((r, c), (r + 1, c))
                if c + 1 < cols and g[r][c + 1] == 1:
                    graph.add_edge((r, c), (r, c + 1))
    return sum(
        1 for comp in nx.connected_components(graph)
        if all(0 < r < rows - 1 and 0 < c < cols - 1
               for r, c in comp))


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "g, expected",
    [
        (EXAMPLE_1, 3),                                    # example 1
        (grid("00000", "01110", "01010", "01110", "00000"),
         1),                                               # example 2
        (grid("1111", "1001", "1111"), 0),                 # example 3
        (grid("0"), 0),
        (grid("1"), 0),
        (grid("010"), 0),                                  # one row
        (grid("000", "010", "000"), 1),
        (grid("0000", "0110", "0110", "0000"), 1),
        (grid("00000", "01010", "00000"), 2),              # diagonal
        (grid("00000", "01100", "00110", "00010"), 0),        # tail
    ],
)
def test_examples(solve, g, expected):
    assert solve(g) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    g = [row[:] for row in EXAMPLE_1]
    solve(g)
    assert g == EXAMPLE_1


def test_random_grids_agree():
    rng = random.Random(1254)
    for _ in range(1000):
        rows, cols = rng.randint(1, 9), rng.randint(1, 9)
        p = rng.random()
        g = [[int(rng.random() < p) for _ in range(cols)]
             for _ in range(rows)]
        want = nx_closed(g)
        for solve in SOLVERS:
            assert solve(g) == want


def test_large_snake_is_fast():
    # one snake-shaped island filling the interior of a 250 x 250 map
    n = 250
    g = [[0] * n for _ in range(n)]
    for r in range(1, n - 1, 2):
        g[r] = [0] + [1] * (n - 2) + [0]
        if r + 1 < n - 1:
            g[r + 1][n - 2 if r % 4 == 1 else 1] = 1
    for solve in SOLVERS:
        assert solve(g) == 1


def test_large_checkerboard():
    n = 250
    g = [[(r + c) % 2 for c in range(n)] for r in range(n)]
    want = sum(1 for r in range(1, n - 1) for c in range(1, n - 1)
               if (r + c) % 2)
    assert closed_island(g) == want
