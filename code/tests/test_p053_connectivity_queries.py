import copy
import random

import pytest

from solutions.p053_connectivity_queries import connectivity_queries
from solutions.p053_connectivity_queries_brute import (
    connectivity_queries_brute,
)

SOLVERS = [connectivity_queries, connectivity_queries_brute]

EXAMPLE_1 = [
    ("link", 3, 1), ("link", 4, 6), ("ask", 1, 6), ("link", 0, 3),
    ("link", 6, 2), ("link", 2, 0), ("ask", 1, 6), ("ask", 5, 0),
]
EXAMPLE_2 = [
    ("ask", 0, 1), ("link", 1, 0), ("ask", 0, 1), ("link", 0, 1),
    ("ask", 2, 2), ("ask", 2, 0),
]
EXAMPLE_3 = [("link", 0, 1), ("link", 1, 2), ("link", 2, 3),
             ("link", 3, 4), ("ask", 4, 0)]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, ops, expected",
    [
        (7, EXAMPLE_1, [False, True, False]),      # book example 1
        (3, EXAMPLE_2, [False, True, True, False]),  # book example 2
        (5, EXAMPLE_3, [True]),                    # a chain (not in book)
        (1, [("ask", 0, 0)], [True]),              # smallest input
        (4, [("link", 0, 1)], []),                 # no questions
        (4, [("ask", 0, 3), ("link", 0, 3), ("ask", 3, 0)],
         [False, True]),                           # answer changes
        (6, [("link", 0, 1), ("link", 2, 3), ("link", 4, 5),
             ("ask", 1, 2), ("ask", 3, 4), ("link", 1, 2),
             ("ask", 0, 3), ("ask", 0, 5)],
         [False, False, True, False]),
    ],
)
def test_examples(solve, n, ops, expected):
    assert solve(n, ops) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    ops = copy.deepcopy(EXAMPLE_1)
    solve(7, ops)
    assert ops == EXAMPLE_1


def test_random_operations_agree_with_brute_force():
    rng = random.Random(53)
    for _ in range(500):
        n = rng.randint(1, 12)
        ops = [(rng.choice(("link", "ask", "ask")),
                rng.randrange(n), rng.randrange(n))
               for _ in range(rng.randint(0, 30))]
        assert (connectivity_queries(n, ops)
                == connectivity_queries_brute(n, ops))


def test_large_input_is_fast():
    n = 100_000
    ops = []
    for i in range(n - 1):              # one long chain 0-1-...-(n-1)
        ops.append(("link", i + 1, i))
        ops.append(("ask", 0, i + 1))
    ops.append(("ask", n - 1, 0))       # 199,999 operations in all
    answers = connectivity_queries(n, ops)
    assert len(answers) == n and all(answers)
    # two separate chains of evens and odds: never connected
    ops = [("link", i, i + 2) for i in range(n - 2)]
    ops += [("ask", i, i + 1) for i in range(0, n - 1, 2)]
    assert not any(connectivity_queries(n, ops))
