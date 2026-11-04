import random
import time

import pytest

from solutions.p013_inform_employees import time_to_inform
from solutions.p013_inform_employees_alt import time_to_inform_memo
from solutions.p013_inform_employees_brute import time_to_inform_brute

SOLVERS = [time_to_inform, time_to_inform_brute, time_to_inform_memo]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, head, manager, inform_time, expected",
    [
        # book example 1: the heavy path 2-1-5 beats the deep path
        (8, 2, [2, 2, -1, 0, 0, 1, 3, 3],
         [4, 6, 4, 1, 0, 0, 0, 0], 10),
        # book example 2: two middle managers, the slow one decides
        (6, 0, [-1, 0, 0, 1, 1, 2], [2, 3, 6, 0, 0, 0], 8),
        # a flat team: everyone hears at once
        (5, 3, [3, 3, 3, -1, 3], [0, 0, 0, 7, 0], 7),
        # former book example 3: a chain of command 3 -> 2 -> 1 -> 0
        (4, 3, [1, 2, 3, -1], [0, 5, 1, 2], 8),
        (1, 0, [-1], [0], 0),                   # head works alone
        (2, 1, [1, -1], [0, 9], 9),
        (3, 0, [-1, 0, 0], [0, 0, 0], 0),       # instant messages
        # a leaf's own inform time never matters
        (3, 0, [-1, 0, 1], [1, 1, 50], 2),
    ],
)
def test_examples(solve, n, head, manager, inform_time, expected):
    assert solve(n, head, manager, inform_time) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    manager = [2, 2, -1, 0, 0, 1, 3, 3]
    inform_time = [4, 6, 4, 1, 0, 0, 0, 0]
    solve(8, 2, manager, inform_time)
    assert manager == [2, 2, -1, 0, 0, 1, 3, 3]
    assert inform_time == [4, 6, 4, 1, 0, 0, 0, 0]


def random_company(rng: random.Random, n: int):
    order = list(range(n))
    rng.shuffle(order)                  # order[0] is the head
    manager = [-1] * n
    for i in range(1, n):
        manager[order[i]] = order[rng.randrange(i)]
    has_reports = set(manager)
    inform_time = [rng.randint(0, 9) if e in has_reports else 0
                   for e in range(n)]
    return order[0], manager, inform_time


def test_random_trees_agree():
    rng = random.Random(1376)
    for _ in range(1000):
        n = rng.randint(1, 12)
        head, manager, inform_time = random_company(rng, n)
        expected = time_to_inform_brute(n, head, manager, inform_time)
        assert time_to_inform(n, head, manager, inform_time) == expected
        assert time_to_inform_memo(
            n, head, manager, inform_time) == expected


@pytest.mark.parametrize("solve", [time_to_inform, time_to_inform_memo])
def test_long_chain_is_fast(solve):
    # A chain of 10^5 employees: recursion would overflow, and the
    # brute force would climb about 5 * 10^9 steps.
    n = 100_000
    manager = [i - 1 for i in range(n)]
    inform_time = [1] * (n - 1) + [0]
    start = time.perf_counter()
    assert solve(n, 0, manager, inform_time) == n - 1
    assert time.perf_counter() - start < 2.0


def test_wide_random_tree_is_fast():
    rng = random.Random(7)
    n = 100_000
    head, manager, inform_time = random_company(rng, n)
    expected = time_to_inform_memo(n, head, manager, inform_time)
    assert time_to_inform(n, head, manager, inform_time) == expected
