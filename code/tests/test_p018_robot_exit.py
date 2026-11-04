import random
import time

import networkx as nx
import pytest

from solutions.p018_robot_exit import can_reach_exit
from solutions.p018_robot_exit_bfs import can_reach_exit_bfs
from solutions.p018_robot_exit_graph import can_reach_exit_graph

SOLVERS = [can_reach_exit, can_reach_exit_bfs, can_reach_exit_graph]

EXAMPLE_1 = [
    "..#...",
    ".##.#.",
    "...#..",
    "#.#...",
    "....#.",
]
EXAMPLE_2 = [
    "..#...",
    ".##.#.",
    "...#..",
    "#.##..",
    "....#.",
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, True),                   # book example 1
        (EXAMPLE_2, False),                  # book example 2 (one more wall)
        (["...", "...", "..#"], False),      # former example 3: exit walled
        (["."], True),                       # 1 x 1 open grid
        (["#"], False),                      # 1 x 1 wall
        (["#.", ".."], False),               # start is a wall
        ([".#", "#."], False),               # only a diagonal link
        (["....."], True),                   # one row
        ([".", ".", "#", "."], False),       # one column, blocked
        ([".#...", ".#.#.", "...#."], True),  # winding corridor
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


def to_networkx(grid):
    rows, cols = len(grid), len(grid[0])
    g = nx.grid_2d_graph(rows, cols)
    g.remove_nodes_from([(r, c) for r in range(rows)
                         for c in range(cols) if grid[r][c] == "#"])
    return g


def test_random_grids_agree_with_networkx():
    rng = random.Random(18)
    for _ in range(2000):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        density = rng.choice((0.2, 0.35, 0.5))
        grid = ["".join("#" if rng.random() < density else "."
                        for _ in range(cols)) for _ in range(rows)]
        g = to_networkx(grid)
        start, goal = (0, 0), (rows - 1, cols - 1)
        expected = (start in g and goal in g
                    and nx.has_path(g, start, goal))
        for solve in SOLVERS:
            assert solve(grid) == expected


def serpentine(rows, cols):
    """Corridors joined at alternating ends: one path of ~rc/2 cells."""
    grid = []
    for r in range(rows):
        if r % 2 == 0:
            grid.append("." * cols)
        elif r % 4 == 1:
            grid.append("#" * (cols - 1) + ".")
        else:
            grid.append("." + "#" * (cols - 1))
    return grid


@pytest.mark.parametrize("solve", SOLVERS)
def test_long_winding_path_is_fast(solve):
    # 399 x 400 grid: the only route is about 80,000 cells long, far
    # too deep for recursion.
    grid = serpentine(399, 400)
    start = time.perf_counter()
    assert solve(grid) is True
    assert time.perf_counter() - start < 2.0


@pytest.mark.parametrize("solve", SOLVERS)
def test_open_grid_is_fast(solve):
    grid = ["." * 400 for _ in range(400)]
    assert solve(grid) is True
    grid[-1] = "." * 399 + "#"
    assert solve(grid) is False
