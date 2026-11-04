import random
import time

import networkx as nx
import pytest

from solutions.p091_sum_distances import sum_of_distances
from solutions.p091_sum_distances_brute import sum_of_distances_brute

SOLVERS = [sum_of_distances, sum_of_distances_brute]

EXAMPLE_1 = [[0, 1], [0, 2], [1, 3], [1, 4], [3, 5], [3, 6], [2, 7]]
EXAMPLE_2 = [[2, 0], [0, 3], [3, 1]]


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
    "n, edges, expected",
    [
        (8, EXAMPLE_1, [14, 12, 18, 14, 18, 20, 20, 24]),  # example 1
        (4, EXAMPLE_2, [4, 6, 6, 4]),                       # example 2
        (1, [], [0]),                                       # one node
        (2, [[0, 1]], [1, 1]),
        (4, [[1, 0], [1, 2], [1, 3]], [5, 3, 5, 5]),        # star
        (5, [[4, 3], [3, 2], [2, 1], [1, 0]], [10, 7, 6, 7, 10]),
    ],
)
def test_examples(solve, n, edges, expected):
    assert solve(n, edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EXAMPLE_1]
    solve(8, edges)
    assert edges == EXAMPLE_1


def test_random_trees_agree_with_networkx():
    rng = random.Random(834)
    for _ in range(800):
        n = rng.randint(1, 15)
        edges = random_tree(rng, n)
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        lengths = dict(nx.all_pairs_shortest_path_length(g))
        expected = [sum(lengths[v].values()) for v in range(n)]
        for solve in SOLVERS:
            assert solve(n, edges) == expected, edges


def test_large_trees_are_fast():
    n = 10**5
    path = [[i, i + 1] for i in range(n - 1)]       # deepest possible
    start = time.perf_counter()
    answer = sum_of_distances(n, path)
    assert answer[0] == answer[-1] == n * (n - 1) // 2
    tree = random_tree(random.Random(5), n)
    sample = sum_of_distances(n, tree)
    assert len(sample) == n and min(sample) > 0
    assert time.perf_counter() - start < 5.0
