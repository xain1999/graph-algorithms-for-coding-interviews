import random
import time

import pytest

from solutions.p061_most_stones import remove_stones
from solutions.p061_most_stones_brute import remove_stones_brute

SOLVERS = [remove_stones, remove_stones_brute]

EXAMPLE_1 = [[0, 0], [2, 5], [4, 1], [0, 3], [1, 4], [2, 3], [3, 2],
             [4, 4], [2, 0]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "stones, expected",
    [
        (EXAMPLE_1, 6),                          # book example 1
        ([[1, 1], [3, 4], [6, 2], [0, 7]], 0),   # book example 2
        ([[5, 0], [5, 3], [8, 3], [8, 6], [2, 6], [2, 9]], 5),  # stairs
        ([[0, 0]], 0),                           # a single stone
        ([[0, 1], [1, 0]], 0),                   # diagonal: no link
        ([[0, 0], [0, 1]], 1),
        ([[3, 3], [3, 0], [0, 3]], 2),           # star around (3, 3)
        ([[i, j] for i in range(3) for j in range(3)], 8),  # full 3x3
        ([[1, 0], [0, 1]], 0),
        ([[0, 0], [0, 10**9], [10**9, 10**9]], 2),  # huge coordinates
    ],
)
def test_examples(solve, stones, expected):
    assert solve(stones) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    stones = [s[:] for s in EXAMPLE_1]
    solve(stones)
    assert stones == EXAMPLE_1


def test_row_and_column_keys_never_collide():
    # Row 2 and column 2 are different lines: these stones share
    # neither, so nothing can be removed.
    assert remove_stones([[2, 0], [0, 2]]) == 0
    assert remove_stones([[0, 0], [1, 1], [2, 2], [3, 3]]) == 0


def test_random_layouts_agree_with_brute_force():
    rng = random.Random(947)
    for _ in range(1500):
        rows, cols = rng.randint(1, 7), rng.randint(1, 7)
        cells = [[r, c] for r in range(rows) for c in range(cols)]
        stones = rng.sample(cells, rng.randint(1, len(cells)))
        assert remove_stones(stones) == remove_stones_brute(stones)


def test_removal_count_is_achievable():
    # Simulate: repeatedly remove a stone that still shares a line,
    # choosing leaves of a DFS tree first, and check the count.
    rng = random.Random(61)
    for _ in range(300):
        cells = [[r, c] for r in range(6) for c in range(6)]
        stones = rng.sample(cells, rng.randint(1, 20))
        left = {tuple(s) for s in stones}
        removed = 0
        changed = True
        while changed:
            changed = False
            for s in sorted(left):
                if any(o != s and (o[0] == s[0] or o[1] == s[1])
                       for o in left):
                    # removing s must not cut its group apart
                    rest = left - {s}
                    if _groups(rest) == _groups(left):
                        left = rest
                        removed += 1
                        changed = True
                        break
        assert removed == remove_stones(stones)


def _groups(stones):
    return len(stones) - remove_stones_brute([list(s) for s in stones])


def test_large_input_is_fast():
    rng = random.Random(5)
    cells = set()
    while len(cells) < 20_000:
        cells.add((rng.randrange(10**9), rng.randrange(300)))
    stones = [list(c) for c in cells]
    start = time.perf_counter()
    answer = remove_stones(stones)
    assert time.perf_counter() - start < 1.0
    # 300 columns, rows almost never repeat: each column is a group
    assert answer == len(stones) - len({c for _, c in cells})
