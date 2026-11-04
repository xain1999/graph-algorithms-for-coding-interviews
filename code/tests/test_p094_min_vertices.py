import random
import time

import networkx as nx
import pytest

from solutions.p094_min_vertices import find_smallest_set_of_vertices
from solutions.p094_min_vertices_brute import (
    find_smallest_set_of_vertices_brute,
)

SOLVERS = [find_smallest_set_of_vertices,
           find_smallest_set_of_vertices_brute]

EXAMPLE_1 = [[5, 1], [1, 3], [3, 0], [6, 3], [6, 4], [2, 4], [4, 0]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (7, EXAMPLE_1, [2, 5, 6]),              # book example 1
        (5, [[0, 2], [1, 2], [2, 3]], [0, 1, 4]),   # book example 2
        (1, [], [0]),                           # smallest input
        (3, [], [0, 1, 2]),                     # no edges at all
        (4, [[3, 2], [2, 1], [1, 0]], [3]),     # one chain
        (4, [[0, 1], [0, 2], [0, 3]], [0]),     # one root
        (4, [[1, 0], [2, 0], [3, 0]], [1, 2, 3]),   # one sink
    ],
)
def test_examples(solve, n, edges, expected):
    assert solve(n, edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EXAMPLE_1]
    solve(7, edges)
    assert edges == EXAMPLE_1


def random_dag(rng, n, p):
    order = list(range(n))
    rng.shuffle(order)
    return [[order[i], order[j]] for i in range(n)
            for j in range(i + 1, n) if rng.random() < p]


def test_random_dags_agree_with_brute_force_and_networkx():
    rng = random.Random(1557)
    for _ in range(500):
        n = rng.randint(1, 9)
        edges = random_dag(rng, n, rng.choice((0.1, 0.3, 0.6)))
        answer = find_smallest_set_of_vertices(n, edges)
        assert answer == find_smallest_set_of_vertices_brute(n, edges)
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        reached = set(answer)
        for node in answer:
            reached |= nx.descendants(g, node)
        assert reached == set(range(n))         # it covers everything
        for node in answer:                     # and none is spare
            assert not nx.ancestors(g, node)


def test_large_dag_is_fast():
    n = 200_000
    edges = [[i, i + 1] for i in range(0, n - 1, 2)]    # 100,000 pairs
    edges += [[i, i + 2] for i in range(0, n - 2, 2)]
    start = time.perf_counter()
    answer = find_smallest_set_of_vertices(n, edges)
    assert answer == [0]
    assert time.perf_counter() - start < 1.0
