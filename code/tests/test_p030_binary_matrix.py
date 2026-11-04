import random

import networkx as nx
import pytest

from solutions.p030_binary_matrix import shortest_path_binary_matrix
from solutions.p030_binary_matrix_brute import shortest_path_brute

SOLVERS = [shortest_path_binary_matrix, shortest_path_brute]

EXAMPLE_1 = [
    [0, 0, 1, 0, 0],
    [1, 0, 1, 0, 1],
    [1, 0, 1, 0, 1],
    [0, 1, 0, 1, 0],
    [0, 0, 1, 1, 0],
]
EXAMPLE_2 = [
    [0, 0, 1, 0],
    [0, 0, 1, 0],
    [1, 1, 1, 0],
    [0, 0, 0, 0],
]
# A diagonal line of 1s is no wall: (1,1) -> (2,2) slips through.
LEAKY = [
    [0, 0, 0, 1],
    [0, 0, 1, 0],
    [0, 1, 0, 0],
    [1, 0, 0, 0],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "grid, expected",
    [
        (EXAMPLE_1, 7),                 # book example 1
        (EXAMPLE_2, -1),                # book example 2 (sealed)
        ([[0]], 1),                     # book example 3
        (LEAKY, 4),                     # pitfall: corner squeeze
        ([[1]], -1),                    # blocked single cell
        ([[0, 0], [0, 0]], 2),          # one diagonal step
        ([[0, 1, 1], [1, 0, 1], [1, 1, 0]], 3),  # diagonal only
        ([[0, 0], [0, 1]], -1),         # blocked end
        ([[1, 0], [0, 0]], -1),         # blocked start
        ([[0, 0, 0], [0, 0, 0], [0, 0, 0]], 3),
    ],
)
def test_examples(solve, grid, expected):
    assert solve(grid) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    grid = [row[:] for row in EXAMPLE_1]
    solve(grid)
    assert grid == EXAMPLE_1


def networkx_answer(grid):
    n = len(grid)
    g = nx.Graph()
    for r in range(n):
        for c in range(n):
            if grid[r][c]:
                continue
            g.add_node((r, c))
            for dr in (-1, 0, 1):
                for dc in (-1, 0, 1):
                    nr, nc = r + dr, c + dc
                    if ((dr or dc) and 0 <= nr < n and 0 <= nc < n
                            and grid[nr][nc] == 0):
                        g.add_edge((r, c), (nr, nc))
    end = (n - 1, n - 1)
    if (0, 0) not in g or end not in g:
        return -1
    try:
        return nx.shortest_path_length(g, (0, 0), end) + 1
    except nx.NetworkXNoPath:
        return -1


def test_random_grids_agree_with_brute_force():
    rng = random.Random(1091)
    for _ in range(600):
        n = rng.randint(1, 4)
        grid = [[int(rng.random() < 0.35) for _ in range(n)]
                for _ in range(n)]
        assert shortest_path_binary_matrix(grid) == \
            shortest_path_brute(grid)


def test_random_grids_agree_with_networkx():
    rng = random.Random(8)
    for _ in range(300):
        n = rng.randint(1, 12)
        grid = [[int(rng.random() < 0.4) for _ in range(n)]
                for _ in range(n)]
        assert shortest_path_binary_matrix(grid) == \
            networkx_answer(grid)


def test_large_grid_is_fast():
    n = 300
    grid = [[0] * n for _ in range(n)]
    assert shortest_path_binary_matrix(grid) == n   # the diagonal
    # A serpentine maze: walls with a gap at alternating ends.
    maze = [[0] * n for _ in range(n)]
    for r in range(1, n - 1, 2):
        for c in range(n):
            maze[r][c] = 1
        maze[r][n - 1 if r % 4 == 1 else 0] = 0
    assert shortest_path_binary_matrix(maze) == networkx_answer(maze)
