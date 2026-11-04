import random

import networkx as nx
import pytest

from solutions.p020_max_area_island import max_area_of_island
from solutions.p020_max_area_island_brute import (
    max_area_of_island_brute,
)
from solutions.p020_max_area_island_recursive import (
    max_area_of_island_recursive,
)

SOLVERS = [max_area_of_island, max_area_of_island_brute,
           max_area_of_island_recursive]

EXAMPLE_1 = [
    [1, 1, 0, 0, 1, 1],
    [1, 0, 0, 1, 1, 0],
    [0, 0, 1, 1, 0, 0],
    [1, 0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1, 1],
]


def nx_max_area(grid):
    g = nx.Graph()
    rows, cols = len(grid), len(grid[0])
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1:
                g.add_node((r, c))
                if r + 1 < rows and grid[r + 1][c] == 1:
                    g.add_edge((r, c), (r + 1, c))
                if c + 1 < cols and grid[r][c + 1] == 1:
                    g.add_edge((r, c), (r, c + 1))
    sizes = [len(s) for s in nx.connected_components(g)]
    return max(sizes, default=0)


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 6),                              # book example 1
        ([[1, 0, 1], [0, 1, 0], [1, 0, 1]], 1),      # book example 2
        ([[1, 1, 1], [1, 0, 1], [1, 1, 1]], 8),      # former book example 3
        ([[0]], 0),
        ([[1]], 1),
        ([[0, 0], [0, 0]], 0),                       # no land at all
        ([[1, 1, 1, 1]], 4),                         # single row
        ([[1], [0], [1], [1]], 2),                   # single column
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_1]
    solve(grid)
    assert grid == EXAMPLE_1


def test_random_grids_agree():
    rng = random.Random(695)
    for _ in range(800):
        rows, cols = rng.randint(1, 8), rng.randint(1, 8)
        p = rng.random()
        grid = [[int(rng.random() < p) for _ in range(cols)]
                for _ in range(rows)]
        want = nx_max_area(grid)
        for solve in SOLVERS:
            assert solve(grid) == want


def test_large_snake_is_fast_and_iterative():
    # a snake through a 400 x 400 grid: one chain of ~80,000 cells
    n = 400
    grid = [[0] * n for _ in range(n)]
    for r in range(0, n, 2):
        grid[r] = [1] * n
        if r + 1 < n:
            grid[r + 1][n - 1 if r % 4 == 0 else 0] = 1
    expected = sum(map(sum, grid))
    assert max_area_of_island(grid) == expected


def test_large_full_grid():
    grid = [[1] * 400 for _ in range(400)]
    assert max_area_of_island(grid) == 160_000
