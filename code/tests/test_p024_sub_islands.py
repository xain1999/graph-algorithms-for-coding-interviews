import random
import time

import pytest

from solutions.p024_sub_islands import count_sub_islands
from solutions.p024_sub_islands_sink import count_sub_islands_sink

SOLVERS = [count_sub_islands, count_sub_islands_sink]

GRID1 = [
    [1, 1, 1, 0, 0, 1],
    [1, 1, 0, 0, 1, 1],
    [0, 1, 1, 0, 1, 0],
    [0, 0, 0, 0, 1, 1],
    [1, 1, 0, 1, 1, 1],
]
GRID2 = [
    [1, 1, 0, 0, 0, 1],
    [0, 1, 1, 0, 0, 1],
    [0, 0, 1, 0, 1, 0],
    [1, 0, 0, 0, 1, 1],
    [1, 1, 0, 0, 0, 1],
]
ALL_LAND = [[1, 1, 1], [1, 1, 1]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid1, grid2, expected",
    [
        (GRID1, GRID2, 2),                      # book example 1
        # book example 2: one big island in grid1 holds three
        (ALL_LAND, [[1, 0, 1], [0, 1, 0]], 3),
        # book example 3: grid2's one island has a hole under it
        ([[1, 1, 0, 1]], [[1, 1, 1, 1]], 0),
        ([[0]], [[0]], 0),
        ([[1]], [[1]], 1),
        ([[0]], [[1]], 0),
        ([[1]], [[0]], 0),
        ([[1, 0, 1]], [[1, 0, 1]], 2),          # identical grids
    ],
)
def test_examples(solve, grid1, grid2, expected):
    assert solve(grid1, grid2) == expected


def early_stop(grid1, grid2):
    """The bug from the text: stop flooding at the first bad cell."""
    rows, cols = len(grid2), len(grid2[0])
    seen = [[False] * cols for _ in range(rows)]
    count = 0
    for sr in range(rows):
        for sc in range(cols):
            if grid2[sr][sc] != 1 or seen[sr][sc]:
                continue
            seen[sr][sc] = True
            stack, ok = [(sr, sc)], True
            while stack:
                r, c = stack.pop()
                if grid1[r][c] == 0:
                    ok = False
                    break
                for nr, nc in ((r + 1, c), (r - 1, c),
                               (r, c + 1), (r, c - 1)):
                    if (0 <= nr < rows and 0 <= nc < cols
                            and grid2[nr][nc] == 1
                            and not seen[nr][nc]):
                        seen[nr][nc] = True
                        stack.append((nr, nc))
            count += ok
    return count


def test_stopping_early_overcounts_example_1():
    assert early_stop(GRID1, GRID2) == 4


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    g1 = [row[:] for row in GRID1]
    g2 = [row[:] for row in GRID2]
    solve(g1, g2)
    assert g1 == GRID1 and g2 == GRID2


def components(grid):
    rows, cols = len(grid), len(grid[0])
    label, k = {}, 0
    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 1 and (r, c) not in label:
                k += 1
                label[(r, c)] = k
                stack = [(r, c)]
                while stack:
                    a, b = stack.pop()
                    for x, y in ((a + 1, b), (a - 1, b),
                                 (a, b + 1), (a, b - 1)):
                        if (0 <= x < rows and 0 <= y < cols
                                and grid[x][y] == 1
                                and (x, y) not in label):
                            label[(x, y)] = k
                            stack.append((x, y))
    return label


def reference(grid1, grid2):
    """Group grid2 cells by island, then check each group."""
    groups = {}
    for cell, k in components(grid2).items():
        groups.setdefault(k, []).append(cell)
    return sum(all(grid1[r][c] == 1 for r, c in cells)
               for cells in groups.values())


def test_random_grids_agree():
    rng = random.Random(1905)
    for _ in range(1500):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        p1, p2 = rng.random(), rng.random()
        g1 = [[int(rng.random() < p1) for _ in range(cols)]
              for _ in range(rows)]
        g2 = [[int(rng.random() < p2) for _ in range(cols)]
              for _ in range(rows)]
        want = reference(g1, g2)
        assert count_sub_islands(g1, g2) == want
        assert count_sub_islands_sink(g1, g2) == want


@pytest.mark.parametrize("solve", SOLVERS)
def test_large_grid_is_fast(solve):
    n = 400
    grid1 = [[1] * n for _ in range(n)]
    snake = [[1 if r % 2 == 0 or (c == n - 1 if r % 4 == 1 else c == 0)
              else 0 for c in range(n)] for r in range(n)]
    start = time.perf_counter()
    assert solve(grid1, snake) == 1     # one long snake
    grid1[n - 1][0] = 0
    assert solve(grid1, snake) == 0     # its tail is over water
    assert time.perf_counter() - start < 5
