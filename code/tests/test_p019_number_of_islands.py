import random
import time

import networkx as nx
import pytest

from solutions.p019_number_of_islands import num_islands
from solutions.p019_number_of_islands_brute import num_islands_brute
from solutions.p019_number_of_islands_uf import num_islands_union_find

SOLVERS = [num_islands, num_islands_brute, num_islands_union_find]
FAST = [num_islands, num_islands_union_find]

EXAMPLE_1 = [
    [1, 1, 0, 0, 1, 1],
    [0, 1, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0],
    [1, 0, 1, 1, 0, 1],
    [1, 0, 0, 1, 0, 1],
]
EXAMPLE_2 = [
    [1, 0, 1, 0],
    [0, 1, 0, 1],
    [1, 0, 1, 0],
]
EXAMPLE_3 = [
    [1, 1, 1, 1, 1],
    [1, 0, 0, 0, 1],
    [1, 0, 1, 0, 1],
    [1, 1, 1, 0, 1],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 5),                      # book example 1
        (EXAMPLE_2, 6),                      # book example 2 (diagonals)
        (EXAMPLE_3, 1),                      # former example 3: one ring
        ([[0]], 0),                          # smallest, no land
        ([[1]], 1),                          # smallest, one island
        ([[0, 0, 0], [0, 0, 0]], 0),         # all water
        ([[1, 1], [1, 1]], 1),               # all land
        ([[1, 0, 1, 0, 1]], 3),              # one row
        ([[1], [1], [0], [1]], 2),           # one column
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_1]
    solve(grid)
    assert grid == EXAMPLE_1


def test_random_grids_agree_with_networkx():
    rng = random.Random(200)
    for _ in range(1500):
        rows, cols = rng.randint(1, 8), rng.randint(1, 8)
        density = rng.choice((0.3, 0.5, 0.7))
        grid = [[1 if rng.random() < density else 0
                 for _ in range(cols)] for _ in range(rows)]
        g = nx.grid_2d_graph(rows, cols)
        g.remove_nodes_from([(r, c) for r in range(rows)
                             for c in range(cols) if grid[r][c] == 0])
        expected = nx.number_connected_components(g)
        for solve in SOLVERS:
            assert solve(grid) == expected


@pytest.mark.parametrize("solve", FAST)
def test_all_land_is_fast(solve):
    # One 400 x 400 island: a recursive flood would go 160,000 deep.
    grid = [[1] * 400 for _ in range(400)]
    start = time.perf_counter()
    assert solve(grid) == 1
    assert time.perf_counter() - start < 2.0


@pytest.mark.parametrize("solve", FAST)
def test_checkerboard_is_fast(solve):
    # The most islands possible: every land cell is alone.
    n = 400
    grid = [[(r + c + 1) % 2 for c in range(n)] for r in range(n)]
    assert solve(grid) == n * n // 2
