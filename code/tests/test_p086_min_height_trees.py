import random
import time

import networkx as nx
import pytest

from solutions.p086_min_height_trees import find_min_height_trees
from solutions.p086_min_height_trees_brute import (
    find_min_height_trees_brute)

SOLVERS = [find_min_height_trees, find_min_height_trees_brute]

EXAMPLE_1 = [[5, 7], [0, 2], [8, 9], [2, 1], [7, 4], [3, 2], [2, 6],
             [4, 8], [2, 5]]
EXAMPLE_2 = [[6, 0], [0, 3], [3, 1], [1, 4], [4, 2], [3, 5]]


def random_tree(n, rng):
    """Random labelled tree: node i joins an earlier node."""
    perm = list(range(n))
    rng.shuffle(perm)
    edges = [[perm[i], perm[rng.randrange(i)]] for i in range(1, n)]
    rng.shuffle(edges)
    return edges


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (10, EXAMPLE_1, [7]),                  # book example 1
        (7, EXAMPLE_2, [1, 3]),                # book example 2
        (1, [], [0]),                          # a lone node
        (2, [[1, 0]], [0, 1]),                 # one edge: both ends
        (3, [[0, 1], [1, 2]], [1]),
        (5, [[3, 0], [3, 1], [3, 2], [3, 4]], [3]),   # star
        (6, [[i, i + 1] for i in range(5)], [2, 3]),  # even path
    ],
)
def test_examples(solve, n, edges, expected):
    assert sorted(solve(n, edges)) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [pair[:] for pair in EXAMPLE_1]
    solve(10, edges)
    assert edges == EXAMPLE_1


def test_random_trees_agree_with_brute_and_networkx():
    rng = random.Random(310)
    for _ in range(500):
        n = rng.randint(1, 40)
        edges = random_tree(n, rng)
        got = find_min_height_trees(n, edges)
        assert got == find_min_height_trees_brute(n, edges)
        graph = nx.Graph()
        graph.add_nodes_from(range(n))
        graph.add_edges_from(edges)
        assert got == sorted(nx.center(graph))
        assert len(got) in (1, 2)
        if len(got) == 2:
            assert graph.has_edge(*got)   # two centers are adjacent


def test_large_trees_are_fast():
    n = 30_000
    rng = random.Random(3)
    start = time.perf_counter()
    path = [[i, i + 1] for i in range(n - 1)]
    assert find_min_height_trees(n, path) == [14_999, 15_000]
    find_min_height_trees(n, random_tree(n, rng))
    assert time.perf_counter() - start < 2.0
