import random
import time

import pytest

from solutions.p040_obstacles import shortest_path
from solutions.p040_obstacles_alt import shortest_path_states
from solutions.p040_obstacles_brute import shortest_path_brute

SOLVERS = [shortest_path, shortest_path_states, shortest_path_brute]

GRID_1 = [
    [0, 1, 0, 0, 0],
    [0, 0, 0, 1, 0],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
]
GRID_3 = [
    [0, 1, 1, 1],
    [1, 1, 1, 1],
    [1, 1, 1, 0],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, k, expected",
    [
        (GRID_1, 1, 9),         # book example 1: one wall, long detour
        (GRID_1, 2, 7),         # book example 2: two walls, straight
        (GRID_3, 4, 5),         # the shortcut applies (pitfall in the book)
        (GRID_3, 3, -1),        # one removal short of any path
        (GRID_1, 0, -1),        # no removals: walled in
        ([[0]], 0, 0),          # start is the target
        ([[0, 0]], 0, 1),
        ([[0], [1], [0]], 0, -1),
        ([[0], [1], [0]], 1, 2),
        ([[0, 0, 0], [0, 0, 0]], 5, 3),  # k far above the need
    ],
)
def test_examples(solve, grid, k, expected):
    assert solve(grid, k) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in GRID_1]
    solve(grid, 1)
    assert grid == GRID_1


def test_random_grids_agree_with_brute_force():
    rng = random.Random(1293)
    for _ in range(700):
        rows, cols = rng.randint(1, 4), rng.randint(1, 4)
        grid = [[int(rng.random() < 0.45) for _ in range(cols)]
                for _ in range(rows)]
        grid[0][0] = grid[-1][-1] = 0
        k = rng.randint(0, 3)
        expected = shortest_path_brute(grid, k)
        assert shortest_path(grid, k) == expected
        assert shortest_path_states(grid, k) == expected


def test_random_larger_grids_agree_with_state_bfs():
    rng = random.Random(40)
    for _ in range(200):
        rows, cols = rng.randint(2, 12), rng.randint(2, 12)
        grid = [[int(rng.random() < 0.5) for _ in range(cols)]
                for _ in range(rows)]
        grid[0][0] = grid[-1][-1] = 0
        k = rng.randint(0, rows + cols)
        assert (shortest_path(grid, k)
                == shortest_path_states(grid, k))


def test_large_grid_is_fast():
    rng = random.Random(7)
    n = 60
    grid = [[int(rng.random() < 0.45) for _ in range(n)]
            for _ in range(n)]
    grid[0][0] = grid[-1][-1] = 0
    start = time.perf_counter()
    for k in (10, 40, 80):
        answer = shortest_path(grid, k)
        assert answer == shortest_path_states(grid, k)
    assert time.perf_counter() - start < 5


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, k, expected",
    [
        ([[0] * 3 for _ in range(3)], 0, 4),  # R01: k = 0, open grid
        ([[0, 1], [1, 0]], 0, -1),            # R02: k = 0, blocked
        ([[0]], 0, 0),                        # R03: k = 0, one cell
    ],
)
def test_review_regressions_k_zero(solve, grid, k, expected):
    assert solve(grid, k) == expected
