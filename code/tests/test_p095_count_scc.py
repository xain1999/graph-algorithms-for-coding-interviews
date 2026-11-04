import random
import time

import networkx as nx
import pytest

from solutions.p095_count_scc import count_scc
from solutions.p095_count_scc_brute import count_scc_brute
from solutions.p095_count_scc_tarjan import count_scc_tarjan

SOLVERS = [count_scc, count_scc_tarjan, count_scc_brute]

EXAMPLE_1 = [[4, 5], [5, 6], [6, 4], [6, 3], [3, 0], [0, 1], [1, 2],
             [2, 0], [5, 2]]
CHAIN = [[0, 1], [1, 2], [2, 3], [3, 4]]


@pytest.mark.parametrize("solve", SOLVERS)
@pytest.mark.parametrize(
    "n, edges, expected",
    [
        (7, EXAMPLE_1, 3),                  # book example 1
        (5, CHAIN, 5),                      # book example 2
        (5, CHAIN + [[4, 0]], 1),           # example 2, closed up
        (1, [], 1),                         # smallest input
        (4, [], 4),                         # no edges
        (2, [[0, 1], [1, 0]], 1),
        (3, [[0, 0], [1, 1]], 3),           # self-loops
        (3, [[0, 1], [0, 1], [1, 0]], 2),   # repeated edge
        (6, [[0, 1], [1, 0], [2, 3], [3, 2], [4, 5]], 4),
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
    rng = random.Random(95)
    for _ in range(600):
        n = rng.randint(1, 12)
        m = rng.randint(0, 3 * n)
        edges = [[rng.randrange(n), rng.randrange(n)] for _ in range(m)]
        g = nx.DiGraph()
        g.add_nodes_from(range(n))
        g.add_edges_from(edges)
        expected = nx.number_strongly_connected_components(g)
        for solve in SOLVERS:
            assert solve(n, edges) == expected


@pytest.mark.parametrize("solve", [count_scc, count_scc_tarjan])
def test_long_paths_need_no_recursion(solve):
    n = 100_000
    chain = [[i, i + 1] for i in range(n - 1)]
    rng = random.Random(7)
    extra = [[rng.randrange(n), rng.randrange(n)] for _ in range(n)]
    expected = nx.number_strongly_connected_components(
        nx.DiGraph(chain + extra))
    start = time.perf_counter()
    assert solve(n, chain) == n
    assert solve(n, chain + [[n - 1, 0]]) == 1      # one big cycle
    assert solve(n, chain + extra) == expected
    assert time.perf_counter() - start < 2.0
