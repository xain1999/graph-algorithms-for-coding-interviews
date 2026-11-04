import random

import networkx as nx
import pytest

from solutions.p009_number_of_provinces import count_provinces
from solutions.p009_number_of_provinces_brute import (
    count_provinces_brute,
)

SOLVERS = [count_provinces, count_provinces_brute]

EXAMPLE_1 = [
    [1, 0, 0, 1, 0, 0],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 1, 0, 0, 0],
    [1, 0, 0, 1, 0, 1],
    [0, 1, 0, 0, 1, 0],
    [0, 0, 0, 1, 0, 1],
]
EXAMPLE_2 = [
    [1, 1, 0, 0],
    [1, 1, 1, 0],
    [0, 1, 1, 1],
    [0, 0, 1, 1],
]


def matrix_from_edges(n, edges):
    m = [[0] * n for _ in range(n)]
    for i in range(n):
        m[i][i] = 1
    for u, v in edges:
        m[u][v] = m[v][u] = 1
    return m


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "matrix, expected",
    [
        (EXAMPLE_1, 3),                     # book example 1
        (EXAMPLE_2, 1),                     # book example 2
        ([[1, 0], [0, 1]], 2),              # no roads
        ([[1]], 1),                         # smallest input
        ([[1] * 5 for _ in range(5)], 1),   # everyone linked
        (matrix_from_edges(5, [[0, 4]]), 4),
        (matrix_from_edges(6, [[0, 5], [5, 1], [2, 4]]), 3),
    ],
)
def test_examples(solve, matrix, expected):
    assert solve(matrix) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    matrix = [row[:] for row in EXAMPLE_1]
    solve(matrix)
    assert matrix == EXAMPLE_1


def test_random_matrices_agree_with_networkx():
    rng = random.Random(547)
    for _ in range(1000):
        n = rng.randint(1, 12)
        p = rng.choice((0.05, 0.15, 0.3))
        edges = [[u, v] for u in range(n) for v in range(u + 1, n)
                 if rng.random() < p]
        matrix = matrix_from_edges(n, edges)
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        expected = nx.number_connected_components(g)
        assert count_provinces(matrix) == expected
        assert count_provinces_brute(matrix) == expected


def test_large_matrix_is_fast():
    n = 500
    # cities i and i + 2 are linked: evens and odds form two chains
    edges = [[i, i + 2] for i in range(n - 2)]
    assert count_provinces(matrix_from_edges(n, edges)) == 2
    assert count_provinces(matrix_from_edges(n, [])) == n
