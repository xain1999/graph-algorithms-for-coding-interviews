import random

import pytest

from solutions.p032_01_matrix import update_matrix
from solutions.p032_01_matrix_brute import update_matrix_brute
from solutions.p032_01_matrix_dp import update_matrix_dp

SOLVERS = [update_matrix, update_matrix_brute, update_matrix_dp]

EXAMPLE_1 = [
    [1, 1, 1, 0, 1],
    [1, 1, 1, 1, 1],
    [0, 1, 1, 1, 1],
    [1, 1, 0, 1, 1],
]
ANSWER_1 = [
    [2, 2, 1, 0, 1],
    [1, 2, 2, 1, 2],
    [0, 1, 1, 2, 3],
    [1, 1, 0, 1, 2],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "mat, expected",
    [
        (EXAMPLE_1, ANSWER_1),                          # example 1
        ([[1, 1, 0, 1, 1, 1]], [[2, 1, 0, 1, 2, 3]]),   # example 2
        ([[0, 0], [0, 0]], [[0, 0], [0, 0]]),           # all zeros (edge case)
        ([[0]], [[0]]),
        ([[1], [1], [0]], [[2], [1], [0]]),             # one column
        ([[1, 1, 1], [1, 1, 1], [1, 1, 0]],
         [[4, 3, 2], [3, 2, 1], [2, 1, 0]]),           # far corner
    ],
)
def test_examples(solve, mat, expected):
    assert solve(mat) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    mat = [row[:] for row in EXAMPLE_1]
    solve(mat)
    assert mat == EXAMPLE_1


def manhattan_answer(mat):
    zeros = [(r, c) for r, row in enumerate(mat)
             for c, v in enumerate(row) if v == 0]
    return [[min(abs(r - zr) + abs(c - zc) for zr, zc in zeros)
             for c in range(len(mat[0]))] for r in range(len(mat))]


def test_random_grids_agree():
    rng = random.Random(542)
    for _ in range(800):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        mat = [[int(rng.random() < 0.7) for _ in range(cols)]
               for _ in range(rows)]
        mat[rng.randrange(rows)][rng.randrange(cols)] = 0
        expected = manhattan_answer(mat)
        for solve in SOLVERS:
            assert solve(mat) == expected


def test_large_grid_is_fast():
    rows, cols = 250, 400                   # 10^5 cells
    mat = [[1] * cols for _ in range(rows)]
    mat[0][0] = 0
    for solve in (update_matrix, update_matrix_dp):
        dist = solve(mat)
        assert dist[rows - 1][cols - 1] == rows + cols - 2
        assert dist[7][9] == 16
