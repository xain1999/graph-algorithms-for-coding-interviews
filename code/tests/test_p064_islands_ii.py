import random
import time

import pytest

from solutions.p064_islands_ii import islands_after_each
from solutions.p064_islands_ii_brute import (
    count_islands,
    islands_after_each_brute,
)

SOLVERS = [islands_after_each, islands_after_each_brute]

EXAMPLE_1 = [[1, 0], [0, 2], [2, 2], [1, 3], [1, 2], [1, 2],
             [3, 4], [1, 1]]
EXAMPLE_2 = [[0, 0], [1, 1], [2, 2], [0, 2], [1, 3], [1, 2]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "rows, cols, added, expected",
    [
        # book example 1: a three-way merge, a repeat, a bridge
        (4, 5, EXAMPLE_1, [1, 2, 3, 4, 2, 2, 3, 2]),
        # book example 2: four diagonal islands joined by one cell
        (3, 4, EXAMPLE_2, [1, 2, 3, 4, 5, 2]),
        # the same cell three times
        (1, 3, [[0, 1], [0, 1], [0, 1]], [1, 1, 1]),
        (1, 1, [[0, 0]], [1]),                     # smallest grid
        (1, 1, [], []),                            # nothing added
        (1, 5, [[0, 0], [0, 4], [0, 2], [0, 1], [0, 3]],
         [1, 2, 3, 2, 1]),                         # a row closes up
        (2, 2, [[0, 0], [1, 1], [0, 1], [1, 0]], [1, 2, 1, 1]),
        # a cell that touches the same island on two sides
        (2, 2, [[0, 0], [0, 1], [1, 0], [1, 1]], [1, 1, 1, 1]),
        # diagonal cells are not neighbors
        (3, 3, [[0, 0], [1, 1], [2, 2]], [1, 2, 3]),
    ],
)
def test_examples(solve, rows, cols, added, expected):
    assert solve(rows, cols, added) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    added = [cell[:] for cell in EXAMPLE_1]
    solve(4, 5, added)
    assert added == EXAMPLE_1


def test_random_agree_with_brute_force():
    rng = random.Random(305)
    for _ in range(600):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        k = rng.randint(0, 2 * rows * cols)
        added = [[rng.randrange(rows), rng.randrange(cols)]
                 for _ in range(k)]
        assert (islands_after_each(rows, cols, added)
                == islands_after_each_brute(rows, cols, added))


def test_large_input_is_fast():
    rng = random.Random(64)
    rows, cols, k = 250, 200, 50_000
    added = [[rng.randrange(rows), rng.randrange(cols)]
             for _ in range(k)]
    start = time.perf_counter()
    counts = islands_after_each(rows, cols, added)
    assert time.perf_counter() - start < 2.0
    grid = [[0] * cols for _ in range(rows)]
    for r, c in added:
        grid[r][c] = 1
    assert counts[-1] == count_islands(grid)


def test_snake_merges_many_islands():
    # Fill every other column first, then the joining cells.
    rows, cols = 50, 99
    added = [[r, c] for c in range(0, cols, 2) for r in range(rows)]
    added += [[0, c] for c in range(1, cols, 2)]
    counts = islands_after_each(rows, cols, added)
    assert counts[rows * 50 - 1] == 50
    assert counts[-1] == 1


def test_merging_with_water_undercounts():
    # Pitfall in the book: union with a water neighbor succeeds, so
    # the count drops for a merge that never happened.
    from solutions.p064_islands_ii import DIRECTIONS, UnionFind
    rows, cols = 1, 3
    uf = UnionFind(rows * cols)
    land = [False] * (rows * cols)
    islands, counts = 0, []
    for r, c in [[0, 0], [0, 2]]:
        cell = r * cols + c
        land[cell] = True
        islands += 1
        for dr, dc in DIRECTIONS:
            nr, nc = r + dr, c + dc
            if (0 <= nr < rows and 0 <= nc < cols
                    and uf.union(cell, nr * cols + nc)):
                islands -= 1            # no land check: the bug
        counts.append(islands)
    assert counts == [0, 0]
    assert islands_after_each(1, 3, [[0, 0], [0, 2]]) == [1, 2]
