import random
import time

import networkx as nx
import pytest

from solutions.p085_root_the_tree import root_tree
from solutions.p085_root_the_tree_rec import root_tree_rec

SOLVERS = [root_tree, root_tree_rec]

EDGES = [[4, 5], [0, 4], [5, 2], [7, 2], [1, 4], [6, 2], [3, 6]]


def random_tree(n, rng):
    """Random labelled tree: node i joins an earlier node."""
    perm = list(range(n))
    rng.shuffle(perm)
    edges = []
    for i in range(1, n):
        a, b = perm[i], perm[rng.randrange(i)]
        edges.append([a, b] if rng.random() < 0.5 else [b, a])
    rng.shuffle(edges)
    return edges


def expected_parents(n, edges, root):
    graph = nx.Graph()
    graph.add_nodes_from(range(n))
    graph.add_edges_from(edges)
    parent = [-1] * n
    for par, child in nx.bfs_edges(graph, root):
        parent[child] = par
    return parent


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, root, expected",
    [
        (8, EDGES, 5, [4, 4, 5, 6, 5, -1, 2, 2]),   # book example 1
        (8, EDGES, 3, [4, 4, 6, -1, 5, 2, 3, 2]),   # book example 2
        (1, [], 0, [-1]),                           # a lone node
        (2, [[1, 0]], 0, [-1, 0]),
        (2, [[1, 0]], 1, [1, -1]),
        (4, [[0, 1], [0, 2], [0, 3]], 2, [2, 0, -1, 0]),   # star
        (4, [[3, 2], [2, 1], [1, 0]], 0, [-1, 0, 1, 2]),   # path
    ],
)
def test_examples(solve, n, edges, root, expected):
    assert solve(n, edges, root) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [pair[:] for pair in EDGES]
    solve(8, edges, 5)
    assert edges == EDGES


def test_random_trees_agree_with_networkx():
    rng = random.Random(85)
    for _ in range(500):
        n = rng.randint(1, 30)
        edges = random_tree(n, rng)
        root = rng.randrange(n)
        want = expected_parents(n, edges, root)
        assert root_tree(n, edges, root) == want
        assert root_tree_rec(n, edges, root) == want


def test_rerooting_flips_only_the_path():
    rng = random.Random(851)
    for _ in range(200):
        n = rng.randint(2, 25)
        edges = random_tree(n, rng)
        old, new = rng.sample(range(n), 2)
        before = root_tree(n, edges, old)
        after = root_tree(n, edges, new)
        path, x = [new], new
        while x != old:
            x = before[x]
            path.append(x)
        changed = {v for v in range(n) if before[v] != after[v]}
        assert changed == set(path)


def test_long_path_is_fast_and_iterative():
    n = 300_000
    edges = [[i, i + 1] for i in range(n - 1)]
    start = time.perf_counter()
    parent = root_tree(n, edges, 0)
    assert parent[n - 1] == n - 2 and parent[0] == -1
    assert time.perf_counter() - start < 2.0
