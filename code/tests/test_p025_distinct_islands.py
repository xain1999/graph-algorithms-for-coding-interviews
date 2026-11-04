import random
import time

import pytest

from solutions.p025_distinct_islands import count_distinct_islands
from solutions.p025_distinct_islands_brute import (
    count_distinct_islands_brute,
)
from solutions.p025_distinct_islands_path import (
    count_distinct_islands_path,
    island_signature,
)

SOLVERS = [count_distinct_islands, count_distinct_islands_path,
           count_distinct_islands_brute]

EXAMPLE_1 = [
    [1, 1, 0, 0, 1, 1, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [0, 0, 1, 0, 0, 0, 1],
    [1, 0, 1, 1, 0, 1, 1],
    [1, 1, 0, 0, 0, 0, 0],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 3),                         # book example 1
        # book example 2: a rotated copy is a different shape
        ([[1, 1, 1, 0, 1], [0, 0, 0, 0, 1], [0, 0, 0, 0, 1]], 2),
        ([[1, 1, 0, 1, 1], [1, 0, 0, 0, 1]], 2),   # mirror images
        ([[0]], 0),
        ([[1]], 1),
        ([[1, 1, 1]], 1),
        ([[1, 0, 1, 1]], 2),                    # sizes differ
        ([[1, 1], [1, 1]], 1),
        ([[1, 0, 1, 0], [0, 1, 0, 1]], 1),      # diagonal: 4 islands
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


def test_backtrack_marker_is_needed():
    # Two L-shaped trominoes from the text: same moves, other shape.
    a = [[1, 1], [1, 0]]
    b = [[1, 0], [1, 1]]
    sig_a = island_signature(a, [[False] * 2 for _ in range(2)], 0, 0)
    sig_b = island_signature(b, [[False] * 2 for _ in range(2)], 0, 0)
    assert sig_a == "DbRbb" and sig_b == "DRbbb"
    assert sig_a.replace("b", "") == sig_b.replace("b", "")


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_1]
    solve(grid)
    assert grid == EXAMPLE_1


def test_random_grids_agree():
    rng = random.Random(694)
    for _ in range(1500):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        p = rng.choice((0.3, 0.5, 0.7))
        grid = [[int(rng.random() < p) for _ in range(cols)]
                for _ in range(rows)]
        want = count_distinct_islands_brute(grid)
        assert count_distinct_islands(grid) == want
        assert count_distinct_islands_path(grid) == want


@pytest.mark.parametrize("solve", [count_distinct_islands,
                                   count_distinct_islands_path])
def test_large_grid_is_fast(solve):
    n = 400
    checker = [[(r // 2 + c // 2) % 2 for c in range(n)]
               for r in range(n)]       # 2x2 blocks: one shape
    full = [[1] * n for _ in range(n)]  # one island of 160,000 cells
    start = time.perf_counter()
    assert solve(checker) == 1
    assert solve(full) == 1
    assert time.perf_counter() - start < 5


def canonical_up_to_symmetry(cells):
    """Smallest normalized form over the 8 rotations/reflections."""
    forms = []
    for sr, sc in ((1, 1), (1, -1), (-1, 1), (-1, -1)):
        for swap in (False, True):
            moved = sorted((sc * c, sr * r) if swap else (sr * r, sc * c)
                           for r, c in cells)
            r0, c0 = moved[0]
            forms.append(tuple((r - r0, c - c0) for r, c in moved))
    return min(forms)


def test_follow_up_example_1_has_one_shape_up_to_symmetry():
    from solutions.p025_distinct_islands_brute import islands_of
    keys = {canonical_up_to_symmetry(i) for i in islands_of(EXAMPLE_1)}
    assert len(keys) == 1
