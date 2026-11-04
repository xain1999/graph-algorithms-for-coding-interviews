import random
import time

import pytest

from solutions.p062_earliest_friends import earliest_all_friends
from solutions.p062_earliest_friends_brute import (
    earliest_all_friends_brute)

SOLVERS = [earliest_all_friends, earliest_all_friends_brute]

EXAMPLE_1 = [[14, 2, 3], [3, 0, 1], [20, 4, 5], [9, 1, 2],
             [27, 0, 3], [31, 3, 4], [40, 1, 5]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, logs, expected",
    [
        (6, EXAMPLE_1, 31),                              # example 1
        (5, [[2, 0, 1], [6, 3, 4], [11, 1, 0], [15, 4, 3]], -1),  # 2
        (3, [[8, 2, 0], [2, 1, 2], [5, 1, 2]], 8),       # unsorted logs
        (2, [[0, 0, 1]], 0),                             # smallest
        (2, [[9, 1, 0], [4, 0, 1]], 4),                  # unsorted
        (3, [[1, 0, 1]], -1),                            # too few logs
        (4, [[5, 0, 1], [5, 2, 3], [5, 1, 2]], 5),       # equal times
        (4, [[1, 0, 1], [2, 0, 1], [3, 1, 0], [4, 2, 3]], -1),
    ],
)
def test_examples(solve, n, logs, expected):
    assert solve(n, logs) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    logs = [log[:] for log in EXAMPLE_1]
    solve(6, logs)
    assert logs == EXAMPLE_1


def test_random_logs_agree_with_brute_force():
    rng = random.Random(1101)
    for _ in range(1500):
        n = rng.randint(2, 8)
        logs = []
        for _ in range(rng.randint(1, 14)):
            a, b = rng.sample(range(n), 2)
            logs.append([rng.randint(0, 20), a, b])
        assert (earliest_all_friends(n, logs)
                == earliest_all_friends_brute(n, logs))


def test_large_input_is_fast():
    rng = random.Random(3)
    n = 100_000
    order = list(range(n))
    rng.shuffle(order)
    # a random spanning chain at times 1..n-1, plus noise after it
    logs = [[i, order[i - 1], order[i]] for i in range(1, n)]
    logs += [[rng.randint(n, 10**9), rng.randrange(n),
              rng.randrange(n)] for _ in range(100_000)]
    rng.shuffle(logs)
    start = time.perf_counter()
    assert earliest_all_friends(n, logs) == n - 1
    assert time.perf_counter() - start < 2.0
