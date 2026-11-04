import itertools
import random
import time

import pytest

from solutions.p097_disconnect_island import min_days
from solutions.p097_disconnect_island_brute import (
    count_islands, min_days_brute)

SOLVERS = [min_days, min_days_brute]

EXAMPLE_1 = [
    [1, 1, 1, 0, 0],
    [1, 1, 1, 1, 1],
    [0, 0, 1, 1, 1],
    [0, 0, 0, 1, 1],
]
EXAMPLE_2 = [
    [1, 1, 1, 0, 0],
    [1, 0, 1, 1, 1],
    [1, 1, 1, 0, 1],
    [0, 0, 1, 1, 1],
]


def exhaustive(grid):
    """Try flooding 0, 1, then 2 cells; checks the 'at most 2' claim."""
    land = [(r, c) for r, row in enumerate(grid)
            for c, v in enumerate(row) if v]
    for days in range(3):
        for cells in itertools.combinations(land, days):
            g = [row[:] for row in grid]
            for r, c in cells:
                g[r][c] = 0
            if count_islands(g) != 1:
                return days
    raise AssertionError("needed more than two days")


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 1),                 # book example 1 (one cut cell)
        (EXAMPLE_2, 2),                 # book example 2 (two rings)
        ([[1, 0], [0, 1]], 0),          # book example 3 (diagonal)
        ([[0, 0, 0]], 0),               # no land at all
        ([[1]], 1),                     # single cell: flood it
        ([[0, 1, 1]], 2),               # two cells: flood both
        ([[1, 1, 1]], 1),               # middle cell is a cut
        ([[1, 1], [1, 1]], 2),          # a square has no cut cell
        ([[1, 1], [1, 0]], 1),          # corner of an L is a cut
        ([[1, 1, 1], [1, 1, 1], [1, 1, 1]], 2),
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


# Review regression cases R06-R11 (tiny islands and witnesses).
REGRESSION = [
    ([[0]], 0),                         # R06 no land
    ([[1]], 1),                         # R07 one cell
    ([[1, 1]], 2),                      # R08 two cells
    ([[1, 1, 1]], 1),                   # R09 middle cell is a cut
    ([[1, 1], [1, 1]], 2),              # R10 square
    ([[1, 0, 1]], 0),                   # R11 two islands already
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize("grid, expected", REGRESSION)
def test_review_regressions(solve, grid, expected):
    assert solve(grid) == expected


def cells_to_flood(grid):
    """The follow-up's rule: which cells to flood, as a list."""
    land = [(r, c) for r, row in enumerate(grid)
            for c, v in enumerate(row) if v]
    if count_islands(grid) != 1:
        return []                       # already disconnected
    if len(land) <= 2:
        return land                     # flood the whole island
    for r, c in land:                   # an articulation point
        g = [row[:] for row in grid]
        g[r][c] = 0
        if count_islands(g) != 1:
            return [(r, c)]
    r, c = land[0]                      # first cell's neighbors
    return [(r + dr, c + dc) for dr, dc in ((1, 0), (0, 1))
            if (r + dr, c + dc) in set(land)]


def test_follow_up_witness_disconnects_in_min_days():
    rng = random.Random(1097)
    grids = [g for g, _ in REGRESSION] + [EXAMPLE_1, EXAMPLE_2]
    for _ in range(400):
        rows, cols = rng.randint(1, 5), rng.randint(1, 5)
        grids.append([[int(rng.random() < 0.75) for _ in range(cols)]
                      for _ in range(rows)])
    for grid in grids:
        cells = cells_to_flood(grid)
        assert len(cells) == min_days(grid)
        g = [row[:] for row in grid]
        for r, c in cells:
            g[r][c] = 0
        assert count_islands(g) != 1


def test_example_1_has_exactly_one_cut_cell():
    cuts = []
    for r, row in enumerate(EXAMPLE_1):
        for c, v in enumerate(row):
            if v:
                g = [row[:] for row in EXAMPLE_1]
                g[r][c] = 0
                if count_islands(g) != 1:
                    cuts.append((r, c))
    assert cuts == [(1, 2)]


def test_example_2_corner_needs_two_floods():
    g = [row[:] for row in EXAMPLE_2]
    g[0][1] = g[1][0] = 0
    assert count_islands(g) == 2


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_2]
    solve(grid)
    assert grid == EXAMPLE_2


def test_random_grids_agree_with_exhaustive_search():
    rng = random.Random(1568)
    for _ in range(600):
        rows, cols = rng.randint(1, 5), rng.randint(1, 5)
        p = rng.choice((0.5, 0.7, 0.85))
        grid = [[int(rng.random() < p) for _ in range(cols)]
                for _ in range(rows)]
        expected = exhaustive(grid)
        assert min_days(grid) == expected
        assert min_days_brute(grid) == expected


def test_random_larger_grids_agree_with_brute_force():
    rng = random.Random(97)
    for _ in range(200):
        rows, cols = rng.randint(1, 12), rng.randint(1, 12)
        grid = [[int(rng.random() < 0.75) for _ in range(cols)]
                for _ in range(rows)]
        assert min_days(grid) == min_days_brute(grid)


def test_large_grids_are_fast():
    full = [[1] * 60 for _ in range(60)]
    snake = [[1 if r % 2 == 0 or (c == 59 if r % 4 == 1 else c == 0)
              else 0 for c in range(60)] for r in range(60)]
    start = time.perf_counter()
    assert min_days(full) == 2
    assert min_days(snake) == 1         # a long path: deep DFS
    assert time.perf_counter() - start < 1.0
