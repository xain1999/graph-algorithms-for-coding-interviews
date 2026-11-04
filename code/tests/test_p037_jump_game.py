import random
import sys

import networkx as nx
import pytest

from solutions.p037_jump_game import can_reach
from solutions.p037_jump_game_rec import can_reach_recursive

SOLVERS = [can_reach, can_reach_recursive]

EXAMPLE = [3, 3, 4, 2, 0, 2, 4, 5]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "arr, start, expected",
    [
        (EXAMPLE, 0, True),             # book example 1: 0 -> 3 -> 1 -> 4
        (EXAMPLE, 7, False),            # book example 2: stuck in {7,2,6}
        ([2, 5, 0, 1], 2, True),        # start on a zero (edge case)
        ([0], 0, True),                 # smallest input
        ([1], 0, False),                # both jumps leave the array
        ([1, 1], 0, False),             # 0 <-> 1 forever, no zero
        ([3, 0, 9, 1], 3, False),       # zero exists, never reached
        ([1, 1, 1, 1, 0], 0, True),     # one step at a time
        ([0, 1, 1, 1, 1], 4, True),     # backwards only
        ([2, 7, 2, 7, 0], 0, True),     # big values just fall off
    ],
)
def test_examples(solve, arr, start, expected):
    assert solve(arr, start) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    arr = EXAMPLE[:]
    solve(arr, 7)
    assert arr == EXAMPLE


def test_random_arrays_agree_with_networkx():
    rng = random.Random(1306)
    for _ in range(2000):
        n = rng.randint(1, 12)
        arr = [rng.randint(0, n + 1) if rng.random() < 0.85 else 0
               for _ in range(n)]
        if rng.random() < 0.3:
            arr = [v or 1 for v in arr]         # often no zero at all
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        for i, v in enumerate(arr):
            for j in (i + v, i - v):
                if 0 <= j < n:
                    g.add_edge(i, j)
        start = rng.randrange(n)
        reach = nx.descendants(g, start) | {start}
        expected = any(arr[i] == 0 for i in reach)
        for solve in SOLVERS:
            assert solve(arr, start) == expected


def test_long_chain_is_fast_and_iterative():
    n = 100_000
    arr = [1] * (n - 1) + [0]               # n - 1 jumps in a row
    assert can_reach(arr, 0) is True
    arr[-1] = 2                              # no zero anywhere now
    assert can_reach(arr, 0) is False


def test_recursive_version_fails_on_long_chain():
    arr = [1] * (sys.getrecursionlimit() * 2) + [0]
    with pytest.raises(RecursionError):
        can_reach_recursive(arr, 0)
