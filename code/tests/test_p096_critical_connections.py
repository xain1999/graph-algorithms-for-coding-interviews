import random
import time

import networkx as nx
import pytest

from solutions.p096_critical_connections import critical_connections
from solutions.p096_critical_connections_brute import (
    critical_connections_brute,
)

SOLVERS = [critical_connections, critical_connections_brute]

EXAMPLE_1 = [[0, 1], [1, 2], [2, 0], [0, 3], [3, 4], [4, 5], [5, 3],
             [5, 6], [6, 7]]
EXAMPLE_2 = [[0, 1], [1, 2], [2, 3], [3, 4], [4, 0], [1, 3]]


def as_set(bridges):
    return {frozenset(edge) for edge in bridges}


def test_book_example_1_exact_order():
    assert critical_connections(8, EXAMPLE_1) == \
        [[6, 7], [5, 6], [0, 3]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, connections, expected",
    [
        (8, EXAMPLE_1, [[0, 3], [5, 6], [6, 7]]),   # book example 1
        (5, EXAMPLE_2, []),                         # book example 2
        (2, [[0, 1]], [[0, 1]]),                    # smallest input
        (4, [[0, 3], [1, 3], [2, 3]], [[0, 3], [1, 3], [2, 3]]),
        (3, [[0, 1], [1, 2], [2, 0]], []),
        # two triangles sharing node 2: a cut node, but no bridge
        (5, [[0, 1], [1, 2], [2, 0], [2, 3], [3, 4], [4, 2]], []),
        # start node 0 hangs off a cycle
        (4, [[0, 1], [1, 2], [2, 3], [3, 1]], [[0, 1]]),
    ],
)
def test_examples(solve, n, connections, expected):
    assert as_set(solve(n, connections)) == as_set(expected)


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    connections = [e[:] for e in EXAMPLE_1]
    solve(8, connections)
    assert connections == EXAMPLE_1


def random_connected(rng, n, extra):
    edges = set()
    for v in range(1, n):                 # random spanning tree
        u = rng.randrange(v)
        edges.add((u, v))
    for _ in range(extra):
        u, v = rng.sample(range(n), 2)
        if (u, v) not in edges and (v, u) not in edges:
            edges.add((u, v))
    labels = list(range(n))
    rng.shuffle(labels)
    return [[labels[u], labels[v]] for u, v in edges]


def test_random_graphs_agree_with_networkx_and_brute():
    rng = random.Random(1192)
    for _ in range(400):
        n = rng.randint(2, 12)
        edges = random_connected(rng, n, rng.randint(0, n))
        expected = as_set(nx.bridges(nx.Graph(edges)))
        assert as_set(critical_connections(n, edges)) == expected
        assert as_set(critical_connections_brute(n, edges)) == expected


def test_long_path_needs_no_recursion():
    n = 200_000
    path = [[i, i + 1] for i in range(n - 1)]
    ring = path + [[n - 1, 0]]
    start = time.perf_counter()
    assert len(critical_connections(n, path)) == n - 1
    assert critical_connections(n, ring) == []
    assert time.perf_counter() - start < 10.0    # a loaded machine


def test_large_random_graph_matches_networkx():
    rng = random.Random(96)
    n = 50_000
    edges = random_connected(rng, n, n // 2)
    expected = as_set(nx.bridges(nx.Graph(edges)))
    assert as_set(critical_connections(n, edges)) == expected
