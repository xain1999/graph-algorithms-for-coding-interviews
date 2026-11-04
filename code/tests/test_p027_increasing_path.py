import random
import time

import pytest

from solutions.p027_increasing_path import longest_increasing_path
from solutions.p027_increasing_path_brute import (
    longest_increasing_path_brute,
)
from solutions.p027_increasing_path_layers import (
    longest_increasing_path_layers,
)
from solutions.p027_increasing_path_memo import (
    longest_increasing_path_memo,
)

FAST = [longest_increasing_path, longest_increasing_path_layers]
SOLVERS = FAST + [longest_increasing_path_memo,
                  longest_increasing_path_brute]

EXAMPLE_1 = [
    [2, 3, 8, 9],
    [1, 5, 6, 7],
    [0, 4, 9, 2],
]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "matrix, expected",
    [
        (EXAMPLE_1, 8),                         # book example 1
        ([[1, 2, 3, 4], [8, 7, 6, 5]], 8),      # book example 2
        ([[7, 7], [7, 7], [7, 7]], 1),          # book example 3
        ([[5]], 1),
        ([[3, 1, 2]], 2),
        ([[1], [2], [3], [2], [1]], 3),
        ([[-5, -4], [0, -3]], 4),               # negatives are fine
        ([[1, 2], [4, 3]], 4),
    ],
)
def test_examples(solve, matrix, expected):
    assert solve(matrix) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    matrix = [row[:] for row in EXAMPLE_1]
    solve(matrix)
    assert matrix == EXAMPLE_1


def test_random_matrices_agree_with_brute_force():
    rng = random.Random(329)
    for _ in range(1500):
        rows, cols = rng.randint(1, 5), rng.randint(1, 5)
        top = rng.choice((2, 5, 30))    # few values: many ties
        matrix = [[rng.randint(0, top) for _ in range(cols)]
                  for _ in range(rows)]
        want = longest_increasing_path_brute(matrix)
        for solve in FAST + [longest_increasing_path_memo]:
            assert solve(matrix) == want


def snake(n: int) -> list[list[int]]:
    """Numbers 0..n*n-1 written boustrophedon: one path of n*n."""
    return [[r * n + (c if r % 2 == 0 else n - 1 - c)
             for c in range(n)] for r in range(n)]


@pytest.mark.parametrize("solve", FAST)
def test_long_path_needs_no_recursion(solve):
    n = 250
    start = time.perf_counter()
    assert solve(snake(n)) == n * n     # 62,500 cells deep
    rng = random.Random(1)
    noise = [[rng.randint(-10**9, 10**9) for _ in range(n)]
             for _ in range(n)]
    assert solve(noise) == longest_increasing_path_layers(noise)
    assert time.perf_counter() - start < 10


def test_recursive_memo_hits_the_limit_on_one_long_row():
    with pytest.raises(RecursionError):
        longest_increasing_path_memo([list(range(3000))])
