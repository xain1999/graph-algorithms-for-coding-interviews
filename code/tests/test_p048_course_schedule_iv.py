import random
import time

import networkx as nx
import pytest

from solutions.p048_course_schedule_iv import check_if_prerequisite
from solutions.p048_course_schedule_iv_bits import (
    check_if_prerequisite_bits,
)
from solutions.p048_course_schedule_iv_brute import (
    check_if_prerequisite_brute,
)
from solutions.p048_course_schedule_iv_closure import (
    check_if_prerequisite_closure,
)

SOLVERS = [check_if_prerequisite, check_if_prerequisite_bits,
           check_if_prerequisite_brute, check_if_prerequisite_closure]

PREREQS_1 = [[3, 0], [3, 4], [2, 4], [0, 1], [4, 1], [1, 5]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, prereqs, queries, expected",
    [
        # book example 1: indirect prerequisites through two levels
        (6, PREREQS_1, [[3, 5], [2, 0], [5, 3], [2, 1]],
         [True, False, False, True]),
        # book example 2: two separate chains
        (5, [[1, 0], [0, 4], [3, 2]], [[1, 4], [3, 4], [2, 3], [3, 2]],
         [True, False, False, True]),
        # no prerequisites at all (not in book)
        (3, [], [[0, 1], [2, 0]], [False, False]),
        (2, [[0, 1]], [[0, 1], [1, 0]], [True, False]),
        (1, [], [], []),
        # diamond: the same ancestor arrives along two paths
        (4, [[0, 1], [0, 2], [1, 3], [2, 3]], [[0, 3], [1, 2]],
         [True, False]),
        # redundant direct edge next to a longer path
        (3, [[0, 1], [1, 2], [0, 2]], [[0, 2], [2, 0]], [True, False]),
    ],
)
def test_examples(solve, n, prereqs, queries, expected):
    assert solve(n, prereqs, queries) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    prereqs = [p[:] for p in PREREQS_1]
    queries = [[3, 5], [2, 0]]
    solve(6, prereqs, queries)
    assert prereqs == PREREQS_1 and queries == [[3, 5], [2, 0]]


def random_dag(rng: random.Random, n: int, p: float):
    order = list(range(n))
    rng.shuffle(order)
    return [[order[i], order[j]] for i in range(n)
            for j in range(i + 1, n) if rng.random() < p]


def test_random_dags_against_networkx():
    rng = random.Random(1462)
    for _ in range(500):
        n = rng.randint(2, 10)
        prereqs = random_dag(rng, n, rng.choice((0.1, 0.25, 0.5)))
        queries = [[u, v] for u in range(n) for v in range(n)
                   if u != v]
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from(prereqs)
        expected = [nx.has_path(g, u, v) for u, v in queries]
        for solve in SOLVERS:
            assert solve(n, prereqs, queries) == expected


@pytest.mark.parametrize("solve", [check_if_prerequisite,
                                   check_if_prerequisite_bits])
def test_dense_dag_is_fast(solve):
    # 150 courses, every pair ordered: about 11,000 edges.
    n = 150
    prereqs = [[i, j] for i in range(n) for j in range(i + 1, n)]
    queries = [[i, j] for i in range(n) for j in range(n)
               if i != j][:20_000]
    start = time.perf_counter()
    answers = solve(n, prereqs, queries)
    assert answers == [i < j for i, j in queries]
    assert time.perf_counter() - start < 2.0


def test_long_chain_bits():
    n = 150
    prereqs = [[i, i + 1] for i in range(n - 1)]
    assert check_if_prerequisite_bits(n, prereqs, [[0, n - 1]]) == [
        True]
