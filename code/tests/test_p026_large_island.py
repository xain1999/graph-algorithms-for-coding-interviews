import random
import time

import pytest

from solutions.p026_large_island import largest_island
from solutions.p026_large_island_brute import (
    largest_island_brute,
    max_area,
)

SOLVERS = [largest_island, largest_island_brute]

EXAMPLE_1 = [
    [1, 1, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [0, 0, 0, 0, 1],
    [1, 1, 0, 1, 1],
    [0, 1, 0, 0, 0],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 10),                        # book example 1
        ([[1, 1, 1], [1, 1, 1]], 6),            # book example 2
        ([[0, 0], [0, 0], [0, 0]], 1),          # book example 3
        ([[0]], 1),
        ([[1]], 1),
        ([[1, 0, 1, 0, 1]], 3),
        ([[1, 1], [1, 0]], 4),                  # one island, 2 sides
        ([[0, 1], [1, 1]], 4),
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


def no_dedup(grid):
    """The bug from the text: add a size once per touching side."""
    rows, cols = len(grid), len(grid[0])
    label = [[0] * cols for _ in range(rows)]
    size = [0]
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and not label[r][c]:
                label[r][c] = len(size)
                stack, area = [(r, c)], 0
                while stack:
                    a, b = stack.pop()
                    area += 1
                    for x, y in ((a + 1, b), (a - 1, b),
                                 (a, b + 1), (a, b - 1)):
                        if (0 <= x < rows and 0 <= y < cols
                                and grid[x][y] == 1
                                and not label[x][y]):
                            label[x][y] = len(size)
                            stack.append((x, y))
                size.append(area)
    best = max(size)
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 0:
                total = 1
                for x, y in ((r + 1, c), (r - 1, c),
                             (r, c + 1), (r, c - 1)):
                    if 0 <= x < rows and 0 <= y < cols:
                        total += size[label[x][y]]
                best = max(best, total)
    return best


def test_counting_an_island_twice_is_wrong():
    # Cell (1, 1) touches the top-left island on three sides.
    assert no_dedup(EXAMPLE_1) == 16
    flipped = [row[:] for row in EXAMPLE_1]
    flipped[1][1] = 1
    assert max_area(flipped) == 6       # the true score


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_1]
    solve(grid)
    assert grid == EXAMPLE_1


def test_random_grids_agree_with_brute_force():
    rng = random.Random(827)
    for _ in range(1000):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        p = rng.choice((0.2, 0.5, 0.8, 1.0))
        grid = [[int(rng.random() < p) for _ in range(cols)]
                for _ in range(rows)]
        assert largest_island(grid) == largest_island_brute(grid)


def test_large_grid_is_fast():
    n = 500
    stripes = [[0 if c % 2 else 1 for c in range(n)]
               for _ in range(n)]       # columns of land and water
    start = time.perf_counter()
    assert largest_island(stripes) == 2 * n + 1  # join two
    full = [[1] * n for _ in range(n)]
    assert largest_island(full) == n * n
    empty = [[0] * n for _ in range(n)]
    assert largest_island(empty) == 1
    assert time.perf_counter() - start < 5
