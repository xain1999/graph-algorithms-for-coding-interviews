import random
import time

import pytest

from solutions.p038_knight_moves import min_knight_moves
from solutions.p038_knight_moves_brute import (
    min_knight_moves_unbounded,
)

SOLVERS = [min_knight_moves, min_knight_moves_unbounded]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "x, y, expected",
    [
        (-6, 4, 4),         # book example 1
        (1, 1, 2),          # book example 2: needs a negative square
        (0, -1, 3),         # one square, three moves (edge case)
        (0, 0, 0),          # already there
        (1, 2, 1),          # one move
        (-2, -1, 1),
        (1, 0, 3),
        (2, 0, 2),
        (2, 2, 4),          # the diagonal neighbor-of-neighbor case
        (3, 3, 2),
        (-1, -1, 2),
        (6, 4, 4),          # example 1, folded
    ],
)
def test_examples(solve, x, y, expected):
    assert solve(x, y) == expected


def test_bounded_matches_unbounded_near_origin():
    # Every target in a 51 x 51 square: the margin of 2 must be enough.
    for x in range(-25, 26):
        for y in range(-25, 26):
            assert (min_knight_moves(x, y)
                    == min_knight_moves_unbounded(x, y)), (x, y)


def test_symmetry_and_random_far_targets():
    rng = random.Random(1197)
    for _ in range(40):
        x, y = rng.randint(-60, 60), rng.randint(-60, 60)
        want = min_knight_moves_unbounded(x, y)
        for sx in (1, -1):
            for sy in (1, -1):
                assert min_knight_moves(sx * x, sy * y) == want
        assert min_knight_moves(y, x) == want   # swap axes too


def test_largest_targets_are_fast():
    start = time.perf_counter()
    assert min_knight_moves(500, 500) == 334
    assert min_knight_moves(-500, 0) == 250
    assert min_knight_moves(1, -500) == 251
    assert time.perf_counter() - start < 5
