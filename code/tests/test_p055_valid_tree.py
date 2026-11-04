import copy
import random

import networkx as nx
import pytest

from solutions.p055_valid_tree import valid_tree
from solutions.p055_valid_tree_dfs import valid_tree_dfs

SOLVERS = [valid_tree, valid_tree_dfs]

EXAMPLE_1 = [[0, 3], [3, 5], [1, 3], [4, 1], [2, 4]]
EXAMPLE_2 = [[0, 3], [3, 5], [1, 3], [4, 1], [5, 1]]
EXAMPLE_3 = [[2, 0], [0, 4], [4, 2], [1, 3], [3, 2], [1, 4]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (6, EXAMPLE_1, True),               # book example 1
        (6, EXAMPLE_2, False),              # book example 2
        (5, EXAMPLE_3, False),              # 6 edges, not in book
        (1, [], True),                      # a single node is a tree
        (2, [], False),                     # two lonely nodes
        (2, [[1, 0]], True),
        (3, [[0, 1]], False),               # a forest, too few edges
        (3, [[0, 0], [1, 2]], False),       # self-loop, n-1 edges
        (3, [[0, 1], [1, 0]], False),       # repeated edge
        (4, [[0, 1], [0, 2], [0, 3]], True),  # a star
    ],
)
def test_examples(solve, n, edges, expected):
    assert solve(n, edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = copy.deepcopy(EXAMPLE_2)
    solve(6, edges)
    assert edges == EXAMPLE_2


def test_random_graphs_agree_with_networkx():
    rng = random.Random(261)
    for _ in range(2000):
        n = rng.randint(1, 9)
        m = rng.choice((n - 2, n - 1, n - 1, n - 1, n))
        edges = [[rng.randrange(n), rng.randrange(n)]
                 for _ in range(max(m, 0))]
        g = nx.MultiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        expected = nx.is_tree(g)
        assert valid_tree(n, edges) == expected
        assert valid_tree_dfs(n, edges) == expected


def test_random_trees_are_accepted():
    rng = random.Random(2610)
    for _ in range(300):
        n = rng.randint(1, 30)
        edges = [[rng.randrange(v), v] for v in range(1, n)]
        rng.shuffle(edges)
        assert valid_tree(n, edges) and valid_tree_dfs(n, edges)


def test_large_graph_is_fast():
    n = 100_000
    path = [[i, i + 1] for i in range(n - 1)]
    assert valid_tree(n, path) and valid_tree_dfs(n, path)
    # n-1 edges, but a cycle at the very end leaves node n-1 alone
    almost = path[:-1] + [[0, n - 2]]
    assert not valid_tree(n, almost)
    assert not valid_tree_dfs(n, almost)
