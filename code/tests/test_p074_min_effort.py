import random
import time

import pytest

from solutions.p074_min_effort import minimum_effort
from solutions.p074_min_effort_binary import minimum_effort_binary
from solutions.p074_min_effort_brute import minimum_effort_brute
from solutions.p074_min_effort_uf import minimum_effort_uf

SOLVERS = [minimum_effort, minimum_effort_brute, minimum_effort_binary,
           minimum_effort_uf]

EXAMPLE_1 = [[2, 2, 3, 10], [5, 6, 5, 1], [3, 2, 1, 6], [6, 11, 3, 4]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "heights, expected",
    [
        (EXAMPLE_1, 2),                    # book example 1
        ([[10, 4, 7]], 6),                 # book example 2
        ([[7]], 0),                        # single cell
        ([[3], [8], [1]], 7),              # single column
        ([[5, 5], [5, 5]], 0),             # flat
        ([[1, 9], [2, 3]], 1),             # detour beats the jump
        ([[1, 100, 1], [1, 100, 1], [1, 1, 1]], 0),  # go around
    ],
)
def test_examples(solve, heights, expected):
    assert solve(heights) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    heights = [row[:] for row in EXAMPLE_1]
    solve(heights)
    assert heights == EXAMPLE_1


def test_random_grids_agree():
    rng = random.Random(1631)
    for _ in range(800):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        top = rng.choice((3, 10, 1000))
        heights = [[rng.randint(1, top) for _ in range(cols)]
                   for _ in range(rows)]
        expected = minimum_effort_brute(heights)
        for solve in SOLVERS:
            assert solve(heights) == expected


def test_large_grid_is_fast():
    rng = random.Random(74)
    heights = [[rng.randint(1, 5_000_000) for _ in range(150)]
               for _ in range(150)]
    start = time.perf_counter()
    answer = minimum_effort(heights)
    assert time.perf_counter() - start < 2.0
    assert answer == minimum_effort_uf(heights)
    assert answer == minimum_effort_binary(heights)
