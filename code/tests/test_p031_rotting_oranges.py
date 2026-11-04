import random

import pytest

from solutions.p031_rotting_oranges import oranges_rotting
from solutions.p031_rotting_oranges_brute import oranges_rotting_brute

SOLVERS = [oranges_rotting, oranges_rotting_brute]

EXAMPLE_1 = [
    [2, 1, 1, 0, 1],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 0],
    [0, 0, 1, 1, 2],
]
EXAMPLE_2 = [
    [2, 1, 1, 0, 1],
    [1, 1, 0, 1, 1],
    [0, 1, 1, 1, 0],
    [1, 0, 1, 1, 2],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 5),                      # book example 1 (two sources)
        (EXAMPLE_2, -1),                     # book example 2 (isolated orange)
        ([[0, 0, 0], [0, 2, 0]], 0),          # nothing fresh (edge case)
        ([[0]], 0),                          # empty grid cell only
        ([[1]], -1),                         # fresh, no rotten
        ([[2]], 0),
        ([[1, 1, 1]], -1),                   # fresh but no source at all
        ([[2, 1, 1, 1, 1]], 4),              # single chain
        ([[2, 1, 1, 1, 2]], 2),              # spreads from both ends
        ([[2, 0, 1]], -1),                   # blocked by empty cell
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_1]
    solve(grid)
    assert grid == EXAMPLE_1


def test_random_grids_agree_with_brute_force():
    rng = random.Random(994)
    for _ in range(2000):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        grid = [[rng.choice((0, 1, 1, 2)) for _ in range(cols)] for _ in range(rows)]
        assert oranges_rotting(grid) == oranges_rotting_brute(grid)


def test_large_grid_is_fast():
    grid = [[1] * 300 for _ in range(300)]
    grid[0][0] = 2
    assert oranges_rotting(grid) == 598     # Manhattan distance to the far corner
