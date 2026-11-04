import copy
import random

import networkx as nx
import pytest

from solutions.p054_count_components import count_components
from solutions.p054_count_components_dfs import count_components_dfs

SOLVERS = [count_components, count_components_dfs]

EXAMPLE_1 = [[0, 5], [5, 2], [6, 1], [2, 0], [3, 7]]
EXAMPLE_2 = [[2, 4], [4, 0], [0, 2], [1, 5], [3, 5], [5, 4]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (8, EXAMPLE_1, 4),                  # book example 1
        (6, EXAMPLE_2, 1),                  # book example 2
        (3, [], 3),                         # book example 3
        (1, [], 1),                         # smallest input
        (2, [[0, 1]], 1),
        (5, [[0, 1], [1, 0], [0, 1]], 4),   # repeated edges
        (4, [[0, 1], [1, 2], [2, 0], [0, 2]], 2),
    ],
)
def test_examples(solve, n, edges, expected):
    assert solve(n, edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = copy.deepcopy(EXAMPLE_1)
    solve(8, edges)
    assert edges == EXAMPLE_1


def test_random_graphs_agree_with_networkx():
    rng = random.Random(323)
    for _ in range(1000):
        n = rng.randint(1, 15)
        edges = []
        for _ in range(rng.randint(0, 2 * n)):
            u, v = rng.sample(range(n), 2) if n > 1 else (0, 0)
            if u != v:
                edges.append([u, v])
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        expected = nx.number_connected_components(g)
        assert count_components(n, edges) == expected
        assert count_components_dfs(n, edges) == expected


def test_large_graph_is_fast():
    n = 100_000
    chain = [[i, i + 1] for i in range(n - 1)]
    assert count_components(n, chain) == 1
    assert count_components_dfs(n, chain) == 1
    # 200,000 edges: evens chain, odds chain, each edge twice
    edges = [[i, i + 2] for i in range(n - 2)] * 2
    assert count_components(n, edges[:200_000]) == 2
