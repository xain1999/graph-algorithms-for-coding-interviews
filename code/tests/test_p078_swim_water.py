import random
import time

import pytest

from solutions.p078_swim_water import swim_in_water
from solutions.p078_swim_water_binary import swim_in_water_binary
from solutions.p078_swim_water_brute import swim_in_water_brute
from solutions.p078_swim_water_uf import swim_in_water_uf

SOLVERS = [swim_in_water, swim_in_water_brute, swim_in_water_binary,
           swim_in_water_uf]

EXAMPLE_1 = [
    [2, 9, 16, 21, 14],
    [5, 12, 3, 7, 20],
    [8, 19, 6, 22, 11],
    [4, 23, 10, 17, 13],
    [1, 15, 18, 24, 0],
]
EXAMPLE_2 = [[6, 2, 3], [1, 0, 4], [7, 5, 1]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 17),                 # book example 1
        (EXAMPLE_2, 6),                  # book example 2 (start counts)
        ([[0]], 0),                      # single cell
        ([[7]], 7),                      # single cell, positive height
        ([[0, 5], [3, 9]], 9),           # the target's height counts
        ([[1, 1], [1, 1]], 1),           # repeated heights
        ([[0, 1, 2], [9, 9, 3], [6, 5, 4]], 4),   # spiral around
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
    rng = random.Random(778)
    for _ in range(1500):
        n = rng.randint(1, 6)
        top = rng.choice((3, 10, 100))
        grid = [[rng.randint(0, top) for _ in range(n)]
                for _ in range(n)]
        expected = swim_in_water_brute(grid)
        assert swim_in_water(grid) == expected
        assert swim_in_water_binary(grid) == expected
        assert swim_in_water_uf(grid) == expected


def test_large_grid_is_fast():
    n = 100
    rng = random.Random(1)
    grid = [[rng.randint(0, 10**6) for _ in range(n)] for _ in range(n)]
    # A snake-shaped low channel forces a long path.
    for r in range(n):
        for c in range(n):
            if r % 4 == 1 and c != n - 1 or r % 4 == 3 and c != 0:
                continue
            grid[r][c] = r * n + c          # channel, < 10**4
    start = time.perf_counter()
    got = swim_in_water(grid)
    assert time.perf_counter() - start < 2.0
    assert got == swim_in_water_binary(grid) == swim_in_water_uf(grid)
