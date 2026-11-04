import random

import networkx as nx
import pytest

from solutions.p007_undirected_cycle import has_cycle
from solutions.p007_undirected_cycle_alt import has_cycle_recursive
from solutions.p007_undirected_cycle_count import (
    has_cycle_by_counting,
)

SOLVERS = [has_cycle, has_cycle_recursive, has_cycle_by_counting]

EXAMPLE_1 = [[0, 1], [0, 2], [3, 4], [4, 5], [5, 6], [6, 4]]
EXAMPLE_2 = EXAMPLE_1[:-1]
EXAMPLE_3 = [[0, 3], [3, 1], [1, 4], [4, 0]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (7, EXAMPLE_1, True),               # book example 1
        (7, EXAMPLE_2, False),              # book example 2 (forest)
        (5, EXAMPLE_3, True),               # 4-cycle, isolated node 2
        (2, [[0, 1]], False),               # one edge
        (1, [], False),                     # smallest input
        (5, [], False),                     # no edges at all
        (3, [[0, 1], [1, 2], [2, 0]], True),            # triangle
        (4, [[0, 1], [1, 2], [2, 3], [3, 0]], True),    # square
        (4, [[0, 1], [0, 2], [0, 3]], False),           # star
        (7, [[0, 1], [2, 3], [4, 5], [6, 4], [5, 6]], True),
    ],
)
def test_examples(solve, n, edges, expected):
    assert solve(n, edges) == expected


@pytest.mark.parametrize("solve", SOLVERS)
def test_does_not_mutate_input(solve):
    edges = [e[:] for e in EXAMPLE_1]
    solve(7, edges)
    assert edges == EXAMPLE_1


def test_random_graphs_agree_with_networkx():
    rng = random.Random(7)
    for _ in range(2000):
        n = rng.randint(1, 10)
        p = rng.choice((0.1, 0.2, 0.35))
        edges = [[u, v] for u in range(n) for v in range(u + 1, n)
                 if rng.random() < p]
        rng.shuffle(edges)
        edges = [e if rng.random() < 0.5 else e[::-1] for e in edges]
        g = nx.Graph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        expected = not nx.is_forest(g)
        for solve in SOLVERS:
            assert solve(n, edges) == expected, (n, edges)


def test_random_trees_have_no_cycle_until_one_edge_is_added():
    rng = random.Random(70)
    for _ in range(300):
        n = rng.randint(3, 30)
        edges = [[rng.randrange(v), v] for v in range(1, n)]
        assert not has_cycle(n, edges)
        present = {tuple(sorted(e)) for e in edges}
        extra = [[u, v] for u in range(n) for v in range(u + 1, n)
                 if (u, v) not in present]
        edges.insert(rng.randrange(len(edges) + 1), rng.choice(extra))
        assert has_cycle(n, edges)
        assert has_cycle_by_counting(n, edges)


def test_deep_graph_is_fast_and_iterative():
    n = 100_000
    path = [[i, i + 1] for i in range(n - 1)]       # far too deep
    assert has_cycle(n, path) is False              # for recursion
    assert has_cycle(n, path + [[n - 1, 0]]) is True
    assert has_cycle_by_counting(n, path) is False


@pytest.mark.parametrize(
    "n, edges",
    [
        (1, [[0, 0]]),                      # a loop: length one
        (2, [[0, 1], [1, 0]]),              # a pair: length two
        (3, [[1, 2], [0, 1], [2, 1]]),
    ],
)
def test_multigraph_variant_is_reported(n, edges):
    # Outside the constraints; the book says the code reports these.
    assert has_cycle(n, edges)
