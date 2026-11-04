import random
import time

import pytest

from solutions.p036_shortest_bridge import shortest_bridge
from solutions.p036_shortest_bridge_brute import shortest_bridge_brute

SOLVERS = [shortest_bridge, shortest_bridge_brute]

EXAMPLE_1 = [
    [1, 1, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 0, 0, 0],
    [1, 0, 0, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 1, 0],
    [0, 0, 0, 0, 0, 0, 0],
]
EXAMPLE_2 = [
    [1, 0, 0, 1],
    [1, 0, 0, 1],
    [1, 0, 0, 1],
]
EXAMPLE_3 = [
    [1, 1, 0],
    [0, 1, 0],
    [0, 0, 1],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 3),                 # book example 1
        (EXAMPLE_2, 2),                 # book example 2
        (EXAMPLE_3, 1),                 # diagonal contact (edge case)
        ([[1, 0, 1]], 1),
        ([[1], [0], [0], [0], [1]], 3),
        ([[1, 0], [0, 1]], 1),
        # One island rings the other: the gap is one cell.
        ([[1, 1, 1, 1, 1],
          [1, 0, 0, 0, 1],
          [1, 0, 1, 0, 1],
          [1, 0, 0, 0, 1],
          [1, 1, 1, 1, 1]], 1),
        ([[0, 0, 0, 0],
          [0, 1, 0, 0],
          [0, 0, 0, 0],
          [0, 0, 0, 1]], 3),            # bridge bends: 4 - 1 cells
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_1]
    solve(grid)
    assert grid == EXAMPLE_1


def count_islands(grid):
    rows, cols = len(grid), len(grid[0])
    seen = set()
    count = 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in seen:
                count += 1
                seen.add((r, c))
                stack = [(r, c)]
                while stack:
                    cr, cc = stack.pop()
                    for nr, nc in ((cr + 1, cc), (cr - 1, cc),
                                   (cr, cc + 1), (cr, cc - 1)):
                        if (0 <= nr < rows and 0 <= nc < cols
                                and grid[nr][nc] == 1
                                and (nr, nc) not in seen):
                            seen.add((nr, nc))
                            stack.append((nr, nc))
    return count


def test_random_two_island_grids_agree_with_brute_force():
    rng = random.Random(934)
    checked = 0
    while checked < 1500:
        rows, cols = rng.randint(1, 8), rng.randint(1, 8)
        p = rng.choice((0.15, 0.3, 0.45))
        grid = [[int(rng.random() < p) for _ in range(cols)]
                for _ in range(rows)]
        if count_islands(grid) != 2:
            continue
        checked += 1
        assert shortest_bridge(grid) == shortest_bridge_brute(grid)


def test_large_grid_is_fast_and_deep_island_is_safe():
    # A 300 x 300 grid: one snake-shaped island of about 45,000 cells
    # (far too deep for recursion) and a single cell far away.
    n = 300
    grid = [[0] * n for _ in range(n)]
    for r in range(0, n - 2, 2):
        for c in range(n - 1):
            grid[r][c] = 1
        grid[r + 1][0 if r % 4 == 2 else n - 2] = 1
    grid[n - 1][n - 1] = 1
    start = time.perf_counter()
    got = shortest_bridge(grid)
    assert time.perf_counter() - start < 2.0
    assert count_islands(grid) == 2
    assert got == 2         # from (297, 298): flip (298, 298), (298, 299)
