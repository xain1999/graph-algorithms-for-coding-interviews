import random
import time

import networkx as nx
import pytest

from solutions.p079_min_cost_grid import MOVES, min_cost
from solutions.p079_min_cost_grid_brute import min_cost_brute
from solutions.p079_min_cost_grid_dijkstra import min_cost_dijkstra

SOLVERS = [min_cost, min_cost_dijkstra, min_cost_brute]

EXAMPLE_1 = [
    [1, 1, 3, 2, 1],
    [3, 4, 2, 4, 3],
    [1, 3, 1, 1, 4],
    [4, 1, 1, 2, 2],
]
EXAMPLE_2 = [[4, 1, 1, 3], [2, 4, 1, 2]]


def networkx_cost(grid):
    rows, cols = len(grid), len(grid[0])
    g = nx.DiGraph()
    g.add_node((0, 0))
    for r in range(rows):
        for c in range(cols):
            for sign, (dr, dc) in MOVES.items():
                nr, nc = r + dr, c + dc
                if 0 <= nr < rows and 0 <= nc < cols:
                    w = 0 if grid[r][c] == sign else 1
                    g.add_edge((r, c), (nr, nc), weight=w)
    return nx.shortest_path_length(g, (0, 0), (rows - 1, cols - 1),
                                   weight="weight")


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 2),                  # book example 1 (free loop)
        (EXAMPLE_2, 1),                  # book example 2 (off the grid)
        ([[4]], 0),                      # start is the target
        ([[1, 1, 3], [4, 4, 3]], 0),     # signs already lead there
        ([[2, 2, 2, 2]], 3),             # one row, all wrong
        ([[4], [4], [4], [4]], 3),       # one column, all wrong
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
    rng = random.Random(1368)
    for _ in range(800):
        rows, cols = rng.randint(1, 6), rng.randint(1, 6)
        grid = [[rng.randint(1, 4) for _ in range(cols)]
                for _ in range(rows)]
        expected = networkx_cost(grid)
        assert min_cost(grid) == expected
        assert min_cost_dijkstra(grid) == expected
        assert min_cost_brute(grid) == expected


def test_large_grid_is_fast():
    rng = random.Random(7)
    grid = [[rng.randint(1, 4) for _ in range(150)] for _ in range(150)]
    start = time.perf_counter()
    got = min_cost(grid)
    assert time.perf_counter() - start < 2.0
    assert got == min_cost_dijkstra(grid)
    # All signs pointing left: every step must be paid for.
    assert min_cost([[2] * 150 for _ in range(150)]) == 298
