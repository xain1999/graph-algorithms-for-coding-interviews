import copy
import random

import networkx as nx
import pytest

from solutions.p056_redundant_connection import (
    find_redundant_connection,
)
from solutions.p056_redundant_connection_brute import (
    find_redundant_connection_brute,
)

SOLVERS = [find_redundant_connection, find_redundant_connection_brute]

EXAMPLE_1 = [[2, 5], [1, 3], [5, 4], [3, 5], [4, 1], [6, 3]]
EXAMPLE_2 = [[1, 4], [4, 2], [2, 1], [3, 5], [5, 1]]
EXAMPLE_3 = [[5, 3], [3, 1], [1, 2], [2, 4], [4, 5]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "edges, expected",
    [
        (EXAMPLE_1, [4, 1]),                # book example 1
        (EXAMPLE_2, [2, 1]),                # book example 2
        (EXAMPLE_3, [4, 5]),                # one loop, not in book
        ([[1, 2], [2, 3], [3, 1]], [3, 1]),  # smallest input
        ([[3, 1], [2, 3], [1, 2]], [1, 2]),
    ],
)
def test_examples(solve, edges, expected):
    assert solve(edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = copy.deepcopy(EXAMPLE_1)
    solve(edges)
    assert edges == EXAMPLE_1


def last_cycle_edge(edges):
    """Reference answer: the last edge whose removal leaves a tree."""
    n = len(edges)
    for i in range(n - 1, -1, -1):
        g = nx.Graph()
        g.add_nodes_from(range(1, n + 1))
        g.add_edges_from(edges[:i] + edges[i + 1:])
        if nx.is_tree(g):
            return edges[i]
    raise AssertionError("input is not a tree plus one edge")


def random_input(rng, n):
    labels = list(range(1, n + 1))
    rng.shuffle(labels)
    edges = [[labels[rng.randrange(v)], labels[v]] for v in range(1, n)]
    present = {frozenset(e) for e in edges}
    while True:
        u, v = rng.sample(labels, 2)
        if frozenset((u, v)) not in present:
            break
    edges.append([u, v])
    rng.shuffle(edges)
    return [e if rng.random() < 0.5 else e[::-1] for e in edges]


def test_random_inputs_agree_with_networkx():
    rng = random.Random(684)
    for _ in range(500):
        edges = random_input(rng, rng.randint(3, 12))
        expected = last_cycle_edge(edges)
        assert find_redundant_connection(edges) == expected
        assert find_redundant_connection_brute(edges) == expected


def test_large_input_is_fast():
    n = 50_000
    ring = [[i, i + 1] for i in range(1, n)] + [[n, 1]]
    assert find_redundant_connection(ring) == [n, 1]
    rng = random.Random(6840)
    edges = random_input(rng, n)
    answer = find_redundant_connection(edges)
    assert answer in edges
