import random

import networkx as nx
import pytest

from solutions.p006_most_connected_node import most_connected_node
from solutions.p006_most_connected_node_alt import (
    most_connected_node_adj,
)
from solutions.p006_most_connected_node_brute import (
    most_connected_node_brute,
)

SOLVERS = [most_connected_node, most_connected_node_adj,
           most_connected_node_brute]

EXAMPLE_1 = [[5, 0], [1, 2], [2, 3], [3, 1], [3, 4], [3, 5]]
EXAMPLE_2 = [[4, 2], [4, 0], [2, 1], [2, 3], [4, 3]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (6, EXAMPLE_1, 3),                  # book example 1
        (5, EXAMPLE_2, 2),                  # book example 2 (tie 2/4)
        (4, [], 0),                         # no edges
        (1, [], 0),                         # smallest input
        (2, [[1, 0]], 0),                   # tie between both ends
        (5, [[3, 4]], 3),                   # isolated 0, 1, 2
        (5, [[4, 0], [4, 1], [4, 2], [4, 3]], 4),   # star
        (6, [[5, 4], [3, 2], [1, 0]], 0),   # all degree 1
    ],
)
def test_examples(solve, n, edges, expected):
    assert solve(n, edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EXAMPLE_1]
    solve(6, edges)
    assert edges == EXAMPLE_1


def test_random_graphs_agree_with_networkx():
    rng = random.Random(6)
    for _ in range(1000):
        n = rng.randint(1, 12)
        edges = [[u, v] for u in range(n) for v in range(u + 1, n)
                 if rng.random() < 0.3]
        rng.shuffle(edges)
        edges = [e if rng.random() < 0.5 else e[::-1] for e in edges]
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        top = max(d for _, d in g.degree())
        expected = min(v for v, d in g.degree() if d == top)
        for solve in SOLVERS:
            assert solve(n, edges) == expected


def test_large_graph_is_fast():
    n = 100_000
    edges = [[i, i + 1] for i in range(n - 1)]      # a long path
    edges += [[n - 1, i] for i in range(0, n - 2, 2)]
    assert most_connected_node(n, edges) == n - 1
    assert most_connected_node_adj(n, edges) == n - 1


def test_multigraph_degree_counts_parallel_edges_and_loops():
    # Outside the constraints: (0,1) twice and a loop at 0 give
    # node 0 degree 4, more than node 2's three distinct neighbors.
    edges = [[0, 1], [0, 1], [0, 0], [2, 3], [2, 4], [2, 1]]
    assert most_connected_node(5, edges) == 0
