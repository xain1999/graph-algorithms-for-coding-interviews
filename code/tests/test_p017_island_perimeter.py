import random

import pytest

from solutions.p017_island_perimeter import island_perimeter
from solutions.p017_island_perimeter_sides import island_perimeter_sides

SOLVERS = [island_perimeter, island_perimeter_sides]

EXAMPLE_1 = [
    [0, 1, 1, 0, 0],
    [1, 1, 1, 1, 0],
    [0, 0, 1, 0, 0],
    [0, 1, 1, 1, 0],
]
EXAMPLE_3 = [
    [1, 1, 1],
    [1, 0, 1],
    [1, 1, 1],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 20),                     # book example 1
        ([[0, 1], [0, 1], [0, 1], [0, 0]], 8),  # book example 2
        ([[0, 0, 0], [0, 1, 1], [0, 1, 0]], 8),  # former book example 3
        ([[1]], 4),                          # smallest island
        (EXAMPLE_3, 16),                     # lake shore counts too
        ([[1, 1, 1, 1]], 10),                # a strip
        ([[1, 1], [1, 1]], 8),               # a square block
        ([[1], [1], [1]], 8),                # a column
        ([[0, 1, 0], [1, 1, 1], [0, 1, 0]], 12),  # a plus sign
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_1]
    solve(grid)
    assert grid == EXAMPLE_1


def random_island(rng, rows, cols):
    """Grow one connected island by random steps from a random cell."""
    grid = [[0] * cols for _ in range(rows)]
    r, c = rng.randrange(rows), rng.randrange(cols)
    grid[r][c] = 1
    land = [(r, c)]
    for _ in range(rng.randint(0, rows * cols)):
        r, c = rng.choice(land)
        dr, dc = rng.choice(((1, 0), (-1, 0), (0, 1), (0, -1)))
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols and not grid[nr][nc]:
            grid[nr][nc] = 1
            land.append((nr, nc))
    return grid


def perimeter_by_edges(grid):
    """Reference: count unit sides that belong to exactly one cell."""
    sides = {}
    for r, row in enumerate(grid):
        for c, v in enumerate(row):
            if v == 1:
                for side in (("h", r, c), ("h", r + 1, c),
                             ("v", r, c), ("v", r, c + 1)):
                    sides[side] = sides.get(side, 0) + 1
    return sum(1 for k in sides.values() if k == 1)


def test_random_islands_agree():
    rng = random.Random(463)
    for _ in range(1500):
        rows, cols = rng.randint(1, 8), rng.randint(1, 8)
        grid = random_island(rng, rows, cols)
        expected = perimeter_by_edges(grid)
        for solve in SOLVERS:
            assert solve(grid) == expected


def test_large_grid_is_fast():
    n = 200
    grid = [[1] * n for _ in range(n)]
    for solve in SOLVERS:
        assert solve(grid) == 4 * n
