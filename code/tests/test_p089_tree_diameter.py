import random
import time

import networkx as nx
import pytest

from solutions.p089_tree_diameter import tree_diameter
from solutions.p089_tree_diameter_brute import tree_diameter_brute
from solutions.p089_tree_diameter_arms import tree_diameter_arms

SOLVERS = [tree_diameter, tree_diameter_brute, tree_diameter_arms]

EXAMPLE_1 = [[3, 4], [4, 5], [5, 6], [4, 7], [7, 8], [8, 9], [3, 0],
             [0, 1], [7, 2]]
EXAMPLE_2 = [[3, 0], [3, 1], [3, 2], [3, 4]]


def random_tree(rng, n):
    edges = []
    for v in range(1, n):
        u = rng.randrange(v)
        edges.append([u, v] if rng.random() < 0.5 else [v, u])
    labels = list(range(n))
    rng.shuffle(labels)
    edges = [[labels[a], labels[b]] for a, b in edges]
    rng.shuffle(edges)
    return edges


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "edges, expected",
    [
        (EXAMPLE_1, 6),                     # book example 1
        (EXAMPLE_2, 2),                     # book example 2 (star)
        ([], 0),                            # a single node
        ([[1, 0]], 1),
        ([[0, 1], [1, 2], [2, 3], [3, 4]], 4),   # a path
        ([[4, 3], [3, 2], [2, 1], [1, 0]], 4),   # path, reversed labels
        ([[0, 1], [0, 2], [0, 3], [3, 4], [4, 5]], 4),
    ],
)
def test_examples(solve, edges, expected):
    assert solve(edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EXAMPLE_1]
    solve(edges)
    assert edges == EXAMPLE_1


def test_random_trees_agree_with_networkx():
    rng = random.Random(1245)
    for _ in range(1500):
        n = rng.randint(1, 14)
        edges = random_tree(rng, n)
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        expected = nx.diameter(g)
        for solve in SOLVERS:
            assert solve(edges) == expected, edges


@pytest.mark.parametrize("solve", [tree_diameter, tree_diameter_arms])
def test_large_trees_are_fast(solve):
    n = 10**5
    path = [[i, i + 1] for i in range(n - 1)]       # deepest possible
    rng = random.Random(7)
    start = time.perf_counter()
    assert solve(path) == n - 1
    tree = random_tree(rng, n)
    assert solve(tree) == tree_diameter(tree)
    assert time.perf_counter() - start < 5.0
