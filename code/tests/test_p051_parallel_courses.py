import random
import time

import networkx as nx
import pytest

from solutions.p051_parallel_courses import minimum_time
from solutions.p051_parallel_courses_brute import minimum_time_brute
from solutions.p051_parallel_courses_memo import minimum_time_memo

SOLVERS = [minimum_time, minimum_time_brute, minimum_time_memo]

EXAMPLE_1 = (7, [[1, 3], [2, 3], [2, 4], [3, 5], [4, 6], [5, 7],
                 [6, 7], [3, 6]], [4, 2, 3, 6, 2, 5, 1])


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, relations, time_, expected",
    [
        (*EXAMPLE_1, 14),                    # book example 1
        (4, [], [3, 9, 1, 5], 9),            # book example 2
        (3, [[3, 1], [1, 2]], [2, 4, 7], 13),  # chain, not in book
        (1, [], [8], 8),
        (2, [[1, 2]], [1, 1], 2),
        (2, [[2, 1]], [5, 1], 6),            # numbering != order
        # diamond: both branches run in parallel
        (4, [[1, 2], [1, 3], [2, 4], [3, 4]], [1, 5, 2, 1], 7),
        # duplicate-free chain plus a shortcut edge
        (3, [[1, 2], [2, 3], [1, 3]], [2, 2, 2], 6),
        # two separate projects: the slower one decides
        (4, [[1, 2], [3, 4]], [1, 1, 4, 4], 8),
    ],
)
def test_examples(solve, n, relations, time_, expected):
    assert solve(n, relations, time_) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    n, relations, time_ = EXAMPLE_1
    rel_copy = [r[:] for r in relations]
    time_copy = time_[:]
    solve(n, relations, time_)
    assert relations == rel_copy and time_ == time_copy


def random_dag(rng: random.Random, n: int, p: float):
    order = list(range(1, n + 1))
    rng.shuffle(order)                  # a hidden topological order
    relations = [[order[i], order[j]]
                 for i in range(n) for j in range(i + 1, n)
                 if rng.random() < p]
    rng.shuffle(relations)
    time_ = [rng.randint(1, 9) for _ in range(n)]
    return relations, time_


def networkx_answer(n, relations, time_):
    """Longest path with node weights, via an edge-weighted DAG."""
    g = nx.DiGraph()
    for c in range(1, n + 1):           # c -> c' carries time[c]
        g.add_edge(("in", c), ("out", c), weight=time_[c - 1])
    for a, b in relations:
        g.add_edge(("out", a), ("in", b), weight=0)
    return nx.dag_longest_path_length(g)


def test_random_dags_agree():
    rng = random.Random(2050)
    for _ in range(500):
        n = rng.randint(1, 9)
        relations, time_ = random_dag(rng, n, rng.random())
        expected = minimum_time_brute(n, relations, time_)
        assert minimum_time(n, relations, time_) == expected
        assert minimum_time_memo(n, relations, time_) == expected
        assert networkx_answer(n, relations, time_) == expected


def test_layered_graph_is_fast():
    # 2 courses per layer, every course needs both of the layer
    # before: 2^k paths, which the plain recursion would all walk.
    k = 40_000
    n = 2 * k
    relations = [[a + 1, b + 1] for i in range(k - 1)
                 for a in (2 * i, 2 * i + 1)
                 for b in (2 * i + 2, 2 * i + 3)]
    time_ = [1, 2] * k
    start = time.perf_counter()
    assert minimum_time(n, relations, time_) == 2 * k
    assert time.perf_counter() - start < 2.0


def test_long_chain_is_fast():
    # A chain of 10^5 courses: too deep for the recursive versions.
    n = 100_000
    relations = [[i, i + 1] for i in range(1, n)]
    time_ = [1000] * n
    assert minimum_time(n, relations, time_) == 1000 * n
